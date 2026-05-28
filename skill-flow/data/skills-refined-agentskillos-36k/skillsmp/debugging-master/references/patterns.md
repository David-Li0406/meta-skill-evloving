# Debugging Master

## Patterns


---
  #### **Name**
The Scientific Method Loop
  #### **Description**
Systematic hypothesis-driven debugging
  #### **When**
Any non-trivial bug (use after 10 minutes of ad-hoc fails)
  #### **Example**
    # The loop:
    # 1. OBSERVE: What exactly is the symptom?
    # 2. HYPOTHESIZE: What could cause this? Pick most likely.
    # 3. PREDICT: If hypothesis is true, what should happen when I do X?
    # 4. EXPERIMENT: Do X, observe result
    # 5. ANALYZE: Did prediction hold? If no, hypothesis is wrong.
    # 6. REPEAT: New hypothesis based on what you learned
    
    # Example debugging session:
    """
    OBSERVE: API returns 500 on POST /users, works on GET
    
    HYPOTHESIS 1: Request body validation failing
    PREDICT: If true, adding logging before validation will show invalid data
    EXPERIMENT: Add log, reproduce
    RESULT: Log shows valid data, validation passes
    CONCLUSION: Hypothesis rejected, not validation
    
    HYPOTHESIS 2: Database insert failing
    PREDICT: If true, database logs will show error
    EXPERIMENT: Check database logs during reproduction
    RESULT: "duplicate key constraint violation on email"
    CONCLUSION: Hypothesis confirmed - email already exists
    
    ROOT CAUSE: Upsert logic missing, plain insert fails on existing email
    """
    

---
  #### **Name**
Binary Search / Wolf Fence
  #### **Description**
Divide and conquer to isolate bug location
  #### **When**
Bug somewhere in a large codebase or commit history
  #### **Example**
    # The wolf fence: Find a wolf in Alaska by halving the search space
    # 1. Put a fence across the middle of Alaska
    # 2. Wait for the wolf to howl
    # 3. The wolf is in one half - discard the other
    # 4. Repeat until you find the wolf
    
    # In code (manual bisect):
    """
    # Bug: output is wrong somewhere in this pipeline
    def process(data):
        step1_result = transform(data)
        step2_result = validate(step1_result)
        step3_result = enrich(step2_result)
        step4_result = format(step3_result)
        return step4_result
    
    # Bisect: Check middle first
    def process(data):
        step1_result = transform(data)
        step2_result = validate(step1_result)
        print(f"CHECKPOINT: {step2_result}")  # Is this correct?
        # If correct: bug is in step3 or step4
        # If wrong: bug is in step1 or step2
        # Repeat in the guilty half
    """
    
    # In git (automated bisect):
    git bisect start
    git bisect bad HEAD          # Current commit is broken
    git bisect good abc123       # This old commit worked
    # Git checks out middle commit
    # Test, then: git bisect good/bad
    # Repeat until git identifies the guilty commit
    

---
  #### **Name**
Five Whys
  #### **Description**
Trace causal chain to root cause
  #### **When**
You found the bug but need to understand why it happened
  #### **Example**
    # The bug: Production server ran out of memory
    
    # WHY 1: Why did we run out of memory?
    # → The cache grew unbounded
    
    # WHY 2: Why did the cache grow unbounded?
    # → TTL was not set on cache entries
    
    # WHY 3: Why was TTL not set?
    # → The caching library changed defaults in v2.0
    
    # WHY 4: Why didn't we catch this in upgrade?
    # → No tests for cache eviction behavior
    
    # WHY 5: Why no tests for eviction?
    # → Cache was treated as optimization, not critical path
    
    # ROOT CAUSE: Missing test coverage for cache behavior
    # FIX: Add eviction tests, set explicit TTL, document library defaults
    

---
  #### **Name**
Minimal Reproducible Example
  #### **Description**
Strip away everything until only the bug remains
  #### **When**
Bug is buried in complex system
  #### **Example**
    # Goal: Smallest possible code that reproduces the bug
    
    # Start with:
    # - Full application
    # - All dependencies
    # - Real database
    # - Production config
    
    # Remove one thing at a time, checking if bug persists:
    # 1. Replace database with in-memory mock → Bug persists? Keep mock.
    # 2. Remove authentication → Bug persists? Keep removal.
    # 3. Remove unrelated routes → Bug persists? Keep removal.
    # 4. Hardcode config → Bug persists? Keep hardcode.
    
    # End with 20-line file that reproduces bug
    # Benefits:
    # - Forces you to identify actual dependencies
    # - Makes bug obvious (less noise)
    # - Shareable for help
    # - Becomes regression test
    

