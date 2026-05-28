# Agent 검토 체크리스트

## Frontmatter 검증

### 필수 필드

| 필드 | 필수 | 검증 규칙 |
|------|------|----------|
| `name` | Yes | 소문자, 하이픈만 사용 (예: `code-reviewer`) |
| `description` | Yes | 목적 + 사용 시점 명시 |
| `tools` | No | 쉼표 구분, 유효한 도구명 |
| `model` | No | `sonnet`, `opus`, `haiku`, `inherit` 중 하나 |
| `skills` | No | 관련 스킬명 |
| `permissionMode` | No | `default`, `acceptEdits`, `bypassPermissions`, `plan` 중 하나 |

### name 검증
```
- [ ] 소문자만 사용
- [ ] 단어 구분은 하이픈(-)
- [ ] 언더스코어(_) 미사용
- [ ] 공백 미사용
```

### description 검증
```
- [ ] "Use PROACTIVELY" 또는 "MUST BE USED" 포함
- [ ] 구체적인 트리거 상황 명시
- [ ] 자동 호출 조건 나열 (1)(2)(3)...
```

**좋은 예:**
```yaml
description: |
  코드 리뷰 전문가.
  Use PROACTIVELY after writing or modifying code.
  자동 호출 조건: (1) 코드 작성 완료 후 (2) PR 생성 전 (3) 리뷰 요청 시
```

**나쁜 예:**
```yaml
description: 코드를 리뷰합니다
```

### tools 검증

유효한 도구 목록:
- `Read`, `Write`, `Edit`
- `Grep`, `Glob`
- `Bash`
- `Task`
- `AskUser`, `TodoWrite`
- `WebFetch`, `WebSearch`

**일반적인 조합:**
- 읽기 전용: `Read, Grep, Glob, Bash`
- 수정 포함: `Read, Write, Edit, Grep, Glob, Bash`

### model 검증

| 값 | 용도 |
|----|------|
| `haiku` | 빠른 작업, 간단한 분석 |
| `sonnet` | 균형잡힌 성능 (기본값) |
| `opus` | 복잡한 추론 필요 시 |
| `inherit` | 메인 대화 모델 사용 |

### skills 검증

```
- [ ] 참조된 스킬이 실제 존재하는지 확인
  - `.claude/skills/{skill-name}/SKILL.md` 존재 여부
- [ ] 삭제/이름변경된 스킬 참조 없음
- [ ] 스킬명 오타 없음 (code-review vs code-reviewer 등)
```

---

## 본문 검증

### 필수 구조

```markdown
You are a [specific role].

When invoked:
1. [First action]
2. [Second action]
3. [Third action]

Guidelines:
- [Guideline 1]
- [Guideline 2]
```

### 체크리스트

```
- [ ] "You are a..." 역할 정의로 시작
- [ ] "When invoked:" 섹션 존재
- [ ] 구체적인 첫 번째 액션 명시
- [ ] "Guidelines:" 또는 유사 섹션 존재
- [ ] 30줄 이하 (간결성)
```

### 권장 섹션

| 섹션 | 필수 | 설명 |
|------|------|------|
| 역할 정의 | Yes | "You are a..." |
| When invoked | Yes | 호출 시 워크플로우 |
| Guidelines | Yes | 가이드라인/제약사항 |
| Focus Areas | No | 집중 영역 |
| Output | No | 출력 형식 |

---

## 베스트 프랙티스 검증

```
- [ ] 30줄 이하로 간결한가?
- [ ] skills 필드로 관련 스킬 연동했는가?
- [ ] 언어/프레임워크를 하드코딩하지 않았는가? (범용성)
- [ ] .claude/rules/ 참조가 있는가? (선택)
- [ ] 스킬과 내용 중복이 없는가?
```

---

## 일반적인 문제

| 문제 | 원인 | 해결 |
|------|------|------|
| 에이전트가 자동 호출 안됨 | description에 트리거 불명확 | "Use PROACTIVELY" + 구체적 조건 추가 |
| 스킬 내용 사용 안함 | skills 필드 누락 | `skills: skill-name` 추가 |
| 너무 장황함 | 상세 내용이 에이전트에 포함 | 스킬로 분리, 에이전트는 참조만 |
| skills 참조 오류 | 스킬 삭제/이름변경 후 미수정 | 에이전트의 skills 필드 업데이트 |
