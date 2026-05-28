# conversation patterns

multi-turn flow examples showing how questions chain and build.

## example 1: saya ack behavior fix

real conversation flow from debugging saya's "on it~" and "yo #channel" issues.

### round 1: exploration

```yaml
questions:
  - question: "how should we fix the 'on it~' ack problem?"
    header: "ack fix"
    options:
      - label: "context-aware ack (Recommended)"
        description: "generate acks based on message content, user relationship, channel vibe"
      - label: "remove acks entirely"
        description: "let reactions do the acknowledgment work"
      - label: "template variety"
        description: "cycle through varied templates randomly"

  - question: "how should we fix the 'yo #channel' pattern?"
    header: "greeting fix"
    options:
      - label: "remove channel echo"
        description: "don't announce location, just respond naturally"
      - label: "context-aware greeting"
        description: "vary greeting based on relationship + channel type"
      - label: "both"
        description: "remove echo AND make greetings context-aware"
```

**user answered**: "context-aware ack" + "both but also similar to ack - onboarding outputs need to be tier and context aware"

### round 2: drilling into context signals

based on "context-aware" theme, explore what context means:

```yaml
questions:
  - question: "for context-aware outputs, what context signals should drive personalization?"
    header: "context"
    multiSelect: true
    options:
      - label: "user relationship tier (Recommended)"
        description: "new user vs familiar vs close collaborator"
      - label: "channel type"
        description: "public vs private vs DM vs thread"
      - label: "workspace culture"
        description: "formal org vs casual team vs personal space"
      - label: "all of the above"
        description: "full context stack, agent decides weight"

  - question: "how dynamic should the tier system be?"
    header: "tier dynamics"
    options:
      - label: "static tiers"
        description: "defined upfront, rarely change"
      - label: "relationship progression"
        description: "tiers evolve based on interaction history"
      - label: "context blend"
        description: "mix of all signals, model decides"

  - question: "should acks ever be skipped entirely when reaction is sufficient?"
    header: "ack skip"
    options:
      - label: "always ack"
        description: "verbal acknowledgment every time"
      - label: "model decides"
        description: "agent determines if ack adds value"
      - label: "reaction only"
        description: "skip acks, reactions are enough"
```

**user answered**: "all of the above" + custom input about agentic awareness step + "model decides"

### round 3: onboarding flow design

answers reveal need for onboarding-specific flow:

```yaml
questions:
  - question: "how should the onboarding awareness agent work?"
    header: "onboarding"
    options:
      - label: "pre-analysis ack + full onboarding (Recommended)"
        description: "quick contextual ack (wave + 'checking out the vibe'), then full analysis"
      - label: "silent analysis + single intro"
        description: "analyze silently, then one well-crafted intro message"
      - label: "async digest style"
        description: "join silently, observe 5-10 min, then introduce with observations"

  - question: "what channel types need special handling?"
    header: "channel type"
    multiSelect: true
    options:
      - label: "public channels"
        description: "more formal, observe before engaging"
      - label: "private channels"
        description: "closer relationship, can be warmer"
      - label: "DMs"
        description: "most personal, full personality"
      - label: "threads"
        description: "contextual to parent message"

  - question: "how should onboarding scope be determined?"
    header: "scope"
    options:
      - label: "always full analysis"
        description: "comprehensive context gathering every time"
      - label: "reuse + augment"
        description: "check for existing analysis, add new context only"
      - label: "progressive"
        description: "light analysis first, deepen as needed"
```

### round 4: meta + synthesis

step back, check for gaps:

```yaml
questions:
  - question: "we've covered acks, tiers, onboarding, and channel types. what's missing?"
    header: "gaps"
    options:
      - label: "nothing, ready to implement"
        description: "clear picture, let's build"
      - label: "testing strategy"
        description: "how do we verify this works in prod?"
      - label: "rollback plan"
        description: "what if users hate the new behavior?"
      - label: "monitoring"
        description: "how do we track what's landing?"
```

**synthesis**:
```
based on your answers:
1. context-aware acks using tier + channel + culture signals
2. model decides when to skip ack (reaction sufficient)
3. onboarding: quick contextual wave, then full analysis
4. reuse existing analysis, augment with new context

ready to proceed, or dig deeper on any point?
```

---

## example 2: feature planning (new API endpoint)

### round 1: scope

```yaml
question: "what's the core use case for this endpoint?"
header: "use case"
options:
  - label: "internal tooling"
    description: "admin dashboard, debugging, ops"
  - label: "public API"
    description: "third-party integrations, external devs"
  - label: "mobile client"
    description: "iOS/android app consumption"
  - label: "other services"
    description: "service-to-service within our infra"
```

### round 2: trade-offs

after user says "internal tooling":

```yaml
question: "what matters most for internal tooling?"
header: "priority"
options:
  - label: "speed to ship (Recommended)"
    description: "get it working, iterate later"
  - label: "flexibility"
    description: "handle many query patterns"
  - label: "observability"
    description: "easy to debug and monitor"
```

### round 3: technical

```yaml
question: "auth approach?"
header: "auth"
options:
  - label: "existing session (Recommended)"
    description: "reuse current auth middleware"
  - label: "API key"
    description: "separate credential for tooling"
  - label: "service account"
    description: "machine-to-machine auth"
```

---

## example 3: debugging flow

### round 1: confirmation

```yaml
question: "found the error in spawn.ts:145. is this the right area?"
header: "location"
options:
  - label: "yes, that's it (Recommended)"
    description: "fix the spawn logic"
  - label: "no, symptom not cause"
    description: "trace back to actual source"
  - label: "show me the code first"
    description: "need to see context before deciding"
```

### round 2: root cause

after user confirms:

```yaml
question: "what's causing the issue?"
header: "root cause"
options:
  - label: "race condition"
    description: "timing issue between operations"
  - label: "missing validation"
    description: "bad input not caught"
  - label: "state corruption"
    description: "data got into bad state"
  - label: "not sure yet"
    description: "need to investigate more"
```

### round 3: fix approach

```yaml
question: "how should we fix it?"
header: "fix"
options:
  - label: "targeted patch (Recommended)"
    description: "fix this specific case, minimal changes"
  - label: "defensive refactor"
    description: "add guards throughout the flow"
  - label: "redesign"
    description: "rethink the approach entirely"
```

---

## chaining principles

### build on keywords

user says "tier" → next question explores tier dimensions
user says "context" → next question asks which context signals
user says "like X" → run tools to understand X, then ask comparison questions

### escalate complexity

start simple, add dimensions as answers reveal depth:
- round 1: binary or single-dimension
- round 2: multi-select, trade-offs surface
- round 3: sequences, edge cases
- round 4: meta, synthesis

### know when to stop

- user gives short answers → they're ready to proceed
- answers repeat themes → consensus reached
- user says "let's do it" → stop asking, start building

### respect "other"

when user types custom answer:
- acknowledge the insight
- integrate into next question
- don't force back to predefined options
