# Langfuse - Sharp Edges

## Missing Flush

### **Id**
missing-flush
### **Summary**
Traces not appearing in dashboard
### **Severity**
high
### **Situation**
No traces visible after running code
### **Why**
  Langfuse batches traces.
  Script exits before flush.
  Network issues silently fail.
  
### **Solution**
  from langfuse import Langfuse
  
  langfuse = Langfuse()
  
  # WRONG - script may exit before flush
  trace = langfuse.trace(name="my-trace")
  # ... do work
  # Script ends
  
  # CORRECT - explicit flush
  trace = langfuse.trace(name="my-trace")
  # ... do work
  langfuse.flush()  # Wait for batch to send
  
  # For serverless (Lambda, Cloud Functions)
  def handler(event, context):
      trace = langfuse.trace(name="handler")
      try:
          result = process(event)
          return result
      finally:
          langfuse.flush()  # MUST flush before return
  
  # With decorators - auto-flush on function exit
  from langfuse.decorators import observe
  
  @observe()
  def my_function():
      # Auto-flushed when function returns
      pass
  
  # Force sync mode (slower but guaranteed)
  langfuse = Langfuse(
      enabled=True,
      debug=True,  # See what's happening
      flush_at=1,  # Flush every event (slow!)
  )
  
  # Check for errors
  langfuse.flush()
  if langfuse.auth_check():
      print("Connected!")
  else:
      print("Auth failed - check keys")
  
### **Symptoms**
  - Empty dashboard
  - No traces found
  - Works locally, fails in prod
### **Detection Pattern**
langfuse.*flush\(\)

## Decorator Context Lost

### **Id**
decorator-context-lost
### **Summary**
Nested spans not connected
### **Severity**
medium
### **Situation**
Spans appear as separate traces
### **Why**
  Context not propagated.
  Called from different thread.
  Async context lost.
  
### **Solution**
  from langfuse.decorators import observe, langfuse_context
  
  # WRONG - separate traces
  @observe()
  def parent():
      child()  # May not connect
  
  @observe()
  def child():
      pass
  
  # CORRECT - explicit context
  @observe()
  def parent():
      # Context automatically passed to @observe functions
      result = child()  # Will be nested
      return result
  
  @observe()
  def child():
      pass
  
  # For threading - pass context
  from langfuse.decorators import get_current_trace
  
  @observe()
  def parent():
      trace_id = langfuse_context.get_current_trace_id()
      # Pass to thread
      thread = Thread(target=child, args=(trace_id,))
      thread.start()
  
  def child(parent_trace_id):
      langfuse = Langfuse()
      span = langfuse.span(
          trace_id=parent_trace_id,
          name="child-span"
      )
      # ... work
      span.end()
  
  # For async - use async decorators
  @observe()
  async def async_parent():
      result = await async_child()  # Context preserved
      return result
  
  @observe()
  async def async_child():
      pass
  
### **Symptoms**
  - Separate unrelated traces
  - Missing parent-child relationships
  - "Orphan" spans
### **Detection Pattern**
@observe

## High Cardinality Names

### **Id**
high-cardinality-names
### **Summary**
Too many unique trace names
### **Severity**
medium
### **Situation**
Dashboard hard to navigate, slow
### **Why**
  Dynamic names create clutter.
  Can't aggregate metrics.
  UI performance degrades.
  
### **Solution**
  # WRONG - dynamic names
  trace = langfuse.trace(
      name=f"process-{user_id}-{timestamp}"  # Millions of names!
  )
  
  # CORRECT - static names with metadata
  trace = langfuse.trace(
      name="process-request",  # Fixed name
      user_id=user_id,  # Use built-in field
      metadata={"timestamp": timestamp}  # Additional context
  )
  
  # WRONG - variable in generation name
  generation = trace.generation(
      name=f"generate-{model_name}"  # Many models = many names
  )
  
  # CORRECT - model in metadata
  generation = trace.generation(
      name="llm-call",
      model=model_name,  # Proper field
      metadata={"variant": "a/b-test-1"}
  )
  
  # Good naming conventions:
  names = [
      "chat-completion",      # Action-based
      "rag-retrieval",        # Feature-based
      "summarize-document",   # Use-case-based
      "tool-call-weather",    # Tool-based (limited set)
  ]
  
  # Use tags for categorization
  trace = langfuse.trace(
      name="chat",
      tags=["production", "premium-user", "high-priority"]
  )
  
### **Symptoms**
  - Slow dashboard
  - Can't find traces
  - Meaningless aggregations
### **Detection Pattern**
name=f"|name=.*\{.*\}

