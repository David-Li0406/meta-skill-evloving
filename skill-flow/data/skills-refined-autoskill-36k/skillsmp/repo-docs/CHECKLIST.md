# Documentation Quality Checklist

Validate documentation before considering it complete.

---

## Structure

- [ ] Document has descriptive title (`# Title`)
- [ ] Brief 1-2 sentence description after title
- [ ] Table of Contents for documents with >3 sections
- [ ] Horizontal rules (`---`) separate major sections
- [ ] Maximum 4 heading levels used (`#` to `####`)
- [ ] Bold text used instead of `#####` or `######`

## Content

- [ ] Purpose of document is clear in first paragraph
- [ ] Commands are copy-paste ready (tested)
- [ ] Configuration examples have inline comments
- [ ] Cross-references link to related documents
- [ ] Status indicators used consistently (✅ ⚠️ ❌ 📊)
- [ ] Tables used for structured data
- [ ] Code blocks specify language for syntax highlighting

## Technical Accuracy

- [ ] All commands tested and working
- [ ] Configuration examples validated
- [ ] Version numbers are current
- [ ] File paths verified to exist
- [ ] URLs tested and accessible
- [ ] Environment variables documented

## Visual Diagrams

- [ ] Architecture has at least one visual diagram
- [ ] Diagram source files (`.mmd`, `.dot`) committed with PNGs
- [ ] Diagrams use consistent color styling
- [ ] Rendering instructions provided in `docs/diagrams/README.md`
- [ ] Diagrams referenced with 📊 indicator

## Completeness by Document Type

### CLAUDE.md
- [ ] Project overview with current status
- [ ] Repository structure diagram
- [ ] Development commands (build, test, deploy)
- [ ] Key patterns explained
- [ ] Common issues documented
- [ ] Links to other documentation

### README.md
- [ ] Quick start section (< 5 steps to run)
- [ ] Feature list with status indicators
- [ ] Installation prerequisites listed
- [ ] Basic and advanced usage examples
- [ ] Configuration reference
- [ ] Links to detailed documentation

### ARCHITECTURE.md
- [ ] High-level system diagram (Mermaid)
- [ ] Component interaction sequence diagram
- [ ] Each component documented with:
  - Technology stack
  - Responsibilities
  - Key functions
  - Configuration
- [ ] Data models with field descriptions
- [ ] Deployment architecture section

### DESIGN_DECISIONS.md
- [ ] Axioms with rationale and anti-patterns
- [ ] Trade-offs table (pros/cons/mitigation)
- [ ] Evolution section tracking changes
- [ ] Version history for significant updates

### MONITORING.md
- [ ] Monitoring stack overview
- [ ] Metrics configuration with annotations
- [ ] Health endpoint documentation
- [ ] Dashboard descriptions with queries
- [ ] Alert definitions (critical and warning)
- [ ] Troubleshooting procedures

### AI_ONBOARDING.md
- [ ] Quick start reading order
- [ ] ASCII component diagram
- [ ] Key concepts explained with code
- [ ] Directory structure
- [ ] Common tasks with commands
- [ ] Gotchas and warnings
- [ ] Pre-change checklist

## Maintenance

- [ ] Version history for significant changes
- [ ] Evolution section for design changes
- [ ] Troubleshooting section included
- [ ] Common issues documented with solutions
- [ ] Last updated date (if applicable)

---

## Quick Validation Commands

```bash
# Check all required Tier 1 docs exist
for doc in CLAUDE.md README.md docs/ARCHITECTURE.md docs/DESIGN_DECISIONS.md; do
  [ -f "$doc" ] && echo "✅ $doc" || echo "❌ $doc missing"
done

# Check for Table of Contents in large docs
for doc in docs/*.md; do
  lines=$(wc -l < "$doc")
  if [ "$lines" -gt 100 ]; then
    grep -q "## Table of Contents" "$doc" && \
      echo "✅ $doc has TOC" || \
      echo "⚠️ $doc ($lines lines) missing TOC"
  fi
done

# Find docs without code blocks (might need examples)
for doc in docs/*.md; do
  grep -q '```' "$doc" || echo "⚠️ $doc has no code blocks"
done

# Check for broken internal links
grep -roh '\[.*\](.*\.md)' docs/ | \
  sed 's/.*(\(.*\))/\1/' | \
  while read link; do
    [ -f "docs/$link" ] || [ -f "$link" ] || echo "❌ Broken link: $link"
  done
```

---

## Common Issues

| Issue | Check | Fix |
|-------|-------|-----|
| Commands don't work | Test in fresh environment | Update commands, add prerequisites |
| Outdated version numbers | Compare with package.json/go.mod | Update all version references |
| Broken internal links | Run link checker | Fix paths or update references |
| Missing diagrams | Check docs/diagrams/ | Create and render diagrams |
| Inconsistent status indicators | Search for ✅⚠️❌ | Standardize usage |
| No code examples | Check for ``` blocks | Add copy-paste examples |
| Deep heading nesting | Search for ##### | Convert to bold text |

---

## Pre-Commit Checklist

Before committing documentation changes:

- [ ] Spell check completed
- [ ] All links tested
- [ ] Code examples syntax highlighted
- [ ] Diagrams rendered and committed
- [ ] Related documents cross-referenced
- [ ] Version/date updated if applicable
- [ ] Reviewed by at least one team member
