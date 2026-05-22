# LangChain Chatbot

A simple and smart AI chatbot web app that talks to you using LangChain. It automatically uses OpenAI when available, and smoothly falls back to a local Llama3 model via Ollama if the API key is missing or fails. 

Built with LangChain, FastAPI, and a single HTML frontend. Perfect for quick testing or personal use.


# What it does

Type anything — from casual chat to complex questions. The bot handles conversation naturally. It intelligently switches between cloud (OpenAI) and local (Ollama) models without you doing anything.

- Works great with OpenAI for high-quality answers
- Falls back to Ollama automatically when needed (fully local & free)
- Real-time streaming responses
- Clean, responsive UI


# Project File Structure

langchain-chatbot/
├── backend.py          # FastAPI + LangChain logic
├── index.html          # Single-file frontend
├── requirements.txt
├── .env



# Tech Stack

- Backend: FastAPI, LangChain, OpenAI, Ollama
- Frontend: Plain HTML + Tailwind CSS + vanilla JavaScript
- LLM: OpenAI (default) with automatic fallback to Llama3 via Ollama


# How to run whole project

1. Clone the repository
 bash:
 
   git clone https://github.com/ketanbagewadi/langchain-chatbot.git
   cd langchain-chatbot


# Create virtual environment & install dependenciesBashpython -m venv .venv

source .venv/bin/activate

.venv\Scripts\activate                 # On Windows

pip install -r requirements.txt


# Configure your .env

Add your OPENAI_API_KEY if you want to use OpenAI.

Leave it blank to run fully on Ollama.

# Setup Ollama (optional - for local mode)Bash# Install Ollama from https://ollama.com

ollama pull llama3
ollama serve                # verify


# Start the backend Bashuvicorn backend 

app --reload --port 8000

# Open the frontend

Just open index.html in your browser (double-click the file).

The chat interface will connect automatically. You'll see which model (OpenAI or Ollama) is being used at the top.
Features

Automatic OpenAI → Ollama fallback
Streaming responses (tokens appear in real-time)
Clean and responsive UI
Conversation history in the current tab
Easy to modify and extend

# Notes

The .env file is gitignored — never commit your API key.
If OpenAI fails or no key is set, it automatically switches to local Llama3.
Refreshing the page clears the chat history.
