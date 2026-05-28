# AI and LLM Tooling in Rust

Comprehensive guide to AI/ML and LLM development in Rust.

## Ecosystem Overview

### ML/AI Frameworks

- **candle** - Minimalist ML framework (Meta/Hugging Face)
- **burn** - Comprehensive deep learning framework
- **lla** - LLM inference and training
- **tract** - ONNX/TensorFlow inference
- **tch-rs** - PyTorch bindings

### LLM Client Libraries

- **async-openai** - OpenAI API client
- **anthropic-sdk-rust** - Anthropic Claude API
- **ollama-rs** - Ollama local models
- **llm** - Universal LLM interface

### Orchestration & Tools

- **langchain-rust** - LangChain port
- **swiftide** - RAG and data pipelines
- **rig** - LLM application framework

## Model Inference

### Using Candle

```toml
[dependencies]
candle-core = "0.3"
candle-nn = "0.3"
candle-transformers = "0.3"
tokenizers = "0.15"
```

```rust
use candle_core::{Device, Tensor};
use candle_transformers::models::bert::{BertModel, Config};
use tokenizers::Tokenizer;

async fn run_inference() -> anyhow::Result<()> {
    let device = Device::cuda_if_available(0)?;

    // Load model
    let config = Config::bert_base_uncased();
    let model = BertModel::load("path/to/model", config, &device)?;

    // Load tokenizer
    let tokenizer = Tokenizer::from_pretrained("bert-base-uncased", None)?;

    // Tokenize input
    let encoding = tokenizer.encode("Hello, world!", false)?;
    let tokens = Tensor::new(encoding.get_ids(), &device)?;

    // Run inference
    let output = model.forward(&tokens)?;

    Ok(())
}
```

### Using llm-chain for Local Models

```toml
[dependencies]
llm = "0.2"
```

```rust
use llm::models::Llama;

fn generate_text() -> anyhow::Result<()> {
    // Load model
    let model = Llama::load(
        "path/to/llama-model.gguf",
        llm::ModelParameters::default(),
    )?;

    // Generate
    let mut session = model.start_session(Default::default());

    session.infer::<std::convert::Infallible>(
        model.as_ref(),
        &mut rand::thread_rng(),
        &llm::InferenceRequest {
            prompt: "Hello, my name is".into(),
            parameters: &llm::InferenceParameters::default(),
            play_back_previous_tokens: false,
            maximum_token_count: Some(50),
        },
        &mut Default::default(),
        |t| {
            print!("{t}");
            std::io::Write::flush(&mut std::io::stdout())?;
            Ok(llm::InferenceFeedback::Continue)
        },
    )?;

    Ok(())
}
```

## API Clients

### OpenAI Client

```toml
[dependencies]
async-openai = "0.20"
tokio = { version = "1", features = ["full"] }
```

```rust
use async_openai::{
    types::{ChatCompletionRequestMessage, CreateChatCompletionRequestArgs, Role},
    Client,
};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::new();

    let request = CreateChatCompletionRequestArgs::default()
        .model("gpt-4")
        .messages(vec![
            ChatCompletionRequestMessage {
                role: Role::System,
                content: Some("You are a helpful assistant.".to_string()),
                ..Default::default()
            },
            ChatCompletionRequestMessage {
                role: Role::User,
                content: Some("What is the capital of France?".to_string()),
                ..Default::default()
            },
        ])
        .build()?;

    let response = client.chat().create(request).await?;

    println!("{}", response.choices[0].message.content.as_ref().unwrap());

    Ok(())
}
```

### Streaming Responses

```rust
use async_openai::types::CreateChatCompletionStreamResponse;
use futures::StreamExt;

async fn stream_chat() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::new();

    let request = CreateChatCompletionRequestArgs::default()
        .model("gpt-4")
        .messages(vec![/* ... */])
        .stream(true)
        .build()?;

    let mut stream = client.chat().create_stream(request).await?;

    while let Some(result) = stream.next().await {
        match result {
            Ok(response) => {
                if let Some(choice) = response.choices.first() {
                    if let Some(delta) = &choice.delta.content {
                        print!("{delta}");
                    }
                }
            }
            Err(e) => eprintln!("Error: {e}"),
        }
    }

    Ok(())
}
```

### Anthropic Claude

```toml
[dependencies]
anthropic-sdk = "0.1"
```

```rust
use anthropic_sdk::{Client, MessagesRequest, Message, ContentBlock};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let client = Client::new(std::env::var("ANTHROPIC_API_KEY")?);

    let request = MessagesRequest {
        model: "claude-3-5-sonnet-20241022".to_string(),
        max_tokens: 1024,
        messages: vec![Message {
            role: "user".to_string(),
            content: vec![ContentBlock::Text {
                text: "Hello, Claude!".to_string(),
            }],
        }],
        ..Default::default()
    };

    let response = client.messages().create(request).await?;

    println!("{:?}", response);

    Ok(())
}
```

### Ollama (Local Models)

```toml
[dependencies]
ollama-rs = "0.1"
```

