# Analysis Patterns

> Focus별 코드 분석 패턴 상세

## Quality Analysis Patterns

### 1. 복잡도 분석

#### 순환 복잡도 (Cyclomatic Complexity)

```bash
# 조건문 개수로 추정
grep -c "if\|when\|for\|while\|catch\|&&\|||" file.kt
```

| 복잡도 | 등급 | 조치 |
|--------|------|------|
| 1-10 | 🟢 Good | 유지 |
| 11-20 | 🟡 Warning | 리팩토링 권장 |
| 21-50 | 🟠 High | 리팩토링 필요 |
| 50+ | 🔴 Critical | 즉시 분할 |

#### 인지 복잡도 (Cognitive Complexity)

중첩 깊이와 제어 흐름 고려:

```kotlin
// 복잡도 +1: 기본 분기
if (condition) { ... }

// 복잡도 +2: 중첩 분기
if (outer) {
    if (inner) { ... }  // +1 (중첩 보너스)
}

// 복잡도 +1: 논리 연산자
if (a && b || c) { ... }
```

### 2. 중복 코드 탐지

#### 유사 코드 블록

```bash
# 동일한 import 그룹
grep -h "^import" src/**/*.kt | sort | uniq -c | sort -rn | head -20

# 유사 메서드 시그니처
grep -rn "fun .*(.*):" src/ --include="*.kt" | cut -d: -f3 | sort | uniq -d
```

#### 복사-붙여넣기 패턴

```text
탐지 대상:
├─ 3줄 이상 동일 코드
├─ 변수명만 다른 동일 로직
└─ 유사한 예외 처리 블록
```

### 3. 코드 스멜

| 스멜 | 탐지 패턴 | 심각도 |
|------|----------|--------|
| Long Method | 30줄 이상 | Medium |
| Large Class | 300줄 이상 | Medium |
| Long Parameter List | 5개 이상 파라미터 | Medium |
| Feature Envy | 다른 클래스 메서드 과다 호출 | Low |
| Data Clumps | 반복되는 파라미터 그룹 | Low |
| Primitive Obsession | 원시 타입 과다 사용 | Low |

## Security Analysis Patterns

### 1. OWASP Top 10 검사

#### A01: Broken Access Control

```bash
# 인가 없는 엔드포인트
grep -rn "@GetMapping\|@PostMapping" src/ --include="*.kt" | grep -v "@PreAuthorize\|@Secured"

# 직접 객체 참조
grep -rn "findById.*request\." src/ --include="*.kt"
```

#### A02: Cryptographic Failures

```bash
# 약한 암호화
grep -rn "MD5\|SHA1\|DES\|RC4" src/ --include="*.kt"

# 하드코딩된 키
grep -rn "private.*key\|secret.*=.*\"" src/ --include="*.kt"
```

#### A03: Injection

```bash
# SQL Injection
grep -rn "\$.*select\|\".*+.*where" src/ --include="*.kt"

# Command Injection
grep -rn "Runtime\.getRuntime\|ProcessBuilder" src/ --include="*.kt"

# NoSQL Injection
grep -rn "BasicDBObject\|Document.*append" src/ --include="*.kt"
```

### 2. 인증/인가 검사

```kotlin
// 취약 패턴
fun deleteUser(userId: Long) {
    userRepository.deleteById(userId)  // 권한 검사 없음!
}

// 안전 패턴
@PreAuthorize("hasRole('ADMIN') or #userId == authentication.principal.id")
fun deleteUser(userId: Long) { ... }
```

### 3. 민감 데이터 노출

```bash
# 로깅에 민감 정보
grep -rn "log.*password\|log.*token\|log.*secret" src/ --include="*.kt"

# Response에 민감 정보
grep -rn "password.*response\|token.*return" src/ --include="*.kt"
```

## Performance Analysis Patterns

### 1. N+1 쿼리 탐지

```kotlin
// N+1 패턴 (위험)
posts.forEach { post ->
    val comments = commentRepository.findByPostId(post.id)  // N번 쿼리!
}

// 개선: JOIN FETCH 또는 BatchSize
@Query("SELECT p FROM Post p JOIN FETCH p.comments")
fun findAllWithComments(): List<Post>
```

#### 탐지 명령

```bash
# flatMap 내 repository 호출
grep -rn "flatMap\|forEach" src/ --include="*.kt" | xargs -I {} grep -l "repository\." {}

# 루프 내 쿼리
awk '/for.*\{|forEach/{found=1} found && /repository\./{print FILENAME":"NR} /\}/{found=0}' src/**/*.kt
```

### 2. 블로킹 호출 탐지

| 패턴 | 심각도 | 대안 |
|------|--------|------|
| `.block()` | Critical | `awaitSingle()`, Mono chain |
| `.blockFirst()` | Critical | `awaitFirst()` |
| `Thread.sleep()` | Critical | `delay()` |
| `.get()` (Future) | High | `await()` |
| `@Synchronized` | Medium | `Mutex` |

```bash
# 블로킹 호출 탐지
grep -rn "\.block()\|\.blockFirst()\|\.blockLast()\|Thread\.sleep\|\.get()" src/ --include="*.kt"
```

### 3. 메모리 효율성

```bash
# 큰 컬렉션 생성
grep -rn "mutableListOf\|ArrayList\|HashMap" src/ --include="*.kt"

# 문자열 연결 (루프 내)
grep -rn "for.*\+=" src/ --include="*.kt"

# 불필요한 객체 생성
grep -rn "\.map.*\.map.*\.map" src/ --include="*.kt"
```

## Architecture Analysis Patterns

### 1. 레이어 의존성 검사

```text
허용된 의존성:
Controller → Service → Repository
Controller → DTO
Service → Domain, DTO
Repository → Domain

금지된 의존성:
Repository → Service
Service → Controller
Domain → Service/Repository
```

```bash
# 레이어 위반 탐지
# Service가 Controller 참조
grep -rn "import.*controller" src/main/**/service/**/*.kt

# Repository가 Service 참조
grep -rn "import.*service" src/main/**/repository/**/*.kt

# Domain이 Infrastructure 참조
grep -rn "import.*repository\|import.*service" src/main/**/domain/**/*.kt
```

### 2. 순환 의존성

```bash
# 패키지별 의존성 추출
for pkg in $(find src/main -type d -name "*.kt" | xargs dirname | sort -u); do
    echo "=== $pkg ==="
    grep -h "^import" $pkg/*.kt 2>/dev/null | sort -u
done
```

### 3. SOLID 원칙 검사

| 원칙 | 검사 | 패턴 |
|------|------|------|
| SRP | 클래스 책임 | 한 클래스에 여러 도메인 import |
| OCP | 확장성 | when/if 분기가 많은 클래스 |
| LSP | 치환 가능성 | override + throw UnsupportedOperation |
| ISP | 인터페이스 분리 | 구현 안 된 인터페이스 메서드 |
| DIP | 의존성 역전 | 구체 클래스 직접 의존 |

```bash
# DIP 위반 (구체 클래스 주입)
grep -rn "@Autowired.*Impl\|@Inject.*Impl" src/ --include="*.kt"

# LSP 위반
grep -rn "throw UnsupportedOperationException\|TODO()" src/ --include="*.kt"
```
