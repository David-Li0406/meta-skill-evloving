---
name: nodes-quick-index
description: "Quick reference to all 110+ Kailash nodes. Use when asking 'node list', 'all nodes', 'node reference', 'what nodes', 'available nodes', or 'node catalog'."
---

# Nodes Quick Index

Quick reference to all 115+ tested and validated Kailash workflow nodes.

> **Skill Metadata**
> Category: `nodes`
> Priority: `CRITICAL`
> SDK Version: `0.9.25+`
> Related Skills: All node-specific skills
> Related Subagents: `pattern-expert` (node selection, workflow patterns)

## Quick Decision: Which Node to Use?

| Task | Use This Node | Not PythonCodeNode |
|------|---------------|-------------------|
| Read CSV/Excel | `CSVReaderNode`, `ExcelReaderNode` | Read CSV/Excel | `CSVReaderNode`, `ExcelReaderNode` | ❌ `pd.read_csv()` |
| Call REST API | `HTTPRequestNode`, `RESTClientNode` | ❌ `requests.get()` |
| Query Database | `AsyncSQLDatabaseNode` ⭐ | ❌ `cursor.execute()` |
| Use LLM/AI | `LLMAgentNode`, `IterativeLLMAgentNode` ⭐ | ❌ OpenAI SDK |
| Filter/Transform | `FilterNode`, `DataTransformer` | ❌ List comprehensions |
| Route Logic | `SwitchNode`, `ConditionalRouterNode` | ❌ if/else blocks |
| Send Alerts | `DiscordAlertNode`, `EmailSenderNode` | ❌ SMTP/webhook code |
| Distributed Transactions | `DistributedTransactionManagerNode` | ❌ Manual 2PC/Saga |

## Node Categories (115+ total)

### 📁 Data I/O (20+ nodes)
```python
# File operations
from kailash.nodes.data import CSVReaderNode, CSVWriterNode
from kailash.nodes.data import JSONReaderNode, JSONWriterNode
from kailash.nodes.data import TextReaderNode, ExcelReaderNode

# Database
from kailash.nodes.data import AsyncSQLDatabaseNode  # ⭐⭐⭐ Production recommended
from kailash.nodes.data import WorkflowConnectionPool  # ⭐⭐ Connection pooling
from kailash.nodes.data import QueryRouterNode  # ⭐⭐⭐ Intelligent routing
from kailash.nodes.data import SQLDatabaseNode  # Simple queries
```

### 🤖 AI/ML (20+ nodes)
```python
# LLM Agents
from kailash.nodes.ai import LLMAgentNode, IterativeLLMAgentNode  # Real MCP execution
from kailash.nodes.ai import MonitoredLLMAgentNode
from kailash.nodes.ai import EmbeddingGeneratorNode

# Coordination
from kailash.nodes.ai import A2AAgentNode, A2ACoordinatorNode
from kailash.nodes.ai import SharedMemoryPoolNode

# Self-organizing
from kailash.nodes.ai import AgentPoolManagerNode
from kailash.nodes.ai import SelfOrganizingAgentNode
from kailash.nodes.ai import TeamFormationNode
```

### 🌐 API (10+ nodes)
```python
from kailash.nodes.api import HTTPRequestNode, AsyncHTTPRequestNode
from kailash.nodes.api import RESTClientNode, AsyncRESTClientNode
from kailash.nodes.api import GraphQLClientNode
from kailash.nodes.api import RateLimitedAPINode
```

### 🔀 Logic (10+ nodes)
```python
from kailash.nodes.logic import SwitchNode, MergeNode
from kailash.nodes.logic import ConditionalRouterNode
from kailash.nodes.logic import LoopNode, WhileNode
from kailash.nodes.logic import ConvergenceCheckerNode
```

### 🔄 Transform (15+ nodes)
```python
from kailash.nodes.transform import FilterNode
from kailash.nodes.transform import DataTransformer
from kailash.nodes.transform import AggregationNode
from kailash.nodes.transform import TextSplitterNode
```

### 💻 Code Execution (6+ nodes)
```python
from kailash.nodes.code import PythonCodeNode  # Use sparingly!
from kailash.nodes.code import MCPToolNode
from kailash.nodes.code import ScriptRunnerNode
```

### 🔒 Security & Admin (15+ nodes)
```python
from kailash.nodes.security import OAuth2Node, JWTValidatorNode
from kailash.nodes.security import AuthenticationNode, EncryptionNode
from kailash.nodes.admin import UserManagementNode, RoleManagementNode
from kailash.nodes.admin import PermissionCheckNode, AccessControlNode
```

### 📊 Monitoring (5+ nodes)
```python
from kailash.nodes.monitoring import TransactionMetricsNode
from kailash.nodes.monitoring import TransactionMonitorNode
from kailash.nodes.monitoring import DeadlockDetectorNode
from kailash.nodes.monitoring import RaceConditionDetectorNode
from kailash.nodes.monitoring import PerformanceAnomalyNode
```

### 🔄 Distributed Transactions (4+ nodes)
```python
from kailash.nodes.transaction import DistributedTransactionManagerNode  # Auto-select
from kailash.nodes.transaction import SagaCoordinatorNode  # High availability
from kailash.nodes.transaction import SagaStepNode
from kailash.nodes.transaction import TwoPhaseCommitCoordinatorNode  # Strong consistency
```

