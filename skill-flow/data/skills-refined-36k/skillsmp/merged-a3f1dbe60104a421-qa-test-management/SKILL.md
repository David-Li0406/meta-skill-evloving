---
name: qa-test-management
description: Use this skill when you need to manage QA testing tasks, including requesting tests, running tests, and updating test results.
---

# QA Test Management Skill

## Purpose

This skill facilitates the management of QA testing tasks, allowing users to request tests, run tests, and update test results efficiently.

## Workflow

### 1. Requesting a Test

Use this section to request QA testing for completed tasks.

#### Required Information

| 필수 정보 | 설명 | 예시 |
|----------|------|------|
| 프로젝트 | GitHub 레포지토리 | `semicolon-devteam/half-time` |
| 태스크카드 | GitHub 이슈 번호 | `#123` |

#### Execution Flow

1. **이슈 정보 조회**: Retrieve issue information using the GitHub CLI.
2. **QA 테스트 항목 검증**: Ensure the issue contains QA test items.
3. **Assignee 할당**: Assign the QA responsible person.
4. **Slack 알림 발송**: Send a notification to the relevant Slack channel.

#### Output Format

```markdown
[SEMO] Skill: request-test 완료

✅ QA 테스트 요청 완료

**프로젝트**: semicolon-devteam/{repo}
**이슈**: #{이슈번호} - {이슈제목}
**담당자**: @kokkh (GitHub) / @Goni (Slack)
**Slack 알림**: ✅ 전송됨
```

### 2. Running Tests

This section describes how to execute tests and analyze results.

#### Test Types

| 유형 | 설명 | Gradle 명령 |
|------|------|-------------|
| **unit** | 단위 테스트 | `./gradlew test` |
| **integration** | 통합 테스트 | `./gradlew integrationTest` |
| **all** | 전체 테스트 | `./gradlew check` |

#### Execution Flow

1. **테스트 탐색**: Explore test files.
2. **테스트 실행**: Execute tests using Gradle.
3. **결과 분석**: Analyze results and coverage.
4. **실패 분석**: Investigate reasons for test failures.

#### Output Format

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

### 3. Updating Test Results

This section allows QA personnel to update the results of assigned tests.

#### Required Inputs

| 입력 | 설명 | 필수 |
|------|------|------|
| 이슈 번호 | GitHub 이슈 번호 | ✅ |
| 테스트 결과 | pass / fail | ✅ |
| 코멘트 | 추가 설명 | ❌ |

#### Execution Flow

1. **이슈 조회**: Retrieve issue details.
2. **체크박스 업데이트**: Update the test status in the issue body.
3. **코멘트 추가**: Add a comment with the test result.
4. **라벨 변경**: Change the label from testing to tested.
5. **Slack 알림 (선택)**: Optionally send a notification to the requester.

#### Output Format

```markdown
[SEMO] Skill: qa-test → 테스트 결과 업데이트 완료

✅ **테스트 완료**: #123 - 로그인 기능 테스트

📋 **결과**: Pass
💬 **코멘트**: 추가됨
🏷️ **라벨**: testing → tested
📢 **알림**: @Reus에게 Slack 전송됨
```

## References

- [Team Members](../../semo-core/_shared/team-members.md) - GitHub/Slack ID 매핑
- [Test Patterns](references/test-patterns.md)
- [Coverage Guide](references/coverage-guide.md)
- [Troubleshooting](references/troubleshooting.md)

## Triggers

| 트리거 | 예시 |
|--------|------|
| "테스트 요청" | "테스트 요청해줘" |
| "QA 요청" | "QA 요청 보내줘" |
| "request-test" | "request-test 실행" |
| "테스트 할당" | "이슈에 테스트 할당해줘" |
| "내 테스트 목록" | "할당된 테스트" |
| "#123 테스트 완료" | "123 테스트 결과 업데이트" |
| "테스트 완료 처리해줘" | "테스트 완료" |