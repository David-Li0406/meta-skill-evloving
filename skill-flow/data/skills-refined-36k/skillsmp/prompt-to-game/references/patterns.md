# Prompt-to-Game Development

## Patterns


---
  #### **Id**
component-by-component-prompting
  #### **Name**
Component-by-Component Prompting
  #### **Description**
Build games piece by piece, testing after each generation
  #### **When To Use**
Any game larger than a single-screen prototype
  #### **Structure**
    1. Generate minimal viable game (one mechanic)
    2. Test immediately in browser/engine
    3. Add one feature via new prompt
    4. Test again
    5. Refactor when code becomes messy
    6. Repeat until complete
    
  #### **Code Example**
    // Prompt sequence for platformer
    // Prompt 1: "Create a player that moves with WASD in Phaser 3"
    // Test - verify movement works
    
    // Prompt 2: "Add gravity and jumping with spacebar"
    // Test - verify physics
    
    // Prompt 3: "Add platforms the player can stand on"
    // Test - verify collision
    
    // Prompt 4: "Add a score counter in the top left"
    // Test - verify UI
    
    // Continue component by component...
    
  #### **Benefits**
    - Catch issues immediately
    - Maintain context coherence
    - Easier debugging
  #### **Pitfalls**
    - Slower than mega-prompts (but more reliable)

---
  #### **Id**
reference-existing-games
  #### **Name**
Reference Existing Games Pattern
  #### **Description**
Use well-known games as shorthand for mechanics
  #### **When To Use**
When describing complex mechanics
  #### **Structure**
    1. Identify game with similar mechanic
    2. Reference it explicitly in prompt
    3. Specify differences from reference
    4. Let AI fill in expected patterns
    
  #### **Code Example**
    // Effective references
    "Create a roguelike like Binding of Isaac but with..."
    "Make a bullet hell inspired by Vampire Survivors..."
    "Add a grappling hook similar to Hades' cast ability..."
    "Implement inventory like Stardew Valley's backpack..."
    
    // Bad: vague references
    "Make it like Mario" // Which Mario? Which mechanic?
    
    // Good: specific references
    "Add a double-jump like Hollow Knight with coyote time"
    
  #### **Benefits**
    - Leverages AI training on game discussions
    - Communicates complex mechanics concisely
    - Sets clear expectations
  #### **Pitfalls**
    - AI may not know obscure games
    - Verify AI understood the reference

---
  #### **Id**
framework-in-prompt
  #### **Name**
Specify Framework in Every Prompt
  #### **Description**
Always declare your framework and version
  #### **When To Use**
Every prompt for game code generation
  #### **Structure**
    1. Start prompt with framework name
    2. Include version number
    3. Reference specific APIs if known
    4. Maintain consistency across conversation
    
  #### **Code Example**
    // Good prompts
    "Using Phaser 3.90, create a player sprite that..."
    "In Godot 4.2 GDScript, implement a state machine..."
    "With Three.js r162, add a first-person camera..."
    "Using Kaboom.js v3000, make a bullet pattern..."
    
    // Bad prompts
    "Make the player move" // What framework?
    "Add physics" // Which physics system?
    
  #### **Benefits**
    - Correct API usage
    - Proper version-specific patterns
    - Fewer hallucinated methods
  #### **Pitfalls**
    - AI may use patterns from different version
    - Verify imports match your actual setup

---
  #### **Id**
seed-lock-and-document
  #### **Name**
Seed Lock and Document Pattern
  #### **Description**
Save everything when something works
  #### **When To Use**
After any successful generation
  #### **Structure**
    1. Immediately save working code to git
    2. Document the exact prompt used
    3. Note any manual fixes applied
    4. Tag working versions for rollback
    
  #### **Code Example**
    # prompt_log.md
    ## Working Player Movement
    **Prompt**: "Using Phaser 3.90, create WASD movement..."
    **Model**: Claude 3.5 Sonnet
    **Manual fixes**:
      - Changed `this.physics` to `this.scene.physics`
      - Added null check for cursors
    **Commit**: abc1234
    
    ## Working Jump Mechanic
    **Prompt**: "Add jumping with spacebar to the player..."
    ...
    
  #### **Benefits**
    - Can reproduce successful generations
    - Learn what prompting styles work
    - Rollback when new changes break things
  #### **Pitfalls**
    - Takes time but saves more time later

