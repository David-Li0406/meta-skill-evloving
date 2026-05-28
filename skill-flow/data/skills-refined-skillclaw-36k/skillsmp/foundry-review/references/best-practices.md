# Best Practices

## DO
- Run LSP structural pre-check before expensive AI review
- Use `documentSymbol` to verify expected classes/functions exist
- Use `findReferences` and `incomingCalls` to assess deviation impact
- Validate that spec_id and task_id/phase_id are provided
- Present findings clearly with categorized deviations
- Highlight recommendations for remediation
- Note AI consensus from multiple tool perspectives
- Provide context from the fidelity assessment
- Surface the saved JSON report path so the caller can inspect the full consensus artifacts

## DON'T
- Skip LSP pre-check for files with language server support
- Attempt to manually implement review logic (the MCP tool handles it)
- Read spec files directly with Read/Python/jq/Bash (the MCP tool loads them)
- Use grep/sed/awk to parse JSON—the MCP responses are already structured
- Ignore the MCP tool's consensus analysis
- Make up review findings not sourced from the MCP output
- Perform additional analysis beyond the MCP consensus results
- Open the persisted JSON report; reference its filepath instead
