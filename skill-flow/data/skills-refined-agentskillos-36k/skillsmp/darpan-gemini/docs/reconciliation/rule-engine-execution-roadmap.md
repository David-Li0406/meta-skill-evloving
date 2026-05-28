# Rule Engine Detailed Execution Roadmap

This document provides a granular, step-by-step breakdown of the work required to implement the Rule Engine using Apache Drools. It is designed to ensure success by covering every aspect of implementation, from dependencies to UI and verification.

## Phase 1: Foundation & Data Model
**Goal:** Establish the necessary project structure, dependencies, and database schema.

### 1.1. Dependency Management
- [ ] **Update build.gradle**
    - Add `org.drools:drools-core:7.74.1.Final` (or compatible version).
    - Add `org.drools:drools-compiler:7.74.1.Final`.
    - Add `org.kie:kie-api:7.74.1.Final`.
    - **Verification**: Run `./gradlew dependencies` to ensure no conflicts.

### 1.2. Entity Design (Database)
- [ ] **Define RuleSet Entity** (`RuleEntities.xml`)
    - Fields: `ruleSetId` (PK), `ruleSetName`, `description`, `statusId`, `targetEntity` (optional).
    - **Key Management**:
        - `primaryKeyPath`: JSONPath to the unique ID (e.g., `$.id`, `order_id`). Used for tracking results.
        - `explosionPath`: JSONPath to the array to explode (e.g., `$.items`, `line_items`). If null, treats root as list.
    - **Verification**: Check default Moqui entity validation.
- [ ] **Define Rule Entity** (`RuleEntities.xml`)
    - Fields: `ruleId` (PK), `ruleSetId` (FK), `ruleText` (Human readable), `ruleCondition` (Executable DRL/Expression), `errorMessage` (What to show if failed), `severity` (Info/Warn/Error), `sequenceNum`.
    - **Verification**: Verify Foreign Key constraints.
- [ ] **Define RuleExecutionResult Entity** (Optional but recommended for auditing)
    - Fields: `executionId`, `ruleId`, `resultStatus`, `timestamp`, `recordId` (if applicable).
- [ ] **Deprecate Legacy Entities**
    - Edit `MappingEntities.xml`.
    - Add `deprecated="true"` attribute to `ReconciliationMapping` and `ReconciliationMappingMember`.
    - Add descriptions to guide developers to the new entities.

## Phase 2: Core Rule Service Implementation
**Goal:** Create the backend services that load, compile, and execute rules.

### 2.1. Service Definition
- [ ] **Create RuleServices.xml**
    - Define `executeRuleSet`
        - In: `ruleSetId`, `dataList` (List<Map>).
        - Out: `results` (List<Map>).
    - Define `validateRuleSyntax` (for UI validation).

### 2.2. Drools Integration logic (`RuleServices.groovy`)
- [ ] **Method: `getKieBase(ruleSetId)`**
    - Fetch all active `Rule` records for `ruleSetId`.
    - Construct a `StringBuilder` for the DRL file:
        - Header: `package darpan.rules;`
        - Import: `import java.util.Map;`
        - Loop through rules and append:
            ```drools
            rule "Rule_${ruleId}"
            when
                $m : Map( ${ruleCondition} )
            then
                results.add( ["ruleId": "${ruleId}", "status": "FAIL", "data": $m] );
            end
            ```
    - Use `KieHelper` to build the `KieBase` from the string.
    - **Critical**: Implement caching (store `KieBase` in static Map keyed by `ruleSetId`). Provide a way to clear cache on Rule update.

- [ ] **Method: `executeRuleSet`**
    - Validation: Check if `dataList` is empty.
    - Context Setup: Initialize a `results` list global.
    - Session Creation: `kieBase.newKieSession()`.
    - Global Setting: `session.setGlobal("results", resultsList)`.
    - Fact Insertion: Validated batch insertion.
        ```groovy
        for (item in dataList) session.insert(item)
        ```
    - Execution: `session.fireAllRules()`.
    - Return: `resultsList`.

### 2.3. Data Preparation (Spark Integration) - **[NEW]**
- [ ] **Service: `prepareRuleData`**
    - Input: `inputFileLocation`, `ruleSetId`.
    - Logic:
        1. Retrieve `explosionPath` and `primaryKeyPath` from RuleSet.
        2. Read JSON/CSV using Spark.
        3. If `explosionPath` is set:
            - Explode the array column.
            - Flatten the structure (Select `col("*")`).
        4. Convert DataFrame to `List<Map>` for Drools Config.
            - *Optimization*: For huge datasets, process in partitions/batches.

## Phase 3: Rule Parser (The "Science" Part)
**Goal:** Allow users to write "Human" logic that translates to Drools code.

### 3.1. DSL / syntax Definition
- [ ] **Define Supported Grammar**
    - Field access: `field_name` -> `this["field_name"]`
    - Operators:
        - `is` -> `==`
        - `is not` -> `!=`
        - `contains` -> `toString().contains(...)`
        - `is empty` -> `== null || == ""`
    - Logic: `AND` -> `&&`, `OR` -> `||`.

### 3.2. Parser Implementation
- [ ] **Create `RuleParser.groovy`**
    - Method `parseToDrools(String humanRule)`
    - Step 1: Tokenize (split by space/operators).
    - Step 2: Identify variables (words that match schema keys).
    - Step 3: Replace operators with Groovy/Java equivalents.
    - Step 4: Validate syntax (try compiling a dummy expression).
    - **Output**: The condition string ready for insertion into the `when` block.

## Phase 4: User Interface Implementation
**Goal:** Accessible, user-friendly screens for management.

### 4.1. Ruleset Management
- [ ] **Screen: `RuleSetBrowse`**
    - List all RuleSets.
    - Filters: Name, Status.
    - Action: "Create New RuleSet".
- [ ] **Screen: `RuleSetEdit`** (Header)
    - Edit Name, Description.
    - Status transition buttons.

### 4.2. Rule Editor
- [ ] **Screen: `RuleEdit`** (Master-Detail or Inline)
    - List Rules within RuleSet.
    - **Add/Edit Form**:
        - `Rule Text` (TextArea).
        - **"Check Syntax" Button**: Calls `validateRuleSyntax` service to show if it parses correctly.
        - `Error Message` field.
        - `Severity` dropdown.
    - Drag-and-drop reordering (update `sequenceNum`).

### 4.3. Test Bench (Sandbox)
- [ ] **Screen: `RuleTestConsole`**
    - Input: Select `RuleSet`.
    - Input: Text Area for `JSON Sample`.
    - Button: "Test Execute".
    - Output: Grid showing which rules fired for the sample data.

## Phase 5: Verification & Documentation
**Goal:** Ensure reliability and future maintainability.

### 5.1. Automated Testing
- [ ] **Unit Tests (`RuleServicesTests.groovy`)**
    - Test Parser: Verify "A is B" becomes "A == B".
    - Test Engine: Verify facts trigger the correct rules.
    - Test Caching: Verify updating a rule clears the cache for that RuleSet.
- [ ] **Integration Tests**
    - Run against large dataset (10k items) to benchmark performance.

### 5.2. Documentation
- [ ] **User Guide**: How to write rules (Cheat Sheet of operators).
- [ ] **Developer Guide**: How to add new operators to the parser.
- [ ] **API documentation**: Helper services for other teams to consume.

## Success Metrics
- **Flexibility**: Can we write a rule for "If total > 100 AND customer is VIP"?
- **Performance**: Does 10k execution finish in < 2 seconds?
- **Usability**: Can a non-developer create a working rule in < 5 minutes?
