# locustfile.py
import os
import random
from locust import HttpUser, task, between

# -------- Configuración básica --------
# Locust usará el host que le pases por CLI (-H) o por la UI.
# Ejemplo:
#   locust -f locustfile.py -H http://localhost:8001
#
# Puedes personalizar queries y top_k por variables de entorno.
DEFAULT_QUERIES = [
    "¿Qué es un sistema RAG?",
    "explica la arquitectura del sistema",
    "beneficios de usar FAISS",
    "búsqueda semántica con embeddings",
    "riesgos de seguridad en RAG",
]

RAW_QUERIES = os.getenv("RETRIEVER_QUERIES")
if RAW_QUERIES:
    QUERIES = [q.strip() for q in RAW_QUERIES.split(",") if q.strip()]
else:
    QUERIES = DEFAULT_QUERIES

TOP_K = int(os.getenv("RETRIEVER_TOP_K", "4"))


class RetrieverUser(HttpUser):
    """
    Usuario que estresa el servicio Retriever (FAISS).

    Secuencia típica:
    - on_start: hace /health y opcionalmente un /upsert pequeño (warm-up).
    - Durante la prueba:
        * Mucho tráfico a /search (lecturas, crítico en RAG).
        * Algo de tráfico a /upsert (ingesta/escrituras).
        * Health check periódico.
    """

    # Tiempo de espera entre peticiones por usuario
    wait_time = between(0.1, 1.0)

    # ------- Hooks de inicio -------

    def on_start(self):
        """Pequeño warm-up al iniciar el usuario."""
        self.health_check()
        # Si quieres que cada usuario ingeste algo al inicio, descomenta:
        # self.upsert_docs()

    # ------- Tareas principales -------

    @task(8)
    def search_query(self):
        """
        Punto más crítico: /search
        La mayoría de la carga de un RAG real son búsquedas.
        """
        query = random.choice(QUERIES)
        payload = {"query": query, "top_k": TOP_K}

        with self.client.post(
            "/search",
            json=payload,
            name="/search",
            catch_response=True,
        ) as resp:
            if resp.status_code != 200:
                resp.failure(f"Status code {resp.status_code}")
            else:
                # Puedes validar estructura si quieres:
                # data = resp.json()
                # if "passages" not in data:
                #     resp.failure("Respuesta sin 'passages'")
                pass

    @task(2)
    def upsert_docs(self):
        """
        Carga de escritura: /upsert
        Menos frecuente que /search, pero importante para medir
        impacto de ingesta concurrente sobre el índice.
        """
        # Genera documentos pequeños sintéticos
        num_docs = random.randint(1, 3)
        docs = []
        for i in range(num_docs):
            doc_id = f"locust-doc-{self.environment.runner.user_count}-{random.randint(1, 1_000_000)}"
            text = (
                "Documento de prueba generado por Locust. "
                "Sirve para estresar el endpoint /upsert del retriever."
            )
            docs.append(
                {
                    "id": doc_id,
                    "text": text,
                    "meta": {"source": "locust", "batch": i},
                }
            )

        payload = {"docs": docs}

        with self.client.post(
            "/upsert",
            json=payload,
            name="/upsert",
            catch_response=True,
        ) as resp:
            if resp.status_code != 200:
                resp.failure(f"Status code {resp.status_code}")
            else:
                # Opcional: validar que responda "ok"
                try:
                    data = resp.json()
                    if data.get("status") != "ok":
                        resp.failure(f"Respuesta inesperada: {data}")
                except Exception as e:
                    resp.failure(f"Error parseando JSON: {e}")

    @task(1)
    def health_check_task(self):
        """
        Healthcheck periódico. Menor peso.
        """
        self.health_check()



    def health_check(self):
        with self.client.get(
            "/health",
            name="/health",
            catch_response=True,
        ) as resp:
            if resp.status_code != 200:
                resp.failure(f"Healthcheck fallo: {resp.status_code}")
            else:
                try:
                    data = resp.json()
                    if data.get("status") != "ok":
                        resp.failure(f"Health no OK: {data}")
                except Exception as e:
                    resp.failure(f"Error parseando JSON health: {e}")
