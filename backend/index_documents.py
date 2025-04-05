# backend/index_documents.py

from pdf_loader import load_pdfs_recursive
from embedding import E5Embedder
from vector_store import ChromaVectorStore

def run_indexing():
    # Load all PDF chunks
    print("📄 Loading PDF chunks...")
    docs = load_pdfs_recursive("data/documents")

    # Initialize embedder
    embedder = E5Embedder()
    print(f"🔍 Embedding {len(docs)} chunks...")
    embeddings = [embedder.embed_document_text(doc["content"]) for doc in docs]

    # Store in Chroma
    print("🧠 Storing in ChromaDB...")
    vector_db = ChromaVectorStore()
    vector_db.add_documents(docs, embeddings)

    print("✅ Indexing complete!")

if __name__ == "__main__":
    run_indexing()