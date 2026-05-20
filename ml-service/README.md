# Fraud Detection ML Service

Production-grade FastAPI microservice for training and serving an XGBoost fraud detection model. The service supports batch and real-time inference, Kafka integration, and MLflow experiment tracking.

## Features
- XGBoost training pipeline with imbalanced data handling
- Feature engineering for transaction behavior signals
- FastAPI endpoints for training and prediction
- Batch inference support
- Kafka consumer/producer integration
- MLflow logging for metrics and model artifacts

## Project Structure
- app/: API, services, model pipeline, Kafka, MLflow utilities
- data/: sample training data
- models/: trained model bundle and artifacts

## Setup
1. Create a virtual environment and install dependencies.
2. Configure environment variables in .env.
3. Start the API with uvicorn.

## Environment Variables
See .env for defaults. Important settings:
- DATA_PATH
- MODEL_PATH
- MODEL_VERSION
- MLFLOW_TRACKING_URI
- KAFKA_BOOTSTRAP_SERVERS

## Run API
```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Train Model
```
curl -X POST http://localhost:8000/train -H "Content-Type: application/json" -d "{}"
```

## Predict
```
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{
  "amount": 5000,
  "currency": "INR",
  "location": "Nagpur",
  "deviceId": "device123",
  "userId": "uuid-123"
}'
```

## Kafka Consumer
Run the consumer in a separate process to process transaction events:
```
python -m app.kafka.consumer
```
