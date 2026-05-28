---
name: commit
description: >
  Git 커밋 생성을 위한 skill.
  TDD 사이클 완료 후 또는 작업 단위 완료 시 호출하여 일관된 커밋 메시지 생성.
  상세 convention은 references/convention.md 참조.
---

# Commit Skill

작업 완료 후 커밋 생성 가이드

## 커밋 생성 절차

1. 변경사항 확인
   ```bash
   git diff --stat
   ```

2. 100줄 이하인지 확인 (TDD 작업 시)

3. 커밋 생성
   ```bash
   git add -A && git commit -m "$(cat <<'EOF'
   {type}: {description}
   EOF
   )"
   ```

## 커밋 타입 요약

| 타입 | 용도 |
|------|------|
| `feat` | 새 기능 추가 |
| `fix` | 버그 수정 |
| `test` | 테스트 코드 |
| `refactor` | 리팩토링 |
| `docs` | 문서 수정 |
| `chore` | 빌드, 설정 변경 |

**상세 규칙**: `references/convention.md` 참조
