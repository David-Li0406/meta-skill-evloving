# Multi-Step Command Palette - Flow Diagram

## Visual Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                       Multi-Step Command Palette                     │
│                        (Raycast-style Pattern)                       │
└─────────────────────────────────────────────────────────────────────┘

LEVEL 0: Root Level
┌─────────────────────────────────────────────────────────────────────┐
│  🔍 Search or select a command...                                   │
├─────────────────────────────────────────────────────────────────────┤
│  📁 web-app                                                          │
│     Main web application (React + TypeScript)                       │
│                                                                       │
│  🚀 api-server                                                       │
│     Backend API service (Node.js + Express)                         │
│                                                                       │
│  📱 mobile-app                                                       │
│     iOS and Android app (React Native)                              │
│                                                                       │
│  📦 design-system                                                    │
│     Shared component library                                         │
│                                                                       │
│  📄 documentation                                                    │
│     Product and API docs                                             │
├─────────────────────────────────────────────────────────────────────┤
│  ↑↓ navigate   Enter select                      Level 1 of 3      │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ User selects "web-app"
                                    │ push(web-app)
                                    ↓

LEVEL 1: Repository Actions
┌─────────────────────────────────────────────────────────────────────┐
│  Home > web-app                                                  ✕  │
├─────────────────────────────────────────────────────────────────────┤
│  🔍 Search or select a command...                                   │
├─────────────────────────────────────────────────────────────────────┤
│  🚀 Deploy                                                           │
│     Deploy to production                                             │
│                                                                       │
│  🌿 Switch Branch                                                   │
│     Change active branch                                             │
│                                                                       │
│  🔀 Create Pull Request                                             │
│     Open new PR                                                      │
│                                                                       │
│  ⚙️  Repository Settings                                            │
│     Manage repo configuration                                        │
│                                                                       │
│  👥 Manage Collaborators                                            │
│     Add or remove team members                                       │
│                                                                       │
│  📝 Edit README                                                      │
│     Update repository documentation                                  │
├─────────────────────────────────────────────────────────────────────┤
│  ↑↓ navigate   Enter select   Backspace back     Level 2 of 3      │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ User selects "Deploy"
                                    │ push(deploy-action)
                                    ↓

LEVEL 2: Confirmation
┌─────────────────────────────────────────────────────────────────────┐
│  Home > web-app > Deploy                                         ✕  │
├─────────────────────────────────────────────────────────────────────┤
│  🔍 Search or select a command...                                   │
├─────────────────────────────────────────────────────────────────────┤
│  ✅ Confirm                                                          │
│     Execute Deploy to production                                     │
│                                                                       │
│  ❌ Cancel                                                           │
│     Go back                                                          │
├─────────────────────────────────────────────────────────────────────┤
│  ↑↓ navigate   Enter select   Backspace back     Level 3 of 3      │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ User selects "Confirm"
                                    │ executeCommand(deploy)
                                    │ reset() + close
                                    ↓
                              ┌───────────┐
                              │  Deploy!  │
                              └───────────┘
```

## Alternative Flow: Branch Selection

```
LEVEL 1: Repository Actions (web-app selected)
        │
        │ User selects "Switch Branch"
        │ push(switch-branch-action)
        ↓

LEVEL 2: Branch Selection
┌─────────────────────────────────────────────────────────────────────┐
│  Home > web-app > Switch Branch                                  ✕  │
├─────────────────────────────────────────────────────────────────────┤
│  🔍 Search or select a command...                                   │
├─────────────────────────────────────────────────────────────────────┤
│  🌿 main                                                            │
│     Main production branch                                           │
│                                                                       │
│  🌿 develop                                                         │
│     Development branch                                               │
│                                                                       │
│  🌿 feature/auth                                                    │
│     Authentication feature                                           │
│                                                                       │
│  🌿 hotfix/security                                                 │
│     Security hotfix                                                  │
├─────────────────────────────────────────────────────────────────────┤
│  ↑↓ navigate   Enter select   Backspace back     Level 3 of 3      │
└─────────────────────────────────────────────────────────────────────┘
```

## Navigation Patterns

### Forward Navigation (Push)

```
User Action: Select command with nextLevel
     ↓
Stack: [cmd1] → [cmd1, cmd2]
     ↓
Level: 1 → 2
     ↓
Breadcrumb: ["cmd1"] → ["cmd1", "cmd2"]
     ↓
Current Commands: cmd1.nextLevel → cmd2.nextLevel
```

### Back Navigation (Pop)

```
User Action: Press Backspace or ESC (empty search)
     ↓
Stack: [cmd1, cmd2] → [cmd1]
     ↓
Level: 2 → 1
     ↓
Breadcrumb: ["cmd1", "cmd2"] → ["cmd1"]
     ↓
Current Commands: cmd2.nextLevel → cmd1.nextLevel
```

### Jump Navigation (NavigateTo)

```
User Action: Click breadcrumb item at level N
     ↓
Stack: [cmd1, cmd2, cmd3] → [cmd1, cmd2]
     ↓
Level: 3 → 2
     ↓
Breadcrumb updates automatically
```

### Reset Navigation

```
User Action: Click ✕ button
     ↓
Stack: [cmd1, cmd2] → []
     ↓
Level: 2 → 0
     ↓
Breadcrumb: ["cmd1", "cmd2"] → []
     ↓
Current Commands: → rootCommands
```

## State Machine

```
┌──────────┐
│   Root   │ Level 0
│  (Empty  │
│  Stack)  │
└────┬─────┘
     │
     │ push(cmd1)
     ↓
