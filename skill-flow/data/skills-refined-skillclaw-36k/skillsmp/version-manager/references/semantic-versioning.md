# Semantic Versioning Rules

> version-manager의 시맨틱 버저닝 상세 규칙

## MAJOR (x.0.0)

### 트리거

- 호환성 깨지는 변경
- 워크플로우 근본 변경
- Orchestrator 라우팅 규칙 대폭 변경
- 패키지 구조 근본 변경

### 예시

- sync-tasks Skill 제거, draft-task-creator로 대체
- Agent 실행 방식 변경 (Orchestrator-First Policy 도입)

## MINOR (0.x.0)

### 트리거

- 기능 추가 (하위 호환)
- Agent 추가/삭제
- Skill 추가/삭제
- Command 추가/삭제
- CLAUDE.md 섹션 추가/변경
- 워크플로우 개선

### 예시

- draft-task-creator Agent 추가
- command-creator Agent 추가
- CHANGELOG 구조 개선

## PATCH (0.0.x)

### 트리거

- 버그 수정
- 오타 수정
- 문서 보완
- 성능 개선 (API 변경 없음)

### 예시

- Agent 파일 오타 수정
- CLAUDE.md 설명 보완
- 코드 주석 개선

## Version Inference Algorithm

```python
def infer_version_type(changes):
    # MAJOR 조건
    if any(c['type'] == 'removed' and c['breaking'] for c in changes):
        return 'major'
    if any('호환성' in c['description'] for c in changes):
        return 'major'
    if any('근본' in c['description'] for c in changes):
        return 'major'

    # MINOR 조건
    if any(c['type'] == 'added' for c in changes):
        return 'minor'
    if any(c['type'] == 'removed' for c in changes):
        return 'minor'
    if any(c['component'] in ['Agent', 'Skill', 'Command'] for c in changes):
        return 'minor'

    # PATCH (기본값)
    return 'patch'
```

## New Version Calculation

```python
def calculate_new_version(current, version_type):
    major, minor, patch = map(int, current.split('.'))

    if version_type == 'major':
        return f"{major + 1}.0.0"
    elif version_type == 'minor':
        return f"{major}.{minor + 1}.0"
    elif version_type == 'patch':
        return f"{major}.{minor}.{patch + 1}"
```

### 예시

- 3.7.0 + MINOR → 3.8.0
- 3.8.0 + PATCH → 3.8.1
- 3.8.1 + MAJOR → 4.0.0
