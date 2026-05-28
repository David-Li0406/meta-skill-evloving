<!-- TIER: 3 | DETAILED REFERENCE -->
<!-- Read after: SKILL.md, agent-script-reference.md -->
<!-- Contains: Pattern selection + Best practices combined -->

# Patterns & Best Practices

This guide combines pattern selection (what to use) with implementation best practices (how to use it well).

---

## Part 1: Pattern Selection

### Pattern Decision Tree

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     PATTERN DECISION TREE                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  What problem are you solving?                                           │
│  │                                                                       │
│  ├─► "I need to run code BEFORE/AFTER every response"                   │
│  │   └─► Lifecycle Events Pattern                                       │
│  │       File: templates/patterns/lifecycle-events.agent                │
│  │                                                                       │
│  ├─► "After action X, Y must ALWAYS happen"                             │
│  │   └─► Action Callbacks Pattern                                       │
│  │       File: templates/patterns/action-callbacks.agent                │
│  │                                                                       │
│  ├─► "Go to specialist topic, then return with results"                 │
│  │   └─► Bidirectional Routing Pattern                                  │
│  │       File: templates/patterns/bidirectional-routing.agent           │
│  │                                                                       │
│  ├─► "Just starting out - what's the minimum?"                          │
│  │   └─► Hello World                                                    │
│  │       File: templates/agents/hello-world.agent                       │
│  │                                                                       │
│  ├─► "Multiple topics, user chooses where to go"                        │
│  │   └─► Multi-Topic Router                                             │
│  │       File: templates/agents/multi-topic.agent                       │
│  │                                                                       │
│  └─► "Need input validation before actions"                             │
│      └─► Error Handling Pattern                                         │
│          File: templates/components/error-handling.agent                │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### Pattern Details

#### 1. Lifecycle Events

**File**: `templates/patterns/lifecycle-events.agent`

**Purpose**: Execute code automatically before and after every reasoning step.

> **⚠️ Deployment Note**: The `run` keyword in lifecycle blocks is **GenAiPlannerBundle only**. AiAuthoringBundle supports `before_reasoning` / `after_reasoning` with `set` statements, but NOT the `run` keyword.

```agentscript
topic conversation:
   before_reasoning:
      set @variables.turn_count = @variables.turn_count + 1
      run @actions.refresh_context                    # ⚠️ GenAiPlannerBundle only
         with user_id=@variables.EndUserId
         set @variables.context = @outputs.fresh_context

   reasoning:
      instructions: ->
         | Turn {!@variables.turn_count}: {!@variables.context}

   after_reasoning:
      run @actions.log_analytics                      # ⚠️ GenAiPlannerBundle only
         with turn=@variables.turn_count
```

| ✅ Good Use Case | ❌ Not Ideal For |
|------------------|------------------|
| Track conversation metrics | One-time setup (use conditional) |
| Refresh context every turn | Heavy processing (adds latency) |
| Log analytics after each response | Actions that might fail often |

---

#### 2. Action Callbacks

**File**: `templates/patterns/action-callbacks.agent`

**Purpose**: Chain deterministic follow-up actions using the `run` keyword.

> **⚠️ Deployment Note**: The `run` keyword is **GenAiPlannerBundle only**. Agents using `run` will NOT be visible in Agentforce Studio.

```agentscript
process_order: @actions.create_order
   with customer_id=@variables.customer_id
   set @variables.order_id = @outputs.order_id
   run @actions.send_confirmation                    # ⚠️ GenAiPlannerBundle only
      with order_id=@variables.order_id
   run @actions.log_activity                         # ⚠️ GenAiPlannerBundle only
      with event="ORDER_CREATED"
```

| ✅ Good Use Case | ❌ Not Ideal For |
|------------------|------------------|
| Audit logging (must happen) | Optional follow-ups (let LLM decide) |
| Send notification after action | Complex branching logic |
| Chain dependent actions | More than 1 level of nesting |

