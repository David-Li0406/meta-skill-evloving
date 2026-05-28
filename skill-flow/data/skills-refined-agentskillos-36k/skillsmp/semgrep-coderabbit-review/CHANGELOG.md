# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-22

### Added

- **OpenCode Skill:** Two-stage code review workflow
- **Skill Documentation:** `SKILL.md` with comprehensive guidance
- **README:** Quick start guide and common issues
- **Focus Areas:** Security, API, database, web, and comprehensive review modes
- **Checklists:** Per-layer verification checklists
- **Common Issues:** 15+ security, architecture, and code quality patterns with fixes
- **Workflow Guide:** Stage 1 (Semgrep) → Stage 2 (CodeRabbit) → Fix → Verify
- **Troubleshooting:** Solutions for common issues
- **Related Resources:** Links to plugin, documentation, and tools
- MIT License

### Features

- 🚀 Two-stage workflow for comprehensive code review
- ⚡ 10-20 second pattern detection with Semgrep
- 🤖 AI-powered semantic analysis with CodeRabbit
- 🎯 Focused review areas (security, API, database, web)
- ✅ Layer-specific checklists (API, database, web, types)
- 📊 Priority levels with clear guidance
- 📝 Common issues with ready-to-use fixes
- ⚙️ Configurable focus areas

### Dependencies

- Requires: `opencode-semgrep-coderabbit-plugin >= 1.0.0`
- Peer tools: Semgrep CLI, CodeRabbit CLI

### Integration

- Works with Running Days project conventions
- Aligns with AGENTS.md standards
- Repository Pattern validation
- Svelte 5 runes compliance
- Oracle database best practices

---

## Planning & Roadmap

### Potential Future Enhancements

- [ ] Additional focus areas (performance, accessibility, documentation)
- [ ] Integration with GitHub Actions CI/CD
- [ ] Historical trend analysis and metrics
- [ ] Custom rule templates for projects
- [ ] Multi-language support
- [ ] Parallel review execution
- [ ] Review result caching
- [ ] Performance profiling
- [ ] Team best practices guide

---

**Repository:** https://github.com/acedergren/opencode-semgrep-coderabbit-skill  
**Author:** Alexander Cedergren  
**License:** MIT  
**Version:** 1.0.0  
**Status:** Production Ready
