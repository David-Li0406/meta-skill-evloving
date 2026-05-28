---
name: version-manager
description: SEMO 패키지 시맨틱 버저닝 자동화. Use when (1) Agent/Skill/Command 변경 후 릴리스, (2) VERSION 및 CHANGELOG 업데이트, (3) Keep a Changelog 형식 버전 관리.
tools: [Bash, Read, Write, Edit]
---

> **🔔 시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: version-manager 호출 - {버전 타입}` 시스템 메시지를 첫 줄에 출력하세요.

# version-manager Skill

> SEMO 패키지 버저닝 자동화 Skill

---

## 🔴 NON-NEGOTIABLE: 버저닝 완료 조건

> **⚠️ 아래 체크리스트를 모두 완료해야 버저닝 완료로 간주합니다. 하나라도 누락 시 미완료 상태입니다.**

### 필수 완료 체크리스트

| # | 단계 | 완료 확인 메시지 |
|---|------|-----------------|
| 1 | VERSION 파일 업데이트 | `[SEMO] Versioning: {old} → {new}` |
| 2 | CHANGELOG 생성 | `✓ CHANGELOG/{version}.md 생성` |
| 3 | 커밋 | `[SEMO] Versioning: 커밋 완료` |
| 4 | 푸시 | `[SEMO] Versioning: 푸시 완료` |
| **5** | **🔴 Slack 알림** | `[SEMO] Versioning: Slack 알림 전송 완료` |
| 6 | (semo-meta만) 로컬 동기화 | `[SEMO] Versioning: 로컬 동기화 완료` |

### 자동 체인 실행

버저닝 푸시 완료 즉시 **자동으로** 체인 스킬을 호출합니다:

```text
git push 성공
    ↓
[자동] notify-slack Skill 호출
    ↓
Slack 알림 전송 완료
    ↓
[자동] changelog-writer Skill 호출 (MAJOR/MINOR만)
    ↓
블로그 원고 생성
    ↓
버저닝 완료
```

**⚠️ Slack 알림 없이 "버저닝 완료"라고 말하지 마세요.**

### 블로그 원고 자동 생성 (선택)

MAJOR 또는 MINOR 버전 변경 시 `changelog-writer`가 자동 호출됩니다:

| 버전 유형 | 원고 생성 |
|----------|----------|
| MAJOR | ✅ 자동 |
| MINOR (기능 추가) | ✅ 자동 |
| PATCH | ❌ 스킵 |

원고 위치: `docs/blog/drafts/{YYYY-MM-DD}-{package}-{version}.md`

---

## Purpose

SEMO 패키지의 Semantic Versioning 관리를 자동화합니다.

- VERSION 파일 업데이트
- CHANGELOG/{version}.md 파일 생성
- CHANGELOG/INDEX.md 업데이트
- Keep a Changelog 형식 준수

## Quick Start

```bash
# 1. 현재 버전 확인
cat sax/VERSION

# 2. 변경사항 분석 후 버전 타입 결정 (MAJOR/MINOR/PATCH)

# 3. VERSION 업데이트
echo "3.15.0" > sax/VERSION

# 4. CHANGELOG 생성
# sax/CHANGELOG/{version}.md 파일 작성

# 5. 커밋 & 푸시
git add -A && git commit -m "🔖 [SEMO] 3.15.0: {변경 요약}"
git push origin main

# 6. 🔴 Slack 알림 (필수) - 아래 섹션 참조
```

## Semantic Versioning 요약

| 버전 | 트리거 | 예시 |
|------|--------|------|
| **MAJOR** | 호환성 깨지는 변경 | 워크플로우 근본 변경 |
| **MINOR** | 기능 추가/삭제 | Agent/Skill 추가, CLAUDE.md 변경 |
| **PATCH** | 버그/오타 수정 | 문서 보완, 성능 개선 |

## 📣 피드백 이슈 연동 (선택)

> **사용자 피드백 기반 버저닝 시, 피드백 작성자에게 알림**

### 자동 감지

커밋 메시지에 피드백 이슈 참조가 있는 경우 자동으로 처리합니다:

| 패턴 | 예시 |
|------|------|
| `#이슈번호` | `#123` |
| `Fixes #이슈번호` | `Fixes #45` |
| `Closes #이슈번호` | `Closes #78` |

