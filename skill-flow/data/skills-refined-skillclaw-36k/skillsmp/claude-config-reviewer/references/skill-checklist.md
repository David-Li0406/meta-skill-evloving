# Skill 검토 체크리스트

## 디렉토리 구조 검증

### 필수 구조
```
skill-name/
├── SKILL.md          # 필수
└── references/       # 권장 (상세 문서)
    └── *.md
```

### 선택 구조
```
skill-name/
├── SKILL.md
├── references/       # 참조 문서
├── assets/           # 출력용 파일, 템플릿
└── scripts/          # 실행 스크립트
```

### 체크리스트
```
- [ ] SKILL.md 파일 존재
- [ ] 디렉토리명 = skill name (소문자, 하이픈)
- [ ] 불필요한 파일 없음 (README.md, CHANGELOG.md 등)
```

---

## Frontmatter 검증

### 필수 필드

| 필드 | 필수 | 검증 규칙 |
|------|------|----------|
| `name` | Yes | 소문자, 하이픈만 사용 |
| `description` | Yes | 기능 + 사용 시기 명시 |

### name 검증
```
- [ ] 소문자만 사용
- [ ] 단어 구분은 하이픈(-)
- [ ] 디렉토리명과 일치
```

### description 검증
```
- [ ] 스킬 기능 설명 포함
- [ ] "사용 시기: (1)...(2)...(3)..." 패턴
- [ ] 트리거 키워드 포함 (선택)
- [ ] "(project)" 태그 포함 (프로젝트 스킬인 경우)
```

**좋은 예:**
```yaml
description: |
  Kotlin/Spring 코드 문서화 전문 skill. KDoc 작성, 인라인 주석 추가.
  사용 시기: (1) 코드에 KDoc/주석 추가 요청 시 (2) 문서화 품질 검토 시
  (3) "문서화", "KDoc" 키워드 사용 시 (project)
```

**나쁜 예:**
```yaml
description: 문서를 작성합니다
```

---

## 본문 검증

### 권장 구조

```markdown
# Skill Name

## 개요
[간단한 설명]

## Quick Start
[기본 사용 예시]

## Workflow
1. [단계 1]
2. [단계 2]
3. [단계 3]

## 결과 출력 형식
[예시 출력]

## Resources
- references/: [설명]
- assets/: [설명]
```

### 체크리스트
```
- [ ] 제목 (# Skill Name) 존재
- [ ] 개요/설명 섹션 존재
- [ ] Workflow 또는 사용법 섹션 존재
- [ ] 500줄 이하 (초과 시 references로 분리)
- [ ] 명령형 동사 사용 ("Create", "Use", "Analyze")
```

---

## References 검증 (해당 시)

### 체크리스트
```
- [ ] 100줄 이상 파일은 목차 포함
- [ ] SKILL.md에서 링크로 참조
- [ ] 정보 중복 없음 (SKILL.md 또는 references 중 하나에만)
- [ ] 1단계 깊이만 유지 (중첩 참조 피하기)
```

### 권장 파일명 패턴
- `checklist.md` - 체크리스트
- `examples.md` - 예시 모음
- `guidelines.md` - 상세 가이드라인
- `templates.md` - 템플릿

---

## Assets/Scripts 검증 (해당 시)

### assets/ 체크리스트
```
- [ ] 출력에 사용되는 파일만 포함
- [ ] 템플릿 파일은 명확한 구조
- [ ] 불필요한 파일 없음
```

### scripts/ 체크리스트

⚠️ **스킬 내 scripts/ 폴더 발견 시 → script/로 통합 권장**

이유:
- 중앙 집중 관리 (script/ 폴더)
- 다른 에이전트/스킬에서도 재사용 가능
- npx로 생성된 scripts/는 placeholder일 가능성 높음

```
- [ ] scripts/ 폴더 존재 시 → script/로 이동 권장
- [ ] placeholder/스캐폴딩이 아닌 실제 구현 확인
  - 확인: analyze() 내부에 실제 로직 있는지
- [ ] SKILL.md에서 script/ 경로 참조로 변경
- [ ] 이동 후 scripts/ 폴더 삭제
```

---

## 베스트 프랙티스 검증

```
- [ ] SKILL.md 500줄 이하
- [ ] 상세 내용은 references/로 분리
- [ ] Claude가 이미 아는 내용 중복 없음
- [ ] 에이전트와 내용 중복 없음
- [ ] 점진적 공개 패턴 적용 (SKILL.md → references/)
```

---

## 중복 스킬 검증

```
- [ ] 유사한 이름의 스킬 존재 여부 확인
  - 예: code-review vs code-reviewer
- [ ] 중복 시 하나로 통합 권장
- [ ] 삭제된 스킬을 참조하는 에이전트 없는지 확인
```

---

## 일반적인 문제

| 문제 | 원인 | 해결 |
|------|------|------|
| 스킬이 자동 호출 안됨 | description에 트리거 불명확 | "사용 시기:" + 키워드 추가 |
| SKILL.md가 너무 김 | 모든 내용을 포함 | references/로 분리 |
| 에이전트에서 사용 안됨 | 에이전트 skills 필드 누락 | 에이전트에 `skills: skill-name` 추가 |
| 중복 스킬 존재 | npx로 여러 번 생성 | 하나로 통합 후 나머지 삭제 |
| scripts/ placeholder | npx 자동 생성 | script/로 통합 또는 실제 구현 |
