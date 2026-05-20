from __future__ import annotations

import json

from kafka import KafkaConsumer

from app.config import settings
from app.kafka.producer import FraudResultProducer
from app.schemas.transaction_schema import TransactionRequest
from app.services.inference_service import InferenceService
from app.utils.logger import get_logger

logger = get_logger(__name__)


def consume_transactions() -> None:
    consumer = KafkaConsumer(
        settings.kafka_input_topic,
        bootstrap_servers=settings.kafka_bootstrap_servers,
        group_id=settings.kafka_consumer_group,
        auto_offset_reset="earliest",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )

    inference_service = InferenceService()
    producer = FraudResultProducer()

    for message in consumer:
        try:
            payload = message.value
            request = TransactionRequest(**payload)
            result = inference_service.predict_single(request)
            payload_out = (
                result.model_dump(by_alias=True) if hasattr(result, "model_dump") else result.dict(by_alias=True)
            )
            producer.publish(payload_out)
        except Exception:
            logger.exception("Failed to process message")
