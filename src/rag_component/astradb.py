from langchain_astradb import AstraDBVectorStore
from langchain_community.embeddings import JinaEmbeddings

from src.rag_component import COLLECTION_NAME, EMBEDDING_MODEL

from logger.custom_logger import CustomLogger
from exception.custom_exception import CustomException

import sys

logging = CustomLogger().get_logger(__file__)

class AstraDB:
    def __init__(
            self, collection_name:str=COLLECTION_NAME, embedding_model:str=EMBEDDING_MODEL
        ):
        try:
            jina_embeddings = JinaEmbeddings(
                model_name=embedding_model
            )
            self.vector_store = AstraDBVectorStore(
                collection_name=collection_name,
                embedding=jina_embeddings
            )

            logging.info(f"AstraDB initialized with collection: {collection_name} and embedding model: {embedding_model}")
        except Exception as e:
            app_exc = CustomException(e, sys)
            logging.error("Failed to initialize AstraDBVectorStore")
            logging.error(app_exc)

    def rag_retrieve(self, query:str, k:int=4):
        """
        Retrieves relevant documents from the AstraDB vector store based on the input query.

        Args:
            query (str): The input query string.
            k (int): The number of top relevant documents to retrieve. Default is 4.

        Returns:
            list: A list of retrieved documents.
        """
        try:
            docs = self.vector_store.similarity_search(query, k=k)

            return docs
        
        except Exception as e:
            app_exc = CustomException(e, sys)
            logging.error("Failed to retrieve documents from AstraDBVectorStore")
            logging.error(app_exc)
    
    def ingestion(self, data:list, type:str='document'):
        """
        Ingests a list of texts into the AstraDB vector store.

        Args:
            texts (list[dict]): A list of texts to be ingested.
            ids (list[str], optional): A list of IDs corresponding to the texts. Defaults to None.

        Returns:
            None
        """
        try:
            if type == 'document':
                logging.info(f"Ingesting {len(data)} documents into AstraDBVectorStore")
                self.vector_store.add_documents(data)
            elif type == 'text':
                logging.info(f"Ingesting {len(data)} texts into AstraDBVectorStore")
                self.vector_store.add_texts(data)
            else:
                logging.error("Invalid type. Must be 'document' or 'text'.")
                raise ValueError("Invalid type. Must be 'document' or 'text'.")
            
        except Exception as e:
            app_exc = CustomException(e, sys)
            logging.error("Failed to ingest data into AstraDBVectorStore")
            logging.error(app_exc)