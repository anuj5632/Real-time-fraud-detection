package com.fraud.fraud_detection.config;

import org.apache.kafka.clients.admin.NewTopic;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.kafka.config.TopicBuilder;

public class KafkaTopicConfig {

    @Value("${kafka.topics.transaction-events}")
    private String transactionEventsTopic;

    @Value("${kafka.topics.fraud-results}")
    private String fraudResultsTopic;

    @Bean
    public NewTopic getTransactionEventsTopic(){
        return TopicBuilder.name(transactionEventsTopic)
                .partitions(3)
                .replicas(1)
                .build();
    }

    @Bean
    public NewTopic fraudresultsTopic(){
        return TopicBuilder.name(fraudResultsTopic)
                .partitions(3)
                .replicas(1)
                .build();
    }

}
