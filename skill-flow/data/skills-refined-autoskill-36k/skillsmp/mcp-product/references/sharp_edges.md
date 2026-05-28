# Mcp Product - Sharp Edges

## First Call Friction

### **Id**
first-call-friction
### **Summary**
First tool call asks for things users don't have yet
### **Severity**
critical
### **Situation**
  You design a tool that requires project_id, user_id, or session_id
  as a required parameter, but users calling for the first time
  don't have any of these yet.
  
### **Why**
  Vibe coders are exploring. They don't have IDs because they haven't
  started yet. If your tool immediately blocks them with "missing required
  parameter", they'll assume Spawner is broken and leave.
  
  This is the #1 reason tools fail to get adoption.
  
### **Solution**
  Make IDs optional with smart defaults:
  - No project_id? Create an anonymous session
  - No user_id? Generate a temporary one
  - Let them get value FIRST, persist LATER
  
  ```typescript
  // Bad
  inputSchema: {
    required: ["project_id", "code"]
  }
  
  // Good
  inputSchema: {
    required: ["code"],
    properties: {
      project_id: {
        description: "Optional - we'll create one if you don't have one yet"
      }
    }
  }
  ```
  
### **Symptoms**
  - What's my project ID?
  - How do I start?
  - This tool isn't working
  - High bounce rate on first tool call
### **Detection Pattern**
required.*project_id|required.*user_id|required.*session

## Jargon In Errors

### **Id**
jargon-in-errors
### **Summary**
Error messages use technical terms vibe coders don't know
### **Severity**
critical
### **Situation**
  Tool returns errors like "Invalid JSON-RPC request", "Schema validation
  failed", "Hydration mismatch", or "RLS policy violation"
  
### **Why**
  Vibe coders don't know what JSON-RPC is. They don't know what a schema is.
  When they see these errors, they feel stupid and blame themselves - or
  worse, they think AI is broken and give up on building entirely.
  
  Your error killed someone's dream of building their first app.
  
### **Solution**
  Translate every error to plain language with actionable next steps:
  
  ```typescript
  // Bad
  throw new Error("Zod validation failed: expected string, got undefined")
  
  // Good
  return {
    error: "I need to know what code you want me to check",
    what_to_do: "Try again with the code you want validated",
    example: 'spawner_validate(code="your code here", file_path="app.tsx")'
  }
  ```
  
### **Symptoms**
  - Users copy-paste errors to Claude asking what they mean
  - I don't understand what went wrong
  - Users disappear after hitting errors
### **Detection Pattern**
throw new Error.*Zod|validation failed|schema.*error

## No Next Steps

### **Id**
no-next-steps
### **Summary**
Tool returns results without telling users what to do next
### **Severity**
high
### **Situation**
  Tool successfully completes but returns minimal output like
  { "success": true } or just raw data without context
  
### **Why**
  Vibe coders don't know what comes next. They got a result but have no
  idea what to do with it. Expert developers might figure it out, but
  you've created a dead end for 70% of your users.
  
  Every tool response is a teaching moment. Don't waste it.
  
### **Solution**
  Always include:
  1. What just happened (confirmation)
  2. What it means (context)
  3. What to do next (action)
  
  ```typescript
  // Bad
  return { created: true, id: "abc123" }
  
  // Good
  return {
    created: true,
    id: "abc123",
    what_happened: "I created your SaaS project with Next.js and Supabase",
    what_this_means: "You now have a starter project with auth, database, and payments ready",
    next_steps: [
      "Open your terminal and run: cd my-saas && npm install",
      "Create a .env.local file with your Supabase keys",
      "Run npm run dev to see your app at localhost:3000"
    ]
  }
  ```
  
### **Symptoms**
  - What do I do now?
  - It said success but nothing happened
  - Users immediately ask Claude for help after tool returns

## Tool Name Confusion

### **Id**
tool-name-confusion
### **Summary**
Tool names don't match what users are trying to do
### **Severity**
high
### **Situation**
  Tools named after technical operations (create, read, update, delete,
  fetch, query) rather than user goals
  
### **Why**
  Users think "I'm stuck" not "I need to call the unstick function".
  Users think "I want to remember this" not "I need to POST to the
  decisions endpoint".
  
  CRUD naming is database thinking. User-goal naming is product thinking.
  
### **Solution**
  Name tools by the job users hire them to do:
  
  ```
  # Bad (technical operations)
  spawner_create_project
  spawner_get_skills
  spawner_update_memory
  spawner_fetch_edges
  
  # Good (user goals)
  spawner_plan        → "I want to plan my project"
  spawner_skills      → "I need skills for this"
  spawner_remember    → "Remember this decision"
  spawner_sharp_edge  → "What gotchas should I know?"
  spawner_unstick     → "I'm stuck, help me"
  ```
  
### **Symptoms**
  - Users don't know which tool to use
  - Claude picks wrong tools frequently
  - "Is there a tool for X?" when X already exists

## Parameter Overload

### **Id**
parameter-overload
### **Summary**
Tool schema exposes too many parameters
### **Severity**
high
### **Situation**
  Tool definition has 10+ parameters, most optional, making the
  schema overwhelming to read and hard for Claude to fill correctly
  
### **Why**
  More parameters = more cognitive load = more chances for errors.
  Claude has to decide what to fill. Users have to understand options.
  
  Stripe's genius is making complex things feel simple. 20 parameters
  is the opposite of that.
  
