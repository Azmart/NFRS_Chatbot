# backend/main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_pipeline import RAGPipeline

app = FastAPI(title="NFRS/IFRS RAG API")

# Allow requests from Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in prod
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = RAGPipeline()

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
def query_financial_knowledge(req: QueryRequest):
    result = pipeline.run(req.question)
    return {
        "answer": result["answer"],
        "sources": result["references"]
    }