**Critical Rule**: Only 1 level of `run` nesting allowed!

---

#### 3. Bidirectional Routing

**File**: `templates/patterns/bidirectional-routing.agent`

**Purpose**: Navigate to specialist topic, do work, return with results.

```agentscript
# Main hub stores return address
topic main_hub:
   reasoning:
      actions:
         consult_pricing: @utils.transition to @topic.pricing_specialist

# Specialist records where to return
topic pricing_specialist:
   before_reasoning:
      set @variables.return_topic = "main_hub"

   reasoning:
      actions:
         return_with_results: @utils.transition to @topic.main_hub
```

| ✅ Good Use Case | ❌ Not Ideal For |
|------------------|------------------|
| "Consult expert" workflows | Simple linear flows |
| Results need to come back | One-way topic changes |
| Complex multi-step processes | Single-topic agents |

---

#### 4. Multi-Topic Router (Hub-and-Spoke)

**File**: `templates/agents/multi-topic.agent`

**Purpose**: Central topic routes to specialized topics based on user intent.

```agentscript
start_agent topic_selector:
   reasoning:
      instructions: ->
         | Determine what the user needs.
      actions:
         go_orders: @utils.transition to @topic.orders
         go_billing: @utils.transition to @topic.billing
         go_support: @utils.transition to @topic.support
```

| ✅ Good Use Case | ❌ Not Ideal For |
|------------------|------------------|
| Multiple distinct use cases | Single-purpose agents |
| Clear routing criteria | Complex interdependencies |
| Modular topic development | Need to share state heavily |

---

#### 5. Error Handling

**File**: `templates/components/error-handling.agent`

**Purpose**: Validate input before processing, handle failures gracefully.

```agentscript
reasoning:
   instructions: ->
      if @variables.amount is None:
         set @variables.valid = False
         | Please provide an amount.

      if @variables.amount > 10000:
         set @variables.valid = False
         | Amount exceeds maximum allowed.

   actions:
      process: @actions.execute_operation
         available when @variables.valid == True
      retry: @utils.transition to @topic.validation
         available when @variables.operation_failed == True
```

| ✅ Good Use Case | ❌ Not Ideal For |
|------------------|------------------|
| Payment processing | Simple queries |
| Data mutations | Read-only operations |
| Compliance workflows | Low-stakes interactions |

---

### Topic Delegation Pattern (@topic.*)

**Delegation** allows a topic to "consult" another topic and receive control back, unlike permanent transitions.

```agentscript
# ═══════════════════════════════════════════════════════════
# DELEGATION vs TRANSITION
# ═══════════════════════════════════════════════════════════
#
# DELEGATION (@topic.*):     Control CAN return to caller
# TRANSITION (@utils.transition): Control does NOT return
#
# ═══════════════════════════════════════════════════════════

topic main_hub:
   description: "Main conversation hub"
   reasoning:
      actions:
         # DELEGATION - specialist returns control when done
         consult_billing: @topic.billing_specialist
            description: "Ask billing expert for help"
            available when @variables.needs_billing_help == True

         # TRANSITION - permanent move, no return
         go_checkout: @utils.transition to @topic.checkout
            # Note: no description on transitions!

topic billing_specialist:
   description: "Billing expert that returns to caller"
   reasoning:
      instructions: ->
         | Answer billing questions.
         | When done, control returns to main_hub.
```

| Feature | Delegation (`@topic.*`) | Transition (`@utils.transition to`) |
|---------|------------------------|-------------------------------------|
| Returns to caller? | ✅ YES | ❌ NO (permanent) |
| Use in `reasoning.actions` | ✅ YES | ✅ YES |
| Use in `before/after_reasoning` | ❌ NO | ✅ YES (bare syntax) |
| Best for | Consult & return | Menu/workflow navigation |

---

### N-ary Boolean Expressions

