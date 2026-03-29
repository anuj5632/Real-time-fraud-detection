package com.fraud.fraud_detection.service;

import com.fraud.fraud_detection.dto.AuthResponse;
import com.fraud.fraud_detection.dto.LoginRequest;
import com.fraud.fraud_detection.dto.SignupRequest;
import com.fraud.fraud_detection.exception.InvalidCredentialsException;
import com.fraud.fraud_detection.exception.UserAlreadyExistsException;
import com.fraud.fraud_detection.model.User;
import com.fraud.fraud_detection.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class AuthServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private PasswordEncoder passwordEncoder;

    @Mock
    private JwtService jwtService;

    private AuthService authService;

    @BeforeEach
    void setUp() {
        authService = new AuthService(userRepository, passwordEncoder, jwtService);
    }

    @Test
    void signupThrowsWhenEmailExists() {
        SignupRequest request = new SignupRequest();
        request.setName("Anuj");
        request.setEmail("anuj@gmail.com");
        request.setPassword("password123");

        when(userRepository.existsByEmail("anuj@gmail.com")).thenReturn(true);

        assertThrows(UserAlreadyExistsException.class, () -> authService.signup(request));
    }

    @Test
    void loginReturnsAuthResponseForValidCredentials() {
        UUID userId = UUID.randomUUID();
        User user = new User();
        user.setId(userId);
        user.setName("Anuj");
        user.setEmail("anuj@gmail.com");
        user.setPassword("hashed");

        LoginRequest request = new LoginRequest();
        request.setEmail("anuj@gmail.com");
        request.setPassword("password123");

        when(userRepository.findByEmail("anuj@gmail.com")).thenReturn(Optional.of(user));
        when(passwordEncoder.matches("password123", "hashed")).thenReturn(true);
        when(jwtService.generateToken(userId, "anuj@gmail.com")).thenReturn("jwt-token");

        AuthResponse response = authService.login(request);

        assertNotNull(response);
        assertEquals("Login successful", response.getMessage());
        assertEquals("jwt-token", response.getToken());
        assertEquals("anuj@gmail.com", response.getUser().getEmail());
    }

    @Test
    void loginThrowsOnInvalidPassword() {
        User user = new User();
        user.setEmail("anuj@gmail.com");
        user.setPassword("hashed");

        LoginRequest request = new LoginRequest();
        request.setEmail("anuj@gmail.com");
        request.setPassword("wrong");

        when(userRepository.findByEmail("anuj@gmail.com")).thenReturn(Optional.of(user));
        when(passwordEncoder.matches("wrong", "hashed")).thenReturn(false);

        assertThrows(InvalidCredentialsException.class, () -> authService.login(request));
    }
}

