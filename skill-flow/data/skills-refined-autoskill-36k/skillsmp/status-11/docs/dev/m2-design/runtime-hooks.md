# Runtime Integration Hooks and Rollback Semantics

This document specifies how validated branch proposals are integrated into the story runtime and how to safely rollback if errors occur.

## Overview

The **runtime integration** process safely injects an AI-generated branch into the active story without corrupting game state. The **rollback mechanism** allows automatic recovery if the branch fails or contradicts the main story.

Key principles:
- **Safe injection**: Branches can only be injected at designated hook points
- **Atomic transactions**: Either the branch integrates fully, or not at all
- **Automatic recovery**: On error, system rolls back to last known good state without player intervention
- **Audit trail**: All integrations/rollbacks logged for analysis and reproducibility

## Runtime Hook Points

Branches can only be injected at **safe insertion points** in the story runtime. Hook points are moments where:
1. The story is awaiting player input (choice point, dialogue, etc.)
2. Save state is consistent and complete
3. No active animations, cutscenes, or scripted sequences are running
4. Player character state won't be corrupted by branch injection

### Hook Point Categories

#### Category 1: Scene Boundaries

**Description**: Transition between scenes (safe point to insert branch)

```
Scene A (complete) → Hook Point → Branch Injected → Scene B (main story resumes)
```

**Characteristics**:
- Scene has fully loaded and reached stable state
- All NPCs have finished initialization
- Environment is fully rendered
- Save game is written to disk

**Implementation**:
```python
# In scene manager
def on_scene_ready():
    """Called when scene is fully loaded and ready for player input."""
    # Check if branch is ready to integrate
    if branch_queue.has_ready_proposal():
        branch = branch_queue.peek()
        inject_branch_at_scene_boundary(branch)
    else:
        unlock_player_input()
```

**Properties**:
- ✓ Safe: Scene is at rest
- ✓ Clear: Player sees scene transition naturally
- ✓ Persistent: Safe to save before/after integration
- Latency: 100–500ms (acceptable before scene loads)

#### Category 2: Choice Point (Dialogue/Interaction)

**Description**: Transition between dialogue choices (safe point to inject branch)

```
Dialogue A → Player makes choice → Hook Point → Branch Dialogue OR Main Story
```

**Characteristics**:
- Player has made a choice (input locked)
- Dialogue system is processing the choice
- Scene is stable; no movement is happening
- State snapshot exists

**Implementation**:
```python
# In dialogue system
def process_player_choice(choice_id: str):
    """Process player's dialogue choice."""
    # Snapshot state
    state_before = save_game_to_memory()
    
    # Check if branch should be offered
    if should_offer_branch(choice_id):
        branch = get_approved_branch()
        if integrate_branch(branch, state_before):
            return RESULT_BRANCH_INTEGRATED
    
    # Otherwise, continue main story
    return process_main_story_choice(choice_id)
```

**Properties**:
- ✓ Very safe: Player input locked; state is known
- ✓ Natural: Player is already expecting outcome
- ✓ Recoverable: Easy to rollback to pre-choice state
- Latency: 500–2000ms (acceptable during choice processing)

#### Category 3: Quest/Event Checkpoint

**Description**: Completion of a quest or major event (safe point to inject branch)

```
Quest A Complete → Hook Point → Branch Quest OR Main Story Quest B
```

**Characteristics**:
- Quest has completed; quest reward given
- State has been saved after quest completion
- No active dialogue or combat
- Clear narrative break point

**Implementation**:
```python
# In quest system
def on_quest_complete(quest_id: str, completion_data: dict):
    """Called when player completes a quest."""
    # Save quest completion
    save_quest_completion(quest_id, completion_data)
    
    # Check for branch injection opportunity
    if should_inject_branch_after_quest(quest_id):
        branch = get_approved_branch_for_quest(quest_id)
        # Branch starts where quest ended (same location, same time)
        integrate_branch(branch, parent_quest=quest_id)
    else:
        # Continue with main story
        advance_main_quest_line()
```