AgentScript supports **3 or more conditions** chained with `and`/`or`:

```agentscript
# ═══════════════════════════════════════════════════════════
# THREE+ CONDITIONS WITH AND
# ═══════════════════════════════════════════════════════════

before_reasoning:
   if @variables.is_authenticated and @variables.has_permission and @variables.is_active:
      transition to @topic.authorized

# ═══════════════════════════════════════════════════════════
# THREE+ CONDITIONS WITH OR
# ═══════════════════════════════════════════════════════════

before_reasoning:
   if @variables.is_admin or @variables.is_moderator or @variables.is_owner:
      transition to @topic.elevated_access

# ═══════════════════════════════════════════════════════════
# IN available when CLAUSES
# ═══════════════════════════════════════════════════════════

reasoning:
   actions:
      process_return: @actions.handle_return
         description: "Process customer return request"
         available when @variables.eligible == True and @variables.order_id != None and @variables.tier != "basic"

      premium_action: @actions.premium_feature
         description: "Premium tier feature"
         available when @variables.tier == "premium" or @variables.tier == "enterprise" or @variables.is_trial_premium == True
```

**Key Points:**
- Chain as many conditions as needed with `and` or `or`
- Use `()` grouping for complex expressions: `(a and b) or (c and d)`
- Works in `if` statements and `available when` clauses

---

### Combining Patterns

Patterns can be combined for complex scenarios:

```
┌─────────────────────────────────────────────────────────────┐
│           LIFECYCLE + CALLBACKS + ROUTING                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  topic order_hub:                                            │
│     before_reasoning:                        ◄── Lifecycle   │
│        set @variables.turn_count = ... + 1                   │
│                                                              │
│     reasoning:                                               │
│        actions:                                              │
│           process: @actions.create                           │
│              run @actions.notify           ◄── Callback      │
│              run @actions.log                                │
│                                                              │
│           consult: @utils.transition       ◄── Routing       │
│              to @topic.specialist                            │
│                                                              │
│     after_reasoning:                         ◄── Lifecycle   │
│        run @actions.update_metrics                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Part 2: Best Practices

### 1. Structure & Organization

#### Use Meaningful Names

```agentscript
# ✅ GOOD - Clear, descriptive names
topic order_management:
    description: "Handles order creation, updates, and status inquiries"

# ❌ BAD - Vague names
topic topic1:
    description: "Does stuff"
```

#### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Agent name | PascalCase with underscores | `Customer_Service_Agent` |
| Topic name | snake_case | `order_management` |
| Variable name | snake_case | `user_email` |
| Action name | snake_case | `get_account_details` |

#### Keep Topics Focused

Each topic should handle ONE category of tasks:

```agentscript
# ✅ GOOD - Single responsibility
topic billing_inquiries:
    description: "Answers questions about invoices, payments, and account balances"

topic order_tracking:
    description: "Provides order status and shipping updates"

# ❌ BAD - Too broad
topic customer_stuff:
    description: "Handles billing, orders, support, and everything else"
```

---

### 2. Variable Management

#### Initialize Variables with Defaults (Recommended)

```agentscript
variables:
    # ✅ RECOMMENDED - Has default value (clearer intent)
    user_name: mutable string = ""
        description: "Customer's full name"

    order_count: mutable number = 0
        description: "Number of orders in cart"

    # ✅ ALSO VALID - Works but less explicit
    # user_name: mutable string
    #     description: "Customer's full name"
```

> **Note**: Variables without defaults ARE supported. However, providing defaults is recommended for clarity.

#### Use Appropriate Types

| Data | Type | Example |
|------|------|---------|
| Names, IDs, text | `string` | `"John Doe"` |
| Counts, amounts | `number` | `42`, `99.99` |
| Flags, toggles | `boolean` | `True`, `False` |

#### Document Every Variable

```agentscript
variables:
    cart_total: mutable number = 0
        description: "Total value of items in cart, in USD"

    needs_approval: mutable boolean = False
        description: "Whether the order requires manager approval (>$10,000)"
