# Agent Output Parsing Protocol

This reference consolidates output parsing specifications for all cartographer agents. Use this when parsing agent responses in commands.

## Delimiter Registry

| Agent | Start Delimiter | End Delimiter | Model |
|-------|-----------------|---------------|-------|
| surveyor (full) | `---ANALYSIS---` | `---END---` | sonnet |
| surveyor (quick) | `---QUICK_SCAN---` | `---END_QUICK_SCAN---` | sonnet |
| import-analyzer | `---IMPORT_ANALYSIS---` | `---END_IMPORT_ANALYSIS---` | sonnet |
| auditor | `---AUDIT---` | `---END---` | sonnet |
| atlas-validator | `---ATLAS-VALIDATION---` | `---END---` | haiku |
| pattern-enforcer | `---PATTERN-ENFORCEMENT---` | `---END---` | sonnet |
| architecture-auditor | `---ARCHITECTURE-AUDIT---` | `---END---` | sonnet |
| anti-pattern-detector | `---ANTI-PATTERN-SCAN---` | `---END---` | sonnet |
| convention-checker | `---CONVENTION-CHECK---` | `---END---` | haiku |

## Standard Parsing Algorithm

```
1. Find start delimiter marker in agent output
2. Parse YAML content until end delimiter
3. Validate required fields present
4. Validate paths exist where specified
5. Store parsed data for further processing
```

## Field Validation Rules

| Field Type | Validation |
|------------|------------|
| `path` | Must exist in filesystem |
| `count` | Must be positive integer or `~` prefixed approximation |
| `confidence` | Must be `high`, `medium`, or `low` |
| `severity` | Must be `error` or `warning` |
| `status` | Must be `healthy`, `warning`, or `critical` |

## Severity Classification Standards

Agents report severity at two levels that map to review outcomes:

| Agent Severity | Review Severity | Action Required |
|----------------|-----------------|-----------------|
| `error` | `blocker` | Must fix before PR |
| `warning` | `tech_debt` | Should fix, can defer |
| (recommendations) | `skippable` | Optional |

## Parse Error Handling

If any agent output fails to parse:

```
⚠️ Failed to parse {agent_name} output

Error: {parsing_error}
Agent output preview: {first 300 chars}

Continuing with results from other agents.
```

Continue processing with successfully parsed agent results. Note partial results in final report.

---

## Agent-Specific Schemas

### 1. Surveyor Agent (Full Mode)

**Used by:** `/cartographer:chart`

**Delimiters:** `---ANALYSIS---` / `---END---`

```yaml
metadata:
  project: string          # Required
  type: string             # Required: frontend_spa|backend_api|fullstack|monorepo|cli|library
  type_confidence: string  # Required: high|medium|low
  organization_style: string  # Required: domains|layers|hybrid
  stack:
    language: string       # Required
    version: string        # Optional
    framework: string      # Optional
    framework_version: string  # Optional
  architecture: string     # Optional

domains:                   # Required, at least 2
  {domain_name}:
    location: string       # Required, validate path exists
    purpose: string        # Required
    count: number          # Required (can be ~approximate)
    confidence: string     # Required: high|medium|low
    key_files: [strings]   # Required

layers:                    # Optional, required if organization_style includes layers
  {layer_name}:
    location: string       # path or pattern
    file_pattern: string   # glob pattern
    count: number
    purpose: string
    key_files: [strings]
    domains_served: [strings]

file_patterns:             # Required, at least 2
  {pattern_name}:
    pattern: string        # glob pattern
    example: string        # actual file path
    count: number
    purpose: string

config_files:
  entry_point: string      # main file
  package_manager: string
  build_command: string
  test_command: string
  lint_command: string
  env_template: string
  files: [{path, purpose}]

task_mappings:
  - id: string
    description: string
    entry_point: string
    patterns: [strings]

integrations:
  - name: string
    purpose: string
    config_location: string
    usage_locations: [strings]

async_infrastructure:
  type: string             # bullmq|sqs|rabbitmq|redis|none
  queues:
    - name: string
      handler: string
      purpose: string

testing:
  framework: string
  location: string
  pattern: string
  coverage: string

validation:
  working_dir: string
  commands:
    - name: string
      command: string

keyword_index:
  {keyword}: {pattern_id}

patterns:                  # Required
  {pattern_id}:
    keywords: [strings]
    file_convention: string
    test_convention: string
    registration:
      - file: string
        action: string
    validation_commands: [strings]
    example_files: [strings]
    related: [strings]
    anti_patterns_summary: [strings]  # 2-4 items, start with "Don't..."

technology_observations:
  - category: string
    observed: string
    evidence: [strings]

observations: [strings]
```

### 2. Surveyor Agent (Quick Scan Mode)

**Used by:** `/cartographer:chart --interactive` (phase 1)

