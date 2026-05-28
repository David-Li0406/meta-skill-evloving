# Testing LLM Applications

Testing LLM applications requires different strategies than traditional software testing due to non-deterministic outputs and cost considerations.

## Testing Pyramid for LLM Apps

```
         /\
        /  \  E2E Tests (few)
       /----\  Full pipeline with real LLM
      /      \
     /--------\  Integration Tests (some)
    / Real LLM  \  Module tests with real API
   /   or VCR    \
  /--------------\  Unit Tests (many)
 /  Mocked LLM    \  Logic tests with mocked responses
/------------------\
```

## Unit Testing (Mocked LLM)

### Why Mock?
- Fast execution (no API calls)
- Deterministic results
- No cost
- Test edge cases easily

### Mock Patterns

```
Test: EmailClassifier
  Setup:
    mock_predictor = Mock()
    mock_predictor.forward.returns({
      category: "technical",
      confidence: 0.95
    })
    classifier = EmailClassifier(predictor: mock_predictor)

  Test "returns classification":
    result = classifier.forward(
      subject: "Login issue",
      body: "Can't access account"
    )

    assert result.category == "technical"
    assert mock_predictor.forward.called_once()
```

### Testing Module Logic

```
Test: SupportRouter
  Test "routes technical to technical handler":
    mock_classifier = Mock(returns: { category: "technical" })
    mock_tech_handler = Mock(returns: { response: "..." })
    mock_billing_handler = Mock()

    router = SupportRouter(
      classifier: mock_classifier,
      technical_handler: mock_tech_handler,
      billing_handler: mock_billing_handler
    )

    router.forward(ticket)

    assert mock_tech_handler.called_once()
    assert mock_billing_handler.not_called()
```

## Integration Testing (Real LLM)

### Why Use Real LLM?
- Verify actual model behavior
- Test prompt effectiveness
- Catch prompt regressions

### Recording/Playback (VCR Pattern)

```
Test: EmailClassifier (integration)
  Setup:
    # First run: records responses
    # Subsequent runs: plays back recordings
    with vcr.use_cassette("email_classification"):
      classifier = EmailClassifier()

  Test "classifies technical emails":
    result = classifier.forward(
      subject: "Password reset not working",
      body: "I clicked the link but nothing happens"
    )

    assert result.category == "technical"
```

### Deterministic Settings

```
Configure for tests:
  temperature: 0.0      # No randomness
  seed: 12345           # Fixed seed (if supported)
  model: "gpt-4o-mini"  # Consistent model
```

## Property-Based Testing

### Type Validation

```
Test: OutputTypes
  Repeat 10 times:
    result = classifier.forward(random_email())

    assert result.category in ["technical", "billing", "general"]
    assert 0.0 <= result.confidence <= 1.0
    assert isinstance(result.reasoning, str)
```

### Constraint Validation

```
Test: SummaryLength
  inputs = [short_doc, medium_doc, long_doc]

  for doc in inputs:
    result = summarizer.forward(doc, max_words: 100)

    assert word_count(result.summary) <= 100
```

## Evaluation Testing

### Golden Dataset

Maintain a set of inputs with expected outputs:

```
golden_examples = [
  {
    input: { subject: "Can't login", body: "..." },
    expected: { category: "technical" }
  },
  {
    input: { subject: "Billing question", body: "..." },
    expected: { category: "billing" }
  },
  ...
]

Test: Accuracy
  correct = 0
  for example in golden_examples:
    result = classifier.forward(example.input)
    if result.category == example.expected.category:
      correct += 1

  accuracy = correct / len(golden_examples)
  assert accuracy >= 0.90  # 90% threshold
```

### Regression Testing

```
Test: NoRegressions
  baseline_accuracy = 0.92  # From last release

  current_accuracy = evaluate(classifier, test_set)

  # Alert if accuracy drops
  assert current_accuracy >= baseline_accuracy - 0.02
```

## Edge Case Testing

### Empty/Null Inputs

```
Test: HandlesEmptyInput
  result = classifier.forward(subject: "", body: "")

  # Should not crash, return sensible default
  assert result.category in valid_categories
```

### Long Inputs

```
Test: HandlesLongInput
  long_text = "word " * 10000  # Very long

  result = summarizer.forward(long_text)

  # Should truncate or handle gracefully
  assert result.summary is not None
```

### Special Characters

```
Test: HandlesSpecialCharacters
  inputs = [
    "Email with émojis 🎉",
    "SQL injection'; DROP TABLE--",
    "Unicode: 中文 العربية",
    "<script>alert('xss')</script>"
  ]

  for input in inputs:
    result = classifier.forward(subject: input, body: input)
    # Should handle without crashing
    assert result is not None
```

## Cost-Aware Testing

### Test Budget

```
Config:
  test_budget:
    daily_limit: $10
    per_test_limit: $0.10

before_each_test:
  if daily_spend >= daily_limit:
    skip("Budget exhausted")
```

### Tiered Testing

```
# Fast tests (mocked): Run always
# Integration tests (real LLM): Run on PR
# Full evaluation: Run nightly

CI Pipeline:
  on_commit:
    run: unit_tests  # Mocked, free, fast

  on_pr:
    run: unit_tests
    run: integration_tests  # Real LLM, limited

  nightly:
    run: full_evaluation  # Full test suite
```

## Prompt Regression Testing

### Snapshot Testing

```
Test: PromptSnapshot
  prompt = classifier.build_prompt(sample_input)

  # Compare to saved snapshot
  assert prompt == load_snapshot("classifier_prompt")

  # Update snapshot when intentionally changing prompt
```

### A/B Comparison

```
Test: NewPromptPerformance
  old_classifier = Classifier(prompt: old_prompt)
  new_classifier = Classifier(prompt: new_prompt)

  old_score = evaluate(old_classifier, test_set)
  new_score = evaluate(new_classifier, test_set)

  # New prompt should be at least as good
  assert new_score >= old_score
```

## Test Organization

### Directory Structure

```
tests/
├── unit/
│   ├── test_classifier.py
│   ├── test_router.py
│   └── test_summarizer.py
├── integration/
│   ├── test_classifier_integration.py
│   └── cassettes/  # VCR recordings
├── evaluation/
│   ├── test_accuracy.py
│   └── golden_data/
└── fixtures/
    ├── sample_emails.json
    └── sample_documents.json
```

### Test Data Management

```
fixtures/
├── inputs/
│   ├── technical_emails.json
│   ├── billing_emails.json
│   └── edge_cases.json
├── expected/
│   ├── classifications.json
│   └── summaries.json
└── cassettes/
    └── llm_responses/
```

## Continuous Testing

### CI Integration

```
CI Pipeline:

  unit_tests:
    runs: always
    timeout: 5 min
    cost: $0

  integration_tests:
    runs: on PR
    timeout: 15 min
    cost: ~$1

  evaluation:
    runs: nightly
    timeout: 60 min
    cost: ~$10
    alerts: if accuracy < threshold
```

### Monitoring in Production

```
Production Testing:

  shadow_mode:
    # Run new model alongside old
    # Compare outputs without affecting users

  canary_deployment:
    # Route 5% of traffic to new model
    # Monitor metrics before full rollout

  continuous_evaluation:
    # Sample production inputs
    # Evaluate against golden labels
    # Alert on drift
```
