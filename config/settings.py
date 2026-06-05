import os

class Config:
    MODEL_NAME = os.getenv("MODEL_NAME", "gemma2:2b")
    TEMPERATURE = float(os.getenv("TEMPERATURE", 0.8))
    VECTOR_DB_PATH = "vector_db"
    DOCS_PATH = "data/docs"