**Properties**:
- ✓ Safe: Clear story break point
- ✓ Justified: Branch is outcome of quest
- ✓ Persistent: Quest completion is saved before branch
- Latency: <1000ms (acceptable during quest wrap-up)

#### Category 4: Rest/Load State

**Description**: Player sleeps, fast-travels, or loads a save (safe point to pre-load branches)

```
Player sleeps → Hook Point → Load pre-generated branches for next location
```

**Characteristics**:
- Player is not actively playing
- State is stable and saved
- Background processing is acceptable
- Pre-loading can happen asynchronously

**Implementation**:
```python
# In rest/travel system
async def on_player_rest():
    """Called when player rests. Pre-load branches for next day."""
    next_location = player.planned_destination
    next_npcs = predict_npcs_at_location(next_location)
    
    # Background: request branch proposals for likely encounters
    for npc in next_npcs:
        request_background_branch_generation(
            lore=current_lore,
            npc=npc,
            priority='background',  # Low priority; don't wait
            deadline='before_scene_load'
        )
```

**Properties**:
- ✓ Non-blocking: Happens in background
- ✓ Flexible: Can prepare multiple branches
- ⚠ Speculative: May generate branches that don't get used
- Latency: Asynchronous (no impact on player experience)

#### Category 5: Combat Victory Moment

**Description**: After combat victory, before reward screen (safe point for combat-related branches)

```
Combat victory → Hook Point → Vanquished enemy speaks OR Main story continues
```

**Characteristics**:
- Combat has concluded; enemy defeated
- Combat UI is clearing
- Player character is out of danger
- Victory state snapshot exists

**Implementation**:
```python
# In combat system
def on_combat_victory(defeated_enemy: Actor):
    """Called when player wins combat."""
    # Snapshot state after victory
    state = save_game_to_memory()
    
    # Check for branch: defeated enemy final dialogue?
    if should_offer_branch_for_defeated_enemy(defeated_enemy):
        branch = get_branch_for_enemy(defeated_enemy)
        integrate_branch(branch, state, context={'defeated_enemy': defeated_enemy})
    
    # Otherwise show victory rewards
    show_victory_rewards()
```

**Properties**:
- ✓ Thematic: Natural moment for enemy reflection
- ✓ Safe: Combat won't resume
- ✓ Clear: Victory is guaranteed
- Latency: <1500ms (acceptable during victory wrap-up)

### Hook Points NOT Allowed

These are **unsafe** and branches cannot be injected:

- ❌ **During combat**: Could interrupt turn order or damage calculations
- ❌ **During cutscenes**: Would desync cinematic and story
- ❌ **During character animations**: Would corrupt animation state
- ❌ **During load/save operations**: Could corrupt save data
- ❌ **During inventory interaction**: Could corrupt item state
- ❌ **Concurrent with other branches**: Prevents state consistency

## Branch Integration State Machine

### States

```
                                    ┌──────────────┐
                                    │  SUBMITTED   │
                                    └──────────────┘
                                            ↓
                                    ┌──────────────┐
                        ┌──────────→│ VALIDATING   │←──────────┐
                        │           └──────────────┘           │
                        │                   ↓                  │
                        │           ┌──────────────┐          │
                        │           │  VALIDATED   │          │
                        │           └──────────────┘          │
                        │                   ↓                  │
                        │           ┌──────────────┐          │
                        ├──────────→│  REJECTED    │←─────────┤
                        │           └──────────────┘          │
                        │                                      │
                        │           ┌──────────────┐          │
                        └──────────→│   QUEUED     │←─────────┘
                                    └──────────────┘
                                            ↓
                                    ┌──────────────┐
                                    │  PRESENTING  │
                                    └──────────────┘
                                            ↓
                    ┌───────────────────────┴───────────────────────┐
                    ↓                                                 ↓
            ┌──────────────┐                                ┌──────────────┐
            │  INTEGRATING │                                │   DECLINED   │
            └──────────────┘                                └──────────────┘
                    ↓
            ┌──────────────┐
            │ INTEGRATED   │
            └──────────────┘
                    ↓
            ┌──────────────┐
            │  EXECUTING   │
            └──────────────┘
                    ↓
        ┌───────────┴───────────┐
        ↓                       ↓
   ┌──────────┐          ┌──────────────┐
   │ REVERTED │          │  ARCHIVED    │
   └──────────┘          └──────────────┘
```