```

---

### 3. Topic Design

#### Start with a Topic Selector

```agentscript
start_agent topic_selector:
    description: "Routes users to the appropriate topic based on their needs"
    reasoning:
        instructions: ->
            | Determine what the user needs help with.
            | Ask clarifying questions if the intent is unclear.
        actions:
            orders: @utils.transition to @topic.order_management
                description: "Help with orders and purchases"
            support: @utils.transition to @topic.technical_support
                description: "Technical issues and troubleshooting"
```

#### Provide Clear Descriptions

```agentscript
# ✅ GOOD - Specific and actionable
topic password_reset:
    description: "Helps users reset forgotten passwords and unlock accounts"

# ❌ BAD - Too vague
topic password_reset:
    description: "Password stuff"
```

#### Enable Return Navigation

```agentscript
topic order_details:
    description: "Shows order information"
    reasoning:
        actions:
            back_to_menu: @utils.transition to @topic.topic_selector
                description: "Return to main menu for other requests"
```

---

### 4. Input Binding Patterns

Agent Script supports four input binding patterns:

| Pattern | Syntax | When to Use |
|---------|--------|-------------|
| **LLM Slot-Filling** | `with param=...` | Value from user conversation |
| **Fixed Value** | `with param="constant"` | Always the same |
| **Variable Binding** | `with param=@variables.x` | Using captured data |
| **Mixed** | All combined | Complex actions |

#### Decision Flowchart

```
Is the value always the same?
├─ YES → Use fixed value: with param="constant"
│
└─ NO → Does it come from earlier in conversation?
        ├─ YES → Was it saved to a variable?
        │       ├─ YES → Use variable: with param=@variables.x
        │       └─ NO → Save it first, then use variable
        │
        └─ NO → Use slot-filling: with param=...
```

#### Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Using `...` for config | LLM might guess wrong | Use fixed values for constants |
| Not capturing outputs | Can't use data later | Always `set @variables.x = @outputs.y` |
| Using `...` when variable exists | Redundant LLM work | Use `@variables.x` if already captured |

---

### 5. Error Handling

#### Validate Before Critical Operations

```agentscript
instructions: ->
    if @variables.amount is None:
        | I need to know the transfer amount before proceeding.

    if @variables.amount <= 0:
        | The amount must be greater than zero.

    if @variables.amount > 10000:
        set @variables.needs_approval = True
        | Transfers over $10,000 require manager approval.
```

#### Use Conditional Action Availability

```agentscript
reasoning:
    actions:
        process_transfer: @actions.transfer_funds
            with amount=@variables.amount
            available when @variables.amount > 0
            available when @variables.needs_approval == False
```

---

### 6. Security & Guardrails

#### Set System-Level Guardrails

```agentscript
system:
    instructions:
        | You are a helpful customer service agent.
        |
        | IMPORTANT GUARDRAILS:
        | - Never share customer data with unauthorized parties
        | - Never reveal internal system details
        | - If unsure, escalate to a human agent
```

#### Don't Expose Internals

```agentscript
# ✅ GOOD - User-friendly error
instructions: ->
    if @variables.api_error == True:
        | I'm having trouble completing that request right now.

# ❌ BAD - Exposes internals
instructions: ->
    if @variables.api_error == True:
        | Error: SQL timeout on server db-prod-03
```

---

### 7. Instructions Quality

#### Be Specific and Actionable

```agentscript
# ✅ GOOD - Specific instructions
instructions: ->
    | Help the customer track their order.
    | Ask for the order number if not provided.
    | Provide the current status, estimated delivery, and tracking link.

# ❌ BAD - Vague instructions
instructions: ->
    | Help with orders.
