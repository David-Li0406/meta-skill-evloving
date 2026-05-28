# Structured Output

## Patterns


---
  #### **Name**
OpenAI JSON Mode
  #### **Description**
Native JSON output from OpenAI models
  #### **When To Use**
Simple JSON structures with GPT-4/GPT-4o
  #### **Implementation**
    from openai import OpenAI
    from pydantic import BaseModel
    import json
    
    client = OpenAI()
    
    class UserInfo(BaseModel):
        name: str
        age: int
        email: str
    
    # Method 1: JSON mode (requires "json" in prompt)
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "Extract user info. Respond in JSON."},
            {"role": "user", "content": "John Doe is 30, email john@example.com"}
        ]
    )
    data = json.loads(response.choices[0].message.content)
    
    # Method 2: Structured Outputs (with schema - RECOMMENDED)
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",  # Must use compatible model
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "user_info",
                "strict": True,
                "schema": UserInfo.model_json_schema()
            }
        },
        messages=[
            {"role": "user", "content": "John Doe is 30, email john@example.com"}
        ]
    )
    # Guaranteed to match schema
    user = UserInfo.model_validate_json(response.choices[0].message.content)
    

---
  #### **Name**
OpenAI Function Calling
  #### **Description**
Use tools/functions for structured extraction
  #### **When To Use**
When you need tool semantics or complex schemas
  #### **Implementation**
    from openai import OpenAI
    from pydantic import BaseModel, Field
    import json
    
    client = OpenAI()
    
    class ExtractedData(BaseModel):
        """Data extracted from text."""
        entities: list[str] = Field(description="Named entities found")
        sentiment: str = Field(description="Overall sentiment: positive, negative, neutral")
        summary: str = Field(description="One sentence summary")
    
    # Define as a tool
    tools = [
        {
            "type": "function",
            "function": {
                "name": "extract_data",
                "description": "Extract structured data from text",
                "parameters": ExtractedData.model_json_schema()
            }
        }
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": "Apple announced record profits. Tim Cook was excited."}
        ],
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "extract_data"}}
    )
    
    # Parse the function call
    tool_call = response.choices[0].message.tool_calls[0]
    data = ExtractedData.model_validate_json(tool_call.function.arguments)
    print(data.entities)  # ["Apple", "Tim Cook"]
    

---
  #### **Name**
Anthropic Tool Use
  #### **Description**
Structured output via Claude's tool use
  #### **When To Use**
When using Claude models
  #### **Implementation**
    import anthropic
    from pydantic import BaseModel, Field
    
    client = anthropic.Anthropic()
    
    class Analysis(BaseModel):
        """Analysis result."""
        key_points: list[str] = Field(description="Main points from the text")
        action_items: list[str] = Field(description="Suggested actions")
        priority: str = Field(description="high, medium, or low")
    
    # Define tool from Pydantic model
    tools = [
        {
            "name": "provide_analysis",
            "description": "Provide structured analysis of the input",
            "input_schema": Analysis.model_json_schema()
        }
    ]
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        tools=tools,
        tool_choice={"type": "tool", "name": "provide_analysis"},
        messages=[
            {"role": "user", "content": "Review this meeting: We discussed Q4 goals..."}
        ]
    )
    
    # Extract tool use block
    for block in response.content:
        if block.type == "tool_use":
            analysis = Analysis.model_validate(block.input)
            print(analysis.key_points)
    

---
  #### **Name**
Instructor Library
  #### **Description**
Pydantic-first structured extraction
  #### **When To Use**
Production applications needing validation and retries
  #### **Implementation**
    import instructor
    from openai import OpenAI
    from pydantic import BaseModel, Field, field_validator
    from typing import Optional
    
    # Patch the client
    client = instructor.from_openai(OpenAI())
    
    class User(BaseModel):
        name: str
        age: int = Field(ge=0, le=150)  # Validation!
        email: str
    
        @field_validator("email")
        @classmethod
        def validate_email(cls, v):
            if "@" not in v:
                raise ValueError("Invalid email")
            return v
    
    # Simple extraction with automatic retries
    user = client.chat.completions.create(
        model="gpt-4o",
        response_model=User,
        messages=[
            {"role": "user", "content": "John Doe, 30 years, john@example.com"}
        ]
    )
    print(user.name)  # "John Doe"
    
    # With validation retries
    user = client.chat.completions.create(
        model="gpt-4o",
        response_model=User,
        max_retries=3,  # Retry on validation failure
        messages=[
            {"role": "user", "content": "Extract: Jane, age 25, jane.doe@company.org"}
        ]
    )
    
    # Streaming partial objects
    from instructor import Partial
    
    for partial_user in client.chat.completions.create(
        model="gpt-4o",
        response_model=Partial[User],
        stream=True,
        messages=[{"role": "user", "content": "..."}]
    ):
        print(partial_user)  # Partial object updates as tokens arrive
    
    # Works with Anthropic too
    import anthropic
    client = instructor.from_anthropic(anthropic.Anthropic())
    

---
  #### **Name**
Outlines Constrained Generation
  #### **Description**
Token-level constraints for local models
  #### **When To Use**
