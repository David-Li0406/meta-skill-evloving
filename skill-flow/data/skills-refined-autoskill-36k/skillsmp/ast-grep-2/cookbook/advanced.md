# Advanced Cookbook

Higher-signal queries and scope control.

---

## Match a sub-node with selector

**Problem**: Match a call expression inside a larger pattern.

**Solution**:
```bash
sg -p 'if ($COND) { $BODY }' --selector call_expression -l ts src
```

**Tip**: Use `--debug-query=ast` to see node kinds.

---

## Debug pattern parsing

**Problem**: Pattern does not match; inspect structure.

**Solution**:
```bash
sg -p 'await $CALL($$$)' -l ts --debug-query=ast
```

**Tip**: Try `--debug-query=cst` when punctuation matters.

---

## Tighten or relax matching

**Problem**: Over-matching or under-matching.

**Solution**:
```bash
sg -p '$A && $A()' -l ts --strictness=ast src
```

**Tip**: `relaxed` ignores comments; `cst` is strict.

---

## Include/exclude with globs

**Problem**: Search only src TS, exclude tests.

**Solution**:
```bash
sg -p 'new $TYPE($$$)' -l ts --globs 'src/**/*.ts' --globs '!**/*.test.ts' .
```

**Tip**: Later globs override earlier ones.

---

## Narrow by file list

**Problem**: Restrict search to a known file set.

**Solution**:
```bash
rg -l "console\\.log" src | xargs sg -p 'console.log($$$)' -l ts
```

**Tip**: Use a cheap prefilter to cut parse cost.

---

## Compact JSON for scripts

**Problem**: Emit minimal JSON for tooling.

**Solution**:
```bash
sg -p 'new $TYPE($$$)' -l ts --json=compact src
```

**Tip**: Pair with `--files-with-matches` when you only need paths.
