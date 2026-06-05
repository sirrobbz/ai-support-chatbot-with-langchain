import os
import sys
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader

from config.settings import Config


def load_docs():
    docs = []

    for file in os.listdir(Config.DOCS_PATH):
        file_path = os.path.join(Config.DOCS_PATH, file)

        # ----------------------
        # TXT FILES
        # ----------------------
        if file.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read().strip()
                if text:
                    docs.append(Document(
                        page_content=text,
                        metadata={"source": file}
                    ))

        # ----------------------
        # PDF FILES
        # ----------------------
        elif file.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            pdf_pages = loader.load()  # returns page-wise documents

            for page in pdf_pages:
                if page.page_content.strip():
                    docs.append(Document(
                        page_content=page.page_content,
                        metadata={
                            "source": file,
                            "page": page.metadata.get("page", None)
                        }
                    ))

    return docs


def build_vectorstore():
    raw_docs = load_docs()

    print(f"📄 Loaded documents: {len(raw_docs)}")

    if len(raw_docs) == 0:
        raise ValueError("No documents found in data/docs/")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(raw_docs)

    print(f"✂️ Total chunks: {len(chunks)}")

    if len(chunks) == 0:
        raise ValueError("No chunks created from documents")

    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    if os.path.exists(Config.VECTOR_DB_PATH):
        shutil.rmtree(Config.VECTOR_DB_PATH)

    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(Config.VECTOR_DB_PATH)

    print("✅ Vector DB built successfully (PDF + TXT supported)")
