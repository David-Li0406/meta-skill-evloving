# Rule Engine Project Plan

## Overview
The goal of this phase is to integrate **Apache Drools** to provide a flexible, scalable Rule Engine for the Darpan component. This will replace the rigid mapping entities and allow users to define complex validation logic using natural language-like syntax.

## Goals
1.  **Flexibility**: Support complex logic (AND/OR, grouping, mathematical operations) without hardcoding.
2.  **Usability**: Users define rules in readable sentences.
3.  **Extensibility**: Easy to add new rule types or actions in the backend.
4.  **Performance**: Efficiently process large datasets using Drools' RETE algorithm.

## System Design

### Data Model
New entities will be introduced to store rule definitions:

*   **RuleSet**: Represents a group of rules (e.g., "Shopify vs OMS Validation").
*   **Rule**: A single logical check.
    *   `ruleText`: "If cancelledAt is not NULL and status is Cancelled..."
    *   `logic`: The internal representation (DRL or expression) used by the engine.

### Service Architecture
The core service `executeRules` will:
1.  **Load Rules**: Fetch all active rules for the requested `RuleSet`.
2.  **Compile Logic**: Dynamically generate a Drools Knowledge Base (caching this for performance).
3.  **Load Data**: Accept the input dataset (List of Maps).
4.  **Execute**:
    *   Insert each data item as a "Fact" into the Drools session.
    *   Fire all rules.
5.  **Collect Results**: Each rule firing will add a result object (passed/failed/info) to a global results list.
6.  **Return**: The final list of results is returned as JSON.

### Integration with Drools
We will use the generic `Map<String, Object>` interface so that we don't need to generate POJOs for every dataset. Drools supports accessing Map keys directly in rules (e.g., `this["statusId"] == "Cancelled"`).

## Work Breakdown

### Phase 1: Foundation (Current)
- [ ] Add Drools dependencies to `build.gradle`.
- [ ] Create `RuleSet` and `Rule` entities.
- [ ] Deprecate `ReconciliationMapping` entities.

### Phase 2: Core Service Implementation
- [ ] Implement `RuleServices.groovy` to handle Drools initialization.
- [ ] Create a "Rule Compiler" that converts the `Rule` entity data into a valid DRL file string.
- [ ] Implement the execution loop (insert facts -> fire rules -> collect results).

### Phase 3: Rule Logic Parsing
- [ ] Develop a parser to translate "Human Readable" sentences into DRL conditions.
    - *Example*: "statusId is 'Cancelled'" -> `this["statusId"] == "Cancelled"`
- [ ] Support standard operators: `is`, `is not`, `contains`, `> usage`, etc.

### Phase 4: User Interface
- [ ] Create screens to Manage RuleSets (Create/Edit/Delete).
- [ ] Create a Rule Editor (Add rules to a set, reorder them).
- [ ] Create a "Test Bench" to run a RuleSet against a pasted JSON sample.

## Migration Guide
Users currently using `ReconciliationMapping` should prepare to migrate. The old mapping entities will be marked as deprecated but will remain available for backward compatibility for one release cycle.
