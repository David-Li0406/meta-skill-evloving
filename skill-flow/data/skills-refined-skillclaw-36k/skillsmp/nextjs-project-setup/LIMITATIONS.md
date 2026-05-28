# Known Limitations and Constraints

**Skill**: Next.js Project Setup
**Version**: 1.0.0
**Last Updated**: 2025-10-29

---

## Overview

This document outlines known limitations, constraints, and edge cases for the Next.js Project Setup skill. Understanding these limitations helps users set appropriate expectations and developers plan future improvements.

---

## Technical Limitations

### 1. Token Budget Enforcement

**Current State**: Documentation-based, not programmatically enforced

**Limitation**:
- Agents are instructed to stay within ≤2500 tokens
- No runtime validation prevents exceeding budget
- Relies on template structure and manual validation

**Impact**: Low
- All agents currently comply with budget
- validation script available for manual checks

**Workaround**:
```bash
# Manual validation after generation
./validate-report-tokens.sh agent-report.md
```

**Future Enhancement**:
```typescript
// Programmatic enforcement
function generateReport(content: string, budget: number = 2500) {
  const tokens = countTokens(content)
  if (tokens > budget) {
    throw new TokenBudgetExceededError(tokens, budget)
  }
  return content
}
```

---

### 2. Token Counting Accuracy

**Current State**: Estimation-based (word count × 1.33)

**Limitation**:
- Rough approximation, not exact
- Can be off by ±10-15%
- Different content types have different token densities

**Impact**: Low-Medium
- Estimates generally accurate within margin
- Budget padding accounts for variance

**Actual vs Estimated**:
```
Markdown with code blocks: 0.8 tokens/word
Plain prose: 0.75 tokens/word
JSON/structured data: 1.0 tokens/word

Current estimate: 0.75 tokens/word (average)
```

**Future Enhancement**:
- Integrate tiktoken or similar tokenizer library
- Real-time token counting during generation
- Per-content-type adjustments

---

### 3. MCP Tool Availability

**Current State**: Assumes MCP servers configured

**Limitation**:
- Skill fails gracefully if MCP tools unavailable
- Some functionality reduced without tools
- No auto-setup of MCP servers

**Impact**: Medium
- Core functionality preserved (uses WebSearch/WebFetch fallback)
- Quality reduced without specialized tools

**Affected Agents**:
- design-ideator: Needs mcp__shadcn__* for component discovery
- research-supabase: Needs mcp__supabase__* for schema queries
- research-design: Needs mcp__21st-dev__* for design inspiration

**Workaround**:
```markdown
If mcp__shadcn__* unavailable:
  → Use WebSearch for Shadcn documentation
  → Manual component discovery via file system
  → Reduced automation, same output quality
```

**Future Enhancement**:
- Auto-detect MCP availability
- Provide setup instructions if missing
- Cache common MCP responses

---

### 4. Parallel Execution Dependency Management

**Current State**: Manual dependency specification in ARCHITECTURE.md

**Limitation**:
- No runtime dependency resolution
- Orchestrator must manually sequence agents
- Risk of incorrect execution order

**Impact**: Low
- Clear documentation prevents errors
- Simple dependency graph (research → design → validation)

**Current Dependencies**:
```
research-vercel   ]
research-shadcn   ] → No dependencies (parallel)
research-supabase ]
research-design   ]

design-ideator → Depends on research-* reports

qa-validator   ] → Depends on project files
doc-auditor    ] → Depends on project files
```

**Future Enhancement**:
```typescript
interface AgentDependencies {
  agent: string
  dependsOn: string[]
  canRunInParallel: boolean
}

const dependencies: AgentDependencies[] = [
  { agent: 'design-ideator', dependsOn: ['research-*'], canRunInParallel: false },
  { agent: 'qa-validator', dependsOn: [], canRunInParallel: true }
]
```

---

## Functional Limitations

### 5. Project Type Coverage

**Current State**: Optimized for SaaS dashboards

**Limitation**:
- Primary focus: SaaS, e-commerce, blogs
- Less coverage: Mobile apps, desktop apps, embedded systems
- No support: Non-Next.js frameworks

**Supported Project Types**:
- ✅ SaaS dashboards (excellent coverage)
- ✅ E-commerce stores (good coverage)
- ✅ Blogs & content sites (good coverage)
- ✅ Landing pages (good coverage)
- ⚠️ Real-time apps (limited guidance)
- ⚠️ Complex integrations (basic patterns only)
- ❌ Non-web applications
- ❌ Other frameworks (Vue, Angular, Svelte)

**Impact**: Medium
- Works well for 80% of Next.js use cases
- May need customization for specialized apps

**Future Enhancement**:
- Add research-realtime.md agent (WebSocket patterns)
- Add research-integrations.md agent (API patterns)
- Create framework-agnostic base skill

---

### 6. Design System Customization

