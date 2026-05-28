---
name: coding-convention
description: Kotlin 코드 작성, 코드 리뷰, 리팩토링 시 사용. 네이밍 규칙, 함수/클래스 설계, 레이어별 책임 분리 등 코딩 컨벤션을 따름.
---

# 코딩 컨벤션 (Kotlin + Spring Boot)

이 문서는 Kotlin과 Spring Boot 4를 사용하여 깔끔하고 유지보수하기 쉬운 코드를 작성하기 위한 지침을 제공합니다.

---

## 1. 네이밍 규칙

### 1.1 의미 있는 이름 사용

```kotlin
// Bad - 의미 불명확
val d: Int = 7
fun calc(x: Int): Int

// Good - 의도가 명확
val daysSinceLastLogin: Int = 7
fun calculateDiscountedPrice(originalPrice: Int): Int
```

### 1.2 일관된 네이밍 컨벤션

| 대상        | 컨벤션                  | 예시                                     |
|-----------|----------------------|----------------------------------------|
| 클래스/인터페이스 | PascalCase           | `TermService`, `WorkspaceRepository`   |
| 함수/변수     | camelCase            | `findByEmail()`, `accessToken`         |
| 상수        | SCREAMING_SNAKE_CASE | `MAX_RETRY_COUNT`, `DEFAULT_PAGE_SIZE` |
| 패키지       | lowercase            | `com.mkroo.termbase.domain`            |

### 1.3 도메인 용어 사용

프로젝트의 도메인 언어(Ubiquitous Language)를 일관되게 사용합니다.

```kotlin
// Bad - 일반적인 용어
class WordManager

fun addWord(word: String)

// Good - 도메인 용어
class TermService

fun registerTerm(name: String, definition: String)
```

### 1.4 접두사/접미사 규칙

| 유형     | 패턴                    | 예시                                                |
|--------|-----------------------|---------------------------------------------------|
| 인터페이스  | 명사/형용사 (접두사 없음)       | `TermRepository`, `Extractable`                   |
| 구현체    | 기술명 + 인터페이스명          | `JpaTermRepository`, `KomoranTermExtractor`       |
| 추상 클래스 | Abstract + 이름         | `AbstractMessageProcessor`                        |
| DTO    | 용도 + Request/Response | `CreateTermRequest`, `TermFrequencyResponse`      |
| 예외     | 도메인명 + Exception      | `TermNotFoundException`, `InvalidPeriodException` |

---

## 2. 함수 설계

### 2.1 단일 책임 원칙 (SRP)

함수는 하나의 작업만 수행해야 합니다.

```kotlin
// Bad - 여러 책임을 가짐
fun processAndSaveAndNotify(message: SlackMessage) {
    val terms = extractTerms(message.text)
    termOccurrenceRepository.saveAll(terms.map { /* ... */ })
    slackClient.postMessage(/* ... */)
}

// Good - 각 함수가 하나의 책임
fun processMessage(message: SlackMessage): List<ExtractedTerm> {
    return termExtractor.extract(message.text)
}

fun saveOccurrences(terms: List<ExtractedTerm>, message: SlackMessage) {
    termOccurrenceRepository.saveAll(terms.map { /* ... */ })
}

fun notifyExtraction(channelId: String, termCount: Int) {
    slackClient.postMessage(/* ... */)
}
```

### 2.2 함수 파라미터

- 파라미터는 3개 이하로 유지
- 많은 파라미터가 필요하면 객체로 그룹화

```kotlin
// Bad - 파라미터가 너무 많음
fun findTerms(
    channelIds: List<Long>,
    startDate: LocalDate,
    endDate: LocalDate,
    excludeRegistered: Boolean,
    excludeIgnored: Boolean,
    limit: Int
): List<TermFrequency>

// Good - Value Object로 그룹화
fun findTerms(query: FrequencyQuery): List<TermFrequency>

data class FrequencyQuery(
    val channelIds: List<Long>,
    val period: DateRange,
    val excludeRegistered: Boolean = false,
    val excludeIgnored: Boolean = true,
    val limit: Int = 100
)
```

### 2.3 함수 길이

- 함수는 20줄 이하로 유지
- 길어지면 private 함수로 분리

```kotlin
// Good - 적절한 추상화 레벨 유지
fun reindex(request: ReindexRequest): IndexVersion {
    val version = createNewVersion(request)
    val channels = findMonitoringChannels()

    channels.forEach { channel ->
        processChannelMessages(channel, version, request.period)
    }

    return completeVersion(version)
}

private fun processChannelMessages(
    channel: Channel,
    version: IndexVersion,
    period: DateRange
) {
    // 채널별 메시지 처리 로직
}
```

