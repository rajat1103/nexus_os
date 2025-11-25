import uuid
import chromadb
from chromadb.utils import embedding_functions
from app.core.database import get_vector_client

def store_memory(content, category):
    client = get_vector_client()
    
    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    collection = client.get_or_create_collection(
        name="nexus_primary_memory",
        embedding_function=embedding_function
    )
    
    record_id = str(uuid.uuid4())
    
    collection.add(
        documents=[content],
        metadatas=[{"category": category}],
        ids=[record_id]
    )
    
    return {"id": record_id, "status": "stored"}

def retrieve_memory(query, n_results=5):
    client = get_vector_client()
    
    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    collection = client.get_or_create_collection(
        name="nexus_primary_memory",
        embedding_function=embedding_function
    )
    
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    return results