---
  #### **Id**
negative-constraints
  #### **Name**
Negative Constraints Pattern
  #### **Description**
Tell AI what NOT to do to avoid common issues
  #### **When To Use**
When AI keeps making unwanted choices
  #### **Structure**
    1. Identify common AI anti-patterns
    2. Explicitly forbid them in prompt
    3. Provide preferred alternative
    
  #### **Code Example**
    "Create a player controller. Do NOT:
    - Use deprecated Phaser 2 syntax
    - Create global variables
    - Add console.log statements
    - Use any external libraries not already imported
    
    DO:
    - Use ES6 class syntax
    - Use this.scene for scene references
    - Handle edge cases for input"
    
  #### **Benefits**
    - Prevents common AI mistakes
    - Reduces iteration cycles
    - Cleaner generated code
  #### **Pitfalls**
    - Don't overload with constraints
    - Keep negative list focused

---
  #### **Id**
refactor-threshold
  #### **Name**
Refactor at Threshold Pattern
  #### **Description**
Know when to stop prompting and restructure
  #### **When To Use**
When code becomes unwieldy
  #### **Structure**
    1. Set file size threshold (~500 lines)
    2. Set complexity threshold (nested conditionals > 3)
    3. When exceeded, pause features
    4. Prompt for refactoring specifically
    5. Resume feature development
    
  #### **Code Example**
    // Refactoring prompt
    "Refactor this game.js into separate modules:
    - player.js: Player class and movement
    - enemies.js: Enemy class and AI
    - world.js: World generation and tiles
    - ui.js: HUD and menus
    
    Use ES6 imports/exports.
    Maintain all existing functionality."
    
    // Then verify each module works
    
  #### **Benefits**
    - Maintains code quality
    - Easier debugging
    - Better AI context in future prompts
  #### **Pitfalls**
    - Refactoring can introduce bugs
    - Test thoroughly after restructure

---
  #### **Id**
three-prompt-workflow
  #### **Name**
Three-Prompt Workflow
  #### **Description**
Rapid prototyping in three stages
  #### **When To Use**
Game jams, quick prototypes, proof of concepts
  #### **Structure**
    1. Prompt 1: Core gameplay loop
    2. Prompt 2: One major feature addition
    3. Prompt 3: Polish and bug fixes
    
  #### **Code Example**
    // Prompt 1: Core loop
    "Create a top-down shooter in Phaser 3 where the
    player moves with WASD and shoots at enemies with
    mouse click. Enemies spawn from edges and move
    toward player."
    
    // Test and verify core works
    
    // Prompt 2: Major feature
    "Add a weapon upgrade system. Killing enemies drops
    XP orbs. At 10, 25, 50 XP, offer choice of 3 random
    upgrades (fire rate, damage, speed)."
    
    // Test upgrade system
    
    // Prompt 3: Polish
    "Add screen shake on enemy kill, particle effects
    for bullets, and a game over screen with restart
    button. Fix any bugs you notice."
    
  #### **Benefits**
    - Complete game in hours
    - Clear milestone structure
    - Iterative polish
  #### **Pitfalls**
    - Skips foundation work
    - May need more prompts for complex games

---
  #### **Id**
security-first-validation
  #### **Name**
Security-First Validation
  #### **Description**
Treat all AI code as untrusted
  #### **When To Use**
Before shipping any AI-generated game
  #### **Structure**
    1. Run linter immediately after generation
    2. Check for common vulnerabilities
    3. Validate all user inputs
    4. Never expose secrets in client code
    5. Use security scanning tools
    
  #### **Code Example**
    // Common AI security issues
    
    // BAD: AI might generate
    eval(userInput);  // Remote code execution
    const apiKey = "sk-..."; // Exposed secret
    document.innerHTML = userMessage; // XSS
    
    // GOOD: Validate everything
    if (!isValidInput(userInput)) return;
    const apiKey = process.env.API_KEY; // Server-side
    element.textContent = sanitize(userMessage); // Escaped
    
  #### **Benefits**
    - Prevents security incidents
    - Builds secure habits
    - Catches AI mistakes
  #### **Pitfalls**
    - Takes extra time
    - AI will repeat bad patterns if not caught

