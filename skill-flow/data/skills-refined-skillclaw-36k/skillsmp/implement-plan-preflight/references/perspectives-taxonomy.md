**Skill**: [Implement Plan Preflight](../SKILL.md)

# Perspectives Taxonomy (11 Types)

Use `perspectives` in ADR frontmatter to describe how the ADR relates to the broader ecosystem.

## Taxonomy Table

| Perspective                   | Description                                          | Example Use Case                         |
| ----------------------------- | ---------------------------------------------------- | ---------------------------------------- |
| `ProviderToOtherComponents`   | Creating something for others to consume             | Building a shared library or API         |
| `HostPlatformForContributors` | Building a framework others contribute to            | Plugin system, extension architecture    |
| `StandaloneComponent`         | Self-contained exploration, no external dependencies | Proof of concept, isolated experiment    |
| `UpstreamIntegration`         | Consuming external frameworks/infrastructure         | Integrating third-party API or SDK       |
| `BoundaryInterface`           | Public APIs, adapters, contract definitions          | REST API design, GraphQL schema          |
| `OperationalService`          | Runtime, SRE, observability concerns                 | Monitoring setup, alerting configuration |
| `SecurityBoundary`            | Security, compliance, threat modeling                | Auth implementation, data encryption     |
| `ProductFeature`              | User-facing value, UX decisions                      | New feature for end users                |
| `EcosystemArtifact`           | SDK, templates, reference implementations            | CLI tool, starter template               |
| `LifecycleMigration`          | Versioning, deprecation, migration strategies        | Database migration, API version bump     |
| `OwnershipGovernance`         | Organizational, process, ownership decisions         | Team ownership, code review policy       |

---

## Usage in Frontmatter

```yaml
---
perspectives: [UpstreamIntegration, BoundaryInterface]
---
```

Multiple perspectives can apply to a single ADR.

---

## Selection Guide

### When to Use Each Perspective

**ProviderToOtherComponents**

- Building shared utilities consumed by multiple projects
- Creating internal libraries or packages
- Designing reusable components

**HostPlatformForContributors**

- Designing plugin/extension systems
- Building platforms that accept external contributions
- Framework development

**StandaloneComponent**

- Isolated experiments or proofs of concept
- Self-contained scripts or tools
- No integration with existing systems

**UpstreamIntegration**

- Consuming third-party APIs (Stripe, AWS, etc.)
- Integrating with external databases
- Using external SDKs or libraries

**BoundaryInterface**

- Designing public APIs
- Contract-first development
- Adapter patterns between systems

**OperationalService**

- Monitoring and alerting setup
- Log aggregation configuration
- SRE and DevOps concerns

**SecurityBoundary**

- Authentication/authorization changes
- Data encryption decisions
- Compliance requirements (GDPR, SOC2)

**ProductFeature**

- User-facing functionality
- UX/UI decisions
- Feature flags and rollout strategies

**EcosystemArtifact**

- CLI tools for developers
- Starter templates and boilerplates
- Reference implementations

**LifecycleMigration**

- Database schema migrations
- API versioning strategies
- Deprecation timelines

**OwnershipGovernance**

- Team ownership boundaries
- Code review policies
- Process changes

---

## Related Repos Reference

When perspective implies external dependencies, reference related repos in ADR body:

```markdown
## References

- [Upstream: github.com/Eon-Labs/alpha-forge](https://github.com/Eon-Labs/alpha-forge) (UpstreamIntegration)
- [Consumer: github.com/Eon-Labs/trading-bot](https://github.com/Eon-Labs/trading-bot) (ProviderToOtherComponents)
```

**Always use public GitHub URLs, never local paths.**
