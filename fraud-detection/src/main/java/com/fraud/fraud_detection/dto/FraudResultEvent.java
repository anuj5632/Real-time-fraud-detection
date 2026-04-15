package com.fraud.fraud_detection.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class FraudResultEvent {
    private String transactionId;
    private Boolean isFraud;
    private Double fraudProbability;
    private String modelVersion;
}