from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json
from typing import List, Dict
import chromadb
import tiktoken

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./data/chroma_db")
collection = chroma_client.get_or_create_collection(name="document_qa")

class Query(BaseModel):
    question: str

def is_greeting(text: str) -> bool:
    """Check if the input is a greeting."""
    greetings = {'hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening'}
    return text.lower().strip() in greetings

def format_citation(metadata: dict) -> str:
    """Format the citation string based on metadata."""
    citation = f"in {metadata['document_name']}"
    if metadata['section']:
        citation += f", Section {metadata['section']}"
    if metadata['point']:
        citation += f", Point {metadata['point']}"
    if metadata['article']:
        citation += f", Article {metadata['article']}"
    return citation

def count_tokens(text: str) -> int:
    """Approximate token count using tiktoken"""
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")  # This is approximate
    return len(encoding.encode(text))

def truncate_context(contexts: List[str], max_tokens: int = 3000) -> str:
    """Truncate contexts to fit within token limit"""
    total_text = ""
    for context in contexts:
        if count_tokens(total_text + context) > max_tokens:
            break
        total_text += context + "\n\n"
    return total_text.strip()

@app.post("/ask")
async def ask_question(query: Query):
    try:
        # Handle greetings separately
        if is_greeting(query.question):
            return {
                "answer": "Hello! I'm your NFRS/IFRS assistant. I can help you with questions about financial reporting standards. What would you like to know?"
            }
        
        # Get relevant context
        results = collection.query(
            query_texts=[query.question],
            n_results=2,
            include=['metadatas', 'documents']
        )
        
        if not results['documents'] or not results['documents'][0]:
            return {
                "answer": "I couldn't find any relevant information in the documents. Could you please rephrase your question?"
            }

        # Prepare context with citations
        contexts = []
        for i in range(len(results['documents'][0])):
            context = results['documents'][0][i]
            metadata = results['metadatas'][0][i]
            citation = f"Source: {metadata['document_name']}"
            if metadata.get('section'): citation += f", Section {metadata['section']}"
            if metadata.get('point'): citation += f", Point {metadata['point']}"
            contexts.append(f"Context {i+1} ({citation}):\n{context}")
        
        # Truncate context to fit within token limit
        combined_context = truncate_context(contexts)
        
        # Simplified prompt
        prompt = f"""Please answer the question based on this context from NFRS/IFRS documents.

Context:
{combined_context}

Question: {query.question}

Provide a clear answer with specific references to the source documents."""

        try:
            # Increased timeout to 60 seconds
            response = requests.post(
                "http://localhost:1234/v1/chat/completions",
                headers={"Content-Type": "application/json"},
                json={
                    "model": "gemma-3-12b-it",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a financial regulations expert. Provide clear, accurate answers about NFRS and IFRS standards."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 500,  # Set a specific limit instead of -1
                    "stream": False
                },
                timeout=60  # Increased timeout to 60 seconds
            )
            
            if response.status_code != 200:
                print(f"LM Studio API Error: Status {response.status_code}")
                print(f"Response content: {response.text}")
                return {
                    "answer": "I apologize, but I'm having trouble processing your question. Please try again in a moment."
                }
            
            try:
                response_data = response.json()
                if 'choices' in response_data and len(response_data['choices']) > 0:
                    if 'message' in response_data['choices'][0]:
                        answer = response_data['choices'][0]['message']['content'].strip()
                        # Check if the answer is incomplete
                        if answer.endswith((':', ',', '-', 'by')):
                            answer += " [Response was cut off. Please try asking a more specific question.]"
                        return {"answer": answer}
                    else:
                        answer = response_data['choices'][0].get('text', '').strip()
                        if answer:
                            return {"answer": answer}
                
                return {
                    "answer": "I apologize, but I couldn't generate a proper response. Please try asking your question differently."
                }
                
            except json.JSONDecodeError as e:
                print(f"JSON Parse Error: {e}")
                print(f"Raw response: {response.text}")
                return {
                    "answer": "I apologize, but there was an error processing the response. Please try again."
                }
                
        except requests.exceptions.Timeout:
            print("Request timed out after 60 seconds")
            return {
                "answer": "I apologize, but the response is taking longer than expected. Please try again or ask a more specific question."
            }
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            return {
                "answer": "I apologize, but I'm having trouble connecting to the language model. Please ensure LM Studio is running and try again."
            }
            
    except Exception as e:
        print(f"General Error: {type(e).__name__}: {str(e)}")
        return {
            "answer": "I apologize, but an error occurred while processing your question. Please try again."
        }
