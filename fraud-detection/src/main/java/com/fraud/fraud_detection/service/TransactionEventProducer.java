package com.fraud.fraud_detection.service;


import com.fraud.fraud_detection.dto.TransactionEvent;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.SendResult;
import org.springframework.stereotype.Service;
import java.util.concurrent.CompletableFuture;

@Slf4j
@Service
@RequiredArgsConstructor
public class TransactionEventProducer {
    @Value("${kafka.topic.transaction-events}")
    private String transactionEventsTopic;

    private final KafkaTemplate<String, Object> kafkaTemplate;

    public void sendTransactionEvent(TransactionEvent event){
        CompletableFuture<SendResult<String, TransactionEvent>> future =
                kafkaTemplate.send(transactionEventsTopic,event.getTransactionId(),event);

        future.whenComplete((result, ex) -> {
            if( ex != null){
                log.error("Failed to send transaction event: {}", event.getTransactionId(), ex.getMessage());
            }
            else{
                log.info("Transaction event sent | ID: {} | Partition: {} Offset: {} ",
                        event.getTransactionId(),
                        result.getRecordMetadata().partition(),
                        result.getRecordMetadata().offset()
                        );
            }
        });
    }
}
