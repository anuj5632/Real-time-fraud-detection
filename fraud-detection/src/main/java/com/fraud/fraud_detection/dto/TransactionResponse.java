package com.fraud.fraud_detection.dto;
import com.fraud.fraud_detection.model.TransactionStatus;
import lombok.Builder;
import lombok.Data;
import java.time.LocalDateTime;
import java.util.UUID;
@Data
@Builder
public class TransactionResponse {
    private UUID id;
    private UUID userId;
    private double amount;
    private String currency;
    private String location;
    private String deviceId;
    private TransactionStatus status;
    private LocalDateTime createdAt;
}
