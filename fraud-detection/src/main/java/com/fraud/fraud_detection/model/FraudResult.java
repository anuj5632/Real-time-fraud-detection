package com.fraud.fraud_detection.model;


import jakarta.persistence.*;
import lombok.Data;

import java.time.LocalDateTime;

@Entity
@Data
@Table(name = "fraud_results")
public class FraudResult {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne
    @JoinColumn(name = "transaction_id")
    private Transaction transaction;

    private boolean isFraud;

    private double probability;

    private String modelVersion;

    private LocalDateTime evaluatedAt = LocalDateTime.now();

}
