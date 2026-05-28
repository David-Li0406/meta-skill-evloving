# Output Format

> package-validator의 출력 형식 및 에러 핸들링

## 성공 시

```json
{
  "status": "✅ PASS",
  "package": "semo-po",
  "scope": "full",
  "summary": {
    "agents": 5,
    "skills": 8,
    "commands": 3,
    "errors": 0,
    "warnings": 0
  },
  "message": "모든 검증 통과"
}
```

## 실패 시

```json
{
  "status": "❌ FAIL",
  "package": "semo-po",
  "scope": "full",
  "summary": {
    "agents": 5,
    "skills": 8,
    "commands": 3,
    "errors": 3,
    "warnings": 1
  },
  "errors": [
    {
      "type": "frontmatter",
      "file": "agents/epic-master.md",
      "message": "description 필드 누락"
    },
    {
      "type": "naming",
      "file": "skills/createEpic/SKILL.md",
      "message": "kebab-case 위반: createEpic → create-epic"
    },
    {
      "type": "consistency",
      "file": "CLAUDE.md",
      "message": "Agents 테이블에 누락: draft-task-creator"
    }
  ],
  "warnings": [
    {
      "type": "progressive-disclosure",
      "file": "skills/sync-tasks/",
      "message": "references/ 디렉토리 없음 (선택적)"
    }
  ]
}
```

## Error Handling

### 치명적 에러 (즉시 중단)

| 에러 | 설명 |
|------|------|
| CLAUDE.md 파일 없음 | 패키지 설정 파일 필수 |
| agents/ 디렉토리 없음 | Agent 디렉토리 필수 |
| YAML 문법 오류 | Frontmatter 파싱 실패 |

### 경고 (계속 진행)

| 경고 | 설명 |
|------|------|
| references/ 누락 | Progressive Disclosure 선택적 |
| orchestrator.md 없음 | 패키지에 따라 선택적 |
| tools 필드 없음 | Skill의 경우 권장 |

## Error Types

| Type | 설명 |
|------|------|
| `frontmatter` | Frontmatter 필드 누락/형식 오류 |
| `naming` | kebab-case 위반, 이중 콜론 |
| `consistency` | CLAUDE.md와 실제 파일 불일치 |
| `routing` | orchestrator 라우팅 오류 |
| `progressive-disclosure` | SKILL.md 크기 초과, references/ 참조 오류 |
