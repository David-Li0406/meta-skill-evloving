# Microcopy & UX Writing

Concise, scannable copy improves usability 58%. Specific button labels can increase completion 14%.

## Core Principles

| Principle | Implementation |
|-----------|---------------|
| **Clarity over cleverness** | Plain language; no jargon |
| **One idea per element** | Each label = single concept |
| **Consistency** | Same term everywhere ("Sign in" not sometimes "Log in") |
| **Action verbs** | "Save changes" not "Changes saving" |
| **Specific buttons** | "Create account" > "Submit" |
| **Positive framing** | "Enter valid email" not "Invalid email" |
| **Scannable** | Short paragraphs, bullets, clear headers |

## Context-Specific Patterns

### Button Labels
| Bad | Good |
|-----|------|
| Submit | Create my account |
| Click here | Download the guide |
| Next | See my results |
| OK | Got it |
| Cancel | Keep editing |

### Error Messages
**Structure**: What happened + How to fix it

| Bad | Good |
|-----|------|
| Invalid input | Please enter a valid email (e.g., name@example.com) |
| Error | Password needs at least 8 characters |
| Required | Please enter your name so we know what to call you |

### Empty States
**Structure**: What goes here + How to populate it

```
No messages yet

Start a conversation with your team.
[Send a message]
```

### Loading States
Reassure the user:
- "Finding the best results..."
- "Saving your changes..."
- "Almost there..."

### Success Messages
Confirm + Suggest next step:
- "Message sent! They'll receive it shortly."
- "Account created. Let's set up your profile."
- "Payment successful. Check your email for the receipt."

### Form Labels
- Clear, above the field
- Not inside placeholder (accessibility issue)
- Helper text below for complex fields

```
Email address
[                    ]
We'll send your receipt here

NOT:

[Enter your email address]  ← placeholder disappears
```

### Tooltips
- Concise help only
- Don't repeat the label
- Trigger on hover/focus, not click (unless mobile)

### Placeholders
Use for format hints, not labels:
- "e.g., john@example.com"
- "MM/DD/YYYY"
- "Search..."

## Tone Guidelines

| Context | Tone |
|---------|------|
| Errors | Helpful, not blaming |
| Success | Celebratory but brief |
| Instructions | Clear, direct |
| Confirmations | Reassuring |
| Warnings | Serious but not alarming |

## Word Choice

### Prefer
- Simple words (use/help vs utilize/assist)
- Active voice (We sent your email vs Your email was sent)
- Present tense (This creates vs This will create)
- Contractions (You're, we'll, don't)

### Avoid
- Jargon and technical terms
- Double negatives
- Hedging (might, possibly, should)
- Unnecessary words (please note that, in order to)

## Formatting

- **Bold** for key terms or actions
- Sentence case for headers (This is a header)
- Title Case for buttons sometimes (Get Started)
- Numbers: 1, 2, 3 (not one, two, three)
- Keep paragraphs to 2-3 sentences max

## Testing Microcopy

A/B test:
- Button labels (14% completion increase from specific labels)
- Error message tone
- CTA copy (first-person vs second-person)
- Headline variations

## Checklist

- [ ] Would a 12-year-old understand this?
- [ ] Is it the same term used elsewhere?
- [ ] Does the button describe the outcome?
- [ ] Does the error explain how to fix it?
- [ ] Is there any jargon?
- [ ] Can it be shorter?
