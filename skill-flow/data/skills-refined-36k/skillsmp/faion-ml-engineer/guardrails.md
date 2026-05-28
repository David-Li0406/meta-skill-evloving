---
id: guardrails
name: "Guardrails"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Guardrails

## Overview

Guardrails are safety mechanisms that validate, filter, and constrain LLM inputs and outputs. They protect against harmful content, ensure compliance, maintain quality, and prevent prompt injection attacks.

## When to Use

- Production LLM applications
- User-facing chatbots
- Content generation systems
- When handling sensitive data
- Regulated industries (healthcare, finance)
- Multi-tenant applications

## Key Concepts

### Guardrail Types

| Type | Purpose | When Applied |
|------|---------|--------------|
| Input Guardrails | Validate/sanitize user input | Before LLM call |
| Output Guardrails | Filter/validate LLM response | After LLM call |
| Structural | Ensure format compliance | After LLM call |
| Safety | Block harmful content | Both |
| Compliance | Regulatory requirements | Both |

### Defense Layers

```
┌─────────────────────────────────────────────┐
│              User Input                      │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│         Input Guardrails                     │
│  - Prompt injection detection               │
│  - PII detection/redaction                  │
│  - Topic filtering                          │
│  - Length limits                            │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│              LLM                             │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│         Output Guardrails                    │
│  - Content moderation                       │
│  - Factuality checking                      │
│  - Format validation                        │
│  - Hallucination detection                  │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│              Response                        │
└─────────────────────────────────────────────┘
```

## Implementation

### Input Validation

```python
import re
from typing import Tuple, List
from dataclasses import dataclass

@dataclass
class ValidationResult:
    is_valid: bool
    sanitized_input: str
    violations: List[str]

class InputGuardrails:
    """Validate and sanitize user inputs."""

    def __init__(
        self,
        max_length: int = 4000,
        blocked_patterns: List[str] = None,
        pii_patterns: dict = None
    ):
        self.max_length = max_length
        self.blocked_patterns = blocked_patterns or []
        self.pii_patterns = pii_patterns or {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'
        }

    def validate(self, text: str) -> ValidationResult:
        """Validate input text."""
        violations = []
        sanitized = text

        # Length check
        if len(text) > self.max_length:
            violations.append(f"Input exceeds max length ({self.max_length})")
            sanitized = sanitized[:self.max_length]

        # Check blocked patterns
        for pattern in self.blocked_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                violations.append(f"Blocked pattern detected")
                sanitized = re.sub(pattern, '[BLOCKED]', sanitized, flags=re.IGNORECASE)

        # PII detection
        for pii_type, pattern in self.pii_patterns.items():
            if re.search(pattern, text):
                violations.append(f"PII detected: {pii_type}")
                sanitized = re.sub(pattern, f'[{pii_type.upper()}_REDACTED]', sanitized)

        return ValidationResult(
            is_valid=len(violations) == 0,
            sanitized_input=sanitized,
            violations=violations
        )
```

### Prompt Injection Detection

```python
from typing import List, Tuple
import re

class PromptInjectionDetector:
    """Detect and block prompt injection attempts."""

    INJECTION_PATTERNS = [
        # Ignore instructions
        r'ignore\s+(all\s+)?(previous|above|prior)\s+(instructions?|prompts?)',
        r'disregard\s+(all\s+)?(previous|above)',
        # Role manipulation
        r'you\s+are\s+(now|actually)\s+a',
        r'pretend\s+(to\s+be|you\s+are)',
        r'act\s+as\s+(if|a)',
        # System prompt extraction
        r'(show|reveal|display|print|output)\s+(your|the)\s+(system\s+)?prompt',
        r'what\s+(is|are)\s+your\s+(instructions?|rules?)',
        # Jailbreak attempts
        r'(DAN|STAN|DUDE|KEVIN)\s+mode',
        r'developer\s+mode',
        r'bypass\s+(safety|filter)',
        # Code injection
        r'<\s*script',
        r'{{.*}}',  # Template injection
        r'\$\{.*\}',  # String interpolation
    ]

    def __init__(self, custom_patterns: List[str] = None):
        self.patterns = self.INJECTION_PATTERNS + (custom_patterns or [])

    def detect(self, text: str) -> Tuple[bool, List[str]]:
        """Detect prompt injection attempts."""
        detections = []

        for pattern in self.patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                detections.append({
                    'pattern': pattern,
                    'matches': matches
                })

        return len(detections) > 0, detections

    def is_safe(self, text: str) -> bool:
        """Check if input is safe."""
        is_injection, _ = self.detect(text)
        return not is_injection
```

