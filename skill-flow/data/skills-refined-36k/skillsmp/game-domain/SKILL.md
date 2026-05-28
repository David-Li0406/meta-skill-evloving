---
name: game-domain
description: Complete game lifecycle and domain patterns for ActionPhase turn-based gaming platform. Covers game states, phase transitions (common room, action, results), character workflows (creation, approval, death), messaging systems (common room posts, private messages, GM results), action submissions, and the complete flow from recruitment through game completion. Use when working with game state management, phase advancement, character status, or understanding game mechanics.
---

# ActionPhase Game Domain

## Purpose

Comprehensive guide to the game lifecycle, state management, phase transitions, and player workflows in ActionPhase's turn-based gaming system.

## When to Use This Skill

- Understanding game flow and state transitions
- Implementing phase management (common room, action, results)
- Working with character workflows and approvals
- Building messaging systems (posts, comments, private messages)
- Managing action submissions and GM results
- Debugging game state issues
- Designing features that interact with game mechanics

---

## Game Lifecycle Overview

### Complete Game Flow

```
1. SETUP → 2. RECRUITMENT → 3. CHARACTER_CREATION → 4. IN_PROGRESS → 5. COMPLETED/CANCELLED
```

**IN_PROGRESS** contains the repeating phase cycle:
```
COMMON ROOM (discussion) → ACTION (submissions) → RESULTS (GM feedback) → [repeat]
```

**See**: [game-states.md](resources/game-states.md) for complete state definitions and transition rules

---

## Quick Reference

### Game States

```sql
state CHECK (state IN (
    'setup',              -- Initial creation
    'recruitment',        -- Accepting players
    'character_creation', -- Players creating characters
    'in_progress',        -- Active gameplay
    'paused',            -- Temporarily suspended
    'completed',         -- Finished normally
    'cancelled'          -- Terminated early
))
```

**See**: [game-states.md](resources/game-states.md)

### Phase Types

```sql
phase_type CHECK (phase_type IN (
    'common_room',  -- Discussion/planning phase
    'action',       -- Players submit actions
    'results'       -- GM publishes results
))
```

**See**: [phase-system.md](resources/phase-system.md)

### Character Status

```sql
status CHECK (status IN (
    'pending',    -- Awaiting GM review
    'approved',   -- GM approved, waiting for game start
    'active',     -- In gameplay
    'rejected',   -- GM rejected
    'dead'        -- Died in-game
))
```

**See**: [character-workflows.md](resources/character-workflows.md)

---

## Core Concepts

### 1. Game State Machine

Games transition through defined states with specific rules for advancement.

- **SETUP**: GM configures game
- **RECRUITMENT**: Players apply to join
- **CHARACTER_CREATION**: Players create characters, GM approves
- **IN_PROGRESS**: Active gameplay with phase cycles
- **COMPLETED**: Game ends normally, archive becomes public
- **CANCELLED**: Game terminates early

**Details**: [game-states.md](resources/game-states.md)

### 2. Phase Cycle (The Game Loop)

The repeating cycle during IN_PROGRESS state:

1. **COMMON ROOM**: Public discussion forum, planning, coordination
2. **ACTION**: Private action submissions, one per player
3. **RESULTS**: GM sends private results to each player

**Details**: [phase-system.md](resources/phase-system.md)

### 3. Character Lifecycle

Players create characters that go through approval workflow:

**PENDING** → **APPROVED** → **ACTIVE** (when game starts)

Or: **PENDING** → **REJECTED** (player revises and resubmits)

Or: **ACTIVE** → **DEAD** (character dies, may create new one)

**Details**: [character-workflows.md](resources/character-workflows.md)

### 4. Messaging System

Four distinct message types with different visibility rules:

- **Common Room Posts**: Public to all participants
- **Private Messages**: Between specific characters
- **Action Submissions**: Private to player (GM sees after ACTION phase)
- **GM Results**: Private GM → player messages

**Details**: [messaging-system.md](resources/messaging-system.md)

