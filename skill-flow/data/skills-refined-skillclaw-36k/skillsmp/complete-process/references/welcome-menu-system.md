# Welcome Message and Menu System

When users invoke the plugin using trigger phrases like "use pseudo-code prompting plugin" or "run pseudo-code prompting plugin", you MUST display a welcome message with an interactive menu.

## Welcome Message Structure

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Welcome to Pseudo-Code Prompting Plugin! 🎯
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Transform natural language into structured, validated pseudo-code.

📖 **Help & Documentation**
   Type 'help' or ask 'how does this work?'

⚡ **Available Commands**
   • transform-query - Transform natural language to pseudo-code
   • validate-requirements - Validate pseudo-code completeness
   • optimize-prompt - Enhance pseudo-code with missing parameters
   • compress-context - Compress verbose requirements
   • complete-process - Full workflow (transform + validate + optimize)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Quick: help | transform | validate | optimize | complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Menu Display Triggers

Display the welcome menu when the user's message contains ANY of these patterns:

- "use pseudo-code prompting plugin"
- "use pseudocode prompting plugin"
- "run pseudo-code prompting plugin"
- "invoke complete-process"
- "show plugin menu"

## State Management for Menu Persistence

**CRITICAL**: After displaying the welcome menu, you MUST maintain awareness of the menu context throughout the conversation using the following strategy:

### Instruction-Based State Management

Since Claude Code doesn't have technical state management between turns, menu persistence is achieved through **behavioral instructions**:

1. **After Displaying Menu**: In EVERY subsequent response until user makes a selection, you MUST:
   - Check if user's message references any menu keywords
   - If YES: Route to appropriate skill
   - If NO: Provide helpful response AND append menu reminder footer

2. **Menu Reminder Footer**: Append this to all responses while menu is active:
   ```
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   💡 Quick access: help | transform | validate | optimize | complete
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ```

3. **Context Window Memory**: Use the last 2-3 messages to detect if menu was shown

### Menu State Tracking

Track these conceptual states (via conversation context, not technical state):

- `menu_displayed`: Was welcome menu shown in recent turns?
- `selection_made`: Has user selected a specific command/skill?

## User Selection Routing

When user's message contains menu keywords, route as follows:

| Keyword Detected | Action | Skill to Invoke |
|------------------|--------|-----------------|
| "help", "how does this work", "documentation" | Show comprehensive help | Display plugin documentation |
| "commands", "list commands", "what can you do" | List all available skills | Show all command descriptions |
| "transform", "transform-query" | Transform natural language to pseudo-code | `pseudo-code-prompting:prompt-structurer` |
| "validate", "validate-requirements" | Validate pseudo-code | `pseudo-code-prompting:requirement-validator` |
| "optimize", "optimize-prompt" | Optimize pseudo-code | `pseudo-code-prompting:prompt-optimizer` |
| "compress", "compress-context" | Compress verbose text | `pseudo-code-prompting:context-compressor` |
| "complete", "complete-process", "full workflow" | Run full pipeline | Execute complete mode workflow |

### Keyword Detection Logic

```
on_user_message:
  if menu_was_displayed_recently:
    detected_keywords = parse_for_menu_keywords(user_message)

    if detected_keywords.length > 0:
      route_to_skill(detected_keywords[0])
    else:
      respond_to_user_question()
      append_menu_reminder_footer()
```

## Command Execution

When a user selects a command from the menu, you MUST:

1. **Invoke the appropriate skill** using the Skill tool

2. **Provide feedback** to the user about which skill is being executed

3. **Wait for skill completion** before returning to menu if needed

## Menu Exit Conditions

Stop displaying menu reminders when ANY of these occur:

1. User explicitly selects a command/skill
2. User says "exit", "cancel", or "close menu"
3. User asks 3+ unrelated questions in a row (menu no longer relevant)
4. Skill execution completes successfully
5. User explicitly requests to stop seeing reminders

## Error Handling for Menu System

| Error Scenario | Handling Strategy |
|----------------|-------------------|
| Skill invocation fails | Show error, redisplay menu with "try again?" |
| Invalid menu selection | "I didn't recognize that command. Available options: ..." |
| User confusion | Rephrase menu with simpler language |
| Timeout (menu shown but no selection for 5+ turns) | Ask: "Still interested in using the plugin? (yes/no)" |

## Menu Examples

### Example 1: User Invokes Plugin

**User**: "use pseudo-code prompting plugin"

**Assistant**: *Displays welcome menu*

**User**: "help"

**Assistant**: *Shows comprehensive plugin documentation*

### Example 2: Complete Process Flow

**User**: "use pseudo-code prompting plugin"

**Assistant**: *Displays welcome menu*

**User**: "complete"

**Assistant**: *Invokes complete-process workflow*

### Example 3: Menu Persistence

**User**: "use pseudo-code prompting plugin"

**Assistant**: *Displays welcome menu*

**User**: "how does the validate command work?"

**Assistant**: *Explains validation feature AND appends menu reminder footer*

**User**: "transform"

**Assistant**: *Invokes `pseudo-code-prompting:prompt-structurer`*