### Content Moderation

```python
from openai import OpenAI
from typing import Dict, List

client = OpenAI()

class ContentModerator:
    """Moderate content for safety."""

    CATEGORIES = [
        'hate', 'hate/threatening',
        'harassment', 'harassment/threatening',
        'self-harm', 'self-harm/intent', 'self-harm/instructions',
        'sexual', 'sexual/minors',
        'violence', 'violence/graphic'
    ]

    def __init__(
        self,
        threshold: float = 0.5,
        blocked_categories: List[str] = None
    ):
        self.threshold = threshold
        self.blocked_categories = blocked_categories or self.CATEGORIES

    def moderate(self, text: str) -> Dict:
        """Check content against moderation API."""
        response = client.moderations.create(input=text)
        result = response.results[0]

        flagged = []
        scores = {}

        for category in self.CATEGORIES:
            score = getattr(result.category_scores, category.replace('/', '_').replace('-', '_'))
            scores[category] = score

            if category in self.blocked_categories and score > self.threshold:
                flagged.append({
                    'category': category,
                    'score': score
                })

        return {
            'is_flagged': len(flagged) > 0,
            'flagged_categories': flagged,
            'scores': scores
        }

    def is_safe(self, text: str) -> bool:
        """Quick safety check."""
        result = self.moderate(text)
        return not result['is_flagged']
```

### Output Validation

```python
from typing import List, Dict, Callable
import json

class OutputGuardrails:
    """Validate and filter LLM outputs."""

    def __init__(self):
        self.validators: List[Callable] = []
        self.filters: List[Callable] = []

    def add_validator(self, validator: Callable):
        """Add a validator function."""
        self.validators.append(validator)

    def add_filter(self, filter_func: Callable):
        """Add a filter function."""
        self.filters.append(filter_func)

    def validate(self, output: str) -> Tuple[bool, List[str]]:
        """Run all validators on output."""
        errors = []

        for validator in self.validators:
            try:
                is_valid, error = validator(output)
                if not is_valid:
                    errors.append(error)
            except Exception as e:
                errors.append(f"Validator error: {e}")

        return len(errors) == 0, errors

    def filter(self, output: str) -> str:
        """Apply all filters to output."""
        filtered = output

        for filter_func in self.filters:
            try:
                filtered = filter_func(filtered)
            except Exception as e:
                pass  # Skip failed filters

        return filtered

# Common validators
def validate_no_profanity(output: str) -> Tuple[bool, str]:
    """Check for profanity."""
    profanity_list = ['...']  # Add actual list
    for word in profanity_list:
        if word.lower() in output.lower():
            return False, f"Profanity detected: {word}"
    return True, ""

def validate_json_format(output: str) -> Tuple[bool, str]:
    """Validate JSON format."""
    try:
        json.loads(output)
        return True, ""
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"

def validate_length(max_length: int):
    """Create length validator."""
    def validator(output: str) -> Tuple[bool, str]:
        if len(output) > max_length:
            return False, f"Output exceeds {max_length} characters"
        return True, ""
    return validator

# Common filters
def filter_remove_urls(output: str) -> str:
    """Remove URLs from output."""
    url_pattern = r'https?://\S+'
    return re.sub(url_pattern, '[URL REMOVED]', output)

def filter_remove_code_blocks(output: str) -> str:
    """Remove code blocks from output."""
    return re.sub(r'```[\s\S]*?```', '[CODE REMOVED]', output)
```

### Hallucination Detection

