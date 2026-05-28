# Tactical Design (전술적 설계)

## Overview

Tactical Design은 Bounded Context 내부의 도메인 모델을 구체적으로 설계하는 DDD의 하위 레벨 설계입니다.

## Aggregate

### 정의

Aggregate는 일관성 경계를 가진 Entity와 Value Object의 클러스터입니다.

### 설계 원칙

1. **작은 Aggregate**: 가능한 한 작게 (대부분 1개 Entity)
2. **ID 참조**: Aggregate 간 객체 참조 대신 ID 참조
3. **트랜잭션 경계**: 하나의 트랜잭션 = 하나의 Aggregate
4. **불변식 보호**: 비즈니스 규칙은 Aggregate 내부에서 보호

### 예시

```kotlin
// ✅ 작은 Aggregate + ID 참조
class Vote(
    val id: VoteId,
    val userId: UserId,          // ID 참조
    val artistId: ArtistId,      // ID 참조
    private var status: VoteStatus
) {
    fun cast() {
        require(status == VoteStatus.PENDING) { "이미 투표 완료" }
        status = VoteStatus.COMPLETED
    }
}
```

## Entity

### 정의

식별자(ID)를 가지며, 생명주기 동안 연속성을 유지하는 객체입니다.

### 특징

- 고유 식별자로 구분
- 상태 변경 가능
- equals/hashCode는 ID 기반

```kotlin
class Concert(
    val id: ConcertId,
    var name: String,
    var venue: Venue,
    private var status: ConcertStatus
) {
    override fun equals(other: Any?) = other is Concert && id == other.id
    override fun hashCode() = id.hashCode()
}
```

## Value Object

### 정의

속성만으로 식별되는 불변 객체입니다.

### 특징

- 불변성
- 자가 검증
- 개념적 완전성

```kotlin
data class Email private constructor(val value: String) {
    companion object {
        fun of(value: String): Email {
            require(value.matches("^[A-Za-z0-9+_.-]+@.+$".toRegex()))
            return Email(value)
        }
    }
}

data class Money(val amount: BigDecimal, val currency: Currency) {
    operator fun plus(other: Money): Money {
        require(currency == other.currency)
        return Money(amount + other.amount, currency)
    }
}
```

## Domain Event

### 정의

도메인에서 발생한 중요한 사건. 과거형으로 명명합니다.

```kotlin
sealed interface DomainEvent {
    val occurredAt: Instant
    val aggregateId: String
}

data class VoteCasted(
    override val aggregateId: String,
    val userId: String,
    val artistId: String,
    override val occurredAt: Instant = Instant.now()
) : DomainEvent
```

### 활용

- Eventual Consistency (여러 Aggregate 간 일관성)
- 감사 로그
- 알림 발송
- Context 간 통합

## Domain Service

### 정의

여러 Aggregate에 걸친 비즈니스 로직을 담는 무상태 서비스입니다.

```kotlin
class VoteDuplicateChecker(
    private val voteRepository: VoteRepository
) {
    fun isDuplicate(userId: UserId, sessionId: VoteSessionId): Boolean {
        return voteRepository.existsByUserIdAndSessionId(userId, sessionId)
    }
}
```

## Repository

### 정의

Aggregate의 영속성을 담당하는 인터페이스입니다.

```kotlin
// Domain Layer - 인터페이스
interface VoteRepository {
    fun save(vote: Vote): Vote
    fun findById(id: VoteId): Vote?
    fun findByUserId(userId: UserId): List<Vote>
}

// Infrastructure Layer - 구현
class JpaVoteRepository : VoteRepository { ... }
```

## Entity vs Value Object

| 기준 | Entity | Value Object |
|------|--------|--------------|
| 식별 | ID | 속성 |
| 가변성 | 가변 | 불변 |
| 예시 | User, Vote, Concert | Email, Money, DateRange |

## Best Practices

- ✅ Aggregate는 작게 유지
- ✅ ID 참조로 결합도 최소화
- ✅ Value Object로 도메인 개념 표현
- ✅ Domain Event로 Eventual Consistency
- ❌ Aggregate 간 객체 참조
- ❌ 여러 Aggregate를 한 트랜잭션에서 수정
- ❌ Primitive Obsession (String, Int 남용)
