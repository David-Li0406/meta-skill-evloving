# KDoc Guidelines

## Controller 문서화 (필수)

```kotlin
/**
 * 저장소 상세 정보 조회
 *
 * 네임스페이스와 저장소명으로 상세 정보를 반환합니다.
 * 비공개 저장소는 소유자만 조회 가능합니다.
 *
 * @param namespace 네임스페이스 (예: "alice")
 * @param name 저장소명 (예: "myapp")
 * @param user 요청 사용자 (W4에서 @AuthenticationPrincipal로 대체 예정)
 * @return 저장소 상세 정보
 * @throws BusinessException NOT_FOUND - 저장소 미존재
 * @throws BusinessException FORBIDDEN - 접근 권한 없음
 */
@GetMapping("/{namespace}/{name}")
fun getRepository(...): ResponseEntity<ApiResponse<RepositoryDetailResponse>>
```

### Controller KDoc 체크리스트
- [ ] 한 줄 요약 (무엇을 하는가)
- [ ] 상세 설명 (필요시)
- [ ] @param 모든 파라미터
- [ ] @return 반환값 설명
- [ ] @throws 발생 가능한 예외

## Service Interface 문서화 (권장)

```kotlin
/**
 * 저장소 상세 정보 조회
 *
 * 접근 권한 검증 후 저장소 정보를 반환합니다.
 * - 공개 저장소: 모든 사용자 접근 가능
 * - 비공개 저장소: 소유자만 접근 가능
 *
 * @param repoName 전체 저장소 경로 (예: "alice/myapp")
 * @param requestUser 요청 사용자
 * @return 저장소 상세 정보
 */
fun getRepositoryDetail(repoName: String, requestUser: String): RepositoryDetailResponse
```

### Service Interface KDoc 체크리스트
- [ ] 비즈니스 의미 설명
- [ ] 접근 제어 규칙 (있다면)
- [ ] @param, @return

## Service Impl 문서화 (인라인 주석만)

```kotlin
override fun getRepositoryDetail(repoName: String, requestUser: String): RepositoryDetailResponse {
    val repo = repositoryRepo.findByName(repoName)
        ?: throw BusinessException(ErrorCode.NOT_FOUND, "Repository not found: $repoName")

    // 접근 권한 검증: 공개 또는 소유자인 경우만 허용
    if (!isAccessible(repo, requestUser)) {
        throw BusinessException(ErrorCode.FORBIDDEN, "Access denied")
    }

    // 태그 수 계산 (삭제된 태그 제외)
    val tagCount = tagRepo.countByRepoName(repoName)

    return RepositoryDetailResponse(...)
}
```

### Impl 인라인 주석 체크리스트
- [ ] Interface에 KDoc이 있으면 Impl에는 KDoc 금지 (DRY)
- [ ] 복잡한 로직에만 인라인 주석
- [ ] "왜" 이렇게 구현했는지 설명

## DTO 문서화

### 단순 DTO (생략 가능)
```kotlin
data class RepositoryDetailResponse(
    val name: String,
    val owner: String,
    val visibility: String,
    val tagCount: Long
)
```

### 복잡 DTO (권장)
```kotlin
/**
 * 저장소 상세 응답
 *
 * @property name 전체 저장소 경로 (예: "alice/myapp")
 * @property visibility "public" 또는 "private"
 * @property tagCount 활성 태그 수 (삭제된 태그 제외)
 */
data class RepositoryDetailResponse(
    val name: String,
    val owner: String,
    val visibility: String,
    val tagCount: Long
)
```

## Private 함수 문서화

```kotlin
private fun extractOwnerFromRepoName(repoName: String): String {
    // "alice/myapp" -> "alice", 네임스페이스 없으면 전체를 owner로 사용
    val parts = repoName.split("/")
    return if (parts.size >= 2) parts[0] else repoName
}
```

## Anti-Patterns

### 1. Interface + Impl 중복 (DRY 위반)
```kotlin
// BAD: 중복 KDoc
interface UserService {
    /** 사용자 조회 */
    fun getUser(id: String): User
}

class UserServiceImpl : UserService {
    /** 사용자 조회 */  // <- 중복! 삭제해야 함
    override fun getUser(id: String): User { ... }
}
```

### 2. 코드 반복 주석 (무의미)
```kotlin
// BAD: 코드가 이미 설명하는 내용
// 사용자 이름을 반환한다
fun getUserName(): String

// GOOD: 추가 맥락 제공
// 캐시된 값 반환, DB 조회 없음
fun getUserName(): String
```

### 3. 과도한 문서화
```kotlin
// BAD: 너무 장황함
/**
 * 이 함수는 사용자 ID를 받아서 데이터베이스에서
 * 해당 사용자를 조회하고 결과를 반환합니다.
 * 만약 사용자가 없으면 null을 반환합니다.
 */
fun findById(id: String): User?

// GOOD: 간결함
/** ID로 사용자 조회 (없으면 null) */
fun findById(id: String): User?
```