```python
class HallucinationDetector:
    """Detect potential hallucinations in LLM output."""

    def __init__(self, client, model: str = "gpt-4o"):
        self.client = client
        self.model = model

    def check_factuality(
        self,
        claim: str,
        context: str
    ) -> Dict:
        """Check if a claim is supported by context."""
        prompt = f"""Determine if the claim is supported by the context.

Context:
{context}

Claim:
{claim}

Respond with JSON:
{{
    "verdict": "supported" | "not_supported" | "partially_supported",
    "confidence": 0.0-1.0,
    "explanation": "..."
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    def detect_hallucinations(
        self,
        output: str,
        context: str
    ) -> Dict:
        """Detect hallucinations in output given context."""
        prompt = f"""Analyze the response for potential hallucinations.
A hallucination is information not supported by the given context.

Context:
{context}

Response to analyze:
{output}

Return JSON:
{{
    "has_hallucinations": true/false,
    "hallucinated_claims": ["claim1", "claim2"],
    "supported_claims": ["claim1", "claim2"],
    "confidence": 0.0-1.0
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)
```

### Topic/Intent Classification

```python
from enum import Enum
from typing import List

class Intent(Enum):
    GENERAL = "general"
    HARMFUL = "harmful"
    PERSONAL_DATA = "personal_data"
    SYSTEM_MANIPULATION = "system_manipulation"
    OFF_TOPIC = "off_topic"

class IntentClassifier:
    """Classify user intent for filtering."""

    def __init__(
        self,
        client,
        allowed_topics: List[str] = None,
        model: str = "gpt-4o-mini"
    ):
        self.client = client
        self.model = model
        self.allowed_topics = allowed_topics

    def classify(self, text: str) -> Dict:
        """Classify the intent of user input."""
        topics_str = ", ".join(self.allowed_topics) if self.allowed_topics else "any"

        prompt = f"""Classify the intent of this message.

Allowed topics: {topics_str}

Message: {text}

Return JSON:
{{
    "intent": "general|harmful|personal_data|system_manipulation|off_topic",
    "is_allowed": true/false,
    "confidence": 0.0-1.0,
    "detected_topics": ["topic1", "topic2"],
    "reasoning": "..."
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)
```

### Complete Guardrails Pipeline

