# AI Tool Reference

## ai_spawn

Spawn an AI CLI asynchronously:

```python
job = ai_spawn(
    cli="claude",           # "claude", "codex", or "gemini"
    prompt="Your question",
    files=["src/file.py"],  # Optional: files to include as context
    timeout=300             # Max seconds for CLI to complete
)
# Returns: AISpawnResult with status="spawned", job_id, cli
```

## ai_fetch

Fetch result of spawned AI:

```python
result = ai_fetch(
    job_id="abc123",  # From ai_spawn
    timeout=30        # Seconds to wait (0 = instant check)
)
# Returns AIFetchResult with one of:
# status="completed", content="...", metadata={...}
# status="running", message="Job still running..."
# status="failed", error="..."
# status="timeout", error="CLI timed out..."
```

## ai_call

Synchronous call (blocks until complete):

```python
result = ai_call(
    cli="claude",
    prompt="Your question",
    files=["src/file.py"],
    timeout=300
)
# Returns: AICallResult with status="success", content="...", metadata={...}
```

## ai_review

Spawn all 3 CLIs in parallel:

```python
review = ai_review(
    prompt="Analyze this code...",
    files=["src/"],
    timeout=300
)
# Returns: AIReviewResult with jobs dict containing claude, codex, gemini job info
```

## ai_list

List all active jobs:

```python
jobs = ai_list()
# Returns: AIListResult with list of AIJobInfo objects
```
