package com.fraud.fraud_detection.model;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.UuidGenerator;

import java.time.LocalDateTime;

@Entity
@Table(name = "model_metadata")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ModelMetadata {

    @Id
    @UuidGenerator
    @Column(name = "id", updatable = false, nullable = false)
    private String id;

    @Column(name = "model_version", nullable = false, unique = true, length = 50)
    private String modelVersion;

    @Column(name = "accuracy", precision = 5, scale = 4)
    private Double accuracy;

    @Column(name = "precision_score", precision = 5, scale = 4)
    private Double precisionScore;

    @Column(name = "recall", precision = 5, scale = 4)
    private Double recall;

    @Column(name = "f1_score", precision = 5, scale = 4)
    private Double f1Score;

    @Column(name = "trained_at", nullable = false)
    private LocalDateTime trainedAt;

    // Only one model can be active at a time
    @Column(name = "is_active", nullable = false)
    @Builder.Default
    private Boolean isActive = false;

    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        this.createdAt = LocalDateTime.now();
    }
}