# verification methods

advanced techniques for verifying AGENTS.md accuracy.

## file counting

### basic count

```bash
fd -e ts -e tsx . directory | wc -l
```

### separate source from tests

```bash
# total
total=$(fd -e ts -e tsx . dir | wc -l | tr -d ' ')

# tests (multiple patterns)
tests=$(fd -e ts -e tsx . dir | grep -E '\.(test|spec)\.' | wc -l | tr -d ' ')

# source
source=$((total - tests))

echo "total: $total, tests: $tests, source: $source"
```

### exclude generated

```bash
fd -e ts -e tsx . dir | grep -v '_generated' | grep -v '.d.ts' | wc -l
```

## export verification

### function exists

```bash
rg "export (function|const) functionName" dir --type ts
```

### type exists

```bash
rg "export (type|interface) TypeName" dir --type ts
```

### class exists

```bash
rg "export class ClassName" dir --type ts
```

### re-export exists

```bash
rg "export \{ functionName \}" dir --type ts
rg "export \* from" dir --type ts
```

## pattern usage

### count usages

```bash
rg "patternName" dir --type ts --count
```

### find files using pattern

```bash
rg "patternName" dir --type ts -l
```

### verify import path works

```bash
# check the file exists at the documented path
test -f "src/lib/utils.ts" && echo "exists" || echo "missing"
```

## symlink verification

### check is symlink

```bash
test -L path/CLAUDE.md && echo "is symlink" || echo "is file"
```

### check target

```bash
readlink path/CLAUDE.md
# should output: AGENTS.md
```

### verify target exists

```bash
target=$(readlink path/CLAUDE.md)
test -f "$(dirname path/CLAUDE.md)/$target" && echo "valid" || echo "broken"
```

## change detection

### files changed since date

```bash
git log --since="7 days ago" --name-only --pretty=format: | sort -u
```

### files changed in directory

```bash
git log --since="7 days ago" --name-only --pretty=format: | grep "^src/auth/"
```

### AGENTS.md last modified

```bash
git log -1 --format="%ar" -- path/AGENTS.md
# outputs: "3 days ago"
```

### check for drift

```bash
# files changed more recently than AGENTS.md
agents_mtime=$(git log -1 --format="%ct" -- dir/AGENTS.md)
git log --since="@$agents_mtime" --name-only --pretty=format: | grep "^dir/" | grep -E '\.(ts|tsx)$'
```

## bulk verification

### all AGENTS.md files

```bash
fd "^AGENTS\.md$" . --type f | while read f; do
  dir=$(dirname "$f")
  count=$(fd -e ts -e tsx . "$dir" -d 1 2>/dev/null | wc -l | tr -d ' ')
  echo "$f: $count files"
done
```

### orphaned CLAUDE.md (no AGENTS.md sibling)

```bash
fd "^CLAUDE\.md$" . --type f | while read f; do
  dir=$(dirname "$f")
  test -f "$dir/AGENTS.md" || echo "orphan: $f"
done
```
