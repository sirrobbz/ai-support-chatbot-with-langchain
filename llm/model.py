from langchain_ollama import ChatOllama
from config.settings import Config

def get_llm():
    return ChatOllama(
        model=Config.MODEL_NAME,
        temperature=Config.TEMPERATURE
    )
