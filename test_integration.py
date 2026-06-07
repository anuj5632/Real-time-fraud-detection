import json
import time
import uuid
from datetime import datetime
from kafka import KafkaProducer, KafkaConsumer

KAFKA_BOOTSTRAP_SERVERS = "localhost:29092"
INPUT_TOPIC = "transaction-events"
OUTPUT_TOPIC = "fraud-results"

def test_integration():
    print("🚀 Starting Integration Test")
    
    # 1. Setup Producer (Simulating Java Backend)
    print(f"📦 Setting up producer to '{INPUT_TOPIC}'...")
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

    # 2. Setup Consumer (Simulating Java Backend / RAG Service listening to results)
    print(f"🎧 Setting up consumer for '{OUTPUT_TOPIC}'...")
    consumer = KafkaConsumer(
        OUTPUT_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="latest",
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        consumer_timeout_ms=10000  # 10 second timeout waiting for msg
    )

    # 3. Create a mock transaction
    transaction = {
        "id": str(uuid.uuid4()),
        "amount": 15000.50,         # High amount to potentially trigger fraud 
        "currency": "USD",
        "location": "Dark Web",     # Suspicious location
        "deviceId": "unknown-device-999",
        "userId": "user-404",
        "createdAt": datetime.utcnow().isoformat(),
        "status": "PENDING"
    }

    print(f"\n📤 Sending Transaction to '{INPUT_TOPIC}':")
    print(json.dumps(transaction, indent=2))
    
    # Send message Let ML service process it
    producer.send(INPUT_TOPIC, transaction)
    producer.flush()
    print("✅ Transaction sent successfully! Waiting for ML service prediction...\n")

    # 4. Listen for the prediction result 
    print(f"⏳ Listening on '{OUTPUT_TOPIC}'...")
    messages_received = 0
    for message in consumer:
        messages_received += 1
        result = message.value
        print(f"🎯 🧠 Prediction Received from '{OUTPUT_TOPIC}':")
        print(json.dumps(result, indent=2))
        break # Exit after first result

    if messages_received == 0:
        print("❌ No prediction received. Ensure ML Service consumer is running!")

    consumer.close()
    producer.close()
    print("\n🏁 Integration Test Completed!")

if __name__ == "__main__":
    test_integration()
