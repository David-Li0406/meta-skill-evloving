# 패키지 정보 조회

> semo-help 스킬에서 설치된 SEMO 패키지 정보를 조회하는 방법

## 설치된 패키지 확인

### 기본 조회

```bash
# 패키지 목록
ls -d .claude/semo-* 2>/dev/null | xargs -I {} basename {}

# 버전 포함
for dir in .claude/semo-*/; do
  name=$(basename "$dir")
  version=$(cat "$dir/VERSION" 2>/dev/null || echo "unknown")
  echo "| $name | $version |"
done
```

### 상세 정보 조회

```bash
# CLAUDE.md에서 패키지 설명 추출
for dir in .claude/semo-*/; do
  name=$(basename "$dir")
  desc=$(head -5 "$dir/CLAUDE.md" 2>/dev/null | grep -E "^>" | head -1)
  echo "$name: $desc"
done
```

## 패키지별 구성 요소

### Agent 목록

```bash
# 패키지별 Agent 조회
ls .claude/semo-*/agents/*/
```

### Skill 목록

```bash
# 패키지별 Skill 조회
ls .claude/semo-*/skills/*/
```

### Command 목록

```bash
# 패키지별 Command 조회
ls .claude/semo-*/commands/*/
```

## 응답 템플릿

### 패키지 목록 응답

```markdown
[SEMO] Skill: semo-help 응답

## 설치된 SEMO 패키지

| 패키지 | 버전 | 설명 |
|--------|------|------|
| semo-core | 0.10.0 | 공통 컴포넌트 |
| semo-meta | 0.35.0 | SEMO 패키지 관리 |
| ... | ... | ... |

### 총 구성 요소
- Agents: {n}개
- Skills: {m}개
- Commands: {k}개
```

### 특정 패키지 응답

```markdown
[SEMO] Skill: semo-help 응답

## {package_name} 패키지

**버전**: {version}
**설명**: {description}

### Agents
| Agent | 역할 |
|-------|------|
| ... | ... |

### Skills
| Skill | 역할 |
|-------|------|
| ... | ... |

---
📚 상세 정보: .claude/{package_name}/CLAUDE.md
```

## 패키지 정보 캐시

- 세션 시작 시 패키지 정보 한 번 조회
- 이후 질문에서는 캐시된 정보 사용
- `/SEMO:update` 후 캐시 갱신
