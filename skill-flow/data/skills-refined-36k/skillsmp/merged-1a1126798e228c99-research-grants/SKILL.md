---
name: research-grants
description: Write competitive research proposals for NSF, NIH, DOE, DARPA, and Taiwan NSTC, focusing on agency-specific formatting, review criteria, budget preparation, broader impacts, significance statements, innovation narratives, and compliance with submission requirements.
---

# Research Grant Writing

## Overview

Research grant writing is the process of developing competitive funding proposals for federal agencies and foundations. Master agency-specific requirements, review criteria, narrative structure, budget preparation, and compliance for NSF (National Science Foundation), NIH (National Institutes of Health), DOE (Department of Energy), DARPA (Defense Advanced Research Projects Agency), and Taiwan's NSTC (National Science and Technology Council) submissions.

**Critical Principle: Grants are persuasive documents that must simultaneously demonstrate scientific rigor, innovation, feasibility, and broader impact.** Each agency has distinct priorities, review criteria, formatting requirements, and strategic goals that must be addressed.

## When to Use This Skill

This skill should be used when:
- Writing research proposals for NSF, NIH, DOE, DARPA, or NSTC programs
- Preparing project descriptions, specific aims, or technical narratives
- Developing broader impacts or significance statements
- Creating research timelines and milestone plans
- Preparing budget justifications and personnel allocation plans
- Responding to program solicitations or funding announcements
- Addressing reviewer comments in resubmissions
- Planning multi-institutional collaborative proposals
- Writing preliminary data or feasibility sections
- Preparing biosketches, CVs, or facilities descriptions

## Visual Enhancement with Scientific Schematics

**⚠️ MANDATORY: Every research grant proposal MUST include at least 1-2 AI-generated figures using the scientific-schematics skill.**

This is not optional. Grant proposals without visual elements are incomplete and less competitive. Before finalizing any document:
1. Generate at minimum ONE schematic or diagram (e.g., project timeline, methodology flowchart, or conceptual framework)
2. Prefer 2-3 figures for comprehensive proposals (research workflow, Gantt chart, preliminary data visualization)

**How to generate figures:**
- Use the **scientific-schematics** skill to generate AI-powered publication-quality diagrams
- Simply describe your desired diagram in natural language
- Nano Banana Pro will automatically generate, review, and refine the schematic

**How to generate schematics:**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

The AI will automatically:
- Create publication-quality images with proper formatting
- Review and refine through multiple iterations
- Ensure accessibility (colorblind-friendly, high contrast)
- Save outputs in the figures/ directory

**When to add schematics:**
- Research methodology and workflow diagrams
- Project timeline Gantt charts
- Conceptual framework illustrations
- System architecture diagrams (for technical proposals)
- Experimental design flowcharts
- Broader impacts activity diagrams
- Collaboration network diagrams
- Any complex concept that benefits from visualization

For detailed guidance on creating schematics, refer to the scientific-schematics skill documentation.

---

## Agency-Specific Overview

### NSF (National Science Foundation)
**Mission**: Promote the progress of science and advance national health, prosperity, and welfare

**Key Features**:
- Intellectual Merit + Broader Impacts (equally weighted)
- 15-page project description limit (most programs)
- Emphasis on education, diversity, and societal benefit
- Collaborative research encouraged
- Open data and open science emphasis
- Merit review process with panel + ad hoc reviewers

### NIH (National Institutes of Health)
**Mission**: Enhance health, lengthen life, and reduce illness and disability

**Key Features**:
- Specific Aims (1 page) + Research Strategy (12 pages for R01)
- Significance, Innovation, Approach as core review criteria
- Preliminary data typically required for R01s
- Emphasis on rigor, reproducibility, and clinical relevance
- Modular budgets ($250K increments) for most R01s
- Multiple resubmission opportunities

### DOE (Department of Energy)
**Mission**: Ensure America's security and prosperity through energy, environmental, and nuclear challenges

