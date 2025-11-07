FROM python:3.11-slim
WORKDIR /app
COPY app.py /app/app.py
RUN pip install --no-cache-dir flask requests
ENV PORT=3000
EXPOSE 3000
CMD ["python", "app.py"]