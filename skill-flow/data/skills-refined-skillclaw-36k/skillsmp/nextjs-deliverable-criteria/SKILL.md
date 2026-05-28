---
name: nextjs-deliverable-criteria
description: Quality gates and acceptance criteria for Next.js 15 App Router projects
---

# Next.js Deliverable Quality Gates

## Pre-Deployment Checklist

### Compilation

**Requirements:**
- TypeScript compilation passes without errors
- Next.js build completes successfully (next build)
- No build warnings for missing pages or routes
- Static generation succeeds for all designated pages

**Commands:**
```bash
npm run build
npm run type-check  # if configured
```

**Acceptance:**
- Pass: Build completes with exit code 0
- Fail: Any TypeScript errors or build failures

### Linting

**Requirements:**
- ESLint passes with no errors
- ESLint warnings reviewed and addressed
- Prettier formatting applied consistently
- No disabled rules without justification

**Commands:**
```bash
npm run lint
npm run format:check  # if configured
```

**Acceptance:**
- Pass: Zero lint errors, warnings reviewed and justified
- Fail: Any lint errors or unaddressed critical warnings

### Testing

**Requirements:**
- All tests passing
- No skipped tests without justification
- Coverage meets minimum thresholds
- E2E tests pass for critical paths

**Commands:**
```bash
npm test
npm run test:e2e
npm run test:coverage
```

**Acceptance:**
- Pass: 100% test pass rate, coverage > 80% for core features
- Fail: Any failing tests or coverage below threshold

## Functionality

### Routing

**Criteria:**
- All routes accessible and render correctly
- Dynamic routes handle all expected params
- 404 pages show for invalid routes
- Navigation works without page refresh
- Deep linking works (URLs are shareable)

**Verification:**
- Manual testing of all routes
- E2E tests covering navigation flows
- Browser back/forward buttons work correctly

### Data Fetching

**Criteria:**
- All data displays correctly on initial load
- Loading states show during data fetch
- Error states display for failed requests
- Stale data invalidated appropriately
- No unnecessary re-fetches

**Verification:**
- Test with slow 3G network simulation
- Test with offline mode
- Verify caching behavior
- Check Network tab for request patterns

### Interactivity

**Criteria:**
- All forms submit successfully
- Form validation works correctly
- Buttons and links respond to clicks
- Loading indicators during async operations
- Success/error feedback after actions

**Verification:**
- Test all user flows
- Verify form validation messages
- Test keyboard navigation
- Test with JavaScript disabled (where applicable)

## Performance

### Core Web Vitals

**Requirements:**

| Metric | Target |
|--------|--------|
| Largest Contentful Paint (LCP) | < 2.5s |
| First Input Delay (FID) | < 100ms |
| Cumulative Layout Shift (CLS) | < 0.1 |
| First Contentful Paint (FCP) | < 1.8s |
| Time to Interactive (TTI) | < 3.8s |

**Verification:**
- Lighthouse audit score > 90
- PageSpeed Insights check
- WebPageTest.org analysis
- Real-world testing on 3G networks

### Bundle Size

**Criteria:**
- Initial JavaScript bundle < 200KB (gzipped)
- Total page weight < 1MB
- No duplicate dependencies in bundle
- Large libraries loaded dynamically

**Verification:**
- Bundle analysis with @next/bundle-analyzer
- Check Network tab in DevTools
- Verify code splitting working

### Caching

**Criteria:**
- Static assets cached appropriately
- API responses cached with correct strategy
- Stale-while-revalidate for dynamic content
- Cache invalidation works after updates

**Verification:**
- Check Response headers (Cache-Control)
- Verify cache behavior in Network tab
- Test cache invalidation scenarios

## Accessibility

### WCAG Compliance

**Criteria:**
- WCAG 2.1 Level AA compliance
- All images have alt text
- Proper heading hierarchy (h1-h6)
- Sufficient color contrast (4.5:1 for text)
- Keyboard navigation works completely
- Screen reader friendly

**Verification:**
- Lighthouse accessibility audit > 95
- axe DevTools scan with 0 violations
- Manual keyboard navigation test
- Screen reader test (VoiceOver/NVDA)

### Focus Management

**Criteria:**
- Focus visible on all interactive elements
- Tab order logical and predictable
- Focus trapped in modals
- Skip links for keyboard users

**Verification:**
- Tab through entire page
- Verify focus indicators visible
- Test modal focus behavior

## SEO

