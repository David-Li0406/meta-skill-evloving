#!/usr/bin/env python3
"""
Agent Quality Validator - 0-70 Scoring Rubric

Validates agent quality across 7 categories:
- Phase Structure (0-15 pts)
- Success Criteria (0-15 pts)
- Self-Critique (0-10 pts)
- Progressive Disclosure (0-10 pts)
- Tool Usage (0-10 pts)
- Documentation (0-10 pts)
- Edge Case Handling (0-10 pts)

Total: 0-70 points
60+ = Excellent (production ready)
50-59 = Good (minor improvements)
40-49 = Fair (significant improvements)
<40 = Poor (major refactoring)
"""

import sys
import re
from pathlib import Path

def validate_agent(agent_path):
    """Validate agent and return score breakdown"""
    agent_path = Path(agent_path)

    if not agent_path.exists():
        return {
            'total': 0,
            'max': 70,
            'error': f"Agent file not found: {agent_path}"
        }

    content = agent_path.read_text()

    # Initialize scoring
    scores = {
        'phase_structure': {'score': 0, 'max': 15, 'details': []},
        'success_criteria': {'score': 0, 'max': 15, 'details': []},
        'self_critique': {'score': 0, 'max': 10, 'details': []},
        'progressive_disclosure': {'score': 0, 'max': 10, 'details': []},
        'tool_usage': {'score': 0, 'max': 10, 'details': []},
        'documentation': {'score': 0, 'max': 10, 'details': []},
        'edge_cases': {'score': 0, 'max': 10, 'details': []},
    }

    # Extract frontmatter
    frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    frontmatter = frontmatter_match.group(1) if frontmatter_match else ""

    # 1. Phase Structure (0-15 pts)
    phases = re.findall(r'##\s+Phase\s+\d+:', content, re.IGNORECASE)
    phase_count = len(phases)

    if 3 <= phase_count <= 5:
        scores['phase_structure']['score'] += 10
        scores['phase_structure']['details'].append(f"✅ Optimal phase count: {phase_count}")
    elif phase_count == 2:
        scores['phase_structure']['score'] += 5
        scores['phase_structure']['details'].append(f"⚠️  Only {phase_count} phases (3-5 recommended)")
    elif phase_count > 5:
        scores['phase_structure']['score'] += 5
        scores['phase_structure']['details'].append(f"⚠️  Too many phases: {phase_count} (3-5 recommended)")
    else:
        scores['phase_structure']['details'].append(f"❌ No phase structure found")

    # Check for Objectives and Deliverables
    objectives = re.findall(r'\*\*Objective\*\*:', content, re.IGNORECASE)
    deliverables = re.findall(r'\*\*Deliverable\*\*:', content, re.IGNORECASE)

    if len(objectives) >= phase_count * 0.8:  # At least 80% of phases have objectives
        scores['phase_structure']['score'] += 3
        scores['phase_structure']['details'].append(f"✅ {len(objectives)} phases have objectives")
    else:
        scores['phase_structure']['details'].append(f"❌ Only {len(objectives)}/{phase_count} phases have objectives")

    if len(deliverables) >= phase_count * 0.8:
        scores['phase_structure']['score'] += 2
        scores['phase_structure']['details'].append(f"✅ {len(deliverables)} phases have deliverables")
    else:
        scores['phase_structure']['details'].append(f"❌ Only {len(deliverables)}/{phase_count} phases have deliverables")

    # 2. Success Criteria (0-15 pts)
    success_section = re.search(r'\n##\s+Success\s+Criteria(.*?)(?=\n##\s+[^#]|\Z)', content, re.DOTALL | re.IGNORECASE)
    if success_section:
        success_items = re.findall(r'[-\*]\s+[✅✓]', success_section.group(1))
        count = len(success_items)

        if 10 <= count <= 16:
            scores['success_criteria']['score'] += 15
            scores['success_criteria']['details'].append(f"✅ Optimal criteria count: {count}")
        elif 7 <= count < 10:
            scores['success_criteria']['score'] += 10
            scores['success_criteria']['details'].append(f"⚠️  Criteria count: {count} (10-16 recommended)")
        elif count > 16:
            scores['success_criteria']['score'] += 10
            scores['success_criteria']['details'].append(f"⚠️  Too many criteria: {count} (10-16 recommended)")
        elif count > 0:
            scores['success_criteria']['score'] += 5
            scores['success_criteria']['details'].append(f"❌ Too few criteria: {count} (10-16 recommended)")
    else:
        scores['success_criteria']['details'].append("❌ No Success Criteria section found")

    # 3. Self-Critique (0-10 pts)
    critique_section = re.search(r'\n##\s+Self-Critique[^\n]*(.*?)(?=\n##\s+[^#]|\Z)', content, re.DOTALL | re.IGNORECASE)
    if critique_section:
        # Count questions (numbered or bullet points followed by questions)
        questions = re.findall(r'(\d+\.|\*|-)\s+\*\*[^*]+\*\*:', critique_section.group(1))
        count = len(questions)

        if 6 <= count <= 10:
            scores['self_critique']['score'] += 10
            scores['self_critique']['details'].append(f"✅ Optimal question count: {count}")
        elif 4 <= count < 6:
            scores['self_critique']['score'] += 6
            scores['self_critique']['details'].append(f"⚠️  Question count: {count} (6-10 recommended)")
        elif count > 10:
            scores['self_critique']['score'] += 8
            scores['self_critique']['details'].append(f"⚠️  Too many questions: {count} (6-10 recommended)")
        elif count > 0:
            scores['self_critique']['score'] += 3
            scores['self_critique']['details'].append(f"❌ Too few questions: {count} (6-10 recommended)")
    else:
        scores['self_critique']['details'].append("❌ No Self-Critique section found")

    # 4. Progressive Disclosure (0-10 pts)
    line_count = len(content.split('\n'))
    reference_docs = re.findall(r'\*\*Reference Documentation\*\*:|references/[a-z-]+\.md', content, re.IGNORECASE)

    if 150 <= line_count <= 250:
        scores['progressive_disclosure']['score'] += 10
        scores['progressive_disclosure']['details'].append(f"✅ Optimal length: {line_count} lines")
    elif 100 <= line_count < 150:
        scores['progressive_disclosure']['score'] += 8
        scores['progressive_disclosure']['details'].append(f"⚠️  Short: {line_count} lines (150-250 ideal)")
    elif 250 < line_count <= 300:
        if len(reference_docs) > 0:
            scores['progressive_disclosure']['score'] += 8
            scores['progressive_disclosure']['details'].append(f"⚠️  {line_count} lines with references (good)")
        else:
            scores['progressive_disclosure']['score'] += 4
            scores['progressive_disclosure']['details'].append(f"❌ {line_count} lines, no references (extract to refs)")
    elif line_count > 300:
        if len(reference_docs) > 0:
            scores['progressive_disclosure']['score'] += 6
            scores['progressive_disclosure']['details'].append(f"⚠️  Long ({line_count} lines) but has references")
        else:
            scores['progressive_disclosure']['score'] += 2
            scores['progressive_disclosure']['details'].append(f"❌ Too long: {line_count} lines (extract to refs)")
    else:
        scores['progressive_disclosure']['score'] += 6
        scores['progressive_disclosure']['details'].append(f"⚠️  Very short: {line_count} lines")

    # 5. Tool Usage (0-10 pts)
    tools_match = re.search(r'tools:\s*([^\n]+)', frontmatter)
    if tools_match:
        declared_tools = [t.strip() for t in tools_match.group(1).split(',')]
        scores['tool_usage']['score'] += 5
        scores['tool_usage']['details'].append(f"✅ Tools declared: {len(declared_tools)}")

        # Check if declared tools are used in phases
        unused_tools = []
        for tool in declared_tools:
            # Search for tool usage in phases (case-insensitive)
            if not re.search(rf'\b{re.escape(tool)}\b', content, re.IGNORECASE):
                unused_tools.append(tool)

        if len(unused_tools) == 0:
            scores['tool_usage']['score'] += 5
            scores['tool_usage']['details'].append(f"✅ All declared tools are used")
        elif len(unused_tools) <= 2:
            scores['tool_usage']['score'] += 3
            scores['tool_usage']['details'].append(f"⚠️  {len(unused_tools)} tools unused: {', '.join(unused_tools)}")
        else:
            scores['tool_usage']['score'] += 1
            scores['tool_usage']['details'].append(f"❌ {len(unused_tools)} tools unused: {', '.join(unused_tools[:3])}...")
    else:
        scores['tool_usage']['details'].append("❌ No tools declared in frontmatter")

    # 6. Documentation (0-10 pts)
    has_examples = bool(re.search(r'##\s+(Example|Usage|Quick Start)', content, re.IGNORECASE))
    has_description = bool(re.search(r'description:\s*[^\n]+', frontmatter))
    has_purpose = bool(re.search(r'\*\*Purpose\*\*:', content))
    has_references = len(reference_docs) > 0

    if has_examples:
        scores['documentation']['score'] += 3
        scores['documentation']['details'].append("✅ Examples included")
    else:
        scores['documentation']['details'].append("❌ No examples section")

    if has_description:
        scores['documentation']['score'] += 3
        scores['documentation']['details'].append("✅ Description in frontmatter")
    else:
        scores['documentation']['details'].append("❌ No description in frontmatter")

    if has_purpose:
        scores['documentation']['score'] += 2
        scores['documentation']['details'].append("✅ Purpose statement")

    if has_references:
        scores['documentation']['score'] += 2
        scores['documentation']['details'].append(f"✅ {len(reference_docs)} reference docs")

    # 7. Edge Case Handling (0-10 pts)
    edge_case_keywords = [
        r'edge\s+case', r'error', r'fail', r'exception', r'missing',
        r'invalid', r'empty', r'null', r'undefined', r'timeout', r'boundary'
    ]
    edge_case_mentions = sum(len(re.findall(pattern, content, re.IGNORECASE)) for pattern in edge_case_keywords)

    if edge_case_mentions >= 10:
        scores['edge_cases']['score'] += 10
        scores['edge_cases']['details'].append(f"✅ Comprehensive edge case handling ({edge_case_mentions} mentions)")
    elif edge_case_mentions >= 5:
        scores['edge_cases']['score'] += 7
        scores['edge_cases']['details'].append(f"⚠️  Adequate edge case handling ({edge_case_mentions} mentions)")
    elif edge_case_mentions >= 2:
        scores['edge_cases']['score'] += 4
        scores['edge_cases']['details'].append(f"⚠️  Minimal edge case handling ({edge_case_mentions} mentions)")
    else:
        scores['edge_cases']['details'].append(f"❌ No edge case handling found")

    # Check for temporal awareness (bonus insight, not scored separately)
    temporal_pattern = r'CURRENT_DATE.*date\s+[\'"]'
    has_temporal = bool(re.search(temporal_pattern, content, re.IGNORECASE))

    # Calculate total
    total_score = sum(s['score'] for s in scores.values())
    max_score = sum(s['max'] for s in scores.values())

    return {
        'total': total_score,
        'max': max_score,
        'scores': scores,
        'has_temporal': has_temporal,
        'phase_count': phase_count,
        'line_count': line_count,
        'grade': get_grade(total_score)
    }