**Key Features**:
- Focus on energy, climate, computational science, basic energy sciences
- Often requires cost sharing or industry partnerships
- Emphasis on national laboratory collaboration
- Strong computational and experimental integration
- Energy innovation and commercialization pathways
- Varies by office (ARPA-E, Office of Science, EERE, etc.)

### DARPA (Defense Advanced Research Projects Agency)
**Mission**: Make pivotal investments in breakthrough technologies for national security

**Key Features**:
- High-risk, high-reward transformative research
- Focus on "DARPA-hard" problems (what if true, who cares)
- Emphasis on prototypes, demonstrations, and transition paths
- Often requires multiple phases (feasibility, development, demonstration)
- Strong project management and milestone tracking
- Teaming and collaboration often required
- Varies dramatically by program manager and BAA (Broad Agency Announcement)

### NSTC (National Science and Technology Council - Taiwan)
**Mission**: Advance scientific breakthrough, industrial application, and societal impact in Taiwan.

**Key Features**:
- **CM03 Form**: The core technical proposal format.
- **Bilingual**: Abstract required in both Chinese and English.
- **Innovation & Feasibility**: Primary review focus.
- **Preliminary Data**: Highly critical for credibility.
- **Research Architecture Diagram**: A mandatory visual element for clarity.

## Core Components of Research Proposals

### 1. Executive Summary / Project Summary / Abstract

Every proposal needs a concise overview that communicates the essential elements of the research to both technical reviewers and program officers.

**Purpose**: Provide a standalone summary that captures the research vision, significance, and approach

**Length**: 
- NSF: 1 page (Project Summary with separate Overview, Intellectual Merit, Broader Impacts)
- NIH: 30 lines (Project Summary/Abstract)
- DOE: Varies (typically 1 page)
- DARPA: Varies (often 1-2 pages)

**Essential Elements**:
- Clear statement of the problem or research question
- Why this problem matters (significance, urgency, impact)
- Novel approach or innovation
- Expected outcomes and deliverables
- Qualifications of the team
- Broader impacts or translational pathway

**Writing Strategy**:
- Open with a compelling hook that establishes importance
- Use accessible language (avoid jargon in opening sentences)
- State specific, measurable objectives
- Convey enthusiasm and confidence
- Ensure every sentence adds value (no filler)
- End with transformative vision or impact statement

**Common Mistakes to Avoid**:
- Being too technical or detailed (save for project description)
- Failing to articulate "why now" or "why this team"
- Vague objectives or outcomes
- Neglecting broader impacts or significance
- Generic statements that could apply to any proposal

### 2. Project Description / Research Strategy

The core technical narrative that presents the research plan in detail.

**Structure Varies by Agency:**

**NSF Project Description** (typically 15 pages):
- Introduction and background
- Research objectives and questions
- Preliminary results (if applicable)
- Research plan and methodology
- Timeline and milestones
- Broader impacts (integrated throughout or separate section)
- Prior NSF support (if applicable)

