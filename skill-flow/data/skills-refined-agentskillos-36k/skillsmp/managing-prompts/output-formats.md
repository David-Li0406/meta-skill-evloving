# Output Format Templates

XML templates for structured prompt engineering deliverables.

## Analysis Report Template

Use when evaluating existing prompts (Workflow 1).

```xml
<prompt_analysis>
  <summary>
Brief overview of prompt and assessment (2-3 sentences)
  </summary>

  <structure_evaluation>
    <role_definition>Assessment of role clarity</role_definition>
    <context_provision>Assessment of background information</context_provision>
    <objective_clarity>Assessment of goal and success criteria</objective_clarity>
    <constraints>Assessment of rules and boundaries</constraints>
    <output_format>Assessment of structure specification</output_format>
  </structure_evaluation>

  <techniques_used>
    <clarity>Score (0-10) and notes on instruction explicitness</clarity>
    <examples>Count and quality assessment (0=none, 1, 3-5, 5+)</examples>
    <reasoning>CoT type (none|basic|guided|structured) and effectiveness</reasoning>
    <xml_structure>Quality and consistency assessment</xml_structure>
    <other_techniques>List any additional techniques (prefilling, templates, etc.)</other_techniques>
  </techniques_used>

  <guardrails_assessment>
    <hallucination_prevention>Measures present (quote-grounding, citations, uncertainty permission, knowledge restriction)</hallucination_prevention>
    <consistency_enforcement>Mechanisms used (format spec, examples, prefilling, knowledge base)</consistency_enforcement>
    <security>Safeguards implemented (screening, leak protection, jailbreak resistance, sanitization)</security>
  </guardrails_assessment>

  <context_efficiency>
    <token_count>Total tokens and breakdown by section</token_count>
    <caching_opportunities>Identified cacheable sections (≥1024 tokens static)</caching_opportunities>
    <optimization_potential>Strategies applicable (remove redundancy, chaining, quote-grounding, etc.)</optimization_potential>
  </context_efficiency>

  <claude_45_optimization>
    <alignment>Assessment of Claude 4.5 best practices (explicit instructions, motivation, example quality, action framing, summary requests)</alignment>
    <improvements_needed>Specific updates required for Claude 4.5 optimization</improvements_needed>
  </claude_45_optimization>

  <issues>
    <critical>
      - [Issue causing prompt to fail or produce wrong results]
    </critical>
    <major>
      - [Issue significantly impacting quality/reliability]
    </major>
    <minor>
      - [Issue that could be improved but not essential]
    </minor>
  </issues>

  <recommendations>
    <recommendation>
      <priority>critical|major|minor</priority>
      <change>Specific modification to make</change>
      <rationale>Why this improves the prompt</rationale>
      <implementation>How to apply the change</implementation>
      <before>Current problematic pattern (optional)</before>
      <after>Improved pattern (optional)</after>
    </recommendation>
    <!-- Repeat for each recommendation -->
  </recommendations>
</prompt_analysis>
```

---

## Optimization Report Template

Use when improving prompt efficiency or quality (Workflow 3).

```xml
<optimization_report>
  <goal>Primary optimization objective (context reduction|quality improvement|consistency enhancement|hallucination reduction|caching implementation|prompt splitting)</goal>

  <current_state>
    <token_count>Current total tokens</token_count>
    <issues>
      - [Problem 1]
      - [Problem 2]
    </issues>
  </current_state>

  <strategy>Chosen optimization approach and rationale</strategy>

  <changes>
    <change>
      <type>context_reduction|quality|consistency|hallucination|caching|splitting</type>
      <before>Original pattern or structure</before>
      <after>Optimized pattern or structure</after>
      <impact>Expected improvement (quantified if possible)</impact>
    </change>
    <!-- Repeat for each change -->
  </changes>

  <results>
    <token_savings>Amount saved (e.g., "450 tokens, 60% reduction")</token_savings>
    <quality_improvement>Measure of quality gain (e.g., "Added 3 examples for consistency")</quality_improvement>
    <other_gains>
      - [Additional benefit 1]
      - [Additional benefit 2]
    </other_gains>
  </results>

  <implementation_notes>
Any special considerations or next steps for applying optimization
  </implementation_notes>
</optimization_report>
```

---

## Extraction Decision Template

Use when deciding if logic should become prompt/script (Workflow 5).

