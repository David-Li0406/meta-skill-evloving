package {{PACKAGE}}.domain.{{CONTEXT}}

import java.math.BigDecimal

// ============================================================
// 기본 Value Object 패턴
// ============================================================

/**
 * {{VALUE_OBJECT_NAME}}
 *
 * 불변 객체입니다. 생성 시점에 유효성이 검증됩니다.
 */
data class {{VALUE_OBJECT_NAME}}(
    val {{PROPERTY_1}}: {{PROPERTY_1_TYPE}},
    val {{PROPERTY_2}}: {{PROPERTY_2_TYPE}}
) {
    init {
        require({{VALIDATION_1}}) { "{{ERROR_MESSAGE_1}}" }
        require({{VALIDATION_2}}) { "{{ERROR_MESSAGE_2}}" }
    }

    // 비즈니스 로직
    fun {{BUSINESS_METHOD}}(): {{RETURN_TYPE}} {
        // 구현
        return {{RETURN_VALUE}}
    }
}

// ============================================================
// Private Constructor 패턴 (복잡한 생성 로직)
// ============================================================

/**
 * Email Value Object
 *
 * 이메일 형식을 검증하는 Value Object
 */
data class Email private constructor(val value: String) {
    companion object {
        private val EMAIL_REGEX = "^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+$".toRegex()

        fun of(value: String): Email {
            require(value.matches(EMAIL_REGEX)) {
                "유효하지 않은 이메일 형식입니다: $value"
            }
            return Email(value.lowercase())
        }
    }

    val domain: String get() = value.substringAfter("@")
    val localPart: String get() = value.substringBefore("@")
}

// ============================================================
// Money 패턴 (화폐 연산)
// ============================================================

/**
 * Money Value Object
 *
 * 금액과 통화를 함께 표현합니다.
 */
data class Money(
    val amount: BigDecimal,
    val currency: Currency
) {
    init {
        require(amount >= BigDecimal.ZERO) {
            "금액은 0 이상이어야 합니다: $amount"
        }
    }

    operator fun plus(other: Money): Money {
        requireSameCurrency(other)
        return Money(amount + other.amount, currency)
    }

    operator fun minus(other: Money): Money {
        requireSameCurrency(other)
        require(amount >= other.amount) {
            "잔액이 부족합니다"
        }
        return Money(amount - other.amount, currency)
    }

    operator fun times(multiplier: Int): Money {
        return Money(amount * multiplier.toBigDecimal(), currency)
    }

    fun applyDiscount(discountRate: DiscountRate): Money {
        val discountAmount = amount * discountRate.rate
        return Money(amount - discountAmount, currency)
    }

    private fun requireSameCurrency(other: Money) {
        require(currency == other.currency) {
            "통화가 다릅니다: $currency vs ${other.currency}"
        }
    }

    companion object {
        fun krw(amount: Long) = Money(amount.toBigDecimal(), Currency.KRW)
        fun usd(amount: Double) = Money(amount.toBigDecimal(), Currency.USD)
        fun zero(currency: Currency) = Money(BigDecimal.ZERO, currency)
    }
}

enum class Currency {
    KRW, USD, JPY, EUR
}

// ============================================================
// 범위 패턴 (DateRange, NumericRange)
// ============================================================

/**
 * DateRange Value Object
 *
 * 날짜 범위를 표현합니다.
 */
data class DateRange(
    val start: java.time.LocalDate,
    val end: java.time.LocalDate
) {
    init {
        require(start <= end) {
            "시작일($start)은 종료일($end)보다 이전이어야 합니다"
        }
    }

    fun contains(date: java.time.LocalDate): Boolean {
        return date in start..end
    }

    fun overlaps(other: DateRange): Boolean {
        return start <= other.end && other.start <= end
    }

    fun duration(): Long {
        return java.time.temporal.ChronoUnit.DAYS.between(start, end)
    }
}

// ============================================================
// 비율/백분율 패턴
// ============================================================

/**
 * DiscountRate Value Object
 *
 * 할인율을 표현합니다. (0.0 ~ 1.0)
 */
@JvmInline
value class DiscountRate(val rate: BigDecimal) {
    init {
        require(rate >= BigDecimal.ZERO && rate <= BigDecimal.ONE) {
            "할인율은 0과 1 사이여야 합니다: $rate"
        }
    }

    companion object {
        fun fromPercentage(percentage: Int): DiscountRate {
            require(percentage in 0..100) {
                "백분율은 0~100 사이여야 합니다: $percentage"
            }
            return DiscountRate(percentage.toBigDecimal().divide(100.toBigDecimal()))
        }

        val NONE = DiscountRate(BigDecimal.ZERO)
        val HALF = DiscountRate(BigDecimal("0.5"))
        val FULL = DiscountRate(BigDecimal.ONE)
    }

    fun toPercentage(): Int = (rate * 100.toBigDecimal()).toInt()
}

// ============================================================
// Inline Value Class 패턴 (단순 래핑)
// ============================================================

/**
 * Nickname Value Object
 *
 * 닉네임을 표현합니다. (2~20자)
 */
@JvmInline
value class Nickname(val value: String) {
    init {
        require(value.length in 2..20) {
            "닉네임은 2~20자여야 합니다: ${value.length}자"
        }
        require(!value.contains(Regex("[^a-zA-Z0-9가-힣_]"))) {
            "닉네임에 특수문자를 사용할 수 없습니다"
        }
    }
}

/**
 * Count Value Object
 *
 * 0 이상의 수량을 표현합니다.
 */
@JvmInline
value class Count(val value: Int) {
    init {
        require(value >= 0) { "수량은 0 이상이어야 합니다: $value" }
    }

    operator fun plus(other: Count) = Count(value + other.value)
    operator fun minus(other: Count): Count {
        require(value >= other.value) { "수량이 부족합니다" }
        return Count(value - other.value)
    }

    fun isZero() = value == 0

    companion object {
        val ZERO = Count(0)
        val ONE = Count(1)
    }
}
