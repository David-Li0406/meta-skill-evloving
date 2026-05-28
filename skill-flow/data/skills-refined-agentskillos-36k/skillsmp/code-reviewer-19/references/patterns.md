# Code Reviewer

## Patterns


---
  #### **Name**
Structured Code Review
  #### **Description**
Systematic approach to reviewing code changes
  #### **When**
Reviewing any pull request
  #### **Example**
    # Code Review Checklist
    
    ## 1. Understand Context (5 min)
    - Read PR description and linked issues
    - Understand the problem being solved
    - Check if approach was discussed beforehand
    
    ## 2. High-Level Review (10 min)
    - Does the architecture make sense?
    - Is this the right place for this code?
    - Are there simpler approaches?
    - Does it follow existing patterns in the codebase?
    
    ## 3. Detailed Review (15 min)
    - Logic correctness and edge cases
    - Error handling completeness
    - Security implications
    - Performance considerations
    - Test coverage and quality
    
    ## 4. Code Quality (5 min)
    - Naming clarity
    - Documentation where needed
    - Code organization
    - DRY violations
    
    ## 5. Provide Feedback
    # Use prefixes to indicate severity:
    
    # [BLOCKING] Must fix before merge
    [BLOCKING] This SQL query is vulnerable to injection.
    Use parameterized queries instead.
    
    # [SUGGESTION] Would improve but not required
    [SUGGESTION] Consider extracting this into a helper
    function for reusability.
    
    # [QUESTION] Need clarification
    [QUESTION] What happens if the user is not found?
    I don't see error handling for that case.
    
    # [NITPICK] Style preference, take it or leave it
    [NITPICK] I'd name this `user_memories` instead
    of `umems` for clarity.
    
    # [PRAISE] Acknowledge good work
    [PRAISE] Love how you handled the edge case here.
    This is much cleaner than the old approach.
    

---
  #### **Name**
Security-Focused Review
  #### **Description**
Identifying security vulnerabilities in code
  #### **When**
Reviewing code that handles user input or sensitive data
  #### **Example**
    # Security Review Checklist
    
    ## Input Validation
    # ❌ Vulnerable: Direct user input in query
    query = f"SELECT * FROM users WHERE id = {user_id}"
    
    # ✅ Secure: Parameterized query
    query = "SELECT * FROM users WHERE id = $1"
    await conn.fetch(query, user_id)
    
    ## Authentication & Authorization
    # Check: Is auth required for this endpoint?
    # Check: Is the user authorized for this specific resource?
    
    @require_auth
    async def get_memory(memory_id: str, user: User):
        memory = await repo.get(memory_id)
        # ❌ Missing: Authorization check
        # ✅ Add: Verify user owns this memory
        if memory.owner_id != user.id:
            raise ForbiddenError("Not your memory")
        return memory
    
    ## Sensitive Data Handling
    # Check: Are secrets logged or exposed?
    # ❌ Leaks secret
    logger.info(f"Connecting with key: {api_key}")
    
    # ✅ Masked
    logger.info(f"Connecting with key: {api_key[:4]}...")
    
    ## Output Encoding
    # Check: Is output properly escaped for context?
    # ❌ XSS vulnerable
    return f"<div>{user_input}</div>"
    
    # ✅ Escaped
    return f"<div>{html.escape(user_input)}</div>"
    
    ## Common Vulnerabilities
    - SQL Injection: User input in queries
    - XSS: User input in HTML output
    - IDOR: Missing authorization on resource access
    - Path Traversal: User input in file paths
    - Command Injection: User input in shell commands
    - SSRF: User-controlled URLs in server requests
    

---
  #### **Name**
Constructive Feedback Patterns
  #### **Description**
Providing feedback that improves code AND morale
  #### **When**
Writing any code review comment
  #### **Example**
    # Constructive Feedback Examples
    
    ## Instead of: "This is wrong"
    ## Write:
    "This approach works for the happy path, but I'm
    concerned about the case where `user` is None.
    What do you think about adding a guard clause here?"
    
    ## Instead of: "Use a better name"
    ## Write:
    "The name `data` is a bit generic. Since this holds
    user preferences, would `user_preferences` make the
    purpose clearer to future readers?"
    
    ## Instead of: "This is inefficient"
    ## Write:
    "I noticed this queries the database in a loop.
    With N users, that's N queries. We could batch this
    with `WHERE id IN (...)` to reduce it to 1 query.
    Would you like me to show an example?"
    
    ## Instead of: "Add tests"
    ## Write:
    "This function has some edge cases (null input,
    empty array, very long strings) that would be great
    to cover with tests. Would you mind adding a few
    test cases for these scenarios?"
    
    ## Give praise where deserved
    "Really clean solution here. The early return pattern
    makes the happy path much easier to follow."
    
    "Great catch on that race condition. The mutex
    approach is exactly right."
    

---
  #### **Name**
Refactoring Guidance
  #### **Description**
Identifying and suggesting refactoring opportunities
  #### **When**
Code works but could be cleaner
  #### **Example**
    # Refactoring Suggestions
    
    ## Extract Method
    # Before: Long function with multiple responsibilities
    async def process_memory(memory: Memory):
        # 50 lines of validation
        # 30 lines of transformation
        # 20 lines of storage
    
    # Suggestion:
    "This function does validation, transformation, and storage.
    Consider extracting:
    - `validate_memory(memory)` → bool
    - `transform_memory(memory)` → TransformedMemory
    - `store_memory(memory)` → StoredMemory
    
    Each becomes testable in isolation."
    
    ## Replace Conditionals with Polymorphism
    # Before
    if memory.type == "episodic":
        handle_episodic(memory)
    elif memory.type == "semantic":
        handle_semantic(memory)
    elif memory.type == "procedural":
        handle_procedural(memory)
    
    # Suggestion:
    "Consider using a strategy pattern here:
    ```python
    handlers = {
        'episodic': EpisodicHandler(),
        'semantic': SemanticHandler(),
        'procedural': ProceduralHandler(),
    }
    handlers[memory.type].handle(memory)
    ```
    Makes it easy to add new memory types."
    
    ## Simplify Nested Conditionals
    # Before
    if user:
        if user.is_active:
            if user.has_permission:
                return do_thing()
    
    # Suggestion:
    "The nesting makes it hard to follow. Consider guard clauses:
    ```python
    if not user:
        return None
    if not user.is_active:
        return None
    if not user.has_permission:
        raise PermissionError()
    return do_thing()
    ```"
    

## Anti-Patterns


---
  #### **Name**
Nitpicking Without Substance
  #### **Description**
Focusing on style over correctness
  #### **Why**
Wastes time, frustrates developers, misses real issues.
  #### **Instead**
Catch bugs first, security second, style last

---
  #### **Name**
Review Without Context
  #### **Description**
Reviewing code without understanding the problem
  #### **Why**
Suggestions may be irrelevant or counterproductive.
  #### **Instead**
Read the issue, understand the goal, then review

---
  #### **Name**
Drive-By Comments
  #### **Description**
Dropping criticism without explanation
  #### **Why**
"This is bad" teaches nothing, creates resentment.
  #### **Instead**
Explain why, suggest alternative, offer to discuss

---
  #### **Name**
Blocking on Preferences
  #### **Description**
Requiring changes for personal style preferences
  #### **Why**
Your style isn't objectively better. Ship the feature.
  #### **Instead**
Block on bugs, suggest on style, accept differences

---
  #### **Name**
Delayed Reviews
  #### **Description**
Letting PRs sit for days without feedback
  #### **Why**
Blocks progress, context is lost, merge conflicts grow.
  #### **Instead**
Review within 24 hours, or communicate delay