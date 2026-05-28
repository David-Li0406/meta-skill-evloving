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

| API 엔드포인트 | 담당 화면 |
|----------------|-----------|
| POST /auth/signup | H002-1 |
| POST /auth/login | H002 |
| POST /auth/google | H002 |
| GET /me | H016 |
| GET /live | H006 |
| GET /live/{id} | H019 |
| GET /news | H001 |
| GET /news/{id} | H011 |
| GET /search | H018 |

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

- MVP 제외 기능 (API 계약서 "MVP에서 제외" 섹션)
- 크롤링 관련 내부 테이블 (crawled_* 중 화면 노출 없는 것)
- 시스템 내부 테이블 (auth_tokens 등)
