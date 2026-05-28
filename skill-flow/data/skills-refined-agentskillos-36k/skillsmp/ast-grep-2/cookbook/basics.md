# Basics Cookbook

Read-only recipes for fast code exploration.

---

## Find call sites

**Problem**: Find all `console.log` calls in TS.

**Solution**:
```bash
sg -p 'console.log($$$)' -l ts src
```

**Tip**: Use `--files-with-matches` for quick file list.

---

## Find a pattern across repo

**Problem**: Find `if ($A) { $B }` patterns in JS.

**Solution**:
```bash
sg -p 'if ($A) { $B }' -l js .
```

**Tip**: Add `-C 2` for context.

---

## Find function declarations

**Problem**: List JS/TS function declarations.

**Solution**:
```bash
sg -p 'function $NAME($$$) { $$$ }' -l ts src
```

**Tip**: Use `--files-with-matches` for a fast index.

---

## Find Python defs

**Problem**: Find Python function definitions.

**Solution**:
```bash
sg -p 'def $NAME($$$): $$$' -l py src
```

**Tip**: Use `-C 1` to see the signature context.

---

## Stream JSON to other tools

**Problem**: Pipe matches to another script.

**Solution**:
```bash
sg -p 'new $TYPE($$$)' -l ts --json=stream src
```

**Tip**: `--json=stream` is one JSON object per line.

---

## Use stdin safely

**Problem**: Search a snippet from stdin.

**Solution**:
```bash
cat snippet.ts | sg -p 'await $CALL($$$)' -l ts --stdin
```

**Tip**: `--lang` is required for stdin.