Local models or when you need guaranteed format
  #### **Implementation**
    import outlines
    from pydantic import BaseModel
    from enum import Enum
    
    class Sentiment(str, Enum):
        positive = "positive"
        negative = "negative"
        neutral = "neutral"
    
    class Review(BaseModel):
        sentiment: Sentiment
        score: int  # 1-5
        summary: str
    
    # Load model
    model = outlines.models.transformers("mistralai/Mistral-7B-Instruct-v0.2")
    
    # Create structured generator
    generator = outlines.generate.json(model, Review)
    
    # Generate - GUARANTEED to match schema
    review = generator("Review: This product is amazing! Best purchase ever.")
    print(review.sentiment)  # Sentiment.positive
    
    # Regex constraint for specific formats
    phone_generator = outlines.generate.regex(
        model,
        r"\(\d{3}\) \d{3}-\d{4}"
    )
    phone = phone_generator("What's your phone number? Mine is")
    # Output: "(555) 123-4567" - guaranteed format
    
    # Choice constraint
    choice_generator = outlines.generate.choice(
        model,
        ["yes", "no", "maybe"]
    )
    answer = choice_generator("Should I buy this? ")  # Only outputs yes/no/maybe
    

---
  #### **Name**
Streaming Structured Output
  #### **Description**
Stream partial structured data
  #### **When To Use**
Long outputs where you want progressive updates
  #### **Implementation**
    import instructor
    from openai import OpenAI
    from pydantic import BaseModel
    from typing import Optional
    
    client = instructor.from_openai(OpenAI())
    
    class Article(BaseModel):
        title: str
        sections: list[str]
        conclusion: Optional[str] = None
    
    # Stream with partial updates
    for partial in client.chat.completions.create(
        model="gpt-4o",
        response_model=instructor.Partial[Article],
        stream=True,
        messages=[
            {"role": "user", "content": "Write an article about AI safety"}
        ]
    ):
        # partial.title available first
        # partial.sections grows as tokens arrive
        print(f"Title: {partial.title}")
        print(f"Sections so far: {len(partial.sections or [])}")
    
    # OpenAI native streaming with response_format
    from openai import OpenAI
    import json
    
    client = OpenAI()
    stream = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        stream=True,
        messages=[...]
    )
    
    full_response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content:
            full_response += chunk.choices[0].delta.content
            # Parse partial JSON as it arrives
            try:
                partial = json.loads(full_response)
                print(partial)
            except json.JSONDecodeError:
                pass  # Not complete yet
    

---
  #### **Name**
Validation and Retry Strategies
  #### **Description**
Handle failures gracefully
  #### **When To Use**
Production systems needing reliability
  #### **Implementation**
    import instructor
    from openai import OpenAI
    from pydantic import BaseModel, Field, ValidationError
    from tenacity import retry, stop_after_attempt, retry_if_exception_type
    
    client = instructor.from_openai(OpenAI())
    
    class StrictOutput(BaseModel):
        value: int = Field(ge=0, le=100)
        category: str = Field(pattern=r"^[A-Z][a-z]+$")  # Capitalized word
    
    # Method 1: Instructor's built-in retries
    result = client.chat.completions.create(
        model="gpt-4o",
        response_model=StrictOutput,
        max_retries=3,  # Automatically retries on validation error
        messages=[...]
    )
    
    # Method 2: Custom retry with tenacity
    @retry(
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type(ValidationError)
    )
    def extract_with_retry(text: str) -> StrictOutput:
        return client.chat.completions.create(
            model="gpt-4o",
            response_model=StrictOutput,
            messages=[{"role": "user", "content": text}]
        )
    
    # Method 3: Fallback chain
    def extract_with_fallback(text: str) -> dict:
        try:
            # Try strict schema first
            return client.chat.completions.create(
                model="gpt-4o",
                response_model=StrictOutput,
                messages=[{"role": "user", "content": text}]
            ).model_dump()
        except ValidationError:
            # Fall back to JSON mode
            response = OpenAI().chat.completions.create(
                model="gpt-4o",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": "Extract data as JSON."},
                    {"role": "user", "content": text}
                ]
            )
            return json.loads(response.choices[0].message.content)
    
    # Method 4: Validation hooks in Instructor
    def validation_hook(error: ValidationError, attempt: int):
        print(f"Attempt {attempt} failed: {error}")
        # Could log to monitoring, adjust prompt, etc.
    
    result = client.chat.completions.create(
        model="gpt-4o",
        response_model=StrictOutput,
        max_retries=3,
        validation_context={"on_error": validation_hook},
        messages=[...]
    )
    

## Anti-Patterns


---
  #### **Name**
Complex Nested Schemas
  #### **Description**
Deeply nested optional fields and unions
  #### **Why Bad**
    High failure rate with LLMs.
    Validation errors hard to debug.
    Retries compound token costs.
    
  #### **What To Do Instead**
    Flatten schemas where possible.
    Use multiple simpler extractions.
    Post-process to build complex structures.
    

---
  #### **Name**
No Validation
  #### **Description**
Trusting raw JSON output without validation
  #### **Why Bad**
    LLMs can output invalid JSON.
    Type mismatches crash downstream.
    Security vulnerabilities.
    
  #### **What To Do Instead**
    Always validate with Pydantic.
    Use try/except with fallbacks.
    Log validation failures for monitoring.
    

---
  #### **Name**
Ignoring Model Capabilities
  #### **Description**
Using same approach for all models
  #### **Why Bad**
    JSON mode support varies.
    Local models need Outlines.
    Some models are unreliable.
    
  #### **What To Do Instead**
    Check model documentation.
    Use Outlines for local models.
    Test reliability before production.
    

---
  #### **Name**
Huge Prompts in Schema
  #### **Description**
Long descriptions in Pydantic fields
  #### **Why Bad**
    Wastes tokens.
    Can confuse the model.
    Harder to maintain.
    
  #### **What To Do Instead**
    Keep field descriptions concise.
    Use examples in system prompt instead.
    One sentence per field max.
    