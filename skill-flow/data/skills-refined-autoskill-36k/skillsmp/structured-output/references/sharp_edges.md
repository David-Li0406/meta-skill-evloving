# Structured Output - Sharp Edges

## Json Mode Requires Prompt

### **Id**
json-mode-requires-prompt
### **Summary**
JSON mode needs "json" in prompt
### **Severity**
high
### **Situation**
OpenAI returns text instead of JSON
### **Why**
  OpenAI JSON mode requires mentioning JSON in the prompt.
  Without it, returns plain text.
  Easy to forget.
  
### **Solution**
  # WRONG - no mention of JSON
  response = client.chat.completions.create(
      model="gpt-4o",
      response_format={"type": "json_object"},
      messages=[
          {"role": "user", "content": "Extract the name and age"}
      ]
  )
  # May return: "The name is John and age is 30"
  
  # CORRECT - mention JSON in prompt
  response = client.chat.completions.create(
      model="gpt-4o",
      response_format={"type": "json_object"},
      messages=[
          {"role": "system", "content": "Extract data. Respond in JSON format."},
          {"role": "user", "content": "John is 30 years old"}
      ]
  )
  # Returns: {"name": "John", "age": 30}
  
  # BETTER - use structured outputs (no prompt requirement)
  response = client.chat.completions.create(
      model="gpt-4o-2024-08-06",
      response_format={
          "type": "json_schema",
          "json_schema": {...}
      },
      messages=[...]  # No need to mention JSON
  )
  
### **Symptoms**
  - Plain text instead of JSON
  - "I'll help you with that..." responses
  - JSON parsing errors
### **Detection Pattern**
response_format.*json_object

## Strict Schema Model Requirement

### **Id**
strict-schema-model-requirement
### **Summary**
Structured outputs require specific models
### **Severity**
high
### **Situation**
Schema not enforced, malformed output
### **Why**
  Only certain OpenAI models support json_schema.
  Older models ignore the schema.
  Silently falls back to unstructured.
  
### **Solution**
  # WRONG - old model doesn't support strict schemas
  response = client.chat.completions.create(
      model="gpt-4",  # Old model
      response_format={
          "type": "json_schema",
          "json_schema": {
              "name": "output",
              "strict": True,
              "schema": {...}
          }
      },
      messages=[...]
  )
  # Schema may not be enforced!
  
  # CORRECT - use compatible model
  response = client.chat.completions.create(
      model="gpt-4o-2024-08-06",  # Supports structured outputs
      # Or: gpt-4o-mini-2024-07-18
      response_format={
          "type": "json_schema",
          "json_schema": {
              "name": "output",
              "strict": True,
              "schema": {...}
          }
      },
      messages=[...]
  )
  
  # Check model capabilities
  STRUCTURED_OUTPUT_MODELS = [
      "gpt-4o-2024-08-06",
      "gpt-4o-mini-2024-07-18",
      "gpt-4o",  # Latest versions
  ]
  
### **Symptoms**
  - Schema violations
  - Missing required fields
  - Wrong types in output
### **Detection Pattern**
json_schema.*strict

## Instructor Mode Mismatch

### **Id**
instructor-mode-mismatch
### **Summary**
Wrong Instructor mode for use case
### **Severity**
medium
### **Situation**
Extraction fails or uses wrong method
### **Why**
  Instructor has multiple modes.
  Default mode may not match provider.
  Mode affects reliability.
  
### **Solution**
  import instructor
  from openai import OpenAI
  
  # Instructor modes:
  # - TOOLS: Uses function calling (default for OpenAI)
  # - JSON: Uses JSON mode
  # - MD_JSON: Extracts JSON from markdown
  # - PARALLEL: Multiple tool calls
  
  # Default - uses tools/function calling
  client = instructor.from_openai(OpenAI())
  
  # Explicit JSON mode
  client = instructor.from_openai(
      OpenAI(),
      mode=instructor.Mode.JSON
  )
  
  # For Anthropic (always uses tools)
  import anthropic
  client = instructor.from_anthropic(anthropic.Anthropic())
  
  # For OpenAI structured outputs (strictest)
  client = instructor.from_openai(
      OpenAI(),
      mode=instructor.Mode.JSON_SCHEMA  # Uses response_format
  )
  
  # Mode selection guide:
  # - Simple extraction: JSON mode
  # - Complex schemas: TOOLS mode
  # - Multiple extractions: PARALLEL mode
  # - Anthropic: Always TOOLS (no JSON mode)
  
### **Symptoms**
  - Unexpected extraction method
  - "tool_calls" when expecting JSON
  - Anthropic returning markdown
### **Detection Pattern**
instructor\.from_

## Pydantic Optional Gotcha

### **Id**
pydantic-optional-gotcha
### **Summary**
Optional fields default to None unexpectedly
### **Severity**
medium
### **Situation**
Fields missing when expected
### **Why**
  LLM may skip optional fields.
  Pydantic fills with None.
  Logic may not handle None.
  
