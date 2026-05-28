# Troubleshooting Guide

Solutions for common Design Ops issues.

---

## Installation Issues

### "Permission denied" running scripts

**Problem**: Scripts won't execute.

**Solution**:
```bash
chmod +x enforcement/*.sh
chmod +x tools/*.sh
```

### "Command not found: bc"

**Problem**: Confidence calculator needs `bc` for calculations.

**Solution**:
```bash
# macOS
brew install bc

# Ubuntu/Debian
sudo apt-get install bc
```

### Scripts fail with path errors

**Problem**: Paths with spaces cause issues.

**Solution**: The scripts handle this. If issues persist, try:
```bash
# Quote paths
"$SCRIPT_DIR/validator.sh" "path/with spaces/spec.md"
```

---

## Validation Issues

### False positive: HTML comments trigger violations

**Problem**: `<!-- comment -->` content triggers invariants.

**Solution**: This is now fixed. HTML comments are skipped. If still occurring, update your validator.sh.

### "Ambiguity is Invalid" on technical terms

**Problem**: Words like "process", "handle" trigger violations.

**Solution**: The validator looks for vague terms without context. Fix by adding specifics:
```markdown
# Bad
Process user input

# Good
Process user input: validate_schema → sanitize_html → store_db
```

### "State Must Be Explicit" on descriptions

**Problem**: Narrative text triggers state violations.

**Solution**: Use → notation for actual state changes:
```markdown
# Bad
Users update their preferences

# Good
user.prefs → update_theme(dark) → user.prefs{theme: dark}
```

### Invariant triggers on code blocks

**Problem**: Code examples trigger validation.

**Solution**: Code blocks are partially excluded. If issues persist:
1. Use fenced code blocks (```)
2. Avoid violation patterns in example code

### Too many warnings

**Problem**: Valid spec has many warnings.

**Solution**: Warnings don't block generation. Address them by:
1. Adding fallback strategies for external dependencies
2. Defining degradation paths
3. Adding explicit bounds

---

## PRP Generation Issues

### "Spec has violations. Cannot generate PRP"

**Problem**: Spec failed validation.

**Solution**:
1. Run `/design validate spec.md`
2. Fix each violation
3. Re-run validation until pass
4. Then generate PRP

### PRP missing sections

**Problem**: Generated PRP incomplete.

**Solution**:
1. Check template exists: `templates/prp-base.md`
2. Verify spec has enough content to extract
3. Fill `[FILL_THIS_IN]` placeholders manually

### Low quality score

**Problem**: prp-checker gives low score.

**Solution**: Check the specific warnings:
- Missing required sections? Add them
- Vague success criteria? Add metrics
- No validation gates? Add pass/fail criteria

### Wrong template selected

**Problem**: Auto-detection picks wrong template.

**Solution**: Specify template explicitly:
```bash
./spec-to-prp.sh spec.md --template api-integration
```

---

## Confidence Calculator Issues

### "syntax error in expression"

**Problem**: bc calculation fails.

**Solution**: Ensure inputs are decimal (0.0-1.0):
```bash
# Bad
./confidence-calculator.sh 9 8 7 6 9

# Good
./confidence-calculator.sh 0.9 0.8 0.7 0.6 0.9
```

### Score always 0

**Problem**: Calculator returns 0/10.

**Solution**: Check inputs are valid decimals between 0.0 and 1.0.

---

## Review Issues

### "Spec file not found"

**Problem**: Review can't find the spec.

**Solution**: Use absolute path or path relative to current directory:
```bash
/design review ./specs/S-001.md ./src/feature/
```

### Low coverage reported

**Problem**: Review shows low requirements coverage.

**Solution**:
1. Check spec requirements against implementation
2. Some requirements may need different file paths
3. Coverage is based on keyword matching - review manually

---

## Integration Test Issues

### Tests fail on fresh install

**Problem**: Integration tests fail immediately.

**Solution**:
1. Ensure all scripts are executable
2. Check test-spec.md exists
3. Run pre-flight checks:
```bash
ls -la enforcement/*.sh
```

### Test spec has violations

**Problem**: test-spec.md fails validation.

**Solution**: The test spec is designed to pass. If it fails:
1. Check validator.sh is latest version
2. Run validator manually to see specific issues
3. Update test-spec.md to fix any new violations

---

## CI/CD Issues

### GitHub Action fails

**Problem**: validate-specs workflow fails.

**Solution**:
1. Check workflow file syntax: `.github/workflows/validate-specs.yml`
2. Ensure scripts are committed and executable
3. Check paths match your repository structure

### Pre-commit hook too slow

**Problem**: Hook takes too long.

**Solution**: The hook only validates staged .md files. If still slow:
1. Check for large files being validated
2. Consider skipping non-spec files:
```bash
# In pre-commit, add filter
if [[ ! "$file" =~ ^specs/ ]]; then
    continue
fi
```

---

## Common Error Messages

### "Core invariants file not found"

**Cause**: system-invariants.md missing.

**Fix**: Ensure `system-invariants.md` exists in the DesignOps root directory (same directory as `design.md`).

### "Domain file not found"

**Cause**: Specified domain doesn't exist.

**Fix**: Check domain path. Available domains in `domains/` directory.

### "Template file not found"

**Cause**: PRP template missing.

**Fix**: Ensure `templates/prp-base.md` exists.

### "Output directory does not exist"

**Cause**: Can't create output file.

**Fix**: Create directory or use existing path:
```bash
mkdir -p output/
./spec-to-prp.sh spec.md --output output/prp.md
```

---

## Performance Issues

### Validation slow on large specs

**Problem**: Large specs take too long.

**Solution**: Validator reads line-by-line. For very large specs:
1. Split into multiple specs
2. Optimize content (remove unnecessary sections)

### PRP generation slow

**Problem**: spec-to-prp.sh takes too long.

**Solution**:
1. Skip validation if already done: `--skip-validation`
2. Use simpler template
3. Reduce codebase scanning scope

---

## Getting More Help

### Debug mode

Add verbose output to see what's happening:
```bash
bash -x ./validator.sh spec.md
```

### Check versions

```bash
head -5 enforcement/validator.sh  # Shows version
```

### Reset to known state

If things are broken, re-download the latest scripts from the repository.

---

## Reporting Issues

When reporting bugs, include:
1. Script version (from file header)
2. Exact command run
3. Full error output
4. Spec content (if not sensitive)
5. Operating system

---

*Still stuck? Check FAQ.md or ask the community.*
