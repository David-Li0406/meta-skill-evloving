# Prompt To Game - Sharp Edges

## AI Hallucinated APIs and Methods

### **Id**
hallucinated-apis
### **Severity**
critical
### **Description**
  5.2-21.7% of AI suggestions include hallucinated dependencies. Methods that don't exist, wrong signatures, made-up libraries. AI is confident but wrong.
  
### **Detection Pattern**
import|require|from.*(?!react|phaser|three|kaboom|godot)
### **Symptoms**
  - "X is not a function" errors
  - "Cannot find module" errors
  - Method exists but signature is wrong
### **Solution**
  1. Verify every unfamiliar method in official docs
  2. Use TypeScript for compile-time catching
  3. Test imports immediately after generation
  4. Keep official docs open while prompting
  5. Ask AI: "Are you sure this method exists in [framework] [version]?"
  
### **Technical Detail**
  Claude is better than GPT at avoiding hallucinations but still does it. Always verify.
  

## 45% of AI Code Has Security Vulnerabilities

### **Id**
security-vulnerabilities-45-percent
### **Severity**
critical
### **Description**
  Veracode 2025: 45% of AI-generated code contains security issues. Java: 72% security failure rate. 86% fail XSS protection. 88% vulnerable to log injection. AI doesn't think about security.
  
### **Detection Pattern**
eval|innerHTML|dangerouslySetInnerHTML|document\.write
### **Symptoms**
  - XSS vulnerabilities in user-facing code
  - SQL/command injection in backend
  - Exposed API keys in client code
  - Insecure randomness for security features
### **Solution**
  1. Treat ALL AI code as untrusted
  2. Run SAST tools (ESLint security rules, Semgrep)
  3. Never use eval() or innerHTML with user input
  4. Keep secrets server-side only
  5. Add security review step before shipping
  
### **References**
  - https://www.veracode.com/blog/genai-code-security-report/

## AI Generates Code for Wrong Framework Version

### **Id**
version-mismatch-disaster
### **Severity**
high
### **Description**
  AI trained on old docs. Phaser 2 vs Phaser 3, Three.js r100 vs r162. Subtle bugs from deprecated methods, wrong parameter orders, removed features.
  
### **Detection Pattern**
phaser|three|godot|kaboom|unity
### **Symptoms**
  - Deprecation warnings everywhere
  - This worked in the tutorial but not in my version
  - Methods with slightly wrong parameters
  - Missing required arguments
### **Solution**
  1. ALWAYS specify version in prompts: "Using Phaser 3.90..."
  2. Paste current API examples in context
  3. Check changelogs for deprecated methods
  4. Verify imports match your package.json
  5. Test with latest version before shipping
  
### **Code Example**
  // Phaser 2 (wrong for Phaser 3)
  game.add.sprite(100, 100, 'player');
  
  // Phaser 3 (correct)
  this.add.sprite(100, 100, 'player');
  

## AI Forgets Earlier Code in Long Sessions

### **Id**
context-window-forgetting
### **Severity**
high
### **Description**
  Context windows have limits. Large games exceed them. AI "forgets" earlier functions, creates duplicates, contradicts previous implementations.
  
### **Detection Pattern**
context|window|token|memory
### **Symptoms**
  - Duplicate function definitions
  - Contradictory implementations
  - References to code that doesn't exist
  - "I'll create this function" when it already exists
### **Solution**
  1. Keep files under 500 lines
  2. Split early and often
  3. Start new conversations for new features
  4. Paste relevant code snippets in new contexts
  5. Use tools with larger context (Claude Code)
  
### **Technical Detail**
  Magic.dev claims 100M token context, but most tools are 128k-200k. Summarize and split for safety.
  

## Sunk-Cost Prompting Fallacy Loop

### **Id**
sunk-cost-fallacy-loop
### **Severity**
high
### **Description**
  "I've spent 2 hours prompting, I can't stop now." Continuing to prompt when you should reset or code manually. Each failed attempt adds broken context.
  
### **Detection Pattern**
try.*again|not.*working|still.*broken
### **Symptoms**
  - Same error after 3+ attempts
  - Prompts getting longer and more desperate
  - AI reverting previous fixes
  - Increasingly complex workarounds
