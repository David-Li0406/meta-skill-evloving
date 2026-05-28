package {{PACKAGE}}.domain.{{CONTEXT}}

import java.time.Instant

/**
 * {{ENTITY_NAME}} Entity
 *
 * Aggregate 내부의 Entity입니다.
 * Aggregate Root를 통해서만 접근/수정됩니다.
 */
class {{ENTITY_NAME}} internal constructor(
    val id: {{ENTITY_NAME}}Id,
    private var _{{PROPERTY_1}}: {{PROPERTY_1_TYPE}},
    private var _{{PROPERTY_2}}: {{PROPERTY_2_TYPE}},
    val createdAt: Instant
) {
    // 속성 조회
    val {{PROPERTY_1}}: {{PROPERTY_1_TYPE}} get() = _{{PROPERTY_1}}
    val {{PROPERTY_2}}: {{PROPERTY_2_TYPE}} get() = _{{PROPERTY_2}}

    companion object {
        /**
         * Entity 생성 팩토리 메서드
         * Aggregate Root에서만 호출됩니다.
         */
        internal fun create(
            id: {{ENTITY_NAME}}Id,
            {{PROPERTY_1}}: {{PROPERTY_1_TYPE}},
            {{PROPERTY_2}}: {{PROPERTY_2_TYPE}}
        ): {{ENTITY_NAME}} {
            return {{ENTITY_NAME}}(
                id = id,
                _{{PROPERTY_1}} = {{PROPERTY_1}},
                _{{PROPERTY_2}} = {{PROPERTY_2}},
                createdAt = Instant.now()
            )
        }

        /**
         * Repository에서 복원 시 사용
         */
        internal fun reconstitute(
            id: {{ENTITY_NAME}}Id,
            {{PROPERTY_1}}: {{PROPERTY_1_TYPE}},
            {{PROPERTY_2}}: {{PROPERTY_2_TYPE}},
            createdAt: Instant
        ): {{ENTITY_NAME}} {
            return {{ENTITY_NAME}}(
                id = id,
                _{{PROPERTY_1}} = {{PROPERTY_1}},
                _{{PROPERTY_2}} = {{PROPERTY_2}},
                createdAt = createdAt
            )
        }
    }

    // ============ 비즈니스 로직 ============

    /**
     * {{PROPERTY_1}} 업데이트
     * Aggregate Root를 통해 호출됩니다.
     */
    internal fun update{{PROPERTY_1_CAPITALIZED}}(new{{PROPERTY_1_CAPITALIZED}}: {{PROPERTY_1_TYPE}}) {
        // 유효성 검증
        require({{VALIDATION_CONDITION}}) {
            "{{VALIDATION_ERROR_MESSAGE}}"
        }

        _{{PROPERTY_1}} = new{{PROPERTY_1_CAPITALIZED}}
    }

    // ============ 동등성 (ID 기반) ============

    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other !is {{ENTITY_NAME}}) return false
        return id == other.id
    }

    override fun hashCode(): Int = id.hashCode()

    override fun toString(): String =
        "{{ENTITY_NAME}}(id=$id, {{PROPERTY_1}}=$_{{PROPERTY_1}})"
}

/**
 * Entity ID (Value Object)
 */
@JvmInline
value class {{ENTITY_NAME}}Id(val value: String) {
    init {
        require(value.isNotBlank()) { "{{ENTITY_NAME}}Id cannot be blank" }
    }

    companion object {
        fun generate(): {{ENTITY_NAME}}Id =
            {{ENTITY_NAME}}Id(java.util.UUID.randomUUID().toString())
    }
}
