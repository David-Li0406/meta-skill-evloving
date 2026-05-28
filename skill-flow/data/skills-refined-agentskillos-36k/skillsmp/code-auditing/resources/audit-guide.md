# Audit Guide (Scanning Protocols)

> High-performance grep patterns for auditing.

## 1. Performance & Logic
```bash
# O(n^2) Loops
grep -rn "forEach.*forEach\|\.map(.*\.map(\|for.*for" --include="*.ts*"

# useEffect Missing Deps (heuristic)
grep -rn "useEffect(() =>" --include="*.tsx"
```

## 2. Design System Violations
```bash
# Hardcoded Colors
grep -rn "#[0-9a-fA-F]\{3,6\}\|rgb(\|rgba(" --include="*.css" --include="*.tsx"

# @apply Misuse
grep -rn "@apply" --include="*.css"
```

## 3. Architecture Violations
```bash
# Zustand Destructuring
grep -rn "const {.*} = use.*Store()" --include="*.tsx"

# Any Type
grep -rn ": any\|as any" --include="*.ts*"
```
