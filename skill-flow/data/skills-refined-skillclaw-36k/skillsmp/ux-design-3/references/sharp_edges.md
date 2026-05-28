# Ux Design - Sharp Edges

## Assumption Trap

### **Id**
assumption-trap
### **Summary**
Building features based on assumptions instead of research
### **Severity**
critical
### **Situation**
  "I know what users want", "Our competitor does it this way",
  "The stakeholder said users need this", "It's obvious what they need"
  
### **Why**
  You'll build the wrong thing confidently. Users don't know what they want until
  they use it. Competitors may also be wrong. Stakeholders have biases.
  "Obvious" is relative to your knowledge, not theirs.
  
### **Solution**
  # Validation methods:
  1. User interviews (5-8 minimum)
     Ask about behavior, not preferences
     "Tell me about the last time you..."
     NOT: "Would you use feature X?"
  
  2. Observation
     Watch actual usage
     Look for workarounds
     Note moments of confusion
  
  3. Prototype testing
     Clickable mockup before code
     5 users finds 80% of issues
     Fail fast, fail cheap
  
  4. Analytics review
     Where do users actually go?
     Where do they drop off?
  
  # Research before every major feature
  # "We don't have time" = We have time to build the wrong thing
  
### **Symptoms**
  - Features nobody uses
  - Redesigns needed soon after launch
  - Users are using it wrong
  - High churn despite features
### **Detection Pattern**


## Happy Path Only

### **Id**
happy-path-only
### **Summary**
Only designing for ideal scenarios, ignoring edge cases
### **Severity**
critical
### **Situation**
  Designing the perfect flow: User signs up → Completes profile → Uses product → Success!
  Ignoring all the ways reality differs from this ideal.
  
### **Why**
  Real users live in the edge cases. Special characters in names, wrong emails,
  session expiration, network failures, missing info, accessibility needs,
  slow connections, different languages.
  
### **Solution**
  # Edge cases to design for:
  - Empty states: No data yet
  - Error states: Something went wrong
  - Loading states: Data in transit
  - Partial states: Incomplete data
  - Offline states: No connection
  - Timeout states: Too slow
  - Permission states: Access denied
  - First-time states: New user
  - Expert states: Power user
  
  # For each flow, ask:
  - What if they can't continue?
  - What if they want to go back?
  - What if they need help?
  - What if something breaks?
  - What if they have nothing yet?
  
### **Symptoms**
  - Users stuck in broken states
  - Blank screens with no guidance
  - Error messages that don't help
  - Support tickets about edge cases
### **Detection Pattern**


## Feature Overload

### **Id**
feature-overload
### **Summary**
Adding features without considering cognitive load
### **Severity**
high
### **Situation**
  V1: Simple, focused, works great
  V2: Added "requested" features
  V3: Added more "power user" features
  V4: Nobody can find anything
  
### **Why**
  More features = more confusion = fewer completions. Hick's Law: time to decide
  increases with number of options. Every feature is cognitive load.
  
### **Solution**
  # For each feature, ask:
  1. How many users need this?
  2. How often do they need it?
  3. How critical is it when needed?
  
  # Feature Priority Matrix:
               │ Many Users │ Few Users
  ─────────────┼────────────┼───────────
  Frequent Use │ CORE       │ CONSIDER
  ─────────────┼────────────┼───────────
  Rare Use     │ ACCESSIBLE │ HIDE/CUT
  
  CORE: Primary navigation, always visible
  ACCESSIBLE: Settings, menus, secondary nav
  HIDE/CUT: Probably don't build
  
### **Symptoms**
  - Long onboarding needed
  - Users ask "where is X?"
  - Support tickets increase
  - Core metrics decline
### **Detection Pattern**


## Jargon Jungle

### **Id**
jargon-jungle
### **Summary**
Using internal terminology in user-facing interfaces
### **Severity**
high
### **Situation**
  Using words like "Workspace", "Instance", "Sync", "Module", "Entity", "Tenant"
  that mean something internally but confuse users.
  
### **Why**
  Users don't speak your language. They don't know your architecture.
  They think in their own mental models, not yours.
  
### **Solution**
  # Internal → User language:
  "Workspace" → "Your projects"
  "Instance" → "Your copy"
  "Sync" → "Save changes"
  "Dashboard" → "Your stats"
  "Module" → "Your apps"
  
  # Testing jargon:
  1. 5-second test: Show screen, ask "What is this for?"
  2. First-click test: "Where would you click to [task]?"
  3. Card sorting: What do users call things?
  
  # Rules:
  - Use verbs for actions: "Save" not "Persist"
  - Use nouns users know: "Messages" not "Communications"
  - Describe outcomes: "Share with team" not "Set permissions"
  
