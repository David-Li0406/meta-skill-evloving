# Code Quality - Sharp Edges

## Abstraction Addiction - Layers Upon Layers

### **Id**
abstraction-addiction
### **Severity**
critical
### **Situation**
  You want to add a simple feature. Should take 20 lines. But first you need
  to add an interface. Then an implementation. Then register it in DI. Then
  add a factory. Three hours later, you've added 200 lines across 8 files
  for what should have been a 20-line change.
  
### **Why**
  Abstractions have cost. Every layer adds cognitive overhead, places to look,
  and potential bugs. "Just in case" abstractions are premature optimization
  for change that may never come. Simplicity today beats flexibility you'll
  never use.
  
### **Solution**
  1. Ask: "What problem does this abstraction solve TODAY?"
     - If answer is "future flexibility" - you're probably wrong
     - If answer is "testability" - consider if you really can't test without it
     - If answer is "separation of concerns" - is the concern real or imagined?
  
  2. Start without the abstraction:
     - Write the simplest code that works
     - Add abstraction when you feel pain, not before
     - "Three strikes" rule: abstract on third occurrence
  
  3. Measure abstraction cost:
     - How many files to change for a simple feature?
     - Can a new developer understand it in 15 minutes?
     - How deep is the call stack for a simple operation?
  
### **Symptoms**
  - Simple features require changes in 5+ files
  - New developers take weeks to contribute
  - Abstractions have only one implementation
  - Interface + Impl pattern everywhere
### **Detection Pattern**
interface I\w+|Factory|Provider|Strategy|Handler

## DRY Obsession - Wrong Abstraction Is Worse Than Duplication

### **Id**
dry-obsession
### **Severity**
high
### **Situation**
  You see code that looks similar in two places. You immediately extract it
  into a shared function. Later, the two uses diverge. Now you're adding
  parameters, conditions, and flags to handle both cases. The "shared" code
  becomes more complex than two separate implementations would be.
  
