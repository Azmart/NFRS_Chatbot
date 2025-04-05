# backend/test_rag.py

from rag_pipeline import RAGPipeline

if __name__ == "__main__":
    pipeline = RAGPipeline()
    question = input("🧠 Ask your financial reporting question: ")
    result = pipeline.run(question)

    print("\n💬 Answer:")
    print(result["answer"])
    print("\n📎 Sources used:")
    for ref in result["references"]:
        print(f"- {ref['source']} (Page {ref['page']})")