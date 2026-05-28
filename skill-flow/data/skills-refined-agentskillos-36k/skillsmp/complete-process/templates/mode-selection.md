# Mode Selection Template

Template for presenting workflow mode options to users.

## Standard Mode Selection

Use this template when presenting the mode selection to users:

```
Choose transformation workflow:

○ Quick Transform Only
  Transform to pseudo-code only (5-15s, best for simple queries)

● Complete Process (Recommended)
  Transform → Validate → Optimize (30-90s, production-ready output)
```

## AskUserQuestion Implementation

```json
{
  "questions": [
    {
      "question": "Choose transformation workflow:",
      "header": "Workflow Mode",
      "multiSelect": false,
      "options": [
        {
          "label": "Quick Transform Only",
          "description": "Transform to pseudo-code only (5-15s, best for simple queries)"
        },
        {
          "label": "Complete Process (Recommended)",
          "description": "Transform → Validate → Optimize (30-90s, production-ready output)"
        }
      ]
    }
  ]
}
```

## Mode Selection with Preference Hint

When user has a saved preference:

```
Choose transformation workflow:
(Last time you used: Complete Process)

○ Quick Transform Only
  Transform to pseudo-code only (5-15s, best for simple queries)

● Complete Process (Recommended)
  Transform → Validate → Optimize (30-90s, production-ready output)
```

## Mode Descriptions

### Quick Transform Only

**Best for:**
- Simple, well-defined queries
- Rapid prototyping and iteration
- Non-critical features
- Learning and experimentation

**Output:**
- Raw pseudo-code
- No validation report
- No optimization enhancements

**Estimated Duration:** 5-15 seconds

**Example Use Cases:**
- "Add a logout button"
- "Create a helper function for date formatting"
- "Update button color to blue"

---

### Complete Process (Recommended)

**Best for:**
- Production feature implementation
- Complex requirements with multiple parameters
- Features requiring validation
- Security-sensitive implementations
- Team environments with quality standards

**Output:**
- Optimized pseudo-code
- Comprehensive validation report
- Optimization summary with improvements
- Implementation-ready code

**Estimated Duration:** 30-90 seconds

**Example Use Cases:**
- "Implement user authentication with OAuth"
- "Create a payment processing endpoint"
- "Add file upload with validation"
- "Build a real-time notification system"

---

## Decision Helper

### Choose Quick Mode If:
- [ ] Query is simple (< 50 words)
- [ ] Requirements are crystal clear
- [ ] Single action or component
- [ ] Prototyping or exploring
- [ ] Don't need validation
- [ ] Speed is priority

### Choose Complete Mode If:
- [ ] Query is complex (multiple requirements)
- [ ] Production feature
- [ ] Security-sensitive
- [ ] Need validation and error handling
- [ ] Team environment
- [ ] Quality over speed

## CLI Prompts

### Initial Prompt (No Preference)
```
┌────────────────────────────────────────────┐
│     Complete Process Orchestrator          │
├────────────────────────────────────────────┤
│                                            │
│  Choose transformation workflow:           │
│                                            │
│  1. Quick Transform Only                   │
│     • Duration: 5-15 seconds               │
│     • Output: Raw pseudo-code              │
│     • Best for: Simple queries             │
│                                            │
│  2. Complete Process (Recommended)         │
│     • Duration: 30-90 seconds              │
│     • Output: Validated + Optimized        │
│     • Best for: Production features        │
│                                            │
│  Enter choice (1 or 2): _                  │
│                                            │
│  ☐ Remember my choice for next time        │
│                                            │
└────────────────────────────────────────────┘
```

### Prompt with Saved Preference
```
┌────────────────────────────────────────────┐
│     Complete Process Orchestrator          │
├────────────────────────────────────────────┤
│                                            │
│  Your preference: Complete Process         │
│                                            │
│  Proceed with Complete Process?            │
│                                            │
│  [Y] Yes, use Complete Process             │
│  [Q] Switch to Quick Transform             │
│  [C] Change preference                     │
│                                            │
│  Choice: _                                 │
│                                            │
└────────────────────────────────────────────┘
```