### State Descriptions

| State | Meaning | Triggered By | Actions |
|-------|---------|--------------|---------|
| **SUBMITTED** | Branch proposal created, awaiting validation | AI Writer generates proposal | Validate against policy ruleset |
| **VALIDATING** | Policy/sanitization pipeline running | ValidationPipeline.validate() | Check rules, apply transforms, compute risk score |
| **VALIDATED** | Proposal passed validation | Policy checks complete, no critical violations | Move to queue or reject if issues found |
| **REJECTED** | Proposal failed validation | Critical policy violations found | Log violations, archive proposal, discard |
| **QUEUED** | Validated proposal waiting for runtime insertion | Branch approved by Director | Wait for hook point; OR timeout after N minutes |
| **PRESENTING** | Branch is being offered to player (e.g., as dialogue choice) | Hook point reached; branch is safe to offer | Show branch option; allow player to accept/decline |
| **DECLINED** | Player declined the branch | Player chooses main story path | Archive as "declined"; no integration |
| **INTEGRATING** | Branch is being injected into runtime | Player accepted branch; lock player input | Inject branch content; establish rollback point |
| **INTEGRATED** | Branch successfully injected; execution starting | Injection complete; save checkpoint | Execute branch dialogue/story; allow player input |
| **EXECUTING** | Branch is actively playing | Branch started; player is making choices | Execute branch dialogue/choices; track state |
| **REVERTED** | Branch encountered error; automatic rollback triggered | Runtime error during branch execution | Restore state snapshot; resume main story |
| **ARCHIVED** | Branch completed successfully or timed out | Branch finished OR timeout reached | Log telemetry; store for analysis; clean up |

### State Transitions

```python
class BranchProposalStateMachine:
    """Manages branch proposal lifecycle."""
    
    # SUBMITTED → VALIDATING
    def validate(self):
        """Start validation pipeline."""
        self.state = 'VALIDATING'
        try:
            results = validation_pipeline.run(self.proposal)
            if results.has_critical_violations():
                self.state = 'REJECTED'
                self.rejection_reason = results.violations
            else:
                self.state = 'VALIDATED'
                self.validation_results = results
        except Exception as e:
            self.state = 'REJECTED'
            self.rejection_reason = f"Validation error: {e}"
    
    # VALIDATED → QUEUED
    def queue_for_integration(self):
        """Move to runtime queue."""
        if self.state != 'VALIDATED':
            raise StateError(f"Can't queue from state {self.state}")
        self.state = 'QUEUED'
        self.queued_at = now()
    
    # QUEUED → PRESENTING
    def present_to_player(self):
        """Branch is being offered to player."""
        if self.state != 'QUEUED':
            raise StateError(f"Can't present from state {self.state}")
        self.state = 'PRESENTING'
        self.presented_at = now()
    
    # PRESENTING → INTEGRATING (accepted) OR DECLINED (rejected)
    def on_player_choice(self, choice: str):
        """Player accepts or declines branch."""
        if choice == 'accept':
            self.state = 'INTEGRATING'
            self.snapshot_state()  # Save rollback point
        elif choice == 'decline':
            self.state = 'DECLINED'
    
    # INTEGRATING → INTEGRATED
    def confirm_integration(self):
        """Branch successfully injected."""
        if self.state != 'INTEGRATING':
            raise StateError(f"Can't confirm from state {self.state}")
        self.state = 'INTEGRATED'
        self.integrated_at = now()
        self.state = 'EXECUTING'
    
    # EXECUTING → REVERTED (error) OR ARCHIVED (success)
    def on_branch_complete(self, success: bool, error: str = None):
        """Branch execution finished."""
        if not success:
            self.state = 'REVERTED'
            self.error = error
            self.rollback()
        else:
            self.state = 'ARCHIVED'
            self.completed_at = now()
```

## Rollback Semantics

