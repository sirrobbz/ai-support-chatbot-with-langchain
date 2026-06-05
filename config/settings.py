import os

class Config:
    MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2:3b")
    TEMPERATURE = float(os.getenv("TEMPERATURE", 0.8))
    VECTOR_DB_PATH = "vector_db"
    DOCS_PATH = "data/docs"