### **Solution**
  from pydantic import BaseModel, Field
  from typing import Optional
  
  # PROBLEMATIC - too many optionals
  class User(BaseModel):
      name: str
      age: Optional[int] = None
      email: Optional[str] = None
      phone: Optional[str] = None
  
  # LLM might return just {"name": "John"}
  # All optionals become None
  
  # BETTER - required with defaults
  class User(BaseModel):
      name: str
      age: int = Field(default=0, description="Age, 0 if unknown")
      email: str = Field(default="", description="Email if provided")
  
  # BEST - separate required from optional
  class RequiredInfo(BaseModel):
      """Always extracted."""
      name: str
      age: int
  
  class OptionalInfo(BaseModel):
      """Extracted if available."""
      email: Optional[str] = None
      phone: Optional[str] = None
  
  # Two-pass extraction
  required = client.chat.completions.create(
      response_model=RequiredInfo,
      messages=[...]
  )
  optional = client.chat.completions.create(
      response_model=OptionalInfo,
      messages=[...]
  )
  
  # Or use discriminated unions
  from typing import Literal
  
  class CompleteUser(BaseModel):
      type: Literal["complete"] = "complete"
      name: str
      email: str
  
  class PartialUser(BaseModel):
      type: Literal["partial"] = "partial"
      name: str
  
### **Symptoms**
  - Unexpected None values
  - Optional fields always None
  - Downstream None errors
### **Detection Pattern**
Optional\[.*\]\s*=\s*None

## Streaming Partial Validation

### **Id**
streaming-partial-validation
### **Summary**
Partial objects fail validation during stream
### **Severity**
medium
### **Situation**
Validation errors mid-stream
### **Why**
  Partial object missing required fields.
  Validators run on incomplete data.
  Stream interrupts on error.
  
### **Solution**
  from pydantic import BaseModel, Field, model_validator
  from typing import Optional
  import instructor
  
  # PROBLEMATIC - validator on required field
  class Article(BaseModel):
      title: str
      content: str
  
      @model_validator(mode="after")
      def validate_content_length(self):
          if len(self.content) < 100:
              raise ValueError("Content too short")
          return self
  
  # Fails mid-stream when content is partial!
  
  # CORRECT - make validator streaming-aware
  class Article(BaseModel):
      title: Optional[str] = None
      content: Optional[str] = None
      _is_partial: bool = False
  
      @model_validator(mode="after")
      def validate_content_length(self):
          # Skip validation during streaming
          if self._is_partial or self.content is None:
              return self
          if len(self.content) < 100:
              raise ValueError("Content too short")
          return self
  
  # Use instructor's Partial wrapper
  from instructor import Partial
  
  for partial in client.chat.completions.create(
      response_model=Partial[Article],  # Handles incomplete data
      stream=True,
      messages=[...]
  ):
      # partial.title may be None initially
      # partial.content grows over time
      # No validation errors during stream
      print(partial.title)
  
### **Symptoms**
  - Stream stops unexpectedly
  - "validation error" mid-response
  - Partial data lost
### **Detection Pattern**
Partial\[|stream=True

## Anthropic Tool Result Handling

### **Id**
anthropic-tool-result-handling
### **Summary**
Must handle tool_use blocks correctly
### **Severity**
high
### **Situation**
Tool response not processed
### **Why**
  Claude returns tool_use blocks.
  Must iterate content to find them.
  Different from OpenAI structure.
  
### **Solution**
  import anthropic
  from pydantic import BaseModel
  
  client = anthropic.Anthropic()
  
  class Output(BaseModel):
      result: str
      confidence: float
  
  response = client.messages.create(
      model="claude-sonnet-4-20250514",
      max_tokens=1024,
      tools=[{
          "name": "provide_output",
          "input_schema": Output.model_json_schema()
      }],
      tool_choice={"type": "tool", "name": "provide_output"},
      messages=[...]
  )
  
  # WRONG - treating like OpenAI
  # data = response.content[0].input  # May be TextBlock!
  
  # CORRECT - find tool_use block
  tool_input = None
  for block in response.content:
      if block.type == "tool_use":
          tool_input = block.input
          break
  
  if tool_input is None:
      raise ValueError("No tool use in response")
  
  output = Output.model_validate(tool_input)
  
  # Or use instructor for Anthropic
  import instructor
  
  client = instructor.from_anthropic(anthropic.Anthropic())
  output = client.messages.create(
      model="claude-sonnet-4-20250514",
      response_model=Output,  # Handles everything
      messages=[...]
  )
  
### **Symptoms**
  - AttributeError on response
  - TextBlock has no attribute 'input'
  - Empty results
### **Detection Pattern**
anthropic.*tool

## Outlines Model Loading

### **Id**
outlines-model-loading
### **Summary**
Outlines model loading is slow
### **Severity**
low
### **Situation**
Long startup time, high memory
### **Why**
  Downloads and loads full model.
  No lazy loading by default.
  Memory intensive.
  
### **Solution**
  import outlines
  
  # SLOW - loads on every call
  def process(text):
      model = outlines.models.transformers("mistral")  # Slow!
      generator = outlines.generate.json(model, Schema)
      return generator(text)
  
  # CORRECT - load once, reuse
  class StructuredGenerator:
      def __init__(self):
          # Load at startup
          self.model = outlines.models.transformers(
              "mistralai/Mistral-7B-Instruct-v0.2",
              device="cuda"  # Specify device
          )
          # Pre-compile generators
          self.schema_generator = outlines.generate.json(
              self.model, Schema
          )
  
      def process(self, text):
          return self.schema_generator(text)
  
  # Singleton pattern
  _generator = None
  
  def get_generator():
      global _generator
      if _generator is None:
          _generator = StructuredGenerator()
      return _generator
  
  # For serverless, use modal.com or similar
  # that keeps models warm
  
### **Symptoms**
  - Slow first request
  - High memory usage
  - Timeout on cold start
### **Detection Pattern**
outlines\.models\.