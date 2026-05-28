# Severity Definitions

> 분석 결과 심각도 정의

## 심각도 레벨

### 🔴 Critical

**정의**: 즉시 수정 필요. 보안 위험 또는 시스템 장애 가능성.

**조치**: PR 차단. 배포 금지.

| Focus | Critical 조건 |
|-------|--------------|
| Quality | 순환 복잡도 > 50, 컴파일 에러 |
| Security | 하드코딩 비밀, SQL Injection, 인증 우회 |
| Performance | `.block()` in Reactive, 무한 루프 가능성 |
| Architecture | 순환 의존성 (핵심 모듈) |

**예시**:
```kotlin
// Critical - Security: 하드코딩된 비밀
val apiKey = "sk-live-1234567890abcdef"

// Critical - Performance: 블로킹 호출
fun getUser(id: Long): User = repository.findById(id).block()!!
```

### 🟠 High

**정의**: 빠른 수정 권장. 잠재적 문제 또는 품질 저하.

**조치**: 현재 스프린트 내 수정. PR 승인 조건부.

| Focus | High 조건 |
|-------|----------|
| Quality | 순환 복잡도 21-50, 메서드 50줄+ |
| Security | 불완전한 입력 검증, 과도한 권한 |
| Performance | N+1 쿼리, 캐시 미사용 (핫패스) |
| Architecture | 레이어 의존성 위반 |

**예시**:
```kotlin
// High - Performance: N+1 쿼리
posts.forEach { post ->
    val comments = commentRepo.findByPostId(post.id)
}

// High - Architecture: 레이어 위반
// In Repository:
import com.example.service.UserService  // Repository → Service 금지
```

### 🟡 Medium

**정의**: 계획된 수정. 유지보수성/가독성 영향.

**조치**: 백로그 등록. 다음 스프린트 고려.

| Focus | Medium 조건 |
|-------|------------|
| Quality | 순환 복잡도 11-20, 중복 코드 |
| Security | 디버그 정보 노출, @Suppress 사용 |
| Performance | 불필요한 객체 생성, 최적화 가능 |
| Architecture | 과도한 의존성, 패키지 구조 문제 |

**예시**:
```kotlin
// Medium - Quality: 긴 파라미터 목록
fun createUser(
    name: String,
    email: String,
    phone: String,
    address: String,
    city: String,
    country: String,  // 6개 파라미터 → Parameter Object 권장
    zipCode: String
)

// Medium - Security: @Suppress
@Suppress("UNCHECKED_CAST")  // 타입 안전성 저하
```

### 🟢 Low / Info

**정의**: 개선 기회. 베스트 프랙티스 제안.

**조치**: 선택적 수정. 리팩토링 시 고려.

| Focus | Low 조건 |
|-------|---------|
| Quality | 네이밍 개선, 문서화 부족 |
| Security | 보안 모범 사례 제안 |
| Performance | 마이너 최적화 기회 |
| Architecture | 패턴 일관성, 구조 개선 |

**예시**:
```kotlin
// Low - Quality: 네이밍 개선
fun proc(d: Data)  // → fun processData(data: Data)

// Low - Architecture: 패턴 일관성
// 일부는 Repository, 일부는 Dao 사용
```

## Focus별 심각도 매트릭스

### Quality Focus

| 항목 | Critical | High | Medium | Low |
|------|----------|------|--------|-----|
| 순환 복잡도 | >50 | 21-50 | 11-20 | - |
| 메서드 라인 | >100 | 51-100 | 31-50 | - |
| 클래스 라인 | >500 | 301-500 | 201-300 | - |
| 파라미터 개수 | - | >7 | 5-7 | - |
| 중복 코드 | >10블록 | 5-10 | 2-4 | - |
| 컴파일 에러 | ✓ | - | - | - |

### Security Focus

| 항목 | Critical | High | Medium | Low |
|------|----------|------|--------|-----|
| 하드코딩 비밀 | ✓ | - | - | - |
| SQL Injection | ✓ | - | - | - |
| 인증 우회 | ✓ | - | - | - |
| 불완전 검증 | - | ✓ | - | - |
| 과도한 권한 | - | ✓ | - | - |
| 디버그 노출 | - | - | ✓ | - |
| @Suppress | - | - | ✓ | - |
| 모범 사례 | - | - | - | ✓ |

### Performance Focus

| 항목 | Critical | High | Medium | Low |
|------|----------|------|--------|-----|
| .block() | ✓ | - | - | - |
| Thread.sleep | ✓ | - | - | - |
| 무한 루프 | ✓ | - | - | - |
| N+1 쿼리 | - | ✓ | - | - |
| 캐시 미사용 (핫) | - | ✓ | - | - |
| 불필요 객체 | - | - | ✓ | - |
| 문자열 연결 | - | - | ✓ | - |
| 마이너 최적화 | - | - | - | ✓ |

### Architecture Focus

| 항목 | Critical | High | Medium | Low |
|------|----------|------|--------|-----|
| 순환 의존 (핵심) | ✓ | - | - | - |
| 순환 의존 (주변) | - | ✓ | - | - |
| 레이어 위반 | - | ✓ | - | - |
| SOLID 위반 | - | ✓ | ✓ | - |
| 과도한 의존 | - | - | ✓ | - |
| 패턴 일관성 | - | - | - | ✓ |

## 자동 조치 연동

| 심각도 | 자동 조치 |
|--------|----------|
| Critical | PR 차단, 슬랙 알림 |
| High | PR 경고, 리뷰어 추가 태그 |
| Medium | 백로그 이슈 자동 생성 |
| Low | 리포트에만 포함 |
