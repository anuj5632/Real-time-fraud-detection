package com.fraud.fraud_detection.dto;
import lombok.Builder;
import lombok.Data;
import java.time.LocalDateTime;
import java.util.List;
@Data
@Builder
public class ErrorResponse {
    private String message;
    private String errorCode;
    private LocalDateTime timestamp;
    private List<String> details;
}