### Metadata

**Criteria:**
- Unique title for each page
- Meta descriptions for all pages
- Open Graph tags for social sharing
- Twitter Card metadata
- Canonical URLs set correctly
- Robots.txt configured
- Sitemap.xml generated

**Verification:**
- View page source for each route
- Test social share previews
- Check robots.txt and sitemap.xml
- Google Search Console validation

### Structured Data

**Criteria:**
- Schema.org markup where appropriate
- JSON-LD for structured data
- Valid structured data (no errors)

**Verification:**
- Google Rich Results Test
- Schema markup validator

## Security

### Authentication

**Criteria:**
- Protected routes require authentication
- JWT tokens stored securely (httpOnly cookies)
- Session timeout implemented
- Logout clears all auth data

**Verification:**
- Test accessing protected routes without auth
- Verify token storage method
- Test session expiration

### API Security

**Criteria:**
- Input validation on all API routes
- SQL injection prevention (parameterized queries)
- XSS prevention (sanitized output)
- CSRF protection for mutations
- Rate limiting on public endpoints
- API keys in environment variables

**Verification:**
- Penetration testing
- Input fuzzing
- Check .env not committed
- Verify CORS configuration

### Headers

**Criteria:**
- Content-Security-Policy header set
- X-Frame-Options set to DENY or SAMEORIGIN
- X-Content-Type-Options: nosniff
- Strict-Transport-Security (HSTS) for HTTPS

**Verification:**
- Security headers check (securityheaders.com)
- Verify headers in Response

## Mobile

### Responsive Design

**Criteria:**
- Works on screen sizes 320px - 2560px
- Touch targets minimum 44x44px
- No horizontal scrolling on mobile
- Font sizes readable on mobile (16px minimum)
- Images scale appropriately

**Verification:**
- Test on actual devices (iOS, Android)
- Chrome DevTools device emulation
- Test in portrait and landscape

### Performance

**Criteria:**
- LCP < 2.5s on 3G
- First load < 3s on 3G
- Total page weight < 500KB for mobile

**Verification:**
- Lighthouse mobile audit
- Test on 3G throttled connection

## Browser Compatibility

### Support

**Criteria:**
- Last 2 versions of Chrome, Firefox, Safari, Edge
- Safari iOS latest 2 versions
- Chrome Android latest 2 versions
- Graceful degradation for older browsers

**Verification:**
- BrowserStack testing
- Manual testing on major browsers
- Check caniuse.com for feature support

## Error Handling

### User Experience

**Criteria:**
- Error boundaries catch all React errors
- User-friendly error messages
- Recovery options provided (retry, go back)
- Errors logged to monitoring service

**Verification:**
- Simulate various error conditions
- Verify error tracking in monitoring service
- Check error messages are non-technical

## Monitoring

### Production Readiness

**Criteria:**
- Error tracking configured (Sentry, etc.)
- Performance monitoring active
- Analytics tracking implemented
- Health check endpoint available
- Logging configured appropriately

**Verification:**
- Verify errors appear in tracking service
- Check analytics events firing
- Test /api/health endpoint

## Deployment

### Configuration

**Criteria:**
- Environment variables documented
- Production .env.production configured
- Database migrations applied
- CDN configuration verified
- Domain SSL certificate valid

**Verification:**
- Review .env.example completeness
- Verify all environment variables set in production
- Check SSL certificate expiration

### Rollback Plan

**Criteria:**
- Rollback procedure documented
- Previous version can be restored quickly
- Database migrations are reversible

## Final Sign-Off

### Required Approvals

- [ ] Developer self-review completed
- [ ] Peer code review approved
- [ ] QA testing passed
- [ ] Product owner acceptance
- [ ] Security review completed (for sensitive features)
- [ ] Performance benchmarks met
- [ ] Accessibility audit passed

### Documentation

- [ ] README updated
- [ ] API documentation current
- [ ] Deployment instructions documented
- [ ] Environment variables documented
- [ ] Known issues documented

### Release Notes

- [ ] CHANGELOG updated
- [ ] Breaking changes documented
- [ ] Migration guide provided (if needed)

## Acceptance

### Go/No-Go

**Pass Criteria:**
- All critical tests passing
- No critical bugs open
- Performance meets requirements
- Security review complete
- Accessibility standards met

**Blockers:**
- Any critical security vulnerabilities
- Core functionality broken
- Performance regression > 20%
- Accessibility violations
- Data loss scenarios