**Current State**: 3-5 pre-defined options generated

**Limitation**:
- No fully custom design from scratch
- Options based on 2025 trends (may become dated)
- Limited to Shadcn UI component library

**Design Constraints**:
- Uses Shadcn UI components only (not Material UI, Chakra, etc.)
- Tailwind CSS required (no styled-components, CSS-in-JS)
- Color palettes limited to WCAG-compliant combinations

**Impact**: Low-Medium
- Shadcn UI + Tailwind covers 90% of needs
- Generated designs are professional and modern
- Custom designs require manual adjustment

**Workaround**:
- Use design-ideator output as starting point
- Manually adjust color palettes
- Add custom components outside Shadcn

**Future Enhancement**:
- Support for additional component libraries
- AI-driven custom palette generation
- Import existing design tokens

---

### 7. Multi-Tenant Complexity

**Current State**: Basic multi-tenant patterns provided

**Limitation**:
- Tenant isolation via RLS (row-level security)
- No advanced features: subdomain routing, tenant-specific themes
- Simple tenant_id foreign key approach only

**Not Covered**:
- Subdomain-based tenant routing (tenant1.app.com)
- Tenant-specific feature flags
- Tenant-specific theming/branding
- Advanced billing per tenant
- Tenant analytics and metrics

**Impact**: Medium
- Basic multi-tenancy works well
- Advanced needs require custom implementation

**Current Pattern**:
```sql
-- Simple tenant isolation
CREATE TABLE projects (
  id UUID PRIMARY KEY,
  tenant_id UUID REFERENCES tenants(id),
  ...
);

CREATE POLICY "Tenant isolation"
ON projects FOR ALL
USING (tenant_id = (SELECT tenant_id FROM users WHERE id = auth.uid()));
```

**Future Enhancement**:
- research-multitenancy.md agent
- Advanced tenant routing patterns
- Feature flag systems

---

## Scale Limitations

### 8. Project Size Assumptions

**Current State**: Optimized for small-to-medium projects

**Limitation**:
- Assumes <100 database tables
- Assumes <50 Shadcn components
- Assumes <500 routes

**Performance at Scale**:
| Project Size | Status | Notes |
|-------------|--------|-------|
| 1-20 tables | ✅ Excellent | Optimal performance |
| 20-50 tables | ✅ Good | May need manual optimization |
| 50-100 tables | ⚠️ Acceptable | Requires custom architecture |
| 100+ tables | ❌ Not Recommended | Use microservices instead |

**Impact**: Low-Medium
- Most Next.js projects <50 tables
- Skill guides toward simple architectures

**Future Enhancement**:
- Add complexity detector
- Recommend microservices when appropriate
- Provide service decomposition patterns

---

### 9. Team Collaboration Features

**Current State**: Single-user workflow

**Limitation**:
- No built-in collaboration features
- No version control integration
- No team member handoff protocols

**Not Included**:
- Git workflow recommendations
- Code review checklists
- Team communication templates
- Deployment pipeline setup

**Impact**: Low
- Individual developers well-served
- Teams need to add collaboration layer

**Workaround**:
- Use generated specs for team communication
- Add git workflow manually
- Integrate with existing tools (Jira, Linear, etc.)

**Future Enhancement**:
- Team collaboration templates
- Git workflow recommendations
- PR description auto-generation

---

## Quality Limitations

### 10. Accessibility Testing Depth

**Current State**: Checklist-based validation

**Limitation**:
- No automated accessibility testing
- No screen reader simulation
- No keyboard navigation testing

**Current Validation**:
- ✅ Color contrast calculation (WCAG ratios)
- ✅ Semantic HTML structure check
- ✅ ARIA attribute presence
- ❌ Actual screen reader testing
- ❌ Keyboard navigation flow
- ❌ Focus management validation

**Impact**: Medium
- Basic accessibility covered
- Production apps need real user testing

**Recommendation**:
```bash
# Manual testing required
npm install --save-dev @axe-core/react
npm install --save-dev jest-axe

# Run Lighthouse CI
npx lighthouse https://your-app.com --view
```

**Future Enhancement**:
- Integrate axe-core for automated testing
- Add Playwright accessibility tests
- Generate VPAT (Voluntary Product Accessibility Template)

---

### 11. Performance Testing Depth

**Current State**: Build analysis only

**Limitation**:
- No load testing
- No stress testing
- No real-world performance metrics

**Current Validation**:
- ✅ Build size analysis
- ✅ First Load JS calculation
- ✅ Core Web Vitals estimation
- ❌ Actual LCP/FID/CLS measurement
- ❌ API response time testing
- ❌ Database query performance

**Impact**: Medium
- Estimates are usually accurate
- Production needs real metrics

**Recommendation**:
```bash
# Real performance testing
npm install --save-dev lighthouse
npm install --save-dev @vercel/analytics

# Run performance tests
npm run build
npm run analyze
```