### 피드백 이슈 판별 조건

다음 조건을 **모두** 만족해야 피드백 이슈로 판별합니다:

1. 이슈에 `bug` 또는 `enhancement` 라벨 존재
2. 이슈가 `semo-core/skills/feedback`에 의해 생성됨 (본문에 SEMO Feedback Skill 표시)

### 처리 흐름

```text
1. 커밋 메시지에서 이슈 번호 추출
   ↓
2. 이슈 정보 조회 (gh issue view)
   ↓
3. 피드백 이슈 여부 판별
   ├─ 아님 → 일반 버저닝 완료
   └─ 맞음 → 아래 단계 진행
   ↓
4. 이슈 작성자 조회
   ↓
5. GitHub 이슈에 완료 코멘트 추가 (@작성자 멘션)
   ↓
6. Slack 알림에 피드백 작성자 멘션 추가
```

### 명시적 지정

피드백 이슈를 명시적으로 지정할 수도 있습니다:

```yaml
feedback_issues:
  - repo: "semo-po"
    number: 123
```

> 상세 워크플로우는 [Workflow - Phase 10](references/workflow.md#phase-10-피드백-이슈-완료-처리-조건부) 참조

## 🔴 필수: Slack 릴리스 알림

> **버저닝은 Slack 알림까지 완료해야 완료로 간주됩니다.**

커밋 & 푸시 완료 후 **반드시** `notify-slack` Skill 호출:

```markdown
[SEMO] Skill: notify-slack 호출 - 릴리스 알림
```

### 알림 내용

| 항목 | 값 |
|------|-----|
| **채널** | #_협업 |
| **타입** | release |
| **패키지** | sax-{package} |
| **버전** | v{new_version} |
| **변경 내역** | CHANGELOG 요약 |

### 완료 확인

```markdown
[SEMO] Versioning: Slack 알림 전송 완료 (#_협업)
```

> **⚠️ 이 단계를 누락하면 버저닝 미완료 상태입니다.**

## 🔴 필수: semo-meta 로컬 동기화

> **semo-meta 버저닝 시, 현재 환경의 `.claude/semo-meta/`도 동기화해야 합니다.**

semo-meta를 수정하는 환경 = semo-meta가 설치된 환경이므로,
원본 push 후 로컬 서브모듈도 반드시 동기화:

```bash
cd .claude/semo-meta && git pull origin main
```

### 동기화 완료 확인

```markdown
[SEMO] Versioning: 로컬 동기화 완료 (.claude/semo-meta/)
```

> **⚠️ semo-meta 버저닝 시 이 단계를 누락하면 버저닝 미완료 상태입니다.**

## SEMO Message

```markdown
[SEMO] Skill: version-manager 사용

[SEMO] Versioning: {old_version} → {new_version} ({version_type})

[SEMO] Versioning: 커밋 완료 → 푸시 진행

[SEMO] Versioning: 완료 (푸시 성공)

[SEMO] Skill: notify-slack 호출 - 릴리스 알림

[SEMO] Versioning: Slack 알림 전송 완료 (#_협업)

[SEMO] Versioning: 로컬 동기화 완료 (.claude/semo-meta/)  # semo-meta 버저닝 시만
```

## Related

- [semo-architect Agent](../../agents/semo-architect/semo-architect.md)
- [package-validator Skill](../package-validator/SKILL.md)
- [SEMO Core - Principles](https://github.com/semicolon-devteam/semo-core/blob/main/PRINCIPLES.md)

## References

For detailed documentation, see:

- [Semantic Versioning Rules](references/semantic-versioning.md) - MAJOR/MINOR/PATCH 상세 규칙
- [Workflow](references/workflow.md) - 10단계 버저닝 프로세스 (커밋 & 푸시 & Slack 알림 & 피드백 이슈 처리)
- [Changelog Format](references/changelog-format.md) - Keep a Changelog 템플릿
- [Output Format](references/output-format.md) - 성공/실패 출력, Edge Cases
