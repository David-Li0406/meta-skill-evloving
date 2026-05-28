"""Tests for prompts module."""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from prompts import (
    EXPORT_TASKS_PROMPT,
    FOCUS_AREAS,
    PERSONAS,
    PRESERVE_INTENT_PROMPT,
    PRESS_PROMPT_TEMPLATE,
    REVIEW_PROMPT_TEMPLATE,
    get_doc_type_name,
    get_system_prompt,
)


class TestGetSystemPrompt:
    def test_prd_returns_prd_prompt(self):
        # Mutation: changing SYSTEM_PROMPT_PRD content would fail these assertions
        result = get_system_prompt("prd")
        assert "Product Requirements Document" in result
        assert "product manager" in result.lower()
        assert "user stories" in result.lower() or "user personas" in result.lower()
        assert len(result) > 500  # PRD prompt should be substantial

    def test_tech_returns_tech_prompt(self):
        # Mutation: changing SYSTEM_PROMPT_TECH content would fail these assertions
        result = get_system_prompt("tech")
        assert "Technical Specification" in result
        assert "API" in result or "architecture" in result.lower()
        assert len(result) > 500  # Tech prompt should be substantial

    def test_unknown_returns_generic_prompt(self):
        # Mutation: setting SYSTEM_PROMPT_GENERIC to None would fail
        result = get_system_prompt("unknown")
        assert result is not None
        assert isinstance(result, str)
        assert "spec" in result.lower()
        assert len(result) > 200  # Generic prompt should have content

    def test_known_persona_returns_persona_prompt(self):
        # Mutation: changing PERSONAS content would fail these assertions
        result = get_system_prompt("tech", persona="security-engineer")
        assert "security" in result.lower()
        assert "engineer" in result.lower() or "experience" in result.lower()
        assert len(result) > 50

    def test_unknown_persona_returns_custom_prompt(self):
        result = get_system_prompt("tech", persona="fintech auditor")
        assert "fintech auditor" in result
        assert "adversarial spec development" in result

    def test_persona_overrides_doc_type(self):
        # Mutation: changing PERSONAS["oncall-engineer"] would fail
        result = get_system_prompt("prd", persona="oncall-engineer")
        assert "on-call" in result.lower() or "oncall" in result.lower()
        assert "paged" in result.lower() or "production" in result.lower()
        assert len(result) > 50


class TestGetDocTypeName:
    def test_prd(self):
        assert get_doc_type_name("prd") == "Product Requirements Document"

    def test_tech(self):
        assert get_doc_type_name("tech") == "Technical Specification"

    def test_unknown(self):
        assert get_doc_type_name("other") == "specification"


class TestFocusAreas:
    def test_all_focus_areas_exist(self):
        expected = [
            "security",
            "scalability",
            "performance",
            "ux",
            "reliability",
            "cost",
        ]
        for area in expected:
            assert area in FOCUS_AREAS

    def test_focus_areas_contain_critical_focus(self):
        for name, content in FOCUS_AREAS.items():
            assert "CRITICAL FOCUS" in content

    def test_security_focus_content(self):
        # Mutation: XX prefix/suffix would fail keyword checks
        content = FOCUS_AREAS["security"]
        assert "security" in content.lower()
        assert "authentication" in content.lower() or "authorization" in content.lower()

    def test_scalability_focus_content(self):
        # Mutation: XX prefix/suffix would fail keyword checks
        content = FOCUS_AREAS["scalability"]
        assert "scale" in content.lower() or "load" in content.lower()

    def test_performance_focus_content(self):
        # Mutation: XX prefix/suffix would fail keyword checks
        content = FOCUS_AREAS["performance"]
        assert "performance" in content.lower() or "latency" in content.lower()

    def test_ux_focus_content(self):
        # Mutation: XX prefix/suffix would fail keyword checks
        content = FOCUS_AREAS["ux"]
        assert "user" in content.lower() or "ux" in content.lower()

    def test_reliability_focus_content(self):
        # Mutation: XX prefix/suffix would fail keyword checks
        content = FOCUS_AREAS["reliability"]
        assert "reliability" in content.lower() or "failure" in content.lower()

    def test_cost_focus_content(self):
        # Mutation: XX prefix/suffix would fail keyword checks
        content = FOCUS_AREAS["cost"]
        assert "cost" in content.lower() or "budget" in content.lower()


