from fastapi import FastAPI
from models import UpsertRequest, SearchRequest
from vectorstore import VectorStore

app = FastAPI(title="Retriever (FAISS)")
vs = VectorStore()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/upsert")
async def upsert(payload: UpsertRequest):
    vs.upsert([d.dict() for d in payload.docs])
    return {"status": "ok", "count": len(payload.docs)}

@app.post("/search")
async def search(payload: SearchRequest):
    res = vs.search(payload.query, top_k=payload.top_k)
    return {"passages": res}
