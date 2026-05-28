---
name: contract-validation
description: Validate agent input/output contracts to ensure correct execution
---

# Contract Validation Skill

This skill teaches agents how to validate their input and output contracts using the Contract-First design pattern.

## When to Use

Use this skill when:
- Starting agent execution (validate input contract)
- Completing agent execution (validate output contract)
- Debugging failed agent executions
- Verifying state.json updates

## Core Concepts

### Agent Contract Structure

Every agent must define:
1. **Input Contract**: What the agent needs to start
2. **Output Contract**: What the agent must produce
3. **Validation Rules**: How to verify correctness

### Contract Validation Flow

```
1. Read agent contract definition
2. Gather input data from specified sources
3. Validate input contract
4. Execute agent logic
5. Validate output contract
6. Update state.json with results
```

## How to Use

### Step 1: Define Your Contract

Create a contract definition file (e.g., `contracts/tdd.json`):

```json
{
  "agent": "tdd",
  "description": "TDD Implementation Agent",
  "method": {
    "name": "Test-Driven Development",
    "description": "Red → Green → Refactor"
  },
  "input_contract": {
    "required": [
      {
        "field_name": "requirements",
        "description": "Requirements document",
        "type": "string",
        "validation": ["fileExists"]
      },
      {
        "field_name": "architecture",
        "description": "Architecture design document",
        "type": "string",
        "validation": ["fileExists"]
      }
    ],
    "optional": [
      {
        "field_name": "existing_tests",
        "description": "Existing test files",
        "type": "array"
      }
    ],
    "source": [
      {
        "location": "outputs/pm.md",
        "description": "Requirements from PM agent"
      },
      {
        "location": "outputs/arch.md",
        "description": "Architecture from Architect agent"
      }
    ]
  },
  "output_contract": {
    "required": [
      {
        "field_name": "test_files",
        "description": "Test files created",
        "type": "array",
        "validation": ["minItems:1"]
      },
      {
        "field_name": "implementation_files",
        "description": "Implementation files modified",
        "type": "array",
        "validation": ["minItems:1"]
      },
      {
        "field_name": "tests_status",
        "description": "Test execution status",
        "type": "string",
        "validation": ["pattern:^\\d+/\\d+ passed$"]
      }
    ],
    "destination": [
      "tests/",
      "src/",
      "outputs/tdd.md"
    ]
  }
}
```

### Step 2: Validate Input Before Execution

Before starting your agent work:

1. **Read your contract**:
```bash
Read the contract file: contracts/<agent-name>.json
```

2. **Gather input data**:
```typescript
// Check each source location specified in input_contract.source
const inputData = {
  requirements: await Read("outputs/pm.md"),
  architecture: await Read("outputs/arch.md"),
  existing_tests: await Glob("tests/**/*.test.ts")
};
```

3. **Validate input**:
```typescript
// Use the ContractValidator from lib/contract-validator.ts
import { ContractValidator } from '${CLAUDE_PLUGIN_ROOT}/lib/contract-validator.js';

const validationResult = ContractValidator.validateInput(contract, {
  agent: 'tdd',
  task_id: 'TASK-123',
  phase: 'execution',
  input_data: inputData
});

if (!validationResult.valid) {
  // Report errors and stop
  console.log(ContractValidator.formatValidationResult(validationResult, 'input'));
  throw new Error('Input contract validation failed');
}
```

### Step 3: Validate Output After Execution

After completing your work:

1. **Collect output data**:
```typescript
const outputData = {
  test_files: await Glob("tests/**/*.test.ts"),
  implementation_files: await Glob("src/**/*.ts"),
  tests_status: "15/15 passed",
  complexity_actual: 13
};
```

2. **Validate output**:
```typescript
const validationResult = ContractValidator.validateOutput(contract, {
  agent: 'tdd',
  task_id: 'TASK-123',
  phase: 'execution',
  input_data: inputData,
  output_data: outputData
});

if (!validationResult.valid) {
  console.log(ContractValidator.formatValidationResult(validationResult, 'output'));
  // Decide: fix issues or report to user
}
```

3. **Update state.json**:
```typescript
import { StateManager } from '${CLAUDE_PLUGIN_ROOT}/lib/state-manager.js';

const stateManager = new StateManager(process.cwd());
await stateManager.recordExecutionAgent('tdd', validationResult);
```

