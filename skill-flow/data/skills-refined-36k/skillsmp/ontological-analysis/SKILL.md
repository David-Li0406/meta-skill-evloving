---
name: ontological-analysis
description: Analyze repository through 8 philosophical dimensions for MVV extraction
version: 1.0.0
author: Claude-Dev-eed7-001
---

# Ontological Analysis Skill

## Purpose

Performs deep philosophical analysis of a repository or codebase through 8 complementary dimensions derived from the ONTOLOGISTA framework. This analysis extracts the essential nature, purpose, and identity of a project to enable accurate Mission, Vision, and Values (MVV) synthesis.

The 8 dimensions provide a comprehensive ontological map that reveals not just what a project does, but WHY it exists, HOW it relates to its domain, and WHAT principles guide its evolution.

## When to Use

- Before generating Mission, Vision, and Values statements
- When onboarding to understand a new codebase deeply
- For strategic documentation requiring philosophical grounding
- When auditing project alignment with stated objectives
- During architecture reviews to validate design coherence
- When preparing executive summaries that require essence distillation

## Invocation Syntax

```
/ontological-analysis <target> [options]
```

### Targets

| Target | Description | Example |
|--------|-------------|---------|
| `repo` | Analyze entire repository | `/ontological-analysis repo` |
| `module <path>` | Analyze specific module | `/ontological-analysis module src/core` |
| `file <path>` | Analyze single file | `/ontological-analysis file README.md` |

### Options

| Option | Description | Example |
|--------|-------------|---------|
| `--dimensions <list>` | Analyze specific dimensions only | `--dimensions 1,2,5` |
| `--depth <level>` | Analysis depth: shallow/medium/deep | `--depth deep` |
| `--output <format>` | Output format: markdown/json/yaml | `--output json` |
| `--for-mvv` | Optimize output for MVV synthesis | `--for-mvv` |
| `--verbose` | Include detailed rationale | `--verbose` |

## The 8 Philosophical Dimensions

### Dimension 1: Context and Category

**Question**: What is this? In what domain does it exist?

**Analysis Focus**:
- Project type classification (library, framework, application, tool, platform)
- Primary domain (DevOps, AI, Finance, Healthcare, etc.)
- Operational context (CLI, web, mobile, embedded, cloud)
- Target environment (development, production, hybrid)

**Data Sources**:
- README.md, package.json/pom.xml/Cargo.toml
- Directory structure patterns
- CI/CD configuration
- Deployment manifests

**Output Fields**:
```yaml
context:
  project_type: <classification>
  primary_domain: <domain>
  secondary_domains: [<list>]
  operational_context: <context>
  target_environment: <environment>
  confidence: <0.0-1.0>
```

---

### Dimension 2: Purpose and Function

**Question**: What is its reason for being? What problem does it solve?

**Analysis Focus**:
- Core problem statement
- Value proposition
- Target beneficiaries (users, developers, organizations)
- Success metrics (explicit or implicit)
- Differentiation from alternatives

**Data Sources**:
- README.md introduction and motivation sections
- Documentation "Why" sections
- Issue templates and feature requests
- Commit message patterns (what changes are prioritized)

**Output Fields**:
```yaml
purpose:
  problem_statement: <description>
  value_proposition: <statement>
  target_beneficiaries:
    primary: <audience>
    secondary: [<list>]
  success_indicators: [<list>]
  differentiation: <unique_value>
  confidence: <0.0-1.0>
```

---

### Dimension 3: Taxonomy and Classification

**Question**: How does it relate to its peers? What category does it belong to?

**Analysis Focus**:
- Genus-species classification (general → specific)
- Hierarchical positioning in technology ecosystem
- Peer comparison (similar tools/frameworks)
- Superordinate category (what family does it belong to)
- Subordinate elements (what variations exist)

**Data Sources**:
- "Awesome" lists inclusion
- Comparison documentation
- Technology stack declarations
- Integration patterns

