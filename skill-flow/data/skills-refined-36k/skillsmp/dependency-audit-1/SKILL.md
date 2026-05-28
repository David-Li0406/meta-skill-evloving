---
name: dependency-audit
description: Audit npm dependencies for security vulnerabilities, outdated packages, unused deps, license compliance, and bundle impact. Use regularly for security hygiene, before major releases, or when bundle size grows unexpectedly.
---

# Dependency Audit

Comprehensive audit of project dependencies for security, maintenance, and efficiency.

## Scope

### 1. Security Vulnerabilities
- Run `npm audit` for known vulnerabilities
- Check severity levels (critical, high, medium, low)
- Identify transitive dependency risks
- Review Dependabot/security advisories if available

### 2. Outdated Packages
- Compare current vs latest versions
- Identify packages with major version gaps
- Check for deprecated packages
- Review changelogs for breaking changes

### 3. Unused Dependencies
- Dependencies in package.json not imported anywhere
- devDependencies that should be dependencies (or vice versa)
- Duplicate functionality (multiple packages doing same thing)
- Per AGENTS.md: "Remove unused deps promptly"

### 4. License Compliance
- Identify licenses of all dependencies
- Flag copyleft licenses (GPL, AGPL) if problematic
- Check for license compatibility
- Document any commercial license requirements

### 5. Bundle Impact Analysis
- Large dependencies affecting client bundle
- Dependencies that should be dynamically imported
- Server-only packages accidentally in client bundle
- Tree-shaking effectiveness

### 6. Supply Chain Risk
- Packages with very few maintainers
- Packages with no recent updates (abandoned)
- Packages with suspicious update patterns
- Typosquatting risks

### 7. Core Dependency Health (project-specific)
Check health of key dependencies:
- **Next.js** - Framework updates, security patches
- **Drizzle ORM** - Database layer stability
- **Supabase client** - Auth/storage compatibility
- **TanStack Query** - Caching layer
- **Radix UI / shadcn** - Component primitives
- **TipTap** - Rich text editor
- **dnd-kit** - Drag and drop
- **date-fns** - Date handling
- **Zod** - Validation schemas

## Actions

1. Run `npm audit` and capture output
2. Run `npm outdated` to list version gaps
3. Search for unused imports with grep patterns
4. Check `package.json` against actual imports
5. Analyze bundle with build output

## Output Format

### Security Findings
```
[SEVERITY: CRITICAL|HIGH|MEDIUM|LOW]
Package: package-name@version
Vulnerability: CVE or advisory ID
Description: What the vulnerability allows
Fix: Upgrade path or mitigation
```

### Outdated Packages
```
Package: package-name
Current: x.y.z
Latest: a.b.c
Risk: Breaking changes likelihood
Action: Upgrade/Hold/Investigate
```

### Unused Dependencies
```
Package: package-name
Type: dependency|devDependency
Evidence: Not found in codebase
Action: Remove from package.json
```

### Bundle Impact
```
Package: package-name
Size: XXkB (gzipped)
Location: client|server|both
Issue: Should be server-only / dynamically imported
```

## Dependency Management Rules (from AGENTS.md)

- Install via `npm install <package>@latest`
- Record rationale in PRs
- Remove unused deps promptly
- Do not edit `package.json` or lockfiles directly (use CLI)

## Post-Audit

Generate:
- Security remediation priority list
- Safe upgrade commands
- Packages to remove
- Bundle optimization opportunities
- Maintenance risk assessment
