# Example Outputs

Sample interactions and generated content for common scenarios.

---

## Project Examples

### Software Feature

**User:** "Create a project for adding dark mode to our app"

**Generated CLI Command:**
```bash
bun ${CLAUDE_PLUGIN_ROOT}/src/cli.ts create --template project \
  --title "Launch Dark Mode" \
  --arg "Project title=Launch Dark Mode" \
  --arg "Target completion date (YYYY-MM-DD)=2025-03-31" \
  --arg "Area=[[Product Development]]" \
  --content '{
    "Why This Matters": "Dark mode reduces eye strain during extended use and improves battery life on OLED devices. User feedback consistently requests this feature, with 47 mentions in the last quarter'\''s support tickets. Competitors (Slack, Discord, Notion) already offer it, making this table-stakes for user retention.",
    "Success Criteria": "- [ ] Theme toggle accessible from Settings > Appearance\n- [ ] User preference persists across sessions and devices\n- [ ] All 50+ UI components render correctly in dark theme\n- [ ] WCAG 2.1 AA contrast ratios maintained (4.5:1 minimum)\n- [ ] No performance regression (Lighthouse score stable)",
    "Objectives": "- [ ] Week 1-2: Design system tokens defined\n- [ ] Week 3-4: Core components converted\n- [ ] Week 5: Edge cases and testing\n- [ ] Week 6: Beta rollout to 10% users",
    "Next Actions": "- [ ] Audit current color usage in codebase (use grep for hardcoded colors)\n- [ ] Schedule design review with Sarah for token definitions\n- [ ] Create feature flag for gradual rollout",
    "Risks & Blockers": "- **Dependency:** Design team capacity for token definitions\n- **Technical:** Third-party components (date picker, charts) may not support theming\n- **Knowledge:** Unsure about handling user-uploaded images in dark mode"
  }'
```

### Personal Goal

**User:** "I want to run a half marathon this year"

**Generated CLI Command:**
```bash
bun ${CLAUDE_PLUGIN_ROOT}/src/cli.ts create --template project \
  --title "Complete Half Marathon" \
  --arg "Project title=Complete Half Marathon" \
  --arg "Target completion date (YYYY-MM-DD)=2025-09-15" \
  --arg "Area=[[Health]]" \
  --content '{
    "Why This Matters": "Completing a half marathon represents a significant fitness milestone and proves commitment to long-term health. The structured training provides accountability for consistent exercise. This goal aligns with my broader objective of maintaining energy for family activities.",
    "Success Criteria": "- [ ] Complete 21.1km without walking breaks\n- [ ] Finish under 2:15:00\n- [ ] No injuries during training\n- [ ] Enjoy race day experience",
    "Objectives": "- [ ] Month 1-2: Build base (run 3x/week, reach 25km/week)\n- [ ] Month 3-4: Build endurance (long runs to 15km)\n- [ ] Month 5: Peak training (18km long run)\n- [ ] Month 6: Taper and race",
    "Next Actions": "- [ ] Research beginner half marathon training plans\n- [ ] Book doctor appointment for pre-training checkup\n- [ ] Order new running shoes (current pair has 800km)",
    "Risks & Blockers": "- **Resource:** Time commitment of 4-5 hours/week\n- **Technical:** History of knee issues - need proper warm-up routine\n- **External:** Melbourne weather unpredictable for outdoor training"
  }'
```

---

## Area Examples

### Professional Area

**User:** "Create an area for Engineering"

**Generated CLI Command:**
```bash
bun ${CLAUDE_PLUGIN_ROOT}/src/cli.ts create --template area \
  --title "Engineering" \
  --arg "Area title=Engineering" \
  --content '{
    "Overview": "Technical skills and software development responsibilities. Encompasses coding proficiency, system design, code quality, and staying current with industry practices. Primary focus for career growth and daily work output.",
    "Standards to Maintain": "- [ ] Code reviews completed within 24 hours\n- [ ] Test coverage above 80% on new code\n- [ ] Documentation updated with major changes\n- [ ] Technical debt addressed each sprint\n- [ ] Learning: 2 hours/week on new technologies",
    "Routines & Habits": "- **Daily**: Morning code review, end-of-day commit\n- **Weekly**: Architecture review, technical writing\n- **Monthly**: Deep dive into new technology, refactor legacy code\n- **Quarterly**: Review tech stack decisions, update skills roadmap"
  }'
```

### Personal Area

**User:** "Create an area for Family"

**Generated CLI Command:**
```bash
bun ${CLAUDE_PLUGIN_ROOT}/src/cli.ts create --template area \
  --title "Family" \
  --arg "Area title=Family" \
  --content '{
    "Overview": "Relationships with Melanie and Levi. Encompasses quality time, communication, household coordination, and supporting each other'\''s goals. Foundation for personal fulfillment and emotional wellbeing.",
    "Standards to Maintain": "- [ ] Weekly 1:1 quality time with Levi\n- [ ] Date night with Melanie monthly minimum\n- [ ] Family dinner together 5x/week\n- [ ] Present and phone-free during family activities\n- [ ] Coordinate schedules Sunday evening",
    "Routines & Habits": "- **Daily**: Breakfast together, bedtime routine with Levi\n- **Weekly**: Family activity Saturday, Sunday planning\n- **Monthly**: Date night, family outing to new place\n- **Quarterly**: Family goals discussion, holiday planning"
  }'
```

---

## Resource Examples

