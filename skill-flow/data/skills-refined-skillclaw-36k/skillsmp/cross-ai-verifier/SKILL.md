---
name: cross-ai-verifier
description: "다중 AI 모델을 통한 코드 검증 (OpenAI + Gemini)"
version: "2.0.0"
author: "Claude Code"

triggers:
  keywords:
    - "검증"
    - "verify"
    - "GPT 리뷰"
    - "Gemini 검토"
    - "교차 검증"
    - "외부 AI"
  file_patterns:
    - "src/**/*.py"
    - "src/**/*.ts"
    - "**/*.tsx"
    - "**/*.jsx"
  context:
    - "코드 품질 검증"
    - "외부 AI 리뷰"
    - "보안 취약점 분석"

capabilities:
  - parallel_verification
  - security_analysis
  - bug_detection
  - performance_review

model_preference: opus
phase: [4, 5]
auto_trigger: false
token_budget: 3000
---

# Cross-AI Verifier Skill

Claude가 작성한 코드를 외부 AI(GPT, Gemini)가 교차 검증합니다.

## 사용법

```bash
# 단일 Provider 검증
/verify src/auth.py --focus security --provider openai
/verify tests/ --focus bugs --provider gemini

# 병렬 검증 (OpenAI + Gemini 동시)
/verify --all src/ --parallel
```

## 지원 Provider

| Provider | 모델 | 인증 |
|----------|------|------|
| **OpenAI** | GPT-4 | OAuth 토큰 (ai-login 스킬) |
| **Gemini** | Gemini Pro | OAuth 토큰 (ai-login 스킬) |

## 검증 Focus

| Focus | 설명 |
|-------|------|
| `security` | 보안 취약점 분석 (SQL Injection, XSS 등) |
| `bugs` | 논리 오류 및 버그 검사 |
| `performance` | 성능 이슈 및 최적화 제안 |
| `all` | 종합 코드 리뷰 |

## 인증 설정

```bash
# OAuth 로그인 (권장)
/ai-login openai
/ai-login gemini
```

## 관련 문서

- [AI Login Skill](../ai-login/SKILL.md)
- [PRD-0035](../../../tasks/prds/PRD-0035-multi-ai-consensus-verifier.md)