### **Solution**
  - Required params: 1-3 max
  - Optional params: Hide in "advanced" or omit from schema entirely
  - Smart defaults: Pick the right answer for 80% of cases
  
  ```typescript
  // Bad: 12 parameters
  inputSchema: {
    properties: {
      code, file_path, check_types, severity_filter, auto_fix,
      strict_mode, ignore_patterns, include_patterns, max_issues,
      output_format, context_lines, enable_suggestions
    }
  }
  
  // Good: 2 required, 1 optional
  inputSchema: {
    required: ["code", "file_path"],
    properties: {
      code: { description: "The code to check" },
      file_path: { description: "Where this code lives" },
      check_types: { description: "Optional: focus on specific issues" }
    }
  }
  ```
  
### **Symptoms**
  - Claude guesses wrong parameter values
  - Users confused about what to fill in
  - Tool calls fail due to missing/wrong params

## Inconsistent Responses

### **Id**
inconsistent-responses
### **Summary**
Different tools return data in different formats
### **Severity**
medium
### **Situation**
  One tool returns { result: ... }, another returns { data: ... },
  another returns { output: ... }. Status might be "success", "ok",
  true, or "completed" depending on the tool.
  
### **Why**
  Inconsistency forces users to learn each tool separately. Claude
  has to parse different response shapes. Integrations become brittle.
  
  Stripe's API consistency is legendary - every endpoint follows
  the same patterns.
  
### **Solution**
  Define a standard response envelope and stick to it:
  
  ```typescript
  interface ToolResponse<T> {
    success: boolean
    data?: T
    error?: {
      message: string      // Human-readable
      code: string         // Machine-readable
      suggestion?: string  // What to try
    }
    meta?: {
      took_ms: number
      next_steps?: string[]
    }
  }
  ```
  
### **Symptoms**
  - Wrapper code to normalize responses
  - How do I check if this worked?
  - Different error handling per tool

## Missing Progress Feedback

### **Id**
missing-progress-feedback
### **Summary**
Long operations give no indication of progress
### **Severity**
medium
### **Situation**
  Tool takes 5+ seconds to complete but returns nothing until done.
  User (and Claude) have no idea if it's working or hung.
  
### **Why**
  After 100ms without feedback, humans assume something is broken.
  Vibe coders will retry, cancel, or give up. Even "Working..." is
  better than silence.
  
### **Solution**
  For operations over 2 seconds:
  - Return immediately with a status
  - Use streaming if MCP transport supports it
  - Or return progress indicators Claude can relay
  
  ```typescript
  // If streaming isn't available, at least return fast with status
  return {
    status: "processing",
    message: "Analyzing your codebase... this usually takes 10-15 seconds",
    check_back: "I'll have results ready shortly"
  }
  ```
  
### **Symptoms**
  - Is it working?
  - Users cancel and retry
  - Duplicate operations

## No Dry Run

### **Id**
no-dry-run
### **Summary**
Destructive operations can't be previewed
### **Severity**
medium
### **Situation**
  Tool modifies files, database, or state with no way to see
  what would happen before committing
  
### **Why**
  Vibe coders are experimenting. They're not sure what they want.
  If every action is permanent, they'll be afraid to try things.
  
  Safe exploration = more engagement = more learning = more value.
  
### **Solution**
  Add preview/dry-run capability for state-changing operations:
  
  ```typescript
  // Allow preview before commit
  spawner_plan(action="create", project_name="my-app", dry_run=true)
  
  // Returns what WOULD happen without doing it
  {
    "dry_run": true,
    "would_create": {
      "files": ["package.json", "src/app.tsx", ...],
      "directories": ["src", "public", ...],
    },
    "confirm": "Run again with dry_run=false to create these files"
  }
  ```
  
### **Symptoms**
  - Wait, what did that just do?
  - Users afraid to try commands
  - Requests to undo operations

## Version Specific Gotchas

### **Id**
version-specific-gotchas
### **Summary**
Tool behavior depends on versions but doesn't surface this
### **Severity**
low
### **Situation**
  Tool gives advice that's correct for Next.js 14 but wrong for
  Next.js 15, and there's no indication which version applies
  
### **Why**
  Vibe coders don't track versions. They copy-paste from tutorials
  that might be outdated. Giving them version-specific advice without
  version context causes mysterious failures.
  
### **Solution**
  - Detect versions when possible (from package.json)
  - State version assumptions in responses
  - Flag when advice is version-sensitive
  
  ```typescript
  {
    "recommendation": "Use the new 'use cache' directive for caching",
    "version_note": "This requires Next.js 15+. I see you're on 14.x, so use the older revalidate pattern instead.",
    "alternative": "export const revalidate = 3600"
  }
  ```
  
### **Symptoms**
  - \"This doesn't work\" (works on different version)
  - Outdated advice
  - Version-mismatch errors

## Assuming Context

### **Id**
assuming-context
### **Summary**
Tool assumes user has context they don't have
### **Severity**
medium
### **Situation**
  Tool response references previous decisions, files, or state
  without explaining what that context is
  
### **Why**
  Each conversation might be fresh. Vibe coders forget what they
  decided 3 sessions ago. Assuming context breaks continuity.
  
### **Solution**
  - Briefly recap relevant context in responses
  - Don't assume memory persists between sessions
  - Offer to re-explain if context seems stale
  
  ```typescript
  {
    "recommendation": "Based on your earlier decision to use Stripe...",
    "context_recap": "You chose Stripe for payments because you need subscription billing",
    "still_applies": "If this has changed, let me know and we can reconsider"
  }
  ```
  
### **Symptoms**
  - What decision?
  - I don't remember choosing that
  - Confusion across sessions