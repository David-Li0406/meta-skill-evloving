# VUI Conversation Design

### Conversation Components

| Component | Function | Example |
|-----------|----------|---------|
| Wake word | Activate assistant | "Hey Google" |
| Intent | User's goal | "Set timer" |
| Entities | Parameters | "5 minutes" |
| Prompt | System question | "What should I call this timer?" |
| Confirmation | Verify action | "Timer set for 5 minutes" |
| Error handling | Recovery | "I didn't catch that. How long?" |

### Dialog Flow Design

```
Happy Path:
User: "Set a timer for 5 minutes"
VUI: "5-minute timer started"

Missing Entity:
User: "Set a timer"
VUI: "For how long?"
User: "5 minutes"
VUI: "5-minute timer started"

Clarification:
User: "Set a timer for five"
VUI: "5 minutes or 5 hours?"
User: "Minutes"
VUI: "5-minute timer started"
```

### Prompt Design Guidelines

| Type | Guideline |
|------|-----------|
| Open prompts | "How can I help?" |
| Directed prompts | "What city?" |
| Option prompts | "Red, blue, or green?" |
| Confirmation | "Is that correct?" (yes/no) |
