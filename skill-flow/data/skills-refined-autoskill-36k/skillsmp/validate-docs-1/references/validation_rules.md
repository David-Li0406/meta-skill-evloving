# 문서 정합성 검증 규칙

## 1. 화면-DB 매핑 규칙

### 화면별 필수 테이블

| 화면 ID | 화면명 | 필수 테이블 |
|---------|--------|-------------|
| H001 | 메인 화면 | crawled_news, crawled_charts, posts |
| H002 | 로그인 | users, auth_tokens |
| H002-1 | 회원가입 | users |
| H003 | 팬 커뮤니티 | posts(MongoDB), artists |
| H003-1 | 아티스트 필터 | artists |
| H004 | 투표 페이지 | polls, vote_options, votes, points |
| H005 | 차트 순위 | crawled_charts, crawled_charts_history, artists |
| H006 | 라이브 & 이벤트 | streaming_events |
| H007 | 콘서트 일정 | crawled_concerts |
| H008 | 광고 & 리워드 | points, point_transactions, rewards, crawled_ads |
| H009 | 팬 멤버십 | memberships, users |
| H010 | 설정 페이지 | users |
| H011 | 뉴스 상세 | crawled_news |
| H012 | 상세 게시글 | posts(MongoDB), comments(MongoDB), likes |
| H013 | 게시글 작성 | posts(MongoDB), media |
| H014 | 아티스트 상세 | artists |
| H015 | 상세 공연 정보 | crawled_concerts |
| H016 | 마이페이지 | users, points, memberships |
| H017 | 알림 목록 | notifications |
| H018 | 검색 화면 | search_history |
| H019 | 라이브 상세 | streaming_events, chat_messages, live_hearts |
| H020 | 좋아요한 아티스트 | user_favorites, artists |
| H021 | 저장한 게시물 | saved_posts, posts(MongoDB) |
| H022 | 예매 내역 | ticket_reservations, crawled_concerts |
| H022-1 | 예매 상세 | ticket_reservations |
| H023 | 고객센터 | - |
| H023-1 | FAQ | faq |
| H023-2 | 1:1 문의 | support_tickets |
| H023-3 | 문의 작성 | support_tickets |
| H023-4 | 공지사항 | notices |
| H023-5 | 공지사항 상세 | notices |
| H024 | 에러 페이지 | - |
| H025 | 메뉴 (드로어) | - |

## 2. 기획서 기능-화면 매핑

| 기획서 기능 | 담당 화면 |
|-------------|-----------|
| 팬 커뮤니티 & 소셜 피드 | H003, H012, H013 |
| 라이브 스트리밍 | H006, H019 |
| 콘서트 티켓 예매 | H007, H015, H022 |
| 팬 참여형 투표 | H004 |
| 광고 및 수익화 | H008 |
| 팬덤 멤버십 | H009 |
| 로그인/인증 | H002, H002-1 |

## 3. API-화면 매핑 (MVP)

> **참조 문서**: `doc/mvp/mvp_API_명세서.md`

| API 엔드포인트 | 담당 화면 | 설명 |
|----------------|-----------|------|
| POST /auth/signup | H002-1 | 회원가입 |
| POST /auth/login | H002 | 로그인 |
| POST /auth/google | H002 | 구글 소셜 로그인 |
| POST /auth/logout | H010 | 로그아웃 |
| GET /me | H016 | 내 정보 조회 |
| GET /live | H006 | 라이브 목록 |
| GET /live/{id} | H019 | 라이브 상세 |
| GET /news | H001 | 뉴스 목록 |
| GET /news/{id} | H011 | 뉴스 상세 |
| GET /search | H018 | 검색 |

> **Note**: API 명세서가 업데이트되면 이 매핑도 함께 갱신해야 합니다.

## 4. 용어 사전

문서 간 통일해야 할 용어:

| 표준 용어 | 허용 변형 | 비허용 |
|-----------|-----------|--------|
| 화면 ID | 화면ID, Screen ID | 페이지 ID |
| 사용자 | 유저, user | 회원 (문맥에 따라) |
| 게시글 | 포스트, post | 글 |
| 아티스트 | artist | 가수 |
| 투표 | poll, voting | 선거 |
| 멤버십 | membership | 구독 (문맥에 따라) |
| 포인트 | point | 리워드 (다른 의미) |

