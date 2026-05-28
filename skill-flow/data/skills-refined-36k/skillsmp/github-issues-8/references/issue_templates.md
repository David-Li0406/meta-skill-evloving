# GitHub 이슈 템플릿

## 1. 플랫폼별 이슈 템플릿

### iOS 화면 이슈

```markdown
## 📋 화면 정보
- **화면 ID**: H001
- **화면명**: 메인(홈)
- **경로**: HomeViewController

## ✅ 구현 요구사항
### UI 컴포넌트
- [ ] UICollectionView로 Live Now/Upcoming 섹션 구성
- [ ] 최신 뉴스 섹션 구성 (요약 카드)
- [ ] 라이브 카드 (썸네일, 제목, 아티스트, 상태)
- [ ] 뉴스 카드 (썸네일, 제목, 요약)
- [ ] Pull-to-refresh

### API 연동
- [ ] `GET /live?status=LIVE&limit=5` - Live Now
- [ ] `GET /live?status=SCHEDULED&limit=5` - Upcoming
- [ ] `GET /news?limit=10` - 최신 뉴스
- [ ] 로딩 상태 처리
- [ ] 에러 상태 처리
- [ ] 빈 상태 처리

### 네비게이션
- [ ] 라이브 카드 탭 → LiveDetailViewController
- [ ] 뉴스 카드 탭 → NewsDetailViewController

## 📚 참고 문서
- `doc/mvp/mvp_화면_정의서.md` - Section 3.5
- `doc/mvp/mvp_API_명세서.md` - Section 3, 4

## 🔗 관련 이슈
- 기존 이슈 #42 대체
```

### Android 화면 이슈

```markdown
## 📋 화면 정보
- **화면 ID**: H001
- **화면명**: 메인(홈)
- **경로**: HomeFragment/HomeActivity

## ✅ 구현 요구사항
### UI 컴포넌트
- [ ] RecyclerView로 Live Now/Upcoming 섹션 구성
- [ ] 최신 뉴스 섹션 구성 (요약 카드)
- [ ] 라이브 카드 (썸네일, 제목, 아티스트, 상태)
- [ ] 뉴스 카드 (썸네일, 제목, 요약)
- [ ] SwipeRefreshLayout

### API 연동
- [ ] `GET /live?status=LIVE&limit=5` - Live Now
- [ ] `GET /live?status=SCHEDULED&limit=5` - Upcoming
- [ ] `GET /news?limit=10` - 최신 뉴스
- [ ] ViewModel로 데이터 바인딩
- [ ] 로딩 상태 처리
- [ ] 에러 상태 처리
- [ ] 빈 상태 처리

### 네비게이션
- [ ] 라이브 카드 클릭 → LiveDetailFragment
- [ ] 뉴스 카드 클릭 → NewsDetailFragment

## 📚 참고 문서
- `doc/mvp/mvp_화면_정의서.md` - Section 3.5
- `doc/mvp/mvp_API_명세서.md` - Section 3, 4

## 🔗 관련 이슈
- 기존 이슈 #32 대체
```

### Web 화면 이슈

```markdown
## 📋 화면 정보
- **화면 ID**: H001
- **화면명**: 메인(홈)
- **경로**: `/`

## ✅ 구현 요구사항
### UI 컴포넌트
- [ ] Live Now/Upcoming 섹션 (요약 카드)
- [ ] 최신 뉴스 섹션 (요약 카드)
- [ ] 라이브 카드 (썸네일, 제목, 아티스트, 상태)
- [ ] 뉴스 카드 (썸네일, 제목, 요약)
- [ ] Pull-to-refresh

### API 연동
- [ ] `GET /live?status=LIVE&limit=5` - Live Now
- [ ] `GET /live?status=SCHEDULED&limit=5` - Upcoming
- [ ] `GET /news?limit=10` - 최신 뉴스
- [ ] 로딩 상태 처리
- [ ] 에러 상태 처리
- [ ] 빈 상태 처리

### 네비게이션
- [ ] 라이브 카드 클릭 → `/live/:id`
- [ ] 뉴스 카드 클릭 → `/news/:id`

## 📚 참고 문서
- `doc/mvp/mvp_화면_정의서.md` - Section 3.5
- `doc/mvp/mvp_API_명세서.md` - Section 3, 4
```

