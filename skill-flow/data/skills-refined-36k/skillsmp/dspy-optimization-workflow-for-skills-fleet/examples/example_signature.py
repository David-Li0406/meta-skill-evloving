"""Example of a well-structured DSPy signature with best practices.

This example demonstrates:
- Literal types for constrained outputs
- Specific OutputField descriptions with quality indicators
- Concise, actionable docstring
- Proper type hints
"""

from __future__ import annotations

from typing import Literal

import dspy


class GatherRequirementsSignature(dspy.Signature):
    """Gather and analyze requirements for skill creation.
    
    Extract user intent, determine taxonomy placement, and identify
    related skills and dependencies.
    """
    
    # INPUT FIELDS
    task_description: str = dspy.InputField(
        desc="User's task description for skill creation"
    )
    
    # OUTPUT FIELDS
    domain: Literal[
        "python",
        "web",
        "devops",
        "testing",
        "api",
        "database",
        "architecture",
        "practices",
        "domain",
        "memory",
    ] = dspy.OutputField(
        desc="Primary domain category for this skill"
    )
    
    category: str = dspy.OutputField(
        desc="Specific category within domain (e.g., 'async', 'authentication')"
    )
    
    target_level: Literal["beginner", "intermediate", "advanced"] = dspy.OutputField(
        desc="Skill complexity level"
    )
    
    skill_type: Literal["guide", "reference", "workflow", "troubleshooting"] = dspy.OutputField(
        desc="Type of skill content to generate"
    )
    
    topics: list[str] = dspy.OutputField(
        desc="3-7 specific topics this skill should cover"
    )
    
    parent_skills: list[str] = dspy.OutputField(
        desc="Prerequisite skills user should know (e.g., ['python/basics', 'testing/pytest'])"
    )
    
    related_skills: list[str] = dspy.OutputField(
        desc="Related skills for cross-referencing"
    )
    
    estimated_length: Literal["short", "medium", "long"] = dspy.OutputField(
        desc="Estimated skill length: short (<500 words), medium (500-2000), long (>2000)"
    )
    
    key_insights: list[str] = dspy.OutputField(
        desc="2-4 key insights or principles this skill teaches, quality score >0.75"
    )


class GenerateSkillContentSignature(dspy.Signature):
    """Generate production-ready skill content.
    
    Creates comprehensive SKILL.md with examples, best practices,
    and actionable guidance. Quality score >0.80 required.
    """
    
    # INPUT FIELDS
    skill_metadata: dict = dspy.InputField(
        desc="Metadata from requirements gathering (name, description, category, etc.)"
    )
    
    content_plan: str = dspy.InputField(
        desc="Content structure and key points to cover"
    )
    
    # OUTPUT FIELDS
    skill_content: str = dspy.OutputField(
        desc="Complete SKILL.md markdown content, quality score >0.80, "
        "includes 3-5 concrete examples, production-ready code snippets, "
        "✅/❌ good/bad contrast patterns, copy-paste ready"
    )
    
    usage_examples: list[str] = dspy.OutputField(
        desc="3-5 real-world usage scenarios with code examples"
    )
    
    best_practices: list[str] = dspy.OutputField(
        desc="5-8 actionable best practices specific to this skill"
    )
    
    common_mistakes: list[str] = dspy.OutputField(
        desc="3-5 common mistakes to avoid with explanations"
    )
    
    related_references: list[str] = dspy.OutputField(
        desc="External documentation links for deeper learning"
    )


# Usage example
if __name__ == "__main__":
    import dspy
    
    # Configure DSPy (you would normally do this once at startup)
    lm = dspy.LM("gemini/gemini-3-flash-preview", api_key="...")
    dspy.configure(lm=lm)
    
    # Use signature with ChainOfThought
    gather = dspy.ChainOfThought(GatherRequirementsSignature)
    
    result = gather(
        task_description="Create a skill for async Python programming with asyncio"
    )
    
    # Access typed outputs
    print(f"Domain: {result.domain}")  # Type: Literal["python", "web", ...]
    print(f"Category: {result.category}")  # Type: str
    print(f"Target Level: {result.target_level}")  # Type: Literal["beginner", ...]
    print(f"Topics: {result.topics}")  # Type: list[str]
    
    # Use with optimization
    from dspy.evaluate import Evaluate
    
    def metric(example, pred, trace=None) -> float:
        """Evaluation metric for optimization."""
        score = 0.0
        
        # Check domain matches expected
        if hasattr(example, "expected_domain"):
            if pred.domain == example.expected_domain:
                score += 0.3
        
        # Check has sufficient topics
        if len(pred.topics) >= 3:
            score += 0.3
        
        # Check target level is reasonable
        if pred.target_level in ["beginner", "intermediate", "advanced"]:
            score += 0.2
        
        # Check has parent skills identified
        if len(pred.parent_skills) > 0:
            score += 0.2
        
        return score
    
    # Optimize with MIPROv2
    trainset = [...]  # Your training examples
    
    optimizer = dspy.MIPROv2(metric=metric, auto="medium")
    optimized_gather = optimizer.compile(
        gather,
        trainset=trainset,
        max_bootstrapped_demos=2,
        max_labeled_demos=2,
    )
    
    # Use optimized version
    optimized_result = optimized_gather(
        task_description="Create a skill for async Python programming"
    )
