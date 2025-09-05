from langchain_astradb import AstraDBVectorStore
from langchain_community.embeddings import JinaEmbeddings

from src.rag_component import COLLECTION_NAME, EMBEDDING_MODEL

class AstraDB:
    def __init__(
            self, collection_name:str=COLLECTION_NAME, embedding_model:str=EMBEDDING_MODEL
        ):
        jina_embeddings = JinaEmbeddings(
            model_name=embedding_model
        )
        self.vector_store = AstraDBVectorStore(
            collection_name=collection_name,
            embedding=jina_embeddings
        )

    
    def rag_retrieve(self, query:str, k:int=4):
        """
        Retrieves relevant documents from the AstraDB vector store based on the input query.

        Args:
            query (str): The input query string.
            k (int): The number of top relevant documents to retrieve. Default is 4.

        Returns:
            list: A list of retrieved documents.
        """
        docs = self.vector_store.similarity_search(query, k=k)
        return docs
    
    def ingestion(self, data:list, type:str='document'):
        """
        Ingests a list of texts into the AstraDB vector store.

        Args:
            texts (list[dict]): A list of texts to be ingested.
            ids (list[str], optional): A list of IDs corresponding to the texts. Defaults to None.

        Returns:
            None
        """
        if type == 'document':
            self.vector_store.add_documents(data)
        elif type == 'text':
            self.vector_store.add_texts(data)
        else:
            raise ValueError("Invalid type. Must be 'document' or 'text'.")