# FastMCP Quality Checklist

Based on [Anthropic MCP Directory Policy](https://support.claude.com/en/articles/11697096-anthropic-mcp-directory-policy).

## 1. Tool Descriptions (20 points)

### Requirements
- [ ] Tool names ≤ 64 characters
- [ ] Descriptions are clear and unambiguous
- [ ] Descriptions match actual functionality exactly
- [ ] No promised but undelivered features
- [ ] No vague descriptions like "does stuff" or "utility function"

### Scoring
| Criteria | Points |
|----------|--------|
| All tool names ≤ 64 chars | 5 |
| All tools have descriptions | 5 |
| Descriptions are specific and accurate | 5 |
| No misleading or vague descriptions | 5 |

### Red Flags
```python
# BAD - vague
@mcp.tool()
def process_data(data):
    """Process the data."""  # What kind of processing?

# GOOD - specific
@mcp.tool()
def convert_csv_to_json(csv_content: str) -> dict:
    """Convert CSV string to JSON object. Returns dict with headers as keys."""
```

## 2. Error Handling (15 points)

### Requirements
- [ ] Graceful error handling for all failure modes
- [ ] Helpful error messages (not generic "Error occurred")
- [ ] No unhandled exceptions that crash the server
- [ ] Errors include actionable information

### Scoring
| Criteria | Points |
|----------|--------|
| Try/except blocks present | 3 |
| Custom error messages | 4 |
| Error messages are actionable | 4 |
| No bare `except:` clauses | 4 |

### Red Flags
```python
# BAD - generic error
except Exception:
    return {"error": "An error occurred"}

# GOOD - helpful error
except FileNotFoundError as e:
    return {"error": f"File not found: {path}. Check the path exists."}
```

## 3. Annotations (15 points)

### Requirements
- [ ] `readOnlyHint` for tools that don't modify state
- [ ] `destructiveHint` for tools that delete/modify data
- [ ] `title` for human-readable tool names
- [ ] Proper Pydantic annotations with descriptions

### Scoring
| Criteria | Points |
|----------|--------|
| Annotated parameters with descriptions | 5 |
| Read-only tools marked appropriately | 5 |
| Destructive tools marked appropriately | 5 |

### Example
```python
from typing import Annotated

@mcp.tool()
def delete_job(
    job_id: Annotated[int, "Job ID to delete"],
) -> dict:
    """Delete a job from the queue. DESTRUCTIVE: cannot be undone."""
    # destructiveHint should be True
```

## 4. Token Efficiency (15 points)

### Requirements
- [ ] Responses are concise, not verbose
- [ ] No unnecessary metadata in responses
- [ ] Large data is paginated or summarized
- [ ] No redundant information

### Scoring
| Criteria | Points |
|----------|--------|
| Responses are minimal but complete | 5 |
| No unnecessary fields in responses | 5 |
| Large lists are paginated | 5 |

### Red Flags
```python
# BAD - verbose
return {
    "status": "success",
    "message": "Operation completed successfully",
    "data": result,
    "timestamp": datetime.now().isoformat(),
    "server_version": "1.0.0",
    "request_id": uuid4(),
}

# GOOD - minimal
return {"job_id": job.id, "status": "pending"}
```

## 5. Test Coverage (20 points)

### Requirements
- [ ] pytest tests exist
- [ ] Tests use FastMCP in-memory client
- [ ] Tests cover happy path AND error cases
- [ ] Tests are deterministic (no flaky tests)

### Scoring
| Criteria | Points |
|----------|--------|
| Test file exists | 5 |
| Uses FastMCP Client for testing | 5 |
| >50% tool coverage | 5 |
| Error cases tested | 5 |

### Required Test Pattern
```python
import pytest
from fastmcp import Client

@pytest.fixture
async def mcp_client():
    async with Client(transport=mcp) as client:
        yield client

async def test_list_tools(mcp_client):
    tools = await mcp_client.list_tools()
    assert len(tools) > 0

async def test_tool_error_handling(mcp_client):
    result = await mcp_client.call_tool("get_job", {"job_id": -1})
    assert "error" in result.data
```

## 6. Documentation (15 points)

### Requirements
- [ ] All tools have docstrings
- [ ] At least 3 working usage examples
- [ ] Clear description of server purpose
- [ ] Troubleshooting information available

### Scoring
| Criteria | Points |
|----------|--------|
| All tools have docstrings | 5 |
| 3+ usage examples documented | 5 |
| Server purpose is clear | 3 |
| Error troubleshooting documented | 2 |

## Total Score Calculation

```
Total = (tool_descriptions + error_handling + annotations +
         token_efficiency + test_coverage + documentation)

Grade:
  90-100: A (Production ready)
  75-89:  B (Good, minor fixes)
  60-74:  C (Acceptable, needs work)
  40-59:  D (Significant issues)
  0-39:   F (Major redesign needed)
```
