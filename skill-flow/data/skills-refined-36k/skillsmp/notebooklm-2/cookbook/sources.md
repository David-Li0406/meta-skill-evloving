# Sources Cookbook

---

## List sources for a notebook

**Problem**: See what sources a notebook has.

**Solution**:
```bash
nlm sources <notebook-id>
```

**Tip**: If the user just said “my knowledge base,” ask them which notebook ID to use.

---

## Add a URL or file as a source

**Problem**: Add new material to a notebook.

**Solution**:
```bash
nlm add <notebook-id> https://example.com/article
nlm add <notebook-id> /path/to/file.pdf
```

**Tip**: For stdin, use `-` as the input path.

---

## Remove a source (destructive)

**Problem**: Remove an outdated source.

**Solution**:
```bash
nlm rm-source <notebook-id> <source-id>
```

**Tip**: Always confirm before running this.
