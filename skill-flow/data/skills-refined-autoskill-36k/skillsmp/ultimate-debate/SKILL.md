---
name: ultimate-debate
description: "3AI 병렬 분석 및 합의 판정 시스템"
version: "2.0.0"
author: "Claude Code"

triggers:
  keywords:
    - "토론"
    - "debate"
    - "합의"
    - "다중 AI"
    - "3AI 분석"
    - "교차 검토"
  file_patterns:
    - ".claude/debates/**/*.md"
  context:
    - "복잡한 설계 결정"
    - "여러 관점 필요"
    - "아키텍처 결정"
    - "전략 수립"

capabilities:
  - multi_ai_parallel
  - consensus_building
  - round_based_debate
  - context_management
  - strategy_patterns

model_preference: opus
phase: [1, 2]
auto_trigger: false
token_budget: 5000
---

# Ultimate Debate Skill

**Type**: Cross-AI Consensus Verifier
**Status**: Phase 2 - Hybrid Architecture

## 개요

3개 AI(Claude, GPT, Gemini)가 병렬 분석 → 교차 검토 → 합의 판정 → 재토론을 반복하여 최종 합의안을 도출하는 스킬입니다.

## 핵심 기능

| 기능 | 설명 |
|------|------|
| **병렬 분석** | 3 AI가 동시에 독립적으로 분석 |
| **교차 검토** | 서로의 분석 결과 리뷰 |
| **합의 판정** | 해시 기반 결론 비교로 합의 체크 |
| **재토론** | 불일치 시 근거 기반 토론 |
| **Context 관리** | MD 파일로 히스토리 저장 (메인 Context 절약) |

## 5-Phase 워크플로우

```
Phase 1: 병렬 분석 (3 AI 동시)
    ↓
Phase 2: 초기 합의 체크 (해시 비교)
    ↓
Phase 3: 교차 검토 (합의 실패 시)
    ↓
Phase 4: 재토론 (불일치 해결)
    ↓
Phase 5: 최종 전략 수립
```

## 디렉토리 구조 (Hybrid Architecture)

### Core Engine (독립 패키지)
```
packages/ultimate-debate/
├── pyproject.toml
├── src/ultimate_debate/
│   ├── engine.py               # 메인 토론 엔진
│   ├── comparison/             # 3-Layer 비교 시스템
│   ├── consensus/              # 합의 프로토콜
│   ├── strategies/             # 전략 패턴
│   └── storage/                # Context 관리
└── tests/
```

### Skill Layer (Claude Code 통합)
```
.claude/skills/ultimate-debate/
├── SKILL.md
├── requirements.txt
└── scripts/
    ├── main.py                 # CLI 엔트리포인트
    ├── adapter.py              # Core Engine 어댑터
    └── debate/                 # 레거시 (fallback)
```

## 사용법

### CLI 사용

```bash
# 새 토론 시작
python .claude/skills/ultimate-debate/scripts/main.py --task "API 리팩토링 전략"

# 상태 확인
python .claude/skills/ultimate-debate/scripts/main.py --status --task-id debate_20260118_abc123

# 옵션 설정
python .claude/skills/ultimate-debate/scripts/main.py \
  --task "보안 감사" \
  --max-rounds 3 \
  --threshold 0.9 \
  --output text
```

## Context 관리 시스템

모든 토론 히스토리는 MD 파일로 저장되어 메인 Context를 절약합니다.

```
.claude/debates/{task_id}/
├── TASK.md                      # 초기 작업 설명
├── round_00/
│   ├── claude.md                # Claude 분석
│   ├── gpt.md                   # GPT 분석
│   └── gemini.md                # Gemini 분석
└── FINAL.md                     # 최종 합의안
```

## 합의 상태

| 상태 | 조건 | 다음 액션 |
|------|------|-----------|
| `FULL_CONSENSUS` | ≥ 80% 일치 | None (종료) |
| `PARTIAL_CONSENSUS` | 50-80% 일치 | CROSS_REVIEW |
| `NO_CONSENSUS` | < 50% 일치 | DEBATE |

## 설치 방법

```bash
# Core Engine 설치 (개발 모드)
cd C:\claude\packages\ultimate-debate
pip install -e .

# 테스트 실행
python -m pytest tests/ -v
```

## 관련 문서

- PRD: `tasks/prds/PRD-0035-multi-ai-consensus-verifier.md`
- Cross-AI Verifier: `.claude/skills/cross-ai-verifier/`

---

**Last Updated**: 2026-01-19
**License**: MIT
