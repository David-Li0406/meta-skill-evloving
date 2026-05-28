---
id: langchain-patterns
name: "LangChain Patterns"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# LangChain Patterns

## Overview

LangChain is a framework for building LLM applications. It provides abstractions for prompts, chains, agents, memory, and retrieval, enabling rapid development of complex AI systems.

## When to Use

- Rapid prototyping of LLM applications
- Building conversational agents
- RAG implementations
- Multi-step reasoning workflows
- When you need composable LLM components
- Integration with many different LLMs and tools

## Key Concepts

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                      LangChain Stack                         │
├─────────────────────────────────────────────────────────────┤
│  Agents          - Autonomous decision making               │
│  Chains          - Sequence of operations                   │
│  Memory          - Conversation history                     │
│  Retrievers      - Document retrieval                       │
│  Prompts         - Template management                      │
│  LLMs/Chat Models- Model interfaces                         │
└─────────────────────────────────────────────────────────────┘
```

### LCEL (LangChain Expression Language)

LCEL is the modern way to compose LangChain components using a pipe (`|`) syntax.

## Implementation

### Basic Setup

```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Initialize model
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Simple chain with LCEL
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}")
])

chain = prompt | llm | StrOutputParser()

# Invoke
response = chain.invoke({"input": "What is the capital of France?"})
print(response)
```

### Prompt Templates

```python
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder
)

# Basic template
simple_prompt = ChatPromptTemplate.from_template(
    "Translate '{text}' to {language}."
)

# Chat template with system message
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {role} expert."),
    ("user", "{question}")
])

# With message history placeholder
history_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}")
])

# Few-shot template
from langchain_core.prompts import FewShotChatMessagePromptTemplate

examples = [
    {"input": "2+2", "output": "4"},
    {"input": "3+3", "output": "6"},
]

example_prompt = ChatPromptTemplate.from_messages([
    ("user", "{input}"),
    ("assistant", "{output}")
])

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples
)

final_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a calculator."),
    few_shot_prompt,
    ("user", "{input}")
])
```

### Output Parsers

```python
from langchain_core.output_parsers import (
    StrOutputParser,
    JsonOutputParser,
    PydanticOutputParser
)
from pydantic import BaseModel, Field
from typing import List

# String output
str_parser = StrOutputParser()

# JSON output
json_parser = JsonOutputParser()

# Pydantic output
class MovieReview(BaseModel):
    title: str = Field(description="Movie title")
    rating: float = Field(ge=0, le=10, description="Rating out of 10")
    pros: List[str] = Field(description="Positive points")
    cons: List[str] = Field(description="Negative points")

pydantic_parser = PydanticOutputParser(pydantic_object=MovieReview)

# Get format instructions
format_instructions = pydantic_parser.get_format_instructions()

# Chain with Pydantic parser
review_prompt = ChatPromptTemplate.from_messages([
    ("system", f"Analyze movie reviews. {format_instructions}"),
    ("user", "Review: {review}")
])

review_chain = review_prompt | llm | pydantic_parser

result = review_chain.invoke({
    "review": "Amazing visuals but the plot was confusing. 7/10."
})
print(result.title, result.rating)
```

### Chains with LCEL

```python
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableLambda,
    RunnableParallel
)

# Sequential chain
def step1(x):
    return x.upper()

def step2(x):
    return x + "!!!"

sequential = RunnableLambda(step1) | RunnableLambda(step2)
print(sequential.invoke("hello"))  # "HELLO!!!"

# Parallel execution
parallel = RunnableParallel(
    uppercase=RunnableLambda(lambda x: x.upper()),
    length=RunnableLambda(lambda x: len(x)),
    original=RunnablePassthrough()
)
print(parallel.invoke("hello"))
# {"uppercase": "HELLO", "length": 5, "original": "hello"}

# Branching
from langchain_core.runnables import RunnableBranch

classifier_chain = (
    ChatPromptTemplate.from_template("Classify as positive/negative: {text}")
    | llm
    | StrOutputParser()
)