### **Solution**
  1. Set attempt limit: 3 tries max for same issue
  2. After limit: reset context, start fresh
  3. Consider: "Can I code this in 5 minutes manually?"
  4. Sometimes the answer is to just write the code
  5. Document what doesn't work to avoid repeating
  
### **References**
  - https://dev.to/samuelfaure/the-ai-programming-sunk-cost-fallacy-loop-and-how-to-break-it-13d6

## "Works on AI's Machine" - Missing Local Context

### **Id**
works-on-ai-machine
### **Severity**
high
### **Description**
  AI doesn't have access to your file structure, installed dependencies, environment variables, or current state. Code works in AI's imagination but fails locally.
  
### **Detection Pattern**
file.*path|require|import|env
### **Symptoms**
  - "File not found" errors
  - "Module not installed" errors
  - Works in AI preview, breaks locally
  - Incorrect relative paths
### **Solution**
  1. Share your package.json in context
  2. Provide explicit file paths
  3. List existing files when asking about structure
  4. Test in clean environment (Docker)
  5. Verify imports against actual node_modules
  

## Same Prompt Produces Different Games

### **Id**
consistency-between-runs
### **Severity**
medium
### **Description**
  Running identical prompt 10 times produces 10 different games. Non-deterministic outputs. Can't reproduce exact behavior. Hard to debug systematically.
  
### **Detection Pattern**
random|generate|create
### **Symptoms**
  - Yesterday's prompt doesn't work today
  - Can't reproduce successful generation
  - Inconsistent code style across sessions
### **Solution**
  1. Save working code IMMEDIATELY
  2. Document exact prompts used
  3. Git commit after every working state
  4. Don't rely on regeneration
  5. Consider temperature=0 for more consistency
  
### **References**
  - https://www.tabulamag.com/p/i-asked-claude-code-to-write-the

## AI Generates Spaghetti Code

### **Id**
ai-spaghetti-code
### **Severity**
medium
### **Description**
  AI adds features wherever convenient. Tightly coupled components. Redundant logic. Single-file chaos. Technical debt accumulates faster than with human-written code.
  
### **Detection Pattern**
add.*feature|implement|create
### **Symptoms**
  - File exceeds 500 lines
  - Functions exceed 100 lines
  - Nested callbacks 4+ levels deep
  - Duplicate code across functions
### **Solution**
  1. Set refactoring thresholds (500 lines, 3 deep nesting)
  2. Prompt for refactoring explicitly
  3. Apply Single Responsibility Principle
  4. Split files by concern
  5. Refactor BEFORE adding new features when threshold hit
  
### **Code Example**
  // Refactoring prompt
  "Refactor this into separate modules:
  - player.js: Player class
  - enemies.js: Enemy class
  - world.js: World generation
  Use ES6 imports. Maintain all functionality."
  

## AI's False Confidence in Generated Code

### **Id**
false-confidence-syndrome
### **Severity**
medium
### **Description**
  AI presents code with extreme confidence even when wrong. "Here's the working implementation" for code that doesn't run. No uncertainty markers for unreliable sections.
  
### **Detection Pattern**
here.*is|working|complete|ready
### **Symptoms**
  - AI says "this will work" but it doesn't
  - No caveats or warnings
  - Confident explanations of buggy code
### **Solution**
  1. Never trust "working" claim without testing
  2. Test EVERYTHING before accepting
  3. Ask "What could go wrong with this code?"
  4. Look for edge cases AI might miss
  5. Maintain healthy skepticism
  

## Browser-Only APIs in Node.js Code (and Vice Versa)

### **Id**
browser-only-vs-node
### **Severity**
medium
### **Description**
  AI mixes browser and Node.js APIs. Uses `window` in Node. Uses `fs` in browser code. Doesn't consider runtime environment.
  
### **Detection Pattern**
window|document|fs\.|process\.|require.*fs
### **Symptoms**
  - "window is not defined" in Node
  - "require is not defined" in browser
  - "document is not defined" in tests
### **Solution**
  1. Specify runtime in prompt: "for browser" or "for Node.js"
  2. Check generated imports
  3. Use environment-aware patterns
  4. Test in target runtime immediately
  
### **Code Example**
  // Browser-only
  const data = localStorage.getItem('key');
  
  // Node.js-only
  const data = fs.readFileSync('file.json');
  
  // Universal (with check)
  const isBrowser = typeof window !== 'undefined';
  