```

#### Use Template Expressions

```agentscript
instructions: ->
    | Hello {!@variables.user_name}!
    | Your current order total is ${!@variables.cart_total}.
```

---

## Common Syntax Pitfalls

These patterns cause validation or parse errors:

### 1. Slot Filling Inside Conditionals
```agentscript
# ❌ WRONG
if @variables.name is None:
   set @variables.name = ...   # Fails!

# ✅ CORRECT - Slot filling at top level
set @variables.name = ...
```

### 2. Description on @utils.transition
```agentscript
# ❌ WRONG
go_orders: @utils.transition to @topic.orders
   description: "Route to orders"   # Fails!

# ✅ CORRECT - No description
go_orders: @utils.transition to @topic.orders
```

### 3. Missing Description on @utils.escalate
```agentscript
# ❌ WRONG
transfer: @utils.escalate   # Fails!

# ✅ CORRECT - Description required
transfer: @utils.escalate
   description: "Transfer to human agent"
```

### 4. Empty Lifecycle Blocks
```agentscript
# ❌ WRONG
before_reasoning:
   # Just a comment   # Fails!

# ✅ CORRECT - Remove empty blocks or add content
```

### 5. Dynamic Action Invocation
```agentscript
# ❌ WRONG
invoke: {!@actions.search}   # Fails!

# ✅ CORRECT - Define multiple actions, LLM auto-selects
search_products: @actions.product_search
search_orders: @actions.order_search
```

---

## Validation Scoring Summary

| Pattern | Points | Key Requirement |
|---------|--------|-----------------|
| Config block | 10 | All 4 required fields |
| Linked variables | 10 | EndUserId, RoutableId, ContactId |
| Topic structure | 10 | label, description, reasoning |
| Language block | 5 | default_locale present |
| Lifecycle blocks | 5 | Proper before/after structure |
| Action callbacks | 5 | No nested run |
| Error handling | 5 | Validation patterns |
| Template expressions | 5 | {!@variables.x} syntax |

---

## Quick Reference Checklist

Before deploying an agent, verify:

- [ ] All topics have clear descriptions
- [ ] All variables have descriptions and defaults
- [ ] All actions have input/output descriptions
- [ ] System guardrails are defined
- [ ] Error handling is in place for critical operations
- [ ] Navigation back to main menu from all topics
- [ ] Template expressions use correct syntax `{!@variables.name}`
- [ ] Consistent indentation (tabs recommended)

---

## Slot Filling Reliability Patterns

### Problem: LLM Fails to Extract Values Correctly

Slot filling (`with param=...`) relies on LLM inference, which can fail in subtle ways:

| Symptom | What Happened | Example |
|---------|---------------|---------|
| Empty JSON `{}` sent to action | LLM couldn't find value in conversation | User said "look up my account" without ID |
| Wrong field names | LLM abbreviated or guessed | `_id` instead of `account_id` |
| Wrong value extracted | LLM picked similar value from context | Picked Contact ID instead of Account ID |
| Retry/crash cycles | No recovery path after failure | Agent keeps trying same extraction |

### Root Cause

The `...` syntax is **probabilistic** - the LLM infers what value to use. For critical inputs (IDs, amounts, required fields), this unreliability causes downstream failures.

### Solution: Deterministic Critical Input Collection

Instead of relying on slot filling for critical inputs, use this 5-pattern approach:

#### Pattern 1: First-Interaction Collection

Tell the LLM its PRIMARY GOAL is to collect the input:

```agentscript
reasoning:
   instructions: ->
      | YOUR PRIMARY GOAL: Collect the account ID from the user.
      | Do NOT proceed with any other actions until account_id is captured.
      |
      if @variables.account_id == "":
         | ⚠️ Account ID not yet collected. ASK the user for it.
