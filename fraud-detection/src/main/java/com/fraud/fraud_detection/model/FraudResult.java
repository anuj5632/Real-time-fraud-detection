package com.fraud.fraud_detection.model;


import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Entity
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
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

    @Column(name = "justification", columnDefinition = "TEXT")
    private String justification;

    private LocalDateTime evaluatedAt = LocalDateTime.now();
}
