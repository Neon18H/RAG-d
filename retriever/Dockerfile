FROM python:3.11-slim
WORKDIR /app
COPY app /app
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir fastapi uvicorn[standard] numpy faiss-cpu pydantic sentence-transformers
EXPOSE 8001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]