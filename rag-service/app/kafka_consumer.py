import json
import logging
import time
from kafka import KafkaConsumer
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "fraud-results")

def consume_fraud_results():
    logger.info(f"Starting RAG consumer to listen to {KAFKA_TOPIC} on {KAFKA_BOOTSTRAP_SERVERS}")
    
    # Retry logic for Kafka connection
    max_retries = 10
    retry_count = 0
    consumer = None
    
    while retry_count < max_retries:
        try:
            consumer = KafkaConsumer(
                KAFKA_TOPIC,
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                value_deserializer=lambda v: json.loads(v.decode("utf-8")),
                auto_offset_reset="earliest",
                group_id="rag-service-group"
            )
            logger.info("Successfully connected to Kafka!")
            break
        except Exception as e:
            logger.warning(f"Failed to connect to Kafka (Attempt {retry_count + 1}/{max_retries}): {e}. Retrying in 5 seconds...")
            retry_count += 1
            time.sleep(5)
            
    if not consumer:
        logger.error("Could not connect to Kafka after maximum retries. Exiting consumer thread.")
        return

    try:
        for msg in consumer:
            logger.info(f"RAG Service received fraud result: {msg.value}")
            # Insert logic here to embed data into vector DB or trigger alert explanations
            
    except Exception as e:
        logger.error(f"Error in RAG Kafka Consumer: {e}")

if __name__ == "__main__":
    consume_fraud_results()
