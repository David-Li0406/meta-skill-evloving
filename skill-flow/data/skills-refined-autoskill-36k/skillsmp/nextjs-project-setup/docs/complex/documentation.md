# Phase 8: Documentation

**Duration**: 1-2 hours
**Prerequisites**: Phase 7 (QA complete, production-ready)
**Next Phase**: Deployment & Handover

---

## Overview

**Purpose**: Create comprehensive documentation for developers, users, and AI agents

**Inputs**:
- Completed application (Phases 2-6)
- QA report (Phase 7)
- Tech stack and architecture (plan.md from Phase 3)
- Design system (design-system.md from Phase 4)

**Outputs**:
- `/README.md` (project overview for humans)
- `/CLAUDE.md` (AI agent context and conventions)
- `/docs/API.md` (if API routes exist)
- `/docs/DEPLOYMENT.md` (deployment guide)
- `/CHANGELOG.md` (version history setup)
- Component documentation (inline or Storybook)

---

## Documentation Philosophy

**Target Audiences**:
1. **Developers** (new team members, contributors) → README.md, API.md
2. **AI Agents** (Claude Code, Cursor) → CLAUDE.md
3. **DevOps** (deployment, maintenance) → DEPLOYMENT.md
4. **Users** (if open source or internal tool) → User guides

**Quality Standards**:
- Concise but complete (no fluff)
- Actionable (commands that work, not theory)
- Maintainable (easy to update as project evolves)
- Searchable (clear headings, keywords)

---

## Tools Required

- **File System**: Documentation creation
- **doc-auditor agent** (optional): Validates documentation completeness

---

## Workflow (CoD^Σ)

```
Project_Context → README.md + CLAUDE.md
  ↓
Tech_Stack → API.md + Component_Docs
  ↓
Deployment_Config → DEPLOYMENT.md
  ↓
QA_Report → Known_Issues_Section
  ↓
Doc_Auditor_Agent → Completeness_Check
  ↓
Documentation_Complete
```

---

## Documentation Creation

### 1. README.md (Developer-Focused)

**Purpose**: Entry point for developers joining the project

**Structure**:
```markdown
# [Project Name]

[One-line description of what this project does]

## Features

- ✨ Feature 1 (from P1 user story)
- ✨ Feature 2 (from P1 user story)
- ✨ Feature 3 (from P2 user story)

## Tech Stack

- **Framework**: Next.js 14+ (App Router)
- **Database**: Supabase (PostgreSQL)
- **Auth**: Supabase Auth
- **Styling**: Tailwind CSS + Shadcn UI (@ui registry)
- **Language**: TypeScript
- **Testing**: Vitest + Testing Library

## Prerequisites

- Node.js 18+ (LTS recommended)
- npm 9+ or pnpm 8+
- Supabase account (for database & auth)

## Getting Started

### Installation

```bash
# Clone repository
git clone [repository-url]
cd [project-name]

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your Supabase keys
```

### Environment Variables

Required in `.env.local`:
```bash
NEXT_PUBLIC_SUPABASE_URL=your-project-url
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

### Database Setup

```bash
# Run migrations
npx supabase db push

# Seed database (optional)
npm run db:seed
```

### Development

```bash
# Start development server
npm run dev

# Open http://localhost:3000
```

### Testing

```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run E2E tests
npm run test:e2e
```

### Build

```bash
# Create production build
npm run build

# Start production server
npm start
```

## Project Structure

```
/app              # Next.js App Router pages
  /api            # API routes
  /auth           # Authentication pages
  /dashboard      # Dashboard pages
  layout.tsx      # Root layout
  page.tsx        # Home page
/components
  /ui             # Shadcn UI components
  /auth           # Authentication components
  /dashboard      # Dashboard components
/lib
  /supabase       # Supabase client setup
  /utils          # Utility functions
/tests
  /e2e            # E2E tests (Playwright)
  /integration    # Integration tests
  /unit           # Unit tests
/public           # Static assets
/docs             # Additional documentation
```

## Key Commands

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm test` | Run tests |
| `npm run lint` | Run ESLint |
| `npm run type-check` | Run TypeScript compiler |

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for contribution guidelines.

## License

[Your License] - See [LICENSE](./LICENSE) for details.

## Support

- Documentation: [docs/](./docs/)
- Issues: [GitHub Issues](repository-issues-url)
- Discussions: [GitHub Discussions](repository-discussions-url)

---

**Made with ❤️ by [Your Team]**
```

