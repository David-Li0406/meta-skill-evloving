# Severity Levels Guide

## 🔴 Critical (Blocks PR)

Issues that **MUST** be fixed before PR approval:

- Test failures
- TypeScript errors
- ESLint errors
- Constitution violations (Principles I, II, III, VIII)
- Spec misalignment
- Page load failures
- JS crashes
- 핵심 기능 불가

**Action**: Fix immediately. PR will be REJECTED until resolved.

## 🟡 Warning (Should Fix)

Issues that **SHOULD** be fixed but don't block PR:

- Debug code (`console.log`, `debugger`)
- 'any' types
- Missing tests
- Low coverage (below thresholds)
- Documentation gaps
- 콘솔 경고
- 스타일 이슈
- 비핵심 기능 문제

**Action**: Recommended fix before merge. Status: APPROVED_WITH_WARNINGS

## 🟢 Suggestion (Nice to Have)

Improvements for better quality:

- Performance optimizations
- Accessibility improvements
- Code style preferences
- Additional test cases
- 성능 개선 제안
- UI 개선 제안

**Action**: Optional. Can be addressed in future PRs.

## Critical Rules

1. **Never Auto-Fix**: Always report, never fix automatically
2. **Constitution Authority**: Principles are non-negotiable
3. **Spec Analysis First**: Integrated spec compliance check runs first
4. **Actionable Feedback**: Provide file/line references
5. **Approval Criteria**: No critical issues = APPROVED

## Error Handling

If verification fails:

1. Generate comprehensive report
2. Categorize by severity (Critical/Warning/Suggestion)
3. Provide specific fix recommendations with file/line refs
4. Return REJECTED status
5. Agent decides fix strategy

## Dependencies

### Foundation Commands (Layer 1)

- None (spec analysis fully integrated)

### Skills (Layer 2)

- `skill:check-team-codex` - Team Codex validation
- `skill:validate-architecture` - DDD architecture validation

### External Tools

- `npm test` - Test execution
- `npm run test:coverage` - Coverage report
- `npm run lint` - ESLint
- `npx tsc --noEmit` - TypeScript check

## Related Skills

- `spec` - SDD Phase 1-3
- `implement` - ADD Phase 4
- `spike` - Technical exploration
- `constitution` - Constitution management

## Performance

| Mode | Time |
|------|------|
| Full verification | ~2-3 minutes |
| Quick check (no tests) | ~30 seconds |
| Spec-only | ~15 seconds |

## Success Criteria

This skill succeeds when:

- ✅ All 6 verification layers complete
- ✅ Report generated with actionable feedback
- ✅ Status determined (APPROVED/APPROVED_WITH_WARNINGS/REJECTED)
- ✅ No false positives in critical issues
- ✅ All file/line references accurate
