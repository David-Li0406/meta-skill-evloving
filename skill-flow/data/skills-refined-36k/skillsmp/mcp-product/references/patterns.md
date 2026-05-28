# MCP Product Design

## Patterns


---
  #### **Name**
Magic First Moment
  #### **Description**
    Users should get value in under 60 seconds. The first tool call
    should produce something useful, not ask for configuration.
    
  #### **Example**
    # Good: spawner_plan with just an idea
    spawner_plan(idea="I want to build a marketplace for art")
    # Returns: Questions, recommendations, next steps - immediate value
    
    # Bad: Requiring project_id before anything works
    spawner_context(project_id="???") # User has no ID yet!
    
  #### **When**
Designing any new MCP tool or improving existing ones

---
  #### **Name**
Progressive Disclosure
  #### **Description**
    Simple by default, powerful when needed. Don't expose all options
    upfront - let users discover advanced features as they grow.
    
  #### **Example**
    # Level 1: Just works
    spawner_validate(code="...", file_path="app.tsx")
    
    # Level 2: When they need more
    spawner_validate(code="...", file_path="app.tsx", check_types=["security"])
    
    # Level 3: Expert mode
    spawner_validate(code="...", file_path="app.tsx", check_types=["security"], strict=true)
    
  #### **When**
Tool has many possible options or configurations

---
  #### **Name**
Explain As You Go
  #### **Description**
    Don't just return results - explain what happened and why.
    Vibe coders learn through usage, so teach while you work.
    
  #### **Example**
    # Bad output:
    { "status": "created", "project_id": "abc123" }
    
    # Good output:
    {
      "status": "created",
      "project_id": "abc123",
      "what_happened": "Created your SaaS project with Next.js, Supabase, and Stripe",
      "next_steps": [
        "Run 'npm install' to install dependencies",
        "Copy .env.example to .env.local and add your keys",
        "Run 'npm run dev' to start building"
      ],
      "why_this_stack": "SaaS apps need auth (Supabase), payments (Stripe), and fast iteration (Next.js)"
    }
    
  #### **When**
Any tool that produces results users need to act on

---
  #### **Name**
Sensible Defaults
  #### **Description**
    Pick the right default for 80% of users. Don't make them choose
    when there's an obvious right answer.
    
  #### **Example**
    # Bad: Requiring action parameter
    spawner_plan(action="discover", idea="...")
    
    # Good: Default to discover since that's where everyone starts
    spawner_plan(idea="...")  # action defaults to "discover"
    
  #### **When**
Tool has modes or actions where one is clearly most common

---
  #### **Name**
Error Messages Are UX
  #### **Description**
    Errors should tell users what to do, not what failed.
    Translate technical problems into actionable guidance.
    
  #### **Example**
    # Bad:
    "Error: ENOENT: no such file or directory"
    
    # Good:
    "I couldn't find the file 'src/app.tsx'.
    
     This might mean:
     - The file hasn't been created yet (try creating it first)
     - You're in the wrong directory (check your current path)
     - There's a typo in the filename
    
     Would you like me to help create this file?"
    
  #### **When**
Any error handling in tools

---
  #### **Name**
Confirm State Changes
  #### **Description**
    When tools modify something, explicitly report what changed
    so users can mentally model the new state.
    
  #### **Example**
    # After spawner_remember saves a decision:
    {
      "saved": true,
      "what_i_remembered": "You decided to use Stripe for payments because...",
      "project_state": {
        "decisions_count": 5,
        "last_updated": "just now"
      }
    }
    
  #### **When**
Tools that save, update, or modify state

## Anti-Patterns


---
  #### **Name**
ID Before Value
  #### **Description**
Requiring IDs or configuration before users get any value
  #### **Why**
    Vibe coders don't have project IDs yet. They're exploring.
    If the first thing your tool asks for is an ID they don't have,
    they'll leave and never come back.
    
  #### **Instead**
    Make IDs optional. Generate them if needed. Let users get value
    first, then persist if they want to continue.
    

---
  #### **Name**
Jargon Wall
  #### **Description**
Using technical terms without explanation
  #### **Why**
    "RLS policies", "hydration errors", "server components" mean
    nothing to someone who started vibe coding last week. You'll
    lose them immediately.
    
  #### **Instead**
    Use plain language first, technical terms in parentheses if needed.
    "Row-level security" → "Rules that control who can see what data"
    

---
  #### **Name**
Silent Success
  #### **Description**
Returning minimal confirmation without context
  #### **Why**
    { "ok": true } tells users nothing. Did it work? What happened?
    What should they do next? They're left guessing.
    
  #### **Instead**
    Confirm what happened, show the result, suggest next steps.
    Turn every success into a learning moment.
    

---
  #### **Name**
All Options Upfront
  #### **Description**
Exposing every parameter in the tool definition
  #### **Why**
    20 parameters in the schema is overwhelming. Users don't know
    what matters. Claude doesn't know what to fill in. Everyone loses.
    
  #### **Instead**
    Minimal required params, smart defaults for everything else.
    Advanced options can be documented but not prominent.
    

---
  #### **Name**
CRUD Naming
  #### **Description**
Naming tools like database operations (create, read, update, delete)
  #### **Why**
    "spawner_create_project" is database thinking, not user thinking.
    Users don't think in CRUD - they think in goals and workflows.
    
  #### **Instead**
    Name tools by what users are trying to accomplish:
    spawner_plan, spawner_unstick, spawner_remember
    

---
  #### **Name**
Error Codes Without Context
  #### **Description**
Returning error codes or stack traces without human explanation
  #### **Why**
    "-32602: Invalid params" helps no one. Vibe coders don't know
    what params are. Developers need to know WHICH param and WHY.
    
  #### **Instead**
    Always include: what went wrong, why it might have happened,
    what to try next.
    