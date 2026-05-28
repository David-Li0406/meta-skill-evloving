---
name: run-tests
description: |
  테스트 실행 및 품질 검증. Use when:
  (1) 테스트 실행 요청, (2) 변경 후 검증 필요, (3) 커버리지 확인.
tools: [Bash, Read, Glob, Grep]
model: inherit
---

> **시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: run-tests 호출 - {테스트 유형}` 시스템 메시지를 첫 줄에 출력하세요.

# run-tests Skill

> Spring Boot + Kotlin 테스트 실행 및 분석 Skill

## Purpose

테스트를 실행하고 결과를 분석하여 품질을 검증합니다.

### 테스트 유형

| 유형 | 설명 | Gradle 명령 |
|------|------|-------------|
| **unit** | 단위 테스트 | `./gradlew test` |
| **integration** | 통합 테스트 | `./gradlew integrationTest` |
| **all** | 전체 테스트 | `./gradlew check` |

## Workflow

1. **테스트 탐색**: 테스트 파일 탐색
2. **테스트 실행**: Gradle 테스트 실행
3. **결과 분석**: HTML 리포트 및 커버리지 분석
4. **실패 분석**: 실패 테스트 원인 분석

## Output Format

```markdown
[SEMO] Skill: run-tests 완료

## 테스트 결과: ✅ 성공

| 항목 | 결과 |
|------|------|
| 총 테스트 | 127 |
| 성공 | 127 |
| 실패 | 0 |

### 커버리지
- Line: 78.3%
- Branch: 65.2%
```

## References

- [Test Patterns](references/test-patterns.md)
- [Coverage Guide](references/coverage-guide.md)
- [Troubleshooting](references/troubleshooting.md)
