# Output Patterns

Skill 출력 형식 패턴 가이드.

## Template Pattern

**엄격한 형식 (API 응답, 데이터 형식)**:

```markdown
## Report structure

ALWAYS use this exact template:

# [Title]

## Summary
[One-paragraph overview]

## Key Findings
- Finding 1
- Finding 2

## Recommendations
1. Action 1
2. Action 2
```

**유연한 형식 (상황에 따라 조정)**:

```markdown
## Report structure

Sensible default, adjust as needed:

# [Title]

## Summary
[Overview - adapt based on context]

## Findings
[Tailor sections to specific analysis]
```

## Examples Pattern

출력 품질이 예시에 의존하는 경우:

```markdown
## Commit message format

**Example 1:**
Input: Added user authentication
Output:
feat(auth): implement JWT authentication

**Example 2:**
Input: Fixed date display bug
Output:
fix(reports): correct date formatting
```

예시는 설명보다 스타일 전달에 효과적입니다.