def get_grade(score):
    """Convert score to grade (0-80 scale)"""
    if score >= 70:
        return "Excellent"
    elif score >= 60:
        return "Good"
    elif score >= 50:
        return "Fair"
    else:
        return "Poor"

def print_report(result):
    """Print formatted validation report"""
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
        return

    # Header
    print(f"\n{'='*60}")
    print(f"Agent Quality Validation Report")
    print(f"{'='*60}\n")

    # Overall score
    grade = result['grade']
    emoji = "✅" if result['total'] >= 60 else "⚠️" if result['total'] >= 40 else "❌"
    print(f"{emoji} Quality Score: {result['total']}/{result['max']} ({grade})")
    print()

    # Category breakdown
    print("Category Breakdown:")
    print("-" * 60)

    for category, data in result['scores'].items():
        score = data['score']
        max_score = data['max']
        percentage = (score / max_score * 100) if max_score > 0 else 0
        emoji = "✅" if percentage >= 80 else "⚠️" if percentage >= 60 else "❌"

        category_name = category.replace('_', ' ').title()
        print(f"\n{emoji} {category_name}: {score}/{max_score} ({percentage:.0f}%)")
        for detail in data['details']:
            print(f"   {detail}")

    # Temporal awareness check
    print(f"\n{'='*60}")
    if result['has_temporal']:
        print("✅ Temporal Awareness: FOUND in Phase 1")
    else:
        print("❌ Temporal Awareness: NOT FOUND (add date checking in Phase 1)")

    # Recommendations
    print(f"\n{'='*60}")
    print("Recommendations:")
    print("-" * 60)

    recommendations = []

    if result['scores']['success_criteria']['score'] < 10:
        target_count = 10 if result['total'] < 70 else 12
        recommendations.append(f"• Add more success criteria (target: {target_count}-16 items)")

    if result['scores']['self_critique']['score'] < 8:
        recommendations.append("• Add domain-specific self-critique questions (target: 6-10)")

    if result['scores']['edge_cases']['score'] < 5:
        recommendations.append("• Document edge cases and error handling")

    if result['scores']['documentation']['score'] < 7:
        recommendations.append("• Add examples and usage documentation")

    if result['line_count'] > 250 and result['scores']['progressive_disclosure']['score'] < 8:
        recommendations.append("• Extract details to references/ for progressive disclosure")

    if not result['has_temporal']:
        recommendations.append("• Add temporal awareness (REQUIRED) in Phase 1")

    if result['scores']['tool_usage']['score'] < 8:
        recommendations.append("• Remove unused tools from frontmatter or use them in phases")

    if not recommendations:
        recommendations.append("• Excellent! No major improvements needed.")

    for rec in recommendations:
        print(rec)

    # Final verdict
    print(f"\n{'='*60}")
    if result['total'] >= 70:
        print("✅ VERDICT: Production Ready - Ship it!")
    elif result['total'] >= 60:
        print("⚠️  VERDICT: Almost There - Minor improvements recommended")
    elif result['total'] >= 50:
        print("⚠️  VERDICT: Needs Work - Significant improvements required")
    else:
        print("❌ VERDICT: Major Refactoring Required")
    print(f"{'='*60}\n")

def main():
    if len(sys.argv) != 2:
        print("Usage: validate_agent.py <path/to/agent.md>")
        print("\nExample:")
        print("  validate_agent.py ~/.claude/agents-library/my-agent.md")
        sys.exit(1)

    agent_path = sys.argv[1]
    print(f"Validating agent: {agent_path}\n")

    result = validate_agent(agent_path)
    print_report(result)

    # Exit code based on score
    if result['total'] >= 60:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Needs improvement

if __name__ == "__main__":
    main()