```xml
<extraction_decision>
  <current_logic>
Description of the logic being evaluated for extraction
  </current_logic>

  <criteria_evaluation>
    <prompt_extraction>
      <reusability>
        <score>0|1</score>
        <reasoning>Will be reused across 3+ contexts/conversations?</reasoning>
      </reusability>
      <prompt_techniques>
        <score>0|1</score>
        <reasoning>Needs examples, CoT, XML structure, or template variables?</reasoning>
      </prompt_techniques>
      <guardrails>
        <score>0|1</score>
        <reasoning>Requires hallucination prevention, consistency enforcement, or security?</reasoning>
      </guardrails>
      <context_optimization>
        <score>0|1</score>
        <reasoning>Would benefit from caching, document organization, or splitting?</reasoning>
      </context_optimization>
      <standardization>
        <score>0|1</score>
        <reasoning>Team needs consistent approach across uses?</reasoning>
      </standardization>
      <complexity>
        <score>0|1</score>
        <reasoning>Instructions would be >200 tokens or requires multiple steps?</reasoning>
      </complexity>
      <total_score>X/6 (0-2: keep inline, 3-4: extract, 5-6: strongly recommended)</total_score>
    </prompt_extraction>

    <script_extraction>
      <deterministic>
        <score>0|1</score>
        <reasoning>Same input always produces same output? No judgment required?</reasoning>
      </deterministic>
      <computation>
        <score>0|1</score>
        <reasoning>Involves calculations, data processing, or performance-critical operations?</reasoning>
      </computation>
      <testing>
        <score>0|1</score>
        <reasoning>Can write unit tests with clear pass/fail criteria?</reasoning>
      </testing>
      <reusability>
        <score>0|1</score>
        <reasoning>Multiple different prompts would use this logic?</reasoning>
      </reusability>
      <reasoning_needed>
        <score>0|1</score>
        <reasoning>No understanding or context interpretation required? (score 1 if no reasoning needed)</reasoning>
      </reasoning_needed>
      <format_conversion>
        <score>0|1</score>
        <reasoning>Converting formats, validating structure, or parsing data?</reasoning>
      </format_conversion>
      <total_score>X/6 (0-2: keep in prompt, 3-4: extract, 5-6: strongly recommended)</total_score>
    </script_extraction>
  </criteria_evaluation>

  <recommendation>
    <decision>extract_to_prompt|extract_to_script|keep_inline</decision>
    <rationale>
Detailed reasoning for decision based on scoring above
    </rationale>
    <structure>
If extracting, proposed design:
- For prompt: template structure, variables, techniques to apply
- For script: interface (inputs/outputs), key functions, integration approach
- For inline: justification (one-time use, context-specific, etc.)
    </structure>
  </recommendation>
</extraction_decision>
```

---

## Creation Summary Template

Use when documenting a newly created prompt (Workflow 2).

```xml
<prompt_creation_summary>
  <metadata>
    <name>Prompt name or identifier</name>
    <purpose>What the prompt accomplishes</purpose>
    <use_cases>
      - [Use case 1]
      - [Use case 2]
    </use_cases>
    <complexity>simple|medium|complex</complexity>
  </metadata>

  <architecture>
    <pattern>simple_task|complex_reasoning|agent_workflow|multi_window</pattern>
    <rationale>Why this pattern was selected</rationale>
  </architecture>

  <techniques_applied>
    <technique>
      <name>Explicit instructions | Multishot prompting | Chain-of-thought | XML structure | etc.</name>
      <implementation>How it was applied</implementation>
      <purpose>Why it was needed</purpose>
    </technique>
    <!-- Repeat for each technique -->
  </techniques_applied>

  <guardrails_implemented>
    <guardrail>
      <type>hallucination_prevention|consistency_enforcement|security|character_maintenance</type>
      <pattern>Specific pattern used (quote-grounding, format spec, input screening, etc.)</pattern>
      <risk_addressed>What risk this mitigates</risk_addressed>
    </guardrail>
    <!-- Repeat for each guardrail -->
  </guardrails_implemented>

  <context_optimization>
    <token_count>Estimated total tokens</token_count>
    <caching_strategy>If applicable, what content is cached and why</caching_strategy>
    <efficiency_measures>
      - [Measure 1: e.g., "Used bullets instead of prose"]
      - [Measure 2: e.g., "Quote-grounding reduces 50K docs to 5K"]
    </efficiency_measures>
  </context_optimization>

  <validation_completed>
    <checklist_status>All items from quick-reference.md checklist verified</checklist_status>
    <golden_test>Colleague clarity check: passed|not_performed</golden_test>
    <test_results>
Summary of testing with sample inputs (if performed)
    </test_results>
  </validation_completed>

  <usage_notes>
Any special instructions for using this prompt, expected behavior, or integration guidance
  </usage_notes>
</prompt_creation_summary>
```

