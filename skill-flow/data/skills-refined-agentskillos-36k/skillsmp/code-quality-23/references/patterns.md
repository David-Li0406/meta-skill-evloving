# Code Quality

## Patterns


---
  #### **Name**
Readable Before Clever
  #### **Description**
Optimize for the reader, not the writer
  #### **When**
Any code that will be maintained by others (all code)
  #### **Example**
    # BAD: Clever one-liner
    const activeAdmins = users.filter(u => u.role === 'admin' && u.active).map(u => u.id);
    
    # GOOD: Readable steps
    const admins = users.filter(user => user.role === 'admin');
    const activeAdmins = admins.filter(user => user.active);
    const adminIds = activeAdmins.map(user => user.id);
    
    # ALSO GOOD: Clear single chain with line breaks
    const adminIds = users
      .filter(user => user.role === 'admin')
      .filter(user => user.active)
      .map(user => user.id);
    
    # The rule: Would a new team member understand this in 10 seconds?
    # If not, simplify.
    

---
  #### **Name**
Naming That Communicates
  #### **Description**
Names should reveal intent, context, and type
  #### **When**
Naming anything - variables, functions, classes, files
  #### **Example**
    # VARIABLES: Reveal what it is and why it exists
    
    # BAD: Generic or abbreviated
    const d = new Date();
    const tmp = users.filter(u => u.active);
    const data = fetchUsers();
    
    # GOOD: Descriptive and contextual
    const accountCreatedAt = new Date();
    const activeUsers = users.filter(user => user.active);
    const fetchedUsers = fetchUsers();
    
    # FUNCTIONS: Verb + noun, describe the action and result
    
    # BAD: Vague or misleading
    function process(data) { }
    function handle(event) { }
    function getData() { }  // Get from where?
    
    # GOOD: Specific and honest
    function validateOrderItems(items) { }
    function handlePaymentWebhook(event) { }
    function fetchUserFromDatabase(userId) { }
    
    # BOOLEANS: Read like a question
    
    # BAD: Ambiguous
    const user = true;
    const loading = false;
    
    # GOOD: Reads naturally
    const isActiveUser = true;
    const isLoading = false;
    const hasPermission = checkPermission(user, action);
    

---
  #### **Name**
Functions That Do One Thing
  #### **Description**
Each function has a single, clear purpose
  #### **When**
Writing or reviewing any function
  #### **Example**
    # The test: Can you describe what the function does without using "and"?
    
    # BAD: Does multiple things
    function processOrder(order) {
      // Validates order
      if (!order.items.length) throw new Error('Empty order');
    
      // Calculates total
      const total = order.items.reduce((sum, item) => sum + item.price, 0);
    
      // Saves to database
      await db.orders.insert({ ...order, total });
    
      // Sends confirmation email
      await sendEmail(order.user.email, 'Order confirmed', { order });
    
      // Updates inventory
      for (const item of order.items) {
        await db.inventory.decrement(item.productId, item.quantity);
      }
    }
    
    # GOOD: Each function has one job
    function validateOrder(order) {
      if (!order.items.length) throw new Error('Empty order');
    }
    
    function calculateOrderTotal(items) {
      return items.reduce((sum, item) => sum + item.price, 0);
    }
    
    async function processOrder(order) {
      validateOrder(order);
      const total = calculateOrderTotal(order.items);
      const savedOrder = await saveOrder({ ...order, total });
      // Queue these as background jobs
      await queue.add('send-confirmation', { orderId: savedOrder.id });
      await queue.add('update-inventory', { items: order.items });
      return savedOrder;
    }
    
    # Note: Don't go too far. 3-5 line functions everywhere is also bad.
    # Balance single responsibility with reasonable locality.
    

---
  #### **Name**
Pragmatic SOLID
  #### **Description**
Apply SOLID principles with judgment, not dogma
  #### **When**
Designing classes or modules
  #### **Example**
    # SOLID is a guide, not a religion. Here's when to apply each:
    
    ## Single Responsibility Principle (SRP)
    # WHEN TO APPLY: Class doing unrelated things
    # WHEN TO IGNORE: Would create class explosion for trivial logic
    
    # BAD: Too strict SRP
    class UserNameValidator { }
    class UserEmailValidator { }
    class UserPasswordValidator { }
    class UserValidatorOrchestrator { }
    
    # GOOD: Pragmatic SRP
    class UserValidator {
      validateName(name) { }
      validateEmail(email) { }
      validatePassword(password) { }
    }
    
    ## Open/Closed Principle (OCP)
    # WHEN TO APPLY: You've already extended the same code 3+ times
    # WHEN TO IGNORE: Speculative future needs ("might need to extend")
    
    # YAGNI violation: Plugin architecture for 2 payment providers
    # Pragmatic: Switch statement for 2 providers, refactor if adding 3rd
    
    ## Liskov Substitution Principle (LSP)
    # WHEN TO APPLY: You're using inheritance
    # BETTER ADVICE: Prefer composition over inheritance, then LSP rarely matters
    
    ## Interface Segregation Principle (ISP)
    # WHEN TO APPLY: Classes implementing methods they don't use
    # WHEN TO IGNORE: Would create interface explosion
    
    ## Dependency Inversion Principle (DIP)
    # WHEN TO APPLY: Testing is hard due to concrete dependencies
    # WHEN TO IGNORE: For stable, unlikely-to-change dependencies
    
    # BAD: Abstracting everything
    interface ILogger { }
    interface IDateProvider { }
    interface IStringFormatter { }
    
    # GOOD: Abstract unstable dependencies
    interface PaymentGateway { }  // This might change
    // Just use console.log, Date, String directly
    

---
  #### **Name**
