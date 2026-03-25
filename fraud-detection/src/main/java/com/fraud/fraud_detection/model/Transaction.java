package com.fraud.fraud_detection.model;

import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.resource.transaction.spi.TransactionStatus;

import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Data
@Table(name = "transactions")
public class Transaction {

    @Id
    @GeneratedValue
    private UUID id;

    private UUID userId;

    private double amount;

    private String currency;

    private String location;

    private String deviceId;

    @Enumerated(EnumType.STRING)
    private TransactionStatus status; // PENDING, SUCCESS, FRAUD

    private LocalDateTime createdAt = LocalDateTime.now();
}