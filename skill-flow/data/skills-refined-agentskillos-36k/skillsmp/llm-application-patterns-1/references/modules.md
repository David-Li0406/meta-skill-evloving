# Module Patterns

Modules encapsulate LLM operations into reusable, composable units. They're the building blocks of LLM applications.

## Basic Module Structure

```
Module: ModuleName
  Initialize:
    # Set up predictors and dependencies
    predictor = Predict(SomeSignature)

  Forward(inputs):
    # Process inputs and return outputs
    return predictor.forward(inputs)
```

## Module Types

### Simple Predictor Wrapper

The most basic module wraps a single predictor:

```
Module: EmailClassifier
  Initialize:
    predictor = Predict(EmailClassificationSignature)

  Forward(email_subject, email_body):
    return predictor.forward(
      email_subject: email_subject,
      email_body: email_body
    )
```

### Chain of Thought Module

For tasks requiring reasoning:

```
Module: MathSolver
  Initialize:
    predictor = ChainOfThought(MathProblemSignature)

  Forward(problem):
    result = predictor.forward(problem: problem)
    # Returns: { reasoning: "...", answer: "..." }
    return result
```

### Multi-Step Pipeline

Chain multiple modules together:

```
Module: DocumentProcessor
  Initialize:
    extractor = EntityExtractor()
    classifier = DocumentClassifier()
    summarizer = DocumentSummarizer()

  Forward(document):
    # Step 1: Extract entities
    entities = extractor.forward(document)

    # Step 2: Classify document type
    classification = classifier.forward(document, entities)

    # Step 3: Generate summary
    summary = summarizer.forward(document, classification)

    return {
      entities: entities,
      classification: classification,
      summary: summary
    }
```

### Conditional Router

Route to different handlers based on classification:

```
Module: SupportRouter
  Initialize:
    classifier = TicketClassifier()
    technical_handler = TechnicalSupportModule()
    billing_handler = BillingSupportModule()
    general_handler = GeneralSupportModule()

  Forward(ticket):
    classification = classifier.forward(ticket)

    switch classification.category:
      case "technical":
        return technical_handler.forward(ticket)
      case "billing":
        return billing_handler.forward(ticket)
      default:
        return general_handler.forward(ticket)
```

### Agent Module

For tasks requiring tool usage:

```
Module: ResearchAgent
  Initialize:
    agent = ReAct(
      signature: ResearchSignature,
      tools: [
        WebSearchTool(),
        WikipediaTool(),
        CalculatorTool()
      ],
      max_iterations: 10
    )

  Forward(question):
    return agent.forward(question: question)
```

## Composition Patterns

### Sequential Composition

```
Module: Pipeline
  Forward(input):
    result = step1.forward(input)
    result = step2.forward(result)
    result = step3.forward(result)
    return result
```

### Parallel Composition

Run multiple modules on the same input:

```
Module: MultiAnalyzer
  Initialize:
    sentiment = SentimentAnalyzer()
    topics = TopicExtractor()
    entities = EntityExtractor()

  Forward(text):
    # Run all in parallel (if supported)
    return {
      sentiment: sentiment.forward(text),
      topics: topics.forward(text),
      entities: entities.forward(text)
    }
```

### Map-Reduce Pattern

Process items individually, then aggregate:

```
Module: BatchProcessor
  Initialize:
    item_processor = ItemAnalyzer()
    aggregator = ResultAggregator()

  Forward(items):
    # Map: process each item
    results = items.map(item => item_processor.forward(item))

    # Reduce: aggregate results
    return aggregator.forward(results)
```

## State Management

### Stateless Modules (Preferred)

```
Module: StatelessClassifier
  # No instance state
  Forward(input):
    return predictor.forward(input)

# Each call is independent
classifier.forward(email1)  # No memory of this
classifier.forward(email2)  # Fresh prediction
```

### Stateful Modules (When Needed)

```
Module: ConversationModule
  Initialize:
    history = []

  Forward(user_message):
    # Include history in context
    result = predictor.forward(
      history: history,
      message: user_message
    )

    # Update history
    history.append({
      user: user_message,
      assistant: result.response
    })

    return result

  Reset():
    history = []
```

### Caching

```
Module: CachedModule
  Initialize:
    cache = {}

  Forward(input):
    cache_key = hash(input)

    if cache_key in cache:
      return cache[cache_key]

    result = predictor.forward(input)
    cache[cache_key] = result
    return result
```

## Error Handling

### Retry Pattern

```
Module: RobustModule
  MAX_RETRIES = 3

  Forward(input):
    for attempt in range(MAX_RETRIES):
      try:
        return predictor.forward(input)
      catch ValidationError:
        if attempt == MAX_RETRIES - 1:
          raise
        sleep(2 ** attempt)  # Exponential backoff
```

### Fallback Pattern

```
Module: FallbackModule
  Initialize:
    primary = PrimaryPredictor()
    fallback = FallbackPredictor()

  Forward(input):
    try:
      return primary.forward(input)
    catch Error:
      log("Primary failed, using fallback")
      return fallback.forward(input)
```

### Graceful Degradation

```
Module: GracefulModule
  Forward(input):
    try:
      full_result = full_analysis.forward(input)
      return full_result
    catch Error:
      # Return partial result instead of failing
      basic_result = basic_analysis.forward(input)
      return {
        ...basic_result,
        degraded: true,
        missing: ["detailed_analysis", "recommendations"]
      }
```

## Testing Modules

### Unit Testing

```
Test: EmailClassifier
  Setup:
    classifier = EmailClassifier()
    configure_test_provider()

  Test "classifies technical emails":
    result = classifier.forward(
      email_subject: "Login broken",
      email_body: "I can't access my account"
    )

    assert result.category == "technical"
    assert result.confidence > 0.7
```

### Integration Testing

```
Test: DocumentPipeline
  Setup:
    pipeline = DocumentProcessor()

  Test "processes document end-to-end":
    result = pipeline.forward(sample_document)

    assert result.entities is not empty
    assert result.classification in valid_categories
    assert result.summary.length < 500
```

### Mock Testing

```
Test: RouterWithMocks
  Setup:
    mock_classifier = Mock(returns: { category: "technical" })
    mock_handler = Mock(returns: { response: "..." })
    router = SupportRouter(
      classifier: mock_classifier,
      technical_handler: mock_handler
    )

  Test "routes to correct handler":
    router.forward(ticket)

    assert mock_classifier.called_once()
    assert mock_handler.called_once()
```

## Best Practices

### 1. Keep Modules Focused

```
Bad:
  Module: DoEverything
    # Classifies, extracts, summarizes, translates...

Good:
  Module: Classifier
  Module: Extractor
  Module: Summarizer
  Module: Pipeline  # Composes the above
```

### 2. Make Dependencies Explicit

```
Bad:
  Module: HiddenDependency
    Forward(input):
      # Uses global config, hidden state, etc.

Good:
  Module: ExplicitDependency
    Initialize(config, predictor):
      self.config = config
      self.predictor = predictor
```

### 3. Validate at Boundaries

```
Good:
  Module: ValidatedModule
    Forward(input):
      # Validate input
      validate_input(input)

      result = predictor.forward(input)

      # Validate output
      validate_output(result)

      return result
```

### 4. Log for Observability

```
Good:
  Module: ObservableModule
    Forward(input):
      log.info("Processing", input_size: len(input))

      start = now()
      result = predictor.forward(input)
      duration = now() - start

      log.info("Completed", duration: duration, success: true)
      return result
```