**Delimiters:** `---QUICK_SCAN---` / `---END_QUICK_SCAN---`

```yaml
project_name: string
project_type: string       # frontend_spa|backend_api|fullstack|monorepo|cli|library
type_confidence: string    # high|medium|low

organization_style_detected: string  # domains|layers|hybrid
organization_evidence: [strings]

preliminary_domains:
  - name: string
    location: string
    file_count: string     # ~approximate

preliminary_layers:
  - name: string
    location: string
    pattern_guess: string

detected_patterns: [strings]

framework: string
language: string
```

### 3. Import Analyzer Agent

**Used by:** `/cartographer:chart --deep`

**Delimiters:** `---IMPORT_ANALYSIS---` / `---END_IMPORT_ANALYSIS---`

```yaml
summary:
  files_analyzed: number
  imports_traced: number
  domains_analyzed: number
  coupling_issues_found: number
  layering_violations_found: number

import_matrix:
  {domain_a}:
    {domain_b}: number     # count of files in A importing from B
    external: number

coupling_analysis:
  strong_coupling:
    - domains: [strings]
      direction: string    # bidirectional|unidirectional
      evidence: string
      recommendation: string

  fan_in_hubs:
    - domain: string
      imported_by: number
      evidence: string

  fan_out_concerns:
    - domain: string
      imports_from: number
      evidence: string

layering_violations:
  - layer: string
    violation_type: string  # skip_layer|reverse_direction
    expected: string
    actual: string
    count: number
    examples:
      - file: string
        import: string
        fix: string

domain_adjustments:
  split_candidates:
    - domain: string
      reason: string
      suggested_split:
        - name: string
          files: [strings]

  merge_candidates:
    - domains: [strings]
      reason: string
      suggested_name: string

  new_domain_candidates:
    - path: string
      reason: string
      suggested_name: string

extracted_anti_patterns:
  {pattern_id}:
    - string               # "Don't..." statements

observations: [strings]
```

### 4. Auditor Agent

**Used by:** `/cartographer:health` (drift detection)

**Delimiters:** `---AUDIT---` / `---END---`

```yaml
summary:
  status: string           # healthy|warning|critical
  total_domains: number
  valid_domains: number
  drift_detected: string   # yes|no
  staleness_score: number  # 0.0-1.0
  last_updated: string
  days_since_update: number

critical_issues:
  - type: string           # missing_path|invalid_reference
    domain: string
    documented_path: string
    message: string

high_issues:
  - type: string           # count_drift
    domain: string
    documented: number
    actual: number
    drift_percent: number
    message: string

medium_issues:
  - type: string           # orphan_directory|moderate_drift
    path: string
    file_count: number
    message: string

low_issues:
  - type: string           # minor_drift
    domain: string
    documented: number
    actual: number

domain_status:
  {domain_name}:
    path_exists: string    # yes|no
    documented_count: number
    actual_count: number
    drift_percent: number
    status: string         # valid|warning|invalid

pattern_status:
  {pattern_name}:
    documented_count: number
    actual_count: number
    drift_percent: number
    status: string

reference_status:
  {reference_path}:
    exists: string         # yes|no
    links_valid: string    # yes|no
    broken_links: [strings]

recommendations:
  - priority: string       # critical|high|medium|low
    action: string
    command: string

observations: [strings]
```

### 5. Atlas Validator Agent

**Used by:** `/cartographer:health` (structure validation)

**Delimiters:** `---ATLAS-VALIDATION---` / `---END---`

```yaml
summary:
  status: string           # valid|warnings|errors
  files_checked: number
  errors: number
  warnings: number
  mode: string             # standard|strict

structure:
  skill_md: string         # exists|missing
  schema_yaml: string      # exists|missing
  references_dir: string   # exists|missing
  pattern_guides: number
  domain_references: number

errors:
  - type: string           # missing_required_file|invalid_frontmatter|missing_required_section|broken_link|schema_violation
    file: string
    field: string
    section: string
    link: string
    line: number
    path: string
    expected: string
    actual: string
    message: string

warnings:
  - type: string           # missing_recommended|incomplete_pattern|weak_anti_patterns|generic_anti_pattern|stale_atlas
    file: string
    field: string
    pattern: string
    missing: [strings]
    count: number
    anti_pattern: string
    last_updated: string
    days_old: number
    message: string

reference_integrity:
  total_links: number
  valid_links: number
  broken_links: number
  broken:
    - source: string
      link: string
      line: number

completeness:
  domains_with_docs: string    # count/total
  patterns_with_anti_patterns: string
  patterns_with_examples: string
  patterns_with_tests: string

auto_fixable:
  - type: string
    file: string
    action: string

recommendations:
  - priority: string       # high|medium|low
    type: string           # add_content|fix_link|improve_quality
    description: string
```

