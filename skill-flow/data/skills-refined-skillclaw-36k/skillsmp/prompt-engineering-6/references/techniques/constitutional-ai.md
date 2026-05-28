# Constitutional AI (Self-Critique)

Built-in quality control loop. Generate, critique, revise.

## Template

```xml
<task>
[Task requiring quality control]
</task>

<phase_1_generate>
Generate initial response.
</phase_1_generate>

<phase_2_critique>
Review against criteria:
- [ ] Accurate and factual
- [ ] Complete (all requirements)
- [ ] Safe (no harmful content)
- [ ] Appropriate tone
- [ ] Correct format

Issues found:
- Issue 1: [Description]
- Issue 2: [Description]
</phase_2_critique>

<phase_3_revise>
Fix identified issues.
Explain each change.
</phase_3_revise>

<final_output>
[Improved response]
</final_output>
```

## Example

```xml
<task>
Write a product description for our new AI writing tool, targeting small business owners.
</task>

<phase_1_generate>
Introducing WriteBot Pro - the revolutionary AI-powered writing assistant that will transform your business forever! Our cutting-edge neural networks produce flawless content in seconds. Say goodbye to writer's block and hello to unlimited productivity!
</phase_1_generate>

<phase_2_critique>
Review:
- [ ] Accurate: FAIL - "flawless" and "unlimited" are overclaims
- [x] Complete: OK - covers main benefit
- [x] Safe: OK - no harmful content
- [ ] Tone: FAIL - too hyperbolic for small business audience
- [x] Format: OK

Issues:
1. Overclaims ("flawless", "unlimited", "revolutionary")
2. Tone too aggressive for target audience
3. Missing concrete benefit/use case
</phase_2_critique>

<phase_3_revise>
Changes made:
1. Removed superlatives → replaced with specific benefits
2. Softened tone → more conversational
3. Added concrete use case → emails, social posts
</phase_3_revise>

<final_output>
Meet WriteBot Pro - your AI writing partner for everyday business tasks. Draft emails, social posts, and customer responses in minutes instead of hours. Built for busy small business owners who want quality content without the time investment.
</final_output>
```

## When to Use

- Public-facing content
- Legal/compliance documents
- Safety-critical outputs
- When accuracy is paramount
- Content that will be widely distributed

## When NOT to Use

- Internal/draft content
- Speed is priority
- Low-stakes outputs
- Creative brainstorming (critique kills creativity)
