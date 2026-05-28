package {{PACKAGE}}.domain.{{CONTEXT}}

import java.time.Instant

// ============================================================
// Domain Service
// ============================================================

/**
 * Domain Service는 다음 경우에 사용합니다:
 *
 * 1. 여러 Aggregate에 걸친 비즈니스 로직
 * 2. 특정 Aggregate에 속하지 않는 도메인 로직
 * 3. 외부 시스템과의 도메인 관련 연동
 *
 * Domain Service는 무상태(Stateless)입니다.
 */

// ============================================================
// 중복 확인 서비스 패턴
// ============================================================

/**
 * 투표 중복 확인 서비스
 *
 * 사용자가 동일 세션에서 이미 투표했는지 확인합니다.
 */
class VoteDuplicateChecker(
    private val voteRepository: VoteRepository
) {
    /**
     * 중복 투표 여부 확인
     *
     * @return true if already voted
     */
    fun isDuplicate(userId: UserId, sessionId: VoteSessionId): Boolean {
        return voteRepository.existsByUserIdAndSessionId(userId, sessionId)
    }

    /**
     * 중복 투표 검증 (예외 발생)
     *
     * @throws DuplicateVoteException if already voted
     */
    fun validateNotDuplicate(userId: UserId, sessionId: VoteSessionId) {
        if (isDuplicate(userId, sessionId)) {
            throw DuplicateVoteException(userId, sessionId)
        }
    }
}

class DuplicateVoteException(
    userId: UserId,
    sessionId: VoteSessionId
) : RuntimeException("User ${userId.value} already voted in session ${sessionId.value}")

// ============================================================
// 계산 서비스 패턴
// ============================================================

/**
 * 티켓 가격 계산 서비스
 *
 * 콘서트, 멤버십, 좌석 등급에 따른 최종 가격을 계산합니다.
 */
class TicketPriceCalculator {

    /**
     * 최종 티켓 가격 계산
     */
    fun calculate(
        basePrice: Money,
        membership: Membership?,
        seatGrade: SeatGrade,
        isEarlyBird: Boolean
    ): TicketPrice {
        var price = basePrice

        // 좌석 등급 배율 적용
        price = applySeatGradeMultiplier(price, seatGrade)

        // 멤버십 할인 적용
        val membershipDiscount = membership?.let { calculateMembershipDiscount(price, it) }
            ?: Money.zero(price.currency)

        // 얼리버드 할인 적용
        val earlyBirdDiscount = if (isEarlyBird) {
            price.applyDiscount(DiscountRate.fromPercentage(10))
        } else {
            Money.zero(price.currency)
        }

        val totalDiscount = membershipDiscount + earlyBirdDiscount
        val finalPrice = price - totalDiscount

        return TicketPrice(
            basePrice = basePrice,
            seatGradePrice = price,
            membershipDiscount = membershipDiscount,
            earlyBirdDiscount = earlyBirdDiscount,
            finalPrice = finalPrice
        )
    }

    private fun applySeatGradeMultiplier(price: Money, seatGrade: SeatGrade): Money {
        val multiplier = when (seatGrade) {
            SeatGrade.VIP -> 2.0
            SeatGrade.R -> 1.5
            SeatGrade.S -> 1.2
            SeatGrade.A -> 1.0
        }
        return Money(
            price.amount.multiply(multiplier.toBigDecimal()),
            price.currency
        )
    }

    private fun calculateMembershipDiscount(price: Money, membership: Membership): Money {
        return price.applyDiscount(membership.discountRate)
    }
}

data class TicketPrice(
    val basePrice: Money,
    val seatGradePrice: Money,
    val membershipDiscount: Money,
    val earlyBirdDiscount: Money,
    val finalPrice: Money
)

enum class SeatGrade { VIP, R, S, A }

// ============================================================
// 정책 서비스 패턴
// ============================================================

/**
 * 투표권 정책 서비스
 *
 * 투표권 부여, 소모, 만료 정책을 처리합니다.
 */