### 2.4 명령과 쿼리 분리 (CQS)

상태를 변경하는 함수(Command)와 값을 반환하는 함수(Query)를 분리합니다.

```kotlin
// Bad - 상태 변경과 조회가 혼합
fun getOrCreateTerm(name: String): Term {
    return termRepository.findByName(name)
        ?: termRepository.save(Term(name = name))
}

// Good - 명시적으로 분리
// Query
fun findTermByName(name: String): Term?

// Command (필요시 별도 호출)
fun createTerm(name: String): Term
```

---

## 3. 클래스 설계

### 3.1 작은 클래스 유지

- 클래스는 200줄 이하로 유지
- 하나의 명확한 책임만 가짐

### 3.2 불변 객체 선호

```kotlin
// Good - 불변 data class
data class ExtractedTerm(
    val term: String,
    val originalForm: String,
    val position: Int
)

// Good - 불변 Entity (상태 변경은 새 인스턴스 반환)
class Term private constructor(
    val id: Long?,
    val name: String,
    val definition: String?,
    val ignored: Boolean,
    val ignoredReason: String?,
    val ignoredAt: Instant?
) {
    fun ignore(reason: String): Term = copy(
        ignored = true,
        ignoredReason = reason,
        ignoredAt = Instant.now()
    )

    fun unignore(): Term = copy(
        ignored = false,
        ignoredReason = null,
        ignoredAt = null
    )

    private fun copy(
        ignored: Boolean = this.ignored,
        ignoredReason: String? = this.ignoredReason,
        ignoredAt: Instant? = this.ignoredAt
    ): Term = Term(id, name, definition, ignored, ignoredReason, ignoredAt)
}
```

### 3.3 상속보다 합성

```kotlin
// Bad - 불필요한 상속
class KomoranTermExtractor : AbstractTermExtractor() {
    override fun doExtract(text: String): List<String> { /* ... */
    }
}

// Good - 합성 사용
class KomoranTermExtractor(
    private val komoran: Komoran,
    private val dictionaryProvider: DictionaryProvider
) : TermExtractor {
    override fun extract(text: String): List<ExtractedTerm> {
        val dictionary = dictionaryProvider.getUserDictionary()
        // komoran을 사용한 추출 로직
    }
}
```

### 3.4 sealed class 활용

제한된 계층 구조에는 sealed class를 사용합니다.

```kotlin
sealed class IndexStatus {
    data object Running : IndexStatus()
    data object Completed : IndexStatus()
    data class Failed(val reason: String) : IndexStatus()
}

// 사용 시 when에서 else 불필요
fun handleStatus(status: IndexStatus) = when (status) {
    is IndexStatus.Running   -> "재인덱싱 진행 중..."
    is IndexStatus.Completed -> "완료"
    is IndexStatus.Failed    -> "실패: ${status.reason}"
}
```

---

## 4. Kotlin 관용구 활용

### 4.1 Extension Functions

유틸리티 메서드 대신 확장 함수를 사용합니다.

```kotlin
// Bad - 유틸리티 클래스
object StringUtils {
    fun isValidTermName(name: String): Boolean =
        name.isNotBlank() && name.length <= 100
}

// Good - 확장 함수
fun String.isValidTermName(): Boolean =
    isNotBlank() && length <= 100

// 사용
if (termName.isValidTermName()) { /* ... */ }
```

### 4.2 Scope Functions 적절히 사용

| 함수      | 컨텍스트 객체 | 반환 값      | 용도             |
|---------|---------|-----------|----------------|
| `let`   | `it`    | Lambda 결과 | null 체크, 변환    |
| `run`   | `this`  | Lambda 결과 | 객체 설정 후 결과 반환  |
| `with`  | `this`  | Lambda 결과 | 객체 메서드 여러 번 호출 |
| `apply` | `this`  | 컨텍스트 객체   | 객체 초기화         |
| `also`  | `it`    | 컨텍스트 객체   | 부수 효과 (로깅 등)   |

```kotlin
// let - null 체크와 변환
val upperName = term?.name?.let { it.uppercase() }

// apply - 객체 초기화
val term = Term().apply {
    name = "API"
    definition = "Application Programming Interface"
}

// also - 부수 효과 (로깅)
return termRepository.save(term).also {
    logger.info("Term saved: ${it.name}")
}

// run - 객체 설정 후 결과 반환
val message = StringBuilder().run {
    append("Terms: ")
    terms.forEach { append("${it.name}, ") }
    toString()
}
```

### 4.3 컬렉션 연산

