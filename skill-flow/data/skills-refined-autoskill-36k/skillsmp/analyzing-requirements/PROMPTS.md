# Requirement Analysis Question Bank

## Deep Detail Categories

### 1. User Impact & Persona
- Who is the *primary* user?
- What is the single most important outcome for them?
- How does this feature change their current workflow?

### 2. Functional Nuance (Opinionated Choices)
When asking about functionality, offer these three perspectives:
- **The Lean Path**: What is the absolute minimum to make this work?
- **The Power Path**: What features would "super-users" expect?
- **The Safety Path**: How do we prevent misuse or data loss?

### 3. Technical & Non-Functional
- **Latency**: Is this "instant" (under 200ms) or "background" (async)?
- **Scalability**: How many concurrent users/actions do we expect?
- **Security**: What level of PII (Personally Identifiable Information) is involved?

### 4. Edge Cases Checklist
- Empty states (no data to show).
- Network failure/Offline mode.
- Unauthorized access attempts.
- Large data volume (e.g., 10,000 items in a list).
