package com.fraud.fraud_detection.repository;

import com.fraud.fraud_detection.model.ModelMetadata;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface ModelMetadataRepository extends JpaRepository<ModelMetadata, String> {

    // Fetch the currently deployed model version
    Optional<ModelMetadata> findByIsActiveTrue();

    // Fetch a specific version by name
    Optional<ModelMetadata> findByModelVersion(String modelVersion);
}