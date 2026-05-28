# Cheatsheet Skills Index

Quick reference guide for all cheatsheet skills in this directory.

## Total Skills: 42

### Cycle Patterns (7 skills)
1. **cycle-aware-nodes** - Cycle-aware node patterns with state preservation
2. **cycle-debugging** - Debugging and troubleshooting cycle issues
3. **cycle-testing** - Testing patterns for cyclic workflows
4. **cycle-state-persistence** - State persistence with field-specific mapping
5. **cycle-scenarios** - Real-world cycle scenarios (ETL, polling, quality)
6. **cyclic-patterns-advanced** - Advanced multi-node cycle patterns
7. **multi-path-cycles** - Multi-path conditional cycles with SwitchNode

### Database & SQL (4 skills)
8. **asyncsql-advanced** - Advanced AsyncSQL patterns for complex queries
9. **distributed-transactions** - Distributed transaction coordination
10. **saga-pattern** - Saga pattern for distributed workflows
11. **query-builder** - Query builder patterns for dynamic SQL
12. **query-routing** - Query routing for multi-database workflows

### Data Integration (4 skills)
13. **node-selection-guide** - Decision guide for choosing the right node (CRITICAL)
14. **data-integration** - Data integration patterns for APIs/files/databases
15. **integration-mastery** - Master integration patterns
16. **workflow-composition** - Composing workflows from reusable components

### Development & Debugging (2 skills)
17. **pythoncode-data-science** - PythonCodeNode for data science workflows
18. **developer-tools** - Advanced developer tools and debugging

### Production & Operations (7 skills)
19. **performance-optimization** - Performance optimization patterns
20. **production-readiness** - Production readiness checklist
21. **production-patterns** - Production workflow patterns
22. **resilience-patterns** - Resilience and fault tolerance patterns
23. **monitoring-alerting** - Monitoring and alerting patterns
24. **validation-testing** - Validation and testing patterns
25. **workflow-api-deployment** - Deploy workflows as REST APIs

### Security & Configuration (3 skills)
26. **security-config** - Security configuration and best practices
27. **env-variables** - Environment variable management
28. **multi-tenancy-patterns** - Multi-tenancy and access control

### Quick Reference (3 skills)
29. **admin-nodes-reference** - Admin and utility nodes reference
30. **kailash-quick-tips** - Essential tips and tricks
31. **common-mistakes-catalog** - Common mistakes to avoid

### Advanced Patterns (3 skills)
32. **workflow-design-process** - Systematic workflow design methodology
33. **node-initialization** - Node initialization and parameter patterns
34. **directoryreader-patterns** - DirectoryReader file discovery patterns

### MCP & Integration (2 skills)
35. **enterprise-mcp** - Enterprise MCP for large-scale deployments
36. **mcp-resource-subscriptions** - MCP resource subscription patterns

### Agent Coordination (1 skill)
37. **a2a-coordination** - Agent-to-Agent (A2A) coordination patterns

### Specialized Integration (2 skills)
38. **ollama-integration** - Ollama LLM integration patterns
39. **custom-node-guide** - Creating custom nodes

### Workflow Utilities (3 skills)
40. **workflow-patterns-library** - Common workflow patterns library
41. **workflow-export** - Exporting and sharing workflows
42. **visualization** - Workflow visualization patterns

## Quick Access by Category

### By Priority
- **HIGH**: All cycle skills, node-selection-guide, production patterns
- **MEDIUM**: Integration, database, MCP skills
- **REFERENCE**: Quick tips, admin nodes, common mistakes

### By Use Case
- **Getting Started**: kailash-quick-tips, workflow-patterns-library
- **Cyclic Workflows**: All cycle-* skills
- **Database Operations**: asyncsql-advanced, query-builder, saga-pattern
- **Production Deployment**: production-*, resilience-patterns, monitoring-alerting
- **Integration**: data-integration, integration-mastery, workflow-composition
- **Debugging**: cycle-debugging, developer-tools, common-mistakes-catalog

## Usage Patterns

### Trigger Keywords
Each skill includes trigger keywords in its frontmatter for automatic detection. Examples:
- "cycle debugging" → cycle-debugging.md
- "which node" → node-selection-guide.md
- "async SQL" → asyncsql-advanced.md
- "production ready" → production-readiness.md

### Related Skills
Skills are cross-referenced for easy navigation:
- Cycle skills link to each other
- Production skills link to monitoring and validation
- Integration skills link to data patterns

## File Structure

```
cheatsheets/
├── README.md (this file)
├── cycle-aware-nodes.md
├── cycle-debugging.md
├── cycle-testing.md
├── cycle-state-persistence.md
├── cycle-scenarios.md
├── cyclic-patterns-advanced.md
├── multi-path-cycles.md
├── asyncsql-advanced.md
├── distributed-transactions.md
├── saga-pattern.md
├── query-builder.md
├── query-routing.md
├── node-selection-guide.md
├── data-integration.md
├── integration-mastery.md
├── workflow-composition.md
├── pythoncode-data-science.md
├── developer-tools.md
├── performance-optimization.md
├── production-readiness.md
├── production-patterns.md
├── resilience-patterns.md
├── monitoring-alerting.md
├── validation-testing.md
├── admin-nodes-reference.md
├── workflow-design-process.md
├── node-initialization.md
├── directoryreader-patterns.md
├── enterprise-mcp.md
├── mcp-resource-subscriptions.md
├── a2a-coordination.md
├── ollama-integration.md
├── custom-node-guide.md
├── security-config.md
├── env-variables.md
├── multi-tenancy-patterns.md
├── kailash-quick-tips.md
├── common-mistakes-catalog.md
├── workflow-patterns-library.md
├── workflow-api-deployment.md
├── workflow-export.md
└── visualization.md
```

## Version History

### Phase 3 Batch 1 (v0.9.25+)
- Added 30 new skills
- Total: 42 skills
- Focus: Cycle patterns, database operations, production deployment

### Phases 1-2 (v0.9.24)
- Initial 12 skills
- Focus: Quick tips, common patterns, basic integration

## Contributing

When adding new skills:
1. Follow the standard template structure
2. Include clear trigger keywords
3. Add working code examples
4. Cross-reference related skills
5. Update this README

## Related Documentation
- **Source**: `/sdk-users/2-core-concepts/cheatsheet/`
- **Skills Directory**: `.claude/skills/3-patterns/cheatsheets/`
- **Taxonomy**: See skills taxonomy document for complete skill hierarchy
