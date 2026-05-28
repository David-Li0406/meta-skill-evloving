# User-Onboarding Test Invokes

## Standard Invoke

```
I'm new to the team and need to set up my MCP Hub access.
I have VS Code open and ready to go.

My experience:
- Terminal: Basic (can run commands)
- Git: Basic (know clone, commit, push)
- Docker: New (never used it)
- IDE: VS Code

Can you help me with onboarding?
```

**Expected behavior:**
- Shows phase overview, waits for "continue"
- Recognizes experience level from message
- Runs real commands (node --version, etc.)
- Docker: Detailed explanations
- Git/Terminal: Concise

---

## Experienced Developer

```
New dev here. Familiar with Terminal, Git, Docker.
What do I need to set up for the MCP Hub?
```

**Expected behavior:**
- Commands only, minimal explanations
- Focus on MCP-specific parts (token, config)
- Skip optional phases

---

## Partial Invokes

### Environment Check Only
```
Check my development environment
```

### MCP Setup Only
```
Help me set up the MCP client in my IDE
```

### Test Connection
```
Test my MCP Hub connection
```

### Concept Explanation
```
What is MCP?
What is a JWT token?
How does the Hub work?
```

---

## Edge Cases

### No Token Yet
```
I don't have a JWT token yet.
```

**Expected behavior:**
- Recognizes problem
- Refers to admin for token generation
- Shows what will be needed

### Token Expired
```
My token doesn't work anymore, getting 401.
```

**Expected behavior:**
- Recognizes token problem
- Refers to admin for new token
- Shows where to replace token

### Docker Issues
```
Docker won't start, getting "Cannot connect to Docker daemon"
```

**Expected behavior:**
- Show Docker troubleshooting steps
- Check Docker Desktop status
- Platform-specific guidance (macOS/Windows/Linux)