```kotlin
// Good - 함수형 연산 체이닝
val topTerms = occurrences
    .filter { !it.term.ignored }
    .groupBy { it.term }
    .mapValues { (_, occurrences) -> occurrences.size }
    .entries
    .sortedByDescending { it.value }
    .take(10)
    .map { TermFrequency(it.key, it.value.toLong()) }

// 단, 복잡한 경우 중간 변수로 가독성 향상
val nonIgnoredOccurrences = occurrences.filter { !it.term.ignored }
val groupedByTerm = nonIgnoredOccurrences.groupBy { it.term }
val countsByTerm = groupedByTerm.mapValues { it.value.size }
// ...
```

### 4.4 Default Arguments & Named Arguments

```kotlin
// Good - 기본값과 named arguments 활용
data class FrequencyQuery(
    val versionId: Long,
    val channelIds: List<Long> = emptyList(),
    val period: DateRange = DateRange.lastWeek(),
    val limit: Int = 100,
    val excludeRegistered: Boolean = false,
    val excludeIgnored: Boolean = true
)

// 호출 시 필요한 파라미터만 명시적으로 지정
val query = FrequencyQuery(
    versionId = currentVersionId,
    limit = 20,
    excludeRegistered = true
)
```

---

## 5. Null Safety

### 5.1 Nullable 타입 최소화

```kotlin
// Bad - 불필요한 nullable
class Term(
    val name: String?,  // 항상 필수인데 nullable
    val definition: String?
)

// Good - 필수 필드는 non-null
class Term(
    val name: String,  // 필수
    val definition: String?  // 선택적
)
```

### 5.2 Early Return 패턴

```kotlin
// Bad - 깊은 중첩
fun processMessage(message: SlackMessage?) {
    if (message != null) {
        if (message.text.isNotBlank()) {
            if (isMonitoringChannel(message.channelId)) {
                // 실제 로직
            }
        }
    }
}

// Good - Early return
fun processMessage(message: SlackMessage?) {
    message ?: return
    if (message.text.isBlank()) return
    if (!isMonitoringChannel(message.channelId)) return

    // 실제 로직
}
```

### 5.3 Elvis 연산자 활용

```kotlin
// Good - 기본값 제공
val pageSize = request.pageSize ?: DEFAULT_PAGE_SIZE

// Good - 예외 던지기
val term = termRepository.findById(termId)
    ?: throw TermNotFoundException(termId)
```

### 5.4 안전한 타입 캐스팅

```kotlin
// Bad - 강제 캐스팅
val term = entity as Term

// Good - 안전한 캐스팅
val term = entity as? Term
    ?: throw IllegalStateException("Expected Term but got ${entity::class}")
```

---

## 6. 에러 처리

### 6.1 도메인 예외 정의

```kotlin
// 계층적 예외 구조
sealed class TermbaseException(
    message: String,
    cause: Throwable? = null
) : RuntimeException(message, cause)

class TermNotFoundException(
    val termId: Long
) : TermbaseException("Term not found: $termId")

class DuplicateTermException(
    val termName: String
) : TermbaseException("Term already exists: $termName")

class InvalidPeriodException(
    val startDate: LocalDate,
    val endDate: LocalDate
) : TermbaseException("Invalid period: $startDate ~ $endDate")
```

### 6.2 예외는 예외적 상황에서만

```kotlin
// Bad - 흐름 제어에 예외 사용
fun findOrCreate(name: String): Term {
    return try {
        termRepository.findByName(name)!!
    } catch (e: NullPointerException) {
        termRepository.save(Term(name = name))
    }
}

// Good - 명시적 조건 검사
fun findOrCreate(name: String): Term {
    return termRepository.findByName(name)
        ?: termRepository.save(Term(name = name))
}
```

### 6.3 Result 타입 활용 (실패 가능한 연산)

```kotlin
// 실패가 예상되는 연산에 Result 사용
fun extractTerms(text: String): Result<List<ExtractedTerm>> = runCatching {
    val analyzed = komoran.analyze(text)
    analyzed.nouns.map { ExtractedTerm(it) }
}

// 호출 측에서 처리
extractTerms(message.text)
    .onSuccess { terms -> saveOccurrences(terms) }
    .onFailure { error -> logger.error("Extraction failed", error) }
```

### 6.4 전역 예외 처리

