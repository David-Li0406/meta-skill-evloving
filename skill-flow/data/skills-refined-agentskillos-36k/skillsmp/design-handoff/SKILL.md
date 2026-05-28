---
name: design-handoff
description: Generate design-to-development handoff documents. Use when (1) preparing designs for developers, (2) documenting component specifications, (3) creating style guides, (4) bridging design and code. Creates comprehensive handoff documents.
tools: [Write, Read, mcp_Framelink]
---

> **🔔 시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: design-handoff 호출 - 핸드오프 문서 생성` 시스템 메시지를 첫 줄에 출력하세요.

# design-handoff Skill

> 디자인-개발 협업을 위한 핸드오프 문서 생성

## 역할

디자인 스펙을 개발자가 이해하고 구현할 수 있는 형태로 문서화합니다.
Claude Code와 Antigravity 간의 정보 전달 브릿지 역할도 수행합니다.

## 트리거

- `/SEMO:handoff` 명령어
- "핸드오프", "개발 전달", "스펙 문서" 키워드
- design-master Agent에서 호출

## Quick Start

```markdown
사용자: "로그인 폼의 핸드오프 문서 만들어줘"

[SEMO] Skill: design-handoff 호출 - 핸드오프 문서 생성

## 디자인 분석
- 대상: 로그인 폼
- 소스: generate-mockup 결과 / Figma 링크

[핸드오프 문서 생성]

✅ design-handoff.md 생성 완료
```

## 프로세스

### Step 1: 소스 식별

입력 유형 확인:
- generate-mockup 결과
- Figma 링크
- 기존 컴포넌트 코드
- 구두 설명

### Step 2: 스펙 추출

Figma 소스인 경우 Framelink MCP 활용

### Step 3: 문서 생성

템플릿에 맞춰 핸드오프 문서 작성

### Step 4: 파일 저장

저장 위치: `docs/handoff/{component-name}-handoff.md`

## References

- [Handoff Template](references/handoff-template.md) - 핸드오프 문서 전체 템플릿
- [Design Sections](references/design-sections.md) - 각 섹션 상세 가이드
- [Antigravity Bridge](references/antigravity-bridge.md) - Claude Code ↔ Antigravity 연동

## Related

- [design-master Agent](../../agents/design-master/design-master.md)
- [generate-mockup Skill](../generate-mockup/SKILL.md)
