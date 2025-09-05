from src.rag_component.astradb import AstraDB

def retriever(query: str, k: int = 4) -> list:
    vector_db = AstraDB()
    docs = vector_db.rag_retrieve(query, k)

    formatted_docs = "/n/n".join(
        f"**Metadata**: {doc.metadata}\n**Content**: {doc.page_content}"
        for doc in docs
    )

    return formatted_docs