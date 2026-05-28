---
id: java-spring-async
name: "Spring Async"
domain: JAVA
skill: faion-software-developer
category: "backend"
---

## Spring Async

### Problem
Process background tasks asynchronously.

### Framework: Async Configuration

```java
// src/main/java/com/example/config/AsyncConfig.java

package com.example.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

import java.util.concurrent.Executor;

@Configuration
@EnableAsync
public class AsyncConfig {

    @Bean(name = "taskExecutor")
    public Executor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(4);
        executor.setMaxPoolSize(8);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("Async-");
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        executor.initialize();
        return executor;
    }

    @Bean(name = "emailExecutor")
    public Executor emailExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(2);
        executor.setMaxPoolSize(4);
        executor.setQueueCapacity(50);
        executor.setThreadNamePrefix("Email-");
        executor.initialize();
        return executor;
    }
}
```

### Async Service

```java
// src/main/java/com/example/service/NotificationService.java

package com.example.service;

import com.example.entity.Order;
import com.example.entity.User;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

import java.util.concurrent.CompletableFuture;

@Service
@RequiredArgsConstructor
@Slf4j
public class NotificationService {

    private final EmailService emailService;
    private final SmsService smsService;

    @Async("emailExecutor")
    public CompletableFuture<Void> sendOrderConfirmation(Order order) {
        log.info("Sending order confirmation for order: {}", order.getId());
        try {
            emailService.send(
                    order.getUser().getEmail(),
                    "Order Confirmation",
                    buildOrderEmailBody(order)
            );
            return CompletableFuture.completedFuture(null);
        } catch (Exception e) {
            log.error("Failed to send order confirmation", e);
            return CompletableFuture.failedFuture(e);
        }
    }

    @Async("taskExecutor")
    public CompletableFuture<Void> sendWelcomeNotifications(User user) {
        CompletableFuture<Void> emailFuture = CompletableFuture.runAsync(() ->
                emailService.send(user.getEmail(), "Welcome!", buildWelcomeEmail(user))
        );

        CompletableFuture<Void> smsFuture = CompletableFuture.runAsync(() ->
                smsService.send(user.getPhone(), "Welcome to our service!")
        );

        return CompletableFuture.allOf(emailFuture, smsFuture)
                .exceptionally(ex -> {
                    log.error("Failed to send welcome notifications", ex);
                    return null;
                });
    }

    private String buildOrderEmailBody(Order order) {
        return "Your order #" + order.getId() + " has been confirmed.";
    }

    private String buildWelcomeEmail(User user) {
        return "Welcome, " + user.getName() + "!";
    }
}
```

### Agent

faion-backend-agent
