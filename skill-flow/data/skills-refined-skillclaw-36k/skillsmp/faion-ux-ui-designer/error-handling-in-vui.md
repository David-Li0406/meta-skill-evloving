# Error Handling in VUI

### Problem

Voice recognition errors frustrate users and break conversations.

### Solution: Graceful Error Recovery

**Error Types:**

| Error | Cause | Solution |
|-------|-------|----------|
| No input | User silent | Repeat prompt with hint |
| No match | Unrecognized speech | Offer alternatives |
| Ambiguous | Multiple interpretations | Ask clarifying question |
| System error | Technical failure | Apologize, suggest retry |

**Progressive Disclosure:**
```
First failure:
"I didn't catch that. What's the city?"

Second failure:
"I'm having trouble understanding.
Try saying something like 'New York' or 'Chicago'"

Third failure:
"Let me try another way.
[Transfer to visual interface or agent]"
```

**Best Practices:**
```
→ Never blame the user
→ Provide immediate feedback
→ Offer recovery options
→ Suggest example phrases
→ Know when to escalate
```
