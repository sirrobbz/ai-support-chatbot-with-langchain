# AI Support Chatbot

An AI-powered Support Chatbot built with Flask, LangChain, Ollama, FAISS, and RAG (Retrieval-Augmented Generation).

## Features

- AI chatbot using Ollama models
- Retrieval-Augmented Generation (RAG)
- FAISS vector database for semantic search
- Supports PDF and TXT documents
- Session-based chat memory
- Flask REST API backend
- Simple web UI

## Project Structure

ai-support-chatbot/
├── app.py
├── config.py
├── requirements.txt
├── routes/
├── services/
├── rag/
├── data/docs/
├── templates/
├── static/
└── vector_db/

## Setup Instructions

### 1. Clone repo
git clone https://github.com/sirrobbz/ai-support-chatbot-with-langchain.git
cd ai-support-chatbot-with-langchain

### 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

### 3. Install dependencies
pip install -r requirements.txt

## Install Ollama

https://ollama.com

ollama pull llama3.2:3b

## Build Vector DB

python rag/ingest.py

## Run App

python app.py

## API

POST /chat

{
  "message": "Hello",
  "session_id": "user1"
}

## License

MIT
