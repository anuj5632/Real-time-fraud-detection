package com.fraud.fraud_detection.service;

import com.fraud.fraud_detection.dto.FraudResultEvent;
import com.fraud.fraud_detection.model.FraudResult;
import com.fraud.fraud_detection.model.Transaction;
import com.fraud.fraud_detection.model.TransactionStatus;
import com.fraud.fraud_detection.repository.TransactionRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

import java.util.UUID;

@Slf4j
@Service
@RequiredArgsConstructor
public class FraudResultConsumer {

    private final TransactionRepository transactionRepository;

    @KafkaListener(
            topics = "${kafka.topic.fraud-results}",
            groupId = "${spring.kafka.consumer.group-id}"
    )
    public void consumeFraudResult(FraudResultEvent event) {
        log.info("Received fraud result for transaction ID: {}", event.getTransactionId());

        UUID transactionId;
        try {
            transactionId = UUID.fromString(event.getTransactionId());
        } catch (IllegalArgumentException ex) {
            log.warn("Invalid transaction ID from fraud result: {}", event.getTransactionId());
            return;
        }

        transactionRepository.findById(transactionId).ifPresentOrElse(
                transaction -> updateTransaction(transaction, event),
                () -> log.warn("Transaction not found for ID: {}", event.getTransactionId())
        );
    }

    private void updateTransaction(Transaction transaction, FraudResultEvent event) {
        boolean isFraud = Boolean.TRUE.equals(event.getIsFraud());

        FraudResult fraudResult = new FraudResult();
        fraudResult.setFraud(isFraud);
        fraudResult.setProbability(event.getFraudProbability() == null ? 0.0 : event.getFraudProbability());
        fraudResult.setModelVersion(event.getModelVersion());

        fraudResult.setTransaction(transaction);
        transaction.setFraudResult(fraudResult);
        transaction.setStatus(isFraud
                ? TransactionStatus.FRAUD
                : TransactionStatus.SUCCESS
        );

        transactionRepository.save(transaction);
        log.info("Transaction {} updated → status: {}, fraud: {}, probability: {}",
                transaction.getId(),
                transaction.getStatus(),
                event.getIsFraud(),
                event.getFraudProbability());
    }
}