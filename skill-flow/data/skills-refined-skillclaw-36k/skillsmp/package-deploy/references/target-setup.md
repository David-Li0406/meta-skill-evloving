# Target Setup

> 배포 대상 프로젝트 설정 가이드

## 프로젝트 유형별 설정

### 1. 그린필드 (신규 프로젝트)

```bash
# 1. 프로젝트 생성
npx create-next-app@latest my-project

# 2. SEMO 배포
cd /path/to/semicolon/docs
./sax/scripts/deploy.sh semo-next /path/to/my-project

# 3. CLAUDE.md 생성
cat > /path/to/my-project/.claude/CLAUDE.md << 'EOF'
# My Project

## SEMO-Next 활성화

@semo-next/CLAUDE.md
EOF

# 4. 초기 커밋
cd /path/to/my-project
git add .claude/
git commit -m "📝 [SEMO] Initial SEMO-Next setup v3.19.0"
```

### 2. 브라운필드 (기존 프로젝트)

```bash
# 1. 기존 .claude 백업 (있는 경우)
cd /path/to/existing-project
if [ -d ".claude" ]; then
  cp -r .claude .claude.backup
fi

# 2. SEMO 배포
cd /path/to/semicolon/docs
./sax/scripts/deploy.sh semo-next /path/to/existing-project

# 3. 기존 CLAUDE.md와 병합
# 기존 내용 유지하면서 SEMO 참조 추가

# 4. 커밋
cd /path/to/existing-project
git add .claude/
git commit -m "📝 [SEMO] Integrate SEMO-Next v3.19.0"
```

### 3. SEMO 업데이트

```bash
# 1. 현재 버전 확인
cat /path/to/project/.claude/semo-next/CLAUDE.md | grep "Version"

# 2. 업데이트 실행
cd /path/to/semicolon/docs
./sax/scripts/deploy.sh semo-next /path/to/project --update

# 3. 커밋
cd /path/to/project
git add .claude/
git commit -m "📝 [SEMO] Sync to v3.19.0"
```

## 필수 설정

### 루트 CLAUDE.md

대상 프로젝트의 `.claude/CLAUDE.md`:

```markdown
# {Project Name}

## Project Context

{프로젝트 설명}

## SEMO-Next 활성화

@semo-next/CLAUDE.md

## Project-Specific Rules

{프로젝트별 추가 규칙}
```

### .gitignore

SEMO 관련 제외 항목:

```gitignore
# SEMO 제외 항목 (필요시)
.claude/*.backup
.claude/*.log
```

## 패키지별 필수 조건

### semo-next

| 조건 | 설명 |
|------|------|
| Node.js | v18+ |
| Next.js | v14+ (권장) |
| gh CLI | Supabase/API 문서 참조용 |
| Git | 버전 관리 |

### semo-core

| 조건 | 설명 |
|------|------|
| gh CLI | Core 문서 참조용 |
| Git | 버전 관리 |

## 문제 해결

### 권한 오류

```bash
# 디렉토리 권한 확인
ls -la /path/to/project/.claude/

# 권한 수정
chmod -R 755 /path/to/project/.claude/
```

### 기존 파일 충돌

```bash
# 백업 후 재배포
mv .claude .claude.old
./sax/scripts/deploy.sh semo-next .

# 필요한 커스텀 파일 복원
cp .claude.old/custom-file.md .claude/
```

### gh CLI 미설치

```bash
# macOS
brew install gh

# 인증
gh auth login
```