**Output Fields**:
```yaml
taxonomy:
  superordinate: <parent_category>
  genus: <general_type>
  species: <specific_type>
  peers: [<similar_projects>]
  subordinates: [<variants_or_plugins>]
  ecosystem_position: <description>
  confidence: <0.0-1.0>
```

---

### Dimension 4: Semantics and Language

**Question**: What language does it use? What terminology defines its domain?

**Analysis Focus**:
- Domain-specific vocabulary
- Naming conventions and patterns
- Metaphors and mental models embedded in code
- API terminology choices
- Documentation language style

**Data Sources**:
- Code identifiers (classes, functions, variables)
- API documentation
- Error messages
- Configuration key names
- Comment patterns

**Output Fields**:
```yaml
semantics:
  primary_language: <programming_language>
  domain_vocabulary: [<key_terms>]
  naming_conventions: <pattern_description>
  dominant_metaphors: [<metaphors>]
  communication_style: <formal/informal/technical>
  terminology_coherence: <0.0-1.0>
  confidence: <0.0-1.0>
```

---

### Dimension 5: Technological Lineage

**Question**: Where does it come from? What are its ancestors and influences?

**Analysis Focus**:
- Foundational technologies and frameworks
- Architectural patterns inherited
- Historical evolution (if visible in git history)
- Dependency tree analysis (core vs peripheral)
- Design pattern influences

**Data Sources**:
- Dependency manifests (package.json, pom.xml, etc.)
- Git history and major milestones
- Architecture documentation
- Framework/library choices
- Migration patterns

**Output Fields**:
```yaml
lineage:
  foundational_technologies: [<list>]
  architectural_ancestors: [<patterns>]
  major_influences: [<projects_or_paradigms>]
  evolutionary_stage: <nascent/growing/mature/legacy>
  core_dependencies: [<list>]
  peripheral_dependencies: [<list>]
  confidence: <0.0-1.0>
```

---

### Dimension 6: Epistemology

**Question**: How does it know what it knows? What assumptions does it make?

**Analysis Focus**:
- Implicit assumptions about the world
- Data models and their worldview
- Validation and verification approaches
- Truth sources (configuration, databases, APIs)
- Knowledge boundaries (what it cannot know)

**Data Sources**:
- Data schemas and models
- Configuration structures
- Validation logic
- Test assertions (what is considered correct)
- Error handling patterns

**Output Fields**:
```yaml
epistemology:
  core_assumptions: [<list>]
  knowledge_sources: [<data_origins>]
  validation_approach: <description>
  truth_model: <description>
  uncertainty_handling: <description>
  knowledge_boundaries: [<limitations>]
  confidence: <0.0-1.0>
```

---

### Dimension 7: Ontology

**Question**: What entities exist in its world? What are their relationships?

**Analysis Focus**:
- Core entities/objects/concepts
- Relationship types between entities
- Entity lifecycle patterns
- Cardinality and constraints
- Emergent behaviors from interactions

**Data Sources**:
- Database schemas
- Class/type definitions
- API resource structures
- State machines
- Event definitions

**Output Fields**:
```yaml
ontology:
  core_entities: [<list>]
  entity_relationships:
    - from: <entity>
      to: <entity>
      type: <relationship_type>
  lifecycle_patterns: [<patterns>]
  constraints: [<rules>]
  emergent_behaviors: [<descriptions>]
  confidence: <0.0-1.0>
```

---

### Dimension 8: Aesthetics and Form

**Question**: What is its form? What style defines it?

**Analysis Focus**:
- Code style and formatting conventions
- Visual design principles (if UI exists)
- Documentation presentation style
- API design philosophy (RESTful, GraphQL, RPC)
- Error message tone and helpfulness
- Overall "feel" of the project

**Data Sources**:
- Linting configurations
- Style guides
- UI/UX patterns
- API design patterns
- README formatting
- Contributing guidelines

**Output Fields**:
```yaml
aesthetics:
  code_style: <description>
  design_principles: [<principles>]
  api_philosophy: <description>
  documentation_style: <description>
  error_tone: <helpful/terse/friendly/technical>
  overall_impression: <description>
  polish_level: <rough/functional/polished/refined>
  confidence: <0.0-1.0>
```

