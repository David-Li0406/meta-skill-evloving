# Game AI Behavior Trees

## Patterns


---
  #### **Name**
Selector-Sequence Basics
  #### **Description**
Core behavior tree patterns for decision making
  #### **When**
Building any behavior tree
  #### **Example**
    // Selector: Try children until one succeeds
    // (OR logic - "try this, else try that")
    
    [Selector: Combat Response]
      ├── [Sequence: Flee if Low Health]
      │     ├── [Condition: Health < 20%]
      │     └── [Action: Flee to Cover]
      ├── [Sequence: Attack if Has Target]
      │     ├── [Condition: Has Valid Target]
      │     └── [Action: Attack Target]
      └── [Action: Patrol]  // Default fallback
    
    // Sequence: All children must succeed
    // (AND logic - "do this, then this, then this")
    
    [Sequence: Open Door]
      ├── [Action: Move to Door]
      ├── [Condition: Is Door Locked?]
      │     └── [Action: Pick Lock] // Only if locked
      └── [Action: Open Door]
    

---
  #### **Name**
Blackboard Communication
  #### **Description**
Shared data between nodes and systems
  #### **When**
Nodes need to share state or receive external input
  #### **Example**
    // Blackboard holds shared data
    class AIBlackboard {
        target: Entity = null
        lastKnownPosition: Vector3 = null
        alertLevel: AlertLevel = CALM
        currentObjective: Objective = null
    
        // LLM can write high-level decisions here
        llmDecision: string = null
        llmDecisionTimestamp: float = 0
    }
    
    // Nodes read from blackboard
    class HasTargetCondition extends BTCondition {
        evaluate(): boolean {
            return blackboard.target != null
        }
    }
    
    // LLM integration node
    class LLMDecisionNode extends BTNode {
        tick(): Status {
            // Only query LLM occasionally, not every tick
            if (time - blackboard.llmDecisionTimestamp > LLM_COOLDOWN) {
                queryLLMForDecision()
                return RUNNING
            }
            return interpretLLMDecision(blackboard.llmDecision)
        }
    }
    

---
  #### **Name**
LLM-Enhanced Decision Making
  #### **Description**
Using LLM for high-level decisions in behavior tree
  #### **When**
NPCs need contextual, dynamic decision-making
  #### **Example**
    // LLM sits at TOP of tree, makes strategic decisions
    // BT nodes execute those decisions efficiently
    
    [Selector: NPC Main Loop]
      ├── [LLM Strategic Advisor]  // Queries LLM every N seconds
      │     └── Sets blackboard.currentStrategy
      ├── [Selector: Execute Strategy]
      │     ├── [Sequence: Strategy = "negotiate"]
      │     │     └── [Subtree: Dialogue Behavior]
      │     ├── [Sequence: Strategy = "attack"]
      │     │     └── [Subtree: Combat Behavior]
      │     ├── [Sequence: Strategy = "flee"]
      │     │     └── [Subtree: Retreat Behavior]
      │     └── [Subtree: Default Patrol]
    
    // LLM query (cached, not every frame)
    class LLMStrategicAdvisor extends BTNode {
        private cooldown: float = 5.0  // Query every 5 seconds max
    
        tick(): Status {
            if (!shouldQueryLLM()) return SUCCESS
    
            // Build context from game state
            context = buildContext(blackboard)
    
            // Async query - don't block
            llm.queryAsync(context, (response) => {
                blackboard.currentStrategy = parseStrategy(response)
            })
    
            return SUCCESS  // Don't wait for response
        }
    }
    

---
  #### **Name**
Parallel Behaviors
  #### **Description**
Running multiple behaviors simultaneously
  #### **When**
NPC needs to do multiple things at once
  #### **Example**
    // Parallel node runs children simultaneously
    
    [Parallel: Combat + Awareness]
      ├── [Subtree: Combat Actions]
      │     ├── [Selector: Attack or Take Cover]
      │     └── [Action: Reload if Needed]
      └── [Subtree: Awareness]
            ├── [Action: Scan for Threats]
            └── [Action: Update Team Blackboard]
    
    // Combat continues while awareness runs
    // Both contribute to blackboard
    // Main tree reads combined state
    

## Anti-Patterns


---
  #### **Name**
God Node
  #### **Description**
Single node that does everything
  #### **Why**
Not reusable, hard to debug, defeats purpose of trees
  #### **Instead**
Break into small, focused nodes. Each node does one thing.

---
  #### **Name**
Deep Nesting
  #### **Description**
Trees nested 10+ levels deep
  #### **Why**
Hard to understand, hard to debug, often indicates design problem
  #### **Instead**
Use subtrees for modularity. Flatten where possible.

---
  #### **Name**
Polling LLM Every Tick
  #### **Description**
Querying LLM in every behavior tree tick
  #### **Why**
Latency makes this impossible. Cost is prohibitive.
  #### **Instead**
Query LLM on cooldown (5-30 sec), cache decisions on blackboard.

---
  #### **Name**
Ignoring Failure States
  #### **Description**
Not handling node failures gracefully
  #### **Why**
Behavior breaks silently, NPCs get stuck
  #### **Instead**
Always have fallback behaviors. Log failures.