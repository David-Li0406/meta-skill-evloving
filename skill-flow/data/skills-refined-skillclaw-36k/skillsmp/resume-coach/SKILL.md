---
name: resume-coach
description: This skill should be used when the user asks to "improve my resume", "review my resume", "help with job application", "이력서 개선해줘", "이력서 코칭해줘", "취업 준비 도와줘", "서류 통과율 높이고 싶어", or wants coaching-style resume improvement rather than simple editing. Provides an interactive 7-level resume coaching process that transforms generic resumes into compelling, personalized documents.
---

# Resume Coach: Interactive Resume Improvement Process

Transform resumes from generic AI-polished documents into compelling, personalized stories that pass recruiter screening. This skill implements a coaching methodology that helps users discover and articulate their unique value proposition.

## Overview

Most AI-assisted resume improvements produce similar results because they lack context. This skill takes a different approach: instead of simply rewriting, it guides users through a structured discovery process that uncovers hidden strengths and creates genuine differentiation.

**Core Philosophy**: The goal is not to write the resume FOR the user, but to help them rediscover and reframe their own experiences.

## Required Inputs

Before starting the process, collect:

1. **Resume**: User's current resume (file path or pasted text)
2. **Job Posting**: Target position description (URL, file, or pasted text)

If either is missing, request it before proceeding.

## The Coaching Process

### Phase 1: Recruiter Perspective Analysis (Level 3)

Analyze the resume from a hiring manager's viewpoint. Identify 3-5 questions a recruiter would ask when reviewing this resume.

**Question Types to Generate:**
- Ambiguous scope: "Did you lead this project alone or as part of a team?"
- Missing metrics: "What was the actual impact of this initiative?"
- Unclear responsibilities: "Were you responsible for A, B, or both?"
- Skill depth: "How extensively did you use this technology?"
- Gap filling: "What happened between these two positions?"

**Implementation:**
```
Use AskUserQuestion to present questions one at a time.
Collect answers to enrich the resume context.
Store responses for use in final resume.
```

### Phase 2: Ideal Candidate Generation (Level 4)

Based on the job posting, generate a fictional "ideal candidate" resume. This represents what the hiring manager imagines as the perfect fit.

**Include in the ideal candidate:**
- Relevant competitor/industry experience
- All required skills at proficiency level
- Impressive quantified achievements
- Perfect career trajectory for the role

**Present to User:**
```markdown
## Ideal Candidate Profile

Based on this job posting, here's what the hiring manager's
"dream candidate" might look like:

[Generated ideal candidate resume summary]

This helps us understand what we're competing against.
```

### Phase 3: Gap Analysis (Level 5)

Compare the user's resume against the ideal candidate. Create a structured comparison that reveals strengths and areas for improvement.

**Comparison Format:**
```markdown
| Area | Ideal Candidate | Your Resume | Analysis |
|------|-----------------|-------------|----------|
| Industry Experience | Competitor A, B | Similar Industry C | Transferable |
| Core Skills | X, Y, Z | X, Y | Highlight Z experience |
| Achievements | 50% revenue growth | Project completion | Quantify impact |
```

**Output:**
- **Strengths**: Areas where user matches or exceeds ideal
- **Opportunities**: Gaps that can be addressed with existing experience
- **Limitations**: Genuine gaps to acknowledge

### Phase 4: High-Spec Version Generation (Level 6)

This phase uses the `high-spec-generator` subagent.

**Why a Subagent?**
The subagent operates without seeing the original resume details, only:
- Company names
- Job titles
- Employment periods
- The job posting

This isolation prevents anchoring to the original resume's framing, producing fresh perspectives on how achievements could be presented.

**Invoke the Subagent:**
```
Launch high-spec-generator agent with:
- User's company names, titles, dates
- Target job posting
- Request: Generate a competitive-level resume
```

### Phase 5: Expression Discovery (Level 6.5)

Compare the high-spec version against the original resume. Help the user identify expressions and framings they can legitimately adopt.

