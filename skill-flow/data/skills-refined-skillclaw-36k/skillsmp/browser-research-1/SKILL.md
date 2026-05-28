---
name: browser-research
description: Research web applications and competitors using automated browser interactions
allowed-tools:
  - Bash
  - WebFetch
  - WebSearch
  - Read
  - Write
  - Glob
  - Grep
---

<objective>
Conduct comprehensive research of web applications using browser automation.

Captures:
- Application structure and features
- User interface patterns and flows
- Technical implementation details
- Competitive analysis data
- User experience insights
- Performance and accessibility information

Uses agent-browser for systematic web application research with AI-friendly data extraction.
</objective>

<execution_context>
@~/.claude/ag4one/skills/agent-browser.md
@~/.claude/ag4one/workflows/research-project.md
@~/.claude/ag4one/templates/browser-research/
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/research/ (existing research if any)
</context>

<process>

<step name="validate_research_setup">
```bash
# Check project context
[ -f .planning/PROJECT.md ] || { echo "ERROR: No PROJECT.md found. Run /ag4:new-project first."; exit 1; }

# Validate agent-browser
if ! command -v agent-browser &> /dev/null; then
    echo "ERROR: agent-browser not found. Install with: npm install -g agent-browser"
    exit 1
fi

# Create research directories
mkdir -p .planning/research/browser
mkdir -p .planning/research/browser/screenshots
mkdir -p .planning/research/browser/data
mkdir -p .planning/research/browser/analysis

echo "Browser research setup complete"
```
</step>

<step name="identify_research_targets">
Extract research targets from PROJECT.md or ask user:

Use AskUserQuestion:
- header: "Research targets"
- question: "What web applications or websites should we research?"
- options:
  - "Competitor analysis" — Research competing products
  - "Reference applications" — Study best-in-class examples
  - "Target platform" — Research the platform we're building on
  - "Custom list" — Provide specific URLs to research

For each target, capture:
- Primary URL
- Research focus areas (UI/UX, features, tech stack, etc.)
- Specific pages or flows to analyze
</step>

<step name="create_research_plan">
```bash
# Generate research plan based on targets
cat > .planning/research/browser/plan.md << EOF
# Browser Research Plan

## Research Targets
$(echo "$TARGET_URLS" | tr '\n' '\n- ')

## Research Focus Areas
- User Interface Design
- Feature Set Analysis
- User Experience Flows
- Technical Implementation
- Performance Characteristics
- Accessibility Features

## Data Collection Methods
- Automated screenshots
- DOM structure analysis
- User flow mapping
- Feature inventory
- Performance metrics
- Accessibility audit

## Timeline
$(date): Research initiation
$(date -d "+1 day"): Data collection
$(date -d "+2 days"): Analysis completion
EOF

echo "Research plan created"
```
</step>

<step name="systematic_research">
For each target URL:

```bash
TARGET_URL="$1"
RESEARCH_NAME=$(echo "$TARGET_URL" | sed 's|https\?://||g' | sed 's|[/:.]|_|g')
RESEARCH_DIR=".planning/research/browser/data/$RESEARCH_NAME"

mkdir -p "$RESEARCH_DIR"

# 1. Initial page load analysis
echo "Researching: $TARGET_URL"
agent-browser open "$TARGET_URL"
agent-browser snapshot -i --json > "$RESEARCH_DIR/homepage_snapshot.json"
agent-browser screenshot "$RESEARCH_DIR/homepage.png"
agent-browser screenshot "$RESEARCH_DIR/homepage_full.png" --full

# 2. Technical analysis
echo "Analyzing technical aspects..."
agent-browser eval "JSON.stringify({title: document.title, url: window.location.href, userAgent: navigator.userAgent, language: navigator.language})" > "$RESEARCH_DIR/technical.json"

# 3. Feature and structure analysis
echo "Capturing page structure..."
agent-browser get text "body" --json > "$RESEARCH_DIR/content.json"
agent-browser eval "Array.from(document.querySelectorAll('nav, header, main, aside, footer')).map(el => ({tag: el.tagName, className: el.className, id: el.id}))" > "$RESEARCH_DIR/structure.json"

# 4. Accessibility audit
echo "Running accessibility checks..."
agent-browser eval "JSON.stringify({hasAltText: document.querySelectorAll('img:not([alt])').length, hasAriaLabels: document.querySelectorAll('[aria-label]').length, hasHeadings: document.querySelectorAll('h1, h2, h3, h4, h5, h6').length})" > "$RESEARCH_DIR/accessibility.json"

# 5. Performance indicators
echo "Capturing performance data..."
agent-browser eval "JSON.stringify({totalImages: document.images.length, totalScripts: document.scripts.length, totalLinks: document.links.length, totalForms: document.forms.length})" > "$RESEARCH_DIR/performance.json"

agent-browser close
```

</step>

<step name="analyze_user_flows">
For key user flows (login, signup, main actions):

```bash
# Example: Authentication flow analysis
if [[ "$RESEARCH_AUTH_FLOW" == "true" ]]; then
    echo "Analyzing authentication flow..."
    
    # Find login/signup links
    agent-browser open "$TARGET_URL"
    agent-browser snapshot -i --json > "$RESEARCH_DIR/auth_flow_snapshot.json"
    
    # Attempt to navigate through auth flow
    # (Implementation depends on specific site structure)
    
    agent-browser close
fi
```
</step>

