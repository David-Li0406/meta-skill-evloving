# Refactoring Guide

## Patterns


---
  #### **Name**
The Safe Refactoring Cycle
  #### **Description**
Always refactor with this safety net
  #### **When**
Any refactoring, no matter how small
  #### **Example**
    # THE CYCLE (from Martin Fowler):
    # 1. Make sure tests pass
    # 2. Make a small change
    # 3. Run tests
    # 4. If tests fail, undo immediately
    # 5. If tests pass, commit (or continue)
    # 6. Repeat
    
    # Example: Extract Method refactoring
    
    # BEFORE:
    def process_order(order):
        # Validate
        if not order.items:
            raise ValueError("Empty order")
        if not order.customer_id:
            raise ValueError("No customer")
        for item in order.items:
            if item.quantity <= 0:
                raise ValueError(f"Invalid quantity for {item.id}")
    
        # Calculate total
        subtotal = sum(item.price * item.quantity for item in order.items)
        tax = subtotal * 0.1
        total = subtotal + tax
    
        # Save
        db.save(order, total)
        return total
    
    # STEP 1: Tests pass? Yes. Commit checkpoint.
    
    # STEP 2: Extract validation (small change)
    def validate_order(order):
        if not order.items:
            raise ValueError("Empty order")
        if not order.customer_id:
            raise ValueError("No customer")
        for item in order.items:
            if item.quantity <= 0:
                raise ValueError(f"Invalid quantity for {item.id}")
    
    def process_order(order):
        validate_order(order)
        # ... rest unchanged
    
    # STEP 3: Run tests. Pass? Good.
    
    # STEP 4: Commit: "Extract validate_order from process_order"
    
    # STEP 5: Next extraction (calculate_total)...
    
    # KEY: Each step is tiny. Each step is verified. Each step is committed.
    

---
  #### **Name**
Characterization Tests for Legacy Code
  #### **Description**
Capture existing behavior before touching legacy code
  #### **When**
Refactoring code without tests
  #### **Example**
    # Michael Feathers' technique from "Working Effectively with Legacy Code"
    
    # STEP 1: Write a test that calls the code
    def test_calculate_discount_characterization():
        result = calculate_discount(100, "SUMMER")
        # Don't know what it should return yet!
    
    # STEP 2: Run it and see what happens
    # Output: AssertionError: None != ???
    # Actual result was: 15
    
    # STEP 3: Assert on actual behavior
    def test_calculate_discount_characterization():
        result = calculate_discount(100, "SUMMER")
        assert result == 15  # Captured behavior
    
    # STEP 4: Add more cases to capture more behavior
    def test_calculate_discount_characterization():
        assert calculate_discount(100, "SUMMER") == 15
        assert calculate_discount(100, "WINTER") == 10
        assert calculate_discount(100, "INVALID") == 0
        assert calculate_discount(0, "SUMMER") == 0
        assert calculate_discount(-50, "SUMMER") == 0  # Edge case!
    
    # STEP 5: Now you can refactor safely
    # These tests capture WHAT the code does, not what it SHOULD do
    # If behavior was wrong, fix it separately (with a new test)
    
    # WARNING: Characterization tests are not specification tests
    # They may preserve bugs! That's intentional for safe refactoring.
    # Fix bugs separately after refactoring.
    

---
  #### **Name**
The Strangler Fig Pattern
  #### **Description**
Incrementally replace legacy systems without big-bang rewrites
  #### **When**