## Execution Steps

### Step 1: Gather Raw Data

```
FOR each dimension in [1..8]:
    - Identify relevant data sources
    - Read files (README, configs, schemas, code samples)
    - Extract relevant patterns and keywords
    - Store raw observations
```

### Step 2: Analyze Each Dimension

```
FOR each dimension:
    - Apply dimension-specific analysis rules
    - Extract structured insights
    - Calculate confidence score (based on data availability)
    - Generate dimension output
```

### Step 3: Cross-Reference Dimensions

```
FOR each pair of dimensions:
    - Identify reinforcing patterns (consistency)
    - Identify contradictions (tension points)
    - Note emergent insights from combinations
```

### Step 4: Synthesize Ontological Map

```
COMBINE all dimensions into unified map:
    - Calculate overall coherence score
    - Identify dominant themes
    - Extract essence statement
    - Generate MVV-ready summary (if --for-mvv)
```

### Step 5: Generate Output

```
FORMAT output according to --output option:
    - markdown: Human-readable report
    - json: Structured data for programmatic use
    - yaml: Configuration-friendly format
```

## Output Format

### Full Analysis Report (`/ontological-analysis repo`)

```markdown
# Ontological Analysis Report

## Target: {repository_name}
## Analysis Date: {ISO-8601-timestamp}
## Analysis Depth: {depth_level}

---

## Executive Summary

**Essence Statement**: {one_sentence_essence}

**Coherence Score**: {score}/100

**Dominant Themes**:
1. {theme_1}
2. {theme_2}
3. {theme_3}

---

## Dimension 1: Context and Category

{dimension_1_output}

### Key Insights
- {insight_1}
- {insight_2}

---

## Dimension 2: Purpose and Function

{dimension_2_output}

### Key Insights
- {insight_1}
- {insight_2}

---

[... Dimensions 3-8 ...]

---

## Cross-Dimensional Analysis

### Reinforcing Patterns

| Dimensions | Pattern | Implication |
|------------|---------|-------------|
| 1 + 2 | {pattern} | {implication} |
| 3 + 7 | {pattern} | {implication} |

### Tension Points

| Dimensions | Tension | Recommendation |
|------------|---------|----------------|
| 4 + 8 | {tension} | {recommendation} |

---

## Emergent Insights

1. {emergent_insight_1}
2. {emergent_insight_2}

---

## MVV-Ready Summary (if --for-mvv)

### Mission Elements
- Core purpose: {purpose}
- Target audience: {audience}
- Unique value: {value}

### Vision Elements
- Aspirational state: {vision}
- Success indicators: {indicators}
- Time horizon: {horizon}

### Values Elements
- Explicit values: {explicit}
- Implicit values: {implicit}
- Cultural signals: {signals}

---

*Analysis performed by: {agent_id}*
*Skill version: 1.0.0*
```

### JSON Output (`--output json`)

```json
{
  "meta": {
    "target": "repository_name",
    "timestamp": "2026-01-08T12:00:00Z",
    "depth": "deep",
    "skill_version": "1.0.0"
  },
  "dimensions": {
    "context_and_category": { ... },
    "purpose_and_function": { ... },
    "taxonomy_and_classification": { ... },
    "semantics_and_language": { ... },
    "technological_lineage": { ... },
    "epistemology": { ... },
    "ontology": { ... },
    "aesthetics_and_form": { ... }
  },
  "cross_dimensional": {
    "reinforcing_patterns": [ ... ],
    "tension_points": [ ... ]
  },
  "synthesis": {
    "essence_statement": "...",
    "coherence_score": 85,
    "dominant_themes": [ ... ],
    "mvv_ready": {
      "mission_elements": { ... },
      "vision_elements": { ... },
      "values_elements": { ... }
    }
  }
}
```

## Example Usage

### Example 1: Full Repository Analysis for MVV

**Input**:
```
/ontological-analysis repo --for-mvv --depth deep
```

