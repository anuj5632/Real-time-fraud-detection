package com.fraud.fraud_detection.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TransactionEvent {
    private String transactionId;
    private Double amount;
    private String location;
    private String deviceType;
    private String userId;
    private Long timestamp;
}