### Backend API 이슈

```markdown
## 📋 작업 내용
라이브 스트리밍 목록 및 상세 정보를 제공하는 API를 구현합니다.

## ✅ 구현 요구사항
### API 엔드포인트
- [ ] `GET /live` - 라이브 목록 조회 (페이지네이션)
- [ ] `GET /live/:id` - 라이브 상세 조회

### 데이터베이스
- [ ] `streaming_events` 테이블 마이그레이션
- [ ] `artists` 테이블 마이그레이션
- [ ] 외래키 관계 설정

### 기능
- [ ] Cursor 기반 페이지네이션
- [ ] 상태별 필터링 (LIVE/SCHEDULED/ENDED)
- [ ] YouTube 임베드 URL 반환

## 📚 참고 문서
- `doc/mvp/mvp_API_명세서.md` - Section 3 (Live Context)
- `doc/mvp/mvp_데이터베이스_정의서.md` - Section 2.4, 2.5
```

### DevOps 이슈

```markdown
## 📋 작업 내용
Web 앱의 Preview 및 Production 배포 환경을 구성합니다.

## ✅ 구현 요구사항
### Preview 배포
- [ ] Vercel/Netlify 설정
- [ ] PR별 자동 배포
- [ ] 환경 변수 설정

### Production 배포
- [ ] 도메인 연결
- [ ] HTTPS 설정
- [ ] 환경 변수 설정

### CI/CD
- [ ] GitHub Actions 워크플로우
- [ ] 빌드 및 테스트 자동화
- [ ] 배포 자동화

## 📚 참고 문서
- `doc/mvp/mvp_백로그.md` - Sprint 4
```

### Crawling 이슈

```markdown
## 📋 작업 내용
Google News RSS를 파싱하여 K-POP 관련 뉴스를 자동으로 수집하고 DB에 적재합니다.

## ✅ 구현 요구사항
### RSS 파싱
- [ ] Google News RSS URL 구성 (K-POP 키워드 기반)
- [ ] RSS XML 파싱 (feedparser 등 라이브러리 사용)
- [ ] 뉴스 항목 추출: 제목, 요약, URL, 출처, 게시일

### DB 적재
- [ ] `crawled_news` 테이블 upsert
- [ ] 중복 방지 (URL 기반)
- [ ] 최신 N개만 유지 (오래된 뉴스 삭제)

### 스케줄링
- [ ] 일 1회 자동 실행 (cron job 또는 scheduled task)
- [ ] 실행 로그 기록
- [ ] 에러 알림 (선택)

## 📚 참고 문서
- `doc/mvp/mvp_크롤링.md`
- `doc/mvp/mvp_데이터베이스_정의서.md` - Section 2.6 (crawled_news)

## ⚠️ 참고사항
- MVP Week 4 Stretch 목표
- 수동 Seed 적재가 우선, RSS는 운영 부담 완화용
```

### QA 이슈

```markdown
## 📋 작업 내용
MVP 전체 기능에 대한 회귀 테스트를 수행하고 발견된 버그를 수정합니다.

## ✅ 테스트 체크리스트
### 인증 플로우
- [ ] 이메일 회원가입
- [ ] 이메일 로그인
- [ ] Google 로그인
- [ ] 로그아웃
- [ ] 토큰 만료 처리

### 메인 기능
- [ ] 홈 화면 라이브/뉴스 표시
- [ ] 라이브 목록 조회
- [ ] 라이브 상세 및 YouTube 재생
- [ ] 뉴스 상세 조회
- [ ] 검색 기능

### 에러 처리
- [ ] 네트워크 오류 처리
- [ ] 404 에러 처리
- [ ] 인증 실패 처리
- [ ] 빈 결과 상태 표시

### 성능
- [ ] 페이지 로딩 속도
- [ ] 이미지 로딩 최적화
- [ ] 무한 스크롤 성능

## 📝 버그 리포팅
발견된 버그는 별도 이슈로 생성하여 이 이슈에 링크합니다.
```