```

**Why it works:** Explicit priority instructions override LLM's tendency to "help" by guessing.

#### Pattern 2: Variable Setter Action

Create a **dedicated action** to capture and validate critical input:

```agentscript
actions:
   capture_account_id:
      description: "Captures and validates the Salesforce Account ID from user"
      inputs:
         account_id: string
            description: "The 18-character Salesforce Account ID (starts with 001)"
            is_required: True
      outputs:
         validated_id: string
            description: "The validated account ID (empty if invalid)"
         is_valid: boolean
            description: "Whether the ID is valid"
      target: "flow://Validate_Account_Id"
```

**Why it works:** The Flow performs server-side validation, ensuring only valid IDs are stored.

#### Pattern 3: Single-Use Pattern

Make the setter action **unavailable once the variable is set**:

```agentscript
reasoning:
   actions:
      validate_id: @actions.capture_account_id
         with account_id=...
         set @variables.account_id = @outputs.validated_id
         set @variables.account_id_validated = @outputs.is_valid
         # ★ SINGLE-USE: Becomes unavailable after successful capture
         available when @variables.account_id == ""
```

**Why it works:** Prevents redundant re-collection attempts that can introduce errors.

#### Pattern 4: Null Guard All Downstream Actions

Block ALL other actions until critical input is validated:

```agentscript
reasoning:
   actions:
      # ★ RESEARCH ACTION - Uses variable, NOT slot filling
      do_research: @actions.research_account
         with account_id=@variables.account_id    # Variable binding!
         available when @variables.account_id_validated == True

      # ★ TOPIC TRANSITION - Also guarded
      go_research: @utils.transition to @topic.research
         available when @variables.account_id_validated == True
```

**Why it works:** Ensures downstream actions receive valid data, not LLM guesses.

#### Pattern 5: Explicit Action References in Instructions

Guide the LLM on WHICH action to use:

```agentscript
instructions: ->
   | To capture the account ID, use {!@actions.capture_account_id}.
   | This ensures the ID is validated before proceeding.
```

**Why it works:** Reduces ambiguity about which action handles input collection.

---

### When NOT to Use Slot Filling

| Use Slot Filling (`...`) | Use Variable/Fixed Value |
|--------------------------|--------------------------|
| Optional, non-critical inputs | Critical IDs (account, order, case) |
| User preference inputs | Values that must be validated |
| One-time collection | Values used across multiple actions |
| Simple text descriptions | Values with specific formats (dates, IDs) |

**Decision Rule:** If invalid input would cause downstream failure, use deterministic collection.

---

### Troubleshooting Slot Filling Issues

#### Symptom: Empty JSON Sent to Action

```
ERROR: Action received {} instead of {account_id: "001..."}
```

**Cause:** LLM couldn't extract value from conversation.

**Fix:**
1. Add explicit collection instructions: "YOUR PRIMARY GOAL: collect account_id"
2. Use a dedicated setter action with clear input description
3. Add `available when @var != ""` guard on downstream actions

#### Symptom: Wrong Field Names

```
ERROR: Property _id not found. Expected: account_id
```

**Cause:** LLM inferred/abbreviated field name.

**Fix:**
1. Use exact field name in action input description
2. Add instruction: "The account_id must be the exact value provided by user"
3. Use validation action that normalizes input

#### Symptom: Agent Retries Then Crashes

```
Agent attempted 5 times, then failed with: Internal Error
```

**Cause:** No recovery path after extraction failure.

**Fix:**
1. Add retry counter: `collection_attempts: mutable number = 0`
2. Increment on each attempt: `set @var = @var + 1`
3. Add escape condition: `if @variables.attempts > 3: | Please verify your ID format`

---

### Complete Pattern Template

See `templates/patterns/critical-input-collection.agent` for a complete implementation demonstrating all five patterns together.

---

## Related Documentation

- [Agent Script Reference](agent-script-reference.md) - Complete syntax guide
- [Actions Reference](actions-reference.md) - Action integration details
- [Prompt Templates](prompt-templates.md) - Prompt Template integration
