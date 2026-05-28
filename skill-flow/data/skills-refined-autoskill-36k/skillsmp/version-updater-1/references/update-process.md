# SEMO Update Process

> SEMO 패키지 업데이트 상세 절차

## 1. 버전 체크 절차

### 1.1 로컬 버전 확인

```bash
# 각 패키지의 VERSION 파일 읽기
cat .claude/semo-core/VERSION
cat .claude/semo-meta/VERSION
cat .claude/semo-{package}/VERSION
```

### 1.2 원격 버전 확인

```bash
# GitHub API로 최신 버전 조회
gh api repos/semicolon-devteam/semo-core/contents/VERSION --jq '.content' | base64 -d
gh api repos/semicolon-devteam/semo-meta/contents/VERSION --jq '.content' | base64 -d
gh api repos/semicolon-devteam/semo-{package}/contents/VERSION --jq '.content' | base64 -d
```

### 1.3 버전 비교

```bash
# 버전 비교 로직
compare_versions() {
  local LOCAL=$1
  local REMOTE=$2

  if [ "$LOCAL" = "$REMOTE" ]; then
    echo "LATEST"
  elif [ "$(printf '%s\n' "$LOCAL" "$REMOTE" | sort -V | head -n1)" = "$LOCAL" ]; then
    echo "UPDATE_AVAILABLE"
  else
    echo "LOCAL_AHEAD"  # 로컬이 더 최신 (개발 중)
  fi
}
```

## 2. 업데이트 절차

### 2.1 서브모듈 업데이트

```bash
# 1. 변경사항 확인
cd .claude/semo-{package}
git status

# 2. 로컬 변경사항이 있으면 stash
git stash

# 3. 최신 버전 가져오기
git fetch origin main
git reset --hard origin/main

# 4. stash 복원 (필요 시)
git stash pop

cd -
```

### 2.2 claude-health 호출 (심링크 자동 수정)

업데이트 완료 후 `claude-health` 스킬이 자동으로 호출됩니다:

```markdown
[SEMO] version-updater: 업데이트 완료 → claude-health 호출
```

**claude-health 동작**:

1. 패키지 감지 (po, next, qa, meta, pm, backend, infra)
2. `.claude` 구조 검증 (CLAUDE.md, agents/, skills/, commands/SEMO/)
3. 문제 발견 시 자동 수정 (install-sax.sh와 동일 로직)
4. 결과 보고

이로써 `install-sax.sh --update`를 별도로 실행할 필요 없이 심링크가 자동으로 관리됩니다.

### 2.3 전체 업데이트 스크립트

```bash
#!/bin/bash
# update-sax.sh

# 모든 SEMO 서브모듈 업데이트
git submodule update --remote --merge

# 심링크 재구성
for pkg in .claude/semo-*/; do
  if [ -d "$pkg" ]; then
    name=$(basename "$pkg" | sed 's/semo-//')
    ./install-sax.sh "$name" --refresh-links 2>/dev/null || true
  fi
done

echo "SEMO 업데이트 완료"
```

## 3. 업데이트 시 주의사항

### 3.1 Breaking Change 확인

MAJOR 버전 변경 시:
1. CHANGELOG 확인
2. Breaking Change 목록 검토
3. 필요한 마이그레이션 수행

### 3.2 로컬 수정사항 보존

- 업데이트 전 `git stash`로 로컬 변경 보존
- 업데이트 후 `git stash pop`으로 복원
- 충돌 발생 시 수동 해결

### 3.3 심링크 무결성

- 심링크가 깨지지 않았는지 확인
- `ls -la .claude/` 로 심링크 상태 확인
- 문제 시 `--refresh-links` 옵션으로 재구성

## 4. 롤백 절차

문제 발생 시 이전 버전으로 롤백:

```bash
# 1. 이전 커밋 해시 확인
cd .claude/semo-{package}
git log --oneline -5

# 2. 특정 버전으로 롤백
git checkout {commit_hash}

# 3. 또는 특정 태그로 롤백
git checkout v{version}

cd -
```

## 5. 자동 업데이트 비활성화

자동 버전 체크를 비활성화하려면:

```markdown
<!-- .claude/CLAUDE.md 에 추가 -->
## SEMO Settings

- **auto_version_check**: false
```
