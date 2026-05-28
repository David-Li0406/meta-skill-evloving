# MCP Integration & Context Standards (Dec 2025)
## 1. The "Universal Adapter" Audit
MCP is the standard protocol for connecting AI models to tools and data. Review for interoperability and context efficiency.
### Context Budgeting
- [ ] **Token Overhead:** Does the MCP server definition exceed 5k tokens? (Target: Keep server definitions lean to preserve the ~200k context window).
- [ ] **On-Demand Loading:** Is the server configured for "Progressive Disclosure"? (Don't load the full tool schema until the agent requests it).
- [ ] **Context Duplication:** Ensure the MCP server doesn't provide data already present in `CLAUDE.md` or other skills.
### Security & Tool Permissions
- [ ] **Tool Isolation:** Does the MCP server follow the Principle of Least Privilege? (e.g., A GitHub MCP server should only have access to specific repos, not the whole org).
- [ ] **Environment Injection:** Are environment variables for MCP servers (API keys, DB strings) stored in a secure vault, not the `mcp-config.json`?
- [ ] **Bash/Write Gating:** Does the MCP server allow unrestricted shell access? (🔴 **Critical:** Must require human confirmation for `write_file` or `execute_command` tools).
## 2. MCP Performance & Latency
- [ ] **Cold Start:** If the MCP server is serverless (e.g., an AWS Lambda MCP), is it optimized for sub-100ms response times to prevent "Agent Stalling"?
- [ ] **Data Locality:** Is the MCP server deployed in the same region as the model inference to minimize "Tool-Call Latency"?
- [ ] **Streaming Support:** Does the server support streaming tool outputs for long-running data retrievals?
## 3. Review Questions for MCP Configuration
1. Does this agent *really* need access to this entire database schema via MCP, or just a specific view?
2. How does the agent handle an MCP "Server Down" state? (Is there a graceful fallback?)
3. Are we logging the inputs and outputs of every MCP tool call for the audit trail?
