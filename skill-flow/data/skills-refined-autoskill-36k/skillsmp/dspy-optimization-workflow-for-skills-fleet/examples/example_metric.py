"""Example custom evaluation metric for DSPy optimization.

This demonstrates how to create effective metrics for optimizing
skill generation quality.
"""

from __future__ import annotations

import dspy


def simple_quality_metric(example: dspy.Example, prediction: dspy.Prediction, trace=None) -> float:
    """Simple metric for testing optimization.
    
    Checks basic quality indicators without complex logic.
    Good for initial experiments and debugging.
    
    Args:
        example: Training example with expected outputs
        prediction: Model prediction to evaluate
        trace: Optional execution trace (unused)
    
    Returns:
        Score between 0.0 and 1.0
    """
    score = 0.0
    
    # Check required fields exist
    if hasattr(prediction, "domain") and prediction.domain:
        score += 0.25
    
    if hasattr(prediction, "category") and prediction.category:
        score += 0.25
    
    # Check field matches expected (if available)
    if hasattr(example, "expected_taxonomy_path"):
        expected_parts = example.expected_taxonomy_path.split("/")
        predicted_category = getattr(prediction, "category", "")
        
        if predicted_category.lower() in expected_parts[0].lower():
            score += 0.25
    
    # Check topics list is reasonable
    if hasattr(prediction, "topics") and isinstance(prediction.topics, list):
        if 3 <= len(prediction.topics) <= 7:
            score += 0.25
    
    return min(score, 1.0)


def taxonomy_accuracy_metric(example: dspy.Example, prediction: dspy.Prediction, trace=None) -> float:
    """Evaluate taxonomy path prediction accuracy.
    
    More sophisticated metric focusing on taxonomy placement.
    Used in production for Phase 1 (Understanding) optimization.
    
    Args:
        example: Example with expected_taxonomy_path
        prediction: Prediction with taxonomy_path
        trace: Optional trace (unused)
    
    Returns:
        Score 0.0-1.0 (1.0 = exact match, 0.7 = category match, 0.0 = miss)
    """
    if not hasattr(example, "expected_taxonomy_path"):
        return 0.5  # Neutral if no expectation
    
    expected = example.expected_taxonomy_path
    
    # Try different field names
    predicted = None
    for field in ["taxonomy_path", "recommended_path", "path"]:
        if hasattr(prediction, field):
            predicted = getattr(prediction, field)
            break
    
    if not predicted:
        return 0.0
    
    # Exact match: full score
    if predicted == expected:
        return 1.0
    
    # Category match: partial credit
    expected_category = expected.split("/")[0] if "/" in expected else expected
    predicted_category = predicted.split("/")[0] if "/" in predicted else predicted
    
    if expected_category.lower() == predicted_category.lower():
        return 0.7
    
    return 0.0


def composite_metric(example: dspy.Example, prediction: dspy.Prediction, trace=None) -> float:
    """Composite metric combining multiple dimensions.
    
    Weights different quality aspects for balanced optimization.
    This is the recommended approach for production use.
    
    Dimensions:
    - 40%: Taxonomy accuracy (correct placement)
    - 30%: Content quality (structure, examples)
    - 20%: Metadata quality (name, description, tags)
    - 10%: Style alignment (comprehensive vs minimal)
    
    Args:
        example: Training example
        prediction: Model prediction
        trace: Optional trace
    
    Returns:
        Weighted score 0.0-1.0
    """
    # Import sub-metrics
    from skill_fleet.core.dspy.metrics.enhanced_metrics import (
        taxonomy_accuracy_metric,
        metadata_quality_metric,
        skill_style_alignment_metric,
    )
    
    # Calculate component scores
    taxonomy_score = taxonomy_accuracy_metric(example, prediction, trace)
    metadata_score = metadata_quality_metric(example, prediction, trace)
    style_score = skill_style_alignment_metric(example, prediction, trace)
    
    # Content quality (simplified - in production, use full skill_quality_metric)
    content_score = 0.0
    if hasattr(prediction, "skill_content"):
        content = prediction.skill_content
        
        # Check length
        if 500 <= len(content) <= 5000:
            content_score += 0.3
        
        # Check has examples
        if "```" in content:
            content_score += 0.4
        
        # Check has structure
        if content.count("#") >= 3:
            content_score += 0.3
    
    # Weighted combination
    weighted_score = (
        0.4 * taxonomy_score +
        0.3 * content_score +
        0.2 * metadata_score +
        0.1 * style_score
    )
    
    return weighted_score


def create_phase_specific_metric(phase: str):
    """Factory for creating appropriate metric for each phase.
    
    Different workflow phases need different evaluation focus:
    - Phase 1 (Understanding): Taxonomy + intent accuracy
    - Phase 2 (Generation): Comprehensive quality
    - Phase 3 (Validation): Metadata + compliance
    
    Args:
        phase: Phase name ("understanding", "generation", "validation")
    
    Returns:
        Metric function appropriate for that phase
    """
    if phase == "understanding":
        # Focus on intent and taxonomy
        def understanding_metric(ex, pred, trace=None):
            tax_score = taxonomy_accuracy_metric(ex, pred, trace)
            
            # Check topics identified
            topics_score = 0.0
            if hasattr(pred, "topics") and len(pred.topics) >= 3:
                topics_score = 0.5
            
            return 0.7 * tax_score + 0.3 * topics_score
        
        return understanding_metric
    
    elif phase == "generation":
        # Focus on comprehensive quality
        return composite_metric
    
    elif phase == "validation":
        # Focus on compliance
        from skill_fleet.core.dspy.metrics.enhanced_metrics import metadata_quality_metric
        return metadata_quality_metric
    
    else:
        # Default: composite
        return composite_metric


# Usage example
if __name__ == "__main__":
    import dspy
    
    # Create mock example and prediction
    example = dspy.Example(
        task_description="Create async Python skill",
        expected_taxonomy_path="python/async",
        expected_skill_style="comprehensive",
    ).with_inputs("task_description")
    
    prediction = dspy.Prediction(
        domain="python",
        category="async",
        taxonomy_path="python/async",
        topics=["asyncio", "await", "tasks", "event-loop"],
        skill_style="comprehensive",
    )
    
    # Test different metrics
    print("Testing metrics...")
    print(f"Simple: {simple_quality_metric(example, prediction):.3f}")
    print(f"Taxonomy: {taxonomy_accuracy_metric(example, prediction):.3f}")
    print(f"Composite: {composite_metric(example, prediction):.3f}")
    
    # Test phase-specific metrics
    understanding_metric = create_phase_specific_metric("understanding")
    print(f"Understanding: {understanding_metric(example, prediction):.3f}")
