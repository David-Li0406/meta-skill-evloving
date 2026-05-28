---
name: quality-gate
description: |
  코드 품질 검증 스킬. Use when (1) 커밋 전 검증,
  (2) 린트/빌드/테스트 실행, (3) PR 전 품질 확인.
tools: [Read, Bash, Glob]
model: inherit
---

> **시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: quality-gate 호출` 시스템 메시지를 첫 줄에 출력하세요.

# quality-gate Skill

> 코드 품질 검증 통합 스킬 (체이닝 스킬)

## Purpose

커밋 전 코드 품질을 검증합니다. 린트, 타입 체크, 빌드, 테스트를 순차적으로 실행하고 결과를 리포트합니다.

---

## 🔴 스킬 체이닝 (NON-NEGOTIABLE)

> **이 스킬은 implement(write-code) → write-test 체인에서 호출됩니다.**

```text
skill:write-code 완료
    │
    └→ "테스트 작성할까요?"
           │
           ├─ "테스트 작성해줘" → skill:write-test
           │       │
           │       └→ "품질 검증할까요?"
           │              └→ skill:quality-gate (이 스킬)
           │                      │
           │                      └→ "커밋할까요?"
           │                             └→ skill:git-workflow
           │
           └─ "검증해줘" → skill:quality-gate (테스트 건너뜀)
```

---

## 🔴 실행 순서 (NON-NEGOTIABLE)

| 단계 | 명령 | 설명 |
|------|------|------|
| 1 | `npm run lint` | ESLint 검사 |
| 2 | `npx tsc --noEmit` | TypeScript 타입 체크 |
| 3 | `npm run build` | 빌드 검증 |
| 4 | `npm test` | 테스트 실행 |

> **⚠️ 각 단계는 순차 실행되며, 실패 시 즉시 중단**

---

## Workflow

### 1. 프로젝트 설정 확인

```bash
# package.json 스크립트 확인
cat package.json | jq '.scripts'
```

### 2. 단계별 실행

```bash
# 1. Lint
npm run lint

# 2. TypeCheck
npx tsc --noEmit

# 3. Build
npm run build

# 4. Test
npm test
```

### 3. 결과 리포트

각 단계의 성공/실패 여부와 소요 시간을 리포트합니다.

---

## 출력 형식

### 성공 시

```markdown
[SEMO] Skill: quality-gate 완료

✅ **Quality Gate 통과**

| 단계 | 상태 | 소요 시간 |
|------|------|----------|
| Lint | ✅ Pass | 2.3s |
| TypeCheck | ✅ Pass | 4.1s |
| Build | ✅ Pass | 12.5s |
| Test | ✅ Pass (42/42) | 8.2s |

---

💡 **다음 단계**: 커밋할까요?
   - "커밋해줘" → skill:git-workflow 호출
   - "아니" → 대기
```

### 실패 시

```markdown
[SEMO] Skill: quality-gate 실패

❌ **Lint 실패**

에러:
src/utils/auth.ts
  42:10  error  'foo' is not defined  no-undef
  55:3   error  Unexpected any type    @typescript-eslint/no-explicit-any

💡 에러 수정을 도와드릴까요?
   - "수정해줘" → skill:write-code 호출
   - "무시하고 계속" → 다음 단계 진행 (권장하지 않음)
```

---

## 🔴 Post-Action: 커밋 프롬프트 (NON-NEGOTIABLE)

> **Quality Gate 통과 후 반드시 커밋 여부를 확인합니다.**

### 완료 시 자동 프롬프트

```markdown
💡 **다음 단계**: 커밋할까요?
   - "커밋해줘" → skill:git-workflow 호출
   - "아니" → 대기
```

### 사용자 응답별 동작

| 응답 | 동작 |
|------|------|
| "커밋해줘" | `skill:git-workflow` 호출 |
| "푸시까지 해줘" | `skill:git-workflow` 호출 (push 포함) |
| "아니", "계속" | 추가 작업 대기 |

---

## 프로젝트 유형별 설정

### Next.js 프로젝트

```bash
npm run lint        # next lint
npm run build       # next build
npm test            # jest
```

### Node.js 프로젝트

```bash
npm run lint        # eslint
npx tsc --noEmit    # typescript check
npm run build       # tsc
npm test            # jest/mocha
```

### 스크립트 없는 경우

| 스크립트 | 대체 명령 |
|----------|----------|
| `lint` 없음 | `npx eslint .` 실행 또는 건너뜀 |
| `build` 없음 | `npx tsc` 실행 또는 건너뜀 |
| `test` 없음 | 건너뜀 (테스트 없음 표시) |

---

## 옵션

### 특정 단계만 실행

```markdown
"린트만 실행해줘" → npm run lint만 실행
"빌드만 해줘" → npm run build만 실행
"테스트만 돌려줘" → npm test만 실행
```

### 실패 시 계속 진행

```markdown
"실패해도 계속해줘" → 모든 단계 실행 후 최종 리포트
```

---

## Related Skills

| Skill | 역할 | 연결 시점 |
|-------|------|----------|
| `write-code` | 코드 구현 | quality-gate 전 |
| `write-test` | 테스트 작성 | quality-gate 전 |
| `git-workflow` | 커밋/푸시 | quality-gate 후 |

---

## References

- [SEMO Quality Gate 원칙](../../semo-core/principles/QUALITY_GATE.md)
- [write-code Skill](../write-code/SKILL.md)
- [git-workflow Skill](../git-workflow/SKILL.md)
