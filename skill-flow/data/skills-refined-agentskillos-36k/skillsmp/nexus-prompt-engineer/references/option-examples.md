# Option Design Examples

The core of low-friction interaction is replacing open-ended questions with scenario-based options.

## Design Principles

1. **Scenario-based**: Options should describe concrete scenarios, not abstract labels
2. **Mutually exclusive**: Clear distinction between options to reduce user confusion
3. **Comprehensive**: Cover main cases, add "Other" option when necessary
4. **Brief**: Keep each option within one line

## Common Option Templates

### Target Audience

```
Regarding target audience:
  A. Industry experts (use professional terminology, deep analysis, skip basics)
  B. Beginners/General public (plain language, use analogies and examples)
  C. Executives (lead with conclusions, emphasize ROI and strategic value)
  D. Cross-functional colleagues (balance expertise, explain key terms)
```

### Output Format

```
Regarding output format:
  A. Structured report (headings, sections, bullet lists)
  B. Email/Message copy (conversational, natural, friendly)
  C. Code or JSON (strict syntax, no extra explanation)
  D. Conversational response (natural flow, no sections)
```

### Content Depth

```
Regarding content depth:
  A. Quick overview (core points, 3-minute read)
  B. Standard detail (complete logic, 10-minute read)
  C. Deep analysis (fully developed, with cases and data)
```

### Tone Style

```
Regarding tone style:
  A. Formal and rigorous (suitable for business/academic contexts)
  B. Friendly and relaxed (suitable for daily communication/internal sharing)
  C. Inspiring and motivating (suitable for speeches/rallies/marketing)
  D. Direct and sharp (suitable for feedback/criticism/urgent communication)
```

### AI Role Positioning

```
Regarding AI role:
  A. Domain expert (deep expertise, can use jargon and industry conventions)
  B. Senior consultant (strategic perspective, weigh pros and cons, give advice)
  C. Coach/Mentor (guide thinking, ask Socratic questions)
  D. Execution assistant (directly complete tasks, minimal explanation)
```

### Success Criteria

```
Regarding success criteria:
  A. Get actionable concrete steps
  B. Deep understanding of principles and logic
  C. Persuade others to accept a viewpoint
  D. Quickly get usable results
```

## User Response Format

Guide users to reply in brief format:

- Single choice: `1A` or `Question 1: A`
- Multiple choice: `1AB, 2C` or `1A+B, 2C`
- With notes: `1A (Note: my audience is product managers)`

## Anti-Patterns

**❌ Open-ended questions (avoid)**:
- "Please provide more details"
- "Who is your audience?"
- "What style do you want?"
- "Can you be more specific?"

**✅ Scenario-based options (recommended)**:
- All option templates above
