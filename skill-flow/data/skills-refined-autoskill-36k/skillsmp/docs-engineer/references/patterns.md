# Documentation Engineer

## Patterns


---
  #### **Name**
README Structure
  #### **Description**
Essential README for any project
  #### **When**
Creating or updating project README
  #### **Example**
    # Project Name
    
    One-sentence description of what this does and why you'd use it.
    
    ## Quick Start
    
    ```bash
    # Installation
    pip install memory-service
    
    # Basic usage
    from mind import Memory
    
    memory = Memory("Your memory content")
    await memory.save()
    ```
    
    ## Why Memory Service?
    
    - **Semantic retrieval**: Find memories by meaning, not keywords
    - **Automatic consolidation**: Long-term memory without manual curation
    - **Privacy-first**: Your memories stay yours
    
    ## Installation
    
    ```bash
    pip install memory-service
    
    # With optional vector support
    pip install memory-service[vectors]
    ```
    
    ## Basic Usage
    
    ```python
    from mind import Agent, Memory
    
    # Create an agent
    agent = Agent("my-agent")
    
    # Store a memory
    memory = await agent.remember(
        "User prefers dark mode",
        salience=0.8
    )
    
    # Retrieve relevant memories
    memories = await agent.recall("user preferences")
    ```
    
    ## Documentation
    
    - [Full Documentation](https://docs.memory-service.io)
    - [API Reference](https://docs.memory-service.io/api)
    - [Tutorials](https://docs.memory-service.io/tutorials)
    - [Contributing](./CONTRIBUTING.md)
    
    ## License
    
    MIT - see [LICENSE](./LICENSE)
    

---
  #### **Name**
API Documentation
  #### **Description**
Clear, complete API documentation
  #### **When**
Documenting any API endpoint
  #### **Example**
    # OpenAPI documentation example
    
    openapi: 3.0.0
    info:
      title: Memory Service API
      version: 1.0.0
      description: |
        The Memory Service API enables semantic memory management for AI agents.
    
        ## Authentication
        All endpoints require Bearer token authentication.
    
        ## Rate Limits
        - 1000 requests/hour for standard tier
        - 10000 requests/hour for enterprise tier
    
    paths:
      /memories:
        post:
          summary: Create a memory
          description: |
            Creates a new memory for the authenticated agent. The memory
            will be embedded and indexed for semantic retrieval.
    
            **Note**: Memories are processed asynchronously. Use the
            `callback_url` parameter to be notified when processing completes.
          operationId: createMemory
          tags:
            - Memories
          requestBody:
            required: true
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/CreateMemoryRequest'
                example:
                  content: "User prefers dark mode for UI"
                  salience: 0.8
                  tags: ["preferences", "ui"]
          responses:
            '201':
              description: Memory created successfully
              content:
                application/json:
                  schema:
                    $ref: '#/components/schemas/Memory'
                  example:
                    id: "mem_abc123"
                    content: "User prefers dark mode for UI"
                    salience: 0.8
                    created_at: "2024-01-15T10:30:00Z"
            '400':
              description: Invalid request
              content:
                application/json:
                  schema:
                    $ref: '#/components/schemas/Error'
                  example:
                    code: "VALIDATION_ERROR"
                    message: "Content is required"
            '429':
              description: Rate limit exceeded
              headers:
                Retry-After:
                  description: Seconds until rate limit resets
                  schema:
                    type: integer
    

---
  #### **Name**
Tutorial Structure
  #### **Description**
Step-by-step tutorial that actually teaches
  #### **When**
Creating any tutorial or guide
  #### **Example**
    # Building Your First Memory Agent
    
    By the end of this tutorial, you'll have a working agent that
    remembers context across conversations.
    
    **Time**: 15 minutes
    **Prerequisites**: Python 3.10+, pip
    **You'll learn**:
    - How to create an agent
    - How to store and retrieve memories
    - How to use semantic search
    
    ## Step 1: Install Memory Service
    
    ```bash
    pip install memory-service
    ```
    
    Verify installation:
    ```bash
    python -c "import mind; print(mind.__version__)"
    # Should print: 5.0.0
    ```
    
    ## Step 2: Create Your First Agent
    
    Create a file called `my_agent.py`:
    
    ```python
    from mind import Agent
    
    # Create an agent with a unique identifier
    agent = Agent("my-first-agent")
    
    print(f"Agent created: {agent.id}")
    ```
    
    Run it:
    ```bash
    python my_agent.py
    # Output: Agent created: my-first-agent
    ```
    
    ## Step 3: Store a Memory
    
    Add to your file:
    
    ```python
    import asyncio
    from mind import Agent
    
    async def main():
        agent = Agent("my-first-agent")
    
        # Store a memory
        memory = await agent.remember(
            "The user's name is Alice",
            salience=0.9  # High importance
        )
    
        print(f"Stored memory: {memory.id}")
    
    asyncio.run(main())
    ```
    
    **What's happening**:
    - `remember()` stores the content as a memory
    - `salience` indicates importance (0.0 to 1.0)
    - Higher salience memories are prioritized in recall
    
    ## Step 4: Retrieve Memories
    
    Now let's recall relevant memories:
    
    ```python
    # Add after storing
    memories = await agent.recall("what is the user's name?")
    
    for m in memories:
        print(f"[{m.salience:.1f}] {m.content}")
    ```
    
    Output:
    ```
    [0.9] The user's name is Alice
    ```
    
    **How it works**: Memory Service uses semantic search, so "what is the
    user's name?" matches "The user's name is Alice" even though
    the exact words differ.
    
    ## What's Next?
    
    - [Memory Types](./memory-types.md) - Learn about episodic vs semantic memory
    - [Consolidation](./consolidation.md) - How memories are strengthened over time
    - [API Reference](../api/memories.md) - Complete memory API documentation
    

---
  #### **Name**
Code Comments
  #### **Description**
Effective inline documentation
  #### **When**
Adding comments to code
  #### **Example**
    # Good comments explain WHY, not WHAT
    
    # BAD: Describes what code does (obvious from reading)
    # Increment counter by 1
    counter += 1
    
    # GOOD: Explains non-obvious reasoning
    # Using counter instead of len() because memories
    # may be added concurrently during iteration
    counter += 1
    
    # BAD: Obvious from type signature
    def get_user(user_id: str) -> User:
        """Gets a user."""
    
    # GOOD: Explains behavior and edge cases
    def get_user(user_id: str) -> User:
        """
        Retrieve a user by ID.
    
        Uses cached value if available (TTL: 5 min).
        Raises UserNotFoundError if user doesn't exist.
    
        Args:
            user_id: The unique user identifier (format: usr_xxx)
    
        Returns:
            User object with profile data
    
        Raises:
            UserNotFoundError: If user ID doesn't exist
            DatabaseError: If database is unavailable
        """
    
    # GOOD: Explains complex algorithm
    def calculate_salience(memory: Memory) -> float:
        """
        Calculate memory salience using recency-weighted access pattern.
    
        Salience decays with time (72h half-life) but increases with
        access frequency. Based on ACT-R memory model.
    
        Formula: base_salience * recency_decay * (1 + log(access_count))
        """
    

## Anti-Patterns


---
  #### **Name**
Documenting the Obvious
  #### **Description**
Comments that repeat what code says
  #### **Why**
Adds noise without value. Gets out of sync with code.
  #### **Instead**
Document the why, not the what

---
  #### **Name**
Outdated Documentation
  #### **Description**
Docs that no longer match reality
  #### **Why**
Wrong docs are worse than no docs. Create false confidence.
  #### **Instead**
Update docs with code. Automate where possible.

---
  #### **Name**
Wall of Text
  #### **Description**
Long paragraphs without code examples
  #### **Why**
Developers skim. Long text is skipped.
  #### **Instead**
Short explanation → code example → repeat

---
  #### **Name**
Assuming Context
  #### **Description**
Starting with details without explaining basics
  #### **Why**
New users are lost. They leave.
  #### **Instead**
Quick start first. Details for those who seek them.

---
  #### **Name**
Tribal Knowledge
  #### **Description**
Critical info only in people's heads
  #### **Why**
Bus factor. Onboarding hell. Knowledge lost when people leave.
  #### **Instead**
Write it down. Architecture decisions, gotchas, processes.