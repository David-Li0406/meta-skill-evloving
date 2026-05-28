# UX Design

## Patterns


---
  #### **Name**
Jobs-to-Be-Done User Research
  #### **Description**
Frame research around the job users are trying to accomplish, not feature requests
  #### **When**
Conducting user interviews or defining product requirements
  #### **Example**
    Bad question: "Would you use a feature to X?"
    Good question: "Walk me through the last time you tried to accomplish Y"
    
    Framework:
    1. Situation: When does this job arise?
    2. Motivation: Why are they trying to do it?
    3. Outcome: What does success look like?
    4. Obstacles: What prevents them from succeeding today?
    
    Focus on the job, not the solution. Users know their problems, not the answers.
    

---
  #### **Name**
Progressive Disclosure
  #### **Description**
Show only essential information upfront, reveal complexity as users need it
  #### **When**
Designing complex features, settings panels, or power-user tools
  #### **Example**
    Bad (all at once):
    [Form with 20 fields including advanced options]
    
    Good (progressive):
    Step 1: [3 essential fields] → Next
    Step 2: [5 common options] → Next
    Step 3: [Advanced options - collapsed by default]
    
    Or for settings:
    - Basic settings visible
    - "Advanced" accordion collapsed
    - "Show all" option for power users
    
    Serve 80% of users with simple defaults, give 20% access to complexity.
    

---
  #### **Name**
Zero-State Design
  #### **Description**
Design the first experience when nothing exists yet—critical for onboarding and retention
  #### **When**
User first signs up, creates a project, or opens an empty dashboard
  #### **Example**
    Bad zero state:
    [Empty table] "No items to display"
    
    Good zero state:
    [Illustration + clear message]
    "No projects yet"
    [Big CTA button] "Create your first project"
    [Optional: 2-minute video] "Watch how it works"
    
    Zero state should:
    - Explain what will be here
    - Show clear next action
    - Reduce anxiety about "did I do something wrong?"
    

---
  #### **Name**
Error Prevention Over Error Handling
  #### **Description**
Design systems that make errors impossible rather than handling them gracefully
  #### **When**
Designing forms, destructive actions, or complex workflows
  #### **Example**
    Prevention strategies:
    - Disable submit until form is valid (not just show error after)
    - Confirm before delete: "Type 'DELETE' to confirm"
    - Auto-save drafts (user never loses work)
    - Inline validation as user types (catch errors immediately)
    - Smart defaults (most users never change them)
    
    Best error is one that never happens.
    

---
  #### **Name**
Cognitive Load Reduction
  #### **Description**
Minimize mental effort required to understand and use the interface
  #### **When**
Designing any interface, especially for new or infrequent users
  #### **Example**
    Reduce cognitive load:
    - Chunking: Break info into 3-5 item groups
    - Familiarity: Use standard patterns (search in top right)
    - Clear labels: "Save draft" not "Persist state"
    - Visual hierarchy: Most important thing is most prominent
    - Defaults: Pre-select sensible options
    - Contextual help: Show guidance when needed, not always
    
    Test: Can a user accomplish their goal without reading documentation?
    

---
  #### **Name**
User Flow Mapping Before Wireframing
  #### **Description**
Map the complete user journey across screens before designing individual screens
  #### **When**
Starting any new feature or redesigning existing flows
  #### **Example**
    Flow mapping process:
    1. Define entry points (where users start)
    2. Map happy path (ideal flow, no errors)
    3. Add edge cases (what if this fails? empty states?)
    4. Add exit points (how do users leave this flow?)
    5. Identify friction points (where might they get stuck?)
    
    Only after mapping: design individual screens
    This ensures each screen serves the journey, not just looks good in isolation.
    

## Anti-Patterns


---
  #### **Name**
Designing for Edge Cases First
  #### **Description**
Optimizing for rare scenarios before solving the common case
  #### **Why**
Adds complexity that 95% of users never need. Clutters interface. Slows development.
  #### **Instead**
    Design process:
    1. Solve for 80% use case (simple, clean)
    2. Ship and validate with real users
    3. Add edge case handling only if users actually hit it
    
    Example:
    Don't add "advanced filters" on v1 if basic search serves most users.
    Add it later if user requests validate the need.
    

---
  #### **Name**
Feature Parity with Competitors
  #### **Description**
Adding features because competitors have them, not because users need them
  #### **Why**
Bloats product, dilutes focus, copies competitors' mistakes, ignores your unique advantages.
  #### **Instead**
    When stakeholder says "Competitor X has feature Y":
    1. Ask: "What job are users hiring that feature to do?"
    2. Research: "Do our users have that same job?"
    3. Validate: "Is there a simpler way to solve it?"
    
    Linear doesn't have Gantt charts (Jira does). They win by simplicity, not feature parity.
    

---
  #### **Name**
Skipping Wireframes, Jumping to High-Fidelity
  #### **Description**
Starting with polished UI before validating structure and flow
  #### **Why**
Wastes time polishing the wrong solution. Visual design bias prevents honest feedback.
  #### **Instead**
    Design fidelity ladder:
    1. Sketches (10 min) → validate concept
    2. Low-fi wireframes (30 min) → validate structure
    3. Clickable prototype (2 hours) → validate flow
    4. High-fidelity designs → polish validated solution
    
    Each step is cheaper to change than the next. Fail fast, fail cheap.
    

---
  #### **Name**
Asking Users What They Want
  #### **Description**
Taking user feature requests as requirements without understanding underlying needs
  #### **Why**
Users know their problems, not the solutions. Feature requests are often wrong solutions to real problems.
  #### **Instead**
    When user requests feature X:
    1. Ask: "What are you trying to accomplish?"
    2. Ask: "What's the problem with how you do it today?"
    3. Observe them doing the task (don't just ask)
    4. Design solution to the actual problem (may not be feature X)
    
    Classic: Users asked for faster horses. They needed cars.
    

---
  #### **Name**
Navigation-First Design
  #### **Description**
Designing the navigation structure before understanding user tasks and content
  #### **Why**
Navigation serves content and tasks. Designing it first creates wrong structure.
  #### **Instead**
    Content-first navigation:
    1. List all content/features
    2. Card sort with users (how do they group it?)
    3. Map user tasks (what do they need together?)
    4. Design navigation that supports common tasks
    
    Example: Users need billing + usage together (task-based), not in separate "Settings" and "Dashboard" sections.
    

---
  #### **Name**
Mobile-as-Afterthought
  #### **Description**
Designing desktop-first, then trying to cram everything onto mobile
  #### **Why**
Mobile constraints often reveal the core feature. Desktop bloat hides poor prioritization.
  #### **Instead**
    Mobile-first design:
    1. Start with mobile (forces prioritization)
    2. Expand to tablet (add context, not clutter)
    3. Desktop (take advantage of space for power features)
    
    Mobile forces you to answer: "What's actually essential here?"
    