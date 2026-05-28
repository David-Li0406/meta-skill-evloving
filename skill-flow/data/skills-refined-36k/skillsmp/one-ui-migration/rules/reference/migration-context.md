# MXsecurity Migration Context

This guide assists with migrating the MXsecurity project from Angular 16 to Angular 20 in the one-ui monorepo.

## 🎯 Migration Context

**Source Project**: `/Users/jayden/f2e-networking-jayden/apps/mxsecurity-web` (Angular 16)
**Target Project**: `/Users/jayden/one-ui/apps/mxsecurity/mxsecurity` (Angular 20)

## 🎯 Migration Workflow

1. **Analyze old component** in `/Users/jayden/f2e-networking-jayden/apps/mxsecurity-web`
2. **Identify domain concepts** - What business logic, API calls, state?
3. **Create library structure** - domain, features, ui, shell as needed
4. **Migrate in layers**:
   - API types → `shared/api`
   - Services → `domain/`
   - State → `domain/` (SignalStore)
   - Smart components → `features/`
   - Dumb components → `ui/`
   - Routes → `shell/`
5. **Update syntax** - Use checklist above
6. **Test and verify** - Type check, lint, build

## 🔧 Nx Commands

```bash
# Create new library (use script for consistency)
./scripts/nx-generate-lib.sh --scope mxsecurity --domain-name my-feature --type domain

# Type check
npx tsc --noEmit --project libs/mxsecurity/[feature]/tsconfig.lib.json

# Lint
nx lint mxsecurity-[feature]-[type]

# Build
nx build mxsecurity
```

## 📞 Getting Help

When stuck:

1. Check this guide first
2. Look at reference projects in `libs/switch/`
3. Use Context7 to query latest Angular docs
4. Review `/Users/jayden/one-ui/CLAUDE.md` for general patterns
5. Check old implementation in `/Users/jayden/f2e-networking-jayden/apps/mxsecurity-web`

---

**Remember**: Always use Angular 20 syntax, standalone components, signals, the SignalStore pattern, and **OneValidators** for form validation. Migration is about modernizing, not just copying old code.
