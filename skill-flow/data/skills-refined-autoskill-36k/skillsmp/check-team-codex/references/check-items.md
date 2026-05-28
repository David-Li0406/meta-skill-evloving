# Check Items

> **SoT 참조**: 모든 검증 규칙은 `semo-core/TEAM_RULES.md`에서 관리됩니다.

## 검증 명령어 요약

| 항목 | 명령어 |
|------|--------|
| ESLint | `npm run lint` |
| TypeScript | `npx tsc --noEmit` |
| Debug 코드 | `grep -r "console\.log\|debugger" src/` |
| any 타입 | `grep -r ":\s*any\|as any" src/` |
| hook 우회 | `git log -1 --format=%B \| grep -i "no-verify"` |

## 상세 규칙

**semo-core/TEAM_RULES.md 참조**:
- 섹션 2.1: 필수 검증 항목
- 섹션 2.2: 금지 사항
- 섹션 2.5: Severity Levels
- 섹션 6: Quality Gates
