import os
import requests
from typing import Dict

# =======================
# Entorno / Config
# =======================
RETRIEVER_URL = os.getenv("RETRIEVER_URL", "http://retriever:8001")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "local").lower().strip()

# Local (Ollama en host o contenedor)
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2:1b")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")

# OpenRouter (API externa)
OPENROUTER_API_KEY = ""
OPENROUTER_MODEL = ""
OPENROUTER_BASE_URL = ""
OPENROUTER_REFERER = ""
OPENROUTER_TITLE = ""

DEFAULT_TIMEOUT = int(os.getenv("HTTP_TIMEOUT_SECONDS", "300"))


# =======================
# Retriever
# =======================
class Retriever:
    @staticmethod
    def search(query: str, top_k: int = 4) -> Dict:
        r = requests.post(
            f"{RETRIEVER_URL}/search",
            json={"query": query, "top_k": top_k},
            timeout=120,
        )
        r.raise_for_status()
        return r.json()


# =======================
# LLM Providers
# =======================
class LLM:
    @staticmethod
    def _ensure(value: str, name: str):
        if not value or not value.strip():
            raise RuntimeError(f"Falta configurar {name} en el entorno (.env).")
        return value

    @staticmethod
    def generate(prompt: str) -> str:
        provider = (os.getenv("MODEL_PROVIDER", MODEL_PROVIDER) or "local").lower().strip()



       