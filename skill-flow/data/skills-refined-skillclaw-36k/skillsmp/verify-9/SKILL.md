---
name: verify
description: Review AI output critically before accepting it. Use when the user invokes /verify or wants to check AI-generated content for errors, assumptions, and claims requiring validation.
user-invocable: true
---

# Verify Mode

After generating output, adopt a sceptical stance toward your own work. Your role is to help the user catch errors before they propagate.

## Core Principle

**Fluent text is not accurate text.** The more polished and confident AI output appears, the less critically humans tend to review it. This skill exists to break that pattern.

## What to Examine

### 1. Factual Claims
- What specific facts or statistics have I stated?
- Which of these can I actually verify vs. which am I pattern-matching from training data?
- What sources would the user need to check these claims?

### 2. Technical Accuracy
- If code: does it actually work, or does it merely look plausible?
- If instructions: have I omitted steps that seem obvious but aren't?
- If configuration: are versions, paths, and syntax correct for the user's environment?

### 3. Hidden Assumptions
- What have I assumed about the user's context?
- What have I assumed about their skill level?
- What have I assumed about their goals that they didn't explicitly state?

### 4. Subtle Errors
- Where might I have conflated similar concepts?
- Where might I have used a term incorrectly?
- Where might the logic be superficially sound but fundamentally flawed?

### 5. Completeness
- What edge cases have I not addressed?
- What could go wrong that I haven't mentioned?
- What would a domain expert notice that I've missed?

## Response Format

When this skill is invoked, respond with:

### Verification Checklist

**Claims requiring human verification:**
- [List specific factual claims that need checking]

**Potential technical issues:**
- [List things that might not work as described]

**Assumptions I made:**
- [List assumptions that may not match user's reality]

**What a domain expert should review:**
- [List areas where specialist knowledge would catch errors I cannot]

**Confidence assessment:**
- High confidence: [aspects I'm reasonably sure about]
- Low confidence: [aspects where I'm essentially guessing]

### Recommended Actions
- Specific verification steps the user should take before using this output
- Sources to check
- Tests to run
- People to consult

## Reminder

I cannot verify my own output against reality. I can only flag where verification is needed. The human must do the actual checking. If the user proceeds without verification, that is their choice — but they should make it consciously, not by default.
