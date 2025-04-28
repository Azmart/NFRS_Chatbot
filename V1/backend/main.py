# backend/main.py

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.rag_pipeline import RAGPipeline
from backend.models import SessionLocal, Session as ChatSession, Conversation
from sqlalchemy.orm import Session as DBSession
from backend.translation import TranslationService
import uuid
import json
import logging

app = FastAPI(title="NFRS/IFRS RAG API")

# Initialize services
pipeline = RAGPipeline()
translator = TranslationService()

# Configure logging to file
logging.basicConfig(
    filename="query_logs.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    filemode="a"  # append to file
)
logger = logging.getLogger(__name__)

# Allow requests from Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in prod
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str
    session_id: str
    language: str = "en"  # Default to English
    
@app.post("/new_session")
def new_session():
    db: DBSession = SessionLocal()
    new_id = str(uuid.uuid4())
    chat_session = ChatSession(session_id=new_id)
    db.add(chat_session)
    db.commit()
    db.close()
    return {"session_id": new_id}

@app.get("/sessions")
def get_all_sessions():
    db: DBSession = SessionLocal()
    sessions = db.query(ChatSession).order_by(ChatSession.created_at.desc()).all()
    db.close()
    return [{"session_id": s.session_id, "created_at": s.created_at} for s in sessions]

@app.get("history/{session_id}")
def get_session_history(session_id: str):
    db: DBSession = SessionLocal()
    try:
        conversations = (
            db.query(Conversation)
            .filter(Conversation.session_id == session_id)
            .order_by(Conversation.timestamp.asc())
            .all()
        )
        return [
            {
                "question": c.question,
                "answer": c.answer,
            "sources": json.loads(c.sources) if c.sources else [],
            }
            for c in conversations
        ]
    finally:
        db.close()
    

@app.post("/query")
def query_rag(req: QueryRequest):
    db: DBSession = SessionLocal()
    try:
        logger.info(f"🔍 Incoming question: {req.question} (session: {req.session_id}, language: {req.language})")
        
        # Translate to English if needed
        if req.language != "en":
            english_question = translator.translate_to_english(req.question, req.language)
            logger.info(f"🌐 Translated to English: {english_question}")
        else:
            english_question = req.question

        # Get response from RAG pipeline
        result = pipeline.run(english_question)
        logger.info("✅ LLM responded.")

        # Translate response back if needed
        if req.language != "en":
            translated_answer = translator.translate_to_nepali(result["answer"], req.language)
            logger.info("🌐 Translated response back to user's language")
        else:
            translated_answer = result["answer"]

        # Store original English in database
        conversation = Conversation(
            session_id=req.session_id,
            question=english_question,  # Store English version
            answer=result["answer"],    # Store English version
            sources=json.dumps(result["references"])
        )

        db.add(conversation)
        db.commit()
        logger.info("✅ Stored in DB.")

        return {
            "answer": translated_answer,  # Return translated version
            "sources": result["references"]
        }

    except Exception as e:
        logger.error("❌ ERROR in /query", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()