positive_chain = ChatPromptTemplate.from_template(
    "Generate a happy response for: {text}"
) | llm | StrOutputParser()

negative_chain = ChatPromptTemplate.from_template(
    "Generate an empathetic response for: {text}"
) | llm | StrOutputParser()

branched = RunnableBranch(
    (lambda x: "positive" in x["classification"].lower(), positive_chain),
    negative_chain  # default
)
```

### Memory

```python
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Simple memory
memory = ChatMessageHistory()
memory.add_user_message("Hi!")
memory.add_ai_message("Hello! How can I help?")

# Chain with memory
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("user", "{input}")
])

chain = prompt | llm | StrOutputParser()

# Session-based memory
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

# Use with session
response = chain_with_history.invoke(
    {"input": "My name is Bob"},
    config={"configurable": {"session_id": "user123"}}
)

response = chain_with_history.invoke(
    {"input": "What's my name?"},
    config={"configurable": {"session_id": "user123"}}
)
```

### RAG with LangChain

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough

# Initialize embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Create documents
documents = [
    Document(page_content="LangChain is a framework for LLM apps", metadata={"source": "docs"}),
    Document(page_content="LCEL is the expression language for chains", metadata={"source": "docs"}),
]

# Create vector store
vectorstore = Chroma.from_documents(documents, embeddings)

# Create retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# RAG prompt
rag_prompt = ChatPromptTemplate.from_template("""
Answer based on the context below.

Context: {context}

Question: {question}

Answer:""")

# Format docs helper
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# RAG chain
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

answer = rag_chain.invoke("What is LangChain?")
```

### Tools and Agents

```python
from langchain_core.tools import tool
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain import hub

# Define tools
@tool
def get_weather(location: str) -> str:
    """Get the current weather for a location."""
    return f"Weather in {location}: Sunny, 72°F"

@tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        return str(eval(expression))
    except:
        return "Error calculating"

tools = [get_weather, calculate]

# Create agent
prompt = hub.pull("hwchase17/openai-tools-agent")
agent = create_openai_tools_agent(llm, tools, prompt)

# Create executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5
)

# Run agent
response = agent_executor.invoke({
    "input": "What's the weather in Paris? Also, what's 25 * 4?"
})
```

### Document Loading and Processing

```python
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    WebBaseLoader,
    DirectoryLoader
)
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter
)

# Load documents
text_loader = TextLoader("document.txt")
pdf_loader = PyPDFLoader("document.pdf")
web_loader = WebBaseLoader("https://example.com")

# Load directory
dir_loader = DirectoryLoader(
    "./documents",
    glob="**/*.txt",
    loader_cls=TextLoader
)
documents = dir_loader.load()

# Split documents
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    separators=["\n\n", "\n", " ", ""]
)

splits = text_splitter.split_documents(documents)

# With metadata
for i, split in enumerate(splits):
    split.metadata["chunk_id"] = i
```

### Streaming

```python
from langchain_core.output_parsers import StrOutputParser

# Basic streaming
chain = prompt | llm | StrOutputParser()

for chunk in chain.stream({"input": "Tell me a story"}):
    print(chunk, end="", flush=True)

# Async streaming
async def stream_response(query: str):
    async for chunk in chain.astream({"input": query}):
        yield chunk

# Stream with callbacks
from langchain_core.callbacks import StreamingStdOutCallbackHandler

streaming_llm = ChatOpenAI(
    model="gpt-4o",
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()]
)
```

### Custom Runnables

```python
from langchain_core.runnables import Runnable
from typing import Any

class CustomRunnable(Runnable):
    """Custom runnable component."""

    def __init__(self, config: dict = None):
        self.config = config or {}

    def invoke(self, input: Any, config=None) -> Any:
        """Process input."""
        # Your logic here
        return f"Processed: {input}"

    async def ainvoke(self, input: Any, config=None) -> Any:
        """Async process input."""
        return self.invoke(input, config)

# Use in chain
custom = CustomRunnable({"setting": "value"})
chain = custom | llm | StrOutputParser()
```

