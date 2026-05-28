# AI Engineering Patterns

## Raw Patterns (No Frameworks)

### Basic LLM Call Pattern

```python
import httpx

async def call_llm(messages: list[dict], model: str = "gpt-4") -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {settings.openai_api_key}"},
            json={"model": model, "messages": messages}
        )
        return response.json()["choices"][0]["message"]["content"]
```

### Conversation Memory (It's Just a List)

```python
class Conversation:
    def __init__(self, system_prompt: str):
        self.messages = [{"role": "system", "content": system_prompt}]

    async def chat(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})
        response = await call_llm(self.messages)
        self.messages.append({"role": "assistant", "content": response})
        return response
```

### Tool Calling Pattern

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather for a location",
            "parameters": {
                "type": "object",
                "properties": {"location": {"type": "string"}},
                "required": ["location"]
            }
        }
    }
]

async def call_with_tools(messages: list[dict]) -> dict:
    response = await client.post(
        "https://api.openai.com/v1/chat/completions",
        json={"model": "gpt-4", "messages": messages, "tools": tools}
    )
    result = response.json()["choices"][0]
    if result.get("finish_reason") == "tool_calls":
        return await execute_tools(result["message"]["tool_calls"])
    return result["message"]["content"]
```

### RAG Pattern

```python
async def rag_query(query: str, documents: list[str]) -> str:
    query_embedding = await get_embedding(query)
    relevant_docs = find_similar(query_embedding, documents, top_k=3)
    context = "\n".join(relevant_docs)

    messages = [
        {"role": "system", "content": f"Answer based on context:\n{context}"},
        {"role": "user", "content": query}
    ]
    return await call_llm(messages)

async def get_embedding(text: str) -> list[float]:
    response = await client.post(
        "https://api.openai.com/v1/embeddings",
        json={"model": "text-embedding-3-small", "input": text}
    )
    return response.json()["data"][0]["embedding"]
```

### Chunking Strategies

```python
def fixed_chunk(text: str, size: int = 500, overlap: int = 50) -> list[str]:
    chunks = []
    for i in range(0, len(text), size - overlap):
        chunks.append(text[i:i + size])
    return chunks

def semantic_chunk(text: str) -> list[str]:
    paragraphs = text.split("\n\n")
    return [p.strip() for p in paragraphs if p.strip()]
```

## LangChain Patterns

### Basic Chain

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{input}")
])
chain = prompt | llm
response = await chain.ainvoke({"input": "Hello"})
```

### RAG with LangChain

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(documents, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)
```

### LangGraph Agent

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class AgentState(TypedDict):
    messages: list
    next_action: str

def should_continue(state: AgentState) -> str:
    if state["next_action"] == "end":
        return END
    return "agent"

graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
graph.add_conditional_edges("agent", should_continue)
graph.set_entry_point("agent")
app = graph.compile()
```

### Production Best Practices

- Use LangSmith for tracing and debugging
- Implement caching (SQLite/Redis) for repeated queries
- Batch operations (10-20 items) for throughput
- Human-in-the-loop for critical decisions

## Google ADK Patterns

### Basic Agent

```python
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

def get_weather(location: str) -> str:
    """Get weather for a location.

    Args:
        location: City name or coordinates

    Returns:
        Weather description for the location
    """
    return f"Weather in {location}: Sunny, 22°C"

weather_tool = FunctionTool(get_weather)

root_agent = Agent(
    name="weather_agent",
    model="gemini-2.0-flash",
    instruction="Help users with weather queries",
    tools=[weather_tool]
)
```

### Multi-Agent System

```python
from google.adk.agents import Agent, SequentialAgent

researcher = Agent(
    name="researcher",
    model="gemini-2.0-flash",
    instruction="Research and gather information"
)

writer = Agent(
    name="writer",
    model="gemini-2.0-flash",
    instruction="Write based on research findings"
)

pipeline = SequentialAgent(
    name="content_pipeline",
    agents=[researcher, writer]
)
```

### Tool Docstring (Critical)

```python
def search_database(query: str, limit: int = 10) -> list[dict]:
    """Search the database for relevant records.

    The LLM uses this docstring to understand when and how to call
    this tool. Be specific about parameters and return values.

    Args:
        query: Search query string
        limit: Maximum number of results to return (default: 10)

    Returns:
        List of matching records with id, title, and content fields
    """
    pass
```

## Security Checklist

- [ ] Use environment variables for secrets (pydantic-settings)
- [ ] Validate all inputs with Pydantic models
- [ ] Use OAuth2/JWT authentication
- [ ] Configure CORS properly
- [ ] Use HTTPS in production
- [ ] Implement rate limiting
- [ ] Sanitize LLM outputs before execution
- [ ] PII detection/redaction for LLM inputs

## Performance

- Use async database drivers (asyncpg, aiomysql)
- Enable connection pooling
- Cache embeddings and repeated LLM calls
- Use `asyncio.gather()` for parallel operations
- Batch vector store operations
- Profile with py-spy or yappi
