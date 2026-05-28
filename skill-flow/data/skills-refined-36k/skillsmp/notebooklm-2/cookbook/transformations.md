# Transformations Cookbook

---

## Summarize sources

**Problem**: Summarize specific sources within a notebook.

**Solution**:
```bash
nlm summarize <notebook-id> <source-id-1> <source-id-2>
```

**Tip**: Ask the user which sources to include.

---

## Explain concepts from sources

**Problem**: Ask for explanations based on selected sources.

**Solution**:
```bash
nlm explain <notebook-id> <source-id-1> <source-id-2>
```

**Tip**: Use `nlm sources <notebook-id>` to fetch source IDs.

---

## Generate a study guide

**Problem**: Turn sources into a study guide.

**Solution**:
```bash
nlm study-guide <notebook-id> <source-id-1> <source-id-2>
```

**Tip**: For structured outputs, also try `outline`, `faq`, `briefing-doc`, `timeline`, or `toc`.
