# Design Ops FAQ

Frequently asked questions about Design Ops v2.0.

---

## General

### What is Design Ops?

A methodology that combines research-driven design with AI-execution optimization. It bridges the gap between human intent and reliable implementation through validated specs and AI-executable PRPs.

### What's new in v2.0?

- 43 invariants for spec validation
- Automated PRP generation
- Confidence scoring (1-10)
- Implementation review
- CONVENTIONS.md generator

### Do I need to use all the features?

No. Start with `/design validate` and `/design prp`. Add other features as needed.

---

## Validation

### Why did my spec fail validation?

The validator found ambiguous or incomplete content. Check the violation message:
- Line number tells you where
- "Fix" message tells you how

### What are invariants?

Non-negotiable principles specs must satisfy. Like type checking for human intent.

### Which invariants apply to my project?

- Universal (1-10): Always apply
- Domain-specific (11-43): Use `--domain` flag

### Can I ignore warnings?

Warnings don't block PRP generation, but address them before production. They indicate potential issues.

### How do I fix "Ambiguity is Invalid"?

Replace vague terms with specific criteria:
- ❌ "fast", "efficient", "proper"
- ✅ "< 200ms", "< 50MB", "validates schema"

### How do I fix "State Must Be Explicit"?

Use → notation for state transitions:
- ❌ "update user preferences"
- ✅ `prefs={} → set_theme(dark) → prefs={theme:dark}`

### How do I fix "Scope Must Be Bounded"?

Add limits to unbounded terms:
- ❌ "process all records"
- ✅ "process records (max 1000, batch_size 100)"

---

## PRP Generation

### What is a PRP?

Product Requirements Prompt - an AI-executable blueprint generated from a validated spec. Think of it as "compiled" human intent.

### How do I generate a PRP?

```bash
/design prp specs/S-001-feature.md
```

### What if PRP generation fails?

1. Check that spec passed validation
2. Ensure templates exist
3. Check output path is writable

### Can I customize the PRP template?

Yes. Edit `templates/prp-base.md` or create domain-specific templates.

### How do I improve PRP quality score?

- Fill all required sections
- Add measurable success criteria
- Include validation commands
- Document risk mitigation

---

## Confidence Scoring

### What does the confidence score mean?

How likely implementation will succeed without surprises:
- 8-10: High confidence, proceed
- 5-7: Medium, expect iteration
- 1-4: Low, more research needed

### How is confidence calculated?

Five factors:
- Requirement clarity (30%)
- Pattern availability (25%)
- Test coverage plan (20%)
- Edge case handling (15%)
- Tech familiarity (10%)

### What should I do with low confidence?

1. Add detail to unclear requirements
2. Find similar patterns in codebase
3. Research unfamiliar technology
4. Document edge cases

### Can I proceed with low confidence?

You can, but expect problems. Low confidence is an early warning system.

---

## Implementation Review

### What does /design review check?

- Requirements coverage (% implemented)
- Validation command results
- Convention compliance
- Test coverage
- Error handling presence

### When should I run review?

After implementation, before shipping. It verifies code matches design.

### What if review shows gaps?

Fix them. The review tells you exactly what's missing.

---

## Workflow

### What's the recommended workflow?

1. Research → 2. Constraints → 3. Journeys → 4. Specs → 5. Validate → 6. PRP → 7. Implement → 8. Review → 9. Retrospective

### Do I need to follow the full workflow?

For new features, yes. For bug fixes, you might just validate + implement.

### How does this integrate with existing processes?

Design Ops enhances your workflow, doesn't replace it. Use validation and PRP generation where they add value.

---

## CONVENTIONS.md

### What is CONVENTIONS.md?

A document describing your codebase's patterns (naming, structure, error handling). Specs reference it for consistency.

### How do I generate it?

```bash
./tools/conventions-generator.sh /path/to/codebase
```

### Should I edit the generated file?

Yes. The generator extracts patterns, but you should add team-specific conventions and clean up false detections.

---

## Domains

### What domains are available?

1. Consumer Product (11-15)
2. Physical Construction (16-21)
3. Data Architecture (22-26)
4. Integration (27-30)
5. Remote Management (31-36)
6. Skill Gap Transcendence (37-43)

### How do I use a domain?

```bash
/design validate spec.md --domain domains/consumer-product.md
```

### Can I combine domains?

Not directly, but universal invariants always apply with any domain.

### Can I create custom domains?

Yes. Copy an existing domain file and customize the invariants.

---

## Troubleshooting

### Scripts not found

```bash
chmod +x enforcement/*.sh tools/*.sh
```

### Validation too strict

The strictness is intentional. If you're getting false positives, check:
- Are you using HTML comments? They're skipped.
- Is the pattern in a code block? Might be detected.

### PRP quality score low

Check prp-checker output for specific issues:
- Missing required sections
- Unfilled placeholders
- No validation gates

### Integration tests fail

Run tests individually to isolate the issue:
```bash
./validator.sh test-spec.md
./spec-to-prp.sh test-spec.md
./prp-checker.sh output.md
```

---

## Best Practices

### How detailed should specs be?

Detailed enough that:
- An AI agent could implement without asking questions
- Success can be objectively measured
- Edge cases are documented

### How often should I validate?

Every time you update a spec. Set up pre-commit hooks for automation.

### Should I version specs?

Yes. Use version numbers and keep history. Specs are living documents.

### How do I handle changing requirements?

1. Update the spec
2. Re-validate
3. Re-generate PRP if major changes
4. Document in spec-delta if learnings

---

## Getting Help

### Where can I report issues?

Create an issue in the repository.

### How do I contribute?

1. Fork the repository
2. Create a feature branch
3. Follow the spec validation rules
4. Submit a PR with tests

---

*More questions? Check TROUBLESHOOTING.md or ask in the community.*
