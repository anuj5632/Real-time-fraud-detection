package com.fraud.fraud_detection.dto;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;
import java.util.UUID;
@Data
public class CreateTransactionRequest {
    @NotNull(message = "User ID is required")
    private UUID userId;
    @Min(value = 1, message = "Amount must be greater than zero")
    private double amount;
    @NotBlank(message = "Currency is required")
    private String currency;
    @NotBlank(message = "Location is required")
    private String location;
    @NotBlank(message = "Device ID is required")
    private String deviceId;
}