### Ink Variable State Management

When integrating branches, the runtime must capture and potentially restore Ink story state, including all variables.

#### Ink State Snapshot

Before branch integration, capture the complete Ink state:

```javascript
function captureInkState(story) {
    return {
        // Capture all Ink variables
        variablesState: JSON.stringify(story.variablesState.jsonToken),
        
        // Capture visit counts (how many times each knot was visited)
        visitCounts: JSON.stringify(story.state.visitCounts),
        
        // Capture current path in story
        currentPath: story.state.currentPathString,
        
        // Capture choice threads if any
        currentChoices: story.currentChoices.map(c => ({
            text: c.text,
            index: c.index,
            targetPath: c.targetPath
        }))
    };
}
```

#### Ink State Restoration (Rollback)

If rollback is required, restore the Ink state:

```javascript
function restoreInkState(story, snapshot) {
    // Restore variables
    story.variablesState.jsonToken = JSON.parse(snapshot.variablesState);
    
    // Restore visit counts
    story.state.visitCounts = JSON.parse(snapshot.visitCounts);
    
    // Reset to the saved path
    story.ChoosePathString(snapshot.currentPath);
    
    // Rebuild choices
    story.Continue();  // Re-evaluate to restore choices
}
```

**Critical**: Ink variables modified during branch execution are automatically undone by restoring the `variablesState` snapshot. This includes:
- Global variables (`VAR player_health = 100`)
- Temporary variables (`temp local_var = "value"`)
- List state (`LIST inventory = (torch), compass, map`)

### Rollback Mechanism

When a branch encounters a critical error during execution, the system **automatically reverts** to the last known good state without requiring player intervention.

#### Rollback Process

```
1. Error Detection
   ↓
2. State Comparison (Branch state vs. Snapshot)
   ↓
3. Rollback Execution
   ↓
4. Resume Main Story
   ↓
5. Log Event for Analysis
```

#### Step 1: Error Detection

The runtime monitors branch execution for critical errors:

```python
def monitor_branch_execution(branch: BranchProposal):
    """Monitor branch for errors that require rollback."""
    try:
        # Execute branch dialogue/story
        for dialogue_node in branch.dialogue_path:
            player_response = execute_dialogue(dialogue_node)
            
            # Monitor for errors
            if player_response.caused_error:
                raise RuntimeError(f"Dialogue error: {player_response.error}")
            
            # Check state consistency
            if not is_state_consistent():
                raise StateError("State corrupted during branch")
        
        # Branch completed successfully
        return RESULT_SUCCESS
        
    except Exception as e:
        return RESULT_ROLLBACK_REQUIRED, e
```

**Errors that trigger rollback**:
- Dialogue node references non-existent NPC
- Player stat/attribute would become invalid (negative HP, impossible alignment)
- Inventory inconsistency (item appears/disappears unexpectedly)
- Scene reference error (trying to load non-existent location)
- Relationship value out of bounds (-1.0 to 1.0)
- Dialogue choice references undefined outcome

**Errors that don't require rollback** (continue with branch):
- Minor dialogue typos
- Non-critical missing flavor text
- Minor variance in pacing

#### Step 2: State Comparison

Compare branch state against snapshot to identify what changed:

```python
def compare_states(snapshot: GameState, current: GameState) -> StateChange:
    """Identify what changed between snapshot and current state."""
    changes = StateChange()
    
    # Compare player attributes
    for attr in ['health', 'mana', 'inventory', 'relationships']:
        snapshot_val = snapshot.player[attr]
        current_val = current.player[attr]
        if snapshot_val != current_val:
            changes.add(attr, snapshot_val, current_val)
    
    # Compare quest state
    for quest_id, quest in current.quests.items():
        if quest_id not in snapshot.quests:
            changes.quest_added(quest_id)
        elif snapshot.quests[quest_id] != quest:
            changes.quest_modified(quest_id, snapshot.quests[quest_id], quest)
    
    # Compare scene/location
    if snapshot.scene != current.scene:
        changes.location_changed(snapshot.scene, current.scene)
    
    return changes
```

#### Step 3: Rollback Execution