class TestPersonas:
    def test_all_personas_exist(self):
        expected = [
            "security-engineer",
            "oncall-engineer",
            "junior-developer",
            "qa-engineer",
            "site-reliability",
            "product-manager",
            "data-engineer",
            "mobile-developer",
            "accessibility-specialist",
            "legal-compliance",
        ]
        for persona in expected:
            assert persona in PERSONAS

    def test_personas_are_non_empty(self):
        for name, content in PERSONAS.items():
            assert len(content) > 50

    def test_security_engineer_persona_content(self):
        # Mutation: XX prefix/suffix would fail keyword checks
        content = PERSONAS["security-engineer"]
        assert "security" in content.lower()
        assert "penetration" in content.lower() or "attacker" in content.lower()

    def test_oncall_engineer_persona_content(self):
        # Mutation: XX prefix/suffix would fail keyword checks
        content = PERSONAS["oncall-engineer"]
        assert "on-call" in content.lower() or "paged" in content.lower()
        assert "production" in content.lower() or "debug" in content.lower()

    def test_junior_developer_persona_content(self):
        # Mutation: XX prefix/suffix would fail keyword checks
        content = PERSONAS["junior-developer"]
        assert "junior" in content.lower()
        assert "ambiguous" in content.lower() or "implement" in content.lower()

    def test_qa_engineer_persona_content(self):
        # Mutation: XX prefix/suffix would fail keyword checks
        content = PERSONAS["qa-engineer"]
        assert "qa" in content.lower() or "test" in content.lower()
        assert "edge case" in content.lower() or "scenario" in content.lower()

    def test_site_reliability_persona_content(self):
        # Mutation: XX prefix/suffix would fail keyword checks
        content = PERSONAS["site-reliability"]
        assert "sre" in content.lower() or "reliability" in content.lower()

    def test_product_manager_persona_content(self):
        # Mutation: XX prefix/suffix would fail keyword checks
        content = PERSONAS["product-manager"]
        assert "product" in content.lower()
        assert "user" in content.lower() or "business" in content.lower()

    def test_data_engineer_persona_content(self):
        # Mutation: XX prefix/suffix would fail keyword checks
        content = PERSONAS["data-engineer"]
        assert "data" in content.lower()
        assert "data model" in content.lower() or "etl" in content.lower()

    def test_mobile_developer_persona_content(self):
        # Mutation: XX prefix/suffix would fail keyword checks
        content = PERSONAS["mobile-developer"]
        assert "mobile" in content.lower()
        assert "api" in content.lower() or "payload" in content.lower()

    def test_accessibility_specialist_persona_content(self):
        # Mutation: XX prefix/suffix would fail keyword checks
        content = PERSONAS["accessibility-specialist"]
        assert "accessibility" in content.lower() or "wcag" in content.lower()

    def test_legal_compliance_persona_content(self):
        # Mutation: XX prefix/suffix would fail keyword checks
        content = PERSONAS["legal-compliance"]
        assert "legal" in content.lower() or "compliance" in content.lower()
        assert (
            "gdpr" in content.lower()
            or "regulation" in content.lower()
            or "privacy" in content.lower()
        )


class TestPreserveIntentPrompt:
    def test_contains_key_instructions(self):
        assert "PRESERVE ORIGINAL INTENT" in PRESERVE_INTENT_PROMPT
        assert "ASSUME the author had good reasons" in PRESERVE_INTENT_PROMPT
        assert "ERRORS" in PRESERVE_INTENT_PROMPT
        assert "RISKS" in PRESERVE_INTENT_PROMPT
        assert "PREFERENCES" in PRESERVE_INTENT_PROMPT


class TestTemplateConstants:
    def test_review_prompt_template_not_none(self):
        # Mutation: REVIEW_PROMPT_TEMPLATE = None would fail
        assert REVIEW_PROMPT_TEMPLATE is not None
        assert isinstance(REVIEW_PROMPT_TEMPLATE, str)

    def test_review_prompt_template_content(self):
        assert "{round}" in REVIEW_PROMPT_TEMPLATE
        assert "{doc_type_name}" in REVIEW_PROMPT_TEMPLATE
        assert "{spec}" in REVIEW_PROMPT_TEMPLATE
        assert "adversarial spec development" in REVIEW_PROMPT_TEMPLATE

    def test_press_prompt_template_not_none(self):
        # Mutation: PRESS_PROMPT_TEMPLATE = None would fail
        assert PRESS_PROMPT_TEMPLATE is not None
        assert isinstance(PRESS_PROMPT_TEMPLATE, str)

    def test_press_prompt_template_content(self):
        assert "{round}" in PRESS_PROMPT_TEMPLATE
        assert "AGREE" in PRESS_PROMPT_TEMPLATE
        assert "thoroughly reviewing" in PRESS_PROMPT_TEMPLATE.lower()

    def test_export_tasks_prompt_not_none(self):
        # Mutation: EXPORT_TASKS_PROMPT = None would fail
        assert EXPORT_TASKS_PROMPT is not None
        assert isinstance(EXPORT_TASKS_PROMPT, str)

    def test_export_tasks_prompt_content(self):
        assert "[TASK]" in EXPORT_TASKS_PROMPT
        assert "[/TASK]" in EXPORT_TASKS_PROMPT
        assert "title:" in EXPORT_TASKS_PROMPT


class TestPersonaStringIntegrity:
    def test_all_personas_start_with_you_are(self):
        # Mutation: XX prefix would fail this check
        for name, content in PERSONAS.items():
            assert content.startswith("You are"), (
                f"Persona {name} should start with 'You are'"
            )

    def test_custom_persona_fallback_starts_correctly(self):
        # Mutation: XX prefix on fallback would fail
        result = get_system_prompt("tech", persona="custom-role")
        assert result.startswith("You are a custom-role")

    def test_persona_with_space_normalized(self):
        # Mutation: replace(" ", "-") changed would break mapping
        result = get_system_prompt("tech", persona="security engineer")
        # Should map to "security-engineer" persona
        assert "penetration" in result.lower() or "attacker" in result.lower()
        assert "15 years" in result

    def test_persona_with_underscore_normalized(self):
        # Mutation: replace("_", "-") changed would break mapping
        result = get_system_prompt("tech", persona="security_engineer")
        # Should map to "security-engineer" persona
        assert "penetration" in result.lower() or "attacker" in result.lower()
        assert "15 years" in result


class TestFocusAreaStringIntegrity:
    def test_all_focus_areas_start_with_critical(self):
        # Mutation: XX prefix would fail this check
        for name, content in FOCUS_AREAS.items():
            assert content.strip().startswith("**CRITICAL FOCUS"), (
                f"Focus area {name} should start with CRITICAL FOCUS"
            )
