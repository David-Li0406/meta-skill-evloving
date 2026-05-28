---
name: red-green-refactor
description: TDD Red-Green-Refactor 사이클 가이드. 테스트 주도 개발 시 실패하는 테스트 작성(Red), 최소한의 코드로 통과(Green), 리팩토링(Refactor) 순서를 따를 때 사용. Kotest DescribeSpec 기반 Kotlin/JVM 프로젝트에서 TDD 실천 시 활용.
---

# TDD Red-Green-Refactor Cycle

## Red Phase: Write Failing Test

1. Express intended behavior as test first
2. **Test only one behavior** at a time
3. **Must verify failure** by running test (compilation errors count as failures)

```kotlin
// Kotest DescribeSpec example
class CalculatorTest : DescribeSpec({
    describe("Calculator") {
        it("두 숫자를 더한다") {
            val calculator = Calculator()
            calculator.add(2, 3) shouldBe 5
        }
    }
})
```

Verify failure message matches intent. Unexpected failure reasons indicate test issues.

## Green Phase: Make Test Pass

1. **Write minimal code** to pass the test
2. Hardcoding, duplication, messy code allowed
3. Goal is only green bar

```kotlin
class Calculator {
    fun add(a: Int, b: Int): Int = 5  // Hardcoding OK
}
```

"Working code" first, "clean code" next.

## Refactor Phase: Improve Code

1. **Keep tests passing** while improving
2. Remove duplication, improve naming, apply patterns
3. **Must re-run tests** after refactoring
4. No new features - structural improvements only

```kotlin
class Calculator {
    fun add(a: Int, b: Int): Int = a + b  // Generalize
}
```

## Cycle Rules

- No production code without test
- No production code changes without failing test
- Commit after passing tests (keep commits small)
- No new features during refactoring
- Minimize test changes during refactoring

## Checklist

### Red
- [ ] Test verifies single behavior?
- [ ] Verified failure by running test?
- [ ] Failure message as intended?

### Green
- [ ] Passed with simplest approach?
- [ ] Test is green?

### Refactor
- [ ] Tests still green?
- [ ] Duplication removed?
- [ ] Names reveal intent?
- [ ] No new features added?
