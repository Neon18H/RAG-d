""" Ingesta por lotes: lee /docs/*.txt y los sube al retriever. """
import os, glob, requests

RETRIEVER_URL = os.getenv("RETRIEVER_URL", "http://localhost:8001")
DOCS_DIR = os.getenv("DOCS_DIR", "/docs")

files = sorted(glob.glob(os.path.join(DOCS_DIR, "*.txt")))
print(f"Encontrados {len(files)} archivos para ingestar.")

docs = []
for i, path in enumerate(files, 1):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    docs.append({"id": os.path.basename(path), "text": text, "meta": {"source": path}})

if docs:
    r = requests.post(f"{RETRIEVER_URL}/upsert", json={"docs": docs})
    r.raise_for_status()
    print("Ingesta completa:", r.json())
else:
    print("No hay .txt en /docs.")