### Callbacks and Tracing

```python
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from typing import Any, Dict, List
import logging

class LoggingCallbackHandler(BaseCallbackHandler):
    """Custom callback for logging."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs
    ):
        self.logger.info(f"LLM started with {len(prompts)} prompts")

    def on_llm_end(self, response: LLMResult, **kwargs):
        self.logger.info(f"LLM finished")

    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict, **kwargs):
        self.logger.info(f"Chain started: {serialized.get('name')}")

    def on_chain_end(self, outputs: Dict, **kwargs):
        self.logger.info(f"Chain finished")

    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs):
        self.logger.info(f"Tool started: {serialized.get('name')}")

# Use callbacks
llm_with_callbacks = ChatOpenAI(
    model="gpt-4o",
    callbacks=[LoggingCallbackHandler()]
)

# Or with invoke
chain.invoke(
    {"input": "Hello"},
    config={"callbacks": [LoggingCallbackHandler()]}
)
```

### LangSmith Integration

```python
import os

# Set environment variables for tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-api-key"
os.environ["LANGCHAIN_PROJECT"] = "my-project"

# All chains are now traced automatically
chain = prompt | llm | StrOutputParser()
response = chain.invoke({"input": "Hello"})

# Or use context manager
from langsmith import traceable

@traceable
def my_function(query: str) -> str:
    return chain.invoke({"input": query})
```

### Production Patterns

```python
from langchain_core.runnables import RunnableConfig
from langchain_core.runnables.utils import ConfigurableField
from typing import Optional

# Configurable chain
configurable_llm = ChatOpenAI(model="gpt-4o").configurable_fields(
    model=ConfigurableField(
        id="model",
        name="Model",
        description="The model to use"
    ),
    temperature=ConfigurableField(
        id="temperature",
        name="Temperature",
        description="Sampling temperature"
    )
)

chain = prompt | configurable_llm | StrOutputParser()

# Use with different configs
response = chain.invoke(
    {"input": "Hello"},
    config={"configurable": {"model": "gpt-4o-mini", "temperature": 0}}
)

# Fallback pattern
from langchain_core.runnables import RunnableWithFallbacks

primary_llm = ChatOpenAI(model="gpt-4o")
fallback_llm = ChatOpenAI(model="gpt-4o-mini")

robust_llm = primary_llm.with_fallbacks([fallback_llm])

# Retry pattern
from langchain_core.runnables import RunnableRetry

retrying_chain = chain.with_retry(
    stop_after_attempt=3,
    wait_exponential_jitter=True
)

# Batch processing
responses = chain.batch([
    {"input": "Question 1"},
    {"input": "Question 2"},
    {"input": "Question 3"}
], config={"max_concurrency": 5})
```

## Best Practices

1. **Use LCEL**
   - Modern, composable syntax
   - Built-in streaming support
   - Better error handling

2. **Modular Design**
   - Break chains into reusable components
   - Use custom runnables for complex logic
   - Test components independently

3. **Memory Management**
   - Choose appropriate memory type
   - Limit conversation history
   - Clear memory when needed

4. **Error Handling**
   - Use fallbacks for reliability
   - Implement retries for transient errors
   - Log failures for debugging

5. **Observability**
   - Enable LangSmith tracing
   - Use callbacks for monitoring
   - Track costs and latency

## Common Pitfalls

1. **Legacy API** - Using deprecated Chain classes instead of LCEL
2. **Memory Leaks** - Not clearing conversation history
3. **No Error Handling** - Chains fail without fallbacks
4. **Blocking Calls** - Not using async for concurrent requests
5. **Over-complexity** - Building complex chains when simple suffices
6. **No Tracing** - Debugging production issues blind

## References

- [LangChain Documentation](https://python.langchain.com/)
- [LangChain Expression Language](https://python.langchain.com/docs/expression_language/)
- [LangSmith](https://smith.langchain.com/)
- [LangChain Hub](https://smith.langchain.com/hub)
