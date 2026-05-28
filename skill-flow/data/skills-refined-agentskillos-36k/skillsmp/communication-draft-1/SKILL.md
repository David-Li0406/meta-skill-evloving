---
name: communication-draft
description: Draft personalized follow-up communications by analyzing the client's communication style from their emails, calls, and texts. Tailors tone, length, and approach to match how each client prefers to communicate.
---

# Communication Draft

## When to use this skill

- After identifying account needs follow-up
- User requests a draft for specific account
- Preparing batch follow-up communications

## Core Principle: Personalization Over Templates

**Do NOT use generic templates.** Every communication must be personalized based on:

1. How the client writes/speaks (formal vs casual)
2. Their response patterns (brief vs detailed)
3. Topics they care about (price, coverage, speed)
4. Their communication preferences (email vs call vs text)

## Communication Style Analysis

Before drafting, analyze the client's sources to understand their style:

### From Emails
- **Formality**: Do they use "Hi" or "Dear"? Sign off casually or formally?
- **Length**: Short and direct, or detailed explanations?
- **Tone**: Professional, friendly, anxious, busy?
- **Response time**: Quick responder or takes days?

### From Calls
- **Speaking style**: Gets to the point or likes small talk?
- **Decision making**: Decisive or needs time to think?
- **Questions asked**: Price-focused? Coverage-focused? Risk-averse?
- **Objections raised**: What concerns came up?

### From Texts
- **Brevity**: One-word responses or full sentences?
- **Emoji usage**: Professional or casual?
- **Timing**: When do they typically respond?

## Personalization Examples

### Client A: Busy, Direct Professional
Their emails are short, no pleasantries, just facts.

**Draft for them:**
```
Subject: GL Quote Ready - $2,400/year

Quick update - your quote is ready:
- $1M/$2M General Liability
- $2,400 annual premium
- Effective immediately upon binding

Let me know if you want to proceed or have questions.
```

### Client B: Relationship-Oriented, Detail-Seeker
Their calls include personal updates, they ask lots of questions.

**Draft for them:**
```
Subject: Following up on your insurance coverage - hope all is well!

Hi Sarah,

Hope the new location opening is going smoothly! I wanted to check in about the General Liability quote we discussed last week.

I know you mentioned wanting to review the coverage details with your accountant - happy to jump on a call with both of you if that would help. I can walk through exactly what's covered and answer any questions.

No rush, just wanted to make sure you have everything you need to make the best decision for the business.

Talk soon,
[Agent]
```

### Client C: Text-Preferred, Casual
They respond to texts quickly, emails slowly.

**Draft SMS:**
```
Hey [Name]! Following up on the quote for [Company]. Ready to move forward or any questions? Happy to chat whenever works 👍
```

## Analysis Workflow

1. **Read recent sources** (2-3 emails, calls, or texts)
2. **Identify patterns**:
   - Greeting style
   - Sign-off style  
   - Average message length
   - Formality level (1-5 scale)
   - Key concerns mentioned
   - Preferred channel
3. **Match your draft** to their patterns
4. **Reference specific details** from previous conversations

## Context to Pull

| Source | What to Extract |
|--------|-----------------|
| state.md | Stage, next steps, pending items |
| history.md | Last interaction, commitments made |
| emails/ | Writing style, concerns raised, questions asked |
| calls/ | Speaking style, objections, decision timeline |
| sms/ | Brevity preference, response patterns |

## Draft Output

```json
{
  "channel": "email",
  "subject": "...",
  "body": "...",
  "context_used": ["email_339115/raw.txt", "call_150734/summary.md"],
  "style_notes": {
    "formality": "casual",
    "length": "brief", 
    "tone": "friendly but professional",
    "key_concerns": ["price", "quick turnaround"]
  },
  "rationale": "Client uses casual greetings, short emails, mentioned being busy. Keeping this brief and to the point."
}
```

## Anti-Patterns (Avoid These)

- Generic "Just checking in" openers
- Copy-paste templates with [PLACEHOLDER] text
- Formal tone when client is casual (or vice versa)
- Long emails to clients who write short ones
- Email follow-ups to clients who prefer calls/texts
- Ignoring specific concerns they've raised
