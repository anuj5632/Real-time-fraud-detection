package com.fraud.fraud_detection.service;

import com.fraud.fraud_detection.dto.CreateTransactionRequest;
import com.fraud.fraud_detection.dto.TransactionResponse;
import com.fraud.fraud_detection.exception.TransactionNotFoundException;
import com.fraud.fraud_detection.exception.UserNotFoundException;
import com.fraud.fraud_detection.model.Transaction;
import com.fraud.fraud_detection.model.TransactionStatus;
import com.fraud.fraud_detection.repository.TransactionRepository;
import com.fraud.fraud_detection.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class TransactionServiceTest {

    @Mock
    private TransactionRepository transactionRepository;

    @Mock
    private UserRepository userRepository;

    @Mock
    private TransactionEventProducer transactionEventProducer;

    private TransactionService transactionService;

    @BeforeEach
    void setUp() {
        transactionService = new TransactionService(transactionRepository, userRepository, transactionEventProducer);
    }

    @Test
    void createTransactionThrowsWhenUserMissing() {
        UUID userId = UUID.randomUUID();
        CreateTransactionRequest request = new CreateTransactionRequest();
        request.setUserId(userId);
        request.setAmount(5000);
        request.setCurrency("INR");
        request.setLocation("Mumbai");
        request.setDeviceId("device123");

        when(userRepository.existsById(userId)).thenReturn(false);

        assertThrows(UserNotFoundException.class, () -> transactionService.createTransaction(request));
    }

    @Test
    void createTransactionSetsPendingStatus() {
        UUID userId = UUID.randomUUID();
        UUID transactionId = UUID.randomUUID();

        CreateTransactionRequest request = new CreateTransactionRequest();
        request.setUserId(userId);
        request.setAmount(5000);
        request.setCurrency("inr");
        request.setLocation("Mumbai");
        request.setDeviceId("device123");

        Transaction saved = new Transaction();
        saved.setId(transactionId);
        saved.setUserId(userId);
        saved.setAmount(5000);
        saved.setCurrency("INR");
        saved.setLocation("Mumbai");
        saved.setDeviceId("device123");
        saved.setStatus(TransactionStatus.PENDING);

        when(userRepository.existsById(userId)).thenReturn(true);
        when(transactionRepository.save(any(Transaction.class))).thenReturn(saved);

        TransactionResponse response = transactionService.createTransaction(request);

        assertEquals(TransactionStatus.PENDING, response.getStatus());
        assertEquals("INR", response.getCurrency());
    }

    @Test
    void getTransactionByIdThrowsForUnknownId() {
        UUID transactionId = UUID.randomUUID();
        when(transactionRepository.findById(transactionId)).thenReturn(Optional.empty());

        assertThrows(TransactionNotFoundException.class, () -> transactionService.getTransactionById(transactionId));
    }
}