---

## Migration Report Template

Use when updating prompts for Claude 4.5 (Workflow 4).

```xml
<migration_report>
  <prompt_info>
    <identifier>Prompt name or ID</identifier>
    <previous_version>Claude 3.x|Claude 3.5|other</previous_version>
    <target_version>Claude 4.5</target_version>
  </prompt_info>

  <outdated_patterns_identified>
    <pattern>
      <type>insufficient_explicitness|missing_motivation|poor_example_quality|suggestion_framing|no_summary_requests|other</type>
      <location>Where in prompt this appears</location>
      <issue>Why this is problematic for Claude 4.5</issue>
    </pattern>
    <!-- Repeat for each pattern -->
  </outdated_patterns_identified>

  <migration_changes>
    <change>
      <category>explicitness|motivation|examples|framing|summaries|quality_modifiers|parallel_execution|context_awareness|other</category>
      <before>Original pattern</before>
      <after>Claude 4.5 optimized pattern</after>
      <rationale>Why this change improves Claude 4.5 performance</rationale>
    </change>
    <!-- Repeat for each change -->
  </migration_changes>

  <testing_results>
    <test_case>
      <description>What was tested</description>
      <claude_3_behavior>How Claude 3 handled this</claude_3_behavior>
      <claude_45_behavior>How Claude 4.5 handles this after migration</claude_45_behavior>
      <status>passed|needs_adjustment</status>
    </test_case>
    <!-- Repeat for each test -->
  </testing_results>

  <recommendations>
    <recommendation>
      <priority>high|medium|low</priority>
      <suggestion>Further optimization possible</suggestion>
    </recommendation>
  </recommendations>

  <migration_status>complete|needs_further_testing|failed</migration_status>
</migration_report>
```

---

## Template Usage Guide

### When to Use Each Template

| Template | Workflow | Primary Use Case |
|----------|----------|------------------|
| Analysis Report | Workflow 1 | Evaluating existing prompts for improvements |
| Optimization Report | Workflow 3 | Documenting efficiency or quality improvements |
| Extraction Decision | Workflow 5 | Deciding if logic should become prompt/script |
| Creation Summary | Workflow 2 | Documenting newly created prompts |
| Migration Report | Workflow 4 | Updating prompts for Claude 4.5 |

### Filling Out Templates

**Required sections:**
- Always fill: summary, primary assessment sections, recommendations
- Optional: detailed subsections when applicable

**Score guidelines:**
- 0-3: Poor (critical issues)
- 4-6: Fair (major issues)
- 7-8: Good (minor issues)
- 9-10: Excellent (minimal issues)

**Priority levels:**
- Critical: Breaks functionality or causes serious errors
- Major: Significantly impacts quality/reliability
- Minor: Improvements but not essential

### Integration with Workflows

**Workflow 1 (Analysis):**
1. Complete evaluation
2. Fill Analysis Report Template
3. Present to user

**Workflow 3 (Optimization):**
1. Identify optimization goal
2. Apply transformations
3. Fill Optimization Report Template
4. Document results

**Workflow 5 (Extraction):**
1. Evaluate criteria (6 factors each for prompt/script)
2. Fill Extraction Decision Template
3. Provide recommendation

**Workflow 2 (Creation):**
1. Create prompt
2. Fill Creation Summary Template (optional, for documentation)

**Workflow 4 (Migration):**
1. Identify outdated patterns
2. Apply Claude 4.5 updates
3. Fill Migration Report Template
4. Test and validate

### Customization

Templates can be adapted:
- Remove optional sections not applicable
- Add domain-specific assessment criteria
- Adjust scoring scales if needed
- Combine templates for complex analyses

### Output Format

Present templates filled with actual content, not the template structure itself. Structure makes analysis systematic, but user sees completed analysis, not empty template.