### Quick Confirmation (Experienced Users)
```
Mode: [Complete Process ▼]
Proceed? (Y/n): _
```

## Progress Indicators

### Quick Mode Progress
```
🔄 Transforming query to pseudo-code... (8s)
```

### Complete Mode Progress
```
Step 1/3: 🔄 Transforming query to pseudo-code... ✓ (12s)
✓ Step 1/3 complete | Tokens: 1,234

Step 2/3: ✓ Validating requirements... ✓ (8s)
✓ Step 2/3 complete | Tokens: 2,567

Step 3/3: ⚡ Optimizing for implementation... ✓ (18s)
✓ Step 3/3 complete | Tokens: 3,891

✓ Pipeline complete! Review output below.

Total duration: 38 seconds | Total tokens: 3,891
```

## Preference Storage Format

```json
{
  "complete-process-orchestrator": {
    "preferred_mode": "complete",
    "show_progress": true,
    "remember_preference": true,
    "last_updated": "2026-01-18T12:00:00Z",
    "selection_count": {
      "quick": 8,
      "complete": 24
    }
  }
}
```

## Error Messages

### Invalid Selection
```
❌ Invalid choice. Please enter 1 for Quick or 2 for Complete.
```

### Timeout (No Response)
```
⏱️ No response after 5 minutes. Defaulting to Quick Transform.
Press Ctrl+C to cancel.
```

### Preference Load Error
```
⚠️ Could not load saved preference. Showing all options.
```

## Customization Options

### For Power Users
Allow direct mode selection via command flag:
```bash
/complete-process --mode=quick
/complete-process --mode=complete
/complete-process --mode=auto  # Use saved preference
```

### For Teams
Allow team-wide defaults in configuration:
```json
{
  "team_defaults": {
    "default_mode": "complete",
    "require_complete_for_production": true,
    "allow_preference_override": true
  }
}
```

### For Automation
Support non-interactive mode:
```bash
# Environment variable
ORCHESTRATOR_MODE=complete /complete-process "$query"

# Config file
mode: complete
interactive: false
```

## Accessibility

### Screen Reader Support
```
Workflow mode selection. 2 options available.
Option 1 of 2: Quick Transform Only.
  Description: Transform to pseudo-code only, 5 to 15 seconds, best for simple queries.
Option 2 of 2: Complete Process, Recommended.
  Description: Transform, Validate, and Optimize, 30 to 90 seconds, production-ready output.
Current selection: Option 2, Complete Process.
Press Enter to confirm or use arrow keys to change selection.
```

### Keyboard Navigation
- **Arrow Up/Down**: Navigate options
- **Enter**: Confirm selection
- **Tab**: Move to preference checkbox
- **Spacebar**: Toggle preference checkbox
- **Esc**: Cancel operation

## Internationalization

### Translations Needed
- Mode names: "Quick Transform Only", "Complete Process"
- Duration labels: "seconds", "minutes"
- Status indicators: "Transforming", "Validating", "Optimizing"
- Success/failure messages
- Help text

### Example (Spanish)
```
Elige el flujo de trabajo de transformación:

○ Solo Transformación Rápida
  Transformar solo a pseudo-código (5-15s, mejor para consultas simples)

● Proceso Completo (Recomendado)
  Transformar → Validar → Optimizar (30-90s, listo para producción)
```

## Best Practices

### Do's
✓ Always provide estimated durations
✓ Clearly mark recommended option
✓ Show preference hint when available
✓ Provide meaningful descriptions
✓ Allow easy preference management
✓ Support keyboard navigation

### Don'ts
✗ Don't hide mode differences
✗ Don't make selection too complex
✗ Don't force preference saving
✗ Don't obscure duration expectations
✗ Don't skip confirmation for long operations

## Testing Checklist

- [ ] First-time user sees both options equally
- [ ] Returning user sees preference hint
- [ ] Keyboard navigation works
- [ ] Screen reader announces properly
- [ ] Preference saves correctly
- [ ] Preference loads correctly
- [ ] Timeout defaults to safe option
- [ ] Error messages are clear
- [ ] Progress indicators display
- [ ] Duration estimates are accurate
