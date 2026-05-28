# Example Conversation Flow

This document shows a complete PRD creation conversation from start to finish.

## Example: Adding Dark Mode to a TUI Application

### Phase 1: Task Type Identification

**User:** Create a PRD for adding dark mode to the TUI

**Assistant:** I'll help you create a PRD for dark mode. First, let me understand what type of work this is:

What category best describes this work?

| Option | Description |
|--------|-------------|
| A | Feature Development - New features, enhancements, integrations |
| B | Bug Fixing - Investigating and fixing bugs |
| C | Research & Planning - Exploration, architecture decisions |
| D | Maintenance - Refactoring, cleanup, optimization |
| E | DevOps - Deployment, infrastructure, CI/CD |

**User:** A

**Assistant:** Great! This is feature development work. Let me gather some information about what you have in mind.

---

### Phase 2: Brain Dump

**Assistant:** Tell me everything about this dark mode feature. What's the goal? What should it cover? Any constraints or preferences?

**User:** We want to add dark mode support to our terminal UI. The app currently only has a light theme which is hard on the eyes during long sessions. We want a dark theme that's easy on the eyes - soft grays, not pure black. It should apply to all components and remember the user's preference.

---

### Phase 3: Clarifying Questions (Round 1)

**Assistant:** Thanks for that context. A few clarifying questions:

1. What is the primary goal of this feature?
   A. Reduce eye strain for long sessions
   B. Match system theme preference
   C. Provide visual customization options
   D. Other: [please specify]

2. Should the setting persist across sessions?
   A. Yes, save to config file
   B. No, session only
   C. Follow system preference automatically

**User:** 1A, 2A

---

### Phase 3: Clarifying Questions (Round 2)

**Assistant:** Got it - eye strain reduction with persistent config. A couple more questions:

3. Which components need dark mode support?
   A. All TUI components
   B. Only the main execution view
   C. Main view + settings panel
   D. Other: [please specify]

4. How should users switch between themes?
   A. Toggle in settings menu
   B. Command-line flag
   C. Keyboard shortcut
   D. Both A and C

**User:** 3A, 4D

---

### Phase 3: Clarifying Questions (Round 3)

**Assistant:** Excellent. Now I need to understand the quality requirements:

5. What quality commands must pass for each user story?
   A. pnpm typecheck && pnpm lint
   B. npm run typecheck && npm run lint
   C. bun run typecheck && bun run lint
   D. Other: [specify your commands]

6. For UI stories, should we include browser verification?
   A. Yes, use agent-browser skill to verify visually
   B. No, automated tests are sufficient
   C. N/A - this is a TUI, not a web app

**User:** 5A, 6C

---

### Phase 4: Confirm Understanding

**Assistant:** Perfect, I have what I need. Let me confirm my understanding:

**Problem/Goal:**
- Current light theme causes eye strain during long sessions
- Need a dark theme with soft grays (not pure black)
- Theme should apply to all TUI components

**Proposed Solution:**
- Add theme configuration to config file (persists across sessions)
- Create soft-contrast dark palette
- Apply theme to all TUI components
- Provide both settings menu toggle and keyboard shortcut for switching

**Scope In:**
- Theme config with light/dark options
- Dark color palette (soft grays)
- Theme application to all components
- Settings toggle + keyboard shortcut
- Persistent storage

**Scope Out:**
- System theme auto-detection
- Custom color schemes beyond light/dark
- Per-component theme overrides

**Proposed Phases:**
1. Phase 1: Foundation - Config schema, palette definition
2. Phase 2: Implementation - Apply theme to components
3. Phase 3: UX - Toggle and keyboard shortcut
4. Phase 4: Verification - Full testing and validation

**Quality Gates:**
- `pnpm typecheck` - Type checking
- `pnpm lint` - Linting
- (No browser verification needed for TUI)

**Testing Strategy:**
- Visual verification of all components in dark mode
- Contrast ratio verification (WCAG AA)
- Theme persistence across restarts
- Toggle functionality testing

Does this match your expectations? Any changes needed?

**User:** Yes, that looks correct! Go ahead and generate the PRD.

---

### Phase 5: Generate PRD

**Assistant:** Great! Generating the PRD now.

---

[PRD]
# PRD: Dark Mode for Terminal UI

## Overview
Add dark mode support to the terminal UI to reduce eye strain during long sessions. The feature will apply to all TUI components and persist the user's preference in the config file.

## Goals
- Provide a comfortable viewing experience in low-light environments
- Persist theme preference across sessions
- Apply consistent styling to all TUI components
- Support quick theme switching via keyboard shortcut

## Quality Gates

These commands must pass for every user story:
- `pnpm typecheck` - Type checking
- `pnpm lint` - Linting

## Non-Goals
- System theme auto-detection (future enhancement)
- Custom color schemes beyond light/dark
- Per-component theme overrides

## Technical Approach
1. Extend existing config schema to include theme preference
2. Define dark palette using soft gray tones
3. Create theme application system for all TUI components
4. Add keyboard shortcut and settings toggle

## Phases

### Phase 1: Foundation
**Objective:** Establish config and color palette
**Stories:** US-001 through US-002
**Exit criteria:** Config schema updated, palette defined

### Phase 2: Implementation
**Objective:** Apply theme to all components
**Stories:** US-003 through US-004
**Exit criteria:** All components render correctly in dark mode

### Phase 3: User Experience
**Objective:** Add controls for theme switching
**Stories:** US-005 through US-006
**Exit criteria:** Toggle and shortcut work correctly