Revert to snapshot state:

```python
def rollback_to_snapshot(snapshot: GameState):
    """Revert to snapshot state, undoing branch changes."""
    
    # 1. Restore player attributes
    for attr in ['health', 'mana', 'inventory', 'relationships', 'position']:
        current_state[attr] = snapshot[attr]
    
    # 2. Restore quest state
    for quest_id, quest in snapshot.quests.items():
        current_state.quests[quest_id] = quest
    
    # 3. Restore scene/location
    load_scene(snapshot.scene)
    move_player_to(snapshot.position)
    
    # 4. Clear any branch-added NPCs or objects
    for npc in current_state.scene.npcs:
        if npc.added_by_branch:
            despawn_npc(npc)
    
    # 5. Verify state consistency
    assert is_state_consistent()
    
    # 6. Notify player
    show_notification("Technical issue detected. Branch reset. Story continues.")
```

**Verification checklist**:
- ✓ Player attributes in valid range
- ✓ Inventory items still exist (not missing items)
- ✓ Relationships in valid range (-1.0 to 1.0)
- ✓ Scene exists and can be loaded
- ✓ Position is walkable (not stuck in wall)
- ✓ No orphaned quest markers or objectives

#### Step 4: Resume Main Story

After rollback, seamlessly resume main story:

```python
def resume_main_story_after_rollback(branch: BranchProposal, error: Exception):
    """Resume main story after branch rollback."""
    
    # Notify player
    game.show_notification(
        title="Technical Issue",
        message="We encountered a technical issue with a story branch. "
                "The story has been reset to the last safe point. "
                "You may continue the main story.",
        duration=5.0
    )
    
    # Log event
    telemetry.log_branch_rollback(
        branch_id=branch.id,
        error=str(error),
        player_state=current_state,
        timestamp=now()
    )
    
    # Resume main story from rollback point
    # The branch never happened; play continues as if player declined branch
    main_story.resume_from_hook_point()
```

#### Step 5: Log Event for Analysis

Record rollback for post-launch analysis:

```python
def log_branch_rollback(branch_id: str, error: str, state: dict):
    """Log rollback event for analysis."""
    event = {
        'event_type': 'branch_rollback',
        'timestamp': now(),
        'branch_id': branch_id,
        'error': error,
        'error_type': error.__class__.__name__,
        'player_state_hash': hash(state),
        'recovery_successful': True,  # If we got here, rollback succeeded
    }
    telemetry.push(event)
```

### Rollback Safety Properties

| Property | Guarantee |
|----------|-----------|
| **Atomicity** | Either branch fully integrates, or is fully rolled back. No partial states. |
| **Durability** | Snapshot is written to disk before integration. Rollback works even if game crashes. |
| **Idempotency** | Rolling back twice produces same result as rolling back once. Safe to retry. |
| **Consistency** | After rollback, all game systems are in valid state. Can resume immediately. |
| **Observability** | All rollbacks are logged and timestamped for analysis. |

## Persistence and Audit Trail

### What Gets Logged

```python
@dataclass
class IntegrationAuditLog:
    """Complete audit trail for branch integration."""
    
    # Identity
    branch_id: str
    branch_type: str
    proposal_version: str
    
    # Timing
    submitted_at: datetime
    integrated_at: datetime
    completed_at: datetime
    
    # State snapshots
    state_before_integration: dict  # Serialized game state
    state_after_integration: dict
    state_at_rollback: dict  # If rollback occurred
    
    # Outcome
    integration_status: str  # success, rolled_back, declined
    rollback_reason: str  # If rolled back
    
    # Metadata
    player_id: str
    save_slot: int
    play_time: float
    
    # Telemetry
    events: [
        {
            'type': str,  # dialogue_choice, npc_interaction, etc.
            'timestamp': datetime,
            'data': dict
        }
    ]
```

### Storage

```python
def save_integration_audit_log(log: IntegrationAuditLog):
    """Save audit log to persistent storage."""
    
    # In-game storage (JSON)
    path = f"logs/branch_audits/{log.branch_id}.json"
    with open(path, 'w') as f:
        json.dump(asdict(log), f, indent=2)
    
    # Optional: Cloud telemetry (for analysis post-launch)
    if telemetry_enabled:
        telemetry.push_audit_log(log)
```