### **Symptoms**
  - What does this mean?
  - Wrong clicks on first-click tests
  - Users use wrong terminology
  - High support for terminology
### **Detection Pattern**


## Invisible Action

### **Id**
invisible-action
### **Summary**
Important actions that users can't find
### **Severity**
high
### **Situation**
  Actions in hover-only menus, important settings buried deep,
  CTAs that look like text, icons without labels, gestures without hints.
  
### **Why**
  Users can't use features they can't find. If >50% of users can't find an action
  in first-click tests, the action is hidden.
  
### **Solution**
  # Visibility hierarchy:
  Primary actions → Prominent button (always visible)
  Secondary actions → Visible link/button (one click away)
  Tertiary actions → In menus (discoverable)
  Rare actions → Settings or help
  
  # Testing discoverability:
  First-click test: "How would you [action]?"
  >70% correct = discoverable
  <50% correct = hidden
  
  # Fixes:
  - Icons + labels (not icons alone)
  - Visible CTAs, not text links
  - Obvious affordances
  
### **Symptoms**
  - I didn't know I could do that
  - Where is the button for X?
  - High support for basic features
  - Features with low adoption
### **Detection Pattern**


## Infinite Options

### **Id**
infinite-options
### **Summary**
Presenting too many choices at once
### **Severity**
high
### **Situation**
  Pricing page with 7 plans. Settings page with 40 toggles.
  Dropdown with 50 options. Form with 15 fields.
  
### **Why**
  Choice paralysis prevents action. Research shows 2-4 options can be evaluated,
  5-7 slows decisions, 8+ causes paralysis. Users close the tab.
  
### **Solution**
  # Reducing options:
  1. Smart defaults - Pre-select best for most
  2. Progressive disclosure - "Show more options"
  3. Categorization - Group similar options
  4. Recommendations - "Most popular", "Best for you"
  5. Elimination - If <5% use it, remove or hide it
  
  # Good pricing page:
  □ Free (Try it out)
  □ Pro - Most Popular ($29)
  □ Team (Contact us)
  
  # NOT:
  7 plans that differ by small increments
  
### **Symptoms**
  - High drop-off on choice screens
  - I don't know which to pick
  - Analysis paralysis
  - Low conversion on pricing
### **Detection Pattern**


## Broken Flow

### **Id**
broken-flow
### **Summary**
User flows that don't match user mental models
### **Severity**
critical
### **Situation**
  User wants to send $20 to a friend. App requires: add friend, verify identity,
  set up payment, configure settings, initiate transfer, confirm SMS, wait for approval.
  
### **Why**
  Users get lost, frustrated, and leave. Mental model mismatch means your flow
  makes sense to you but not to them. They expected 3 steps, you gave them 8.
  
### **Solution**
  # Flow design principles:
  1. Start with the goal, work backward
     What does user want to achieve?
     What's the minimum path?
  
  2. Progressive complexity
     Easy path for simple cases
     Advanced options for edge cases
  
  3. Forgiving format
     Accept input flexibly
     Don't reject valid variations
  
  4. Clear progress
     Where am I in this process?
     How much is left?
  
  5. Easy recovery
     Go back without losing progress
     Save and continue later
  
### **Symptoms**
  - High drop-off in flows
  - Users start over repeatedly
  - This should be simpler
  - Low completion rates
### **Detection Pattern**


## Feedback Void

### **Id**
feedback-void
### **Summary**
No feedback when users take actions
### **Severity**
high
### **Situation**
  User clicks button. Nothing visible happens. User clicks again.
  Still nothing. User refreshes. Data is duplicated.
  
### **Why**
  Users don't know if actions worked. Without feedback, they retry, creating
  duplicate submissions. Or they leave thinking it's broken.
  
### **Solution**
  # Feedback timing:
  0-100ms: Visual acknowledgment (button press state)
  100ms-1s: Progress indicator
  1-10s: Loading state with progress
  10s+: Background processing with notification
  
  # Implementation:
  onClick = async () => {
    setLoading(true)      // Immediate feedback
    try {
      await action()
      showSuccess()       // Completion feedback
    } catch (e) {
      showError(e)        // Error feedback
    } finally {
      setLoading(false)
    }
  }
  
