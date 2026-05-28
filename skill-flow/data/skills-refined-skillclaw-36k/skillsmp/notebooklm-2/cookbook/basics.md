# Basics Cookbook

Practical recipes for common NotebookLM CLI tasks.

---

## List and choose a notebook

**Problem**: I need a notebook ID to work with.

**Solution**:
```bash
nlm list
```

**Tip**: Ask the user to pick one ID if multiple are shown.

---

## Ask a single question (headless)

**Problem**: Ask a notebook a one-off question without interactive mode.

**Solution**:
```bash
nlm generate-chat <notebook-id> "What are the key takeaways?"
```

**Tip**: Prefer `generate-chat` for scripted/CI usage.

---

## Start an interactive chat

**Problem**: Have a live back-and-forth with a notebook.

**Solution**:
```bash
nlm chat <notebook-id>
```

**Tip**: If it fails due to sources, retry with `-skip-sources`.
