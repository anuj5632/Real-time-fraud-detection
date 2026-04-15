package com.fraud.fraud_detection.model;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.UuidGenerator;

import java.time.LocalDateTime;

@Entity
@Table(name = "rag_context_log")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class RagContextLog {

    @Id
    @UuidGenerator
    @Column(name = "id", updatable = false, nullable = false)
    private String id;

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "transaction_id", nullable = false, unique = true)
    private Transaction transaction;

    // Stores JSON array of ChromaDB retrieved documents
    @Column(name = "retrieved_docs", columnDefinition = "TEXT")
    private String retrievedDocs;

    // Full prompt sent to Claude
    @Column(name = "prompt_sent", columnDefinition = "TEXT")
    private String promptSent;

    // Claude's raw response
    @Column(name = "raw_response", columnDefinition = "TEXT")
    private String rawResponse;

    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        this.createdAt = LocalDateTime.now();
    }
}