### **Symptoms**
  - Double submissions
  - Is it working?
  - Users refreshing pages
  - Duplicate records in database
### **Detection Pattern**


## Forced Registration

### **Id**
forced-registration
### **Summary**
Requiring account creation before showing value
### **Severity**
high
### **Situation**
  User lands on page. "Create an account to continue."
  User has no idea what they're signing up for.
  
### **Why**
  Users leave before seeing why they should sign up. Removing forced registration
  can increase conversion 20-50% because users who sign up actually want to.
  
### **Solution**
  # Better pattern:
  1. Show value first - Let users explore, try, experience
  2. Prompt at value moment - "Save your progress" → Sign up
  3. Progressive registration - Start as guest, convert when necessary
  
  # Examples:
  Duolingo: Complete first lesson → then sign up
  Canva: Create design → sign up to save
  Notion: Use templates → sign up to save
  
  # Value-first flow:
  Landing → Try product → Experience value →
  Natural prompt → Easy signup → Continue
  
### **Symptoms**
  - High bounce on signup wall
  - Low signup completion
  - Users don't know what they're signing up for
  - Competitors winning with trials
### **Detection Pattern**


## Form From Hell

### **Id**
form-from-hell
### **Summary**
Long, complex forms that overwhelm users
### **Severity**
high
### **Situation**
  15-field form requiring name, email, phone, address (5 fields), password,
  birthday, gender, occupation, company, referral source.
  
### **Why**
  Every field is a chance to drop off. Each field removed increases completion
  by 5-10%. Users guard their information. Long forms signal bureaucracy.
  
### **Solution**
  # Minimum viable fields:
  Lead gen: Email only (or + first name)
  Trial signup: Email + password
  Demo request: Name + email + company
  
  # Progressive profiling:
  Get email first → Ask more later in-product
  
  # Smart defaults:
  Auto-detect country, auto-complete address, social sign-in
  
  # Multi-step with progress:
  Step 1 of 3: Basic info
  Step 2 of 3: Preferences
  Step 3 of 3: Confirm
  
  # Field counts:
  Ideal: 1-3 fields
  Acceptable: 4-5 fields
  Too many: 6+ fields
  
### **Symptoms**
  - High form abandonment
  - Users start but don't finish
  - Low lead quality (fake data)
  - Complaints about form length
### **Detection Pattern**


## Dead End

### **Id**
dead-end
### **Summary**
Flows that end without clear next steps
### **Severity**
high
### **Situation**
  Error page: "Something went wrong" (nothing else)
  Empty state: Blank page
  Success: "Done!" (no guidance)
  404: "Page not found" (go home only)
  
### **Why**
  Users don't know what to do next. Every dead end is a lost user.
  No screen should be a dead end.
  
### **Solution**
  # Every end needs:
  1. What happened (status)
  2. What to do next (action)
  3. Alternative paths (options)
  
  # Error page:
  "We couldn't load your data."
  [Try again] [Go to dashboard] [Contact support]
  
  # Empty state:
  "No projects yet"
  "Create your first project to get started"
  [Create project] [Import existing]
  
  # Success:
  "Your order is confirmed!"
  [View order] [Continue shopping] [Track delivery]
  
### **Symptoms**
  - Users stuck on error pages
  - High bounce on empty states
  - "Now what?" questions
  - Low engagement after success
### **Detection Pattern**


## Permission Ambush

### **Id**
permission-ambush
### **Summary**
Asking for permissions without context
### **Severity**
high
### **Situation**
  App loads. Immediately: "Allow notifications?" "Allow location?" "Allow camera?"
  User denies all defensively.
  
### **Why**
  Users deny permissions they'd otherwise grant. Contextual permission requests
  have 2-3x higher grant rates than ambush requests.
  
### **Solution**
  # Contextual permission flow:
  1. Wait until feature is used
     User taps "Take Photo" → camera permission
     User taps "Find nearby" → location permission
  
  2. Explain the benefit first
     "Enable notifications to get updates on your order"
     NOT: "Enable notifications"
  
  3. Pre-permission education
     "To scan documents, we need camera access"
     [Enable Camera] [Not now]
  
  4. Graceful degradation
     If denied, offer alternatives
     "You can also enter the code manually"
  
### **Symptoms**
  - Low permission grant rates
  - Users confused about why you need access
  - Features broken after denial
  - Re-prompting annoys users
### **Detection Pattern**
