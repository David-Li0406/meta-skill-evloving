package {{PACKAGE}}.domain.{{CONTEXT}}

import java.time.Instant

/**
 * {{AGGREGATE_NAME}} Aggregate Root
 *
 * 불변식:
 * - {{INVARIANT_1}}
 * - {{INVARIANT_2}}
 */
class {{AGGREGATE_NAME}} private constructor(
    val id: {{AGGREGATE_NAME}}Id,
    // Value Objects
    private var _status: {{AGGREGATE_NAME}}Status,
    // 다른 Aggregate는 ID로 참조
    val {{RELATED_AGGREGATE_VAR}}Id: {{RELATED_AGGREGATE}}Id,
    // 생성 시점
    val createdAt: Instant
) {
    // Domain Events
    private val _domainEvents = mutableListOf<DomainEvent>()
    val domainEvents: List<DomainEvent> get() = _domainEvents.toList()

    // 상태 조회 (방어적 복사 또는 불변 반환)
    val status: {{AGGREGATE_NAME}}Status get() = _status

    companion object {
        /**
         * Aggregate 생성 팩토리 메서드
         */
        fun create(
            id: {{AGGREGATE_NAME}}Id,
            {{RELATED_AGGREGATE_VAR}}Id: {{RELATED_AGGREGATE}}Id
        ): {{AGGREGATE_NAME}} {
            val aggregate = {{AGGREGATE_NAME}}(
                id = id,
                _status = {{AGGREGATE_NAME}}Status.CREATED,
                {{RELATED_AGGREGATE_VAR}}Id = {{RELATED_AGGREGATE_VAR}}Id,
                createdAt = Instant.now()
            )

            // 생성 이벤트 발행
            aggregate.registerEvent(
                {{AGGREGATE_NAME}}Created(
                    aggregateId = id.value,
                    {{RELATED_AGGREGATE_VAR}}Id = {{RELATED_AGGREGATE_VAR}}Id.value,
                    occurredAt = Instant.now()
                )
            )

            return aggregate
        }

        /**
         * Repository에서 복원 시 사용
         */
        fun reconstitute(
            id: {{AGGREGATE_NAME}}Id,
            status: {{AGGREGATE_NAME}}Status,
            {{RELATED_AGGREGATE_VAR}}Id: {{RELATED_AGGREGATE}}Id,
            createdAt: Instant
        ): {{AGGREGATE_NAME}} {
            return {{AGGREGATE_NAME}}(
                id = id,
                _status = status,
                {{RELATED_AGGREGATE_VAR}}Id = {{RELATED_AGGREGATE_VAR}}Id,
                createdAt = createdAt
            )
        }
    }

    // ============ 비즈니스 로직 ============

    /**
     * {{BUSINESS_ACTION_1}}
     *
     * @throws IllegalStateException {{PRECONDITION_1}}
     */
    fun {{ACTION_1}}() {
        // 사전 조건 검증 (불변식)
        require(_status == {{AGGREGATE_NAME}}Status.CREATED) {
            "{{ERROR_MESSAGE_1}}"
        }

        // 상태 변경
        _status = {{AGGREGATE_NAME}}Status.{{NEXT_STATUS}}

        // 이벤트 발행
        registerEvent(
            {{AGGREGATE_NAME}}{{ACTION_1_PAST}}(
                aggregateId = id.value,
                occurredAt = Instant.now()
            )
        )
    }

    /**
     * {{BUSINESS_ACTION_2}}
     */
    fun {{ACTION_2}}({{PARAM}}: {{PARAM_TYPE}}) {
        require(_status != {{AGGREGATE_NAME}}Status.COMPLETED) {
            "{{ERROR_MESSAGE_2}}"
        }

        // 비즈니스 로직

        registerEvent(
            {{AGGREGATE_NAME}}{{ACTION_2_PAST}}(
                aggregateId = id.value,
                {{PARAM}} = {{PARAM}},
                occurredAt = Instant.now()
            )
        )
    }

    // ============ 이벤트 관리 ============

    private fun registerEvent(event: DomainEvent) {
        _domainEvents.add(event)
    }

    fun clearDomainEvents() {
        _domainEvents.clear()
    }

    // ============ 동등성 (ID 기반) ============

    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other !is {{AGGREGATE_NAME}}) return false
        return id == other.id
    }

    override fun hashCode(): Int = id.hashCode()

    override fun toString(): String =
        "{{AGGREGATE_NAME}}(id=$id, status=$_status)"
}

/**
 * Aggregate ID (Value Object)
 */
@JvmInline
value class {{AGGREGATE_NAME}}Id(val value: String) {
    init {
        require(value.isNotBlank()) { "{{AGGREGATE_NAME}}Id cannot be blank" }
    }

    companion object {
        fun generate(): {{AGGREGATE_NAME}}Id =
            {{AGGREGATE_NAME}}Id(java.util.UUID.randomUUID().toString())
    }
}

/**
 * Aggregate 상태
 */
enum class {{AGGREGATE_NAME}}Status {
    CREATED,
    {{NEXT_STATUS}},
    COMPLETED,
    CANCELLED
}
