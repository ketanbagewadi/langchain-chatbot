from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama

import os
import json
import time
import http.server
import socketserver
import threading
import webbrowser
from http import HTTPStatus
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")

PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Please respond to the user queries clearly and concisely."),
    ("user", "Question:{question}")
])

OUTPUT_PARSER = StrOutputParser()


def try_openai(question: str):
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None, "No OpenAI API key found"
    try:
        llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=api_key, request_timeout=20)
        chain = PROMPT | llm | OUTPUT_PARSER
        result = chain.invoke({"question": question})
        if not result or not result.strip():
            return None, "OpenAI returned empty response"
        return result, None
    except Exception as e:
        return None, str(e)


def try_ollama(question: str):
    try:
        llm = Ollama(model="llama3")
        chain = PROMPT | llm | OUTPUT_PARSER
        result = chain.invoke({"question": question})
        if not result or not result.strip():
            return None, "Ollama returned empty response"
        return result, None
    except Exception as e:
        return None, str(e)


def get_answer(question: str):
    result, err = try_openai(question)
    if result:
        return {"answer": result, "model": "GPT-4o-mini (OpenAI)", "fallback": False}
    openai_err = err

    result, err = try_ollama(question)
    if result:
        return {"answer": result, "model": "Llama3 (Ollama – local)", "fallback": True, "reason": openai_err}

    return {
        "answer": None,
        "error": f"Both models failed.\nOpenAI: {openai_err}\nOllama: {err}"
    }


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # silence default logging

    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        with open("index.html", "rb") as f:
            self.wfile.write(f.read())

    def do_POST(self):
        if self.path != "/ask":
            self.send_response(HTTPStatus.NOT_FOUND)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        data = json.loads(body)
        question = data.get("question", "").strip()

        result = get_answer(question)

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())


PORT = 7860


def open_browser():
    time.sleep(0.8)
    webbrowser.open(f"http://localhost:{PORT}")


if __name__ == "__main__":
    print(f"\n  NeuralQuery running at  http://localhost:{PORT}\n")
    threading.Thread(target=open_browser, daemon=True).start()
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
