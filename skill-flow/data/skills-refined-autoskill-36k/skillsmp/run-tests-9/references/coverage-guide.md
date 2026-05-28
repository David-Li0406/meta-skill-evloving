# Coverage Guide

> JaCoCo 커버리지 설정 및 분석 가이드

## JaCoCo 설정

### build.gradle.kts

```kotlin
plugins {
    jacoco
}

jacoco {
    toolVersion = "0.8.11"
}

tasks.test {
    finalizedBy(tasks.jacocoTestReport)
}

tasks.jacocoTestReport {
    dependsOn(tasks.test)
    reports {
        xml.required.set(true)
        html.required.set(true)
        csv.required.set(false)
    }

    classDirectories.setFrom(
        files(classDirectories.files.map {
            fileTree(it) {
                exclude(
                    "**/config/**",
                    "**/dto/**",
                    "**/entity/**",
                    "**/*Application*"
                )
            }
        })
    )
}

tasks.jacocoTestCoverageVerification {
    violationRules {
        rule {
            limit {
                minimum = BigDecimal("0.70")
            }
        }

        rule {
            element = "CLASS"
            includes = listOf("com.example.service.*")

            limit {
                counter = "LINE"
                minimum = BigDecimal("0.80")
            }

            limit {
                counter = "BRANCH"
                minimum = BigDecimal("0.60")
            }
        }
    }
}
```

## 커버리지 실행

### 기본 커버리지 생성

```bash
# 테스트 실행 + 커버리지 리포트
./gradlew test jacocoTestReport

# 리포트 위치
open build/reports/jacoco/test/html/index.html
```

### 커버리지 검증

```bash
# 최소 기준 충족 검증
./gradlew jacocoTestCoverageVerification

# 실패 시 빌드 실패
```

## 커버리지 메트릭

### 메트릭 종류

| 메트릭 | 설명 | 목표 |
|--------|------|------|
| **LINE** | 실행된 라인 수 | ≥70% |
| **BRANCH** | 분기 커버리지 | ≥60% |
| **METHOD** | 실행된 메서드 수 | ≥70% |
| **CLASS** | 테스트된 클래스 수 | ≥80% |
| **INSTRUCTION** | 바이트코드 명령어 | 참조용 |

### 권장 목표

```text
전체 프로젝트
├─ Line Coverage: ≥70%
├─ Branch Coverage: ≥60%
└─ Method Coverage: ≥70%

핵심 서비스 (service/*)
├─ Line Coverage: ≥80%
├─ Branch Coverage: ≥70%
└─ Method Coverage: ≥80%

컨트롤러 (controller/*)
├─ Line Coverage: ≥75%
└─ Branch Coverage: ≥60%

리포지토리 (repository/*)
└─ Line Coverage: ≥60% (R2DBC 특성 고려)
```

## 커버리지 분석

### 리포트 해석

```text
JaCoCo HTML Report
├─ index.html (전체 요약)
├─ com.example.service/
│   ├─ UserService.html (클래스별 상세)
│   │   ├─ 녹색: 완전히 커버됨
│   │   ├─ 노란색: 부분 커버 (일부 브랜치)
│   │   └─ 빨간색: 커버되지 않음
│   └─ ...
└─ jacoco-sessions.html (세션 정보)
```

### 낮은 커버리지 원인 분석

```bash
# 커버되지 않은 메서드 찾기
grep -rn "@Test" src/test --include="*.kt" | wc -l
# vs
grep -rn "fun " src/main --include="*.kt" | wc -l

# 특정 클래스 커버리지 확인
cat build/reports/jacoco/test/html/com.example.service/UserService.html
```

## 커버리지 제외 패턴

### 제외 권장 대상

```kotlin
// build.gradle.kts
classDirectories.setFrom(
    files(classDirectories.files.map {
        fileTree(it) {
            exclude(
                // 설정 클래스
                "**/config/**",

                // DTO/Entity (Kotlin data class)
                "**/dto/**",
                "**/entity/**",
                "**/model/**",

                // 메인 애플리케이션
                "**/*Application*",

                // 자동 생성 코드
                "**/generated/**",

                // 예외 클래스
                "**/exception/**"
            )
        }
    })
)
```

### 어노테이션 기반 제외

```kotlin
// JaCoCo가 자동으로 무시하는 클래스명
class MyClassGenerated  // "Generated" 포함
class MyClass$$  // Kotlin companion 등

// Lombok @Generated (Kotlin에서는 거의 사용 안 함)
@Generated
class MyGeneratedClass
```

## CI/CD 통합

### GitHub Actions

```yaml
- name: Run tests with coverage
  run: ./gradlew test jacocoTestReport

- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v3
  with:
    files: build/reports/jacoco/test/jacocoTestReport.xml
    fail_ci_if_error: true

- name: Coverage gate
  run: ./gradlew jacocoTestCoverageVerification
```

### PR 커버리지 리포트

```yaml
- name: Add coverage comment
  uses: madrapps/jacoco-report@v1.6
  with:
    paths: build/reports/jacoco/test/jacocoTestReport.xml
    token: ${{ secrets.GITHUB_TOKEN }}
    min-coverage-overall: 70
    min-coverage-changed-files: 80
```

## 커버리지 개선 전략

### 1. 핵심 경로 우선

```text
커버리지 우선순위
1. 비즈니스 로직 (Service Layer) - 가장 중요
2. 입력 검증 (Controller/Request Validation)
3. 에러 처리 경로
4. 엣지 케이스
5. 설정/초기화 코드 - 낮은 우선순위
```

### 2. Branch 커버리지 개선

```kotlin
// Before: 단순 테스트
@Test
fun `should process order`() {
    val result = service.process(validOrder)
    assertThat(result).isNotNull()
}

// After: 모든 분기 테스트
@Test
fun `should process valid order`() { ... }

@Test
fun `should reject order with no items`() { ... }

@Test
fun `should reject order with negative total`() { ... }

@Test
fun `should apply discount for premium user`() { ... }
```

### 3. 파라미터화 테스트

```kotlin
@ParameterizedTest
@CsvSource(
    "STANDARD, 100",
    "EXPRESS, 200",
    "SAME_DAY, 300"
)
fun `should calculate correct shipping`(type: String, expected: Int) {
    val result = service.calculateShipping(ShippingType.valueOf(type))
    assertThat(result).isEqualTo(expected)
}
```
