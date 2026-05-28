# Sync Workflow

> package-sync Skill의 상세 워크플로우

## Phase 1: 사전 검증

### 1.1 패키지 존재 확인

```bash
# 소스 패키지 확인
ls -la sax/packages/{package}/

# 필수 파일 확인
test -f sax/packages/{package}/CLAUDE.md && echo "✅ CLAUDE.md exists"
test -d sax/packages/{package}/agents && echo "✅ agents/ exists"
```

### 1.2 대상 디렉토리 확인

```bash
# .claude 디렉토리 존재 확인
test -d .claude || mkdir -p .claude

# 기존 패키지 버전 확인 (있는 경우)
if [ -f .claude/{package}/CLAUDE.md ]; then
  echo "기존 설치 발견"
fi
```

## Phase 2: 동기화 실행

### 2.1 rsync 명령

```bash
rsync -av --delete --exclude='.git' --exclude='.DS_Store' \
  sax/packages/{package}/ \
  .claude/{package}/
```

**옵션 설명**:

| 옵션 | 설명 |
|------|------|
| `-a` | Archive 모드 (권한, 시간 유지) |
| `-v` | Verbose 출력 |
| `--delete` | 소스에 없는 파일 삭제 |
| `--exclude` | 제외 패턴 |

### 2.2 동기화 대상

```
sax/packages/{package}/
├── CLAUDE.md         → .claude/{package}/CLAUDE.md
├── agents/           → .claude/{package}/agents/
├── skills/           → .claude/{package}/skills/
├── commands/         → .claude/{package}/commands/
└── templates/        → .claude/{package}/templates/
```

## Phase 3: 검증

### 3.1 파일 카운트 비교

```bash
# 소스 파일 수
find sax/packages/{package} -type f | wc -l

# 대상 파일 수
find .claude/{package} -type f | wc -l
```

### 3.2 주요 파일 확인

```bash
# CLAUDE.md 동기화 확인
diff sax/packages/{package}/CLAUDE.md .claude/{package}/CLAUDE.md

# Agents 동기화 확인
ls .claude/{package}/agents/
```

## Phase 4: 완료 보고

```markdown
[SEMO] Skill: package-sync 완료

## ✅ 동기화 결과

**패키지**: {package}
**소스**: `sax/packages/{package}/`
**대상**: `.claude/{package}/`

### 동기화된 파일

| 유형 | 파일 수 |
|------|--------|
| CLAUDE.md | 1 |
| Agents | {agent_count} |
| Skills | {skill_count} |
| Commands | {command_count} |
| **합계** | **{total_count}** |

### 다음 단계

1. ✅ 동기화 완료
2. ⏳ 변경사항 테스트
3. ⏳ Git 커밋
```

## 자동화 트리거

### 동기화가 필요한 상황

1. **Agent/Skill/Command 변경 후**
2. **버저닝 완료 후** (version-manager 실행 후)
3. **CLAUDE.md 업데이트 후**
4. **커밋 직전**

### 권장 워크플로우

```
변경 작업
    ↓
package-validator (검증)
    ↓
version-manager (버저닝)
    ↓
package-sync (동기화)  ← 현재 Skill
    ↓
git commit
```