## 2. 라벨 정의

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

## 3. 마일스톤별 화면 매핑 (Sprint 기반)

### Sprint 1: Skeleton + Contract

| 화면 ID | 화면명 | 플랫폼 | 이슈 |
|---------|--------|--------|------|
| - | 라우팅/기본 구성 | Backend | #124 |
| - | 라우팅/기본 레이아웃 | Web | #125 |
| - | 라우팅/기본 화면 | iOS | #126 |
| - | 라우팅/기본 화면 | Android | #127 |
| H024 | 에러 페이지 | iOS | #156 |
| H024 | 에러 페이지 | Android | #157 |

### Sprint 2: Auth E2E

| 화면 ID | 화면명 | 플랫폼 | 이슈 |
|---------|--------|--------|------|
| - | 회원가입/로그인 API | Backend | #128 |
| - | Google 로그인 API | Backend | #129 |
| H002, H002-1 | 로그인/회원가입 | Web | #130 |
| H002, H002-1 | 로그인/회원가입 | iOS | #131 |
| H002, H002-1 | 로그인/회원가입 | Android | #132 |

### Sprint 3: Live/News E2E

| 화면 ID | 화면명 | 플랫폼 | 이슈 |
|---------|--------|--------|------|
| - | 라이브 API | Backend | #133 |
| - | 뉴스 API | Backend | #134 |
| - | 검색 API | Backend | #135 |
| - | Seed 적재 | Backend | #136 |
| H001 | 홈 화면 | Web | #137 |
| H006, H019 | 라이브 목록/상세 | Web | #138 |
| H011 | 뉴스 상세 | Web | #139 |
| H018 | 검색 | Web | #140 |
| H001 | 홈 화면 | iOS | #148 |
| H006, H019 | 라이브 목록/상세 | iOS | #149 |
| H011 | 뉴스 상세 | iOS | #150 |
| H018 | 검색 | iOS | #151 |
| H001 | 홈 화면 | Android | #152 |
| H006, H019 | 라이브 목록/상세 | Android | #153 |
| H011 | 뉴스 상세 | Android | #154 |
| H018 | 검색 | Android | #155 |

### Sprint 4: QA + Release

| 화면 ID | 화면명 | 플랫폼 | 이슈 |
|---------|--------|--------|------|
| H016, H010 | 마이/설정 | Web | #141 |
| H016, H010 | 마이/설정 | iOS | #142 |
| H016, H010 | 마이/설정 | Android | #143 |
| - | Web 배포 | DevOps | #144 |
| - | iOS TestFlight | DevOps | #145 |
| - | Android 내부 테스트 | DevOps | #146 |
| - | QA | 전체 | #147 |
| - | Google News RSS | Crawling | #158 |
| - | YouTube 메타 갱신 | Crawling | #159 |

## 4. gh CLI 예시

### 라벨 일괄 생성