## Validation Rules Reference

### Built-in Validation Rules

- `minLength:N` - String must have at least N characters
- `maxLength:N` - String must have at most N characters
- `minItems:N` - Array must have at least N items
- `pattern:REGEX` - String must match regex pattern
- `fileExists` - File/directory must exist

### Custom Validation

For complex validation, implement custom logic before calling the validator:

```typescript
// Example: Validate test coverage
if (outputData.coverage < 80) {
  throw new Error('Test coverage must be >= 80%');
}
```

## Common Patterns

### Pattern 1: Sequential Agent Workflow

```typescript
// Agent A validates output
const resultA = ContractValidator.validateOutput(contractA, contextA);
await stateManager.recordPlanningAgent('pm', 'outputs/pm.md', resultA);

// Agent B validates input (depends on A's output)
const inputB = {
  requirements: await Read('outputs/pm.md')
};
const resultB = ContractValidator.validateInput(contractB, {
  ...contextB,
  input_data: inputB
});
```

### Pattern 2: Error Recovery

```typescript
const validationResult = ContractValidator.validateOutput(contract, context);

if (!validationResult.valid) {
  if (validationResult.errors.some(e => e.field === 'tests_status')) {
    // Fix failing tests
    await fixFailingTests();
    // Re-validate
    const retryResult = ContractValidator.validateOutput(contract, context);
  }
}
```

## Debugging

### Check Validation Details

```typescript
console.log(JSON.stringify(validationResult, null, 2));
```

### Common Issues

1. **Missing required field**: Check if source file exists and contains expected data
2. **Type mismatch**: Verify data structure matches contract definition
3. **Validation rule failed**: Check actual value against rule pattern

## Best Practices

1. **Validate early**: Check input before doing any work
2. **Validate completely**: Don't skip output validation
3. **Report clearly**: Use `formatValidationResult()` for human-readable output
4. **Update state**: Always record validation results in state.json
5. **Handle errors gracefully**: Decide whether to fix, retry, or escalate to user

## Example: Complete Agent Execution

```typescript
import { ContractValidator } from '${CLAUDE_PLUGIN_ROOT}/lib/contract-validator.js';
import { StateManager } from '${CLAUDE_PLUGIN_ROOT}/lib/state-manager.js';

async function executeTDDAgent(taskId: string) {
  // 1. Load contract
  const contract = JSON.parse(await Read('contracts/tdd.json'));

  // 2. Gather and validate input
  const inputData = {
    requirements: await Read('outputs/pm.md'),
    architecture: await Read('outputs/arch.md')
  };

  const inputValidation = ContractValidator.validateInput(contract, {
    agent: 'tdd',
    task_id: taskId,
    phase: 'execution',
    input_data: inputData
  });

  if (!inputValidation.valid) {
    throw new Error('Input validation failed:\\n' +
      ContractValidator.formatValidationResult(inputValidation, 'input'));
  }

  // 3. Execute TDD workflow
  // ... (Red → Green → Refactor)

  // 4. Validate output
  const outputData = {
    test_files: await Glob('tests/**/*.test.ts'),
    implementation_files: await Glob('src/**/*.ts'),
    tests_status: '15/15 passed'
  };

  const outputValidation = ContractValidator.validateOutput(contract, {
    agent: 'tdd',
    task_id: taskId,
    phase: 'execution',
    input_data: inputData,
    output_data: outputData
  });

  if (!outputValidation.valid) {
    throw new Error('Output validation failed:\\n' +
      ContractValidator.formatValidationResult(outputValidation, 'output'));
  }

  // 5. Update state
  const stateManager = new StateManager(process.cwd());
  await stateManager.recordExecutionAgent('tdd', outputValidation);

  console.log('✅ TDD agent completed successfully');
}
```

## Integration with jj

Contract validation results are also recorded in jj commit metadata:

```bash
jj describe -m "$(cat <<'EOF'
@tdd completed

{
  "agent": "tdd",
  "input_contract_validation": {
    "requirements": "✓ found",
    "architecture": "✓ found"
  },
  "output_contract_validation": {
    "test_files": "✓ 15 files created",
    "tests_status": "✓ 15/15 passed"
  }
}
EOF
)"
```

This creates a permanent audit trail of contract validations in version control.