### Phase 4: Verification
**Objective:** Comprehensive testing and validation
**Stories:** US-007
**Exit criteria:** All tests pass, no visual issues

## User Stories

### US-001: Add theme configuration
**Description:** As a user, I want to set my preferred theme (light/dark) so that it persists across sessions.

**Tasks:**
- Read existing config schema in `src/config/schema.ts`
- Add `theme` field with values: "light" (default), "dark"
- Ensure backward compatibility (default to light if not specified)

**Acceptance Criteria:**
- [ ] Theme field added to config schema
- [ ] Default value is "light" for backward compatibility
- [ ] Config validates theme values

**Notes:** Follow existing config pattern. Don't break existing configs.

### US-002: Create dark theme color palette
**Description:** As a user, I want a soft-contrast dark theme that's easy on the eyes.

**Tasks:**
- Research existing color patterns in `src/theme/colors.ts`
- Define dark palette with gray tones (not pure black)
- Ensure WCAG AA contrast ratios for all colors

**Acceptance Criteria:**
- [ ] Dark palette defined with soft grays
- [ ] All color combinations meet WCAG AA contrast
- [ ] Palette includes colors for all UI states (selected, hover, disabled)

**Notes:** Use hex codes in the #2a-#4a range for backgrounds, #e0-#f0 for text.

### US-003: Apply theme to TUI components
**Description:** As a user, I want all TUI components to respect my theme preference.

**Tasks:**
- Read existing theme application code
- Update header component to use theme colors
- Update task list component to use theme colors
- Update detail panels to use theme colors
- Update dialogs to use theme colors

**Acceptance Criteria:**
- [ ] All components render correctly in dark mode
- [ ] No hard-coded colors remain
- [ ] Theme switches work correctly

**Notes:** Test each component individually after updating.

### US-004: Add theme toggle in settings
**Description:** As a user, I want to toggle themes from within the settings menu.

**Tasks:**
- Locate settings menu implementation
- Add theme option to settings view
- Implement immediate theme change (no restart required)
- Persist change to config file

**Acceptance Criteria:**
- [ ] Theme option visible in settings
- [ ] Changes apply immediately
- [ ] Changes persist to config file

**Notes:** Follow existing settings menu pattern.

### US-005: Add keyboard shortcut for theme toggle
**Description:** As a user, I want a quick keyboard shortcut to switch themes.

**Tasks:**
- Read keyboard shortcut configuration
- Add theme toggle shortcut (suggest Ctrl/Cmd+D)
- Wire shortcut to theme toggle function
- Document shortcut in help text

**Acceptance Criteria:**
- [ ] Shortcut toggles between light and dark
- [ ] Shortcut documented in help
- [ ] Shortcut doesn't conflict with existing shortcuts

**Notes:** Check existing shortcuts first to avoid conflicts.

### US-006: Verify theme persistence
**Description:** As a user, I want my theme preference to be remembered across sessions.

**Tasks:**
- Start app, set theme to dark, restart
- Start app, set theme to light, restart
- Verify config file is updated correctly
- Verify theme loads correctly on startup

**Acceptance Criteria:**
- [ ] Dark theme persists across restarts
- [ ] Light theme persists across restarts
- [ ] Config file contains correct theme value

**Notes:** Test multiple restart cycles.

### US-007: Final validation and completion
**Description:** Comprehensive verification that all work is complete and working.

**Tasks:**
- Run `pnpm typecheck` - must pass
- Run `pnpm lint` - must pass
- Manually test all components in both themes
- Verify all acceptance criteria from US-001 through US-006
- Check for any visual issues or color problems

**Acceptance Criteria:**
- [ ] All quality gates pass
- [ ] All stories complete
- [ ] No visual or functional issues in either theme
- [ ] Documentation updated if needed

## Testing Strategy

| Level | Stories | Verification |
|-------|---------|--------------|
| Light | US-001, US-002 | Typecheck + lint |
| Standard | US-003, US-004, US-005, US-006 | Typecheck + lint + manual testing |
| Full | US-007 | Complete test suite + full manual review |

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Contrast issues fail accessibility | Medium | Test with contrast checker, use WCAG guidelines |
| Breaking existing configs | Medium | Default to light theme, validate schema carefully |
| Visual inconsistencies | Low | Test each component individually |
| Performance impact | Low | Minimal - theme loading is one-time |

## Success Criteria
- All components render correctly in dark mode
- No accessibility contrast issues
- Theme persists across sessions
- Toggle and shortcut work correctly
- All quality gates pass
[/PRD]

---

## After Generation

**Files created:**
- `docs/prds/tui-dark-mode/PRD.md`
- `docs/prds/tui-dark-mode/prd.json`

**Summary:** 7 user stories across 4 phases

**Execution Guidance:**
1. Create a tmux session for long-running execution: `tmux new -s dark-mode`
2. Create feature branch: `git checkout -b feature/dark-mode`
3. Start execution with: `ralph loop docs/prds/tui-dark-mode/prd.json`
4. Detach with Ctrl+B, D - reattach with `tmux attach -t dark-mode`

**Monitoring Notes:**
- Check back every 10-15 minutes for progress updates
- BLOCKED tasks may need your input
- Progress is tracked in prd.json (passes: true/false)
- The tmux session shows live progress

**Important Reminders:**
- Keep your machine running during execution
- Check back periodically for BLOCKED tasks
- Each story should complete in one AI agent session
- When all stories show `"passes": true`, the PRD is complete
