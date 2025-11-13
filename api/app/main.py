from fastapi import FastAPI
from pydantic import BaseModel
from providers import Retriever, LLM
from prompts import build_prompt
import os

TOP_K = int(os.getenv("TOP_K", "4"))

app = FastAPI(title="RAG API", version="1.0")

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str
    passages: list

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    
    return AskResponse(answer="", passages=[])