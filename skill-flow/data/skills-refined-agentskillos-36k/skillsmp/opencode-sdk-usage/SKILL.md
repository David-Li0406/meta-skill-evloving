---
name: opencode-sdk-usage
description: Comprehensive OpenCode SDK usage guidance for integrating AI-powered code assistance and development tools
---

# What I Cover

This skill provides guidance on using the OpenCode SDK to integrate AI-powered code assistance and development tools into your projects. It covers installation, configuration, API usage, and best practices for leveraging OpenCode's capabilities in software development workflows.

Key areas include:
- SDK installation and setup
- Authentication and API key management
- Core API methods for code generation, analysis, and assistance
- Integration patterns for different development environments
- Error handling and rate limiting
- Security considerations

# Common Patterns

## Basic SDK Usage

```go
// Example from GoPayShortcuts project
package main

import (
    "github.com/opencode/sdk"
)

func main() {
    client := sdk.NewClient("your-api-key")
    
    // Generate code suggestions
    suggestions := client.GenerateCode("Write a Go function to parse JSON shortcuts")
    
    // Analyze code for improvements
    analysis := client.AnalyzeCode("func parseShortcuts(data []byte) ([]Shortcut, error) { ... }")
}
```

## Integration in Build Pipeline

In GoPayShortcuts, the SDK is integrated into the CI/CD pipeline for automated code reviews:

```yaml
# .github/workflows/code-review.yml
steps:
  - name: Code Review with OpenCode SDK
    run: |
      opencode review --api-key ${{ secrets.OPENCODE_API_KEY }} --target ./...
```

## Custom Tool Integration

```go
// Custom tool for shortcut validation
type ShortcutValidator struct {
    client *sdk.Client
}

func (v *ShortcutValidator) Validate(shortcut Shortcut) error {
    prompt := fmt.Sprintf("Validate this shortcut configuration: %+v", shortcut)
    result := v.client.AnalyzeCode(prompt)
    if result.HasIssues() {
        return fmt.Errorf("validation failed: %s", result.Issues)
    }
    return nil
}
```

# Best Practices

1. **Secure API Key Management**: Store API keys in environment variables or secure vaults, never in code.

2. **Rate Limiting Awareness**: Implement exponential backoff for API calls to handle rate limits gracefully.

3. **Caching Results**: Cache API responses for repeated queries to reduce latency and API usage.

4. **Error Handling**: Always check for API errors and provide fallback mechanisms.

5. **Code Quality**: Use the SDK's analysis features to maintain high code quality standards.

6. **Integration Testing**: Test SDK integrations thoroughly to ensure reliability.

# Related Skills

- software-architecture: For designing systems that integrate AI assistance
- frontend-design: For UI components that leverage code generation
- backend-developer: For server-side integrations with development tools
- deployment-specialist: For CI/CD pipeline integrations

This skill focuses specifically on the OpenCode SDK usage within the GoPayShortcuts project and similar development environments.