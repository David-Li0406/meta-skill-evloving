---
name: release-manager
description: |
  STG 배포 및 PRD 태깅 자동화. Use when (1) "stg 배포해줘",
  (2) "prd 태깅해줘", (3) "릴리스 준비해줘", (4) "마일스톤 확인해줘".
tools: [Bash, Read, Write, AskUserQuestion]
model: inherit
---

> **🔔 호출 시 메시지**: 이 Skill이 호출되면 반드시 `[SEMO] Skill: release-manager` 시스템 메시지를 첫 줄에 출력하세요.

# release-manager Skill

> STG 배포 및 프로덕션 태깅 자동화

## Workflow

### 전체 플로우

```text
1. 마일스톤 확인/생성 (release-x.x.x)
2. STG 배포 → Staging CI/CD 실행
3. PRD 태깅 → Production Tagging 실행
```

> 📖 **배포 플로우 상세**: [onpremise-supabase-deploy-flow.md](../../../eng/infra/agents/ci-architect/references/onpremise-supabase-deploy-flow.md)

---

## 🔴 Step 1: 마일스톤 확인/생성

### 마일스톤 네이밍 컨벤션

```yaml
format: release-{major}.{minor}.{patch}
examples:
  - release-1.0.4
  - release-2.1.0
  - release-1.2.3
```

### 확인 절차

```bash
# 레포지토리 마일스톤 목록 조회
gh api repos/{owner}/{repo}/milestones --jq '.[] | {title: .title, state: .state, number: .number}'
```

### 마일스톤 생성 (없을 경우)

```bash
# 마일스톤 생성
gh api repos/{owner}/{repo}/milestones \
  --method POST \
  -f title="release-{version}" \
  -f state="open" \
  -f description="Release {version}"
```

### 사용자 확인

마일스톤이 없으면 사용자에게 확인:

```markdown
📦 **마일스톤 확인**

현재 레포지토리에 `release-{version}` 마일스톤이 없습니다.

**옵션:**
1. 마일스톤 생성 (release-{suggested_version})
2. 다른 버전 지정
3. 취소
```

---

## 🔴 Step 2: STG 배포

### 사전 조건

- dev 환경 테스트 완료
- 마일스톤 생성됨 (release-x.x.x)

### 실행 절차

```bash
# 1. Staging CI/CD 워크플로우 실행
gh workflow run "Staging CI/CD" \
  --repo {owner}/{repo} \
  --ref dev
```

### 모니터링

```bash
# 2. 워크플로우 실행 상태 확인
WORKFLOW_NAME="Staging CI/CD"
RUN_ID=$(gh run list --workflow="$WORKFLOW_NAME" --repo {owner}/{repo} --limit 1 --json databaseId --jq '.[0].databaseId')

# 3. 실행 상태 폴링
gh run watch $RUN_ID --repo {owner}/{repo}
```

### 결과 확인

```bash
# 4. release 브랜치 생성 확인
git fetch origin
git branch -r | grep "release-"

# 5. stg 서버 헬스체크
curl -s https://{service}-stg.semi-colon.space/api/health
```

### 완료 메시지

```markdown
[SEMO] Skill: release-manager → STG 배포 완료

✅ 워크플로우: Staging CI/CD
📦 버전: release-{version}
🌿 브랜치: release-{version} 생성됨
🔗 STG URL: https://{service}-stg.semi-colon.space

---
다음 단계: "prd 태깅해줘" 또는 QA 진행
```

---

## 🔴 Step 3: PRD 태깅

### 사전 조건

- STG 배포 완료
- QA 테스트 완료
- 배포 승인 획득

### 사전 확인

```bash
# release 브랜치 존재 확인
git fetch origin
RELEASE_BRANCH=$(git branch -r | grep "release-" | tail -1 | tr -d ' ')

if [ -z "$RELEASE_BRANCH" ]; then
  echo "❌ release 브랜치가 없습니다. STG 배포를 먼저 진행해주세요."
  exit 1
fi
```

### 실행 절차

```bash
# 1. Production Tagging 워크플로우 실행
gh workflow run "Production Tagging" \
  --repo {owner}/{repo} \
  --ref release-{version}
```

### 모니터링

```bash
# 2. 워크플로우 실행 상태 확인
WORKFLOW_NAME="Production Tagging"
RUN_ID=$(gh run list --workflow="$WORKFLOW_NAME" --repo {owner}/{repo} --limit 1 --json databaseId --jq '.[0].databaseId')

# 3. 실행 상태 폴링
gh run watch $RUN_ID --repo {owner}/{repo}
```

### 결과 확인

```bash
# 4. Release 생성 확인
gh release list --repo {owner}/{repo} --limit 5

# 5. 태그 확인
git tag -l "v*" | tail -5

# 6. Milestone close 확인
gh api repos/{owner}/{repo}/milestones --jq '.[] | select(.state == "closed") | .title'
```

### 완료 메시지

```markdown
[SEMO] Skill: release-manager → PRD 태깅 완료

✅ 워크플로우: Production Tagging
🏷️ 태그: v{version}
📋 Release: https://github.com/{owner}/{repo}/releases/tag/v{version}
📦 Milestone: release-{version} (closed)

---
다음 단계: infra 레포에서 docker-compose.yml 버전 업데이트 후 운영 배포
```

---

## 에러 처리

### 워크플로우 실패 시

```bash
# 실패 로그 확인
gh run view $RUN_ID --repo {owner}/{repo} --log-failed

# 재실행
gh run rerun $RUN_ID --repo {owner}/{repo}
```

### 에러 메시지 포맷

```markdown
[SEMO] Skill: release-manager → ❌ 오류 발생

**워크플로우**: {workflow_name}
**상태**: failed
**Run ID**: {run_id}

**에러 로그**:
```
{error_log}
```

**조치 방법**:
1. 로그 확인: `gh run view {run_id} --log`
2. 재실행: `gh run rerun {run_id}`
3. 수동 확인 후 다시 시도
```

---

## 출력 형식

### 마일스톤 확인 결과

```markdown
[SEMO] Skill: release-manager → 마일스톤 확인

📦 레포지토리: {owner}/{repo}

**Open 마일스톤:**
| 번호 | 제목 | 상태 |
|------|------|------|
| #1 | release-1.0.4 | open |
| #2 | release-1.0.5 | open |

**최신 버전 제안**: release-{next_version}
```

### STG 배포 진행 중

```markdown
[SEMO] Skill: release-manager → STG 배포 진행 중

⏳ 워크플로우: Staging CI/CD
🔄 상태: in_progress
⏱️ 경과: {elapsed_time}

실시간 모니터링: `gh run watch {run_id}`
```

### PRD 태깅 진행 중

```markdown
[SEMO] Skill: release-manager → PRD 태깅 진행 중

⏳ 워크플로우: Production Tagging
🔄 상태: in_progress
⏱️ 경과: {elapsed_time}

실시간 모니터링: `gh run watch {run_id}`
```

---

## References

- [onpremise-supabase-deploy-flow.md](../../../eng/infra/agents/ci-architect/references/onpremise-supabase-deploy-flow.md) - 배포 플로우 상세
- [github-projects.md](../../../../semo-system/semo-core/_shared/github-projects.md) - GitHub 프로젝트 설정
