package {{PACKAGE}}.domain.{{CONTEXT}}

// ============================================================
// Repository 인터페이스 (Domain Layer)
// ============================================================

/**
 * {{AGGREGATE_NAME}} Repository 인터페이스
 *
 * Domain Layer에 위치합니다.
 * Infrastructure Layer에서 구현됩니다.
 */
interface {{AGGREGATE_NAME}}Repository {

    /**
     * Aggregate 저장
     *
     * 새 Aggregate 생성 또는 기존 Aggregate 업데이트
     */
    fun save({{AGGREGATE_VAR}}: {{AGGREGATE_NAME}}): {{AGGREGATE_NAME}}

    /**
     * ID로 Aggregate 조회
     *
     * @return Aggregate 또는 null
     */
    fun findById(id: {{AGGREGATE_NAME}}Id): {{AGGREGATE_NAME}}?

    /**
     * ID로 Aggregate 조회 (필수)
     *
     * @throws {{AGGREGATE_NAME}}NotFoundException Aggregate를 찾을 수 없는 경우
     */
    fun getById(id: {{AGGREGATE_NAME}}Id): {{AGGREGATE_NAME}} {
        return findById(id)
            ?: throw {{AGGREGATE_NAME}}NotFoundException(id)
    }

    /**
     * 존재 여부 확인
     */
    fun existsById(id: {{AGGREGATE_NAME}}Id): Boolean

    /**
     * Aggregate 삭제
     */
    fun delete({{AGGREGATE_VAR}}: {{AGGREGATE_NAME}})

    /**
     * ID로 삭제
     */
    fun deleteById(id: {{AGGREGATE_NAME}}Id)

    // ============ 도메인 특화 쿼리 ============

    /**
     * {{RELATED_AGGREGATE}}로 조회
     */
    fun findBy{{RELATED_AGGREGATE}}Id({{RELATED_AGGREGATE_VAR}}Id: {{RELATED_AGGREGATE}}Id): List<{{AGGREGATE_NAME}}>

    /**
     * 상태로 조회
     */
    fun findByStatus(status: {{AGGREGATE_NAME}}Status): List<{{AGGREGATE_NAME}}>

    /**
     * 중복 확인 (비즈니스 규칙)
     */
    fun existsBy{{UNIQUE_CONDITION}}({{PARAM}}: {{PARAM_TYPE}}): Boolean
}

// ============================================================
// 예외 클래스
// ============================================================

/**
 * Aggregate를 찾을 수 없는 경우
 */
class {{AGGREGATE_NAME}}NotFoundException(
    id: {{AGGREGATE_NAME}}Id
) : RuntimeException("{{AGGREGATE_NAME}} not found: ${id.value}")

// ============================================================
// FanPulse 예시 Repository
// ============================================================

/**
 * Vote Repository
 */
interface VoteRepository {
    fun save(vote: Vote): Vote
    fun findById(id: VoteId): Vote?
    fun getById(id: VoteId): Vote = findById(id)
        ?: throw VoteNotFoundException(id)

    fun findByUserId(userId: UserId): List<Vote>
    fun findBySessionId(sessionId: VoteSessionId): List<Vote>
    fun existsByUserIdAndSessionId(userId: UserId, sessionId: VoteSessionId): Boolean

    fun countBySessionIdAndOptionId(sessionId: VoteSessionId, optionId: VoteOptionId): Int
}

class VoteNotFoundException(id: VoteId)
    : RuntimeException("Vote not found: ${id.value}")

/**
 * VoteSession Repository
 */
interface VoteSessionRepository {
    fun save(session: VoteSession): VoteSession
    fun findById(id: VoteSessionId): VoteSession?
    fun getById(id: VoteSessionId): VoteSession = findById(id)
        ?: throw VoteSessionNotFoundException(id)

    fun findActiveByArtistId(artistId: ArtistId): VoteSession?
    fun findByStatus(status: VoteSessionStatus): List<VoteSession>
    fun findEndingSoon(within: java.time.Duration): List<VoteSession>
}

class VoteSessionNotFoundException(id: VoteSessionId)
    : RuntimeException("VoteSession not found: ${id.value}")

/**
 * Post Repository (커뮤니티)
 */
interface PostRepository {
    fun save(post: Post): Post
    fun findById(id: PostId): Post?
    fun getById(id: PostId): Post = findById(id)
        ?: throw PostNotFoundException(id)

    fun findByAuthorId(authorId: UserId, pageable: Pageable): Page<Post>
    fun findByArtistId(artistId: ArtistId, pageable: Pageable): Page<Post>
    fun searchByKeyword(keyword: String, pageable: Pageable): Page<Post>
}

class PostNotFoundException(id: PostId)
    : RuntimeException("Post not found: ${id.value}")

// ============================================================
// 페이지네이션 지원
// ============================================================

/**
 * 페이지네이션 요청
 */
data class Pageable(
    val page: Int = 0,
    val size: Int = 20,
    val sort: Sort = Sort.UNSORTED
) {
    init {
        require(page >= 0) { "Page must be >= 0" }
        require(size in 1..100) { "Size must be 1-100" }
    }

    val offset: Long get() = (page * size).toLong()

    companion object {
        fun of(page: Int, size: Int) = Pageable(page, size)
        fun first(size: Int) = Pageable(0, size)
    }
}

/**
 * 정렬
 */
data class Sort(
    val orders: List<Order>
) {
    data class Order(
        val property: String,
        val direction: Direction
    )

    enum class Direction { ASC, DESC }

    companion object {
        val UNSORTED = Sort(emptyList())
        fun by(property: String, direction: Direction = Direction.ASC) =
            Sort(listOf(Order(property, direction)))
    }
}

/**
 * 페이지 결과
 */
data class Page<T>(
    val content: List<T>,
    val totalElements: Long,
    val totalPages: Int,
    val currentPage: Int,
    val size: Int
) {
    val hasNext: Boolean get() = currentPage < totalPages - 1
    val hasPrevious: Boolean get() = currentPage > 0
    val isEmpty: Boolean get() = content.isEmpty()

    fun <R> map(transform: (T) -> R): Page<R> = Page(
        content = content.map(transform),
        totalElements = totalElements,
        totalPages = totalPages,
        currentPage = currentPage,
        size = size
    )

    companion object {
        fun <T> empty(): Page<T> = Page(emptyList(), 0, 0, 0, 0)

        fun <T> of(
            content: List<T>,
            pageable: Pageable,
            totalElements: Long
        ): Page<T> {
            val totalPages = if (pageable.size == 0) 0
            else ((totalElements + pageable.size - 1) / pageable.size).toInt()

            return Page(
                content = content,
                totalElements = totalElements,
                totalPages = totalPages,
                currentPage = pageable.page,
                size = pageable.size
            )
        }
    }
}

// Placeholder types
class Vote
class VoteId(val value: String)
class VoteSession
class VoteSessionId(val value: String)
enum class VoteSessionStatus
class VoteOptionId(val value: String)
class Post
class PostId(val value: String)
class UserId(val value: String)
class ArtistId(val value: String)