```python
from dataclasses import dataclass
from typing import Optional, List, Callable
import logging

@dataclass
class GuardrailConfig:
    max_input_length: int = 4000
    max_output_length: int = 8000
    enable_pii_detection: bool = True
    enable_prompt_injection_detection: bool = True
    enable_content_moderation: bool = True
    enable_hallucination_detection: bool = False
    blocked_topics: List[str] = None
    custom_validators: List[Callable] = None

@dataclass
class GuardrailResult:
    is_safe: bool
    input_modified: bool
    output_modified: bool
    original_input: str
    sanitized_input: str
    original_output: Optional[str]
    filtered_output: Optional[str]
    violations: List[Dict]
    metadata: Dict

class GuardrailsPipeline:
    """Complete guardrails pipeline for LLM applications."""

    def __init__(
        self,
        client,
        model: str = "gpt-4o",
        config: Optional[GuardrailConfig] = None
    ):
        self.client = client
        self.model = model
        self.config = config or GuardrailConfig()
        self.logger = logging.getLogger(__name__)

        # Initialize components
        self.input_guardrails = InputGuardrails(
            max_length=self.config.max_input_length
        )
        self.injection_detector = PromptInjectionDetector()
        self.content_moderator = ContentModerator()
        self.output_guardrails = OutputGuardrails()
        self.hallucination_detector = HallucinationDetector(client)

    def process_input(self, user_input: str) -> Tuple[str, List[Dict]]:
        """Process and validate user input."""
        violations = []
        sanitized = user_input

        # Length and PII check
        if self.config.enable_pii_detection:
            result = self.input_guardrails.validate(sanitized)
            if not result.is_valid:
                violations.extend([{"type": "input_validation", "detail": v} for v in result.violations])
            sanitized = result.sanitized_input

        # Prompt injection detection
        if self.config.enable_prompt_injection_detection:
            is_injection, detections = self.injection_detector.detect(sanitized)
            if is_injection:
                violations.append({
                    "type": "prompt_injection",
                    "detail": "Potential prompt injection detected",
                    "detections": detections
                })
                return None, violations  # Block the request

        # Content moderation
        if self.config.enable_content_moderation:
            moderation = self.content_moderator.moderate(sanitized)
            if moderation['is_flagged']:
                violations.append({
                    "type": "content_moderation",
                    "detail": "Content flagged by moderation",
                    "categories": moderation['flagged_categories']
                })
                return None, violations

        return sanitized, violations

    def process_output(
        self,
        output: str,
        context: str = None
    ) -> Tuple[str, List[Dict]]:
        """Process and validate LLM output."""
        violations = []
        filtered = output

        # Content moderation
        if self.config.enable_content_moderation:
            moderation = self.content_moderator.moderate(filtered)
            if moderation['is_flagged']:
                violations.append({
                    "type": "output_moderation",
                    "detail": "Output flagged by moderation",
                    "categories": moderation['flagged_categories']
                })
                # You might filter or block here
                filtered = "[Response filtered due to content policy]"

        # Hallucination detection
        if self.config.enable_hallucination_detection and context:
            hallucination_check = self.hallucination_detector.detect_hallucinations(
                filtered, context
            )
            if hallucination_check.get('has_hallucinations'):
                violations.append({
                    "type": "hallucination",
                    "detail": "Potential hallucinations detected",
                    "claims": hallucination_check.get('hallucinated_claims', [])
                })

        # Custom validators
        if self.config.custom_validators:
            for validator in self.config.custom_validators:
                is_valid, error = validator(filtered)
                if not is_valid:
                    violations.append({
                        "type": "custom_validation",
                        "detail": error
                    })

        # Output filters
        filtered = self.output_guardrails.filter(filtered)

        return filtered, violations

    def run(
        self,
        user_input: str,
        system_prompt: str = "",
        context: str = None
    ) -> GuardrailResult:
        """Run complete guardrails pipeline."""
        all_violations = []

        # Process input
        sanitized_input, input_violations = self.process_input(user_input)
        all_violations.extend(input_violations)

        if sanitized_input is None:
            # Input blocked
            return GuardrailResult(
                is_safe=False,
                input_modified=True,
                output_modified=False,
                original_input=user_input,
                sanitized_input="[BLOCKED]",
                original_output=None,
                filtered_output=None,
                violations=all_violations,
                metadata={"stage": "input_blocked"}
            )

        # Call LLM
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": sanitized_input})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        original_output = response.choices[0].message.content

        # Process output
        filtered_output, output_violations = self.process_output(
            original_output, context
        )
        all_violations.extend(output_violations)

        return GuardrailResult(
            is_safe=len(all_violations) == 0,
            input_modified=sanitized_input != user_input,
            output_modified=filtered_output != original_output,
            original_input=user_input,
            sanitized_input=sanitized_input,
            original_output=original_output,
            filtered_output=filtered_output,
            violations=all_violations,
            metadata={"model": self.model}
        )
```

### Using Guardrails Library

```python
# pip install guardrails-ai

from guardrails import Guard
from guardrails.validators import (
    ValidLength,
    ToxicLanguage,
    RegexMatch,
    ValidJSON
)

# Create guard with validators
guard = Guard().use_many(
    ValidLength(min=1, max=1000, on_fail="fix"),
    ToxicLanguage(threshold=0.5, on_fail="filter"),
)

# Use with LLM
result = guard(
    llm_api=openai.chat.completions.create,
    prompt="Tell me about AI safety",
    model="gpt-4o",
    max_tokens=500
)

if result.validation_passed:
    print(result.validated_output)
else:
    print(f"Validation failed: {result.validation_summary}")
```

## Best Practices

1. **Defense in Depth**
   - Multiple layers of validation
   - Both input and output checks
   - Don't rely on single guardrail

2. **Graceful Degradation**
   - Provide helpful error messages
   - Fall back to safe responses
   - Log violations for analysis

3. **Performance**
   - Use fast checks first
   - Async validation when possible
   - Cache moderation results

4. **Testing**
   - Red team your guardrails
   - Test edge cases
   - Regular adversarial testing

5. **Monitoring**
   - Log all violations
   - Track false positives
   - Alert on patterns

## Common Pitfalls

1. **Over-filtering** - Blocking legitimate content
2. **Under-filtering** - Missing harmful content
3. **No Bypass Detection** - Missing creative injection attempts
4. **Static Rules** - Not updating for new threats
5. **Ignoring Context** - Same rules for all use cases
6. **No Logging** - Can't improve without data

## References

- [OpenAI Moderation API](https://platform.openai.com/docs/guides/moderation)
- [Guardrails AI](https://www.guardrailsai.com/)
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails)