```kotlin
@RestControllerAdvice
class GlobalExceptionHandler {

    @ExceptionHandler(TermNotFoundException::class)
    fun handleTermNotFound(ex: TermNotFoundException): ResponseEntity<ErrorResponse> {
        return ResponseEntity
            .status(HttpStatus.NOT_FOUND)
            .body(ErrorResponse(ex.message ?: "Term not found"))
    }

    @ExceptionHandler(TermbaseException::class)
    fun handleDomainException(ex: TermbaseException): ResponseEntity<ErrorResponse> {
        return ResponseEntity
            .status(HttpStatus.BAD_REQUEST)
            .body(ErrorResponse(ex.message ?: "Bad request"))
    }
}
```

---

## 7. 레이어별 책임

### 7.1 Presentation Layer

- HTTP 요청/응답 처리만 담당
- 비즈니스 로직 포함 금지
- DTO ↔ Domain 변환

```kotlin
@RestController
@RequestMapping("/api/terms")
class TermApiController(
    private val termService: TermService
) {
    @PostMapping
    fun create(@RequestBody @Valid request: CreateTermRequest): ResponseEntity<TermResponse> {
        val term = termService.create(request.toCommand())
        return ResponseEntity
            .created(URI.create("/api/terms/${term.id}"))
            .body(TermResponse.from(term))
    }
}

// Request DTO
data class CreateTermRequest(
    @field:NotBlank val name: String,
    val definition: String?
) {
    fun toCommand() = CreateTermCommand(name, definition)
}

// Response DTO
data class TermResponse(
    val id: Long,
    val name: String,
    val definition: String?,
    val isRegistered: Boolean
) {
    companion object {
        fun from(term: Term) = TermResponse(
            id = term.id!!,
            name = term.name,
            definition = term.definition,
            isRegistered = term.isRegistered()
        )
    }
}
```

### 7.2 Application Layer

- 유스케이스 조율 (Orchestration)
- 트랜잭션 경계 설정
- 도메인 서비스 호출

```kotlin
@Service
@Transactional
class TermService(
    private val termRepository: TermRepository
) {
    fun create(command: CreateTermCommand): Term {
        termRepository.findByName(command.name)?.let {
            throw DuplicateTermException(command.name)
        }

        val term = Term.create(command.name, command.definition)
        return termRepository.save(term)
    }

    @Transactional(readOnly = true)
    fun findAll(): List<Term> = termRepository.findAll()
}
```

### 7.3 Domain Layer

- 순수한 비즈니스 로직
- 프레임워크 의존성 없음 (가능한 한)
- 불변성 유지

```kotlin
// Entity
class Term private constructor(
    val id: Long?,
    val name: String,
    val definition: String?,
    val canonicalTermId: Long?,
    val ignored: Boolean,
    val createdAt: Instant
) {
    fun isRegistered(): Boolean = definition != null && !ignored

    fun isSynonym(): Boolean = canonicalTermId != null

    fun register(definition: String): Term {
        require(definition.isNotBlank()) { "Definition cannot be blank" }
        return copy(definition = definition)
    }

    companion object {
        fun create(name: String, definition: String? = null): Term {
            require(name.isNotBlank()) { "Name cannot be blank" }
            return Term(
                id = null,
                name = name,
                definition = definition,
                canonicalTermId = null,
                ignored = false,
                createdAt = Instant.now()
            )
        }
    }
}

// Repository Interface (Domain Layer에 정의)
interface TermRepository {
    fun save(term: Term): Term
    fun findById(id: Long): Term?
    fun findByName(name: String): Term?
    fun findAll(): List<Term>
    fun delete(id: Long)
}
```

### 7.4 Infrastructure Layer

- 기술적 구현 세부사항
- Repository 구현체
- 외부 API 클라이언트

```kotlin
@Repository
class JpaTermRepository(
    private val jpaRepository: TermJpaRepository
) : TermRepository {

    override fun save(term: Term): Term {
        val entity = TermEntity.from(term)
        return jpaRepository.save(entity).toDomain()
    }

    override fun findById(id: Long): Term? {
        return jpaRepository.findById(id).orElse(null)?.toDomain()
    }
}
```

### 7.5 Spring Data JPA Repository 설계

`JpaRepository`나 `CrudRepository` 대신 최소한의 `Repository<T, ID>` 인터페이스를 사용합니다. 실제 필요한 메서드만 정의합니다.

```kotlin
// Good: 필요한 메서드만 정의
interface TermRepository : Repository<Term, Long> {
    fun save(term: Term): Term
    fun findById(id: Long): Term?
    fun findByName(name: String): Term?
    fun existsByName(name: String): Boolean
}

// Avoid: 불필요한 메서드까지 노출
interface TermRepository : JpaRepository<Term, Long>
```

**이유:**

- 실제 사용하는 메서드만 노출하여 인터페이스 명확성 향상
- 불필요한 `deleteAll()`, `flush()` 등의 위험한 메서드 노출 방지
- 테스트 시 mock 범위 최소화