**README.md Best Practices**:
- Keep it concise (<300 lines)
- Use emoji sparingly (features section only)
- Test all commands (ensure they actually work)
- Update badges if applicable (build status, coverage)
- Link to detailed docs instead of cramming everything into README

### 2. CLAUDE.md (AI Agent Context)

**Purpose**: Guide Claude Code and other AI agents working on this codebase

**Template**: See @templates/claude-md-template.md for basic structure

**Detailed Example Structure**:
```markdown
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Overview

**Project Name**: [Name]
**Description**: [What this project does]
**Core Innovation**: [What makes this unique]

---

## Tech Stack

- **Framework**: Next.js 14+ (App Router)
- **Database**: Supabase (PostgreSQL with RLS)
- **Auth**: Supabase Auth (email/password + social)
- **UI**: Shadcn UI (@ui registry)
- **Styling**: Tailwind CSS with CSS variables
- **Language**: TypeScript (strict mode)
- **Testing**: Vitest + Testing Library + Playwright

---

## Architecture

**App Router Structure**:
- `/app/(auth)` - Authentication pages (login, signup)
- `/app/(dashboard)` - Protected dashboard pages
- `/app/api` - API routes (RESTful)

**Database Schema** (key tables):
- `users` - User accounts (managed by Supabase Auth)
- `profiles` - Extended user profiles
- `[feature-table]` - [Description]

**Authentication Flow**:
1. User logs in via `/auth/login`
2. Supabase Auth validates credentials
3. Session stored in HTTP-only cookie
4. Middleware protects `/dashboard/*` routes
5. RLS policies enforce row-level security

---

## Development Conventions

### Component Organization
- **Pages**: `/app` directory (Next.js App Router)
- **Components**: `/components` organized by feature
- **UI Components**: `/components/ui` (Shadcn only, installed via CLI)
- **Utilities**: `/lib/utils.ts` (shared helpers)

### File Naming
- Components: PascalCase (e.g., `LoginForm.tsx`)
- Utilities: camelCase (e.g., `formatDate.ts`)
- API routes: lowercase (e.g., `/api/users/route.ts`)

### Styling
- **Global CSS Variables ONLY** - No hardcoded colors
- **Design System**: See `/docs/design-system.md`
- **Responsive**: Mobile-first (Tailwind `sm:`, `md:`, `lg:`)
- **Dark Mode**: Via `next-themes` (respects system preference)

### Shadcn Workflow
**MANDATORY**: Always follow this workflow when adding UI components:

1. **Search**: Use MCP to find component
   ```typescript
   mcp__shadcn__search_items_in_registries(['@ui'], 'button')
   ```

2. **View**: Check component details
   ```typescript
   mcp__shadcn__view_items_in_registries(['@ui/button'])
   ```

3. **Example**: Get usage example
   ```typescript
   mcp__shadcn__get_item_examples_from_registries(['@ui'], 'button-demo')
   ```

4. **Install**: Add component to project
   ```bash
   npx shadcn@latest add button
   ```

**NEVER** skip the Example step - it shows correct usage patterns.

### Testing
- **TDD Required**: Write tests BEFORE implementation (no exceptions)
- **Test Location**: `/tests` directory (mirrors `/app` structure)
- **Naming**: `[component].test.tsx` for components, `[feature].spec.ts` for E2E
- **Coverage**: 100% of acceptance criteria must have tests

### Database
- **ORM**: Supabase client (no raw SQL unless necessary)
- **Migrations**: Via Supabase CLI (`supabase migration new [name]`)
- **RLS**: Row Level Security enabled on all tables
- **Seed Data**: `/supabase/seed.sql` for development

---

## Anti-Patterns (Don't Do These)

❌ **Hardcoded Colors** - Use CSS variables from `globals.css`
  - Bad: `className="text-[#000000]"`
  - Good: `className="text-primary"`
  - **Why**: Hardcoded colors break theme switching, prevent design system updates, and create unmaintainable color sprawl.

❌ **Skipping Shadcn Example Step** - Always check examples before using
  - Bad: Guessing component API
  - Good: Following official example patterns
  - **Why**: Examples reveal real-world usage patterns, edge cases, and integration requirements that prevent bugs discovered only after installation.

❌ **Client-Side Auth Checks** - Use middleware for route protection
  - Bad: `if (!session) redirect('/login')` in page
  - Good: Middleware handles redirects
  - **Why**: Client-side checks are bypassable and create race conditions; middleware provides secure server-side enforcement before page renders.

❌ **Mixing Pages & App Router** - This is App Router only
  - Bad: Creating `/pages/` directory
  - Good: All routes in `/app/`
  - **Why**: Mixing routers creates conflicts, confusing behavior, and duplicate routing logic; App Router is the modern standard with better features.

❌ **Custom Tailwind Without Variables** - Extend `tailwind.config.ts` with CSS variables
  - Bad: `colors: { brand: '#FF0000' }`
  - Good: `colors: { brand: 'hsl(var(--brand))' }`
  - **Why**: Hardcoded config values bypass CSS variables system, breaking theme switching and requiring Tailwind recompilation for color changes.

❌ **Direct Supabase Admin Key Usage** - Use service role key only in API routes
  - Bad: SUPABASE_SERVICE_ROLE_KEY in client components
  - Good: Server-side only (API routes, server components)
  - **Why**: Service role keys bypass RLS and grant full database access; exposing in client code creates catastrophic security vulnerability (data theft, deletion, manipulation).

---

## Common Tasks

### Adding a New Page
1. Create file in `/app/[route]/page.tsx`
2. Add to navigation (if applicable)
3. Write E2E test in `/tests/e2e/[route].spec.ts`
4. Update sitemap if public page

### Adding a New Component
1. Follow Shadcn workflow (Search → View → Example → Install)
2. Create wrapper in `/components/[feature]/` if needed
3. Write unit test in `/tests/unit/[component].test.tsx`
4. Use design system variables only

### Adding a New API Route
1. Create `/app/api/[route]/route.ts`
2. Validate input with Zod schema
3. Enforce authentication (check session)
4. Write integration test in `/tests/integration/[route].spec.ts`
5. Document in `/docs/API.md`

### Database Changes
1. Create migration: `supabase migration new [name]`
2. Write migration SQL
3. Apply locally: `supabase db push`
4. Update TypeScript types: `npm run db:types`
5. Test with seed data

---

## Environment Variables

**Development** (`.env.local`):
```bash
NEXT_PUBLIC_SUPABASE_URL=http://localhost:54321
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=eyJhbGc...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGc... (server-side only)
```

**Production** (Vercel):
Set in Vercel dashboard under Settings → Environment Variables

**Security**:
- ✅ `NEXT_PUBLIC_*` - Safe to expose to client
- ❌ Without `NEXT_PUBLIC_` - Server-side only (never expose)

---

## Troubleshooting

### Issue: "Hydration mismatch" error
**Cause**: Server and client render different content
**Solution**: Use `suppressHydrationWarning` on time-sensitive elements or ensure consistent rendering

### Issue: Shadcn component not found
**Cause**: Component not installed or wrong import path
**Solution**: Run `npx shadcn@latest add [component]`, verify import from `@/components/ui/[component]`

### Issue: Database types out of sync
**Cause**: Schema changed but types not regenerated
**Solution**: Run `npm run db:types` to regenerate

### Issue: Authentication not persisting
**Cause**: Cookie configuration or middleware issue
**Solution**: Check middleware.ts is exporting correct `config`, verify Supabase client setup

---

## Resources

- [Next.js App Router Docs](https://nextjs.org/docs/app)
- [Shadcn UI Components](https://ui.shadcn.com)
- [Supabase Documentation](https://supabase.com/docs)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Project Architecture](/docs/architecture.md)
- [API Documentation](/docs/API.md)

---

**This file was generated as part of the Next.js project setup following Intelligence Toolkit best practices.**
```

**CLAUDE.md Best Practices**:
- Focus on AI-relevant context (conventions, anti-patterns, common tasks)
- Include actual command examples (not placeholders)
- Document "why" for conventions (helps AI make better decisions)
- Keep it concise (<500 lines) - AI has limited context window

### 3. API.md (If Applicable)

**Purpose**: Document API routes for developers and AI agents

**Structure**:
```markdown
# API Documentation

Base URL: `http://localhost:3000/api`

---

## Authentication

All API routes under `/api/protected/*` require authentication.

**Headers**:
```http
Authorization: Bearer [session-token]
```

Session token obtained via Supabase Auth (stored in HTTP-only cookie).

---

## Endpoints

### POST /api/auth/login

**Description**: Authenticate user with email and password

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response** (200 OK):
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com"
  },
  "session": {
    "access_token": "eyJhbGc...",
    "refresh_token": "eyJhbGc..."
  }
}
```

**Errors**:
- `401 Unauthorized`: Invalid credentials
- `422 Unprocessable Entity`: Invalid email format
- `500 Internal Server Error`: Database error

---

### GET /api/protected/profile

**Description**: Get current user's profile

**Auth**: Required

**Response** (200 OK):
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "John Doe",
  "avatar_url": "https://...",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Errors**:
- `401 Unauthorized`: Not authenticated
- `404 Not Found`: Profile not found

---

[Continue for all API routes...]

---

## Error Format

All errors follow this format:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": {} // Optional additional context
  }
}
```

---

## Rate Limiting

- Rate limit: 100 requests per minute per IP
- Header: `X-RateLimit-Remaining`
- Exceeded: `429 Too Many Requests`

---

## Testing

Use the Postman collection: `/docs/postman-collection.json`

Or via curl:
```bash
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password"}'
```
```

**API.md Best Practices**:
- Document all routes (don't leave undocumented endpoints)
- Include example requests and responses (actual JSON)
- Document error codes and meanings
- Provide curl examples for testing

### 4. DEPLOYMENT.md

**Purpose**: Guide for deploying to production (Vercel)

**Structure**:
```markdown
# Deployment Guide

This guide covers deploying to Vercel (recommended) and manual deployment.

---

## Prerequisites

- Vercel account ([vercel.com](https://vercel.com))
- Supabase project (production instance)
- GitHub repository (for automatic deployments)

---

## Vercel Deployment (Recommended)

### Initial Setup

1. **Connect Repository**:
   - Visit [vercel.com/new](https://vercel.com/new)
   - Import your GitHub repository
   - Select framework preset: Next.js

2. **Configure Environment Variables**:
   ```
   NEXT_PUBLIC_SUPABASE_URL=https://[your-project].supabase.co
   NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=[your-anon-key]
   SUPABASE_SERVICE_ROLE_KEY=[your-service-role-key]
   ```

3. **Deploy**:
   - Click "Deploy"
   - Wait for build to complete (~2-3 minutes)
   - Visit your production URL

### Automatic Deployments

- **Production**: Push to `main` branch → automatic production deploy
- **Preview**: Open PR → automatic preview deploy
- **Rollback**: Vercel dashboard → Deployments → Rollback

### Custom Domain

1. Go to Vercel dashboard → Settings → Domains
2. Add your domain (e.g., `example.com`)
3. Configure DNS records (follow Vercel instructions)
4. SSL certificate auto-provisioned (Let's Encrypt)

---

## Database Migrations

**Production migrations** via Supabase CLI:

```bash
# Link to production project
supabase link --project-ref [your-project-ref]

# Push migrations
supabase db push
```

**Rollback** (if needed):
```bash
# Reset to specific migration
supabase db reset --version [migration-version]
```

---

## Environment-Specific Configuration

### Development
```bash
NEXT_PUBLIC_SUPABASE_URL=http://localhost:54321
```

### Staging
```bash
NEXT_PUBLIC_SUPABASE_URL=https://[staging-project].supabase.co
```

### Production
```bash
NEXT_PUBLIC_SUPABASE_URL=https://[production-project].supabase.co
```

---

## Monitoring

### Vercel Analytics
- Enabled by default
- View: Vercel dashboard → Analytics
- Tracks: Page views, Core Web Vitals, real user metrics

### Error Tracking
```bash
# Install Sentry (optional)
npm install @sentry/nextjs

# Configure in next.config.js
```

### Logs
- View: Vercel dashboard → Deployment → Runtime Logs
- Filter by severity (info, warn, error)

---

## Performance Optimization

### Build-Time Optimizations
- Static pages generated at build time (ISR)
- Image optimization via Next.js Image
- Font optimization via next/font

### Runtime Optimizations
- Edge functions for auth routes (low latency)
- CDN caching for static assets
- Response caching for API routes

---

## Security Checklist

- [ ] Environment variables set correctly (no secrets exposed)
- [ ] HTTPS enabled (automatic on Vercel)
- [ ] CORS configured correctly (not allow *)
- [ ] Rate limiting implemented
- [ ] Database RLS policies enabled
- [ ] Supabase service role key server-side only

---

## Rollback Procedure

If deployment breaks production:

1. **Immediate Rollback**:
   - Vercel dashboard → Deployments → Find last working deployment → Rollback

2. **Fix Issue**:
   - Revert commit locally
   - Push fix to main branch
   - New deployment triggered automatically

3. **Verify**:
   - Check production URL
   - Run smoke tests
   - Monitor error rates

---

## Manual Deployment (Alternative)

If not using Vercel:

```bash
# Build production bundle
npm run build

# Start production server
npm start

# Or export static site
npm run build && npx next export
```

Deploy `/out` directory to any static host (Netlify, Cloudflare Pages, AWS S3).

---

## Troubleshooting

### Issue: Build fails on Vercel
**Cause**: TypeScript errors or missing dependencies
**Solution**: Run `npm run build` locally first, fix errors, push fix

### Issue: Environment variables not working
**Cause**: Variables not prefixed with `NEXT_PUBLIC_` or not set in Vercel
**Solution**: Add to Vercel dashboard → Settings → Environment Variables, redeploy

### Issue: Database connection fails
**Cause**: Wrong Supabase URL or key
**Solution**: Verify environment variables match production project

---

## Post-Deployment

- [ ] Test production URL (all critical paths)
- [ ] Verify analytics tracking
- [ ] Check error logs (first 24 hours)
- [ ] Monitor performance metrics
- [ ] Set up uptime monitoring (UptimeRobot, Pingdom)

---

**Production URL**: [your-production-url]
**Staging URL**: [your-staging-url] (if applicable)
```

**DEPLOYMENT.md Best Practices**:
- Provide actual commands (not theory)
- Include troubleshooting for common issues
- Document rollback procedure (critical for production)
- Link to external tools (Vercel dashboard, Supabase console)

### 5. CHANGELOG.md Setup

**Purpose**: Track version history and changes

**Structure**:
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- [Nothing yet]

### Changed
- [Nothing yet]

### Fixed
- [Nothing yet]

---

## [1.0.0] - 2024-01-15

### Added
- Initial release
- User authentication (email/password)
- Dashboard with analytics
- Profile management
- Mobile-responsive design
- WCAG 2.1 AA accessibility compliance

### Security
- Rate limiting on auth routes
- Row Level Security (RLS) policies
- Secure session handling

---

## [0.1.0] - 2024-01-10

### Added
- Project setup with Next.js 14 and Supabase
- Basic authentication flow
- Landing page
- Testing infrastructure

---

[Unreleased]: https://github.com/username/repo/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/username/repo/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/username/repo/releases/tag/v0.1.0
```

**CHANGELOG.md Best Practices**:
- Update BEFORE each release (not after)
- Group changes by type (Added, Changed, Deprecated, Removed, Fixed, Security)
- Use semantic versioning (MAJOR.MINOR.PATCH)
- Link to release tags on GitHub

### 6. Component Documentation

**Option A: Inline Documentation** (for small projects):
```typescript
/**
 * LoginForm - User authentication form
 *
 * @component
 * @example
 * ```tsx
 * <LoginForm onSuccess={(user) => router.push('/dashboard')} />
 * ```
 *
 * @prop {Function} onSuccess - Called when login succeeds
 * @prop {Function} onError - Called when login fails
 */
