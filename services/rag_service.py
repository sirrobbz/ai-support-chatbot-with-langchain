from llm.model import get_llm
from llm.prompt import get_rag_prompt
from rag.retriever import get_retriever
from memory.memory_store import add_memory

llm = get_llm()
prompt = get_rag_prompt()

def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])


def build_rag_chain():

    retriever = get_retriever()

    if retriever is None:
        raise RuntimeError("Vector DB not found. Run: python rag/ingest.py")

    def retrieve_and_format(input_dict):
        # Use invoke() — get_relevant_documents() is deprecated
        docs = retriever.invoke(input_dict["input"])
        # Pass through ALL keys so chat_history reaches the prompt's MessagesPlaceholder
        return {
            **input_dict,
            "context": format_docs(docs),
        }

    chain = retrieve_and_format | prompt | llm

    return add_memory(chain)
