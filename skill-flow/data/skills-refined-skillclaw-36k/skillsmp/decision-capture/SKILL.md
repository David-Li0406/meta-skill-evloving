---
name: decision-capture
description: Detects and captures technical decisions during conversations. Use when architectural choices, library selections, design patterns, API designs, or trade-off decisions are made. Automatically prompts user to save decisions as ADR files.
---

# Decision Capture

## Trigger Conditions
다음 상황에서 결정 사항을 감지:
- 아키텍처 또는 설계 패턴 선택
- 라이브러리/프레임워크 선택
- API 설계 방향 결정
- 트레이드오프가 있는 구현 방식 선택
- 컨벤션 또는 규칙 수립

## Required Behavior
결정 사항이 감지되면, 구현 전에 반드시:

1. 결정을 인식했음을 알림
2. 사용자가 왜 이 결정을 내렸는지 명확해질때까지 AskUserQuestion tool을 이용해서 추가 질문
3. 사용자에게 저장 여부를 AskUserQuestion tool을 통해 확인 (e.g. docs/decisions/`에 저장할까요?)

> 💡 **결정 사항 감지됨**
> - 제목: [결정 제목]
> - 요약: [한 줄 요약]
> - 컨텍스트: [결정에 영향을 준 주요 요인들]
> - 결정을 내린 이유: [Bullet point로 결정한 이유 나열]

4. 동의 시 ADR 형식으로 저장

## ADR Format
파일명: `YYYY-MM-DD-NNN-slug.md`
위치: `docs/decisions/`

필수 섹션: 제목, 상태, 컨텍스트, 결정, 결과, 대안들