The Rule of Three
  #### **Description**
Wait for three occurrences before abstracting
  #### **When**
Tempted to create an abstraction for duplicated code
  #### **Example**
    # The pattern: Duplicate once is OK. Twice is a smell. Three times, abstract.
    
    # First occurrence: Just write it
    function createAdminUser(data) {
      const hashedPassword = await hashPassword(data.password);
      return db.users.insert({ ...data, password: hashedPassword, role: 'admin' });
    }
    
    # Second occurrence: Note the duplication, but don't abstract yet
    function createRegularUser(data) {
      const hashedPassword = await hashPassword(data.password);
      return db.users.insert({ ...data, password: hashedPassword, role: 'user' });
    }
    
    # Third occurrence: Now you understand the pattern, abstract
    function createUser(data, role) {
      const hashedPassword = await hashPassword(data.password);
      return db.users.insert({ ...data, password: hashedPassword, role });
    }
    
    # WHY WAIT?
    # - First two cases might diverge in unexpected ways
    # - The "right" abstraction isn't clear from 2 examples
    # - Wrong abstraction is worse than duplication
    

---
  #### **Name**
Comments That Add Value
  #### **Description**
Comment the why, not the what
  #### **When**
Code behavior isn't obvious from context
  #### **Example**
    # BAD: Comments that explain what (the code already says this)
    // Increment counter by 1
    counter++;
    
    // Loop through users
    for (const user of users) { }
    
    # BAD: Comments that become lies
    // Returns user or null
    function getUser(id) {
      return users.get(id) || { guest: true };  // Actually returns guest object
    }
    
    # GOOD: Comments that explain why
    // Using 86400 instead of 60*60*24 for performance (hot path)
    const SECONDS_PER_DAY = 86400;
    
    // Skip validation for internal service calls (already validated upstream)
    if (request.source === 'internal') {
      return processRequest(request);
    }
    
    // Retry 3 times because Stripe occasionally returns 500 on first attempt
    // See: https://github.com/stripe/stripe-node/issues/123
    const result = await retry(3, () => stripe.charges.create(charge));
    
    # GOOD: Comments that warn
    // WARNING: This function is called from a cron job AND the API.
    // Any changes must work for both contexts.
    
    // HACK: Working around React 18 batching bug. Remove after upgrade.
    // See: JIRA-1234
    

---
  #### **Name**
Guard Clauses
  #### **Description**
Handle edge cases early, keep happy path unindented
  #### **When**
Functions with multiple conditions or error cases
  #### **Example**
    # BAD: Deeply nested conditions
    function processPayment(order, user) {
      if (order) {
        if (user) {
          if (user.hasPaymentMethod) {
            if (order.total > 0) {
              // Finally, the actual logic
              return chargeUser(user, order.total);
            } else {
              throw new Error('Invalid order total');
            }
          } else {
            throw new Error('No payment method');
          }
        } else {
          throw new Error('User required');
        }
      } else {
        throw new Error('Order required');
      }
    }
    
    # GOOD: Guard clauses at the top
    function processPayment(order, user) {
      if (!order) throw new Error('Order required');
      if (!user) throw new Error('User required');
      if (!user.hasPaymentMethod) throw new Error('No payment method');
      if (order.total <= 0) throw new Error('Invalid order total');
    
      // Happy path is clear and unindented
      return chargeUser(user, order.total);
    }
    

## Anti-Patterns


---
  #### **Name**
Premature Abstraction
  #### **Description**
Creating abstractions before understanding the pattern
  #### **Why**
    You see two similar things and immediately create an abstraction. But you
    don't yet understand how they're similar or different. The abstraction
    becomes a straitjacket that makes future changes harder, not easier.
    
  #### **Instead**
Apply the Rule of Three. Wait until you've seen the pattern three times before abstracting.

---
  #### **Name**
Enterprise FizzBuzz
  #### **Description**
Simple problems solved with excessive architecture
  #### **Why**
    Interface for everything. Factory for every class. Strategy pattern for
    two options. The code is "extensible" for changes that will never come,
    while simple changes require touching 12 files.
    
  #### **Instead**
Start with the simplest thing that works. Add patterns when complexity demands them, not before.

---
  #### **Name**
Clever Code
  #### **Description**
Code that shows off rather than communicates
  #### **Why**
    One-liners that require 5 minutes to understand. Clever bitwise operations.
    Regex that does 10 things. You feel smart writing it, everyone else suffers
    reading it. Including future you.
    
  #### **Instead**
Write boring code. If you're proud of how clever it is, it's probably too clever.

---
  #### **Name**
Cargo Cult Patterns
  #### **Description**
Using patterns because "that's how it's done"
  #### **Why**
    Repository pattern for a 3-table app. CQRS for a blog. Event sourcing for
    a todo list. Patterns exist to solve specific problems. Using them without
    the problem adds complexity without benefit.
    
  #### **Instead**
Understand WHY a pattern exists. Apply it when you have the problem it solves.

---
  #### **Name**
Comment Rot
  #### **Description**
Comments that no longer match the code
  #### **Why**
    Comments aren't checked by the compiler. When code changes, comments often
    don't. Misleading comments are worse than no comments - they actively
    deceive the reader.
    
  #### **Instead**
Keep comments minimal and focused on why. Update or delete when code changes.

---
  #### **Name**
Boolean Parameters
  #### **Description**
Functions with true/false parameters that hide meaning
  #### **Why**
    What does `createUser(data, true, false)` do? You have to read the function
    signature to know. Boolean parameters are code that requires context from
    elsewhere to understand.
    
  #### **Instead**
Use named parameters or options objects. `createUser(data, { sendEmail: true, skipValidation: false })`