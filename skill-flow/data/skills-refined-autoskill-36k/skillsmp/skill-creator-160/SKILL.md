---
name: skill-creator
description: |
  SEMO Skill 생성 가이드 및 자동화. Use when:
  (1) 새 Skill 생성 요청, (2) Skill 구조 초기화, (3) Skill 검증 필요,
  (4) Skill 패키징. Anthropic Skills 표준 기반.
tools: [Read, Write, Bash]
---

> **🔔 시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: skill-creator 실행 - {작업 유형}` 시스템 메시지를 첫 줄에 출력하세요.

# Skill Creator

SEMO Skill 생성을 위한 가이드와 자동화 스크립트를 제공합니다.

## Core Principles

### Concise is Key

Claude는 이미 똑똑합니다. Claude가 모르는 정보만 추가하세요.

- **포함**: SEMO 워크플로우, 팀 컨벤션, 트리거 조건, 출력 형식
- **제외**: 일반 프로그래밍 개념, 명확한 설명, 장황한 문서

### Progressive Disclosure

3단계 로딩으로 컨텍스트 효율화:

1. **Metadata** (name + description): 항상 로드 (~100 words)
2. **SKILL.md body**: Skill 트리거 시 (<500 lines)
3. **Bundled resources**: 필요 시 로드

## Skill Structure

```text
skill-name/
├── SKILL.md (필수)
│   ├── YAML frontmatter (name, description 필수)
│   └── Markdown instructions
└── Bundled Resources (선택)
    ├── scripts/      - 실행 스크립트 (Python/Bash)
    ├── references/   - 참조 문서 (필요 시 로드)
    └── assets/       - 출력용 파일 (템플릿, 이미지)
```

### 금지 파일

다음 파일은 생성하지 마세요:

- README.md, INSTALLATION_GUIDE.md, QUICK_REFERENCE.md, CHANGELOG.md

## Creation Process

### Step 1: 요구사항 수집

```markdown
## Skill 생성 정보

### 1. What (핵심 기능)
- 무엇을 하는 Skill인가요?

### 2. When (트리거 조건)
- 어떤 상황에서 사용하나요?

### 3. Complexity (복잡도)
- Simple (<100 lines): 단일 SKILL.md
- Medium (100-200 lines): SKILL.md + 1-2 refs
- Complex (>200 lines): SKILL.md + 3+ refs
```

### Step 2: 초기화

```bash
python scripts/init_skill.py <skill-name> --path <output-directory>
```

### Step 3: SKILL.md 작성

**Frontmatter 필수 항목**:

```yaml
---
name: skill-name  # hyphen-case, 최대 64자
description: |
  역할 설명. Use when (1) 조건1, (2) 조건2, (3) 조건3.
---
```

### Step 4: 검증

```bash
python scripts/quick_validate.py <skill-directory>
```

## SEMO Message

```markdown
[SEMO] Skill: skill-creator 실행 - {init|validate}
```

## References

- [Output Patterns](references/output-patterns.md)
- [Workflows](references/workflows.md)

## Related

- [skill-manager Agent](../../agents/skill-manager/skill-manager.md)
- [SEMO Core Principles](https://github.com/semicolon-devteam/docs/blob/main/sax/core/PRINCIPLES.md)
