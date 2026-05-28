---
name: experts
description: This skill should be used when the user explicitly wants authoritative domain expertise applied to their task - seeking guidance from renowned practitioners, specialists, or thought leaders rather than a generic response. The user's intent is to leverage professional perspectives to enhance their request. Do NOT trigger on general help requests where the user simply wants the task done.
version: 0.1.0
---

# Expert-Enhanced Prompt System

Transform simple user requests into expert-informed prompts by discovering relevant domain experts and applying their perspectives to enhance the original request.

## When This Skill Applies

Activate this skill when the user's **intent** is to leverage professional expertise:

**Trigger signals:**
- Mentions experts, specialists, professionals, thought leaders, gurus, 대가, 석학, 프로 등
- Wants "professional perspective" or "expert opinion"
- Asks to approach something "like a pro" or "전문가처럼"
- Seeks authoritative guidance beyond generic help

**Example triggers:**
- "전문가랑 같이 블로그 글 써줘"
- "프로처럼 마케팅 전략 세워줘"
- "get expert help with my presentation"
- "approach this like a specialist would"

**Do NOT activate** when the user simply wants the task done without seeking expert methodology.

## Core Workflow

### Phase 1: Analyze the Request

Parse the user's request to identify:

1. **Domain**: What field or discipline does this request belong to?
2. **Intent**: What is the user actually trying to accomplish?
3. **Implicit needs**: What unstated requirements might exist?
4. **Quality markers**: What would make the output excellent vs. mediocre?

### Phase 2: Discover Domain Experts

Conduct a web search to find 2-3 renowned experts whose work relates to the request.

**Search Strategy**:
- Search for: `"best [domain] experts"`, `"famous [domain] practitioners"`, `"[domain] thought leaders"`
- Look for experts known for distinctive methodologies or frameworks
- Prioritize experts with published works, established reputations, or unique approaches
- Seek diversity in perspectives (academic vs. practitioner, traditional vs. innovative)

**For Each Expert, Gather**:
- Name and brief background
- Their signature approach or methodology
- Key principles they advocate
- What makes their perspective unique

### Phase 3: Present Experts to User

Present the discovered experts with concise profiles:

```
## Discovered Experts

### 1. [Expert Name]
**Background**: [1-2 sentence description]
**Known For**: [Their signature methodology or approach]
**Perspective**: [How they would approach this type of task]

### 2. [Expert Name]
...

### 3. [Expert Name]
...
```

Then ask the user to select which expert perspective(s) to apply.

### Phase 4: Generate Enhanced Prompt

Based on user selection, create an enhanced prompt that incorporates:

1. **Expert's Framework**: Apply their methodology to structure the task
2. **Quality Standards**: What this expert would consider essential
3. **Specific Techniques**: Approaches this expert is known for
4. **Success Criteria**: How the expert would evaluate the output

**Enhanced Prompt Structure**:

```
## Enhanced Prompt (Based on [Expert Name]'s Approach)

### Context
[Expanded context based on expert's domain understanding]

### Task
[Refined task description using expert's terminology and framework]

### Approach
[Step-by-step methodology aligned with expert's known techniques]

### Quality Criteria
[Standards and evaluation metrics the expert would apply]

### Expected Output
[Specific deliverable description with expert-level expectations]
```

## Expert Discovery Guidelines

### Effective Expert Search Patterns

| Domain | Search Terms |
|--------|--------------|
| Writing/Content | "best copywriters", "famous authors [genre]", "content strategy experts" |
| Business/Strategy | "top business strategists", "renowned CEOs", "management thought leaders" |
| Technology | "influential developers", "tech visionaries", "software architecture experts" |
| Design | "famous designers", "UX pioneers", "design thinking leaders" |
| Marketing | "legendary marketers", "brand strategy experts", "growth hackers" |

### Expert Selection Criteria

Select experts who:
- Have demonstrable track records in the relevant domain
- Offer distinct, well-documented methodologies
- Represent different schools of thought when possible
- Have insights applicable to the user's specific context

### Avoiding Poor Expert Matches

Do not select:
- Generic "influencers" without substantive expertise
- Experts whose work is unrelated to the actual request
- Controversial figures without clear professional merit
- Fictional or unverifiable personas

## Prompt Enhancement Principles

### From Vague to Specific

Transform ambiguous requests into precise specifications:

| Original | Enhanced |
|----------|----------|
| "Write a blog post" | "Create a 1,500-word thought leadership article using [Expert]'s inverted pyramid structure, opening with a counterintuitive insight..." |
| "Help me with my presentation" | "Design a presentation following [Expert]'s rule of three, with one key message per slide and visual-first storytelling..." |

### Adding Expert Methodology

Incorporate the expert's known frameworks:

- **Structure**: How they organize information
- **Voice**: Characteristic tone and style
- **Priorities**: What they emphasize most
- **Techniques**: Specific methods they employ

### Preserving User Intent

The enhanced prompt must:
- Maintain the user's original goal
- Not add unwanted scope or complexity
- Respect any constraints the user mentioned
- Be executable with available resources

## User Interaction Flow

1. **Receive request** → Acknowledge and begin analysis
2. **Search experts** → Conduct web search, compile findings
3. **Present options** → Show expert profiles with clear differentiators
4. **Get selection** → User chooses perspective(s) to apply
5. **Deliver enhanced prompt** → Provide the transformed prompt
6. **Offer to execute** → Ask: "이 향상된 프롬프트를 바로 실행할까요?"
7. **Auto-execute if approved** → If user confirms, immediately execute the enhanced prompt

### Auto-Execution Protocol

When the user approves execution:

1. Treat the enhanced prompt as if the user had submitted it directly
2. Begin working on the task using the expert's methodology
3. Apply all quality criteria and frameworks specified in the enhanced prompt
4. Deliver the final output according to the enhanced specifications

**Example dialogue:**
```
User: "블로그 글 써줘"
Claude: [전문가 검색 및 프롬프트 향상 진행]
Claude: "Cal Newport의 관점으로 향상된 프롬프트를 준비했습니다. 바로 실행할까요?"
User: "응"
Claude: [향상된 프롬프트에 따라 블로그 글 작성 시작]
```

## Additional Resources

### Reference Files

For detailed patterns and examples, consult:
- **`references/enhancement-patterns.md`** - Common enhancement patterns by domain
- **`examples/before-after.md`** - Example transformations showing original vs. enhanced prompts

## Quality Standards

A well-enhanced prompt should:

- [ ] Clearly reflect the chosen expert's methodology
- [ ] Be significantly more specific than the original
- [ ] Include actionable structure and guidance
- [ ] Define clear success criteria
- [ ] Remain true to the user's original intent
- [ ] Be immediately usable without further clarification
