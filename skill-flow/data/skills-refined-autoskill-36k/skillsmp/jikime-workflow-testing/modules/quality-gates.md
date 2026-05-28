# Quality Gates

코드 품질 검증을 위한 실용적인 체크리스트와 기준.

## TRUST Quality Checklist

5가지 핵심 품질 기준:

### T - Testable (테스트 가능성)

```markdown
- [ ] 순수 함수로 작성 (동일 입력 → 동일 출력)
- [ ] 의존성 주입 가능 (mocking 용이)
- [ ] 부수 효과 격리 (side effects isolated)
- [ ] 작은 단위로 분리 (single responsibility)
```

**검증 방법**: 테스트 작성이 어려우면 리팩토링 필요

### R - Readable (가독성)

```markdown
- [ ] 의미 있는 변수/함수명 (self-documenting)
- [ ] 함수 50줄 이하
- [ ] 중첩 3단계 이하
- [ ] 주석 없이 이해 가능
```

**검증 방법**: 처음 보는 사람이 5분 내 이해 가능

### U - Unified (일관성)

```markdown
- [ ] 프로젝트 코딩 컨벤션 준수
- [ ] 동일 패턴 반복 사용
- [ ] ESLint/Prettier 경고 없음
- [ ] TypeScript strict 모드 통과
```

**검증 방법**: `npm run lint && npm run type-check`

### S - Secure (보안)

```markdown
- [ ] 사용자 입력 검증 (Zod schema)
- [ ] SQL Injection 방지 (parameterized queries)
- [ ] XSS 방지 (escape/sanitize)
- [ ] 민감 정보 노출 없음 (env variables)
```

**검증 방법**: OWASP Top 10 체크리스트

### T - Traceable (추적 가능성)

```markdown
- [ ] 에러 메시지에 컨텍스트 포함
- [ ] 로깅 적절히 사용
- [ ] 디버깅 가능한 스택 트레이스
- [ ] 버전/배포 정보 추적 가능
```

**검증 방법**: 프로덕션 에러 재현 가능 여부

---

## Coverage Requirements

### Minimum Standards

| Metric | Minimum | Target | Excellent |
|--------|---------|--------|-----------|
| Statements | 70% | 80% | 90%+ |
| Branches | 70% | 80% | 90%+ |
| Functions | 70% | 80% | 90%+ |
| Lines | 70% | 80% | 90%+ |

### Coverage Exemptions (최소화)

정당한 이유가 있는 경우만:

```typescript
/* v8 ignore next */
if (process.env.NODE_ENV === 'development') {
  // Development-only code
}

/* v8 ignore start */
// Generated code or third-party integration
/* v8 ignore stop */
```

---

## PR Merge Checklist

### Required (Blocking)

```markdown
## PR Checklist

### Tests
- [ ] All tests pass: `npm run test:run`
- [ ] Coverage threshold met: `npm run test:coverage`
- [ ] E2E tests pass: `npm run test:e2e`

### Code Quality
- [ ] No TypeScript errors: `npm run type-check`
- [ ] No lint errors: `npm run lint`
- [ ] Build succeeds: `npm run build`

### Review
- [ ] Self-reviewed diff
- [ ] New features have tests
- [ ] Breaking changes documented
```

### Recommended (Non-blocking)

```markdown
### Nice to Have
- [ ] Performance impact considered
- [ ] Accessibility checked (if UI changes)
- [ ] Documentation updated (if API changes)
```

---

## CI Pipeline Gates

### Stage 1: Lint & Type Check

```yaml
lint:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - run: npm ci
    - run: npm run lint
    - run: npm run type-check
```

### Stage 2: Unit Tests

```yaml
test:
  needs: lint
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - run: npm ci
    - run: npm run test:coverage
    - name: Check coverage
      run: |
        COVERAGE=$(cat coverage/coverage-summary.json | jq '.total.lines.pct')
        if (( $(echo "$COVERAGE < 80" | bc -l) )); then
          echo "Coverage $COVERAGE% is below 80%"
          exit 1
        fi
```

### Stage 3: E2E Tests

```yaml
e2e:
  needs: test
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - run: npm ci
    - run: npx playwright install --with-deps
    - run: npm run build
    - run: npm run test:e2e
```

### Stage 4: Deploy (on success)

```yaml
deploy:
  needs: [lint, test, e2e]
  if: github.ref == 'refs/heads/main'
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - run: npm ci
    - run: npm run build
    - run: # Deploy command
```

---

## Quick Reference

### Commands

```bash
# Full quality check
npm run lint && npm run type-check && npm run test:run && npm run build

# Quick check (pre-commit)
npm run lint && npm run type-check

# Pre-push check
npm run test:run && npm run build
```

### Git Hooks (husky + lint-staged)

```json
// package.json
{
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md}": ["prettier --write"]
  }
}
```

```bash
# .husky/pre-commit
npm run lint-staged

# .husky/pre-push
npm run test:run
```

---

## When to Skip Gates

> ⚠️ 게이트 스킵은 **긴급 상황**에서만 사용

```bash
# Skip pre-commit hook (emergency only)
git commit --no-verify -m "hotfix: critical bug"

# Document in PR why gates were skipped
```

**스킵 시 필수 조치**:
1. PR에 스킵 사유 명시
2. 24시간 내 테스트 보완
3. 팀 리드 승인
