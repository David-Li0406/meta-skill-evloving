---
id: voice-ui
name: "Voice UI Design"
domain: UX
skill: faion-ux-ui-designer
category: "ux-design"
---

# Voice UI Design

## Metadata
- **Category:** UX / Design Methods
- **Difficulty:** Advanced
- **Tags:** #methodology #ux #design #voice-ui #conversational
- **Agent:** faion-usability-agent

---

## Problem

Voice interfaces are designed like visual ones. Users don't know what to say. Commands feel robotic and unnatural. Error handling is frustrating. There's no clear mental model. Voice adds friction instead of removing it.

Without proper VUI design:
- Unnatural interactions
- High error rates
- User frustration
- Abandoned voice features

---

## Framework

### What is Voice UI?

Voice UI (VUI) design creates interfaces controlled by speech. This includes voice assistants, voice commands, IVR systems, and voice features in apps.

### Voice UI Components

| Component | Description |
|-----------|-------------|
| **Wake word** | Activates listening (e.g., "Alexa") |
| **Intent** | What the user wants |
| **Slot** | Variable within intent (e.g., city name) |
| **Prompt** | What system says to user |
| **Utterance** | What user can say |
| **Confirmation** | Verification before action |

### When to Use Voice

| Good for Voice | Not Good for Voice |
|----------------|-------------------|
| Hands-busy tasks | Complex data entry |
| Quick commands | Private information |
| Simple queries | Noisy environments |
| Accessibility | Browsing/exploring |
| Multitasking | Detailed comparison |

---

## Process

### Step 1: Define Use Cases

**Identify voice-appropriate tasks:**

```
Questions:
- What tasks are hands-free valuable?
- What can be done faster with voice?
- What's the user context?
- Is there audio output capability?
```

### Step 2: Write Sample Dialogues

Before anything technical, write natural conversations:

```
User: "Set a timer for 15 minutes"
System: "Timer set for 15 minutes, starting now."

User: "What's the weather like?"
System: "Right now in Austin it's 72 degrees and sunny.
         Tonight expect lows around 55."

User: "Add milk to my shopping list"
System: "I've added milk to your shopping list."
```

### Step 3: Define Intents and Slots

**Intent:** The action the user wants
**Slot:** Variables within the intent

```
Intent: SetTimer
Slots:
  - duration (required): "15 minutes", "an hour", "90 seconds"
  - name (optional): "pasta timer", "workout timer"

Sample utterances:
- "Set a timer for {duration}"
- "Set a {duration} timer"
- "Timer {duration}"
- "Start a timer called {name} for {duration}"
```

### Step 4: Design Prompts

**Write what the system says:**

```
Initial prompt:
Clear: "What would you like to order?"
Not: "Hello! Welcome to Pizza Palace, the best pizza in town!
      We have so many great options! What can I get for you today?"

Error prompt:
Helpful: "I didn't catch that. You can say a size like
         'medium' or 'large'."
Not: "Error. Please try again."

Confirmation:
Implicit: "Adding milk to your list."
Explicit: "That's a large pepperoni for pickup at noon.
          Should I place the order?"
```

### Step 5: Handle Errors

**Design for failure:**

```
Error types:
1. No input detected
2. Speech not recognized
3. Intent not understood
4. Slot value invalid
5. Confirmation denied

Error strategy:
1st error: Rephrase prompt
2nd error: Offer examples
3rd error: Offer fallback (agent, visual)
```

### Step 6: Test with Users

```
Testing methods:
- Wizard of Oz (human plays system)
- Prototype testing
- A/B testing prompts
- Analyze real conversations
```

---

## Templates

### Voice Flow Document

```markdown
# Voice Flow: [Feature Name]

**Version:** [Number]
**Date:** [Date]

## Overview

**Purpose:** [What this voice feature does]
**Trigger:** [How user starts interaction]
**Exit:** [How interaction ends]

## User Context

- When: [Typical use times]
- Where: [Environment]
- Device: [Smart speaker / Phone / In-car]
- Hands/Eyes: [Occupied or available]

## Happy Path Dialogue

**User:** [Initial utterance]
**System:** [Response]
**User:** [Follow-up if needed]
**System:** [Final response]

## Intent Definitions

### Intent: [IntentName]

**Description:** [What user wants to do]
**Required slots:**
| Slot | Type | Prompt if missing |
|------|------|-------------------|
| [slot] | [type] | "[prompt]" |

**Sample utterances:**
- "[Utterance 1]"
- "[Utterance 2]"
- "[Utterance 3]"

**Response template:**
"[Response with {slot} placeholders]"

## Error Handling

### No Input Detected
**1st prompt:** "[Reprompt]"
**2nd prompt:** "[Rephrase with examples]"
**3rd prompt:** "[Offer fallback]"

### Speech Not Understood
**Response:** "[Acknowledgment + reprompt]"

### Invalid Slot Value
**Response:** "[Explain valid options]"

## Confirmation Strategy

| Action Type | Confirmation |
|-------------|--------------|
| [Low-risk] | Implicit |
| [High-risk] | Explicit |
| [Irreversible] | Explicit + repeat |

## Edge Cases

| Scenario | Handling |
|----------|----------|
| [Edge case 1] | [Response] |
| [Edge case 2] | [Response] |

## Fallbacks

- Visual fallback: [Screen if available]
- Human fallback: [Transfer to agent]
- Alternative: [Suggest different action]
```

### Prompt Writing Template

