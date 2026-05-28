---
name: job-search-helper
description: Help with job search tasks like analyzing JDs, comparing jobs, understanding requirements, or preparing for interviews
---

# Job Search Assistant

When helping with job search tasks, use the patterns established in `src/utils/prompts.ts`.

## JD Analysis

- Parse job descriptions to extract company, title, requirements, nice-to-haves
- Identify key skills and experience levels
- Note salary and job type (remote/hybrid/onsite)
- Use `JD_ANALYSIS_PROMPT` pattern for structured extraction

## Resume Matching

- Compare candidate skills against JD requirements
- Identify gaps and strengths with specific evidence
- Suggest ways to position experience
- Use `RESUME_GRADING_PROMPT` pattern for scoring

## Cover Letter Generation

- Match tone to company culture
- Highlight relevant experience from resume
- Include honesty guidelines - never fabricate
- Use `COVER_LETTER_PROMPT` pattern

## Interview Prep

- Generate likely behavioral questions (STAR format)
- Prepare technical discussion points
- Suggest questions to ask interviewer
- Use `INTERVIEW_PREP_PROMPT` and `QA_SYSTEM_PROMPT` patterns

## Resume Tailoring

- Use `AUTO_TAILOR_PROMPT` for initial tailoring
- Use `REFINE_RESUME_SYSTEM_PROMPT` for iterative refinement
- Never fabricate - only reframe existing experience
- Apply learned improvements from previous tailoring sessions

## Key Files

- `src/utils/prompts.ts` - All prompt templates
- `src/services/ai.ts` - AI integration (callAI function)
- `src/types/index.ts` - Job, JobSummary, ResumeAnalysis types