class VoteTicketPolicy(
    private val voteTicketRepository: VoteTicketRepository,
    private val clock: Clock = Clock.systemUTC()
) {
    companion object {
        const val DAILY_FREE_TICKETS = 3
        const val VIP_BONUS_TICKETS = 10
        const val AD_WATCH_TICKETS = 1
        const val TICKET_EXPIRY_DAYS = 7L
    }

    /**
     * 일일 무료 투표권 부여
     */
    fun grantDailyFreeTickets(userId: UserId): VoteTicketBundle {
        val expiresAt = clock.instant()
            .plus(java.time.Duration.ofDays(TICKET_EXPIRY_DAYS))

        return voteTicketRepository.save(
            VoteTicketBundle.create(
                userId = userId,
                count = DAILY_FREE_TICKETS,
                reason = VoteTicketReason.DAILY_FREE,
                expiresAt = expiresAt
            )
        )
    }

    /**
     * VIP 가입 보너스 투표권 부여
     */
    fun grantVIPBonusTickets(userId: UserId): VoteTicketBundle {
        val expiresAt = clock.instant()
            .plus(java.time.Duration.ofDays(30))  // VIP 투표권은 30일

        return voteTicketRepository.save(
            VoteTicketBundle.create(
                userId = userId,
                count = VIP_BONUS_TICKETS,
                reason = VoteTicketReason.VIP_BONUS,
                expiresAt = expiresAt
            )
        )
    }

    /**
     * 광고 시청 투표권 부여
     */
    fun grantAdWatchTickets(userId: UserId): VoteTicketBundle {
        val expiresAt = clock.instant()
            .plus(java.time.Duration.ofDays(1))  // 광고 투표권은 1일

        return voteTicketRepository.save(
            VoteTicketBundle.create(
                userId = userId,
                count = AD_WATCH_TICKETS,
                reason = VoteTicketReason.AD_WATCH,
                expiresAt = expiresAt
            )
        )
    }

    /**
     * 투표권 사용 가능 여부 확인
     */
    fun canUseTicket(userId: UserId): Boolean {
        return getAvailableTicketCount(userId) > 0
    }

    /**
     * 사용 가능한 투표권 수 조회
     */
    fun getAvailableTicketCount(userId: UserId): Int {
        val now = clock.instant()
        return voteTicketRepository.findAvailableByUserId(userId, now)
            .sumOf { it.remainingCount }
    }

    /**
     * 투표권 소모
     */
    fun consumeTicket(userId: UserId): VoteTicketBundle {
        val now = clock.instant()
        val availableTickets = voteTicketRepository.findAvailableByUserId(userId, now)
            .sortedBy { it.expiresAt }  // 만료 임박한 것부터 사용

        if (availableTickets.isEmpty()) {
            throw InsufficientVoteTicketsException(userId)
        }

        val ticketToUse = availableTickets.first()
        ticketToUse.consume()

        return voteTicketRepository.save(ticketToUse)
    }
}

class InsufficientVoteTicketsException(userId: UserId)
    : RuntimeException("Insufficient vote tickets for user: ${userId.value}")

enum class VoteTicketReason {
    DAILY_FREE,
    VIP_BONUS,
    AD_WATCH,
    EVENT_REWARD
}

// ============================================================
// 외부 시스템 연동 서비스 패턴
// ============================================================

/**
 * 콘텐츠 필터링 서비스
 *
 * 외부 AI 서비스를 통해 부적절한 콘텐츠를 필터링합니다.
 */
interface ContentFilteringService {
    fun filter(content: String): ContentFilterResult
}

data class ContentFilterResult(
    val isClean: Boolean,
    val filteredContent: String,
    val detectedIssues: List<ContentIssue>
)

data class ContentIssue(
    val type: ContentIssueType,
    val severity: Severity,
    val description: String
)

enum class ContentIssueType {
    PROFANITY,
    SPAM,
    HATE_SPEECH,
    PERSONAL_INFO,
    ADULT_CONTENT
}

enum class Severity { LOW, MEDIUM, HIGH }

// ============================================================
// Placeholder types (컴파일용)
// ============================================================

interface VoteRepository {
    fun existsByUserIdAndSessionId(userId: UserId, sessionId: VoteSessionId): Boolean
}

interface VoteTicketRepository {
    fun save(bundle: VoteTicketBundle): VoteTicketBundle
    fun findAvailableByUserId(userId: UserId, now: Instant): List<VoteTicketBundle>
}

class VoteTicketBundle private constructor(
    val userId: UserId,
    var remainingCount: Int,
    val reason: VoteTicketReason,
    val expiresAt: Instant
) {
    companion object {
        fun create(
            userId: UserId,
            count: Int,
            reason: VoteTicketReason,
            expiresAt: Instant
        ) = VoteTicketBundle(userId, count, reason, expiresAt)
    }

    fun consume() {
        require(remainingCount > 0)
        remainingCount--
    }
}

class Membership(val discountRate: DiscountRate)

typealias Clock = java.time.Clock
