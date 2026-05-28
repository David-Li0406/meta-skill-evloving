# API Documentation

## Authentication

All API endpoints (except `/api/auth/login` and `/health`) require authentication via session cookies.

### Login

`POST /api/auth/login`

```json
{
  "email": "user@example.com",
  "password": "password"
}
```

## Prompts

### List Prompts

`GET /api/prompts/`

### Create Prompt

`POST /api/prompts/`

```json
{
  "name": "summarize",
  "template": "Summarize this: {text}",
  "input_variables": ["text"]
}
```

## Inference

### Run Inference

`POST /api/inference/`

```json
{
  "provider": "openai",
  "model": "gpt-3.5-turbo",
  "input_text": "Hello world",
  "token_value": "sk-..."
}
```

## Evaluation

### Run Evaluation

`POST /api/evaluation/{id}/run`
