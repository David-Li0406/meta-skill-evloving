# Signature Patterns

Signatures define the contract between your application and the LLM. They specify inputs, outputs, and constraints.

## Basic Signature Structure

```
Signature: TaskName
  Description: "Clear description of what this task does"

  Inputs:
    field_name: Type, description: "What this field contains"

  Outputs:
    field_name: Type, description: "What this field returns"
```

## Field Types

### Primitive Types

| Type | Use Case | Example |
|------|----------|---------|
| String | Free-form text | Names, descriptions, content |
| Integer | Whole numbers | Counts, IDs, ratings (1-5) |
| Float | Decimal numbers | Scores, percentages, prices |
| Boolean | Yes/no decisions | Flags, binary classifications |

### Constrained Types

| Type | Use Case | Example |
|------|----------|---------|
| Enum | Fixed set of options | Categories, status values |
| Range | Bounded numbers | Rating 1-10, percentage 0-100 |
| Pattern | Regex-matched strings | Email, phone, URL |
| List | Multiple values | Tags, keywords, items |

### Complex Types

| Type | Use Case | Example |
|------|----------|---------|
| Object | Nested structure | Address, person details |
| Array[Object] | List of structures | Search results, recommendations |
| Optional | May or may not exist | Nullable fields |

## Signature Examples

### Classification

```
Signature: SentimentAnalysis
  Description: "Analyze the sentiment of text"

  Inputs:
    text: String
      description: "The text to analyze"

  Outputs:
    sentiment: Enum["positive", "negative", "neutral"]
      description: "Overall sentiment"
    confidence: Float (0.0-1.0)
      description: "Confidence in the classification"
    reasoning: String
      description: "Brief explanation of the classification"
```

### Entity Extraction

```
Signature: ContactExtraction
  Description: "Extract contact information from text"

  Inputs:
    text: String
      description: "Text that may contain contact info"

  Outputs:
    name: Optional[String]
      description: "Person's name if found"
    email: Optional[String]
      description: "Email address if found"
    phone: Optional[String]
      description: "Phone number if found"
    company: Optional[String]
      description: "Company name if found"
```

### Summarization

```
Signature: DocumentSummary
  Description: "Create a concise summary of a document"

  Inputs:
    document: String
      description: "The full document text"
    max_length: Integer
      description: "Maximum summary length in words"

  Outputs:
    summary: String
      description: "Concise summary of key points"
    key_points: List[String]
      description: "Bullet points of main ideas"
```

### Question Answering

```
Signature: QuestionAnswer
  Description: "Answer a question based on context"

  Inputs:
    context: String
      description: "Background information"
    question: String
      description: "The question to answer"

  Outputs:
    answer: String
      description: "Direct answer to the question"
    confidence: Float (0.0-1.0)
      description: "Confidence in the answer"
    source_quote: Optional[String]
      description: "Relevant quote from context"
```

### Code Generation

```
Signature: CodeGeneration
  Description: "Generate code based on requirements"

  Inputs:
    language: Enum["python", "typescript", "go", "rust"]
      description: "Target programming language"
    requirements: String
      description: "What the code should do"
    context: Optional[String]
      description: "Existing code for context"

  Outputs:
    code: String
      description: "Generated code"
    explanation: String
      description: "What the code does"
    dependencies: List[String]
      description: "Required libraries/imports"
```

### Multi-Label Classification

```
Signature: TopicTagging
  Description: "Assign relevant topic tags to content"

  Inputs:
    content: String
      description: "The content to tag"
    available_tags: List[String]
      description: "Tags to choose from"

  Outputs:
    tags: List[String]
      description: "Selected tags (subset of available)"
    primary_tag: String
      description: "Most relevant single tag"
```

## Vision/Multimodal Signatures

```
Signature: ImageAnalysis
  Description: "Analyze and describe an image"

  Inputs:
    image: Image
      description: "The image to analyze"
    question: Optional[String]
      description: "Specific question about the image"

  Outputs:
    description: String
      description: "What the image shows"
    objects: List[String]
      description: "Objects detected in the image"
    text: Optional[String]
      description: "Any text visible in the image"
```

## Signature Design Guidelines

### 1. Be Specific in Descriptions

```
Bad:
  Inputs:
    data: String  # What data? What format?

Good:
  Inputs:
    customer_email: String
      description: "Raw email text from customer support inbox"
```

### 2. Use Enums for Constrained Outputs

```
Bad:
  Outputs:
    category: String  # LLM might return anything

Good:
  Outputs:
    category: Enum["bug", "feature", "question", "other"]
```

### 3. Include Confidence Scores

```
Good:
  Outputs:
    classification: String
    confidence: Float (0.0-1.0)
      description: "How confident the model is"
```

### 4. Make Optional Fields Explicit

```
Good:
  Outputs:
    email: Optional[String]
      description: "Email if found, null otherwise"
```

### 5. Bound Numeric Outputs

```
Bad:
  Outputs:
    score: Integer  # Could be anything

Good:
  Outputs:
    score: Integer (1-10)
      description: "Quality score from 1 (worst) to 10 (best)"
```

## Validation Patterns

### Input Validation

Before sending to LLM:
- Check required fields are present
- Validate types match expectations
- Enforce length limits
- Sanitize inputs if needed

### Output Validation

After receiving from LLM:
- Verify all required fields present
- Check types are correct
- Validate enums contain valid values
- Ensure numbers in expected ranges
- Retry if validation fails

### Retry Strategy

```
For attempt in 1..max_retries:
  result = llm.predict(signature, inputs)
  if validate(result):
    return result
  else:
    log_validation_error(result)
    continue

raise ValidationError("Failed after max retries")
```
