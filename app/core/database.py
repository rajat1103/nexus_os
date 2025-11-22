import chromadb
from chromadb.config import Settings
import os

def get_vector_client():
    base_path = os.getcwd()
    persist_path = os.path.join(base_path, "nexus_memory")
    
    client = chromadb.PersistentClient(path=persist_path)
    return client