---

## Data Models

### Core Tables

**games**
- Game metadata, state, GM
- Recruitment settings
- Date tracking

**game_participants**
- Players, co-GMs, audience
- Role and status tracking

**characters**
- Player characters and NPCs
- Type and status workflow

**game_phases**
- Phase history and current phase
- Type, number, timing

**posts** + **comments**
- Common room discussions

**private_messages**
- Character-to-character messages

**action_submissions**
- Player actions during ACTION phase

**action_results**
- GM results during RESULTS phase

**See**: [data-models.md](resources/data-models.md) for complete schema

---

## API Endpoints

### Game Management
```
GET/POST/PUT/DELETE  /api/v1/games
PUT                  /api/v1/games/{id}/state
```

### Characters
```
GET/POST  /api/v1/games/{game_id}/characters
POST      /api/v1/characters/{id}/approve
POST      /api/v1/characters/{id}/reject
```

### Phases
```
GET   /api/v1/games/{game_id}/phases
POST  /api/v1/phases/advance
GET   /api/v1/games/{game_id}/phases/current
```

### Messaging
```
GET/POST  /api/v1/games/{game_id}/posts
GET/POST  /api/v1/games/{game_id}/posts/{id}/comments
GET/POST  /api/v1/games/{game_id}/messages/private
```

### Actions & Results
```
GET/POST/PUT  /api/v1/phases/{phase_id}/actions
GET           /api/v1/phases/{phase_id}/actions/all  (GM only)
POST          /api/v1/phases/{phase_id}/results      (GM only)
GET           /api/v1/phases/{phase_id}/results      (Player)
```

**See**: [api-reference.md](resources/api-reference.md) for complete API documentation

---

## Business Rules

### Key Constraints

- ✅ Only ONE active phase per game
- ✅ One action submission per player per phase
- ✅ Actions locked after deadline
- ✅ Only GM can advance phases
- ✅ Must have ACTIVE character to post/act
- ✅ Action submissions hidden from GM until ACTION phase ends
- ✅ Private messages never visible to GM (unless included)
- ✅ Results remain private forever (unless player shares)

**See**: [business-rules.md](resources/business-rules.md) for complete rules

---

## Common Workflows

### Workflow 1: Complete Game Setup to First Phase

```bash
# 1. Create game → 2. Open recruitment → 3. Move to character creation
# 4. Approve characters → 5. Start game → 6. Create first phase

# Full example in resources
```

### Workflow 2: Phase Advancement Cycle

```bash
# Common Room → ACTION → RESULTS → (new Common Room)

# Full example in resources
```

### Workflow 3: Character Death and Replacement

```bash
# Mark dead → Player creates new → GM approves → Becomes active

# Full example in resources
```

**See**: [workflows.md](resources/workflows.md) for complete workflow examples with curl commands

---

## Testing Patterns

### Test Complete Phase Cycle

```bash
# Load test fixtures
./backend/pkg/db/test_fixtures/apply_e2e.sh

# Login as GM and advance phase
./backend/scripts/api-test.sh login-gm
curl -X POST -H "Authorization: Bearer $(cat /tmp/api-token.txt)" \
  http://localhost:3000/api/v1/phases/advance \
  -d '{"game_id": 164}'

# Login as player and submit action
./backend/scripts/api-test.sh login-player
curl -X POST -H "Authorization: Bearer $(cat /tmp/api-token.txt)" \
  http://localhost:3000/api/v1/phases/456/actions \
  -d '{"content": "I investigate the library"}'
```

**See**: [testing-guide.md](resources/testing-guide.md) for complete testing patterns

---

## Database Queries

### Understanding Game State

