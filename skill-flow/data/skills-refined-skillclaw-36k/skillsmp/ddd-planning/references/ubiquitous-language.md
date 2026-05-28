# Ubiquitous Language (유비쿼터스 언어)

## Overview

Ubiquitous Language는 도메인 전문가와 개발자가 공유하는 공통 언어입니다. 코드, 문서, 대화에서 일관되게 사용됩니다.

## 원칙

### 1. 도메인 전문가의 용어 우선

개발 용어가 아닌 비즈니스 용어를 사용합니다.

| ❌ 개발 용어 | ✅ 도메인 용어 |
|-------------|---------------|
| User Entity | 팬 (Fan) |
| Vote Record | 투표 (Vote) |
| Insert Data | 투표하다 (Cast) |
| Flag Status | 투표 상태 (VoteStatus) |

### 2. 명확성

모호한 표현을 피합니다.

| ❌ 모호한 표현 | ✅ 명확한 표현 |
|--------------|---------------|
| 처리하다 | 투표하다, 게시하다, 예매하다 |
| 관리하다 | 생성하다, 수정하다, 삭제하다 |
| 데이터 | 투표 결과, 게시글, 순위 |

### 3. Context별 일관성

같은 Bounded Context 내에서 동일 용어는 동일 의미를 가집니다.

```
투표 Context에서 "투표"
→ 팬이 아티스트에게 선택권을 행사하는 행위

커뮤니티 Context에서 "투표"
→ 게시글에 대한 찬반 의견 표시 (다른 의미!)
```

## 용어집 작성 가이드

### 필수 항목

1. **한글 용어**: 도메인에서 사용하는 한글 명칭
2. **영문 용어**: 코드에서 사용할 영문명
3. **정의**: 명확한 의미 설명
4. **Context**: 해당 용어가 속한 Bounded Context
5. **예시**: 실제 사용 예시

### 선택 항목

- **동의어**: 같은 의미의 다른 표현
- **반의어**: 반대 개념
- **관련 용어**: 연관된 다른 용어

## 용어집 템플릿

### Context: 투표

| 한글 | 영문 | 정의 | 예시 |
|------|------|------|------|
| 투표 | Vote | 팬이 아티스트에게 선택권을 행사하는 행위 | "BTS에 투표하다" |
| 투표 세션 | VoteSession | 특정 기간 동안 진행되는 투표 이벤트 | "주간 인기상 투표 세션" |
| 투표권 | VoteTicket | 투표할 수 있는 권한. 소모성 | "VIP는 매일 10개 투표권 부여" |
| 순위 | Ranking | 투표 집계 결과 | "1위: BTS, 2위: BLACKPINK" |
| 투표 항목 | VoteOption | 투표 대상 선택지 | "아티스트 A, 아티스트 B" |

### Context: 커뮤니티

| 한글 | 영문 | 정의 | 예시 |
|------|------|------|------|
| 게시글 | Post | 팬이 작성한 콘텐츠 | "오늘 콘서트 후기" |
| 댓글 | Comment | 게시글에 대한 반응 | "저도 갔었어요!" |
| 좋아요 | Like | 게시글/댓글에 대한 긍정 표현 | "좋아요 100개" |
| 피드 | Feed | 게시글 목록 | "팔로잉 피드" |

### Context: 멤버십

| 한글 | 영문 | 정의 | 예시 |
|------|------|------|------|
| VIP 멤버십 | VIPMembership | 유료 구독 서비스 | "월 9,900원 VIP" |
| 포인트 | Point | 리워드 적립 단위 | "광고 시청 시 100P 적립" |
| 혜택 | Benefit | VIP 회원에게 제공되는 특전 | "추가 투표권, 굿즈 할인" |

## 코드에서의 적용

### Entity/Value Object 명명

```kotlin
// ✅ 도메인 용어 사용
class Vote(val id: VoteId, val fanId: FanId, val artistId: ArtistId)
class VoteTicket(val count: Int, val expiresAt: LocalDate)

// ❌ 기술 용어 사용
class VoteEntity(val id: Long, val userId: Long, val targetId: Long)
```

### 메서드 명명

```kotlin
// ✅ 도메인 행위 표현
fun castVote(artistId: ArtistId)
fun grantVoteTickets(count: Int)
fun expireVoteSession()

// ❌ CRUD 스타일
fun insertVote(targetId: Long)
fun updateTicketCount(count: Int)
fun setSessionStatus(status: String)
```

### Domain Event 명명

```kotlin
// ✅ 과거형 비즈니스 이벤트
class VoteCasted(...)
class VoteSessionEnded(...)
class RankingUpdated(...)

// ❌ 기술적 표현
class VoteInserted(...)
class SessionStatusChanged(...)
class DataUpdated(...)
```

## 용어 진화

도메인 이해도가 높아지면 용어도 개선됩니다.

```
초기: "투표 기록" (VoteRecord)
      ↓
개선: "투표" (Vote) - 기록이 아닌 행위 자체를 표현

초기: "사용자" (User)
      ↓
개선: "팬" (Fan) - 도메인 특성 반영
```

## 용어 충돌 해결

같은 용어가 다른 Context에서 다른 의미로 사용될 때:

1. **Context 명시**: `투표Context.투표` vs `커뮤니티Context.투표`
2. **용어 분리**: `아티스트투표` vs `게시글평가`
3. **영문 구분**: `Vote` vs `Poll`