Need to replace a legacy system
  #### **Example**
    # Named after strangler figs that grow around trees and eventually replace them
    
    # THE PATTERN:
    # 1. Add new code alongside old code
    # 2. Route some traffic to new code
    # 3. Gradually expand new code coverage
    # 4. Eventually remove old code
    
    # Example: Replacing legacy order processor
    
    # PHASE 1: Facade that delegates to old system
    class OrderProcessor:
        def __init__(self):
            self.legacy = LegacyOrderProcessor()
            self.new = NewOrderProcessor()
    
        def process(self, order):
            # 100% legacy
            return self.legacy.process(order)
    
    # PHASE 2: Feature flag for new system
    def process(self, order):
        if self.use_new_processor(order):
            return self.new.process(order)
        return self.legacy.process(order)
    
    def use_new_processor(self, order):
        # Start with 1% of traffic, low-risk orders
        return (
            order.total < 100 and
            random.random() < 0.01
        )
    
    # PHASE 3: Gradually increase coverage
    def use_new_processor(self, order):
        # Now 50% of low-risk, 10% of all
        if order.total < 100:
            return random.random() < 0.50
        return random.random() < 0.10
    
    # PHASE 4: Full migration
    def use_new_processor(self, order):
        return True  # All traffic to new
    
    # PHASE 5: Remove legacy
    def process(self, order):
        return self.new.process(order)
    # Delete LegacyOrderProcessor entirely
    
    # KEY INSIGHT: Each phase is independently deployable and reversible
    

---
  #### **Name**
Extract Till You Drop
  #### **Description**
Keep extracting until each function does exactly one thing
  #### **When**
Long method that does too much
  #### **Example**
    # Uncle Bob's approach: extract until functions are tiny and well-named
    
    # BEFORE: 50-line method
    def process_payment(order, card):
        # Validate card (10 lines)
        # Check fraud (10 lines)
        # Calculate fees (10 lines)
        # Charge card (10 lines)
        # Update records (10 lines)
    
    # AFTER: Composed method
    def process_payment(order, card):
        validate_card(card)
        check_for_fraud(order, card)
        fees = calculate_processing_fees(order)
        charge_result = charge_card(card, order.total + fees)
        record_payment(order, charge_result)
    
    # Each extracted function:
    # 1. Has a clear, descriptive name
    # 2. Does exactly one thing
    # 3. Is at the same level of abstraction
    # 4. Is independently testable
    
    # WHEN TO STOP:
    # - Function does one thing
    # - Function is at one level of abstraction
    # - You can't think of a good name for an extraction
    # - Extraction would make code harder to understand
    

---
  #### **Name**
Parallel Change (Expand and Contract)
  #### **Description**
Make breaking changes safely through parallel implementation
  #### **When**
Changing interfaces without breaking callers
  #### **Example**
    # Instead of changing in place, run old and new in parallel
    
    # PHASE 1: Expand - add new interface alongside old
    class UserService:
        # Old method - still works
        def get_user(self, user_id: int) -> User:
            return self._fetch_user(user_id)
    
        # New method - takes string UUID
        def get_user_by_uuid(self, uuid: str) -> User:
            return self._fetch_user_by_uuid(uuid)
    
    # PHASE 2: Migrate callers one by one
    # Old: service.get_user(123)
    # New: service.get_user_by_uuid("uuid-123")
    
    # PHASE 3: Contract - remove old method when no callers remain
    class UserService:
        def get_user_by_uuid(self, uuid: str) -> User:
            return self._fetch_user_by_uuid(uuid)
    
    # Or rename to get_user if preferred:
    class UserService:
        def get_user(self, uuid: str) -> User:  # Now takes UUID
            return self._fetch_user_by_uuid(uuid)
    
    # BENEFITS:
    # - Never breaks existing callers
    # - Migration can be gradual
    # - Easy to roll back
    # - Each phase is independently deployable
    

---
  #### **Name**
Seam Identification
  #### **Description**
Find points where you can alter behavior without editing code
  #### **When**
Working with untestable legacy code
  #### **Example**
    # Michael Feathers: A "seam" is a place where you can change behavior
    # without editing the code in that place.
    
    # PROBLEM: Untestable code with hardcoded dependency
    class ReportGenerator:
        def generate(self):
            data = Database.query("SELECT * FROM sales")  # Hardcoded!
            # ... process data
    
    # SEAM TYPE 1: Object Seam (dependency injection)
    class ReportGenerator:
        def __init__(self, database=None):
            self.database = database or Database()
    
        def generate(self):
            data = self.database.query("SELECT * FROM sales")
            # Now testable with mock database
    
    # SEAM TYPE 2: Preprocessing Seam (for legacy code)
    class ReportGenerator:
        def get_database(self):
            return Database()  # Override in test subclass
    
        def generate(self):
            data = self.get_database().query("SELECT * FROM sales")
    
    # In test:
    class TestableReportGenerator(ReportGenerator):
        def get_database(self):
            return MockDatabase()
    
    # SEAM TYPE 3: Link Seam (module level)
    # In production: from database import Database
    # In test: mock the import
    # @patch('report.Database')
    
    # FINDING SEAMS:
    # Look for: imports, new X(), global calls, static methods
    # Each is a potential seam to exploit for testing
    

