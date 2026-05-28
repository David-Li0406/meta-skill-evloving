package {{PACKAGE}}.domain.{{CONTEXT}}

import java.time.Instant

// ============================================================
// Domain Event 기본 인터페이스
// ============================================================

/**
 * Domain Event 기본 인터페이스
 *
 * 모든 Domain Event가 구현해야 하는 공통 속성을 정의합니다.
 */
sealed interface DomainEvent {
    /** 이벤트가 발생한 Aggregate의 ID */
    val aggregateId: String

    /** 이벤트 발생 시각 */
    val occurredAt: Instant

    /** 이벤트 타입 (라우팅에 사용) */
    val eventType: String get() = this::class.simpleName ?: "UnknownEvent"
}

// ============================================================
// Context별 Domain Event 예시
// ============================================================

// ------------------------------------------------------------
// {{CONTEXT}} Context Events
// ------------------------------------------------------------

/**
 * {{AGGREGATE_NAME}} 생성됨
 */
data class {{AGGREGATE_NAME}}Created(
    override val aggregateId: String,
    val {{PROPERTY_1}}: String,
    val {{PROPERTY_2}}: String,
    override val occurredAt: Instant = Instant.now()
) : DomainEvent

/**
 * {{AGGREGATE_NAME}} {{ACTION_1}} 완료됨
 */
data class {{AGGREGATE_NAME}}{{ACTION_1_PAST}}(
    override val aggregateId: String,
    override val occurredAt: Instant = Instant.now()
) : DomainEvent

/**
 * {{AGGREGATE_NAME}} {{ACTION_2}} 완료됨
 */
data class {{AGGREGATE_NAME}}{{ACTION_2_PAST}}(
    override val aggregateId: String,
    val {{PARAM}}: {{PARAM_TYPE}},
    override val occurredAt: Instant = Instant.now()
) : DomainEvent

/**
 * {{AGGREGATE_NAME}} 취소됨
 */
data class {{AGGREGATE_NAME}}Cancelled(
    override val aggregateId: String,
    val reason: String,
    override val occurredAt: Instant = Instant.now()
) : DomainEvent

// ============================================================
// FanPulse 예시 이벤트
// ============================================================

// 투표 Context
data class VoteCasted(
    override val aggregateId: String,  // VoteId
    val userId: String,
    val artistId: String,
    val voteOptionId: String,
    override val occurredAt: Instant = Instant.now()
) : DomainEvent

data class VoteSessionEnded(
    override val aggregateId: String,  // VoteSessionId
    val winnerId: String,
    val totalVotes: Int,
    override val occurredAt: Instant = Instant.now()
) : DomainEvent

data class RankingUpdated(
    override val aggregateId: String,  // RankingId
    val artistId: String,
    val previousRank: Int,
    val newRank: Int,
    override val occurredAt: Instant = Instant.now()
) : DomainEvent

// 멤버십 Context
data class VIPSubscribed(
    override val aggregateId: String,  // MembershipId
    val userId: String,
    val planType: String,
    override val occurredAt: Instant = Instant.now()
) : DomainEvent

data class VoteTicketGranted(
    override val aggregateId: String,  // VoteTicketId
    val userId: String,
    val ticketCount: Int,
    val reason: String,
    override val occurredAt: Instant = Instant.now()
) : DomainEvent

// 커뮤니티 Context
data class PostCreated(
    override val aggregateId: String,  // PostId
    val authorId: String,
    val artistId: String,
    val title: String,
    override val occurredAt: Instant = Instant.now()
) : DomainEvent

data class CommentAdded(
    override val aggregateId: String,  // PostId
    val commentId: String,
    val authorId: String,
    val content: String,
    override val occurredAt: Instant = Instant.now()
) : DomainEvent

// ============================================================
// Event Handler 예시
// ============================================================

/**
 * Domain Event Handler 인터페이스
 */
interface DomainEventHandler<T : DomainEvent> {
    fun handle(event: T)
}

/**
 * 투표 완료 시 랭킹 업데이트 핸들러
 */
class UpdateRankingOnVoteCasted(
    private val rankingRepository: RankingRepository
) : DomainEventHandler<VoteCasted> {

    override fun handle(event: VoteCasted) {
        val ranking = rankingRepository.findByArtistId(event.artistId)
            ?: throw IllegalStateException("Ranking not found: ${event.artistId}")

        ranking.incrementVoteCount()
        rankingRepository.save(ranking)
    }
}

/**
 * VIP 가입 시 투표권 부여 핸들러
 */
class GrantVoteTicketOnVIPSubscribed(
    private val voteTicketService: VoteTicketService
) : DomainEventHandler<VIPSubscribed> {

    override fun handle(event: VIPSubscribed) {
        voteTicketService.grantTickets(
            userId = event.userId,
            count = 10,  // VIP 보너스 투표권
            reason = "VIP 가입 보너스"
        )
    }
}

// ============================================================
// Event Publisher 인터페이스
// ============================================================

/**
 * Domain Event Publisher
 */
interface DomainEventPublisher {
    fun publish(event: DomainEvent)
    fun publishAll(events: List<DomainEvent>)
}

/**
 * Application Service에서 Aggregate의 이벤트를 발행하는 패턴
 */
// class CastVoteUseCase(
//     private val voteRepository: VoteRepository,
//     private val eventPublisher: DomainEventPublisher
// ) {
//     fun execute(command: CastVoteCommand) {
//         val vote = voteRepository.findById(command.voteId)
//             ?: throw VoteNotFoundException(command.voteId)
//
//         vote.cast(command.artistId, command.optionId)
//
//         voteRepository.save(vote)
//
//         // 이벤트 발행
//         eventPublisher.publishAll(vote.domainEvents)
//         vote.clearDomainEvents()
//     }
// }

// Placeholder interfaces for compilation
interface RankingRepository {
    fun findByArtistId(artistId: String): Ranking?
    fun save(ranking: Ranking)
}

interface Ranking {
    fun incrementVoteCount()
}

interface VoteTicketService {
    fun grantTickets(userId: String, count: Int, reason: String)
}