export function LoginForm({
  onSuccess,
  onError
}: LoginFormProps) {
  // ...
}
```

**Option B: Storybook** (for component libraries):
```bash
# Install Storybook
npx storybook@latest init

# Create story
# components/auth/LoginForm.stories.tsx
```

For most projects, **inline documentation is sufficient**.

### 7. Documentation Validation

**Run doc-auditor agent** (optional):
```bash
# Validates documentation completeness
Task(doc-auditor, "Validate all documentation")
```

**Manual Checklist**:
- [ ] README.md exists and is complete
- [ ] CLAUDE.md exists with conventions and anti-patterns
- [ ] API.md exists (if API routes present)
- [ ] DEPLOYMENT.md exists with Vercel instructions
- [ ] CHANGELOG.md set up with initial version
- [ ] All commands in README.md tested (actually work)
- [ ] All links in documentation valid (no 404s)
- [ ] No TODO or placeholder text left in docs

---

## Quality Checks

### Pre-Deployment Documentation Checklist
- [ ] README.md complete (installation, usage, commands)
- [ ] CLAUDE.md complete (conventions, anti-patterns, common tasks)
- [ ] API.md complete (if applicable, all routes documented)
- [ ] DEPLOYMENT.md complete (Vercel setup, environment variables)
- [ ] CHANGELOG.md initialized with first version
- [ ] No placeholder text (TODO, FIXME, [Your Name])
- [ ] All commands tested (npm scripts, bash commands)
- [ ] All links valid (internal and external)

### Documentation Quality Standards
- [ ] Concise but complete (no fluff)
- [ ] Actionable (commands that work, not theory)
- [ ] Maintainable (easy to update)
- [ ] Searchable (clear headings, keywords)
- [ ] Accessible (no jargon without explanation)

---

## Outputs

### 1. README.md
**Location**: `/README.md`
**Target**: Developers (humans)
**Size**: <300 lines

### 2. CLAUDE.md
**Location**: `/CLAUDE.md`
**Target**: AI agents (Claude Code)
**Size**: <500 lines

### 3. API.md
**Location**: `/docs/API.md`
**Target**: Developers integrating with API
**Size**: Varies (50-200 lines per endpoint)

### 4. DEPLOYMENT.md
**Location**: `/docs/DEPLOYMENT.md`
**Target**: DevOps, deployment engineers
**Size**: ~200 lines

### 5. CHANGELOG.md
**Location**: `/CHANGELOG.md`
**Target**: All stakeholders
**Size**: Grows with each release

---

## Next Phase Handover

**Prerequisites for Deployment**:
- ✅ All documentation complete
- ✅ QA passed (Phase 7)
- ✅ No placeholder text in docs
- ✅ All commands tested and working
- ✅ Production readiness checklist complete

**Handover Context**:
- Complete documentation set
- Production deployment guide
- Known issues documented (from QA)
- Changelog initialized

**Next Steps**: Deploy to production following DEPLOYMENT.md

---

## Common Issues & Solutions

### Issue: README.md commands don't work
**Cause**: Commands not tested before documenting
**Solution**: Run every command in README.md locally, fix any errors

### Issue: Documentation out of sync with code
**Cause**: Code changed but docs not updated
**Solution**: Add "Update docs" to PR checklist, make docs changes in same PR as code

### Issue: CLAUDE.md too long (>500 lines)
**Cause**: Including implementation details instead of conventions
**Solution**: Move detailed explanations to separate docs, keep CLAUDE.md focused on conventions and anti-patterns

### Issue: API documentation missing endpoints
**Cause**: New routes added without updating API.md
**Solution**: Use doc-auditor agent to find undocumented routes, add to docs

---

## Success Criteria

- ✅ README.md complete with installation and usage
- ✅ CLAUDE.md complete with conventions and anti-patterns
- ✅ API.md complete (if applicable)
- ✅ DEPLOYMENT.md complete with Vercel guide
- ✅ CHANGELOG.md initialized
- ✅ All commands tested and working
- ✅ All links valid
- ✅ No placeholder text
- ✅ Documentation validated (manual or via doc-auditor)
- ✅ Ready for production deployment

---

## Evidence Requirements (Constitution Article II)

**All documentation MUST be tested**:
- **Commands**: Run every bash command in README.md, verify it works
- **Links**: Click every link, verify no 404s
- **Code examples**: Copy-paste examples, verify they compile and run
- **API requests**: Test every curl example, verify response matches documented format

**Example Good Evidence**:
"README.md installation commands tested (evidence: ran `npm install && npm run dev` on fresh clone, server started successfully on http://localhost:3000). All 12 commands in README.md verified working (evidence: test log in /tmp/readme-test.log)."

---

**This phase completes the Next.js project setup. The project is now documented and ready for production deployment.**
