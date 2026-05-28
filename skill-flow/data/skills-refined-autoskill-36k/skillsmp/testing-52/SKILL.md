---
name: testing
description: 새로운 테스트 코드를 작성할 때 사용. Kotest DescribeSpec 스타일과 100% 커버리지 요구사항을 따름.
---

# 테스트 가이드라인

모든 테스트는 **Kotest DescribeSpec** 스타일로 작성합니다.

## 기본 구조

`describe`로 그룹화하고 `it`으로 개별 테스트 케이스를 작성합니다.

```kotlin
@Import(TestcontainersConfiguration::class)
@SpringBootTest
class ExampleTests : DescribeSpec() {
    init {
        extension(SpringExtension())

        describe("FeatureName") {
            it("should do something") {
                // 테스트 코드
            }

            context("when some condition") {
                it("should behave differently") {
                    // 테스트 코드
                }
            }
        }
    }
}
```

## 핵심 포인트

- `DescribeSpec`을 기본 클래스로 사용
- Spring 통합 테스트에는 `SpringExtension()` 등록
- `describe`로 기능/클래스별 관련 테스트 그룹화
- `context`로 조건별 시나리오 구분
- `it`으로 개별 테스트 케이스 작성
- Kotest assertion 사용 (`shouldBe`, `shouldThrow` 등)

## 테스트 명령어

```bash
# 전체 테스트 실행
./gradlew test

# 단일 테스트 클래스 실행
./gradlew test --tests "com.mkroo.termbase.TermbaseApplicationTests"

# 단일 테스트 메서드 실행
./gradlew test --tests "com.mkroo.termbase.TermbaseApplicationTests.contextLoads"

# 테스트 커버리지 확인
./gradlew jacocoTestReport

# 커버리지 최소 임계값(100%) 검증
./gradlew jacocoTestCoverageVerification
```

## 커버리지 요구사항

- 새 코드의 모든 브랜치, 엣지 케이스, 에러 시나리오를 커버하는 테스트 작성
- 100% 커버리지 달성 필수
- `./gradlew jacocoTestCoverageVerification` 통과 필수