## Anti-Patterns


---
  #### **Id**
mega-prompt-everything
  #### **Name**
Mega-Prompt Everything
  #### **Description**
Asking for entire game in single prompt
  #### **Why Bad**
    Produces inconsistent, spaghetti code. Features conflict. Hard to debug because everything is intertwined. Context window limits cause forgotten features.
    
  #### **Example**
    BAD:
    "Create a complete RPG with:
    - Character creation with 6 classes
    - Turn-based combat with abilities
    - Inventory system with equipment
    - Quest log with 10 quests
    - Dialog trees with NPCs
    - Skill progression system
    - Save/load functionality
    - Multiplayer co-op"
    
  #### **Better Approach**
    Component-by-component prompting. Build each system separately, test, then integrate.
    

---
  #### **Id**
accepting-without-understanding
  #### **Name**
Accepting Code Without Understanding
  #### **Description**
Using AI code you don't understand
  #### **Why Bad**
    Cannot debug when it breaks. Cannot extend safely. May contain security vulnerabilities. Will fail in production when no one knows how it works.
    
  #### **Signs**
    - It works, I won't touch it
    - Cannot explain what code does
    - Afraid to modify any part
  #### **Better Approach**
    Read every line. Ask AI to explain unclear parts. Refactor to patterns you understand.
    

---
  #### **Id**
sunk-cost-prompting
  #### **Name**
Sunk-Cost Prompting Loop
  #### **Description**
Continuing to prompt because you've invested time
  #### **Why Bad**
    "I've spent 2 hours prompting, I can't stop now." This is the AI programming sunk-cost fallacy. Sometimes the answer is to reset and start fresh.
    
  #### **Signs**
    - Same error after 5+ attempts
    - AI keeps reverting previous fixes
    - Prompts getting longer and more desperate
  #### **Better Approach**
    STOP. Reset context. Start fresh with simpler approach. Or just code the 10 lines manually.
    

---
  #### **Id**
ignoring-hallucinated-apis
  #### **Name**
Ignoring Hallucinated APIs
  #### **Description**
Not checking if AI-referenced methods exist
  #### **Why Bad**
    5-21% of AI suggestions include hallucinated dependencies. AI trained on old documentation. Methods that don't exist, wrong signatures, deprecated patterns.
    
  #### **Example**
    // AI generates:
    this.physics.velocityFromAngle(angle, speed);
    // But this method doesn't exist in Phaser 3!
    
    // Should be:
    this.physics.velocityFromRotation(angle, speed, vec);
    
  #### **Better Approach**
    Verify every unfamiliar method in official docs. Use TypeScript for compile-time catching.
    

---
  #### **Id**
version-blindness
  #### **Name**
Version Blindness
  #### **Description**
Not specifying or checking framework versions
  #### **Why Bad**
    AI trained on Phaser 2 generates Phaser 2 code for your Phaser 3 project. Deprecated patterns, wrong APIs, subtle bugs from version differences.
    
  #### **Signs**
    - This worked in the tutorial
    - Deprecation warnings everywhere
    - Methods with slightly wrong parameters
  #### **Better Approach**
    Always specify version in prompts. Check changelogs. Paste current API examples in context.
    

---
  #### **Id**
no-testing-between-prompts
  #### **Name**
No Testing Between Prompts
  #### **Description**
Chaining prompts without running the code
  #### **Why Bad**
    Errors compound. Later prompts build on broken foundation. Debug session becomes impossible when you don't know which of 10 prompts broke things.
    
  #### **Signs**
    - Let me add a few more things first
    - Multiple features, no intermediate testing
    - It was working before I added X... or was it Y?
  #### **Better Approach**
    Test after EVERY prompt. Commit working versions. Never add feature on broken foundation.
    