**Present Discoveries:**
```markdown
## Expressions from High-Spec Version

The high-spec version uses these compelling framings:

1. "Drove 30% increase in team efficiency"
   → Do you have any similar efficiency improvements?

2. "Led cross-functional initiative spanning 3 departments"
   → Did you work across teams? How many stakeholders?

3. "Implemented data-driven decision framework"
   → Any analytical approaches you introduced?
```

**Use AskUserQuestion:**
For each compelling expression, ask if the user has similar experiences they haven't highlighted.

### Phase 6: Final Resume Assembly (Level 7)

Synthesize all collected information into the final resume:

1. **From Phase 1**: Specific details from recruiter-perspective questions
2. **From Phase 3**: Identified strengths to emphasize
3. **From Phase 5**: Validated expressions and framings
4. **Original tone**: Maintain the user's authentic voice

**Quality Criteria:**
- All numbers are factual (from user's answers)
- No fabricated experiences
- Expressions are adapted, not copied verbatim
- Maintains user's professional voice
- Directly addresses job posting requirements

**Output Options:**
1. Display in chat as formatted markdown
2. Save to file (offer path options)

## AskUserQuestion Integration

This skill heavily uses AskUserQuestion for interactive coaching. Follow these patterns:

**For Recruiter Questions (Phase 1):**
```json
{
  "question": "이 프로젝트에서 A를 담당하셨나요, B를 담당하셨나요, 둘 다인가요?",
  "header": "역할 명확화",
  "options": [
    {"label": "A만 담당", "description": "..."},
    {"label": "B만 담당", "description": "..."},
    {"label": "둘 다 담당", "description": "..."}
  ],
  "multiSelect": false
}
```

**For Expression Validation (Phase 5):**
```json
{
  "question": "고스펙 버전에서 '팀 효율성 30% 향상'이라는 표현이 있는데, 비슷한 성과가 있으셨나요?",
  "header": "성과 확인",
  "options": [
    {"label": "네, 비슷한 성과 있음", "description": "구체적으로 말씀해주세요"},
    {"label": "아니요, 해당 없음", "description": "다음 항목으로 넘어갑니다"}
  ],
  "multiSelect": false
}
```

## Progress Tracking

Use TodoWrite to track progress through phases:

```
[ ] Phase 1: Recruiter Perspective Questions
[ ] Phase 2: Ideal Candidate Generation
[ ] Phase 3: Gap Analysis
[ ] Phase 4: High-Spec Version (via subagent)
[ ] Phase 5: Expression Discovery
[ ] Phase 6: Final Resume Assembly
```

Update status as each phase completes.

## Language Handling

- Support both Korean and English
- Match the user's input language
- For bilingual job postings, ask user's preference
- Technical terms may remain in English regardless of language choice

## Output Format

### Final Resume Structure

```markdown
# [Name]

## Contact
[Email] | [Phone] | [LinkedIn] | [Location]

## Summary
[2-3 sentences highlighting key value proposition aligned with job posting]

## Experience

### [Job Title] | [Company]
[Start Date] - [End Date]

- [Achievement with metric from user's answers]
- [Responsibility aligned with job requirements]
- [Project highlighting relevant skills]

### [Previous Position]
...

## Skills
[Skills matching job posting requirements]

## Education
[Relevant education]
```

## Subagent Reference

This skill uses one subagent:

**high-spec-generator**: Generates a competitive-level resume version using only company names, titles, and dates. Located in `agents/high-spec-generator.md`.

## Tips for Effective Coaching

1. **Don't rush**: Each phase builds on the previous one
2. **Validate everything**: Never assume or fabricate details
3. **Respect user's voice**: Adapt framings, don't impose them
4. **Focus on alignment**: Always tie back to job requirements
5. **Be honest about gaps**: Some gaps are real and that's okay

## Error Handling

**Missing resume:**
"이력서를 먼저 공유해주세요. 파일 경로나 텍스트를 직접 붙여넣어도 됩니다."

**Missing job posting:**
"어떤 포지션에 지원하시나요? 채용공고 URL이나 내용을 공유해주세요."

**Incomplete answers:**
If user skips questions, note the gap and proceed. Missing context will be reflected in final output quality.
