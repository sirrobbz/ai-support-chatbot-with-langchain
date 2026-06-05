from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from config.settings import Config
import os

embeddings = OllamaEmbeddings(model="nomic-embed-text")

def load_vectorstore():
    if os.path.exists(Config.VECTOR_DB_PATH):
        return FAISS.load_local(
            Config.VECTOR_DB_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )
    return None
