package com.fraud.fraud_detection.model;

import jakarta.persistence.*;

import java.time.LocalDateTime;

@Entity
public class RagExplanation {

    @Id
    @GeneratedValue(strategy = jakarta.persistence.GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "transaction_id")
    private Transaction transaction;

//    public Transaction getTransaction() {
//        return transaction;
//    }
//
//    public void setTransaction(Transaction transaction) {
//        this.transaction = transaction;
//    }

    @Column(columnDefinition = "TEXT")
    private String explanation;

    private String explanationType;

    private String llmModel;

    private LocalDateTime createdAt =  LocalDateTime.now();

//    @ManyToOne
//    @JoinColumn(name = "user_id")
//    private User user;
}