### 📢 Alerts (5+ nodes)
```python
from kailash.nodes.alerts import DiscordAlertNode, SlackAlertNode
from kailash.nodes.alerts import EmailSenderNode, TeamsAlertNode
from kailash.nodes.alerts import PagerDutyAlertNode
```

## Most Used Nodes (Top 10)

```python
from kailash.nodes.data import CSVReaderNode, AsyncSQLDatabaseNode, WorkflowConnectionPool
from kailash.nodes.ai import LLMAgentNode, IterativeLLMAgentNode  # Enhanced with MCP
from kailash.nodes.api import HTTPRequestNode, RESTClientNode
from kailash.nodes.logic import SwitchNode, MergeNode
from kailash.nodes.transform import FilterNode
```

## Node Selection by Task

### Data Processing
- **CSV/Excel**: [`nodes-data-reference`](nodes-data-reference.md)
- **Database**: `AsyncSQLDatabaseNode`, `WorkflowConnectionPool`, `QueryRouterNode`
- **API**: [`nodes-api-reference`](nodes-api-reference.md)

### AI/ML
- **LLM**: [`nodes-ai-reference`](nodes-ai-reference.md)
- **Embeddings**: `EmbeddingGeneratorNode`
- **Multi-Agent**: `A2AAgentNode`, `SelfOrganizingAgentNode`

### Logic & Control
- **Routing**: [`nodes-logic-reference`](nodes-logic-reference.md)
- **Conditionals**: `SwitchNode`, `ConditionalRouterNode`
- **Loops**: `LoopNode`, `WhileNode`

### Enterprise
- **Security**: `OAuth2Node`, `JWTValidatorNode`, `EncryptionNode`
- **Admin**: [`nodes-admin-reference`](nodes-admin-reference.md)
- **Monitoring**: [`nodes-monitoring-reference`](nodes-monitoring-reference.md)
- **Transactions**: [`nodes-transaction-reference`](nodes-transaction-reference.md)

## Navigation Strategy

1. **Quick task lookup** → Use table above
2. **Category browsing** → Use category-specific skills
3. **Full details** → See comprehensive-node-catalog.md (2194 lines)

## When NOT to Use Nodes

**❌ Avoid PythonCodeNode for:**
- File I/O operations (use CSVReaderNode, etc.)
- HTTP requests (use HTTPRequestNode)
- Database queries (use AsyncSQLDatabaseNode)
- Data filtering/transformation (use FilterNode, DataTransformer)
- Authentication (use OAuth2Node, JWTValidatorNode)
- Standard ML operations (use specialized AI nodes)

**✅ Use PythonCodeNode only for:**
- Ollama/local LLM integration
- Complex custom business logic
- Temporary prototyping

## Related Skills

- **Data Nodes**: [`nodes-data-reference`](nodes-data-reference.md)
- **AI Nodes**: [`nodes-ai-reference`](nodes-ai-reference.md)
- **API Nodes**: [`nodes-api-reference`](nodes-api-reference.md)
- **Database Nodes**: [`nodes-database-reference`](nodes-database-reference.md)
- **Transform Nodes**: [`nodes-transform-reference`](nodes-transform-reference.md)
- **Code Nodes**: [`nodes-code-reference`](nodes-code-reference.md)
- **Logic Nodes**: [`nodes-logic-reference`](nodes-logic-reference.md)
- **File Nodes**: [`nodes-file-reference`](nodes-file-reference.md)
- **Monitoring Nodes**: [`nodes-monitoring-reference`](nodes-monitoring-reference.md)
- **Transaction Nodes**: [`nodes-transaction-reference`](nodes-transaction-reference.md)
- **Admin Nodes**: [`nodes-admin-reference`](nodes-admin-reference.md)

## When to Escalate to Subagent

Use `pattern-expert` subagent when:
- Choosing between multiple node options
- Building complex multi-node workflows
- Optimizing node selection for performance
- Troubleshooting node parameter issues

## Documentation References

### Primary Sources
- **Node Index**: [`sdk-users/2-core-concepts/nodes/node-index.md`](../../../../sdk-users/2-core-concepts/nodes/node-index.md)
- **Node Selection Guide**: [`sdk-users/2-core-concepts/nodes/node-selection-guide.md`](../../../../sdk-users/2-core-concepts/nodes/node-selection-guide.md)
- **Comprehensive Catalog**: [`sdk-users/2-core-concepts/nodes/comprehensive-node-catalog.md`](../../../../sdk-users/2-core-concepts/nodes/comprehensive-node-catalog.md)

## Quick Tips

- Start with specialized nodes before considering PythonCodeNode
- Use async variants (AsyncSQLDatabaseNode, AsyncHTTPRequestNode) for production
- Leverage enterprise nodes (monitoring, transactions, security) for production
- Check node-specific skills for detailed usage patterns

## Version Notes

- **v0.9.25+**: IterativeLLMAgentNode with real MCP execution
- **v0.6.6+**: QueryBuilder, QueryCache, OptimisticLockingNode
- **v0.6.5+**: Enhanced MCP support across AI nodes

<!-- Trigger Keywords: node list, all nodes, node reference, what nodes, available nodes, node catalog, kailash nodes, node index, node types, workflow nodes -->