---
  #### **Name**
Mikado Method
  #### **Description**
Handle complex refactoring with dependency graph
  #### **When**
Refactoring that keeps revealing more needed changes
  #### **Example**
    # When you try to change X, you find you need to change Y first,
    # and Y needs Z, and Z needs W... use the Mikado Method.
    
    # STEP 1: Try the change you want
    # Try: Rename User.name to User.fullName
    # Fails! 200 files use .name
    
    # STEP 2: Draw the goal
    """
    [Rename User.name to fullName] (GOAL)
    """
    
    # STEP 3: Try again, note what breaks, draw dependencies
    """
    [Rename User.name to fullName] (GOAL)
      ├── [Update UserSerializer] (broke)
      ├── [Update UserForm] (broke)
      └── [Update 15 templates] (broke)
    """
    
    # STEP 4: Revert! Pick a leaf node and try that
    # Try: Update UserSerializer
    # Works! Commit it.
    
    """
    [Rename User.name to fullName] (GOAL)
      ├── [Update UserSerializer] ✓ DONE
      ├── [Update UserForm] (try next)
      └── [Update 15 templates]
    """
    
    # STEP 5: Continue until all leaves done, then do goal
    # Each step is small, reversible, and committed
    
    # THE GRAPH HELPS YOU:
    # - Not lose track of what needs doing
    # - Work on independent branches in parallel
    # - Know when the goal is achievable
    # - Visualize the total scope
    

## Anti-Patterns


---
  #### **Name**
The Big Rewrite
  #### **Description**
Throwing away working code to rewrite from scratch
  #### **Why**
    Rewrites take longer than estimated, lose institutional knowledge, introduce
    new bugs, and often get cancelled before completion. Joel Spolsky called this
    "the single worst strategic mistake that any software company can make."
    
  #### **Instead**
Use Strangler Fig pattern. Replace incrementally. Keep the system running.

---
  #### **Name**
Refactoring Without Tests
  #### **Description**
Changing code structure without safety net
  #### **Why**
    Refactoring means changing structure while preserving behavior. Without tests,
    how do you know behavior is preserved? You don't. You're just editing and hoping.
    
  #### **Instead**
Write characterization tests first, or use IDE automated refactorings that are proven safe.

---
  #### **Name**
Refactoring While Adding Features
  #### **Description**
Mixing structural changes with behavior changes
  #### **Why**
    If something breaks, was it the refactoring or the feature? You can't tell.
    Blame is unclear. Rollback is all-or-nothing. It's a debugging nightmare.
    
  #### **Instead**
Separate commits. Better yet, separate branches. Refactor first, then add feature.

---
  #### **Name**
Premature Abstraction
  #### **Description**
Creating abstractions "because we might need them" during refactoring
  #### **Why**
    Refactoring should simplify, not add speculative complexity. Adding interfaces,
    factories, and patterns "for flexibility" often makes code harder to understand
    without providing actual benefit.
    
  #### **Instead**
Refactor to simplicity first. Add abstraction only when you feel concrete pain.

---
  #### **Name**
The Perfection Trap
  #### **Description**
Refactoring endlessly toward ideal code
  #### **Why**
    Perfect is the enemy of good. Refactoring has diminishing returns. At some point,
    the code is "good enough" and further refactoring is procrastination or gold-plating.
    
  #### **Instead**
Set a goal. Stop when you reach it. Ship and move on.

---
  #### **Name**
Shotgun Refactoring
  #### **Description**
Making many scattered changes without a clear goal
  #### **Why**
    Random improvements without focus create churn without benefit. You touch many
    files, increase merge conflicts, but don't actually improve the codebase in a
    coherent direction.
    
  #### **Instead**
Focus on one smell, one area, one goal at a time.