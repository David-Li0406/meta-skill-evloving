# Agent Evaluation - Validations

## Single Run Test for Stochastic Agent

### **Id**
single-run-test
### **Severity**
high
### **Type**
regex
### **Pattern**
expect\([^)]*\)\.to|assert\([^)]*\)|should\.
### **Negative Pattern**
forEach|map|for.*of|repeat|times|runs
### **Message**
Single assertion without repeated runs. LLM agents need statistical evaluation.
### **Fix Action**
Run test multiple times and use statistical thresholds
### **Applies To**
  - *.test.ts
  - *.test.js
  - *.spec.ts
  - *.spec.js

## Exact String Match on LLM Output

### **Id**
exact-string-match
### **Severity**
medium
### **Type**
regex
### **Pattern**
expect\([^)]*output[^)]*\)\.toBe\(["'][^"']+["']\)|expect\([^)]*response[^)]*\)\.toEqual\(["']
### **Message**
Exact string matching on LLM output. Will fail with minor wording changes.
### **Fix Action**
Use semantic comparison or behavior detection
### **Applies To**
  - *.test.ts
  - *.test.js
  - *.spec.ts
  - *.spec.js

## Agent Test Without Timeout

### **Id**
no-timeout-in-test
### **Severity**
medium
### **Type**
regex
### **Pattern**
it\s*\([^)]+,\s*async|test\s*\([^)]+,\s*async
### **Negative Pattern**
timeout|jest\.setTimeout|this\.timeout
### **Message**
Async agent test without timeout configuration.
### **Fix Action**
Add timeout: it('test', async () => {...}, 30000)
### **Applies To**
  - *.test.ts
  - *.test.js
  - *.spec.ts
  - *.spec.js

## Missing Adversarial Test Cases

### **Id**
no-adversarial-tests
### **Severity**
medium
### **Type**
regex
### **Pattern**
describe\s*\(["'].*agent
### **Negative Pattern**
adversarial|attack|inject|malicious|edge.?case
### **Message**
Agent test suite without adversarial test cases.
### **Fix Action**
Add adversarial tests for prompt injection, boundary cases
### **Applies To**
  - *.test.ts
  - *.test.js
  - *.spec.ts
  - *.spec.js

## Test Without Baseline Comparison

### **Id**
no-baseline-comparison
### **Severity**
low
### **Type**
regex
### **Pattern**
expect\([^)]*score|accuracy|passRate
### **Negative Pattern**
baseline|previous|threshold|minimum
### **Message**
Metric assertion without baseline comparison.
### **Fix Action**
Compare against established baseline for regression detection
### **Applies To**
  - *.test.ts
  - *.test.js
  - *.spec.ts
  - *.spec.js

## Tests Using Only Mocked LLM

### **Id**
mock-llm-only
### **Severity**
medium
### **Type**
regex
### **Pattern**
mock.*LLM|jest\.mock.*anthropic|jest\.mock.*openai
### **Negative Pattern**
integration|e2e|real.*model
### **Message**
Agent tests only use mocked LLM. Need some real model tests.
### **Fix Action**
Add integration tests with real model for realistic behavior
### **Applies To**
  - *.test.ts
  - *.test.js
  - *.spec.ts
  - *.spec.js

## Missing Latency Requirements

### **Id**
no-latency-tests
### **Severity**
low
### **Type**
regex
### **Pattern**
agent.*test|test.*agent
### **Negative Pattern**
latency|duration|time|performance|p95|p99
### **Message**
Agent tests without latency requirements.
### **Fix Action**
Add latency assertions for production readiness
### **Applies To**
  - *.test.ts
  - *.test.js
  - *.spec.ts
  - *.spec.js

## Missing Token/Cost Tracking in Tests

### **Id**
no-cost-tracking
### **Severity**
low
### **Type**
regex
### **Pattern**
agent.*test|test.*agent
### **Negative Pattern**
token|cost|usage|budget
### **Message**
Agent tests without token/cost tracking.
### **Fix Action**
Track token usage to catch cost regressions
### **Applies To**
  - *.test.ts
  - *.test.js
  - *.spec.ts
  - *.spec.js

## Missing Behavioral Assertions

### **Id**
no-behavioral-contract
### **Severity**
medium
### **Type**
regex
### **Pattern**
agent.*test|test.*agent
### **Negative Pattern**
behavior|contract|should.*not|must.*not|never
### **Message**
Agent tests without behavioral contract assertions.
### **Fix Action**
Add assertions for what agent should and should not do
### **Applies To**
  - *.test.ts
  - *.test.js
  - *.spec.ts
  - *.spec.js

## Hardcoded Expected Output

### **Id**
hardcoded-expected-output
### **Severity**
low
### **Type**
regex
### **Pattern**
expectedOutput\s*[:=]\s*["'][^"']{100,}["']
### **Message**
Long hardcoded expected output. Consider semantic evaluation.
### **Fix Action**
Use semantic comparison or key fact extraction
### **Applies To**
  - *.test.ts
  - *.test.js
  - *.spec.ts
  - *.spec.js