<step name="competitive_analysis">
```bash
# Compile competitive analysis
cat > .planning/research/browser/competitive_analysis.md << EOF
# Competitive Analysis

## Research Summary
- **Date:** $(date)
- **Targets Analyzed:** $(echo "$TARGET_URLS" | wc -l)
- **Research Duration:** $(date -d "1 day ago" +%Y-%m-%d) to $(date +%Y-%m-%d)

## Key Findings

### UI/UX Patterns
$(find .planning/research/browser/data -name "structure.json" -exec echo "File: {}" \; -exec cat {} \;)

### Common Features
$(find .planning/research/browser/data -name "content.json" -exec grep -o "login\|signup\|dashboard\|profile" {} \; | sort | uniq -c)

### Technical Approaches
$(find .planning/research/browser/data -name "technical.json" -exec echo "Site: $(basename $(dirname {}))" \; -exec cat {} \;)

### Performance Characteristics
$(find .planning/research/browser/data -name "performance.json" -exec echo "Site: $(basename $(dirname {}))" \; -exec cat {} \;)

## Recommendations

### For Our Project
Based on research findings:
1. **Essential Features:** [List critical features found across competitors]
2. **UI Patterns:** [Common design patterns to consider]
3. **Technical Considerations:** [Technical approaches observed]
4. **User Expectations:** [Features users expect in this domain]

### Differentiation Opportunities
1. **Missing Features:** [Gaps in competitor offerings]
2. **UX Improvements:** [Areas where competitors fall short]
3. **Technical Innovations:** [Opportunities for technical advantages]

EOF

echo "Competitive analysis complete"
```
</step>

<step name="generate_insights">
```bash
# Generate actionable insights
cat > .planning/research/browser/insights.md << EOF
# Browser Research Insights

## What We Learned

### Industry Standards
- **Expected Features:** $(grep -r "login\|signup\|dashboard" .planning/research/browser/data/ | wc -l) common features identified
- **UI Conventions:** $(find .planning/research/browser/data -name "structure.json" | wc -l) navigation patterns analyzed
- **Technical Norms:** JavaScript frameworks, responsive design approaches

### User Expectations
- **Core Functionality:** Essential features every competitor has
- **User Experience:** Common interaction patterns and flows
- **Performance Expectations:** Loading times, mobile responsiveness

### Technical Landscape
- **Frontend Technologies:** Common frameworks and libraries
- **Backend Patterns:** API structures, authentication methods
- **Third-party Integrations:** Analytics, payments, social login

## Implications for Our Project

### Must-Have Features
1. Based on competitor analysis, our project needs:
   - User authentication system
   - [List other essential features]

### Technical Decisions
1. Technology stack recommendations
2. Architecture considerations
3. Integration requirements

### UX Strategy
1. Design patterns to follow
2. User flows to implement
3. Accessibility requirements

## Next Steps
- Incorporate insights into requirements definition
- Use findings to inform technical architecture
- Reference screenshots and data during design phase

EOF

echo "Research insights generated"
```
</step>

<step name="compile_research_report">
```bash
# Final research compilation
cat > .planning/research/BROWSER_RESEARCH_SUMMARY.md << EOF
# Browser Research Summary

## Research Overview
- **Conducted:** $(date)
- **Targets:** $(echo "$TARGET_URLS" | tr '\n' ', ')
- **Focus:** Competitive analysis and feature research

## Key Documents
- [Detailed Analysis](.planning/research/browser/competitive_analysis.md)
- [Research Insights](.planning/research/browser/insights.md)
- [Raw Data](.planning/research/browser/data/)
- [Screenshots](.planning/research/browser/screenshots/)

## Executive Summary
Our browser research revealed:
1. **Market Standards:** [Brief summary]
2. **Feature Gaps:** [Opportunities identified]
3. **Technical Requirements:** [Technical implications]

## Integration with Project
This research informs:
- Feature prioritization in requirements
- Technical architecture decisions  
- UI/UX design direction
- Competitive positioning strategy

---

*Research conducted using agent-browser automation for consistent, comprehensive analysis.*
EOF

echo "Research summary compiled"
```
</step>

<step name="done">
```
Browser research complete:

- Competitive analysis: .planning/research/browser/competitive_analysis.md
- Research insights: .planning/research/browser/insights.md
- Raw data: .planning/research/browser/data/
- Screenshots: .planning/research/browser/screenshots/
- Summary: .planning/research/BROWSER_RESEARCH_SUMMARY.md

---

## ▶ Next Up

**Define requirements** — Use research insights to scope your project

`/ag4:define-requirements`

<sub>`/clear` first → fresh context window</sub>

**Flow:** browser-research → define-requirements → create-roadmap

---
```
</step>

</process>

<when_to_use>
**Use browser-research for:**
- Understanding competitive landscape before building
- Analyzing user interface patterns and conventions
- Identifying essential features in a domain
- Researching technical approaches used by competitors
- Gathering screenshots and examples for reference
- Understanding user expectations in a market

**Skip browser-research for:**
- Well-defined internal projects with clear requirements
- API/backend projects without user interface components
- Projects where you already know the domain well
</when_to_use>

<success_criteria>
- [ ] Research targets identified and confirmed
- [ ] Systematic browser automation executed
- [ ] Screenshots and data captured for each target
- [ ] Competitive analysis created
- [ ] Actionable insights generated
- [ ] Research integrated with project context
- [ ] Clear recommendations for next steps
</success_criteria>