**Future Enhancement**:
- Integrate Lighthouse programmatically
- Add synthetic monitoring setup
- Provide RUM (Real User Monitoring) configuration

---

## Documentation Limitations

### 12. Auto-Generated Documentation Quality

**Current State**: Template-based generation

**Limitation**:
- Generic sections need manual refinement
- No code-to-docs synchronization
- Placeholders require filling

**Generated Quality**:
- ✅ Structure and sections (100% complete)
- ✅ Common patterns (90% accurate)
- ⚠️ Project-specific details (60% complete - needs review)
- ❌ Custom business logic (0% - manual addition required)

**Example Placeholders**:
```markdown
## API Endpoints

### POST /api/items
**Purpose**: [FILL IN: Describe what this endpoint does]
**Authentication**: Required | Optional | None
**Parameters**:
- name (string, required): [FILL IN: Description]
```

**Impact**: Medium
- Good starting point
- Requires developer review and refinement

**Future Enhancement**:
- AST parsing for automatic endpoint documentation
- Type extraction from TypeScript
- Auto-generate OpenAPI specs

---

## Edge Cases

### 13. Non-Standard Project Structures

**Current State**: Assumes Next.js conventions

**Limitation**:
- Expects app directory structure (Next.js 13+)
- Assumes standard folder layout
- May not work with custom configurations

**Assumptions**:
```
project/
├── app/
│   ├── (routes)/
│   ├── api/
│   └── layout.tsx
├── components/
│   └── ui/
├── lib/
└── public/
```

**Unsupported Structures**:
- Pages directory (Next.js 12 and earlier)
- Monorepo setups (without adjustments)
- Custom src/ directory structures

**Impact**: Low-Medium
- Next.js 13+ adoption is high
- Skill focuses on modern patterns

**Workaround**:
- Manually adjust generated file paths
- Update templates for custom structure

**Future Enhancement**:
- Auto-detect project structure
- Support pages directory
- Monorepo compatibility

---

### 14. Internationalization (i18n)

**Current State**: Not covered

**Limitation**:
- No i18n patterns included
- No translation workflow
- No locale routing guidance

**Not Included**:
- Multi-language support
- RTL (right-to-left) layouts
- Currency/date localization
- Translation management

**Impact**: Medium (if i18n needed)
- Single-language projects unaffected
- Multi-language needs custom implementation

**Recommendation**:
```bash
# Manual i18n setup
npm install next-intl

# Configure manually
# See: https://next-intl-docs.vercel.app
```

**Future Enhancement**:
- research-i18n.md agent
- Translation workflow templates
- Locale-based routing patterns

---

### 15. Offline Functionality

**Current State**: Not covered

**Limitation**:
- No PWA (Progressive Web App) patterns
- No service worker setup
- No offline data synchronization

**Not Included**:
- Offline-first architecture
- Service worker configuration
- Cache strategies
- Background sync

**Impact**: Low-Medium
- Most SaaS apps require online connection
- PWAs are specialized use case

**Future Enhancement**:
- research-pwa.md agent
- Service worker templates
- Offline-first patterns

---

## Mitigation Strategies

### For Users

**If you encounter limitations**:

1. **Check Workarounds**: Most limitations have documented workarounds
2. **Manual Customization**: Use generated output as starting point
3. **Community Resources**: Consult Next.js/Supabase/Shadcn communities
4. **Report Issues**: Help improve skill by reporting gaps

### For Developers

**When extending the skill**:

1. **Follow Architecture**: Maintain sub-agent pattern (≤2500 tokens)
2. **Document New Limitations**: Update this file with new constraints
3. **Test Edge Cases**: Add tests for boundary conditions
4. **Maintain Backward Compatibility**: Version changes appropriately

---

## Future Roadmap

### Short-Term (v1.1 - v1.2)

- [ ] Add programmatic token counting
- [ ] Implement runtime dependency resolution
- [ ] Create research-realtime.md agent
- [ ] Add automated accessibility testing

### Medium-Term (v1.3 - v1.5)

- [ ] Support additional component libraries
- [ ] Add team collaboration features
- [ ] Create research-i18n.md agent
- [ ] Integrate performance monitoring

### Long-Term (v2.0+)

- [ ] Framework-agnostic base skill
- [ ] Advanced multi-tenancy patterns
- [ ] AI-driven custom design generation
- [ ] Full test automation integration

---

## Version History

**v1.0.0** (2025-10-29): Initial release
- 15 documented limitations
- Mitigation strategies provided
- Future roadmap defined

---

## Contributing

Found a limitation not listed here? Please:
1. Document the issue
2. Provide reproduction steps
3. Suggest potential solutions
4. Submit for review

---

**Maintained By**: Next.js Project Setup Skill Development Team
**Last Review**: 2025-10-29
**Next Review**: 2026-01-29