```sql
-- Get game with current phase
SELECT g.id, g.title, g.state, gp.phase_type, gp.is_active
FROM games g
LEFT JOIN game_phases gp ON gp.game_id = g.id AND gp.is_active = true
WHERE g.id = 164;

-- Get phase history
SELECT phase_number, phase_type, start_time, end_time
FROM game_phases
WHERE game_id = 164
ORDER BY phase_number;

-- Get action submissions for phase
SELECT u.username, c.name, a.submitted_at
FROM action_submissions a
JOIN users u ON a.user_id = u.id
LEFT JOIN characters c ON a.character_id = c.id
WHERE a.phase_id = 456;
```

**See**: [database-queries.md](resources/database-queries.md) for complete query reference

---

## Navigation Guide

| Need to... | Read this |
|------------|-----------|
| Understand game states and transitions | [game-states.md](resources/game-states.md) |
| Learn phase cycle (common room → action → results) | [phase-system.md](resources/phase-system.md) |
| Understand character approval workflow | [character-workflows.md](resources/character-workflows.md) |
| Learn messaging types and visibility | [messaging-system.md](resources/messaging-system.md) |
| See complete data model | [data-models.md](resources/data-models.md) |
| Find API endpoints | [api-reference.md](resources/api-reference.md) |
| Understand business rules and constraints | [business-rules.md](resources/business-rules.md) |
| See workflow examples with code | [workflows.md](resources/workflows.md) |
| Learn testing patterns | [testing-guide.md](resources/testing-guide.md) |
| Find useful database queries | [database-queries.md](resources/database-queries.md) |

---

## Design Principles

### Privacy by Design
- Action submissions hidden from GM during ACTION phase
- Private messages never visible to GM (unless included)
- Results remain private between GM and player
- Dead characters cannot see new content

### Asynchronous by Default
- No real-time requirements
- Players work at their own pace
- Deadlines provide structure but no hard enforcement
- Email notifications for phase changes

### GM Control
- GM controls all phase advancement
- GM decides character approval
- GM manages game state
- GM sets deadlines and pacing

### Public Archive
- Completed games become public
- Action submissions revealed on completion
- Private messages remain private
- Results remain private
- Creates valuable reference material

---

## Related Skills & Context

### Skills
- **backend-dev-guidelines** - Implementing game domain services
- **route-tester** - Testing game API endpoints
- **frontend-dev-guidelines** - Building game UI components
- **game-phase-management** - Phase service implementation details
- **character-management** - Character-specific patterns
- **messaging-system** - Messaging implementation

### Context Files
- `.claude/context/ARCHITECTURE.md` - Service patterns
- `.claude/context/TEST_DATA.md` - Test fixtures with game data
- `.claude/context/TESTING.md` - Testing game workflows
- `.claude/reference/API_DOCUMENTATION.md` - Complete API reference

### Key Backend Files
- `backend/pkg/db/services/phases/` - Phase management service
- `backend/pkg/db/services/games.go` - Game state management
- `backend/pkg/db/services/characters.go` - Character workflow
- `backend/pkg/db/services/messages/` - Messaging services
- `backend/pkg/db/services/actions/` - Action submission service

---

## Quick Start

**New to ActionPhase game domain?** Read in this order:

1. [game-states.md](resources/game-states.md) - Understand the lifecycle
2. [phase-system.md](resources/phase-system.md) - Learn the phase cycle
3. [character-workflows.md](resources/character-workflows.md) - Character approval flow
4. [messaging-system.md](resources/messaging-system.md) - Message types and visibility
5. [workflows.md](resources/workflows.md) - See complete examples

**Implementing a feature?** Check:
- [api-reference.md](resources/api-reference.md) - Find the right endpoints
- [business-rules.md](resources/business-rules.md) - Understand constraints
- [data-models.md](resources/data-models.md) - Database schema

**Debugging?** Use:
- [database-queries.md](resources/database-queries.md) - Query game state
- [testing-guide.md](resources/testing-guide.md) - Test workflows

---

**Skill Status**: COMPLETE ✅
**Line Count**: < 500 ✅
**Progressive Disclosure**: 10 resource files ✅
**Coverage**: Full game lifecycle, state management, phase system, character workflow, messaging ✅
