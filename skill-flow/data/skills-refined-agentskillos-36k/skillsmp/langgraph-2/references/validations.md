# Langgraph - Validations

## Message List Without Reducer

### **Id**
state-without-reducer
### **Severity**
high
### **Type**
regex
### **Pattern**
messages:\s*list(?!\[.*Annotated)
### **Message**
Message list without reducer will overwrite instead of append.
### **Fix Action**
Use Annotated[list, add_messages] for message fields
### **Applies To**
  - *.py

## END Used as String

### **Id**
end-as-string
### **Severity**
high
### **Type**
regex
### **Pattern**
return\s*["']end["']|return\s*["']END["']
### **Message**
Use END constant, not string 'end' or 'END'.
### **Fix Action**
from langgraph.graph import END; return END
### **Applies To**
  - *.py

## Invoke Without Thread Config

### **Id**
invoke-without-config
### **Severity**
medium
### **Type**
regex
### **Pattern**
\.invoke\(\{[^}]+\}\s*\)(?!\s*,|\s*\n\s*,)
### **Message**
invoke() without config loses conversation state.
### **Fix Action**
Add config={'configurable': {'thread_id': '...'}}
### **Applies To**
  - *.py

## Using StateGraph Without Compile

### **Id**
graph-not-compiled
### **Severity**
high
### **Type**
regex
### **Pattern**
StateGraph\([^)]*\)\s*\n(?:[^c]|c[^o]|co[^m])*\.invoke
### **Message**
StateGraph must be compiled before invoke.
### **Fix Action**
app = graph.compile(); app.invoke(...)
### **Applies To**
  - *.py

## ToolNode Without Error Handling

### **Id**
toolnode-no-error-handling
### **Severity**
medium
### **Type**
regex
### **Pattern**
ToolNode\(\s*\w+\s*\)
### **Negative Pattern**
handle_tool_errors
### **Message**
ToolNode without error handling will crash on tool failures.
### **Fix Action**
Use ToolNode(tools, handle_tool_errors=True)
### **Applies To**
  - *.py

## Sync Call in Async Function

### **Id**
sync-in-async
### **Severity**
medium
### **Type**
regex
### **Pattern**
async def.*\n(?:.*\n)*?.*(?<!a)invoke\([^)]*\)
### **Message**
Sync invoke() in async function blocks event loop.
### **Fix Action**
Use ainvoke() in async contexts
### **Applies To**
  - *.py

## Agent Loop Without Max Iterations

### **Id**
no-max-iterations
### **Severity**
medium
### **Type**
regex
### **Pattern**
add_edge\([^,]+,\s*["'][^"']+["']\s*\).*\n.*add_edge\(["'][^"']+["']\s*,
### **Negative Pattern**
iterations|max_|count|limit
### **Message**
Agent loop without iteration limit may run forever.
### **Fix Action**
Add iteration counter in state and check in routing
### **Applies To**
  - *.py

## SQLite Memory Checkpointer in Production

### **Id**
memory-checkpointer-in-prod
### **Severity**
medium
### **Type**
regex
### **Pattern**
SqliteSaver\.from_conn_string\(["']:memory:["']\)
### **Message**
In-memory SQLite loses state on restart. Use persistent storage in production.
### **Fix Action**
Use PostgresSaver or file-based SQLite for production
### **Applies To**
  - *.py

## Graph Without START Edge

### **Id**
missing-start-edge
### **Severity**
high
### **Type**
regex
### **Pattern**
StateGraph\([^)]*\)(?:.*\n)*?compile\(\)
### **Negative Pattern**
add_edge\(START
### **Message**
Graph needs an edge from START to first node.
### **Fix Action**
Add graph.add_edge(START, 'first_node')
### **Applies To**
  - *.py