```rust
use ollama_rs::{Ollama, generation::completion::request::GenerationRequest};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let ollama = Ollama::new("http://localhost:11434".to_string());

    let request = GenerationRequest::new("llama2".to_string(), "Hello!".to_string());

    let response = ollama.generate(request).await?;

    println!("{}", response.response);

    Ok(())
}

// Streaming
use futures::StreamExt;

async fn stream_ollama() -> Result<(), Box<dyn std::error::Error>> {
    let ollama = Ollama::new("http://localhost:11434".to_string());

    let mut stream = ollama.generate_stream(
        GenerationRequest::new("llama2".to_string(), "Tell me a story".to_string())
    ).await?;

    while let Some(response) = stream.next().await {
        let response = response?;
        print!("{}", response.response);
    }

    Ok(())
}
```

## RAG (Retrieval-Augmented Generation)

### Vector Embeddings

```rust
use async_openai::types::CreateEmbeddingRequestArgs;

async fn create_embedding(text: &str) -> Result<Vec<f32>, Box<dyn std::error::Error>> {
    let client = Client::new();

    let request = CreateEmbeddingRequestArgs::default()
        .model("text-embedding-ada-002")
        .input(text)
        .build()?;

    let response = client.embeddings().create(request).await?;

    Ok(response.data[0].embedding.clone())
}
```

### Vector Database Integration

```rust
use qdrant_client::{client::QdrantClient, qdrant::{vectors_config, PointStruct}};

async fn setup_vector_db() -> Result<(), Box<dyn std::error::Error>> {
    let client = QdrantClient::from_url("http://localhost:6334").build()?;

    // Create collection
    client.create_collection(&CreateCollection {
        collection_name: "documents".to_string(),
        vectors_config: Some(vectors_config::Config::Params(VectorParams {
            size: 1536,  // OpenAI embedding size
            distance: Distance::Cosine.into(),
            ..Default::default()
        })),
        ..Default::default()
    }).await?;

    // Insert vectors
    let points = vec![
        PointStruct::new(
            1,
            vec![0.1, 0.2, /* ... */],
            json!({ "text": "Document text" }).into(),
        ),
    ];

    client.upsert_points("documents", None, points, None).await?;

    // Search
    let search_result = client.search_points(&SearchPoints {
        collection_name: "documents".to_string(),
        vector: vec![0.1, 0.2, /* query vector */],
        limit: 5,
        ..Default::default()
    }).await?;

    Ok(())
}
```

### Complete RAG Pipeline

```rust
use async_openai::Client;

struct RAGSystem {
    llm_client: Client,
    vector_db: QdrantClient,
}

impl RAGSystem {
    async fn query(&self, question: &str) -> Result<String, Box<dyn std::error::Error>> {
        // 1. Create embedding for question
        let query_embedding = self.create_embedding(question).await?;

        // 2. Search for relevant documents
        let search_results = self.vector_db.search_points(&SearchPoints {
            collection_name: "documents".to_string(),
            vector: query_embedding,
            limit: 3,
            with_payload: Some(true.into()),
            ..Default::default()
        }).await?;

        // 3. Extract context
        let context: String = search_results
            .result
            .iter()
            .filter_map(|p| p.payload.get("text"))
            .map(|v| v.as_str().unwrap_or(""))
            .collect::<Vec<_>>()
            .join("\n\n");

        // 4. Generate response with context
        let prompt = format!(
            "Context:\n{}\n\nQuestion: {}\n\nAnswer based on the context:",
            context, question
        );

        let response = self.llm_client.chat().create(
            CreateChatCompletionRequestArgs::default()
                .model("gpt-4")
                .messages(vec![ChatCompletionRequestMessage {
                    role: Role::User,
                    content: Some(prompt),
                    ..Default::default()
                }])
                .build()?
        ).await?;

        Ok(response.choices[0].message.content.clone().unwrap_or_default())
    }
}
```

## Function Calling / Tool Use

### OpenAI Function Calling

```rust
use async_openai::types::{
    ChatCompletionTool, ChatCompletionToolType,
    FunctionObject, ChatCompletionToolChoiceOption,
};
use serde_json::json;

async fn function_calling() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::new();

    let tools = vec![
        ChatCompletionTool {
            r#type: ChatCompletionToolType::Function,
            function: FunctionObject {
                name: "get_weather".to_string(),
                description: Some("Get the current weather in a location".to_string()),
                parameters: Some(json!({
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g., San Francisco, CA"
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"]
                        }
                    },
                    "required": ["location"]
                })),
            },
        },
    ];

    let request = CreateChatCompletionRequestArgs::default()
        .model("gpt-4")
        .messages(vec![ChatCompletionRequestMessage {
            role: Role::User,
            content: Some("What's the weather in Boston?".to_string()),
            ..Default::default()
        }])
        .tools(tools)
        .build()?;

    let response = client.chat().create(request).await?;

    // Check for function call
    if let Some(tool_calls) = &response.choices[0].message.tool_calls {
        for tool_call in tool_calls {
            println!("Function: {}", tool_call.function.name);
            println!("Arguments: {}", tool_call.function.arguments);

            // Execute function and send result back
            let result = get_weather(&tool_call.function.arguments)?;

            // Continue conversation with function result
            // ...
        }
    }

    Ok(())
}

fn get_weather(args: &str) -> Result<String, Box<dyn std::error::Error>> {
    // Parse arguments and call weather API
    Ok(json!({"temp": 72, "condition": "sunny"}).to_string())
}
```