```bash
# 플랫폼 라벨
gh label create "platform:web" --color "0366d6" --description "웹 프론트엔드" --force
gh label create "platform:android" --color "3DDC84" --description "Android 앱" --force
gh label create "platform:ios" --color "000000" --description "iOS 앱" --force
gh label create "platform:backend" --color "d73a4a" --description "백엔드 API" --force
gh label create "platform:devops" --color "fbca04" --description "인프라/배포" --force

# 타입 라벨
gh label create "type:feature" --color "a2eeef" --description "새로운 기능" --force
gh label create "type:bug" --color "d73a4a" --description "버그 수정" --force
gh label create "type:enhancement" --color "84b6eb" --description "기능 개선" --force
gh label create "type:docs" --color "0075ca" --description "문서 작업" --force
gh label create "type:infrastructure" --color "fbca04" --description "인프라 작업" --force

# 우선순위 라벨
gh label create "priority:high" --color "d93f0b" --description "높은 우선순위" --force
gh label create "priority:medium" --color "fbca04" --description "중간 우선순위" --force
gh label create "priority:low" --color "0e8a16" --description "낮은 우선순위" --force

# 카테고리 라벨
gh label create "category:auth" --color "c5def5" --description "인증/회원가입" --force
gh label create "category:live" --color "f9d0c4" --description "라이브 스트리밍" --force
gh label create "category:news" --color "fef2c0" --description "뉴스" --force
gh label create "category:search" --color "bfdadc" --description "검색" --force
gh label create "category:ui" --color "d4c5f9" --description "UI/UX" --force
```

### 마일스톤 생성

```bash
gh api repos/{owner}/{repo}/milestones --method POST \
  -f title="Sprint 1: Skeleton + Contract" \
  -f description="Week 1 - 프로젝트 기본 구조 및 API 계약 정의" \
  -f due_on="2026-01-10T23:59:59Z"

gh api repos/{owner}/{repo}/milestones --method POST \
  -f title="Sprint 2: Auth E2E" \
  -f description="Week 2 - 인증 기능 완성 (이메일 + Google 로그인)" \
  -f due_on="2026-01-17T23:59:59Z"

gh api repos/{owner}/{repo}/milestones --method POST \
  -f title="Sprint 3: Live/News E2E" \
  -f description="Week 3 - 라이브/뉴스 기능 완성 + Seed 데이터 적재" \
  -f due_on="2026-01-24T23:59:59Z"

gh api repos/{owner}/{repo}/milestones --method POST \
  -f title="Sprint 4: QA + Release" \
  -f description="Week 4 - 로컬 저장 기능 + QA + 배포" \
  -f due_on="2026-01-31T23:59:59Z"
```

### 이슈 생성 예시

```bash
gh issue create \
  --title "[iOS] 홈 화면 구현 (H001)" \
  --label "platform:ios,type:feature,priority:high,category:ui" \
  --milestone "Sprint 3: Live/News E2E" \
  --body "$(cat <<'EOF'
## 📋 화면 정보
- **화면 ID**: H001
- **화면명**: 메인(홈)
- **경로**: HomeViewController

## ✅ 구현 요구사항
### UI 컴포넌트
- [ ] UICollectionView로 Live Now/Upcoming 섹션 구성
- [ ] 최신 뉴스 섹션 구성 (요약 카드)
- [ ] Pull-to-refresh

### API 연동
- [ ] `GET /live` API 연동
- [ ] `GET /news` API 연동
- [ ] 로딩/에러/빈 상태 처리

## 📚 참고 문서
- `doc/mvp/mvp_화면_정의서.md`
- `doc/mvp/mvp_API_명세서.md`

## 🔗 관련 이슈
- 기존 이슈 #42 대체
EOF
)"
```

### 중복 이슈 닫기

```bash
gh issue close 42 --comment "신규 이슈 #148로 대체됨" --reason "not planned"
```

## 5. GitHub Projects 연동

### 프로젝트에 이슈 일괄 추가 (웹 UI)

1. 프로젝트 열기: https://github.com/{owner}/{repo}/projects
2. "+ Add item" 클릭
3. 검색창에 마일스톤 쿼리 입력:

```
repo:{owner}/{repo} milestone:"Sprint 1: Skeleton + Contract"
repo:{owner}/{repo} milestone:"Sprint 2: Auth E2E"
repo:{owner}/{repo} milestone:"Sprint 3: Live/News E2E"
repo:{owner}/{repo} milestone:"Sprint 4: QA + Release"
```

4. 나타나는 이슈 모두 선택 후 추가
