# LLM-Assisted Game Development

## Patterns


---
  #### **Name**
Spec-First Development
  #### **Description**
Define specifications before generating code
  #### **When**
Starting any non-trivial feature
  #### **Example**
    // WRONG: Jumping straight to code
    // Prompt: "Make a health system for my game"
    
    // RIGHT: Spec first, then implement
    // Phase 1: Define the spec with AI assistance
    
    const healthSystemSpec = `
    ## Health System Specification
    
    ### Core Requirements
    - Player starts with 100 HP
    - HP can be damaged by enemies, environment
    - HP regenerates 1/sec when out of combat
    - Visual indicator: HP bar, screen flash on damage
    
    ### Edge Cases
    - HP cannot go below 0 or above maxHP
    - Death triggers on HP reaching 0
    - Invincibility frames after damage (0.5s)
    
    ### Integration Points
    - Enemy.attack() calls Player.takeDamage()
    - HealthUI subscribes to HP changes
    - SaveSystem includes current HP
    
    ### Testing Criteria
    - Damage reduces HP correctly
    - Can't take damage during invincibility
    - Death triggers at exactly 0 HP
    - Save/load preserves HP
    `
    
    // Phase 2: Generate implementation from spec
    // Prompt: "Implement this health system spec in Unity C#:
    // [paste spec]
    // Follow Unity best practices, use events for HP changes."
    

---
  #### **Name**
Incremental Complexity
  #### **Description**
Build features in small, testable increments
  #### **When**
Building any multi-part system
  #### **Example**
    // Build incrementally, test each step before proceeding
    
    // Step 1: Minimal working version
    // Prompt: "Create a basic enemy that moves toward player in Godot"
    // Test: Does enemy move? Correct direction?
    
    // Step 2: Add one behavior
    // Prompt: "Add to this enemy: stop and attack when within 2 units"
    // Provide: Previous code
    // Test: Does it stop? Attack animation plays?
    
    // Step 3: Add polish
    // Prompt: "Add to this enemy: patrol between points when player far"
    // Provide: Previous code + patrol point setup
    // Test: Patrol works? Transitions smoothly?
    
    // WRONG: All at once
    // "Make an enemy that patrols, chases player, attacks,
    // has multiple attacks, drops loot, has a health bar..."
    // Result: Buggy mess, hard to debug
    

---
  #### **Name**
Context Window Management
  #### **Description**
Strategically manage what context the LLM sees
  #### **When**
Working on complex projects with many files
  #### **Example**
    // LLMs can't see your whole codebase. Feed relevant context.
    
    // Minimal context (fast, focused):
    const prompt = `
    Fix the jump bug in this PlayerController:
    \`\`\`csharp
    ${currentFile}
    \`\`\`
    Bug: Player can jump mid-air.
    `
    
    // Medium context (for integration):
    const prompt = `
    Add enemy spawning to this game.
    
    Current game structure:
    - GameManager.cs: ${summaryOfGameManager}
    - Player.cs: Has TakeDamage(int amount) method
    - Enemy.cs: ${fullEnemyCode}
    
    Spawn enemies from points marked with "SpawnPoint" tag.
    `
    
    // Full context (for architecture):
    const prompt = `
    Review my game's architecture and suggest improvements.
    
    File structure:
    ${fileTree}
    
    Key files:
    GameManager.cs:
    ${gameManagerCode}
    
    Player.cs:
    ${playerCode}
    
    [... other relevant files ...]
    `
    
    // IMPORTANT: Always include error messages in full
    const debugPrompt = `
    Getting this error:
    \`\`\`
    ${fullErrorWithStackTrace}
    \`\`\`
    
    In this code:
    \`\`\`
    ${codeAroundError}
    \`\`\`
    `
    

---
  #### **Name**
Multi-Model Workflow
  #### **Description**
Use different models for different tasks
  #### **When**
Optimizing for speed and cost
  #### **Example**
    // Match model to task
    
    class AIWorkflow:
        fast_model = "claude-3-5-haiku"  // Quick, cheap
        strong_model = "claude-3-5-sonnet"  // Balanced
        power_model = "claude-opus-4"  // Maximum capability
    
        // Rapid iteration: fast model
        def quick_refactor(code, request):
            return self.fast_model.complete(
                f"Refactor this code: {request}\n{code}"
            )
    
        // Normal development: strong model
        def implement_feature(spec):
            return self.strong_model.complete(
                f"Implement: {spec}"
            )
    
        // Architecture decisions: power model
        def design_system(requirements):
            return self.power_model.complete(
                f"Design a system architecture for: {requirements}"
            )
    
        // Code review: strong model (needs nuance)
        def review_code(code):
            return self.strong_model.complete(
                f"Review for bugs, performance, best practices:\n{code}"
            )
    

