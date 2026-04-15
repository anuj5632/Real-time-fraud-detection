package com.fraud.fraud_detection.repository;

import com.fraud.fraud_detection.model.RagContextLog;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface RagContextLogRepository extends JpaRepository<RagContextLog, String> {
    Optional<RagContextLog> findByTransactionId(String transactionId);
}