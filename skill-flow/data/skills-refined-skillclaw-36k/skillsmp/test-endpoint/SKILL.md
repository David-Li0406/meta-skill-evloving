---
name: test_endpoint
description: Test API endpoints and verify responses
agent_types: [testing]
task_keywords: [test, verify, check, validate, request, endpoint, error, fail, recover, retry, problem, issue]
---

# Skill: API Endpoint Testing and Validation

## Purpose
Test API endpoints using documented methodology to verify access and data availability.

## Context
You are a testing specialist verifying that a data source can be successfully accessed.

## Task
Given API documentation:

1. **Construct test request** - Use documented methodology and user requirements
2. **Handle authentication** - Apply credentials as documented
3. **Execute request** - Make the HTTP request
4. **Validate response** - Check status code, format, and data relevance
5. **Verify data** - Ensure returned data matches user requirements

## Available Tools
- make_request: Execute HTTP requests with authentication
- validate_response: Check response format and status
- extract_data: Extract relevant data from response

## Testing Strategy

### Pre-Request Validation
- Verify authentication credentials are available
- Check endpoint is accessible (valid URL)
- Ensure required parameters are provided
- Validate parameter types and formats

### Request Construction
- Use correct HTTP method (GET, POST, etc.)
- Add authentication headers as documented
- Include required parameters
- Handle pagination if needed

### Response Validation Checklist
- HTTP status code (should be 2xx for success)
- Response header content-type
- Response body format (valid JSON/XML/CSV)
- No unexpected error messages
- Data structure matches documentation

### Data Relevance Check
- Does returned data match user's description?
- Are expected fields present?
- Is there actual data (not empty result)?
- Multiple records returned when applicable?

## Output Format

Return test results as JSON:
```json
{
  "success": true/false,
  "status_code": 200,
  "response_time_ms": 1234,
  "data_received": true/false,
  "data_matches_description": true/false,
  "sample_data": {
    "record_count": 10,
    "first_record": {}
  },
  "error_message": "null or error description",
  "attempts": 1,
  "warnings": ["Any issues encountered"]
}
```

## Common Testing Scenarios

### Successful API Response
- Status 200, 201, or 204
- Valid response format
- Data returned
- Expected fields present

### Authentication Failure
- Status 401, 403
- Check credentials
- Verify authentication format
- Check if key has expired

### Rate Limit Exceeded
- Status 429
- Implement backoff
- Note rate limit for future use

### Not Found / Invalid Endpoint
- Status 404
- Verify URL format
- Check if endpoint deprecated
- Try alternative endpoints

### Timeout or Connection Error
- No response received
- Check endpoint availability
- Verify network connectivity
- Try alternative similar service

## Troubleshooting Guide

### Issue: Always getting 401/403
- Check API key format (Bearer vs plain)
- Verify header name (Authorization vs X-API-Key)
- Ensure credentials haven't expired
- Try making request without auth to see if auth required

### Issue: Always getting empty results
- Verify query parameters are correct
- Check if need to provide search criteria
- Try broader search parameters
- Check if data exists in specified range

### Issue: Timeout errors
- Verify endpoint URL is correct and accessible
- Check if endpoint has high latency
- Try simpler requests first
- Check service status page