```markdown
# Prompt: [Prompt Name]

## Context
- Where in flow: [Position]
- User state: [What happened before]
- Goal: [What we need from user]

## Primary Prompt
"[The main prompt text]"

## Variations
- Short: "[Shorter version]"
- Long: "[More detailed version]"
- Casual: "[More conversational]"

## Reprompts
1st: "[First reprompt - shorter]"
2nd: "[Second reprompt - with examples]"
3rd: "[Third reprompt - offer fallback]"

## Design Rationale
- [Why this wording]
- [Trade-offs considered]

## A/B Test Variants
- A: "[Version A]"
- B: "[Version B]"
```

---

## Examples

### Example 1: Food Ordering

**Happy path:**
```
User: "Order my usual from Papa's Pizza"
System: "I'll place your usual order: a large pepperoni
        and a 2-liter Coke for delivery. That's $18.50.
        Should I place the order?"
User: "Yes"
System: "Order placed. Delivery in about 35 minutes."
```

**Error handling:**
```
User: "Order pizza"
System: "Sure! Which pizza place? You've ordered from
        Papa's Pizza and Domino's before."
User: "Papa's"
System: "What would you like from Papa's Pizza?"
```

### Example 2: Smart Home

**Multiple ways to say it:**
```
"Turn off the living room lights"
"Lights off in the living room"
"Living room lights off"
"Turn the living room lights off"
"Switch off the living room lights"
"Kill the lights in the living room"
```

**All should map to same intent:**
```
Intent: ControlLight
Slots:
  - room: "living room"
  - action: "off"
```

---

## Prompt Writing Guidelines

### Do's

| Guideline | Example |
|-----------|---------|
| **Be concise** | "Added." not "I have successfully added the item to your list." |
| **Be conversational** | "What's next?" not "Please state your next request." |
| **Give options** | "You can say 'today' or give a specific date." |
| **Confirm important actions** | "That's a $500 transfer. Confirm?" |
| **Use prosody** | Write for speaking rhythm |

### Don'ts

| Avoid | Why |
|-------|-----|
| **Long prompts** | Users forget the beginning |
| **Too many options** | Can't remember more than 3-4 |
| **Jargon** | Users won't know special terms |
| **Assuming context** | "It" and "that" are ambiguous |
| **Same error message** | Frustrates users who keep trying |

---

## Error Recovery

### Progressive Error Handling

```
1st error:
"Sorry, I didn't catch that. What city?"

2nd error:
"I'm still having trouble. You can say a city name
like 'New York' or 'Los Angeles'."

3rd error:
"Let me help differently. Would you like to type
the city instead, or speak to someone?"
```

### Error Types and Responses

| Error | Good Response |
|-------|--------------|
| **No input** | "I didn't hear anything. Try again?" |
| **Not understood** | "I didn't understand. Could you rephrase?" |
| **Wrong intent** | "I thought you meant X. Did you mean Y?" |
| **Invalid value** | "I don't have that option. You can choose A, B, or C." |
| **System error** | "Something went wrong on my end. Let's try again." |

---

## Multimodal Design

When voice + screen available:

### Voice + Visual Best Practices

| Element | Voice | Visual |
|---------|-------|--------|
| **Lists** | Say top 3 | Show full list |
| **Confirmation** | Speak it | Show details |
| **Input** | Voice command | Tap fallback |
| **Errors** | Speak guidance | Show options |

### Screen Companion

```
Voice: "Here are your upcoming appointments."
Screen: [Shows full calendar with details user can scan]

Voice: "Tap the one you want to reschedule."
Screen: [Each appointment is tappable]
```

---

## Platform Guidelines

### Amazon Alexa

- Custom wake word not allowed
- 8-second response limit
- Card/APL for visual companions
- Certification required

### Google Assistant

- Action invocation
- Multi-surface support
- Rich responses with cards
- Dialogflow for NLU

### Apple Siri

- SiriKit intents (limited)
- Shortcuts for custom
- HomePod integration
- Privacy-focused

---

## Common Mistakes

1. **Too much speech** - Users zone out after 15 seconds
2. **No error variety** - Same message frustrates users
3. **Expecting exact phrases** - Natural language varies
4. **Forgetting context** - Not using conversation history
5. **No escape hatch** - Users must be able to exit
6. **Visual thinking** - Designing for eye, not ear

---

## Testing Voice

### Wizard of Oz Testing

```
Setup:
1. Human plays the "system"
2. User doesn't know it's human
3. Human follows script/flows
4. Record everything

Learn:
- What users actually say
- Where confusion happens
- What's missing
```

### Metrics

| Metric | Meaning |
|--------|---------|
| **Task completion** | Did they accomplish goal? |
| **Turns to complete** | How many exchanges? |
| **Error rate** | How often misunderstood? |
| **Fallback rate** | How often needed escape? |
| **CSAT** | User satisfaction |

---

## Checklist

Design phase:
- [ ] Voice-appropriate use cases identified
- [ ] Sample dialogues written
- [ ] Intents and slots defined
- [ ] Multiple utterances per intent
- [ ] Prompts written conversationally
- [ ] Error handling designed
- [ ] Confirmation strategy defined

Development phase:
- [ ] NLU trained with utterance variations
- [ ] Edge cases handled
- [ ] Fallbacks implemented
- [ ] Multimodal companion (if applicable)

Testing phase:
- [ ] Wizard of Oz testing done
- [ ] Real user testing
- [ ] Error scenarios tested
- [ ] Different accents/voices tested
- [ ] Metrics baseline established

---

## References

- Designing Voice User Interfaces by Cathy Pearl
- Conversational Design by Erika Hall
- VoiceFirst.fm podcast
- Amazon Alexa Design Guide
- Google Conversation Design