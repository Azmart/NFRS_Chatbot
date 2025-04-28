# backend/rag_pipeline.py

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class RAGPipeline:
    def __init__(self):
        """Initialize the RAG pipeline with LM Studio connection."""
        self.api_base = os.getenv("LM_STUDIO_API_BASE", "http://localhost:1234/v1")
        
    def run(self, query: str) -> dict:
        """
        Run the query through the local LLM.
        
        Args:
            query: The user's question about NFRS/IFRS
            
        Returns:
            Dict containing answer and reference sources
        """
        try:
            # Call local LLM through LM Studio
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers={"Content-Type": "application/json"},
                json={
                    "messages": [
                        {"role": "system", "content": "You are a financial chatbot that is knowledgeable about Nepal Financial Reporting Standard (NFRS), and IFRS as well. Your goal is to understand users question and assist them with answers. Keep the conversation short and concise with accurate information. No need to describe in too much details. "},
                        {"role": "user", "content": query}
                    ],
                    "temperature": 0.7,
                    "stream": False
                }
            )
            
            if response.status_code != 200:
                raise Exception(f"LM Studio API error: {response.text}")
            
            answer = response.json()["choices"][0]["message"]["content"]
            
            # For now, return dummy references until we implement proper RAG
            references = [
                {"source": "NFRS 1", "page": 1},
                {"source": "IFRS Guidelines", "page": 15}
            ]
            
            return {
                "answer": answer,
                "references": references
            }
            
        except Exception as e:
            raise Exception(f"Error in RAG pipeline: {str(e)}")