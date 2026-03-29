package com.fraud.fraud_detection.service;

import com.fraud.fraud_detection.dto.CreateTransactionRequest;
import com.fraud.fraud_detection.dto.TransactionResponse;
import com.fraud.fraud_detection.exception.TransactionNotFoundException;
import com.fraud.fraud_detection.exception.UserNotFoundException;
import com.fraud.fraud_detection.model.Transaction;
import com.fraud.fraud_detection.model.TransactionStatus;
import com.fraud.fraud_detection.repository.TransactionRepository;
import com.fraud.fraud_detection.repository.UserRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.UUID;

@Service
public class TransactionService {

    private final TransactionRepository transactionRepository;
    private final UserRepository userRepository;

    public TransactionService(TransactionRepository transactionRepository, UserRepository userRepository) {
        this.transactionRepository = transactionRepository;
        this.userRepository = userRepository;
    }

    @Transactional
    public TransactionResponse createTransaction(CreateTransactionRequest request) {
        if (!userRepository.existsById(request.getUserId())) {
            throw new UserNotFoundException("User not found with id: " + request.getUserId());
        }

        Transaction transaction = new Transaction();
        transaction.setUserId(request.getUserId());
        transaction.setAmount(request.getAmount());
        transaction.setCurrency(request.getCurrency().trim().toUpperCase());
        transaction.setLocation(request.getLocation().trim());
        transaction.setDeviceId(request.getDeviceId().trim());
        transaction.setStatus(TransactionStatus.PENDING);

        Transaction saved = transactionRepository.save(transaction);
        return toResponse(saved);
    }

    @Transactional(readOnly = true)
    public TransactionResponse getTransactionById(UUID transactionId) {
        Transaction transaction = transactionRepository.findById(transactionId)
                .orElseThrow(() -> new TransactionNotFoundException("Transaction not found with id: " + transactionId));

        return toResponse(transaction);
    }

    private TransactionResponse toResponse(Transaction transaction) {
        return TransactionResponse.builder()
                .id(transaction.getId())
                .userId(transaction.getUserId())
                .amount(transaction.getAmount())
                .currency(transaction.getCurrency())
                .location(transaction.getLocation())
                .deviceId(transaction.getDeviceId())
                .status(transaction.getStatus())
                .createdAt(transaction.getCreatedAt())
                .build();
    }
}