### Book Resource

**User:** "Create a resource for 'Atomic Habits' by James Clear"

**Generated CLI Command:**
```bash
bun ${CLAUDE_PLUGIN_ROOT}/src/cli.ts create --template resource \
  --title "Atomic Habits" \
  --arg "Resource title=Atomic Habits" \
  --arg "Source type (book/article/video/course/podcast/etc.)=book" \
  --arg "Primary area this relates to=[[Learning]]" \
  --arg "Author (optional)=James Clear" \
  --content '{
    "Summary": "Small habits compound into remarkable results through consistent application. The book provides a practical framework (cue, craving, response, reward) for building good habits and breaking bad ones. Key insight: focus on identity change ('\''be a runner'\'') rather than outcomes ('\''run a marathon'\'').",
    "Key Insights": "1. **1% Better Daily**: Compound effects mean small improvements accumulate dramatically over time\n2. **Identity-Based Habits**: '\''I am someone who...'\'' is more powerful than '\''I want to...'\''\n3. **Environment Design**: Make good habits obvious, bad habits invisible\n4. **Habit Stacking**: Attach new habits to existing routines\n5. **Two-Minute Rule**: Scale habits down to two minutes to start",
    "Action Items": "- [ ] Identify one keystone habit to focus on this month\n- [ ] Redesign workspace to make deep work the default\n- [ ] Create habit stack: After morning coffee → 5 min reading\n- [ ] Track habits for 30 days to build awareness",
    "Personal Reflection": "This reframes my approach to goals. Instead of setting outcome targets, I should focus on becoming the type of person who achieves those outcomes. The identity shift from '\''trying to exercise more'\'' to '\''being an active person'\'' feels more sustainable."
  }'
```

---

## Task Examples

### Work Task

**User:** "Create a task to review Sarah's PR for the auth refactor"

**Generated CLI Command:**
```bash
bun ${CLAUDE_PLUGIN_ROOT}/src/cli.ts create --template task \
  --title "Review Auth Refactor PR" \
  --arg "Task title=Review Auth Refactor PR" \
  --arg "Task type (task/reminder/habit/chore)=task" \
  --arg "Priority (low/medium/high/urgent)=high" \
  --arg "Effort (small/medium/large)=medium" \
  --arg "Project (optional)=[[Auth System Upgrade]]" \
  --arg "Due date (YYYY-MM-DD)=2025-12-08" \
  --content '{
    "Description": "Review Sarah'\''s pull request #247 for the authentication system refactor. Focus on security implications, test coverage, and backward compatibility with existing sessions.",
    "Success Criteria": "- [ ] Security review complete (no auth bypasses)\n- [ ] Test coverage adequate (new code >80%)\n- [ ] Feedback provided in PR comments\n- [ ] Approval or change requests submitted"
  }'
```

---

## Capture Examples

### Quick Idea

**User:** "Capture: What if we used AI to generate meeting summaries automatically?"

**Generated CLI Command:**
```bash
bun ${CLAUDE_PLUGIN_ROOT}/src/cli.ts create --template capture \
  --title "AI Meeting Summary Idea" \
  --arg "Title=AI Meeting Summary Idea" \
  --arg "Captured from (thought/article/conversation/etc.)=thought" \
  --arg "Resonance (inspiring/useful/personal/surprising)=useful" \
  --arg "Urgency (high/medium/low)=medium" \
  --arg "Content=What if we used AI to generate meeting summaries automatically? Could integrate with Zoom/Teams recordings, extract action items, and push to project notes." \
  --content '{
    "Why I Saved This": "This could save significant time on meeting overhead. Potential application to [[Productivity Tools]] research. Worth exploring existing solutions before building."
  }'
```

---

## Conversation Flow Example

### Full Project Creation Dialogue

**User:** "Help me create a project note"

**Claude:** "What project would you like to track?"

**User:** "Redesigning our website homepage"

**Claude:** "Got it - a homepage redesign. Let me ask a few questions:

1. **Target completion?** When do you need this done by?
2. **Which area does this belong to?** (e.g., Marketing, Product, Engineering)
3. **What problem does this solve?** Why redesign now?"

**User:** "End of January, it's under Marketing. Our current homepage has a 70% bounce rate."

**Claude:** "Thanks. I'll create the project with:
- **Title:** Homepage Redesign
- **Target:** 2025-01-31
- **Area:** [[Marketing]]
- **Why:** Reduce 70% bounce rate

I'll generate success criteria and next actions based on typical web redesign projects. Creating now..."

**[Creates note with generated content]**

---

## Error Recovery Examples

### Missing Template

**Error:** "Template not found: projectt"

**Recovery:** "I couldn't find template 'projectt'. Did you mean 'project'? Run `para-obsidian templates` to list available templates: project, area, resource, task, capture, daily, weekly-review, booking, checklist, itinerary-day, trip-research."

### Missing Required Arg

**Error:** "Missing required argument: Area"

**Recovery:** "The project template requires an Area. Run `para-obsidian template-fields project` to see all required fields. Which area does this project belong to? Your current areas include: [[Work]], [[Health]], [[Family]], [[Learning]]."

### Section Not Found

**Warning:** "sectionsSkipped: [{ heading: 'Custom Section', reason: 'Heading not found' }]"

**Recovery:** "Note created successfully. I couldn't inject content into 'Custom Section' because that heading doesn't exist in the template. The content was saved in the Notes section instead."
