from __future__ import annotations

import json
from typing import Any, Dict

from kafka import KafkaProducer

from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class FraudResultProducer:
    def __init__(self) -> None:
        self.producer = KafkaProducer(
            bootstrap_servers=settings.kafka_bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

    def publish(self, payload: Dict[str, Any]) -> None:
        logger.info("Publishing result to %s", settings.kafka_output_topic)
        self.producer.send(settings.kafka_output_topic, payload)
        self.producer.flush()
