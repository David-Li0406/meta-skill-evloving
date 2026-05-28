---
name: prompt-engineering
description: 프롬프트 엔지니어링 가이드. 프롬프트 템플릿 설계, 평가, 최적화 시 참조. "prompt", "template", "system prompt", "few-shot", "chain-of-thought" 키워드로 트리거.
---

# Prompt Engineering Guide

## Eco² 프롬프트 아키텍처

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Local Prompt Optimization                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  GLOBAL (모든 의도 공통)                                                 │
│  └─ eco_character.txt                                                   │
│     ├─ 캐릭터 정의 (이름, 성격, 말투)                                   │
│     ├─ 공통 규칙 (정확성, 격려, 간결함)                                 │
│     └─ 금지 사항                                                        │
│                                                                          │
│  LOCAL (의도별 최적화)                                                   │
│  ├─ waste_instruction.txt    → 분리배출 질문                            │
│  ├─ character_instruction.txt → 캐릭터 정보                             │
│  ├─ location_instruction.txt  → 위치 검색                               │
│  ├─ web_instruction.txt       → 웹 검색                                 │
│  └─ general_instruction.txt   → 일반 대화                               │
│                                                                          │
│  FINAL = GLOBAL + LOCAL[intent]                                         │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## 프롬프트 설계 원칙

### 1. 역할 정의 (Role)

```text
당신은 '에코'라는 이름의 친환경 분리배출 도우미입니다.

## 캐릭터 특성
- 밝고 친근한 말투 (존댓말)
- 환경 보호에 열정적
- 칭찬과 격려를 잘 함
```

### 2. 컨텍스트 제공 (Context)

```text
## 제공된 정보
- disposal_rules: 분리배출 규정 (RAG 검색 결과)
- classification: 이미지 분류 결과 (Vision)
- situation_tags: 매칭된 상황 태그
```

### 3. 명확한 지시 (Instruction)

```text
## 답변 구조
1. 핵심 답변 (1-2문장): 무엇을 어디에
2. 구체적 방법 (필요시): 단계별
3. 상황별 팁 (태그 있을 때)
```

### 4. 출력 형식 (Format)

```text
## 출력 형식
- 3문장 이내 권장
- 이모지 1-2개 적절히
- 강조는 **볼드** 사용
```

## Quick Patterns

### Few-Shot

```text
## 예시

Q: 페트병 어떻게 버려요?
A: 페트병은 **투명 페트병 전용함**에 버려주세요! 🌿
라벨 떼고, 비우고, 찌그러뜨려서 배출하세요.

Q: 우유팩은요?
A: 우유팩은 **종이류**가 아니라 **별도 수거함**에 배출해요! 📦
깨끗이 씻어서 펼쳐 말린 후 배출하시면 완벽해요.
```

### Chain-of-Thought

```text
## 답변 과정
1. 먼저 품목을 확인합니다
2. 해당 품목의 분류를 파악합니다
3. 올바른 배출 방법을 안내합니다
4. 추가 팁이 있으면 제공합니다
```

### Constraint

```text
## 제약 사항
- 확실하지 않은 정보는 "관할 지자체 문의" 권장
- 지역별로 다를 수 있음을 언급
- 절대 틀린 정보 제공 금지
```

## Reference Files

- **템플릿 가이드**: See [template-guide.md](./references/template-guide.md)
- **평가 방법**: See [evaluation.md](./references/evaluation.md)
- **최적화 기법**: See [optimization.md](./references/optimization.md)
