# API Reference - Optimization Endpoints

Complete documentation for skills-fleet optimization API endpoints.

## Base URL

```
http://localhost:8000/api/v1/optimization
```

## Endpoints

### POST /start

**Start an optimization job**

Triggers background optimization using MIPROv2, GEPA, or BootstrapFewShot.

**Request Body**:
```json
{
  "optimizer": "miprov2",  // or "gepa" or "bootstrap_fewshot"
  "trainset_file": "config/training/trainset_v4.json",  // Path to JSON trainset
  "training_paths": [],  // Alternative: list of skill paths (legacy)
  "auto": "medium",  // MIPROv2 only: "light", "medium", "heavy"
  "max_bootstrapped_demos": 2,  // Max auto-generated examples
  "max_labeled_demos": 2,  // Max human-curated examples
  "save_path": "optimized_v1.pkl"  // Optional: save location
}
```

**Response**:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "message": "Optimization job started. Check status with GET /optimization/status/{job_id}"
}
```

**Example**:
```bash
curl -X POST http://localhost:8000/api/v1/optimization/start \
  -H "Content-Type: application/json" \
  -d '{
    "optimizer": "miprov2",
    "trainset_file": "config/training/trainset_v4.json",
    "auto": "medium"
  }'
```

### GET /status/{job_id}

**Get optimization job status**

Returns current status, progress, and results of an optimization job.

**Response**:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "running",  // "pending", "running", "completed", "failed"
  "progress": 0.65,  // 0.0 to 1.0
  "message": "Running miprov2 optimization...",
  "result": null,  // Populated on completion
  "error": null  // Populated on failure
}
```

**Completed Response**:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "progress": 1.0,
  "message": "Optimization complete. Saved to config/optimized/optimized_v1.pkl",
  "result": {
    "optimizer": "miprov2",
    "training_examples_count": 50,
    "save_path": "optimized_v1.pkl"
  },
  "error": null
}
```

**Example**:
```bash
curl http://localhost:8000/api/v1/optimization/status/550e8400-e29b-41d4-a716-446655440000
```

### GET /optimizers

**List available optimizers**

Returns list of optimizers with their parameters and descriptions.

**Response**:
```json
[
  {
    "name": "miprov2",
    "description": "MIPROv2 optimizer - Multi-stage Instruction Proposal and Optimization",
    "parameters": {
      "auto": {
        "type": "string",
        "options": ["light", "medium", "heavy"],
        "default": "medium",
        "description": "Optimization depth vs cost tradeoff"
      },
      "max_bootstrapped_demos": {
        "type": "integer",
        "default": 4,
        "description": "Maximum auto-generated demonstrations"
      }
    }
  },
  {
    "name": "gepa",
    "description": "GEPA optimizer - Generalized Efficient Prompt Algorithm (fast, reflection-based)",
    "parameters": {
      "num_candidates": {
        "type": "integer",
        "default": 5,
        "description": "Number of instruction candidates to generate"
      }
    }
  }
]
```

**Example**:
```bash
curl http://localhost:8000/api/v1/optimization/optimizers
```

## Python Client Example

```python
import httpx
import asyncio

async def optimize_program():
    async with httpx.AsyncClient() as client:
        # Start optimization
        response = await client.post(
            "http://localhost:8000/api/v1/optimization/start",
            json={
                "optimizer": "miprov2",
                "trainset_file": "config/training/trainset_v4.json",
                "auto": "medium",
                "save_path": "my_optimized_v1.pkl",
            }
        )
        
        if response.status_code != 200:
            print(f"Failed to start: {response.text}")
            return
        
        job_id = response.json()["job_id"]
        print(f"Job started: {job_id}")
        
        # Poll for completion
        while True:
            status_response = await client.get(
                f"http://localhost:8000/api/v1/optimization/status/{job_id}"
            )
            
            data = status_response.json()
            print(f"Status: {data['status']} ({data['progress']:.0%})")
            
            if data["status"] == "completed":
                print(f"✅ Complete! Result: {data['result']}")
                break
            
            if data["status"] == "failed":
                print(f"❌ Failed: {data['error']}")
                break
            
            await asyncio.sleep(5)  # Check every 5 seconds

# Run
asyncio.run(optimize_program())
```

## Error Responses

**400 Bad Request** - Invalid parameters
```json
{
  "detail": "Invalid optimizer: xyz. Use 'miprov2', 'gepa', or 'bootstrap_fewshot'"
}
```

**404 Not Found** - Job not found
```json
{
  "detail": "Optimization job 550e8400-... not found"
}
```

**500 Internal Server Error** - Server error
```json
{
  "detail": "Internal server error during optimization"
}
```

## Best Practices

1. **Use trainset_file over training_paths**: JSON format is more flexible and supports metadata
2. **Start with GEPA for testing**: Faster iteration, good for initial experiments
3. **Use MIPROv2 auto="medium" for production**: Balanced cost/quality
4. **Poll status every 5-10 seconds**: Don't overwhelm the server
5. **Handle all status states**: pending, running, completed, failed
6. **Set reasonable timeouts**: Optimization can take 5-30 minutes
7. **Save results**: Use save_path to persist optimized programs

## Integration with Monitoring

```python
from skill_fleet.core.dspy.monitoring import MLflowLogger, configure_mlflow

# Configure MLflow tracking
configure_mlflow(experiment_name="skill-optimization")

# Run optimization with tracking
with MLflowLogger(run_name="miprov2_v1") as logger:
    # Trigger API optimization
    response = await start_optimization(...)
    
    # Log parameters
    logger.log_params({
        "optimizer": "miprov2",
        "auto": "medium",
        "trainset_size": 50,
    })
    
    # ... wait for completion ...
    
    # Log results
    logger.log_metrics({
        "quality_score": result["quality_score"],
        "training_time": result["time_seconds"],
    })
```

## Production Deployment Notes

1. **Job Storage**: Currently in-memory (lost on restart). For production, use Redis/PostgreSQL.
2. **Concurrency**: Background tasks run in-process. Consider Celery for distributed processing.
3. **Rate Limiting**: No built-in rate limiting. Add middleware if exposing publicly.
4. **Authentication**: No auth by default. Add JWT/API key middleware for production.
5. **Monitoring**: Enable MLflow or custom metrics tracking for production runs.
