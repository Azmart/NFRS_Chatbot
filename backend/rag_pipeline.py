# backend/rag_pipeline.py

from embedding import E5Embedder
from vector_store import ChromaVectorStore
from llm_client import LLMClient

class RAGPipeline:
    def __init__(self):
        self.embedder = E5Embedder()
        self.vector_store = ChromaVectorStore()
        self.llm = LLMClient()

    def build_prompt(self, query, results):
        context_blocks = []
        for i in range(len(results["documents"][0])):
            doc = results["documents"][0][i]
            meta = results["metadatas"][0][i]
            context_blocks.append(f"[Source: {meta['source']} - Page {meta['page']}]\n{doc}")

        context_text = "\n\n---\n\n".join(context_blocks)
        prompt = f"""You are a financial assistant for Nepal reporting standards.

Use the following context to answer the user's question. Always cite the source document and page like this: [Source: filename - Page X].

Context:
{context_text}

Question:
{query}

Answer:"""
        return prompt

    def run(self, query: str, top_k: int = 5):
        print(f"🔍 Embedding query: {query}")
        query_embedding = self.embedder.embed_query(query)

        print("📂 Searching ChromaDB...")
        results = self.vector_store.similarity_search(query_embedding, k=top_k)

        print("📦 Building prompt and calling LLM...")
        prompt = self.build_prompt(query, results)
        answer = self.llm.generate_answer(prompt)

        return {
            "answer": answer,
            "references": results["metadatas"][0]  # List of sources used
        }