## Missing Usage Tokens

### **Id**
missing-usage-tokens
### **Summary**
Cost tracking shows zero
### **Severity**
medium
### **Situation**
No cost data in dashboard
### **Why**
  Usage not passed to generation.
  Wrong format.
  Model not in pricing list.
  
### **Solution**
  # Get usage from OpenAI response
  response = openai.chat.completions.create(
      model="gpt-4o",
      messages=[{"role": "user", "content": "Hello"}]
  )
  
  # WRONG - not passing usage
  generation = trace.generation(
      name="response",
      output=response.choices[0].message.content
  )
  generation.end()
  
  # CORRECT - pass usage dict
  generation = trace.generation(
      name="response",
      model="gpt-4o",  # Required for pricing lookup
      input=messages,
      output=response.choices[0].message.content,
      usage={
          "input": response.usage.prompt_tokens,
          "output": response.usage.completion_tokens,
          "total": response.usage.total_tokens
      }
  )
  generation.end()
  
  # For streaming, accumulate usage
  full_response = ""
  input_tokens = 0
  output_tokens = 0
  
  for chunk in stream:
      if chunk.choices[0].delta.content:
          full_response += chunk.choices[0].delta.content
      if chunk.usage:  # Final chunk has usage
          input_tokens = chunk.usage.prompt_tokens
          output_tokens = chunk.usage.completion_tokens
  
  generation.end(
      output=full_response,
      usage={"input": input_tokens, "output": output_tokens}
  )
  
  # With OpenAI wrapper - automatic
  from langfuse.openai import openai
  # Usage tracked automatically
  
### **Symptoms**
  - $0.00 cost in dashboard
  - Missing token counts
  - Incomplete analytics
### **Detection Pattern**
usage.*prompt_tokens|usage.*input

## Prompt Version Mismatch

### **Id**
prompt-version-mismatch
### **Summary**
Prompt changes not reflected in traces
### **Severity**
medium
### **Situation**
Can't track which prompt version was used
### **Why**
  Not linking generation to prompt.
  Fetching but not associating.
  Wrong label/version.
  
### **Solution**
  from langfuse import Langfuse
  
  langfuse = Langfuse()
  
  # Fetch prompt
  prompt = langfuse.get_prompt("my-prompt", label="production")
  
  # WRONG - prompt not linked
  generation = trace.generation(
      name="response",
      input=prompt.compile(name="John")  # Prompt not tracked
  )
  
  # CORRECT - link prompt object
  generation = trace.generation(
      name="response",
      prompt=prompt,  # Links to version
      input=prompt.compile(name="John")
  )
  
  # Can also link by reference
  generation = trace.generation(
      name="response",
      prompt={
          "name": "my-prompt",
          "version": prompt.version  # Specific version
      }
  )
  
  # View in dashboard:
  # - See which prompt version used
  # - Compare performance across versions
  # - A/B test prompts
  
### **Symptoms**
  - Can't see prompt version
  - No prompt comparison
  - Lost experiment data
### **Detection Pattern**
get_prompt.*generation

## Self Hosted Config

### **Id**
self-hosted-config
### **Summary**
Self-hosted connection issues
### **Severity**
high
### **Situation**
Can't connect to self-hosted instance
### **Why**
  Wrong host URL.
  Network/firewall issues.
  Missing trailing slash.
  
### **Solution**
  from langfuse import Langfuse
  
  # WRONG - common mistakes
  langfuse = Langfuse(
      host="http://localhost:3000/"  # Trailing slash can cause issues
  )
  langfuse = Langfuse(
      host="langfuse.mycompany.com"  # Missing protocol
  )
  
  # CORRECT
  langfuse = Langfuse(
      public_key="pk-lf-...",
      secret_key="sk-lf-...",
      host="https://langfuse.mycompany.com"  # No trailing slash
  )
  
  # Debug connection
  langfuse = Langfuse(debug=True)  # Verbose logging
  
  # Check auth
  if not langfuse.auth_check():
      raise Exception("Langfuse auth failed")
  
  # Environment variables (recommended)
  # LANGFUSE_PUBLIC_KEY=pk-lf-...
  # LANGFUSE_SECRET_KEY=sk-lf-...
  # LANGFUSE_HOST=https://langfuse.mycompany.com
  
  langfuse = Langfuse()  # Reads from env
  
  # For Docker/K8s - check service name
  # host="http://langfuse:3000"  # Internal service name
  
### **Symptoms**
  - Connection refused
  - 401 Unauthorized
  - Timeout errors
### **Detection Pattern**
host=|LANGFUSE_HOST