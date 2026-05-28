# Troubleshooting Cookbook

---

## sg not found

**Problem**: `sg` command missing.

**Solution**:
```bash
ast-grep -p 'pattern' -l ts src
```

**Tip**: If not installed, use `nix run nixpkgs#ast-grep -- -p 'pattern' -l ts src`.

---

## No matches

**Problem**: Expected matches, got none.

**Solution**:
```bash
sg -p 'pattern' -l ts --debug-query=ast
```

**Tip**: Verify `--lang`, try `--strictness=relaxed`.

---

## Wrong language detection

**Problem**: Files parsed as wrong language.

**Solution**:
```bash
sg -p 'pattern' -l ts path/to/file
```

**Tip**: Force `--lang` for generated or unusual extensions.

---

## Too many matches

**Problem**: Pattern too broad.

**Solution**:
```bash
sg -p 'pattern' -l ts --selector identifier src
```

**Tip**: Add structure or use `--strictness=cst`.

---

## Slow search

**Problem**: Search takes too long.

**Solution**:
```bash
sg -p 'pattern' -l ts --globs 'src/**/*.ts' --threads 4 .
```

**Tip**: Limit paths, exclude large dirs with `--globs '!**/dist/**'`.

---

## Stdin errors

**Problem**: Stdin search fails.

**Solution**:
```bash
cat file.ts | sg -p 'pattern' -l ts --stdin
```

**Tip**: `--lang` required; interactive mode is incompatible with stdin.
