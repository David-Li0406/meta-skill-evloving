# Development - Sharp Edges

## Security Vulnerabilities

### **Id**
security-vulnerabilities
### **Summary**
AI often suggests insecure code patterns
### **Severity**
critical
### **Tools Affected**
  - github-copilot
  - cursor
  - codeium
  - tabnine
### **Situation**
AI suggests code with security vulnerabilities
### **Why**
  AI training data includes insecure code:
  - SQL injection patterns
  - Hardcoded secrets
  - Insecure random number generation
  - Missing input validation
  - Unsafe deserialization
  
  AI doesn't understand security context.
  
### **Solution**
  1. Always review security-sensitive code
  2. Run security scanners (SAST)
  3. Never trust AI with auth/crypto
  4. Use security-focused prompts
  5. Code review for security explicitly
  
  ```python
  # Bad: AI might suggest
  query = f"SELECT * FROM users WHERE id = {user_id}"
  
  # Good: Always parameterize
  query = "SELECT * FROM users WHERE id = %s"
  cursor.execute(query, (user_id,))
  ```
  
### **Symptoms**
  - Security scanner finds vulnerabilities
  - Code review catches injection risks
  - Secrets appear in suggestions

## Outdated Patterns

### **Id**
outdated-patterns
### **Summary**
AI suggests deprecated or outdated patterns
### **Severity**
medium
### **Tools Affected**
  - github-copilot
  - cursor
  - codeium
### **Situation**
AI suggests old library versions or deprecated APIs
### **Why**
  Training data includes old code:
  - Deprecated React patterns (class components)
  - Old library versions
  - Superseded APIs
  - Legacy approaches
  
  AI doesn't know "best practice" changed.
  
### **Solution**
  1. Know current best practices
  2. Question patterns that seem old
  3. Check library documentation
  4. Update prompts with version info
  5. Configure AI for modern patterns
  
### **Symptoms**
  - Using class components in React
  - Old callback patterns vs async/await
  - Deprecated warnings at runtime

## Hallucinated Apis

### **Id**
hallucinated-apis
### **Summary**
AI invents APIs that don't exist
### **Severity**
high
### **Tools Affected**
  - github-copilot
  - cursor
  - claude-code
### **Situation**
AI uses function/method that doesn't exist
### **Why**
  AI confuses or invents:
  - Similar library APIs mixed up
  - Methods that "should" exist
  - Plausible but fake functions
  - Wrong library versions
  
  Code looks right but won't compile.
  
### **Solution**
  1. Always test AI code
  2. Verify imports work
  3. Check documentation
  4. Don't trust unfamiliar APIs
  5. Type checking helps catch this
  
### **Symptoms**
  - Module not found errors
  - AttributeError: no such method
  - TypeScript errors on AI code

## Context Loss

### **Id**
context-loss
### **Summary**
AI loses context in large codebases
### **Severity**
medium
### **Tools Affected**
  - github-copilot
  - codeium
### **Situation**
AI suggestions ignore project patterns
### **Why**
  Limited context window means:
  - Can't see whole codebase
  - Misses project conventions
  - Ignores related files
  - Suggests inconsistent patterns
  
  More context-aware tools help.
  
### **Solution**
  1. Use Cursor/Claude Code for large projects
  2. Provide context in prompts
  3. Reference existing patterns
  4. Use consistent file naming
  5. Keep related code near cursor
  
### **Symptoms**
  - Suggestions don't match project style
  - Different patterns for same thing
  - Ignores existing utilities

## Over Engineering

### **Id**
over-engineering
### **Summary**
AI over-complicates simple tasks
### **Severity**
medium
### **Tools Affected**
  - github-copilot
  - cursor
  - claude-code
### **Situation**
AI writes 50 lines when 5 would do
### **Why**
  AI tends to:
  - Add unnecessary abstractions
  - Include unused error handling
  - Over-generalize solutions
  - Add features not requested
  
  More code = more bugs, more maintenance.
  
### **Solution**
  1. Ask for simple solutions
  2. Specify constraints in prompts
  3. Delete unnecessary code
  4. Request minimal implementation
  5. Review for YAGNI violations
  
### **Symptoms**
  - Way more code than needed
  - Abstractions for single use cases
  - Features nobody asked for

## Copy Paste Licensing

### **Id**
copy-paste-licensing
### **Summary**
AI may reproduce copyrighted code
### **Severity**
high
### **Tools Affected**
  - github-copilot
  - cursor
  - codeium