## LLM Orchestration

### LangChain-style Chains

```rust
use langchain_rust::{chain::Chain, llm::OpenAI, prompt::PromptTemplate};

async fn create_chain() -> Result<(), Box<dyn std::error::Error>> {
    let llm = OpenAI::default();

    let template = PromptTemplate::new(
        "You are a helpful assistant. User: {input}\nAssistant:",
        vec!["input"],
    );

    let chain = Chain::new(template, llm);

    let result = chain
        .invoke(vec![("input", "What is Rust?")].into_iter().collect())
        .await?;

    println!("{}", result);

    Ok(())
}
```

### Agent Pattern

```rust
struct LLMAgent {
    client: Client,
    tools: Vec<Tool>,
    conversation_history: Vec<ChatCompletionRequestMessage>,
}

struct Tool {
    name: String,
    description: String,
    function: Box<dyn Fn(&str) -> Result<String, Box<dyn std::error::Error>> + Send + Sync>,
}

impl LLMAgent {
    async fn run(&mut self, user_input: &str) -> Result<String, Box<dyn std::error::Error>> {
        self.conversation_history.push(ChatCompletionRequestMessage {
            role: Role::User,
            content: Some(user_input.to_string()),
            ..Default::default()
        });

        loop {
            let response = self.get_llm_response().await?;

            if let Some(tool_call) = self.extract_tool_call(&response) {
                let tool_result = self.execute_tool(&tool_call)?;
                self.add_tool_result(tool_result);
            } else {
                return Ok(response);
            }
        }
    }

    async fn get_llm_response(&self) -> Result<String, Box<dyn std::error::Error>> {
        let request = CreateChatCompletionRequestArgs::default()
            .model("gpt-4")
            .messages(self.conversation_history.clone())
            .tools(self.get_tool_definitions())
            .build()?;

        let response = self.client.chat().create(request).await?;
        Ok(response.choices[0].message.content.clone().unwrap_or_default())
    }

    fn execute_tool(&self, tool_call: &ToolCall) -> Result<String, Box<dyn std::error::Error>> {
        let tool = self.tools.iter()
            .find(|t| t.name == tool_call.name)
            .ok_or("Tool not found")?;

        (tool.function)(&tool_call.arguments)
    }
}
```

## Fine-Tuning and Training

### Data Preparation

```rust
use serde_json::json;
use std::fs::File;
use std::io::Write;

fn prepare_training_data() -> Result<(), Box<dyn std::error::Error>> {
    let mut file = File::create("training_data.jsonl")?;

    let examples = vec![
        json!({
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is Rust?"},
                {"role": "assistant", "content": "Rust is a systems programming language..."}
            ]
        }),
        // More examples...
    ];

    for example in examples {
        writeln!(file, "{}", serde_json::to_string(&example)?)?;
    }

    Ok(())
}
```

### Evaluation

```rust
async fn evaluate_model(test_cases: Vec<(String, String)>) -> f64 {
    let client = Client::new();
    let mut correct = 0;

    for (input, expected) in test_cases {
        let response = client.chat().create(/* ... */).await.unwrap();
        let actual = response.choices[0].message.content.as_ref().unwrap();

        if actual.contains(&expected) {
            correct += 1;
        }
    }

    correct as f64 / test_cases.len() as f64
}
```

## Best Practices

1. **Rate Limiting**: Implement backoff and retry logic
2. **Caching**: Cache responses for identical queries
3. **Streaming**: Use streaming for better UX
4. **Error Handling**: Handle API errors gracefully
5. **Token Management**: Track token usage and costs
6. **Context Windows**: Manage conversation history size
7. **Prompt Engineering**: Test and iterate on prompts
8. **Security**: Sanitize inputs, validate outputs
9. **Monitoring**: Log requests, track performance
10. **Testing**: Test with various inputs and edge cases

## Performance Optimization

### Batching Requests

```rust
async fn batch_embeddings(texts: Vec<String>) -> Result<Vec<Vec<f32>>, Box<dyn std::error::Error>> {
    let client = Client::new();

    let request = CreateEmbeddingRequestArgs::default()
        .model("text-embedding-ada-002")
        .input(texts)  // Batch multiple texts
        .build()?;

    let response = client.embeddings().create(request).await?;

    Ok(response.data.into_iter().map(|d| d.embedding).collect())
}
```

### Parallel Processing

```rust
use futures::stream::{self, StreamExt};

async fn process_many_queries(queries: Vec<String>) -> Vec<String> {
    stream::iter(queries)
        .map(|query| async move {
            get_llm_response(&query).await.unwrap_or_default()
        })
        .buffered(10)  // Process 10 concurrently
        .collect()
        .await
}
```
