# backend/vector_store.py

import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from typing import List, Dict

class ChromaVectorStore:
    def __init__(self, persist_path="data/chroma_db", collection_name="nfrs_ifrs_docs"):
        import chromadb
        self.client = chromadb.PersistentClient(path=persist_path)
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add_documents(self, docs: List[Dict], embeddings: List, batch_size: int = 5000):
        """Add documents with precomputed embeddings in batches."""
        total = len(docs)
        for start in range(0, total, batch_size):
            end = min(start + batch_size, total)
            batch_docs = docs[start:end]
            batch_embeddings = embeddings[start:end]
            ids = [f"doc_{i}" for i in range(start, end)]
            texts = [doc["content"] for doc in batch_docs]
            metadatas = [doc["metadata"] for doc in batch_docs]

            print(f"📦 Adding batch {start} → {end} to Chroma...")
            self.collection.add(documents=texts, embeddings=batch_embeddings, metadatas=metadatas, ids=ids)

    def similarity_search(self, query_embedding, k=5):
        """Return top-k most similar documents to the query"""
        results = self.collection.query(query_embeddings=[query_embedding], n_results=k)
        return results