---

## 8. 의존성 주입

### 8.1 생성자 주입 사용

```kotlin
// Good - 생성자 주입 (Kotlin에서는 primary constructor 활용)
@Service
class TermService(
    private val termRepository: TermRepository,
    private val eventPublisher: ApplicationEventPublisher
)

// Bad - 필드 주입
@Service
class TermService {
    @Autowired
    private lateinit var termRepository: TermRepository
}
```

### 8.2 인터페이스에 의존

```kotlin
// Good - 인터페이스 의존
class ExtractionService(
    private val termExtractor: TermExtractor,  // 인터페이스
    private val dictionaryProvider: DictionaryProvider  // 인터페이스
)

// 구현체는 설정에서 주입
@Configuration
class ExtractionConfig {
    @Bean
    fun termExtractor(dictionaryProvider: DictionaryProvider): TermExtractor {
        return KomoranTermExtractor(Komoran(DEFAULT_MODEL.FULL), dictionaryProvider)
    }
}
```

---

## 9. 테스트 용이성

### 9.1 테스트 가능한 설계

```kotlin
// Good - 의존성 주입으로 테스트 용이
class ExtractionService(
    private val termExtractor: TermExtractor,
    private val clock: Clock = Clock.systemDefaultZone()  // 테스트 시 고정 시간 주입 가능
) {
    fun extractWithTimestamp(text: String): List<TimestampedTerm> {
        val now = Instant.now(clock)
        return termExtractor.extract(text).map {
            TimestampedTerm(it, now)
        }
    }
}

// 테스트
class ExtractionServiceTest : DescribeSpec() {
    init {
        describe("ExtractionService") {
            val fixedClock = Clock.fixed(Instant.parse("2024-01-01T00:00:00Z"), ZoneOffset.UTC)
            val mockExtractor = mockk<TermExtractor>()
            val service = ExtractionService(mockExtractor, fixedClock)

            it("should add timestamp to extracted terms") {
                // ...
            }
        }
    }
}
```

### 9.2 Pure Functions 선호

```kotlin
// Good - 순수 함수 (테스트 쉬움)
fun calculateFrequency(occurrences: List<TermOccurrence>): Map<Long, Long> {
    return occurrences.groupingBy { it.termId }.eachCount().mapValues { it.value.toLong() }
}

// 테스트
@Test
fun `should calculate frequency correctly`() {
    val occurrences = listOf(
        TermOccurrence(termId = 1),
        TermOccurrence(termId = 1),
        TermOccurrence(termId = 2)
    )

    calculateFrequency(occurrences) shouldBe mapOf(1L to 2L, 2L to 1L)
}
```

---

## 10. 코드 포맷팅

### 10.1 ktlint 규칙 준수

프로젝트에서 ktlint를 사용하여 일관된 포맷팅을 유지합니다.

```bash
# 포맷 검사
./gradlew ktlintCheck

# 자동 포맷팅
./gradlew ktlintFormat
```

### 10.2 Import 정리

- 와일드카드 import 금지
- 사용하지 않는 import 제거
- 알파벳 순 정렬
- fully qualified name 대신 항상 `import` 문 사용

```kotlin
// Good: import 사용
import java.time.Instant

val now = Instant.now()

// Avoid: fully qualified name 사용
val now = java.time.Instant.now()
```

**이유:**

- 코드 가독성 향상
- 일관된 코드 스타일 유지
- 클래스 이름 충돌 시에만 fully qualified name 사용

### 10.3 줄 바꿈 규칙

```kotlin
// 긴 함수 시그니처 - 파라미터별 줄 바꿈
fun findTermOccurrences(
    termId: Long,
    channelIds: List<Long>,
    period: DateRange,
    pageable: Pageable
): Page<TermOccurrence>

// 메서드 체이닝 - 각 호출별 줄 바꿈
val result = occurrences
    .filter { it.isValid() }
    .map { it.toDto() }
    .sortedBy { it.name }
```

---

## 요약 체크리스트

코드 작성 또는 리뷰 시 다음을 확인하세요:

- [ ] 함수/클래스 이름이 의도를 명확히 표현하는가?
- [ ] 함수가 하나의 작업만 수행하는가?
- [ ] 파라미터가 3개 이하인가? (아니면 객체로 그룹화)
- [ ] 불필요한 nullable 타입이 없는가?
- [ ] 예외가 적절히 처리되는가?
- [ ] 레이어 책임이 명확히 분리되어 있는가?
- [ ] 테스트하기 쉬운 구조인가?
