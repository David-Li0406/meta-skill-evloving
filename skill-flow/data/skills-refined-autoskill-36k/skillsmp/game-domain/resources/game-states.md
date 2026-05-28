# Game States and Transitions

Complete reference for game state machine in ActionPhase.

## Game States

```sql
state CHECK (state IN (
    'setup',
    'recruitment',
    'character_creation',
    'in_progress',
    'paused',
    'completed',
    'cancelled'
))
```

## State Definitions

### SETUP
- Initial creation state
- GM configures game details
- Not visible to players yet
- Can edit all settings

### RECRUITMENT
- Game listed publicly (if is_public=true)
- Players can apply to join
- GM reviews applications
- Continues until GM closes or deadline

### CHARACTER_CREATION
- Approved players create characters
- GM reviews character sheets
- Approve/reject workflow
- Continues until all characters approved

### IN_PROGRESS
- Active gameplay
- Phase cycles running
- Players posting and acting
- GM managing phases

### PAUSED
- Temporarily suspended
- No phase advancement
- Resumes with same phase

### COMPLETED
- Game ended normally
- Archive becomes public
- Action submissions revealed
- Read-only state

### CANCELLED
- Game terminated early
- Partial archive
- Marked as cancelled

## State Transition Rules

**SETUP → RECRUITMENT**
- GM ready to accept players
- Game details finalized
- API: `PUT /api/v1/games/{id}/state {"state": "recruitment"}`

**RECRUITMENT → CHARACTER_CREATION**
- GM closes recruitment
- Player slots filled
- API: `PUT /api/v1/games/{id}/state {"state": "character_creation"}`

**CHARACTER_CREATION → IN_PROGRESS**
- All players have approved characters
- GM starts game
- First phase created
- API: `PUT /api/v1/games/{id}/state {"state": "in_progress"}`

**IN_PROGRESS → PAUSED**
- GM pauses game temporarily
- API: `PUT /api/v1/games/{id}/state {"state": "paused"}`

**PAUSED → IN_PROGRESS**
- GM resumes game
- API: `PUT /api/v1/games/{id}/state {"state": "in_progress"}`

**IN_PROGRESS → COMPLETED**
- GM ends game normally
- API: `PUT /api/v1/games/{id}/state {"state": "completed"}`

**ANY STATE → CANCELLED**
- GM cancels game
- API: `PUT /api/v1/games/{id}/state {"state": "cancelled"}`

---

**Back to**: [SKILL.md](../SKILL.md)
