from src.utils import load_config
from dotenv import load_dotenv
from langchain_astradb import AstraDBVectorStore
from langchain_community.embeddings import JinaEmbeddings
import os

config = load_config('config.yaml')

load_dotenv()

COLLECTION_NAME = config['astradb']['collection_name']
EMBEDDING_MODEL = config['astradb']['embedding_model']

# os.environ['ASTRA_DB_API_ENDPOINT'] = userdata.get('ASTRA_DB_API_ENDPOINT')
# os.environ['ASTRA_DB_APPLICATION_TOKEN'] = userdata.get('ASTRA_DB_APPLICATION_TOKEN')
# os.environ['JINA_API_KEY'] = userdata.get('JINA_API_KEY')