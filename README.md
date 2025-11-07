Usuario ─▶ Frontend (Flask)
            │
            ▼
         API (FastAPI)
            │
            ▼
        Retriever + FAISS
            │
            ├─ Ollama (modo local)
            └─ OpenAI/Gemini (modo API)

Backend Team

El equipo de backend trabajó en los servicios:

API (FastAPI): endpoint /ask con la lógica RAG (consulta → recuperación → respuesta).

Retriever: módulo encargado de vectorizar documentos (ingest.py), gestionar FAISS y responder a /search.

Benchmarks: pruebas de latencia y rendimiento en benchmarks/latency_check.py.

Contenedores: configuraron los Dockerfiles y variables .env para cada entorno (local y api).

🔹 Frontend Team

El equipo de frontend desarrolló dos versiones en Flask:

frontend_local → interfaz para el modelo local (Ollama).

frontend_api → interfaz para modelos externos (OpenAI/Gemini).
Ambas consumen la API REST (/ask) y muestran las respuestas al usuario de forma simple y responsiva.

🔹 Integración y Colaboración

Ambos equipos trabajaron sobre la misma base de datos de vectores (FAISS + documentos en docs/).

La comunicación entre servicios se hizo vía HTTP REST, con endpoints estandarizados (/ask, /search, /health).

Se usaron perfiles de Docker Compose (local y api) para probar las dos versiones completas sin conflicto.

El desarrollo se coordinó mediante ramas compartidas (backend/ y frontend/), asegurando compatibilidad continua.