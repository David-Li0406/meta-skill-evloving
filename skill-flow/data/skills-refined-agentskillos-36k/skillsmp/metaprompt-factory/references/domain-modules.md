# domain modules

optional sections to include based on metaprompt domain.

## coding module

include when `domain == coding`:

```xml
<coding_module>
  <repo_conventions>
    <item>language: {language}</item>
    <item>package_manager: {npm|pnpm|cargo|pip}</item>
    <item>folder_layout: {structure}</item>
    <item>lint_command: {command}</item>
    <item>test_command: {command}</item>
    <item>build_command: {command}</item>
  </repo_conventions>

  <dependency_volatility>
    versions change frequently. verify in official docs before assuming
    specific API shapes or behaviors.
  </dependency_volatility>

  <security_and_privacy>
    <rule>never commit secrets or credentials</rule>
    <rule>no PII in logs or error messages</rule>
    <rule>validate all external input</rule>
  </security_and_privacy>
</coding_module>
```

## review module

include when `domain == review`:

```xml
<review_module>
  <audit_passes>
    <pass name="correctness">logic errors, null hazards, missing branches</pass>
    <pass name="security">XSS, injection, secrets exposure</pass>
    <pass name="stability">race conditions, data integrity</pass>
    <pass name="performance">N+1, hot paths, unnecessary recomputation</pass>
    <pass name="readability">naming, dead code, consistency</pass>
    <pass name="tests">coverage gaps, missing edge cases</pass>
  </audit_passes>

  <scoring>
    <dimension name="correctness" weight="0.35"/>
    <dimension name="safety_security" weight="0.15"/>
    <dimension name="stability_data_integrity" weight="0.20"/>
    <dimension name="performance" weight="0.10"/>
    <dimension name="readability_maintainability" weight="0.10"/>
    <dimension name="tests_docs" weight="0.10"/>
  </scoring>

  <output_sections>
    <section>summary</section>
    <section>merge_readiness (0-10 score)</section>
    <section>blocking_issues</section>
    <section>non_blocking_suggestions</section>
    <section>tests_and_qa</section>
  </output_sections>
</review_module>
```

## ops module

include when `domain == ops`:

```xml
<ops_module>
  <runbook_structure>
    <section>pre_flight_checks</section>
    <section>execution_steps</section>
    <section>verification</section>
    <section>rollback_procedure</section>
    <section>escalation_contacts</section>
  </runbook_structure>

  <safety_constraints>
    <rule>always have rollback plan before changes</rule>
    <rule>verify backups exist before destructive ops</rule>
    <rule>use dry-run where available</rule>
    <rule>log all actions for audit trail</rule>
  </safety_constraints>
</ops_module>
```

## research module

include when `domain == research`:

```xml
<research_module>
  <search_strategy>
    <step>identify key terms and synonyms</step>
    <step>search official docs first</step>
    <step>expand to high-quality secondary sources</step>
    <step>cross-reference multiple sources</step>
  </search_strategy>

  <evidence_grading>
    <grade level="A">official docs, specs, RFCs</grade>
    <grade level="B">maintainer blogs, release notes</grade>
    <grade level="C">community tutorials, stack overflow</grade>
    <grade level="D">unverified claims, mark as such</grade>
  </evidence_grading>

  <output_format>
    <section>findings summary</section>
    <section>key sources (with grades)</section>
    <section>confidence assessment</section>
    <section>knowledge gaps</section>
  </output_format>
</research_module>
```

## copilot module

include when generating prompts for copilot:

```xml
<copilot_module>
  <context_packet>
    structured state for copilot, not raw history.
    keep under 10K tokens for cost efficiency.
  </context_packet>

  <packet_schema>
    <field name="session">id, started, issue_id</field>
    <field name="progress">phase, step, total_steps</field>
    <field name="recent_actions">last 3-5 actions taken</field>
    <field name="current_state">what's happening now</field>
    <field name="question">specific ask for this call</field>
  </packet_schema>

  <response_schema>
    <field name="action">what to do next</field>
    <field name="confidence">0-10 score</field>
    <field name="reason">brief justification</field>
    <field name="escalate">true if confidence < 7</field>
  </response_schema>

  <model_hints>
    <hint model="gemini-3-pro">fast, 1M context, good for synthesis</hint>
    <hint model="claude-opus-4.5">best reasoning, use for complex decisions</hint>
    <hint model="sonnet-4">balanced, good default</hint>
  </model_hints>
</copilot_module>
```

## xcode module

include when generating prompts for Xcode/iOS development:

```xml
<xcode_module>
  <tools>xcodebuildmcp via copilot</tools>

  <flywheel>
    <step>build scheme</step>
    <step>boot simulator</step>
    <step>install + launch</step>
    <step>run tests (XCTest)</step>
    <step>UI automation (describe_ui, tap, swipe)</step>
    <step>commit if green</step>
  </flywheel>

  <context_sources>
    <source>AGENTS.md (project conventions)</source>
    <source>Packages/ (local Swift packages)</source>
    <source>scheme list (available build targets)</source>
    <source>recent build errors</source>
  </context_sources>
</xcode_module>
```

## playwright module

include when generating prompts for web E2E testing:

```xml
<playwright_module>
  <tools>@playwright/mcp via copilot</tools>

  <flywheel>
    <step>build (vite/next/etc)</step>
    <step>serve localhost</step>
    <step>navigate to page</step>
    <step>run E2E tests</step>
    <step>UI verification (snapshot, interact, assert)</step>
    <step>commit if green</step>
  </flywheel>

  <capabilities>
    <cap>accessibility-tree based (not pixel)</cap>
    <cap>persistent or isolated profiles</cap>
    <cap>headed or headless</cap>
    <cap>init scripts for setup</cap>
  </capabilities>
</playwright_module>
```
