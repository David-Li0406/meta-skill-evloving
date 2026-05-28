# Deploy Workflow

> package-deploy Skill의 상세 배포 프로세스

## Phase 1: 사전 준비

### 1.1 대상 프로젝트 확인

```bash
# 대상 경로 존재 확인
test -d /path/to/target-project && echo "✅ 대상 경로 존재"

# Git 레포지토리 확인 (권장)
test -d /path/to/target-project/.git && echo "✅ Git 레포"
```

### 1.2 기존 설치 확인

```bash
# 기존 SEMO 설치 확인
if [ -d "/path/to/target/.claude" ]; then
  echo "기존 .claude 디렉토리 발견"

  # 기존 버전 확인
  if [ -f "/path/to/target/.claude/semo-next/CLAUDE.md" ]; then
    grep "Version" /path/to/target/.claude/semo-next/CLAUDE.md
  fi
fi
```

### 1.3 소스 버전 확인

```bash
# 배포할 SEMO 버전
cat sax/VERSION
```

## Phase 2: 배포 실행

### 2.1 deploy.sh 사용 (권장)

```bash
# docs 레포 경로에서 실행
cd /path/to/semicolon/docs

# 신규 설치
./sax/scripts/deploy.sh semo-next /path/to/target-project

# 업데이트
./sax/scripts/deploy.sh semo-next /path/to/target-project --update
```

### 2.2 수동 배포

```bash
TARGET="/path/to/target-project"

# 디렉토리 생성
mkdir -p "$TARGET/.claude/semo-next"
mkdir -p "$TARGET/.claude/agents"
mkdir -p "$TARGET/.claude/skills"

# 패키지 설정 복사
cp sax/packages/semo-next/CLAUDE.md "$TARGET/.claude/semo-next/"

# Agents 복사
cp -r sax/packages/semo-next/agents/* "$TARGET/.claude/agents/"

# Skills 복사
cp -r sax/packages/semo-next/skills/* "$TARGET/.claude/skills/"

# Commands 복사 (있는 경우)
if [ -d "sax/packages/semo-next/commands" ]; then
  mkdir -p "$TARGET/.claude/commands"
  cp -r sax/packages/semo-next/commands/* "$TARGET/.claude/commands/"
fi
```

### 2.3 패키지별 배포 구조

**semo-next**:
```
target-project/.claude/
├── semo-next/
│   └── CLAUDE.md        # 패키지 설정
├── agents/              # Agent 파일들
│   ├── orchestrator/
│   ├── implementation-master/
│   └── ...
└── skills/              # Skill 파일들
    ├── health-check/
    ├── scaffold-domain/
    └── ...
```

**semo-core**:
```
target-project/.claude/
└── semo-core/
    ├── PRINCIPLES.md
    ├── MESSAGE_RULES.md
    ├── PACKAGING.md
    └── TEAM_RULES.md
```

## Phase 3: 배포 후 설정

### 3.1 루트 CLAUDE.md 설정

대상 프로젝트의 `.claude/CLAUDE.md` 생성/수정:

```markdown
# Project CLAUDE.md

## SEMO-Next 활성화

이 프로젝트는 SEMO-Next 패키지를 사용합니다.

@semo-next/CLAUDE.md
```

### 3.2 Health Check 실행

```
/SEMO:health-check
```

## Phase 4: 검증

### 4.1 파일 확인

```bash
# 필수 파일 확인
ls -la "$TARGET/.claude/semo-next/CLAUDE.md"
ls -la "$TARGET/.claude/agents/"
ls -la "$TARGET/.claude/skills/"
```

### 4.2 버전 확인

```bash
# 배포된 버전과 소스 버전 비교
cat sax/VERSION
grep "Version" "$TARGET/.claude/semo-next/CLAUDE.md"
```

## Phase 5: 완료 및 커밋

### 5.1 완료 보고

```markdown
[SEMO] Skill: package-deploy 완료

## ✅ 배포 결과

**패키지**: semo-next
**대상**: /path/to/target-project
**버전**: v3.19.0

### 배포된 컴포넌트

| 유형 | 파일 수 |
|------|--------|
| Agents | 12 |
| Skills | 13 |
| Commands | 4 |

### 다음 단계

1. ✅ 배포 완료
2. ⏳ `.claude/CLAUDE.md` 설정
3. ⏳ `/SEMO:health-check` 실행
4. ⏳ Git 커밋: `📝 [SEMO] Sync to v3.19.0`
```

### 5.2 커밋 (대상 프로젝트에서)

```bash
cd /path/to/target-project
git add .claude/
git commit -m "📝 [SEMO] Sync to v3.19.0"
```
