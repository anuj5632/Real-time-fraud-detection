from fastapi import FastAPI
import asyncio
import os
import threading
from app.kafka_consumer import consume_fraud_results

app = FastAPI(title="Fraud RAG Service")

@app.on_event("startup")
def startup_event():
    print("Starting up RAG Service...")
    # Background task to start Kafka consumer
    threading.Thread(target=consume_fraud_results, daemon=True).start()

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "rag-service"}