┌──────────┐
│  Level 1 │ [cmd1]
│  Stack:  │
│  [cmd1]  │
└────┬─────┘
     │
     │ push(cmd2)
     ↓
┌──────────┐
│  Level 2 │ [cmd1, cmd2]
│  Stack:  │
│ [cmd1,   │
│  cmd2]   │
└────┬─────┘
     │
     │ push(cmd3)
     ↓
┌──────────┐
│  Level 3 │ [cmd1, cmd2, cmd3]
│  Stack:  │
│ [cmd1,   │
│  cmd2,   │
│  cmd3]   │
└──────────┘
     │
     │ pop()
     ↓
   Back to Level 2
     │
     │ reset()
     ↓
   Back to Root
```

## Component Interaction

```
┌─────────────────────────────────────────────────────────────────┐
│                      MultiStepPalette                           │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  useCommandFlow Hook                                       │ │
│  │  ┌──────────────────────────────────────────────────────┐ │ │
│  │  │  State:                                               │ │ │
│  │  │  - stack: Command[]                                   │ │ │
│  │  │  - currentLevel: number                               │ │ │
│  │  │  - breadcrumb: BreadcrumbItem[]                       │ │ │
│  │  │  - currentCommands: Command[]                         │ │ │
│  │  └──────────────────────────────────────────────────────┘ │ │
│  │                                                             │ │
│  │  Actions:                                                   │ │
│  │  - push(command)    → Add to stack                         │ │
│  │  - pop()            → Remove from stack                    │ │
│  │  - reset()          → Clear stack                          │ │
│  │  - navigateTo(n)    → Jump to level                        │ │
│  │  - executeCommand() → Run action                           │ │
│  └───────────────────────────────────────────────────────────┘ │
│                               ↓                                  │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  CommandStep Component                                     │ │
│  │  ┌──────────────────────────────────────────────────────┐ │ │
│  │  │  Props:                                               │ │ │
│  │  │  - commands: currentCommands                          │ │ │
│  │  │  - selectedId: state                                  │ │ │
│  │  │  - onSelect: handleSelect                             │ │ │
│  │  └──────────────────────────────────────────────────────┘ │ │
│  │                                                             │ │
│  │  Renders:                                                   │ │
│  │  - List of commands                                         │ │
│  │  - Selection state                                          │ │
│  │  - Loading state                                            │ │
│  │  - Empty state                                              │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Keyboard Event Flow

```
User presses key
     ↓
┌────────────────┐
│  Key Handler   │
└────┬───────────┘
     │
     ├─ ↑/↓        → Update selectedId
     │
     ├─ Enter      → handleSelect(selected)
     │                   ↓
     │              Has nextLevel?
     │                   ↓
     │              ┌─Yes─┬─No──┐
     │              │     │     │
     │            push() execute()
     │              │     │     │
     │         Next level  Close
     │
     ├─ Backspace  → Check searchQuery
     │                   ↓
     │              Is empty?
     │                   ↓
     │              ┌─Yes─┬─No──┐
     │              │     │     │
     │            pop()   Ignore
     │
     └─ Escape     → Check searchQuery
                        ↓
                   Is empty?
                        ↓
                   ┌─Yes─┬─No──────┐
                   │     │         │
                 pop()  Clear   Stay
                        query
```

## Data Flow: Command Execution

```
User selects command
     ↓
┌─────────────────────────────────────────┐
│  MultiStepPalette.handleSelect()        │
└─────────────────────────────────────────┘
     │
     ├─ Command has nextLevel?
     │
     ├─ YES: Navigation command
     │   │
     │   ├─ push(command)
     │   │     ↓
     │   │ Stack updates
     │   │     ↓
     │   │ Breadcrumb updates
     │   │     ↓
     │   │ currentCommands = command.nextLevel
     │   │     ↓
     │   └─ Re-render with new level
     │
     └─ NO: Terminal command
         │
         ├─ executeCommand(command)
         │     ↓
         │ Command.action()
         │     ↓
         │ onCommandExecute callback
         │     ↓
         ├─ reset()
         │     ↓
         │ Clear stack
         │     ↓
         └─ onOpenChange(false)
               ↓
           Close palette
```

## Persistence Flow

```
Component Mount
     ↓
Check persistKey
     ↓
┌─────────────────────────┐
│  localStorage.getItem() │
└───────────┬─────────────┘
            │
       Found data?
            │
       ┌────┴────┐
       │         │
      Yes        No
       │         │
   Parse JSON  Empty []
       │         │
   Restore    Initialize
    stack       fresh
       │         │
       └────┬────┘
            ↓
    useCommandFlow
        state
            │
            │
      User interacts
     (push/pop/reset)
            │
            ↓
┌─────────────────────────┐
│ localStorage.setItem()  │
│  JSON.stringify(stack)  │
└─────────────────────────┘
```

## Error Handling Flow

```
Command Execution
     ↓
┌────────────────────┐
│  Try execute       │
└────────┬───────────┘
         │
    Succeeded?
         │
    ┌────┴────┐
    │         │
   Yes        No
    │         │
Close      Log error
dialog        │
    │         │
    │    Show toast
    │         │
    │    Keep open
    │         │
    └────┬────┘
         ↓
    User sees
    feedback
```

## Animation Timeline

```
Level Transition (300ms)

0ms:   User selects command
       │
20ms:  isNavigating = true
       │
       └─ opacity: 1 → 0 (200ms)
              │
              ├─ Stack updates
              ├─ Level increments
              └─ Commands change
220ms:        │
              └─ opacity: 0 → 1 (100ms)
320ms:        │
       isNavigating = false
       │
       ↓
   Animation complete
```