### **Why**
  DRY (Don't Repeat Yourself) assumes the duplication is meaningful - that
  the two pieces should stay in sync. But sometimes code looks the same
  accidentally, or the similarities are superficial. The wrong abstraction
  couples things that should be independent.
  
### **Solution**
  1. Apply the "Rule of Three":
     - First duplication: Write it
     - Second duplication: Note it
     - Third duplication: Now abstract (you understand the pattern)
  
  2. Before extracting, ask:
     - If I change one, should the other always change?
     - Are these truly the same concept, or coincidentally similar?
     - Is the shared code stable, or still evolving?
  
  3. If abstraction becomes complex:
     - Too many parameters? Split it back
     - Too many conditionals? Split it back
     - Hard to name? It's probably not a coherent concept
  
### **Symptoms**
  - Shared function with 5+ parameters
  - Boolean flags controlling behavior branches
  - Comments explaining which caller uses which mode
  - Afraid to change shared code due to unknown callers
### **Detection Pattern**
if\s*\(.*mode.*===|\|\|.*default|options\.|config\.

## Naming Lies - Names That Mislead

### **Id**
naming-lies
### **Severity**
high
### **Situation**
  Function is called `validateUser` but actually creates a user if validation
  passes. Variable is called `users` but only contains active users.
  Method is `save` but also sends notifications. The name promises one thing,
  the code does another.
  
### **Why**
  Names are the primary documentation. When reading code, you trust names to
  tell you what things do. Misleading names are worse than unhelpful names -
  they actively deceive. Every reader will be confused or make wrong assumptions.
  
### **Solution**
  1. Names must be honest about side effects:
     - `validateAndCreateUser` if it creates
     - `saveAndNotify` if it notifies
     - Or better: split into separate functions
  
  2. Names must accurately describe contents:
     - `activeUsers` not `users` if filtered
     - `pendingOrders` not `orders` if filtered
     - Include the constraint in the name
  
  3. Maintain name accuracy during changes:
     - Changed what function does? Change the name
     - Added side effects? Update the name or split
     - If name is hard to change (API), consider new function
  
### **Symptoms**
  - This function does more than its name suggests
  - Comments explaining what function really does
  - Bugs from callers assuming name matches behavior
  - Names that require reading implementation to understand
### **Detection Pattern**
validate.*create|save.*notify|get.*update|check.*modify

## Primitive Obsession - Stringly Typed Code

### **Id**
primitive-obsession
### **Severity**
medium
### **Situation**
  User ID is a string. Order ID is a string. Product ID is a string. Email
  is a string. Status is a string. You accidentally pass an order ID where
  user ID is expected. Code runs, data is corrupted, good luck debugging.
  
### **Why**
  Primitives don't carry type information. The compiler/runtime can't tell
  the difference between a user ID string and an email string. Mistakes
  aren't caught until runtime, often much later when data is already corrupt.
  
### **Solution**
  1. Create types for domain concepts:
     ```typescript
     type UserId = string & { readonly brand: unique symbol };
     type OrderId = string & { readonly brand: unique symbol };
  
     function getUser(id: UserId): User { }
     // getUser(orderId) - TypeScript error!
     ```
  
  2. Use enums or literal types for statuses:
     ```typescript
     type OrderStatus = 'pending' | 'paid' | 'shipped' | 'delivered';
     // Not: status: string
     ```
  
  3. Create value objects for complex primitives:
     ```typescript
     class Email {
       constructor(public readonly value: string) {
         if (!value.includes('@')) throw new Error('Invalid email');
       }
     }
     ```
  
### **Symptoms**
  - Many parameters of same primitive type
  - Bugs from swapped arguments
  - Validation repeated in multiple places
  - Magic strings for statuses
### **Detection Pattern**
string.*string.*string|id:\s*string|status:\s*string

## Hidden Dependencies - Implicit Coupling

### **Id**
hidden-dependencies
### **Severity**
high
### **Situation**
  Function works in production but fails in tests. Turns out it depends on
  a global variable, environment state, or another service that's initialized
  elsewhere. The function signature doesn't reveal its true dependencies.
  
### **Why**
  Hidden dependencies make code unpredictable. You can't understand what a
  function needs by looking at its signature. Testing requires replicating
  invisible state. Refactoring risks breaking unknown dependencies.
  
### **Solution**
  1. Make dependencies explicit in signature:
     ```typescript
     // BAD: Hides dependency
     function getPrice(productId) {
       const discount = globalConfig.discount; // Hidden!
       return fetchProduct(productId).price * (1 - discount);
     }
  
     // GOOD: Explicit dependency
     function getPrice(productId, discount) {
       return fetchProduct(productId).price * (1 - discount);
     }
     ```
  
  2. Inject rather than import singletons:
     - Pass the database connection, don't import it
     - Pass the logger, don't reach for global
     - Tests can then provide fakes
  
  3. If global state is necessary:
     - Document it prominently
     - Initialize in one obvious place
     - Provide test utilities to set up state
  
### **Symptoms**
  - Function fails in tests but works in production
  - Need to read implementation to understand requirements
  - Side effects not apparent from signature
  - Did you initialize X first?
### **Detection Pattern**
process\.env|global\.|window\.|singleton|getInstance

## Deep Nesting - Arrow Code

### **Id**
deep-nesting
### **Severity**
medium
### **Situation**
  You're reading code and hit 5 levels of indentation. Each level is a
  condition or loop. By the time you reach the actual logic, you've
  forgotten the context of the outer levels. Code forms an arrow shape
  pointing right.
  
### **Why**
  Human working memory is limited. Deep nesting requires holding multiple
  conditions in mind simultaneously. It's cognitively expensive to read
  and easy to miss edge cases.
  
### **Solution**
  1. Use guard clauses (return early):
     ```typescript
     // BAD: Deep nesting
     if (user) {
       if (user.active) {
         if (user.hasPermission) {
           // Do the thing
         }
       }
     }
  
     // GOOD: Guard clauses
     if (!user) return;
     if (!user.active) return;
     if (!user.hasPermission) return;
     // Do the thing
     ```
  
  2. Extract complex conditions:
     ```typescript
     const canProcessOrder = user && order && order.isPaid;
     if (!canProcessOrder) return;
     ```
  
  3. Extract nested loops into functions:
     ```typescript
     // BAD: Nested loops
     for (const user of users) {
       for (const order of user.orders) {
         for (const item of order.items) { }
       }
     }
  
     // GOOD: Extract
     for (const user of users) {
       processUserOrders(user);
     }
     ```
  
### **Symptoms**
  - Code forms arrow shape (points right)
  - More than 3 levels of indentation
  - Long functions with many conditions
  - Bugs in edge cases (conditions not met)
### **Detection Pattern**
\{\s*\{\s*\{\s*\{|if.*if.*if.*if

## God Function - Does Everything

### **Id**
god-function
### **Severity**
high
### **Situation**
  One function is 500 lines. It validates, transforms, saves, sends emails,
  updates analytics, and logs. Everyone is afraid to touch it. New features
  keep getting added because it's the only place that "knows" everything.
  
### **Why**
  Large functions are hard to understand, test, and modify. They accumulate
  responsibilities over time because it's easier to add a line than extract
  a function. Each addition makes the next addition harder.
  
### **Solution**
  1. Single responsibility at function level:
     - Can you describe it without "and"?
     - "Validates order AND saves AND sends email" = split
  
  2. Extract when you see clear boundaries:
     - Validation is separate from persistence
     - Persistence is separate from notification
     - Each becomes its own testable unit
  
  3. For legacy god functions:
     - Don't rewrite all at once
     - Extract one responsibility at a time
     - Test before and after each extraction
  
### **Symptoms**
  - Function more than 50-100 lines
  - Multiple distinct responsibilities
  - Many local variables
  - Nobody touches this function
### **Detection Pattern**
function.*\{[\s\S]{2000,}\}

## Magic Values - Numbers and Strings Without Names

### **Id**
magic-values
### **Severity**
medium
### **Situation**
  Code has `if (status === 3)` or `setTimeout(callback, 86400000)`. What
  does 3 mean? What's 86400000 milliseconds? You have to trace back to
  comments or documentation (if they exist) to understand.
  
### **Why**
  Numbers and strings without context are meaningless. They force readers
  to look elsewhere for meaning. When the value changes, you might miss
  some occurrences. When requirements change, the meaning is forgotten.
  
### **Solution**
  1. Extract to named constants:
     ```typescript
     // BAD
     if (status === 3) { }
     setTimeout(callback, 86400000);
  
     // GOOD
     const ORDER_STATUS_SHIPPED = 3;
     if (status === ORDER_STATUS_SHIPPED) { }
  
     const ONE_DAY_MS = 24 * 60 * 60 * 1000;
     setTimeout(callback, ONE_DAY_MS);
     ```
  
  2. Use enums for related constants:
     ```typescript
     enum OrderStatus {
       Pending = 1,
       Paid = 2,
       Shipped = 3,
     }
     ```
  
  3. Exception: Obvious values in context:
     - `array[0]` - first element is clear
     - `percentage / 100` - 100 is obvious here
  
### **Symptoms**
  - Numbers without explanation
  - Same number appears in multiple places
  - Comments like "3 means shipped"
  - Bugs from using wrong number
### **Detection Pattern**
===\s*\d{2,}|setTimeout.*\d{5,}|\d{4,}\s*\*

## Mixed Abstraction Levels - High and Low Together

### **Id**
mixed-abstraction-levels
### **Severity**
medium
### **Situation**
  Function starts with high-level business logic, then drops into string
  manipulation, then back to business logic, then database query details.
  Reading it requires constantly shifting mental context between what and
  how.
  
### **Why**
  Code at consistent abstraction levels is easier to understand. When you
  mix high-level intent with low-level implementation, readers must context-
  switch constantly. The "what" gets buried in the "how".
  
### **Solution**
  1. Keep functions at consistent level:
     ```typescript
     // BAD: Mixed levels
     function processOrder(order) {
       validateOrder(order);
       const totalCents = order.items.reduce((sum, i) => sum + i.price * 100, 0);
       await db.query('INSERT INTO orders...', [totalCents]);
       await sendEmail(order.user.email);
     }
  
     // GOOD: Consistent high level
     function processOrder(order) {
       validateOrder(order);
       const total = calculateTotal(order.items);
       await saveOrder(order, total);
       await notifyUser(order.user);
     }
     ```
  
  2. Extract low-level details into well-named functions:
     - The name documents intent
     - The implementation handles detail
     - Readers can drill down when needed
  
  3. Organize by abstraction level:
     - High-level orchestration at top
     - Implementation details at bottom or in separate files
  
### **Symptoms**
  - Business logic mixed with SQL strings
  - High-level functions with string parsing
  - Hard to understand intent
  - Implementation details obscure purpose
### **Detection Pattern**
\bfetch\b.*\bJSON\b|\bquery\b.*\bvalidate\b