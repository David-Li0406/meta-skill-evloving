# Review Modes

## Table of Contents

- [Mode Comparison](#mode-comparison)
- [Quick Review (--quick)](#quick-review---quick)
- [Standard Review (default)](#standard-review-default)
- [Detailed Review (--detailed)](#detailed-review---detailed)
- [Component-Specific Review (--components)](#component-specific-review---components)
- [Mode Selection Guide](#mode-selection-guide)
- [Time Estimates](#time-estimates)

## Mode Comparison

| Mode | Duration | Depth | Coverage | Best For |
|------|----------|-------|----------|----------|
| **Quick** | 2-3 min | High-level | Major issues | Initial assessment |
| **Standard** | 5-10 min | Comprehensive | All components | Complete quality check |
| **Detailed** | 10-15 min | Deep dive | Code-level | Pre-refinement planning |
| **Component** | Variable | Focused | Selected areas | Targeted improvements |

---

## Quick Review (--quick)

### Purpose
Fast initial assessment to identify major issues

### Scope
- Architecture overview
- Critical issues only
- Major structural problems
- Essential compliance

### What It Checks
```
✓ Plugin manifest exists and valid
✓ Directory structure basic compliance
✓ Skills directory present
✓ Major architecture violations
✓ Critical security issues
✓ Missing mandatory components
```

### What It Skips
```
✗ Detailed component analysis
✗ Code-level review
✗ Best practices optimization
✗ Minor issues
✗ Performance considerations
```

### Output
```
Plugin: my-plugin
Score: 6.5/10 (Fair)
Status: ⚠️ Issues Found

Major Issues:
- Missing mandatory URL sections (3 skills)
- Incomplete plugin manifest
- Generic triggers (5 skills)

Quick Actions:
1. Run standard review for full analysis
2. Fix critical issues immediately
3. Consider refinement cycle
```

### When to Use
- First time assessing a plugin
- Quick health check
- Before detailed work
- Screening multiple plugins
- Time-constrained situations

### Example
```bash
/plugin-review-orchestrator /path/to/plugin --quick
# Result: 2-3 minute assessment
```

---

## Standard Review (default)

### Purpose
Comprehensive quality assessment

### Scope
- Full architecture analysis
- All component review
- Complete compliance check
- Detailed scoring

### What It Checks
```
✓ Structural (architecture, structure, disclosure)
✓ Components (skills, commands, agents, hooks)
✓ Standards (URLs, best practices)
✓ Progressive disclosure implementation
✓ Auto-discovery optimization
✓ Security considerations
✓ Performance implications
```

### Output
```
Plugin: my-plugin
Score: 7.7/10 (Good)
Grade: B+

Detailed Findings:
==================

Architecture: 8/10
  ✅ Skills-first approach
  ✅ Good directory structure
  ⚠️ Progressive disclosure incomplete

Skills: 12/15
  ✅ All have YAML frontmatter
  ✅ Clear triggers
  ⚠️ 2 missing mandatory URLs

Commands: 8/10
  ✅ Proper format
  ⚠️ Auto-discovery issues

Recommendations:
================
HIGH (Critical):
1. Add mandatory URLs (2 skills)
2. Fix manifest fields

MEDIUM (Important):
1. Enhance disclosure (5 skills)
2. Improve triggers

LOW (Nice):
1. Add examples
2. Polish workflows
```

### When to Use
- Complete quality assessment
- Before refinement
- Regular maintenance
- Documentation needs
- Standard workflow

### Example
```bash
/plugin-review-orchestrator /path/to/plugin
# Result: 5-10 minute comprehensive review
```

---

## Detailed Review (--detailed)

### Purpose
In-depth analysis for planning and optimization

### Scope
- Code-level examination
- Pattern analysis
- Optimization opportunities
- Best practice deep dive

### What It Checks
```
✓ Line-by-line code review
✓ Pattern appropriateness
✓ Performance optimization
✓ Security audit
✓ Accessibility compliance
✓ Maintainability metrics
✓ Technical debt assessment
✓ Integration quality
```

### Output
```
Plugin: my-plugin (Detailed Analysis)
Score: 8.2/10 (Very Good)
Grade: A-

Technical Analysis:
==================

Skill: api-review
- Frontmatter: ✅ Complete
- URL sections: ⚠️ Needs update
- Trigger quality: ✅ Specific
- Code patterns: ✅ Good
- Performance: ✅ Optimized
- Security: ✅ Secure
- Accessibility: ⚠️ Minor issues

Skill: data-processor
- Frontmatter: ✅ Complete
- URL sections: ✅ Current
- Trigger quality: ✅ Clear
- Code patterns: ⚠️ Over-engineered
- Performance: ⚠️ Could optimize
- Security: ✅ Secure
- Accessibility: ✅ Good

Optimization Opportunities:
1. Simplify data-processor workflow
2. Update api-review URLs
3. Add accessibility features
4. Optimize performance bottlenecks

Best Practices:
1. Consider using progressive disclosure better
2. Add comprehensive examples
3. Implement automated testing
```

### When to Use
- Pre-refinement planning
- Optimization projects
- Technical deep dives
- Quality audits
- Expert review

### Example
```bash
/plugin-review-orchestrator /path/to/plugin --detailed
# Result: 10-15 minute thorough analysis
```

---

## Component-Specific Review (--components)

### Purpose
Focused review of selected component types

### Scope
- Targeted component analysis
- Deep dive into specific areas
- Specialized assessment
- Detailed recommendations

### Component Types

#### Skills Focus
```bash
/plugin-review-orchestrator /path/to/plugin --components skills
```
**Checks**:
- YAML frontmatter quality
- Mandatory URL sections
- Trigger effectiveness
- Progressive disclosure
- Autonomy level
- Documentation quality

#### Commands Focus
```bash
/plugin-review-orchestrator /path/to/plugin --components commands
```
**Checks**:
- Format compliance
- Instruction clarity
- Auto-discovery
- Orchestration quality
- Context injection
- Workflow effectiveness

#### Agents Focus
```bash
/plugin-review-orchestrator /path/to/plugin --components agents
```
**Checks**:
- Prompt quality
- Pattern selection
- Autonomy definition
- Specialization clarity
- Coordination efficiency
- Performance metrics

#### Hooks Focus
```bash
/plugin-review-orchestrator /path/to/plugin --components hooks
```
**Checks**:
- Configuration accuracy
- Security measures
- Event matching
- Automation value
- Performance impact
- Error handling

#### Combined Focus
```bash
/plugin-review-orchestrator /path/to/plugin --components skills,commands
```
**Checks**:
- Both skills and commands
- Integration quality
- Orchestration effectiveness
- Duplication prevention
- Workflow optimization

### Output
```
Component Review: Skills
========================

Skills Found: 5
Analyzed: 5
Issues: 7
Recommendations: 12

Skill-by-Skill Analysis:
------------------------

1. api-review
   Score: 9/10
   Status: ✅ Excellent
   Notes: Follows all best practices

2. data-processor
   Score: 6/10
   Status: ⚠️ Needs work
   Issues:
   - Missing mandatory URLs
   - Generic triggers
   - Incomplete disclosure

Recommendations:
================
1. Add mandatory URL sections (2 skills)
2. Improve trigger specificity (3 skills)
3. Enhance progressive disclosure (4 skills)
4. Optimize workflows (2 skills)

Priority Actions:
================
HIGH:
- Fix missing URLs
- Update generic triggers

MEDIUM:
- Enhance disclosure
- Optimize workflows

LOW:
- Add examples
- Polish documentation
```

### When to Use
- Targeted improvements
- Component-specific issues
- Expert review of area
- Incremental refinement
- Specialized assessment

### Example
```bash
/plugin-review-orchestrator /path/to/plugin --components skills
# Result: Focused skill analysis
```

---

## Mode Selection Guide

### Decision Matrix

**Choose Quick when**:
- Time is limited (< 5 minutes)
- Initial assessment needed
- Screening multiple plugins
- Identifying major issues

**Choose Standard when**:
- Regular quality check
- Before refinement
- Complete review needed
- Documentation required

**Choose Detailed when**:
- Pre-refinement planning
- Optimization project
- Expert review needed
- Technical deep dive

**Choose Component when**:
- Targeted improvements
- Specific issues known
- Incremental updates
- Specialized review

### Recommended Workflow

1. **Quick Review** (Initial scan)
   - Identify major issues
   - Determine if worth detailed review
   - Screen multiple plugins

2. **Standard Review** (Comprehensive)
   - Full quality assessment
   - Complete findings
   - Prioritized recommendations

3. **Component Review** (Targeted)
   - Focus on problem areas
   - Detailed analysis
   - Specific improvements

4. **Detailed Review** (Planning)
   - Pre-refinement
   - Optimization
   - Expert assessment

---

## Time Estimates

### Quick Review
- Start to finish: 2-3 minutes
- Analysis: 1-2 minutes
- Report: 30 seconds

### Standard Review
- Start to finish: 5-10 minutes
- Analysis: 4-8 minutes
- Report: 1-2 minutes

### Detailed Review
- Start to finish: 10-15 minutes
- Analysis: 8-12 minutes
- Report: 2-3 minutes

### Component Review
- Start to finish: 3-8 minutes
- Analysis: 2-6 minutes
- Report: 1-2 minutes

**Note**: Times vary based on plugin complexity and component count.
