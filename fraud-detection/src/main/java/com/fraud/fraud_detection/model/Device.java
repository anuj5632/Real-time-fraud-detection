package com.fraud.fraud_detection.model;


import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Data;

import java.time.LocalDateTime;

@Entity
@Data
@Table(name = "devices")
public class Device {

    @Id
    private String id;

    private String deviceType;

    private boolean isTrusted;

    private LocalDateTime createdAt = LocalDateTime.now();
}
