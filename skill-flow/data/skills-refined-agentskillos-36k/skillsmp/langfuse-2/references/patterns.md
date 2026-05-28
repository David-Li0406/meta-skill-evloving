# Langfuse

## Patterns


---
  #### **Name**
Basic Tracing Setup
  #### **Description**
Instrument LLM calls with Langfuse
  #### **When To Use**
Any LLM application
  #### **Implementation**
    from langfuse import Langfuse
    
    # Initialize client
    langfuse = Langfuse(
        public_key="pk-...",
        secret_key="sk-...",
        host="https://cloud.langfuse.com"  # or self-hosted URL
    )
    
    # Create a trace for a user request
    trace = langfuse.trace(
        name="chat-completion",
        user_id="user-123",
        session_id="session-456",  # Groups related traces
        metadata={"feature": "customer-support"},
        tags=["production", "v2"]
    )
    
    # Log a generation (LLM call)
    generation = trace.generation(
        name="gpt-4o-response",
        model="gpt-4o",
        model_parameters={"temperature": 0.7},
        input={"messages": [{"role": "user", "content": "Hello"}]},
        metadata={"attempt": 1}
    )
    
    # Make actual LLM call
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello"}]
    )
    
    # Complete the generation with output
    generation.end(
        output=response.choices[0].message.content,
        usage={
            "input": response.usage.prompt_tokens,
            "output": response.usage.completion_tokens
        }
    )
    
    # Score the trace
    trace.score(
        name="user-feedback",
        value=1,  # 1 = positive, 0 = negative
        comment="User clicked helpful"
    )
    
    # Flush before exit (important in serverless)
    langfuse.flush()
    

---
  #### **Name**
OpenAI Integration
  #### **Description**
Automatic tracing with OpenAI SDK
  #### **When To Use**
OpenAI-based applications
  #### **Implementation**
    from langfuse.openai import openai
    
    # Drop-in replacement for OpenAI client
    # All calls automatically traced
    
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello"}],
        # Langfuse-specific parameters
        name="greeting",  # Trace name
        session_id="session-123",
        user_id="user-456",
        tags=["test"],
        metadata={"feature": "chat"}
    )
    
    # Works with streaming
    stream = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Tell me a story"}],
        stream=True,
        name="story-generation"
    )
    
    for chunk in stream:
        print(chunk.choices[0].delta.content, end="")
    
    # Works with async
    import asyncio
    from langfuse.openai import AsyncOpenAI
    
    async_client = AsyncOpenAI()
    
    async def main():
        response = await async_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Hello"}],
            name="async-greeting"
        )
    

---
  #### **Name**
LangChain Integration
  #### **Description**
Trace LangChain applications
  #### **When To Use**
LangChain-based applications
  #### **Implementation**
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langfuse.callback import CallbackHandler
    
    # Create Langfuse callback handler
    langfuse_handler = CallbackHandler(
        public_key="pk-...",
        secret_key="sk-...",
        host="https://cloud.langfuse.com",
        session_id="session-123",
        user_id="user-456"
    )
    
    # Use with any LangChain component
    llm = ChatOpenAI(model="gpt-4o")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("user", "{input}")
    ])
    
    chain = prompt | llm
    
    # Pass handler to invoke
    response = chain.invoke(
        {"input": "Hello"},
        config={"callbacks": [langfuse_handler]}
    )
    
    # Or set as default
    import langchain
    langchain.callbacks.manager.set_handler(langfuse_handler)
    
    # Then all calls are traced
    response = chain.invoke({"input": "Hello"})
    
    # Works with agents, retrievers, etc.
    from langchain.agents import create_openai_tools_agent
    
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)
    
    result = agent_executor.invoke(
        {"input": "What's the weather?"},
        config={"callbacks": [langfuse_handler]}
    )
    

---
  #### **Name**
Prompt Management
  #### **Description**
Version and deploy prompts
  #### **When To Use**
Managing prompts across environments
  #### **Implementation**
    from langfuse import Langfuse
    
    langfuse = Langfuse()
    
    # Fetch prompt from Langfuse
    # (Create in UI or via API first)
    prompt = langfuse.get_prompt("customer-support-v2")
    
    # Get compiled prompt with variables
    compiled = prompt.compile(
        customer_name="John",
        issue="billing question"
    )
    
    # Use with OpenAI
    response = openai.chat.completions.create(
        model=prompt.config.get("model", "gpt-4o"),
        messages=compiled,
        temperature=prompt.config.get("temperature", 0.7)
    )
    
    # Link generation to prompt version
    trace = langfuse.trace(name="support-chat")
    generation = trace.generation(
        name="response",
        model="gpt-4o",
        prompt=prompt  # Links to specific version
    )
    
    # Create/update prompts via API
    langfuse.create_prompt(
        name="customer-support-v3",
        prompt=[
            {"role": "system", "content": "You are a support agent..."},
            {"role": "user", "content": "{{user_message}}"}
        ],
        config={
            "model": "gpt-4o",
            "temperature": 0.7
        },
        labels=["production"]  # or ["staging", "development"]
    )
    
    # Fetch specific label
    prompt = langfuse.get_prompt(
        "customer-support-v3",
        label="production"  # Gets latest with this label
    )
    