---
  #### **Name**
Diff-Based Debugging
  #### **Description**
Find what changed when something broke
  #### **When**
It was working yesterday
  #### **Example**
    # If it worked before and doesn't now, something changed.
    # Find the change.
    
    # Code changes:
    git log --oneline --since="yesterday"
    git diff HEAD~5  # What changed recently?
    
    # Dependency changes:
    diff package-lock.json.backup package-lock.json
    git log -p package-lock.json  # When did deps change?
    
    # Environment changes:
    # - New deployment? Check deploy logs
    # - Config change? Diff current vs previous
    # - Infrastructure? Check provider status
    
    # Data changes:
    # - New user triggered edge case?
    # - Data migration ran?
    # - External API changed response format?
    
    # The question is never "why is it broken?"
    # The question is "what changed since it worked?"
    

---
  #### **Name**
Strategic Print Debugging
  #### **Description**
Effective printf debugging that answers specific questions
  #### **When**
Need visibility into runtime behavior
  #### **Example**
    # BAD: Scatter prints everywhere
    print("here 1")
    print("here 2")
    print(data)  # Huge unreadable dump
    
    # GOOD: Answer specific questions
    
    # Question: "Is this function being called?"
    def process_order(order):
        print(f">>> process_order called: order_id={order.id}")
        ...
    
    # Question: "What's the value at this point?"
    def calculate_total(items):
        subtotal = sum(item.price for item in items)
        print(f">>> subtotal={subtotal}, items={len(items)}")
        ...
    
    # Question: "Which branch is executing?"
    if condition_a:
        print(">>> Branch A")
        ...
    elif condition_b:
        print(">>> Branch B")
        ...
    
    # Question: "What's the state before/after?"
    print(f">>> BEFORE transform: {data}")
    result = transform(data)
    print(f">>> AFTER transform: {result}")
    
    # Pro tip: Use distinctive prefix (>>>) so you can grep your prints
    # Pro tip: Remove prints after - they're not documentation
    

## Anti-Patterns


---
  #### **Name**
Confirmation Bias Debugging
  #### **Description**
Looking for evidence that supports your theory
  #### **Why**
    You think you know where the bug is. You look there. You find something
    that could be wrong. You "fix" it. Bug persists. You wasted an hour.
    The bug was never there - you just convinced yourself it was.
    
  #### **Instead**
Try to disprove your hypothesis, not prove it. Ask "what would I see if this ISN'T the cause?"

---
  #### **Name**
The Assumption Blind Spot
  #### **Description**
Not questioning "known good" code
  #### **Why**
    "That part definitely works, I wrote it." "The library handles that."
    "We've never had problems there." Famous last words. The bug often
    hides in the code you trust most, because you never look there.
    
  #### **Instead**
Question everything. Test "known good" code explicitly.

---
  #### **Name**
Symptom Chasing
  #### **Description**
Fixing where the error appears, not where it originates
  #### **Why**
    Error says "null pointer at line 47". You add null check at line 47.
    Bug "fixed". But WHY was it null? The root cause is line 12 where
    you forgot to initialize. Now you have a silent failure instead.
    
  #### **Instead**
Follow the data backward. Where did the bad value come from?

---
  #### **Name**
Debug by Diff
  #### **Description**
Making random changes hoping something works
  #### **Why**
    Change something. Run. Still broken. Change something else. Run.
    Eventually it works. But you don't know why. You can't explain the
    fix. You might have introduced new bugs. You learned nothing.
    
  #### **Instead**
One hypothesis, one change, one test. Know why it works.

---
  #### **Name**
The Heisenbug Surrender
  #### **Description**
Giving up on bugs that disappear when observed
  #### **Why**
    Bug happens in production, not locally. Add logging, bug disappears.
    "Cosmic ray, can't reproduce." But Heisenbugs have causes: timing,
    memory layout, optimization. The observation changes the conditions.
    
  #### **Instead**
Understand what observation changes. That IS the clue.

---
  #### **Name**
Premature Debugging
  #### **Description**
Debugging before confirming the bug exists
  #### **Why**
    User reports "X is broken." You dive into X code. Hours later, you
    discover X works fine - user was holding it wrong, or the bug is
    actually in Y. You debugged the wrong thing.
    
  #### **Instead**
Reproduce first. Verify the bug exists where you think it does.