import os, json, numpy as np
from typing import List, Tuple
from sentence_transformers import SentenceTransformer
import faiss

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
DATA_DIR = "/data"
INDEX_PATH = os.path.join(DATA_DIR, "index.faiss")
META_PATH = os.path.join(DATA_DIR, "meta.json")

class VectorStore:
    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.dim = self.model.get_sentence_embedding_dimension()
        self.index = None
        self.meta = []
        self._load()

    def _load(self):
        if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
            self.index = faiss.read_index(INDEX_PATH)
            with open(META_PATH, "r", encoding="utf-8") as f:
                self.meta = json.load(f)
        else:
            self.index = faiss.IndexFlatIP(self.dim)
            self.meta = []

    def _save(self):
        faiss.write_index(self.index, INDEX_PATH)
        with open(META_PATH, "w", encoding="utf-8") as f:
            json.dump(self.meta, f, ensure_ascii=False, indent=2)

    def _embed(self, texts: List[str]) -> np.ndarray:
        embs = self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        return embs.astype("float32")

    def upsert(self, docs: List[dict]):
        texts = [d["text"] for d in docs]
        vectors = self._embed(texts)
        self.index.add(vectors)
        self.meta.extend([{"id": d["id"], "text": d["text"], "meta": d.get("meta") } for d in docs])
        self._save()

    def search(self, query: str, top_k: int = 4):
        q = self._embed([query])
        D, I = self.index.search(q, top_k)
        indices = I[0].tolist()
        scores = D[0].tolist()
        results = []
        for idx, score in zip(indices, scores):
            if idx == -1 or idx >= len(self.meta):
                continue
            results.append({
                "score": float(score),
                "id": self.meta[idx]["id"],
                "text": self.meta[idx]["text"],
                "meta": self.meta[idx].get("meta")
            })
        return results