---
  #### **Name**
Evaluation and Scoring
  #### **Description**
Evaluate LLM outputs systematically
  #### **When To Use**
Quality assurance and improvement
  #### **Implementation**
    from langfuse import Langfuse
    
    langfuse = Langfuse()
    
    # Manual scoring in code
    trace = langfuse.trace(name="qa-flow")
    
    # After getting response
    trace.score(
        name="relevance",
        value=0.85,  # 0-1 scale
        comment="Response addressed the question"
    )
    
    trace.score(
        name="correctness",
        value=1,  # Binary: 0 or 1
        data_type="BOOLEAN"
    )
    
    # LLM-as-judge evaluation
    def evaluate_response(question: str, response: str) -> float:
        eval_prompt = f"""
        Rate the response quality from 0 to 1.
    
        Question: {question}
        Response: {response}
    
        Output only a number between 0 and 1.
        """
    
        result = openai.chat.completions.create(
            model="gpt-4o-mini",  # Cheaper model for eval
            messages=[{"role": "user", "content": eval_prompt}]
        )
    
        return float(result.choices[0].message.content.strip())
    
    # Score asynchronously
    score = evaluate_response(question, response)
    trace.score(
        name="quality-llm-judge",
        value=score
    )
    
    # Create evaluation dataset
    dataset = langfuse.create_dataset(name="support-qa-v1")
    
    # Add items to dataset
    langfuse.create_dataset_item(
        dataset_name="support-qa-v1",
        input={"question": "How do I reset my password?"},
        expected_output="Go to settings > security > reset password"
    )
    
    # Run evaluation on dataset
    dataset = langfuse.get_dataset("support-qa-v1")
    
    for item in dataset.items:
        # Generate response
        response = generate_response(item.input["question"])
    
        # Link to dataset item
        trace = langfuse.trace(name="eval-run")
        trace.generation(
            name="response",
            input=item.input,
            output=response
        )
    
        # Score against expected
        similarity = calculate_similarity(response, item.expected_output)
        trace.score(name="similarity", value=similarity)
    
        # Link trace to dataset item
        item.link(trace, "eval-run-1")
    

---
  #### **Name**
Decorator Pattern
  #### **Description**
Clean instrumentation with decorators
  #### **When To Use**
Function-based applications
  #### **Implementation**
    from langfuse.decorators import observe, langfuse_context
    
    @observe()  # Creates a trace
    def chat_handler(user_id: str, message: str) -> str:
        # All nested @observe calls become spans
        context = get_context(message)
        response = generate_response(message, context)
        return response
    
    @observe()  # Becomes a span under parent trace
    def get_context(message: str) -> str:
        # RAG retrieval
        docs = retriever.get_relevant_documents(message)
        return "\n".join([d.page_content for d in docs])
    
    @observe(as_type="generation")  # LLM generation span
    def generate_response(message: str, context: str) -> str:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"Context: {context}"},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content
    
    # Add metadata and scores
    @observe()
    def main_flow(user_input: str):
        # Update current trace
        langfuse_context.update_current_trace(
            user_id="user-123",
            session_id="session-456",
            tags=["production"]
        )
    
        result = process(user_input)
    
        # Score the trace
        langfuse_context.score_current_trace(
            name="success",
            value=1 if result else 0
        )
    
        return result
    
    # Works with async
    @observe()
    async def async_handler(message: str):
        result = await async_generate(message)
        return result
    

## Anti-Patterns


---
  #### **Name**
Not Flushing in Serverless
  #### **Description**
Missing langfuse.flush() before exit
  #### **Why Bad**
    Traces are batched.
    Serverless may exit before flush.
    Data is lost.
    
  #### **What To Do Instead**
    Always call langfuse.flush() at end.
    Use context managers where available.
    Consider sync mode for critical traces.
    

---
  #### **Name**
Tracing Everything
  #### **Description**
Instrumenting every tiny function
  #### **Why Bad**
    Noisy traces.
    Performance overhead.
    Hard to find important info.
    
  #### **What To Do Instead**
    Focus on: LLM calls, key logic, user actions.
    Group related operations.
    Use meaningful span names.
    

---
  #### **Name**
No User/Session IDs
  #### **Description**
Traces without user context
  #### **Why Bad**
    Can't debug specific users.
    Can't track sessions.
    Analytics limited.
    
  #### **What To Do Instead**
    Always pass user_id and session_id.
    Use consistent identifiers.
    Add relevant metadata.
    

---
  #### **Name**
Ignoring Scores
  #### **Description**
Tracing without evaluation
  #### **Why Bad**
    Can see what happened, not quality.
    No feedback loop.
    Can't measure improvement.
    
  #### **What To Do Instead**
    Add user feedback scores.
    Implement LLM-as-judge.
    Track key quality metrics.
    