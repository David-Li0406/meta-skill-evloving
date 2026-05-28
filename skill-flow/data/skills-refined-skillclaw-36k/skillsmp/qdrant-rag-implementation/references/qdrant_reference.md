# Qdrant Implementation Reference

## Client Configuration Parameters

### QdrantClient Initialization Options

- `url` (str): The URL of the Qdrant server
- `api_key` (str): Authentication key for secured instances
- `timeout` (int): Global timeout for all operations (in seconds)
- `grpc_port` (int): Port for gRPC communication (default: 6334)
- `prefer_grpc` (bool): Use gRPC for better performance (default: False)

### Method-Specific Timeout Usage

The following methods accept a timeout parameter:
- `create_collection(collection_name, vectors_config, timeout)`
- `delete_collection(collection_name, timeout)`
- `query_points(collection_name, query, limit, timeout)`
- `info(timeout)`

The following methods do NOT accept timeout parameters (use client's global timeout):
- `get_collections()`
- `get_collection(collection_name)`
- `upsert(collection_name, points)`
- `scroll(collection_name, limit)`
- `retrieve(collection_name, ids)`

## Qdrant API Methods Mapping

### Search Operations

**OLD (Deprecated):**
```python
search_results = client.search(
    collection_name="my_collection",
    query_vector=[0.1, 0.2, 0.3],
    limit=10
)
```

**NEW (Current):**
```python
search_results = client.query_points(
    collection_name="my_collection",
    query=[0.1, 0.2, 0.3],  # Parameter renamed from query_vector
    limit=10,
    timeout=30
)
# Access results via search_results.points
for result in search_results.points:
    print(result.payload, result.score)
```

### Health and Information Operations

**Health Checks:**
```python
# OLD (Doesn't exist):
# health = client.health()

# NEW (Current):
info = client.info()  # No timeout parameter
print(f"Version: {info.version}")
print(f"Commit: {info.commit}")
```

### Collection Operations

```python
# Creating collections
client.create_collection(
    collection_name="my_collection",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    timeout=30  # Operation-specific timeout
)

# Verifying collections exist
collections = client.get_collections().collections
collection_names = [c.name for c in collections]

# Getting collection info
collection_info = client.get_collection(collection_name="my_collection")
points_count = collection_info.points_count
```

## Error Handling Patterns

### Common Qdrant Errors

1. **Connection Errors**: Ensure QDRANT_URL and QDRANT_API_KEY are properly set in environment variables
2. **Timeout Errors**: Increase timeout values for large operations
3. **Dimension Mismatch**: Verify embedding dimensions match collection configuration (typically 384)
4. **ID Format Errors**: Use integer IDs instead of string UUIDs
5. **Method Parameter Errors**: Use correct method names and parameters

### Recommended Error Handling Structure

```python
def operation_with_error_handling():
    try:
        # Qdrant operation
        result = client.query_points(
            collection_name="my_collection",
            query=[0.1] * 384,
            limit=5,
            timeout=30
        )
        return result
    except Exception as e:
        # Log the error
        logging.error(f"Qdrant operation failed: {e}")
        
        # Return appropriate fallback
        return []
```

## Performance Optimization

### Batch Operations

Process multiple documents in batches for better performance:

```python
def batch_store_documents(client, documents, batch_size=64):
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        client.upsert(
            collection_name="my_collection",
            points=batch
        )
        # Process batch
```

### Connection Management

1. Use global client instances to avoid repeated connection overhead
2. Prefer gRPC communication for better performance
3. Set appropriate timeout values based on operation complexity
4. Implement connection pooling for high-traffic applications

## ID Handling Requirements

Qdrant requires integer IDs rather than string UUIDs:

```python
def convert_id_to_integer(chunk_id, content=""):
    """
    Convert a string ID to an integer ID that Qdrant can accept
    """
    try:
        # If it's already numeric, convert directly
        if chunk_id.isdigit():
            return int(chunk_id)
        else:
            # Hash the string and take modulo to keep within reasonable range
            return hash(chunk_id) % (10**9)
    except (ValueError, AttributeError):
        # Fallback: hash the content if chunk_id is invalid
        import hashlib
        hex_hash = hashlib.md5(content.encode()).hexdigest()
        return int(hex_hash, 16) % (10**9)

# Usage example
point_id = convert_id_to_integer("chunk_123", "sample content")
```

## Collection Configuration

### Standard Vector Configuration

For most text embedding applications:
- Vector size: 384 (matches FastEmbed MiniLM-L6-v2 model)
- Distance metric: COSINE
- Collection name: Descriptive name specific to use case

```python
collection_config = {
    "size": 384,
    "distance": Distance.COSINE
}
```

### Verification Process

Always verify collection configuration matches expectations:

```python
def verify_collection_config(client, collection_name, expected_size=384, expected_distance=Distance.COSINE):
    """
    Verify that the collection has the expected configuration
    """
    try:
        collection_info = client.get_collection(collection_name=collection_name)
        
        # Check vector configuration
        if hasattr(collection_info.config.params, 'vectors'):
            vec_params = collection_info.config.params.vectors
            if (hasattr(vec_params, 'size') and vec_params.size != expected_size):
                logging.warning(f"Collection has unexpected vector size: {vec_params.size}")
            if (hasattr(vec_params, 'distance') and vec_params.distance != expected_distance):
                logging.warning(f"Collection has unexpected distance metric: {vec_params.distance}")
        
        return True
    except Exception as e:
        logging.error(f"Failed to verify collection config: {e}")
        return False
```

## Async Client Handling

### AsyncOpenAI vs Regular OpenAI Clients

The approach differs depending on the OpenAI client type:

**For AsyncOpenAI clients (like Qwen):**
- The `create` method is inherently async
- Do NOT use `acreate` method
- Always await the `create` method

**For regular OpenAI clients:**
- The `create` method is synchronous
- Use `acreate` method for async operations

### Detection and Handling

```python
async def handle_openai_call(client, model, messages):
    """
    Handle OpenAI API calls properly based on client type
    """
    # For AsyncOpenAI clients (like Qwen), the create method itself is async
    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=500,
        temperature=0.1
    )
    return response
```