---
  #### **Name**
Prompt Library
  #### **Description**
Build reusable prompts for common game dev tasks
  #### **When**
Doing repetitive tasks across projects
  #### **Example**
    // Build a library of battle-tested prompts
    
    const PROMPTS = {
        // Unity state machine
        unityStateMachine: (states, context) => `
            Create a Unity state machine with these states: ${states.join(', ')}
    
            Requirements:
            - Use ScriptableObject-based state pattern
            - Each state has Enter, Update, Exit methods
            - States can transition based on conditions
            - Include debug visualization
    
            Context: ${context}
        `,
    
        // Godot signal setup
        godotSignals: (nodePath, signals) => `
            Set up signals for this Godot node: ${nodePath}
    
            Signals needed: ${signals.join(', ')}
    
            Requirements:
            - Emit signals at appropriate times
            - Connect in _ready() using code (not editor)
            - Include type hints for signal parameters
            - Handle disconnection in _exit_tree()
        `,
    
        // Bug fix template
        bugFix: (code, error, behavior) => `
            Bug report:
            Expected: ${behavior.expected}
            Actual: ${behavior.actual}
    
            Error (if any): ${error}
    
            Code:
            \`\`\`
            ${code}
            \`\`\`
    
            Identify the bug and provide a minimal fix.
            Explain why the bug occurred.
        `,
    
        // Optimization review
        optimize: (code, target) => `
            Optimize this code for ${target}:
            \`\`\`
            ${code}
            \`\`\`
    
            Constraints:
            - Must maintain same behavior
            - Explain performance impact of each change
            - Consider memory vs CPU tradeoffs
        `
    }
    

---
  #### **Name**
AI-Assisted Debugging
  #### **Description**
Use LLMs to debug, but verify fixes
  #### **When**
Encountering bugs in AI-generated or human code
  #### **Example**
    // LLM debugging workflow
    
    class AIDebugger:
        def debug(self, code, error, context):
            // Step 1: Get AI's analysis
            analysis = llm.complete(f"""
            Analyze this bug:
    
            Code: {code}
            Error: {error}
            Context: {context}
    
            Provide:
            1. Root cause analysis
            2. Suggested fix
            3. Potential side effects of fix
            """)
    
            // Step 2: VERIFY before applying
            // Don't blindly trust the fix!
    
            // Step 3: If fix works, understand WHY
            // Ask: "Explain why the original code failed"
    
            // Step 4: Add test to prevent regression
            test = llm.complete(f"""
            Write a unit test that would catch this bug:
            Original bug: {error}
            Fixed code: {fixedCode}
            """)
    
            return {
                analysis,
                fix: "REVIEW BEFORE APPLYING",
                test
            }
    
    // IMPORTANT: AI fixes sometimes mask bugs
    // If AI suggests adding a null check, ask WHY it's null
    // The null might be the symptom, not the disease
    

## Anti-Patterns


---
  #### **Name**
Prompt and Pray
  #### **Description**
Generating code without clear specifications
  #### **Why**
Vague prompts yield vague code that seems to work but breaks
  #### **Instead**
Write specs first. Define edge cases. Then prompt.

---
  #### **Name**
Context Dumping
  #### **Description**
Pasting entire codebase into prompts
  #### **Why**
Context overload confuses models, hits token limits
  #### **Instead**
Curate context. Include only what's relevant to the task.

---
  #### **Name**
No Verification
  #### **Description**
Accepting AI output without testing
  #### **Why**
LLMs hallucinate APIs, methods, and logic that looks right but isn't
  #### **Instead**
Test every piece of generated code. Review like a PR.

---
  #### **Name**
Monolithic Generation
  #### **Description**
Asking for entire systems in one prompt
  #### **Why**
Complex prompts yield buggy, incomplete results
  #### **Instead**
Incremental complexity. Build and test piece by piece.

---
  #### **Name**
Ignoring the Human Loop
  #### **Description**
Letting AI make design decisions
  #### **Why**
AI optimizes for prompt, not for player experience
  #### **Instead**
Human designs, AI implements. Keep creative control.

---
  #### **Name**
Prompt Amnesia
  #### **Description**
Not saving successful prompts
  #### **Why**
Reinventing wheels, inconsistent results
  #### **Instead**
Build a prompt library. Document what works.