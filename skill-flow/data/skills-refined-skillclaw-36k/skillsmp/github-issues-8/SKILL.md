---
name: github-issues
description: "기획 문서 기반 GitHub 이슈/마일스톤 생성 스킬. 화면 정의서, 기획서, 백로그를 분석하여 이슈와 마일스톤을 자동 생성합니다. 사용 시기: (1) 새 프로젝트 초기 이슈 생성 (2) 새 화면/기능 추가 시 이슈 생성 (3) 마일스톤 설정 (4) 이슈 커버리지 분석 (5) /github-issues 호출 시"
---

# GitHub 이슈/마일스톤 생성

## 개요

FanPulse 기획 문서(화면 정의서, 프로젝트 기획서, 백로그)를 분석하여 GitHub 이슈와 마일스톤을 생성합니다.

## 워크플로우

```
1. 문서 분석 → 2. 기존 이슈 확인 → 3. 플랫폼/범위 확인 → 4. 마일스톤/라벨 생성 → 5. 이슈 생성 → 6. 중복 이슈 정리
```

## 생성 모드

### 1. 화면별 이슈 생성

화면 정의서의 각 화면(H001, H002 등)을 기반으로 이슈 생성

```
/github-issues --mode screen --platform web
/github-issues --mode screen --platform ios
/github-issues --mode screen --platform android
/github-issues --mode screen --platform backend
```

### 2. Sprint별 이슈 생성

백로그 기반 Sprint 단위로 이슈 생성

```
/github-issues --mode sprint --sprint 1
/github-issues --mode sprint --all
```

### 3. 전체 생성

```
/github-issues --all
```

### 4. 커버리지 분석

기존 이슈와 새 이슈 간 중복/누락 분석

```
/github-issues --analyze
```

## 라벨 체계

### 플랫폼 라벨 (platform:)

| 라벨 | 색상 | 설명 |
|------|------|------|
| `platform:web` | #0366d6 | 웹 프론트엔드 |
| `platform:android` | #3DDC84 | Android 앱 |
| `platform:ios` | #000000 | iOS 앱 |
| `platform:backend` | #d73a4a | 백엔드 API |
| `platform:devops` | #fbca04 | 인프라/배포 |

### 타입 라벨 (type:)

| 라벨 | 색상 | 설명 |
|------|------|------|
| `type:feature` | #a2eeef | 새로운 기능 |
| `type:bug` | #d73a4a | 버그 수정 |
| `type:enhancement` | #84b6eb | 기능 개선 |
| `type:docs` | #0075ca | 문서 작업 |
| `type:infrastructure` | #fbca04 | 인프라 작업 |

### 우선순위 라벨 (priority:)

| 라벨 | 색상 | 설명 |
|------|------|------|
| `priority:high` | #d93f0b | 높은 우선순위 |
| `priority:medium` | #fbca04 | 중간 우선순위 |
| `priority:low` | #0e8a16 | 낮은 우선순위 |

### 카테고리 라벨 (category:)

| 라벨 | 색상 | 설명 |
|------|------|------|
| `category:auth` | #c5def5 | 인증/회원가입 |
| `category:live` | #f9d0c4 | 라이브 스트리밍 |
| `category:news` | #fef2c0 | 뉴스 |
| `category:search` | #bfdadc | 검색 |
| `category:ui` | #d4c5f9 | UI/UX |

## 이슈 생성 규칙

### 이슈 제목 형식

```
[{플랫폼}] {화면명/기능명} ({화면ID})
```

예시:
- `[iOS] 홈 화면 구현 (H001)`
- `[Backend] 회원가입 및 로그인 API 구현`
- `[DevOps] Web 배포 환경 구성`

### 이슈 본문 템플릿

```markdown
## 📋 화면 정보
- **화면 ID**: {screen_id}
- **화면명**: {screen_name}
- **경로**: {path}

## ✅ 구현 요구사항
### UI 컴포넌트
- [ ] {component_1}
- [ ] {component_2}

### API 연동
- [ ] {api_endpoint}

### 기능
- [ ] {feature_1}
- [ ] {feature_2}

## 📚 참고 문서
- `doc/mvp/mvp_화면_정의서.md`
- `doc/mvp/mvp_API_명세서.md`

## 🔗 관련 이슈
- 기존 이슈 #{old_issue} 대체
```

## 마일스톤 구조 (Sprint 기반)

### MVP 4주 Sprint

| 마일스톤 | 설명 | 마감일 예시 |
|----------|------|-------------|
| Sprint 1: Skeleton + Contract | 프로젝트 기본 구조 및 API 계약 | Week 1 |
| Sprint 2: Auth E2E | 인증 기능 완성 | Week 2 |
| Sprint 3: Live/News E2E | 라이브/뉴스 기능 완성 | Week 3 |
| Sprint 4: QA + Release | QA 및 배포 | Week 4 |

