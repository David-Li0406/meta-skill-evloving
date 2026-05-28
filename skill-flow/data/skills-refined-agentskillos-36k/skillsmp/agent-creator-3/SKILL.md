---
name: agent-creator
description: "Claude Code 서브에이전트 파일(.md) 작성을 위한 가이드. 사용 시점: (1) 새로운 서브에이전트를 생성할 때, (2) 기존 에이전트를 수정하거나 개선할 때, (3) 에이전트의 역할 범위나 트리거 조건을 정의할 때, (4) 에이전트 설정(model, tools, permissionMode)을 구성할 때. 템플릿, 예제, 도구 레퍼런스 포함."
---

# 서브에이전트 작성 가이드

## 작성 워크플로우

1. **템플릿 복사**: [references/template.md](./references/template.md)에서 구조 복사
2. **예제 참고**: [references/example.md](./references/example.md)에서 유사 패턴 확인
3. **섹션별 작성**: 아래 가이드에 따라 내용 작성
4. **도구 선택**: [references/tools.md](./references/tools.md)에서 필요한 도구 선택
5. **체크리스트 검증**: 최종 점검

---

## 저장 위치

| 위치 | 용도 | 우선순위 |
|------|------|----------|
| `.claude/agents/` | 프로젝트 전용 | 높음 |
| `~/.claude/agents/` | 전역 공유 | 낮음 |

---

## YAML 프론트매터

### 필수 필드

| 필드 | 설명 | 예시 |
|------|------|------|
| `name` | kebab-case 이름 | `code-reviewer` |
| `description` | 트리거 조건 (번호 목록) | 아래 패턴 참조 |

### 선택 필드

| 필드 | 기본값 | 옵션 |
|------|--------|------|
| `model` | inherit | `opus`, `sonnet`, `haiku`, `inherit` |
| `tools` | 전체 상속 | [도구 레퍼런스](./references/tools.md) 참조 |
| `permissionMode` | default | `default`, `acceptEdits`, `bypassPermissions`, `plan` |
| `skills` | - | 자동 로드할 스킬 목록 |
| `color` | - | UI 색상 (`red`, `purple`, `blue`, `green` 등) |

### description 작성 패턴

```yaml
description: "use proactively, Use this agent when: 1) 조건1, 2) 조건2, 3) 조건3, 4) 조건4. 추가 설명."
```

### description 작성 지침

- **`use proactively` 필수 포함**: description 시작 부분에 포함하면 Claude가 자동으로 에이전트를 위임
- **트리거 조건 번호 목록**: `Use this agent when:` 다음에 1), 2), 3), 4) 형식으로 조건 나열
- **추가 설명**: 마지막에 에이전트의 특성이나 실행 방식 설명 추가

### model 선택 기준

| 모델 | 용도 |
|------|------|
| `inherit` | 부모 모델 상속 (권장 기본값) |
| `opus` | 복잡한 분석, 깊은 추론 |
| `sonnet` | 균형 잡힌 성능의 일반 작업 |
| `haiku` | 빠른 응답이 필요한 간단한 작업 |

---

## 본문 필수 섹션

### 1. 역할 소개

```markdown
당신은 **{전문가 칭호}**입니다. {경력/전문성}을 바탕으로 {담당 업무}를 수행합니다.
```

### 2. 핵심 역할 및 책임

에이전트의 주요 기능, 자동/수동 실행 여부, 사용하는 도구/참조 자료

### 3. 역할 범위 제한 (중요)

다른 에이전트와의 역할 중복 방지:

```markdown
### 검토하지 않는 항목
- ❌ {다른 에이전트 담당 항목}

### 검토하는 항목
- ✅ {이 에이전트 담당 항목}
```

### 4. 작업 실행 모드

- **모드 1 - 자동 실행**: 트리거 조건, 자동 수집 정보
- **모드 2 - 수동 실행**: 사용자 지정 범위

### 5. 필수 작업 절차

단계별 프로세스 (도구, 참조 리소스, 판단 기준 명시)

### 6. 출력 언어

```markdown
모든 분석 결과, 주석, 리포트는 **한국어**로 작성합니다.
```

---

## 선택 섹션

| 섹션 | 용도 |
|------|------|
| 심각도 분류 기준 | 리뷰/검증 에이전트 |
| 병렬 실행 최적화 | 백그라운드 실행 에이전트 |
| 품질 보증 | 거짓 양성 최소화, 결과물 구체성 |

---

## 체크리스트

### 필수 항목

- [ ] `name`이 kebab-case로 작성되었는가?
- [ ] `description`이 트리거 조건을 번호 목록으로 명시하는가?
- [ ] [템플릿](./references/template.md) 구조를 따르는가?
- [ ] [예제](./references/example.md) 패턴을 참고했는가?

### 선택 항목

- [ ] `model`이 적절히 선택되었는가? (`inherit` 권장)
- [ ] `tools` 제한이 필요한가? ([도구 레퍼런스](./references/tools.md))
- [ ] `permissionMode`가 필요한가?

### 품질 항목

- [ ] 역할 범위가 다른 에이전트와 중복되지 않는가?
- [ ] 필수 작업 절차가 단계별로 명확한가?
- [ ] 출력 언어가 지정되어 있는가?

---

## 레퍼런스 문서

| 문서 | 설명 |
|------|------|
| [template.md](./references/template.md) | 기본 템플릿 구조 |
| [example.md](./references/example.md) | 실제 구현 예제 |
| [tools.md](./references/tools.md) | 사용 가능한 도구 목록 |
