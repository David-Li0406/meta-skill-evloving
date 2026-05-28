# Resume Coach

Interactive 7-level resume coaching process that transforms generic AI-polished resumes into compelling, personalized documents.

## Overview

Most AI-assisted resume improvements produce similar results because they lack context. Resume Coach takes a different approach: instead of simply rewriting, it guides users through a structured discovery process that uncovers hidden strengths and creates genuine differentiation.

**Core Philosophy**: The goal is not to write the resume FOR you, but to help you rediscover and reframe your own experiences.

## Features

- **Recruiter Perspective Analysis**: Identifies questions a hiring manager would ask
- **Ideal Candidate Comparison**: Shows what you're competing against
- **Gap Analysis**: Reveals strengths and areas for improvement
- **High-Spec Version Generation**: Creates an aspirational benchmark (via subagent)
- **Expression Discovery**: Helps you adopt compelling framings legitimately
- **Final Resume Assembly**: Synthesizes everything into a polished result

## Installation

```bash
/plugin marketplace add xavierchoi/xavierchoi_skills
/plugin install resume-coach@xavierchoi-skills-marketplace
```

## Usage

### Trigger Phrases

**Korean:**
- "이력서 개선해줘"
- "이력서 코칭해줘"
- "서류 통과율 높이고 싶어"

**English:**
- "Help me improve my resume"
- "Coach me on my resume"
- "Review my resume for this job"

### Required Inputs

1. **Resume**: File path (`.pdf`, `.docx`, `.md`) or pasted text
2. **Job Posting**: URL, file, or pasted text

### The Coaching Process

| Phase | Level | Description |
|-------|-------|-------------|
| 1 | 3 | Recruiter perspective questions |
| 2 | 4 | Ideal candidate generation |
| 3 | 5 | Gap analysis (ideal vs. your resume) |
| 4 | 6 | High-spec version (via subagent) |
| 5 | 6.5 | Expression discovery (2nd comparison) |
| 6 | 7 | Final resume assembly |

## Components

### Skill: resume-coach

Main skill that orchestrates the entire coaching process using `AskUserQuestion` for interactive guidance.

### Agent: high-spec-generator

Generates a competitive-level resume version using only:
- Company names
- Job titles
- Employment periods

The agent deliberately does NOT see your original resume details to avoid anchoring bias, producing fresh perspectives on how achievements could be presented.

## Example Session

```
User: 이력서 코칭해줘

Claude: 이력서 코칭을 시작하겠습니다. 먼저 두 가지가 필요합니다:
1. 현재 이력서 (파일 경로나 텍스트)
2. 지원하려는 채용공고

User: [이력서와 채용공고 제공]

Claude: [Phase 1 시작 - 채용담당자 관점 질문]
"이 프로젝트에서 A를 담당하셨나요, B를 담당하셨나요?"
...
```

## Language Support

- Korean and English fully supported
- Matches user's input language
- Technical terms may remain in English

## Credits

Inspired by the LinkedIn post "ChatGPT로 서류 통과 확률 50% 이상 높이는 법" - a 7-level methodology for resume improvement.

## License

MIT