### 마일스톤 생성 명령어

```bash
gh api repos/{owner}/{repo}/milestones --method POST \
  -f title="Sprint 1: Skeleton + Contract" \
  -f description="Week 1 - 프로젝트 기본 구조 및 API 계약 정의" \
  -f due_on="2026-01-10T23:59:59Z"
```

## gh CLI 명령어

### 라벨 일괄 생성

```bash
# 플랫폼 라벨
gh label create "platform:web" --color "0366d6" --description "웹 프론트엔드"
gh label create "platform:android" --color "3DDC84" --description "Android 앱"
gh label create "platform:ios" --color "000000" --description "iOS 앱"
gh label create "platform:backend" --color "d73a4a" --description "백엔드 API"
gh label create "platform:devops" --color "fbca04" --description "인프라/배포"

# 타입 라벨
gh label create "type:feature" --color "a2eeef" --description "새로운 기능"
gh label create "type:bug" --color "d73a4a" --description "버그 수정"

# 우선순위 라벨
gh label create "priority:high" --color "d93f0b" --description "높은 우선순위"
gh label create "priority:medium" --color "fbca04" --description "중간 우선순위"
gh label create "priority:low" --color "0e8a16" --description "낮은 우선순위"

# 카테고리 라벨
gh label create "category:auth" --color "c5def5" --description "인증/회원가입"
gh label create "category:live" --color "f9d0c4" --description "라이브 스트리밍"
gh label create "category:news" --color "fef2c0" --description "뉴스"
gh label create "category:search" --color "bfdadc" --description "검색"
gh label create "category:ui" --color "d4c5f9" --description "UI/UX"
```

### 이슈 생성

```bash
gh issue create \
  --title "[iOS] 홈 화면 구현 (H001)" \
  --label "platform:ios,type:feature,priority:high,category:ui" \
  --milestone "Sprint 3: Live/News E2E" \
  --body "$(cat <<'EOF'
## 📋 화면 정보
...
EOF
)"
```

### 중복 이슈 닫기

```bash
gh issue close {issue_number} \
  --comment "신규 이슈 #{new_issue}로 대체됨" \
  --reason "not planned"
```

### 이슈 목록 조회

```bash
# 마일스톤별 이슈 조회
gh issue list --milestone "Sprint 3: Live/News E2E" --limit 50

# 라벨별 이슈 조회
gh issue list --label "platform:ios" --limit 50

# MVP 관련 이슈 조회
gh issue list --search "label:mvp" --limit 100
```

## 이슈 커버리지 분석

### 분석 워크플로우

1. 기존 이슈 목록 조회
2. 새 이슈와 매핑 관계 분석
3. 커버리지 리포트 생성:
   - **완전 커버**: 새 이슈가 기존 이슈 대체
   - **부분 커버**: 일부만 겹침
   - **누락**: 기존에는 있지만 새 이슈에 없음
   - **신규**: 새 이슈에만 있음

### 분석 명령어

```bash
# 전체 이슈 목록 조회 (JSON)
gh issue list --limit 200 --state all --json number,title,labels,milestone
```

## GitHub Projects 연동

### 프로젝트 이슈 추가 (웹 UI)

1. 프로젝트 열기
2. "+ Add item" 클릭
3. 검색창에 마일스톤 쿼리 입력:
   ```
   repo:{owner}/{repo} milestone:"Sprint 1: Skeleton + Contract"
   ```
4. 나타나는 이슈 선택 후 추가
5. Sprint 2, 3, 4 반복

### 프로젝트 뷰 추천

- **Roadmap View**: 타임라인 기반 간트 차트
- **Board View**: 칸반 보드 (Todo/In Progress/Done)
- **Table View**: 스프레드시트 형태

## 실행 전 확인사항

1. `gh auth status`로 GitHub 인증 확인
2. 저장소 접근 권한 확인
3. 기존 이슈/마일스톤 중복 확인
4. 기존 MVP 이슈와의 커버리지 분석

## 문서 경로

| 문서 | 경로 |
|------|------|
| 화면 정의서 | `doc/화면_정의서.md` |
| 프로젝트 기획서 | `doc/프로젝트_기획서.md` |
| MVP 화면 정의서 | `doc/mvp/mvp_화면_정의서.md` |
| MVP 백로그 | `doc/mvp/mvp_백로그.md` |
| MVP API 명세서 | `doc/mvp/mvp_API_명세서.md` |
| MVP DB 정의서 | `doc/mvp/mvp_데이터베이스_정의서.md` |

## 상세 템플릿

이슈 템플릿 상세는 `references/issue_templates.md` 참조