**NIH Research Strategy** (12 pages for R01):
- Significance (why the problem matters)
- Innovation (what's novel and transformative)
- Approach (detailed research plan)
  - Preliminary data
  - Research design and methods
  - Expected outcomes
  - Potential problems and alternative approaches

**DOE Project Narrative** (varies):
- Background and significance
- Technical approach and innovation
- Qualifications and experience
- Facilities and resources
- Project management and timeline

**DARPA Technical Volume** (varies):
- Technical challenge and innovation
- Approach and methodology
- Schedule and milestones
- Deliverables and metrics
- Team qualifications
- Risk assessment and mitigation

For detailed agency-specific guidance, refer to:
- `references/nsf_guidelines.md`
- `references/nih_guidelines.md`
- `references/doe_guidelines.md`
- `references/darpa_guidelines.md`
- `references/nstc_guidelines.md`

### 3. Specific Aims (NIH) or Objectives (NSF/DOE/DARPA)

Clear, testable goals that structure the research plan.

**NIH Specific Aims Page** (1 page):
- Opening paragraph: Gap in knowledge and significance
- Long-term goal and immediate objectives
- Central hypothesis or research question
- 2-4 specific aims with sub-aims
- Expected outcomes and impact
- Payoff paragraph: Why this matters

**Structure for Each Aim:**
- Aim statement (1-2 sentences, starts with action verb)
- Rationale (why this aim, preliminary data support)
- Working hypothesis (testable prediction)
- Approach summary (brief methods overview)
- Expected outcomes and interpretation

**Writing Strategy**:
- Make aims independent but complementary
- Ensure each aim is achievable within timeline and budget
- Provide enough detail to judge feasibility
- Include contingency plans or alternative approaches
- Use parallel structure across aims
- Clearly state what will be learned from each aim

For detailed guidance, refer to `references/specific_aims_guide.md`.

### 4. Broader Impacts (NSF) / Significance (NIH)

Articulate the societal, educational, or translational value of the research.

**NSF Broader Impacts** (critical component, equal weight with Intellectual Merit):

NSF explicitly evaluates broader impacts. Address at least one of these areas:
1. **Advancing discovery and understanding while promoting teaching, training, and learning**
   - Integration of research and education
   - Training of students and postdocs
   - Curriculum development
   - Educational materials and resources

2. **Broadening participation of underrepresented groups**
   - Recruitment and retention strategies
   - Partnerships with minority-serving institutions
   - Outreach to underrepresented communities
   - Mentoring programs

3. **Enhancing infrastructure for research and education**
   - Shared facilities or instrumentation
   - Cyberinfrastructure and data resources
   - Community-wide tools or databases
   - Open-source software or methods

4. **Broad dissemination to enhance scientific and technological understanding**
   - Public outreach and science communication
   - K-12 educational programs
   - Museum exhibits or media engagement
   - Policy briefs or stakeholder engagement

5. **Benefits to society**
   - Economic impact or commercialization
   - Health, environment, or national security benefits
   - Informed decision-making
   - Workforce development

**Writing Strategy for NSF Broader Impacts**:
- Be specific with concrete activities, not vague statements
- Provide timeline and milestones for broader impacts activities
- Explain how impacts will be measured and assessed
- Connect to institutional resources and existing programs
- Show commitment through preliminary efforts or partnerships
- Integrate with research plan (not tacked on)

**NIH Significance**:
- Addresses important problem or critical barrier to progress
- Improves scientific knowledge, technical capability, or clinical practice
- Potential to lead to better outcomes, interventions, or understanding
- Rigor of prior research in the field
- Alignment with NIH mission and institute priorities

For detailed guidance, refer to `references/broader_impacts.md`.

### 5. Innovation and Transformative Potential

Articulate what is novel, creative, and paradigm-shifting about the research.

**Innovation Elements to Highlight**:
- **Conceptual Innovation**: New frameworks, models, or theories
- **Methodological Innovation**: Novel techniques, approaches, or technologies
- **Integrative Innovation**: Combining disciplines or approaches in new ways
- **Translational Innovation**: New pathways from discovery to application
- **Scale Innovation**: Unprecedented scope or resolution

**Writing Strategy**:
- Clearly state what is innovative (don't assume it's obvious)
- Explain why current approaches are insufficient
- Describe how your innovation overcomes limitations
- Provide evidence that innovation is feasible (preliminary data, proof-of-concept)
- Distinguish incremental from transformative advances
- Balance innovation with feasibility (not too risky)

**Common Mistakes**:
- Claiming novelty without demonstrating knowledge of prior work
- Confusing "new to me" with "new to the field"
- Over-promising without supporting evidence
- Being too incremental (minor variation on existing work)
- Being too speculative (no path to success)

### 6. Research Approach and Methods

Detailed description of how the research will be conducted.

**Essential Components**:
- Overall research design and framework
- Detailed methods for each aim/objective
- Sample sizes, statistical power, and analysis plans
- Timeline and sequence of activities
- Data collection, management, and analysis
- Quality control and validation approaches
- Potential problems and alternative strategies
- Rigor and reproducibility measures

**Writing Strategy**:
- Provide enough detail for reproducibility and feasibility assessment
- Use subheadings and figures to improve organization
- Justify choice of methods and approaches
- Address potential limitations proactively
- Include preliminary data demonstrating feasibility
- Show that you've thought through the research process
- Balance detail with readability (use supplementary materials for extensive details)

**For Experimental Research**:
- Describe experimental design (controls, replicates, blinding)
- Specify materials, reagents, and equipment
- Detail data collection protocols
- Explain statistical analysis plans
- Address rigor and reproducibility

**For Computational Research**:
- Describe algorithms, models, and software
- Specify datasets and validation approaches
- Explain computational resources required
- Address code availability and documentation
- Describe benchmarking and performance metrics

**For Clinical or Translational Research**:
- Describe study population and recruitment
- Detail intervention or treatment protocols
- Explain outcome measures and assessments
- Address regulatory approvals (IRB, IND, IDE)
- Describe clinical trial design and monitoring

For detailed methodology guidance by discipline, refer to `references/research_methods.md`.

### 7. Preliminary Data and Feasibility

Demonstrate that the research is achievable and the team is capable.

**Purpose**:
- Prove that the proposed approach can work
- Show that the team has necessary expertise
- Demonstrate access to required resources
- Reduce perceived risk for reviewers
- Provide foundation for proposed work

**What to Include**:
- Pilot studies or proof-of-concept results
- Method development or optimization
- Access to unique resources (samples, data, collaborators)
- Relevant publications from your team
- Preliminary models or simulations
- Feasibility assessments or power calculations

**NIH Requirements**:
- R01 applications typically require substantial preliminary data
- R21 applications may have less stringent requirements
- New investigators may have less preliminary data
- Preliminary data should directly support proposed aims

**NSF Approach**:
- Preliminary data less commonly required than NIH
- May be important for high-risk or novel approaches
- Can strengthen proposal for competitive programs

**Writing Strategy**:
- Present most compelling data that supports your approach
- Clearly connect preliminary data to proposed aims
- Acknowledge limitations and how proposed work will address them
- Use figures and data visualizations effectively
- Avoid over-interpreting or overstating preliminary findings
- Show trajectory of your research program

### 8. Timeline, Milestones, and Management Plan

Demonstrate that the project is well-planned and achievable within the proposed timeframe.

**Essential Elements**:
- Phased timeline with clear milestones
- Logical sequence and dependencies
- Realistic timeframes for each activity
- Decision points and go/no-go criteria
- Risk mitigation strategies
- Resource allocation across time
- Coordination plan for multi-institutional teams

**Presentation Formats**:
- Gantt charts showing overlapping activities
- Year-by-year breakdown of activities
- Quarterly milestones and deliverables
- Table of aims/tasks with timeline and personnel

**Writing Strategy**:
- Be realistic about what can be accomplished
- Build in time for unexpected delays or setbacks
- Show that timeline aligns with budget and personnel
- Demonstrate understanding of regulatory timelines (IRB, IACUC)
- Include time for dissemination and broader impacts
- Address how progress will be monitored and assessed

**DARPA Emphasis**:
- Particularly important for DARPA proposals
- Clear technical milestones with measurable metrics
- Quarterly deliverables and reporting
- Phase-based structure with exit criteria
- Demonstration and transition planning

For detailed guidance, refer to `references/timeline_planning.md`.

### 9. Team Qualifications and Collaboration

Demonstrate that the team has the expertise, experience, and resources to succeed.

**Essential Elements**:
- PI qualifications and relevant expertise
- Co-I and collaborator roles and contributions
-