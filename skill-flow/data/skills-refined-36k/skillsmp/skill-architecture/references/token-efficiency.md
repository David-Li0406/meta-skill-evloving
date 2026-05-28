**Skill**: [Skill Architecture](../SKILL.md)

## Part 2: How Agent Skills Work (Token Efficiency)

### Progressive Disclosure Model

Agent Skills use a **three-tier loading system** to minimize token consumption:

1. **Metadata only** (30-50 tokens): Name + description loaded in system prompt for discovery
1. **SKILL.md content**: Loaded only when Agent Skill is relevant to current task
1. **Referenced files**: Loaded on-demand when explicitly referenced

**Result**: Unlimited Agent Skills possible without bloating context window. Each Agent Skill costs only 30-50 tokens until activated.

### Optimization Strategies

**Split large Agent Skills**:

- Keep mutually exclusive content in separate files
- Example: Put API v1 docs in `reference-v1.md`, API v2 in `reference-v2.md`
- Claude loads only the relevant version

**Reference files properly**:

```markdown
For authentication details, see reference.md section "OAuth Flow".
For examples, consult examples.md.
```

---
