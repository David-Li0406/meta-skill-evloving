---
name: design
description: UX and CX design workflows for wireframing, prototyping, and customer journey mapping. Use when creating wireframes, designing user interfaces, prototyping interactions, mapping customer journeys, or conducting UX/CX design work. Used in PDLC Feature-Refinement workflow for Story_And_Design_Start and Prototyping nodes by UX-Designer and CX-Designer agents.
---

# Design Skill

You are conducting UX and CX design work to create user-centered interfaces and experiences. This skill provides workflows for wireframing, prototyping, and journey mapping.

## Available Workflows

### 1. Wireframing (`workflows/wireframing.md`)
Create low-fidelity wireframes to establish layout and information architecture.
- **Use for**: Early design exploration, layout planning, component structure
- **Output**: F07-wireframes.md artifact (or HTML wireframe)
- **Agent**: UXDesigner

### 2. Prototyping (`workflows/prototyping.md`)
Build interactive prototypes to validate user flows and interactions.
- **Use for**: User testing, stakeholder demos, interaction validation
- **Output**: F08-prototype.md or interactive HTML prototype
- **Agent**: UXDesigner

### 3. Journey Mapping (`workflows/journey-mapping.md`)
Map customer journey to understand touchpoints, emotions, and pain points.
- **Use for**: Understanding end-to-end experience, identifying improvement opportunities
- **Output**: F09-customer-journey.md artifact
- **Agent**: CXDesigner

## Workflow Selection

**Feature Refinement Phase (Story_And_Design_Start node)**:
1. Start with `wireframing` for initial layout and structure
2. Progress to `prototyping` for interaction design
3. Use `journey-mapping` for multi-step or cross-channel experiences

**Story Elaboration Phase**:
- Wireframes and prototypes inform user story creation
- Journey maps identify story boundaries and flows

**Design Review Phase (Story_Design_Review node)**:
- Validate alignment between stories and design artifacts
- Ensure consistent user experience across features

## Context Resources

- **design-patterns.md** - Common UX patterns, component libraries, interaction standards
- **journey-map-templates.md** - Customer journey map structures and examples

## Tools Required

- **Write** - Create design documentation and wireframe descriptions
- **Read** - Review requirements, stories, and existing design system
- **frontend-design skill** - For creating interactive HTML prototypes (optional)

## Integration Points

**Depends on**:
- `specification-writing` - Feature PRD and user stories
- `discovery` - Stakeholder insights and user research
- `frontend-design` - Interactive prototype creation (optional)

**Feeds into**:
- `architecture/workflows/design-frontend.md` - Frontend architecture design
- `implementation` - Development using design specs
- `quality` - Design review and validation

**Used by agents**:
- UXDesigner (wireframing, prototyping)
- CXDesigner (journey mapping)
- ProductManager (design review and alignment)

## Output Standards

All design artifacts must:
1. Be based on user research and stakeholder insights
2. Follow accessibility best practices (WCAG guidelines)
3. Align with existing design system (if applicable)
4. Include rationale for design decisions
5. Be testable with users or stakeholders
6. Be stored in `/docs/workflow/artifacts/`