## 5. 검증 규칙 상세

### 5.1 필수 검증 (ERROR)

- 화면에서 사용하는 데이터의 DB 테이블 부재
- 기획서 핵심 기능에 대응하는 화면 없음
- 화면 ID 불일치 (문서 간 다른 ID 사용)

### 5.2 권장 검증 (WARNING)

- DB 테이블의 "활용 화면" 주석과 실제 화면 기능 불일치
- API 엔드포인트 누락 (화면 기능 대비)
- 용어 비일관성

### 5.3 정보성 검증 (INFO)

- 미사용 DB 테이블 (어떤 화면에서도 사용 안 함)
- TODO/TBD 항목 존재
- 버전 불일치 (문서 간 업데이트 날짜 차이)

## 6. 검증 제외 항목

- MVP 제외 기능 (API 명세서 "MVP에서 제외" 섹션)
- 크롤링 관련 내부 테이블 (crawled_* 중 화면 노출 없는 것)
- 시스템 내부 테이블 (auth_tokens 등)

## 7. DDD-구현 문서 매핑

### Bounded Context-화면 매핑

> **참조 문서**: `doc/ddd/bounded-contexts/`

| Bounded Context | 담당 화면 | 핵심 Aggregate |
|-----------------|-----------|----------------|
| Identity & Access | H002, H002-1, H010, H016 | User, AuthToken |
| Community | H003, H012, H013 | Post, Comment |
| Live Streaming | H006, H019 | StreamingEvent, ChatMessage |
| Voting | H004 | Poll, Vote |
| Concert & Ticket | H007, H015, H022 | Concert, Reservation |
| Points & Rewards | H008 | Point, Reward |
| Membership | H009 | Membership |
| Content Aggregation | H001, H005, H011 | News, Chart |

### Domain Model-DB 매핑

| Domain Entity | DB 테이블 | 비고 |
|---------------|-----------|------|
| User | users | Identity Context |
| Post | posts (MongoDB) | Community Context |
| Comment | comments (MongoDB) | Community Context |
| StreamingEvent | streaming_events | Live Context |
| Poll | polls | Voting Context |
| Vote | votes | Voting Context |
| Concert | crawled_concerts | Concert Context (외부 데이터) |
| Point | points, point_transactions | Rewards Context |

### Ubiquitous Language 검증

> **참조 문서**: `doc/ddd/ubiquitous-language.md`

검증 시 다음 용어가 문서 간 일관되게 사용되는지 확인:

| 도메인 용어 | 화면 표시 | DB 필드 | API 필드 |
|-------------|-----------|---------|----------|
| Fan (팬) | 사용자/팬 | users.role | user.role |
| Artist (아티스트) | 아티스트 | artists | artist |
| Post (게시글) | 게시글/포스트 | posts | post |
| Poll (투표) | 투표 | polls | poll |
| Heart (하트) | 하트/좋아요 | live_hearts | heart |

## 8. IA-화면 구조 매핑

> **참조 문서**: `doc/mvp/mvp_IA.md`

### 네비게이션 구조 검증

| IA 메뉴 | 화면 ID | 하위 화면 |
|---------|---------|-----------|
| 홈 | H001 | H011 (뉴스 상세) |
| 라이브 | H006 | H019 (라이브 상세) |
| 검색 | H018 | - |
| 마이페이지 | H016 | H020, H021, H022 |
| 설정 | H010 | H023 (고객센터) |

### User Journey 검증

> **참조 문서**: `doc/mvp/mvp_user_journey.md`

주요 사용자 여정이 화면 흐름과 일치하는지 확인:

1. **신규 가입 플로우**: H002 → H002-1 → H001
2. **콘텐츠 소비 플로우**: H001 → H011 / H006 → H019
3. **커뮤니티 참여 플로우**: H003 → H012 → H013
4. **투표 참여 플로우**: H004
