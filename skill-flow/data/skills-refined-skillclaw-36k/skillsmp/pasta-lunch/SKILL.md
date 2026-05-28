---
name: pasta-lunch
description: Detect spaghetti code and propose specific refactoring solutions. Analyzes detected issues and provides concrete code improvements.
---

# Spaghetti Code Detection & Resolution

Detect tangled, complex code using PHPMD metrics, then analyze and propose specific fixes.

## Workflow

### Step 1: Run Detection

```bash
./vendor/bin/pasta-lunch src/
```

Or target specific directories:
```bash
./vendor/bin/pasta-lunch src/Resource,src/Service,src/Domain
```

### Step 2: Identify Priority Targets

Focus on **Mamma Mia!** files first. These are structurally broken and cause:
- Bugs on every change
- Unpredictable side effects
- Impossible to test properly

### Step 3: Analyze and Propose Solutions

For each Mamma Mia! file:

1. **Read the file** to understand the actual code
2. **Identify the root cause** (not just the symptom)
3. **Propose specific refactoring** with concrete code

## Metrics and Thresholds

| Metric | Piccolo | Medio | Grande | Mamma Mia! |
|--------|---------|-------|--------|------------|
| CyclomaticComplexity (CC) | ≤10 | 11-15 | 16-20 | 21+ |
| NPathComplexity | ≤100 | 101-200 | 201-500 | 501+ |
| CouplingBetweenObjects (CBO) | ≤10 | 11-15 | 16-20 | 21+ |
| ExcessiveClassComplexity (ECC) | ≤50 | 51-80 | 81-120 | 121+ |
| ExcessiveMethodLength | ≤50 | 51-100 | 101-150 | 151+ |
| ExcessiveParameterList | ≤5 | 6-10 | 11-15 | 16+ |
| TooManyFields | ≤10 | 11-15 | 16-20 | 21+ |
| TooManyPublicMethods | ≤10 | 11-15 | 16-20 | 21+ |

## Issue Analysis Guide

When analyzing a detected issue, provide:

### 1. Problem Explanation
- What the metric measures
- Why this value is problematic
- Link to documentation: `https://koriym.github.io/pasta-lunch/issues/en/{issue-name}`

### 2. Root Cause Analysis
- Read the actual file
- Identify why the metric is high
- Common patterns:
  - **High CBO**: Class doing too many things, needs responsibility extraction
  - **High CC**: Too many conditionals, needs strategy pattern or early returns
  - **High NPath**: Deep nesting, needs guard clauses
  - **High ECC**: God class, needs splitting
  - **TooManyFields**: DTO bloat, needs decomposition
  - **ExcessiveParameterList**: Missing value object or configuration object

### 3. Concrete Refactoring Proposal
- Show before/after code
- Explain the transformation
- Keep changes minimal and focused

## Refactoring Patterns

### High CBO: Extract Service

```php
// Before: CBO=22 - Resource doing everything
class Import extends ResourceObject
{
    public function __construct(
        private readonly DbInterface $db,
        private readonly CacheInterface $cache,
        private readonly LoggerInterface $logger,
        private readonly ValidatorInterface $validator,
        // ... 18 more dependencies
    ) {}

    public function onPost(array $data): static
    {
        // 200 lines of import logic
    }
}

// After: CBO=2 - Resource delegates to Service
class Import extends ResourceObject
{
    public function __construct(
        private readonly ImportService $service,
    ) {}

    public function onPost(array $data): static
    {
        $this->body = $this->service->import($data);
        return $this;
    }
}
```

### High CC: Strategy Pattern

```php
// Before: CC=18
public function process(string $type, array $data): Result
{
    if ($type === 'order') {
        // 30 lines
    } elseif ($type === 'refund') {
        // 25 lines
    } elseif ($type === 'exchange') {
        // 35 lines
    }
    // ... more branches
}

// After: CC=2
public function process(string $type, array $data): Result
{
    $processor = $this->processorFactory->create($type);
    return $processor->process($data);
}
```

### High NPath: Guard Clauses

```php
// Before: NPath=512
public function calculate(Order $order): int
{
    if ($order->hasItems()) {
        if ($order->isValid()) {
            if ($order->customer !== null) {
                if ($order->customer->hasDiscount()) {
                    // calculation with discount
                } else {
                    // calculation without discount
                }
            }
        }
    }
    return 0;
}

// After: NPath=8
public function calculate(Order $order): int
{
    if (!$order->hasItems()) {
        return 0;
    }
    if (!$order->isValid()) {
        return 0;
    }
    if ($order->customer === null) {
        return 0;
    }

    $base = $this->calculateBase($order);
    return $order->customer->hasDiscount()
        ? $this->applyDiscount($base, $order->customer)
        : $base;
}
```

### TooManyFields: Decompose DTO

```php
// Before: 30 fields
class Article
{
    public function __construct(
        public readonly int $id,
        public readonly string $title,
        public readonly string $body,
        public readonly string $authorName,
        public readonly string $authorEmail,
        public readonly string $authorBio,
        public readonly string $metaTitle,
        public readonly string $metaDescription,
        public readonly array $metaKeywords,
        // ... 21 more fields
    ) {}
}

// After: Composed of value objects
class Article
{
    public function __construct(
        public readonly int $id,
        public readonly string $title,
        public readonly string $body,
        public readonly Author $author,
        public readonly Meta $meta,
        public readonly PublishInfo $publishInfo,
    ) {}
}
```

### ExcessiveParameterList: Parameter Object

```php
// Before: 12 parameters
public function createUser(
    string $name,
    string $email,
    string $password,
    string $phone,
    string $address,
    string $city,
    string $country,
    string $postalCode,
    bool $newsletter,
    bool $terms,
    ?string $referral,
    ?string $coupon,
): User

// After: Parameter object
public function createUser(CreateUserRequest $request): User
```

## Output Format

When presenting results:

```markdown
## 🍝 Spaghetti Code Detection

### Summary
- Total files: 150
- Piccolo: 120 (80%)
- Medio: 15 (10%)
- Grande: 10 (6.7%)
- Mamma Mia!: 5 (3.3%)

### Mamma Mia! Files (Immediate Action Required)

#### 1. Service/OrderProcessor.php

**Detected Issues:**
- CyclomaticComplexity: 28 (threshold: 10) in `processOrder()`
- NPathComplexity: 1024 (threshold: 100) in `processOrder()`
- CouplingBetweenObjects: 22 (threshold: 10)

**Root Cause:**
[After reading the file, explain what's actually wrong]

**Proposed Fix:**
[Show concrete refactoring code]

📖 Reference: [CyclomaticComplexity](https://koriym.github.io/pasta-lunch/issues/en/cyclomatic-complexity)
```

## References

- [Issue Types (EN)](https://koriym.github.io/pasta-lunch/issues/en/)
- [Issue Types (JA)](https://koriym.github.io/pasta-lunch/issues/ja/)
- [PHPMD Code Size Rules](https://phpmd.org/rules/codesize.html)
- [PHPMD Design Rules](https://phpmd.org/rules/design.html)
