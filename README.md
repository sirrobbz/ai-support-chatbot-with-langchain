# AI Support Chatbot

An AI-powered Support Chatbot built with Flask, LangChain, Ollama, FAISS, and RAG (Retrieval-Augmented Generation). The application allows users to ask questions based on a custom knowledge base consisting of PDF and TXT documents, while maintaining conversation history for a more natural chat experience.

## Features

🤖 AI-powered chatbot using local Ollama models
📚 Retrieval-Augmented Generation (RAG)
🔍 Semantic search using FAISS vector database
📄 Supports PDF and TXT document ingestion
💬 Conversation memory with session-based chat history
🌐 REST API backend built with Flask
🎨 Simple web-based chat interface
🔒 Runs locally without sending data to external AI providers

## Project Structure

ai-support-chatbot/
├── app.py
├── config.py
├── requirements.txt
├── routes/
    └── chat_routes.py
├── services/
    ├── llm_service.py
    ├── rag_service.py
    └── memory_service.py
├── rag/
    ├── ingest.py
    ├── retriever.py
    └── vectorstore.py
├── data/
    └── docs/
    ├── document1.pdf
    └── document2.txt
├── templates/
    └── index.html
├── static/
    ├── css/
    └── js/
└── vector_db/
    ├── index.faiss
    └── index.pkl

## Requirements

Python 3.10+
Ollama installed
Linux, macOS, or Windows

## Installation

### 1. Clone the Repository

git clone https://github.com/yourusername/ai-support-chatbot.git
cd ai-support-chatbot

### 2. Create a Virtual Environment
python -m venv venv

## Activate it:

Linux/macOS
source venv/bin/activate


### 3. Install Dependencies
pip install -r requirements.txt
Install Ollama

## Download and install Ollama:

curl -fsSL https://ollama.com/install.sh | sh

## Verify installation:

ollama --version

## Pull a model:

ollama pull llama3.2:3b

## You may also use:

ollama pull llama3
ollama pull mistral
ollama pull qwen3

## Configure the Application

### Update your configuration values in config/settings.py

Example:

class Config:
    OLLAMA_MODEL = "llama3.2:3b"
    VECTOR_DB_PATH = "vector_db"

### Add Knowledge Base Documents

Place your documents inside:

data/docs/

### Supported formats:

PDF
TXT

Example:

data/docs/
├── employee_handbook.pdf
├── product_manual.pdf
└── faq.txt

## Build the Vector Database

Before starting the chatbot, generate embeddings and create the FAISS index.

python rag/ingest.py

If it fails, below command:

cat > /srv/ai-support-chatbot/routes/chat_routes.py << 'EOF'
from flask import Blueprint, request, jsonify
from services.rag_service import build_rag_chain

chat_bp = Blueprint("chat", __name__)

_chain = None

def get_chain():
    global _chain
    if _chain is None:
        _chain = build_rag_chain()
    return _chain

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.json

    message = data.get("message")
    session_id = data.get("session_id", "default")

    if not message:
        return jsonify({"error": "message required"}), 400

    try:
        chain = get_chain()
    except Exception as e:
        return jsonify({"error": f"Chain initialization failed: {str(e)}"}), 500

    response = chain.invoke(
        {"input": message},
        config={"configurable": {"session_id": session_id}}
    )

    print("DEBUG response type:", type(response))
    print("DEBUG response value:", response)

    # Handle both AIMessage and plain string outputs
    if hasattr(response, "content"):
        answer = response.content
    elif isinstance(response, str):
        answer = response
    elif isinstance(response, dict):
        answer = response.get("output") or response.get("answer") or response.get("text") or str(response)
    else:
        answer = str(response)

    return jsonify({
        "response": answer,
        "session_id": session_id
    })
EOF


## Expected output:

Loaded documents: 10
Total chunks: 150
Vector DB built successfully

## The command creates:

vector_db/
├── index.faiss
└── index.pkl

## Run Ollama

### Start the Ollama service:

ollama serve

### Verify the model is available:

ollama list

## Start the Application
python app.py

## Expected output:

Running on http://127.0.0.1:5000

## Access the Chatbot

Open your browser:

http://localhost:5000


## How It Works
Documents are loaded from data/docs.
Text is split into chunks.
Ollama embeddings are generated.
FAISS stores the embeddings.
User questions are matched against relevant chunks.
Relevant context is sent to the LLM.
The chatbot generates a response grounded in your documents.

## Troubleshooting
Vector DB Not Found

### Error:

Vector DB not found. Run: python rag/ingest.py

### Solution:

python rag/ingest.py

### Verify the database exists:

ls vector_db

Expected:

index.faiss
index.pkl

## Ollama Connection Issues

### Verify Ollama is running:

ollama serve

### Check available models:

ollama list

## Port Already in Use

### Find the process:

sudo lsof -i :5000

### Kill it:

kill -9 PID

Or run Flask on another port:

flask run --port 5001