**Output** (abbreviated):
```markdown
# Ontological Analysis Report

## Target: multi-agent-os
## Analysis Date: 2026-01-08T12:30:00-03:00
## Analysis Depth: deep

---

## Executive Summary

**Essence Statement**: A framework for orchestrating multiple AI agents with hierarchical coordination, observability, and conflict prevention.

**Coherence Score**: 92/100

**Dominant Themes**:
1. Orchestration and coordination of autonomous agents
2. Safety through observability and anti-loop detection
3. Human-AI collaboration with clear boundaries

---

## Dimension 1: Context and Category

```yaml
context:
  project_type: framework
  primary_domain: AI/Agent Orchestration
  secondary_domains: [DevOps, Automation]
  operational_context: CLI + IDE integration
  target_environment: development
  confidence: 0.95
```

### Key Insights
- Framework designed for AI-assisted software development
- Operates at the meta-level (AI managing AI)

---

[... remaining dimensions ...]

---

## MVV-Ready Summary

### Mission Elements
- Core purpose: Enable safe, observable multi-agent AI collaboration
- Target audience: Development teams using AI assistants
- Unique value: Prevents coordination failures through protocol enforcement

### Vision Elements
- Aspirational state: AI agents as reliable team members
- Success indicators: Zero-conflict parallel work, 100% traceable decisions
- Time horizon: 2-3 years (AI development tooling maturity)

### Values Elements
- Explicit values: Safety, Observability, Human Control
- Implicit values: Pragmatism, Incremental Adoption
- Cultural signals: Documentation-first, Protocol-driven
```

### Example 2: Single Dimension Analysis

**Input**:
```
/ontological-analysis repo --dimensions 2,7 --output json
```

**Output**:
```json
{
  "meta": {
    "target": "multi-agent-os",
    "timestamp": "2026-01-08T12:35:00Z",
    "dimensions_analyzed": [2, 7]
  },
  "dimensions": {
    "purpose_and_function": {
      "problem_statement": "AI agents working in parallel can conflict, loop infinitely, or produce inconsistent results",
      "value_proposition": "Safe multi-agent orchestration with observability",
      "target_beneficiaries": {
        "primary": "Development teams using AI coding assistants",
        "secondary": ["AI researchers", "DevOps engineers"]
      },
      "confidence": 0.90
    },
    "ontology": {
      "core_entities": ["Agent", "Session", "Task", "Worktree", "Trace"],
      "entity_relationships": [
        {"from": "Session", "to": "Agent", "type": "contains"},
        {"from": "Agent", "to": "Task", "type": "executes"},
        {"from": "Agent", "to": "Worktree", "type": "operates_in"}
      ],
      "confidence": 0.88
    }
  }
}
```

## Integration

### With MVV Synthesis Skill

This skill is designed to feed directly into the `mvv-synthesis` skill:

```
/ontological-analysis repo --for-mvv --output json > analysis.json
/mvv-synthesis --input analysis.json
```

The `--for-mvv` flag optimizes the output structure for MVV extraction, including:
- Pre-classified mission elements
- Vision-aligned insights
- Values-indicative patterns

### With Sentinel Protocol

Ontological analysis traces are logged to Sentinel for:
- Tracking analysis quality over time
- Identifying repositories with low coherence scores
- Auditing MVV generation inputs

### With Status Map

Analysis progress can be displayed via Status Map templates:
- PULSE: `[ONTO] ████████░░ D6/8 | Coherence: 85% | → Analyzing aesthetics`
- COMPACT: Full dimension progress table

## Limitations

- Confidence scores require human validation for critical decisions
- Historical analysis limited to available git history
- Non-code artifacts (wikis, external docs) may not be accessible
- Language-specific patterns may miss cross-language nuances
- Implicit values require interpretive inference (higher uncertainty)

## Changelog

### v1.0.0 (2026-01-08)
- Initial release
- 8 philosophical dimensions implemented
- JSON/YAML/Markdown output formats
- MVV-ready synthesis mode
- Cross-dimensional analysis

---

*Ontological Analysis Skill v1.0.0 | Part of MVV Generator | Claude-Dev-eed7-001*
