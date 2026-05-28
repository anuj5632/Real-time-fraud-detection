package com.fraud.fraud_detection.service;

//import com.fasterxml.jackson.databind.ObjectMapper;
import com.fraud.fraud_detection.dto.TransactionEvent;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.SendResult;
import org.springframework.stereotype.Service;
import tools.jackson.databind.ObjectMapper;

import java.util.concurrent.CompletableFuture;

@Slf4j
@Service
@RequiredArgsConstructor
public class TransactionEventProducer {

    @Value("${kafka.topics.transaction-events}")
    private String transactionEventsTopic;

    private final KafkaTemplate<String, String> kafkaTemplate;

    private final ObjectMapper objectMapper;

    public void sendTransactionEvent(TransactionEvent event) {

        try {

            String jsonEvent =
                    objectMapper.writeValueAsString(event);

            CompletableFuture<SendResult<String, String>> future =
                    kafkaTemplate.send(
                            transactionEventsTopic,
                            event.getTransactionId(),
                            jsonEvent
                    );

            future.whenComplete((result, ex) -> {

                if (ex != null) {

                    log.error(
                            "Failed to send transaction event: {}",
                            event.getTransactionId(),
                            ex
                    );

                } else {

                    log.info(
                            "Transaction event sent | ID: {} | Partition: {} | Offset: {}",
                            event.getTransactionId(),
                            result.getRecordMetadata().partition(),
                            result.getRecordMetadata().offset()
                    );
                }
            });

        } catch (Exception e) {

            log.error(
                    "JSON serialization failed for transaction: {}",
                    event.getTransactionId(),
                    e
            );
        }
    }
}