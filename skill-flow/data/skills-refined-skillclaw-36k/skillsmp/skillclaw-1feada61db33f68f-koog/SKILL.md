---
name: koog
description: Use this skill when you want to build AI agents using the JetBrains Koog framework in Kotlin, integrating LLMs and tool calling systems.
---

# Koog AI Agent Framework

Koog is a Kotlin-based framework for building AI agents with multiplatform support, offering an agent execution engine, multi-provider LLM abstraction, tool calling system, and features for observability, persistence, memory, and event handling.

## Project Configuration

```kotlin
// build.gradle.kts
plugins {
    kotlin("jvm") version "2.2.21"
    kotlin("plugin.spring") version "2.2.21"
    id("org.springframework.boot") version "3.5.7"
}

repositories {
    mavenCentral()
}

val koogVersion = "0.1.0"

dependencies {
    // Core Koog dependencies
    implementation("ai.koog:koog-agents:$koogVersion")
    implementation("ai.koog:koog-prompt:$koogVersion")

    // LLM Provider clients
    implementation("ai.koog:koog-llm-openai:$koogVersion")
    implementation("ai.koog:koog-llm-anthropic:$koogVersion")
    implementation("ai.koog:koog-llm-google:$koogVersion")

    // Spring Boot integration
    implementation("ai.koog:koog-spring-boot-starter:$koogVersion")

    // Observability (optional)
    implementation("ai.koog:koog-observability-opentelemetry:$koogVersion")

    // Vector storage for RAG (optional)
    implementation("ai.koog:koog-vector-storage:$koogVersion")
    implementation("ai.koog:koog-embeddings:$koogVersion")
}
```

## Core Concepts

### Key Components
- **`AIAgent<I, O>`** - Primary entry point for creating agents.
- **`AIAgentGraphStrategy`** - Defines workflow as a directed graph.
- **`PromptExecutor`** - Executes prompts against LLMs.
- **`LLMClient`** - Provider-specific interface for LLM communication.
- **`ToolRegistry`** - Builder for registering tools.
- **`Tool<TArgs, TResult>`** - Core abstraction for tool functionality.
- **`AIAgentFeature<TConfig>`** - Extends agent capabilities via pipeline interceptors.

## Creating a Simple Agent

```kotlin
import ai.koog.agents.core.agent.AIAgent
import ai.koog.prompt.executor.llms.all.simpleOpenAIExecutor
import ai.koog.prompt.executor.clients.openai.OpenAIModels

// Minimal agent creation
val agent = AIAgent(
    promptExecutor = simpleOpenAIExecutor(System.getenv("OPENAI_API_KEY")),
    llmModel = OpenAIModels.Chat.GPT4o
)

suspend fun main() {
    val result = agent.run("Hello! How can you help me?")
    println(result)
}
```

## Prompt Building

```kotlin
import ai.koog.prompt.dsl.prompt

val prompt = prompt("Your prompt here")
```