## Integration Test Cases

### Test Case 1: Successful Integration

```python
def test_branch_integration_success():
    """Verify successful branch integration."""
    
    # Setup
    lore = load_test_lore('scenario_1')
    proposal = generate_test_proposal(lore)
    state_before = save_state_to_memory()
    
    # Execute
    result = integrate_branch(proposal)
    
    # Verify
    assert result.status == 'SUCCESS'
    assert branch.state == 'EXECUTING'
    assert current_state.position == proposal.expected_position
    assert current_state.scene == proposal.target_scene
```

### Test Case 2: Automatic Rollback on Error

```python
def test_branch_rollback_on_error():
    """Verify automatic rollback when branch encounters error."""
    
    # Setup
    proposal = create_broken_proposal()  # Will cause error mid-execution
    state_before = save_state_to_memory()
    
    # Execute
    result = integrate_branch(proposal)
    
    # Branch encounters error
    # Automatic rollback triggered
    
    # Verify
    assert branch.state == 'REVERTED'
    assert current_state == state_before
    assert current_state.scene == state_before.scene
    assert current_state.player.inventory == state_before.player.inventory
```

### Test Case 3: Rollback During Dialogue

```python
def test_rollback_during_dialogue_execution():
    """Verify rollback works mid-dialogue if error occurs."""
    
    # Setup
    proposal = load_test_proposal('dialogue_with_error_in_choice_3')
    state_before = save_state_to_memory()
    
    # Execute
    integrate_branch(proposal)
    player_makes_choice(choice_1)  # OK
    player_makes_choice(choice_2)  # OK
    player_makes_choice(choice_3)  # Error occurs here
    
    # Automatic rollback should occur
    
    # Verify
    assert current_state == state_before
    assert branch.state == 'REVERTED'
    assert player.position == state_before.player.position
```

### Test Case 4: Save/Load During Branch Execution

```python
def test_save_load_during_branch():
    """Verify save/load works correctly during branch execution."""
    
    # Setup
    proposal = load_test_proposal('dialogue_branch')
    integrate_branch(proposal)
    
    # Execute part of branch
    player_makes_choice(choice_1)
    state_mid_branch = current_state
    
    # Save game
    save_game()
    
    # Load game
    load_game()
    
    # Verify
    assert current_state == state_mid_branch
    assert current_scene.active_dialogue == state_mid_branch.dialogue_context
```

### Test Case 5: Concurrent Branches (Should Fail)

```python
def test_concurrent_branches_prevented():
    """Verify that two branches can't integrate concurrently."""
    
    # Setup
    proposal_1 = load_test_proposal('dialogue_1')
    proposal_2 = load_test_proposal('dialogue_2')
    
    # Start integration of proposal_1
    integrate_branch(proposal_1)
    assert branch_1.state == 'EXECUTING'
    
    # Attempt to integrate proposal_2 (should fail)
    result = integrate_branch(proposal_2)
    
    # Verify
    assert result.status == 'FAILED'
    assert result.reason == 'Another branch is already executing'
    assert proposal_2.state == 'QUEUED'  # Goes back to queue
```

### Test Case 6: Hook Point Validation

```python
def test_hook_point_validation():
    """Verify branches can only integrate at valid hook points."""
    
    # Hook point VALID: Scene loaded, player input ready
    hook_point = create_scene_ready_hook()
    proposal = load_test_proposal('dialogue_branch')
    result = integrate_branch(proposal, hook_point=hook_point)
    assert result.status == 'SUCCESS'
    
    # Hook point INVALID: Combat in progress
    hook_point_invalid = create_combat_in_progress_hook()
    result = integrate_branch(proposal, hook_point=hook_point_invalid)
    assert result.status == 'FAILED'
    assert result.reason == 'Invalid hook point'
```

---

**Status**: Runtime integration hooks and rollback semantics fully specified. Ready for implementation phase.
