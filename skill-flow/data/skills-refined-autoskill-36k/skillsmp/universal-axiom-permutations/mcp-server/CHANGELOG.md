# Changelog

All notable changes to the Universal Axiom MCP Server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.1] - 2026-01-23

### Security
- **CRITICAL**: Updated all Vercel dependencies to latest secure versions
  - `@vercel/node`: ^3.0.0 → ^5.5.27
  - `vercel`: ^37.0.0 → ^50.4.11
- **Added**: npm package overrides to enforce secure transitive dependencies
  - `path-to-regexp`: ^8.3.0 (fixes high severity regex backtracking vulnerability)
  - `tar`: ^7.5.6 (fixes high severity file overwrite vulnerability)
  - `undici`: ^7.19.0 (fixes moderate severity random value vulnerability)
- **Resolved**: All 17 security vulnerabilities - now at **0 vulnerabilities**

### Added
- `test:vercel` script to validate Vercel deployment configuration
- `test-vercel-config.js` - comprehensive deployment validation test
- Security section in VERCEL_DEPLOYMENT.md documentation
- Automated checks for:
  - Runtime version validation
  - Dependency version validation
  - Security vulnerability scanning
  - Build output verification

### Changed
- Updated `vercel.json` to use latest @vercel/node runtime (5.5.27)
- Enhanced deployment documentation with security information
- Improved package.json with test script for deployment validation

### Fixed
- Security vulnerabilities in Vercel deployment dependencies
- Build configuration for latest Vercel runtime
- Dependency tree to use only secure package versions

## [0.2.0] - 2026-01-17

### Added
- **compare_permutations**: Compare two system permutations across multiple criteria
- **optimize_system**: Get intelligent suggestions for improving system variables
- **predict_trajectory**: Forecast system evolution over future iterations
- **detect_collapse_risk**: Analyze collapse risk with severity levels and warnings
- Comprehensive test suite with 14 tests covering all tools
- Demo script showing analyze_permutation tool in action
- npm publication readiness (LICENSE, .npmignore, enhanced package.json)

### Changed
- Upgraded server version to 0.2.0
- Enhanced package.json with repository, homepage, and file specifications
- Improved TypeScript configuration to exclude test files from compilation

### Fixed
- TypeScript strict mode errors in optimization tool
- Build configuration for proper module compilation

## [0.1.0] - 2026-01-17

### Added
- Initial MCP server implementation
- 8 core tools:
  - **compute_intelligence**: Calculate intelligence using the axiom formula
  - **evolve_system**: Evolve systems forward in time
  - **apply_pressure**: Apply pressure changes to systems
  - **adjust_subjectivity**: Adjust objectivity/subjectivity levels
  - **simulate_evolution**: Simulate evolution over multiple steps
  - **simulate_contradiction_resolution**: Resolve contradictions through the axiom
  - **get_coherence_metric**: Measure system coherence
  - **analyze_permutation**: Get diagnostic analysis with recommendations
- 6 documentation resources accessible via axiom:// URIs
- 2 prompt templates (analyze_problem, reason_with_axiom)
- Full TypeScript implementation with type definitions
- Integration with The Universal Axiom core framework
- Example configuration for Claude Desktop
- Comprehensive README with setup instructions

### Technical Details
- Built on @modelcontextprotocol/sdk v1.0.4
- ES module architecture for modern JavaScript compatibility
- Stdio transport for MCP communication
- Observable, testable variables for transparency
- Multiplicative intelligence model based on natural laws

[0.2.0]: https://github.com/TheUniversalAxiom/pointy-stick/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/TheUniversalAxiom/pointy-stick/releases/tag/v0.1.0