### **Situation**
AI generates code from copyleft or proprietary sources
### **Why**
  Training data includes:
  - GPL licensed code
  - Stack Overflow (CC-BY-SA)
  - Proprietary code (leaked)
  - Various license restrictions
  
  Using could violate licenses.
  
### **Solution**
  1. Enable Copilot's duplication filter
  2. Review long blocks of generated code
  3. Run license scanning
  4. Be cautious with recognizable patterns
  5. Understand your company's policy
  
### **Symptoms**
  - Recognizable code from elsewhere
  - License scanner flags
  - Exact match to Stack Overflow

## Skill Atrophy

### **Id**
skill-atrophy
### **Summary**
Relying on AI can degrade programming skills
### **Severity**
medium
### **Tools Affected**
  - all
### **Situation**
Developer forgets fundamentals, can't code without AI
### **Why**
  Over-reliance leads to:
  - Forgetting syntax
  - Not understanding generated code
  - Unable to debug without AI
  - Losing problem-solving skills
  
  AI should augment, not replace.
  
### **Solution**
  1. Understand code before using it
  2. Code without AI regularly
  3. Explain AI code to yourself
  4. Don't skip learning fundamentals
  5. Use AI to accelerate, not replace thinking
  
### **Symptoms**
  - Can't code without Copilot
  - Don't understand own codebase
  - Can't solve problems AI can't

## Junior Developer Risk

### **Id**
junior-developer-risk
### **Summary**
Junior devs accept bad suggestions more
### **Severity**
medium
### **Tools Affected**
  - all
### **Situation**
Less experienced developers trust AI too much
### **Why**
  Junior developers may:
  - Not recognize bad patterns
  - Can't evaluate suggestions
  - Accept insecure code
  - Miss better alternatives
  
  AI amplifies existing skill gaps.
  
### **Solution**
  1. Senior review of AI-heavy code
  2. Pair programming with AI
  3. Teach how to evaluate suggestions
  4. Emphasis on fundamentals first
  5. Create team guidelines for AI use
  
### **Symptoms**
  - PRs with copied AI patterns
  - Security issues in junior code
  - Inconsistent code quality

## Cost Surprise

### **Id**
cost-surprise
### **Summary**
AI API costs can explode
### **Severity**
high
### **Tools Affected**
  - claude-code
  - aider
### **Situation**
Using API-based tools without cost awareness
### **Why**
  Pay-per-token adds up:
  - Large codebases = large context
  - Multiple iterations
  - Multi-file changes
  - Long conversations
  
  Easy to spend $100+ per day.
  
### **Solution**
  1. Set API spending limits
  2. Monitor usage closely
  3. Use smaller models when possible
  4. Be efficient with prompts
  5. Consider subscription tools instead
  
### **Symptoms**
  - Unexpected API bill
  - Hitting spending limits
  - Cost per feature too high

## Privacy Exposure

### **Id**
privacy-exposure
### **Summary**
Code sent to AI providers
### **Severity**
high
### **Tools Affected**
  - github-copilot
  - cursor
  - codeium
### **Situation**
Proprietary code sent to external AI
### **Why**
  Default settings often:
  - Send code for completion
  - Send code for training
  - Store conversation history
  - Share with third parties
  
  May violate security policies or regulations.
  
### **Solution**
  1. Review privacy settings
  2. Opt out of training data
  3. Use self-hosted options
  4. Enterprise tiers for more control
  5. Policy: no secrets in prompts
  
### **Symptoms**
  - Security audit concerns
  - Compliance questions
  - Code in AI training sets

## Vendor Lock In

### **Id**
vendor-lock-in
### **Summary**
Tooling lock-in to specific AI provider
### **Severity**
low
### **Tools Affected**
  - cursor
  - github-copilot
### **Situation**
Team becomes dependent on one AI tool
### **Why**
  Different tools, different experiences:
  - Cursor workflows don't transfer
  - Copilot muscle memory
  - Extension dependencies
  - Pricing changes affect budget
  
  Switching is painful.
  
### **Solution**
  1. Keep skills tool-agnostic
  2. Know alternatives exist
  3. Don't build processes on one tool
  4. Evaluate periodically
  5. Standard IDE + extensions as fallback
  
### **Symptoms**
  - Panic when tool is down
  - Can't switch easily
  - Price increases hurt