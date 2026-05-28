---
name: ktor-client
description: Use this skill when you need to make backend API calls, perform REST requests, handle serialization, and manage authentication in Kotlin applications.
---

# Ktor HTTP Client

HTTP client for Kotlin. Use when the bot needs to communicate with backend services.

## Setup

```kotlin
// build.gradle.kts
plugins {
    kotlin("plugin.serialization") version "2.0.0"
}

val ktorVersion = "3.1.1"

dependencies {
    implementation("io.ktor:ktor-client-core:$ktorVersion")
    implementation("io.ktor:ktor-client-cio:$ktorVersion")           // Engine (async)
    implementation("io.ktor:ktor-client-content-negotiation:$ktorVersion")
    implementation("io.ktor:ktor-serialization-kotlinx-json:$ktorVersion")
    implementation("io.ktor:ktor-client-logging:$ktorVersion")
    implementation("io.ktor:ktor-client-auth:$ktorVersion")

    // For testing
    testImplementation("io.ktor:ktor-client-mock:$ktorVersion")
}
```

## Client Configuration

```kotlin
import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.plugins.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.client.plugins.logging.*
import io.ktor.serialization.kotlinx.json.*
import kotlinx.serialization.json.Json

val httpClient = HttpClient(CIO) {
    // JSON serialization
    install(ContentNegotiation) {
        json(Json {
            prettyPrint = true
            isLenient = true
            ignoreUnknownKeys = true
        })
    }

    // Logging
    install(Logging) {
        logger = Logger.DEFAULT
        level = LogLevel.INFO
        filter { request -> request.url.host.contains("api") }
        sanitizeHeader { header -> header == HttpHeaders.Authorization }
    }

    // Timeouts
    install(HttpTimeout) {
        requestTimeoutMillis = 30_000
        connectTimeoutMillis = 10_000
        socketTimeoutMillis = 30_000
    }

    // Default request config
    defaultRequest {
        url("https://api.your-project.example.com/api/v1/")
    }
}
```

## Basic Requests

### GET Request

```kotlin
import io.ktor.client.call.*
import io.ktor.client.request.*

// Simple GET
val response: String = httpClient.get("https://api.example.com/data").body()

// GET with path parameter
val user: User = httpClient.get("users/$userId").body()

// GET with query parameters
val users: List<User> = httpClient.get("users") {
    parameter("page", 1)
    parameter("limit", 20)
    parameter("status", "active")
}.body()
```