### 6. Pattern Enforcer Agent

**Used by:** `/navigator:review`

**Delimiters:** `---PATTERN-ENFORCEMENT---` / `---END---`

```yaml
summary:
  files_reviewed: number
  violations_found: number
  patterns_checked: [strings]

violations:
  - file: string
    line: number|null
    pattern: string        # pattern_id
    rule: string           # what was violated
    evidence: string
    atlas_reference: string  # "schema.yaml patterns.{id}.{field}"
    severity: string       # error|warning
    fix: string

compliant:
  - file: string
    patterns: [strings]
    note: string

unclassified:
  - file: string
    reason: string
    suggestion: string

recommendations:
  - type: string           # pattern_update|new_pattern|review_needed
    description: string
```

### 7. Architecture Auditor Agent

**Used by:** `/navigator:review`

**Delimiters:** `---ARCHITECTURE-AUDIT---` / `---END---`

```yaml
summary:
  files_audited: number
  layers_validated: [strings]
  violations: number
  organization_style: string

layer_violations:
  - file: string
    source_layer: string
    import: string
    target_file: string
    target_layer: string
    violation: string      # upward_dependency|skip_layer
    explanation: string
    severity: string       # error|warning
    fix: string

domain_violations:
  - file: string
    source_domain: string
    import: string
    target_domain: string
    violation: string      # cross_domain_coupling
    explanation: string
    severity: string
    fix: string

circular_dependencies:
  - cycle: [strings]       # file paths forming cycle
    layers_involved: [strings]
    severity: string       # error
    fix: string

layer_coverage:
  {layer_name}:
    files_in_layer: number
    files_audited: number
    violations: number

unclassified_files:
  - file: string
    closest_layer: string|null
    suggestion: string

compliant_imports:
  - file: string
    layer: string
    import_count: number
    note: string

recommendations:
  - type: string           # layer_definition|refactor|interface_extraction
    description: string
    impact: string
```

### 8. Anti-Pattern Detector Agent

**Used by:** `/navigator:review`

**Delimiters:** `---ANTI-PATTERN-SCAN---` / `---END---`

```yaml
summary:
  files_scanned: number
  patterns_checked: [strings]
  detections: number
  unique_anti_patterns: number

detections:
  - file: string
    line: number
    pattern: string        # pattern_id
    anti_pattern: string   # "Don't..." statement
    evidence: string       # code snippet (multiline)
    atlas_reference: string
    severity: string       # error|warning
    fix: string
    fix_example: string|null  # corrected code (multiline)

clean_files:
  - file: string
    patterns_checked: [strings]
    anti_patterns_checked: number

anti_pattern_coverage:
  {pattern_id}:
    total_anti_patterns: number
    files_applicable: number
    detections: number

not_applicable:
  - file: string
    reason: string

recommendations:
  - type: string           # add_anti_pattern|clarify_rule|update_pattern
    pattern: string
    suggestion: string
    evidence: string
```

### 9. Convention Checker Agent

**Used by:** `/navigator:review`

**Delimiters:** `---CONVENTION-CHECK---` / `---END---`

```yaml
summary:
  files_checked: number
  new_files: number
  violations: number
  compliant: number

file_location_violations:
  - file: string
    issue: string          # outside_documented_domains|wrong_directory
    expected: string
    actual: string
    pattern: string
    suggestion: string

naming_violations:
  - file: string
    issue: string          # wrong_case|missing_suffix
    expected: string
    actual: string
    example: string
    pattern: string

missing_tests:
  - implementation: string
    pattern: string
    expected_test: string
    test_convention: string

orphan_directories:
  - path: string
    file_count: number
    suggestion: string

compliant_files:
  - file: string
    pattern: string
    conventions: [strings]  # list of conventions met

recommendations:
  - type: string           # add_domain|update_pattern|add_file_pattern
    target: string
    reason: string
```

---

## Aggregation Protocol

When aggregating results from multiple agents (e.g., in `/navigator:review`):

```
1. Collect all violations from all agents
2. Classify by severity:
   - error from any agent → blocker
   - warning from any agent → tech_debt
   - recommendations → skippable
3. Deduplicate (same file:line from multiple agents)
4. Sort by: severity (desc), then file path
5. Count totals for summary table
```

**Severity mapping table:**

| Agent | Output Field | Mapped Severity |
|-------|--------------|-----------------|
| pattern-enforcer | `severity: error` | blocker |
| pattern-enforcer | `severity: warning` | tech_debt |
| architecture-auditor | `severity: error` | blocker |
| architecture-auditor | `severity: warning` | tech_debt |
| anti-pattern-detector | `severity: error` | blocker |
| anti-pattern-detector | `severity: warning` | tech_debt |
| convention-checker | any violation | tech_debt |
| convention-checker | `missing_tests` | skippable |
