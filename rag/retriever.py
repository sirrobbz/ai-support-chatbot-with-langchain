import os
from rag.vectorstore import load_vectorstore

def get_retriever():
    db = load_vectorstore()

    if db is None:
        print("⚠️ Vector DB not found. Run: python rag/ingest.py")
        return None

    return db.as_retriever(search_kwargs={"k": 3})
