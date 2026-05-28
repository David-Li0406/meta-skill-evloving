---
name: git-commit-formatter
description: Formats git commit messages according to Conventional Commits specification. Use this when the user asks to commit changes or write a commit message.
---

# Git Commit Formatter Skill

When writing a git commit message, you MUST follow the Conventional Commits specification.

## Format
`<type>[optional scope]: <description>`

## Allowed Types
- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, etc)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **chore**: Changes to the build process or auxiliary tools and libraries such as documentation generation

## Instructions
1. **변화 유형 파악**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore` 중 하나를 선택합니다.
2. **한국어 작성 선호**: QueryCraft 팀은 가독성을 위해 **한국어 요약**을 선호합니다.
3. **포맷**: `<type>: <description>` 형식으로 작성합니다.

## Example
`feat: 스트림 분석 문제 생성 로직 예외 처리 추가`

