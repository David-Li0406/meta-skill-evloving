# Identifying AI-Induced Technical Debt

## The "Lazy AI" Syndrome
AI models often prioritize getting a feature to work over making it maintainable. This leads to specific types of debt.

---

### 1. Over-Specification (Comment Bloat)
AI often adds verbose comments for obvious code.
- **Debt**: "This line increments the counter." 
- **Elite Fix**: Code should be self-documenting. Use comments only for "Why," not "What."

### 2. "By-the-Book" Hallucinations
AI might use a pattern from a 2022 blog post that isn't idiomatic to your specific 2026 project.
- **Example**: Using `forwardRef` in React 19 when the project uses direct `ref` props.
- **Audit**: Verify every library usage against the current `package.json` versions.

### 3. Logic Fragmentation
AI might implement the same logic in 3 different files because it "forgot" the existing utility package.
- **Audit**: Use `codebase_investigator` to search for similar symbols before allowing new logic.

### 4. Excessive Error Handling (Paranoia)
Sometimes AI wraps everything in redundant `try/catch` blocks that swallow errors and make debugging impossible.
- **Fix**: Use global error boundaries and centralized logging.
