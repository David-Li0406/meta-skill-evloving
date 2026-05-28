# Error Types Reference

Comprehensive reference for Claude Code error types, their meanings, and resolution strategies.

---

## API Errors

Errors from the Claude API service.

### rate_limit_error

**Message:** `You have exceeded your rate limit. Please wait before making more requests.`

**Cause:**
- Too many requests in short period
- Token usage exceeded per-minute limit
- Concurrent request limit reached

**Resolution:**
1. Wait 60 seconds before retrying
2. Reduce request frequency
3. Batch operations to reduce API calls

**Prevention:**
- Add delays between rapid operations
- Use `/compact` to reduce token usage
- Avoid loops that make many API calls

---

### overloaded_error

**Message:** `The API is temporarily overloaded. Please try again later.`

**Cause:**
- High demand on Claude API
- Service temporarily at capacity
- Infrastructure scaling in progress

**Resolution:**
1. Wait 30-60 seconds
2. Retry with exponential backoff
3. If persistent, check status.anthropic.com

**Prevention:**
- Schedule non-urgent tasks for off-peak hours
- Implement retry logic with backoff
- Have fallback workflows ready

---

### context_length_exceeded

**Message:** `The request exceeded the maximum context length.`

**Cause:**
- Too many tokens in conversation
- Large file reads accumulated
- Long session without clearing

**Resolution:**
1. Run `/compact` to summarize context
2. Use `/clear` if compact insufficient
3. Split large file reads into chunks

**Prevention:**
- Monitor context size with `/status`
- Use file read limits (`--limit` parameter)
- Clear context periodically for long sessions

---

### authentication_error

**Message:** `Invalid API key or authentication token.`

**Cause:**
- API key expired or invalid
- Credentials file corrupted
- Wrong authentication method

**Resolution:**
1. Run `claude auth login` to re-authenticate
2. Check `~/.claude/.credentials.json` exists
3. Verify key is valid in Anthropic console

**Prevention:**
- Don't manually edit credentials file
- Use `claude auth` commands for auth changes
- Monitor key expiration dates

---

### invalid_request_error

**Message:** `The request was invalid or malformed.`

**Cause:**
- Malformed JSON in request
- Invalid parameter values
- Missing required fields

**Resolution:**
1. Check input format matches expected
2. Review error details for specific field
3. Validate JSON syntax if applicable

**Prevention:**
- Use Claude Code's built-in tools (not raw API)
- Validate inputs before operations
- Follow documented parameter formats

---

### api_error

**Message:** `An unexpected error occurred on the API side.`

**Cause:**
- Server-side issue
- Temporary infrastructure problem
- Bug in API processing

**Resolution:**
1. Retry after 30 seconds
2. If persistent, check status.anthropic.com
3. Use `/bug` to report if reproducible

**Prevention:**
- Implement retry logic
- Have fallback workflows
- Monitor API status

---

### insufficient_quota_error

**Message:** `Your account has insufficient credits or quota.`

**Cause:**
- Usage quota exhausted
- Billing issue with account
- Plan limits reached

**Resolution:**
1. Check quota in Anthropic console
2. Upgrade plan or add credits
3. Wait for quota reset (monthly)

**Prevention:**
- Monitor usage in console
- Set up usage alerts
- Use efficient prompting strategies

---

## Tool Errors

Errors from Claude Code's built-in tools.

### permission_denied

**Message:** `Permission denied: [tool] is not allowed.`

**Cause:**
- Tool not in allowed list
- Session-level permission denied
- MCP tool not approved

**Resolution:**
1. Run `/permissions`
2. Allow the specific tool
3. For MCP tools, re-approve when prompted

**Prevention:**
- Pre-configure permissions in settings.json
- Use `--dangerously-skip-permissions` only in trusted environments
- Add tool patterns to allow list

---

### file_not_found

**Message:** `File not found: [path]`

**Cause:**
- Path doesn't exist
- Typo in filename
- Wrong working directory
- File was deleted/moved

**Resolution:**
1. Verify path with `ls` or `Glob`
2. Check working directory with `pwd`
3. Search for file with `Glob` pattern

**Prevention:**
- Use absolute paths when possible
- Verify paths before operations
- Use `Glob` to find files first

---

### directory_not_found

**Message:** `Directory not found: [path]`

**Cause:**
- Directory doesn't exist
- Parent path is wrong
- Permissions prevent access

**Resolution:**
1. Check parent directory exists
2. Create directory with `mkdir -p`
3. Verify permissions on parent

**Prevention:**
- Create directory structure first
- Use `mkdir -p` for nested paths
- Validate paths before operations

---

### read_error

**Message:** `Cannot read file: [path]`

**Cause:**
- File is binary/non-text
- Encoding issues
- File locked by another process
- Permission denied

**Resolution:**
1. Check file type with `file [path]`
2. Try different encoding
3. Wait if file is locked
4. Check read permissions

**Prevention:**
- Identify file type before reading
- Handle binary files appropriately
- Check permissions upfront

---

### write_error

**Message:** `Cannot write to file: [path]`

**Cause:**
- Directory doesn't exist
- No write permission
- Disk full
- File locked

**Resolution:**
1. Create parent directory
2. Check write permissions
3. Check disk space
4. Wait if file locked

**Prevention:**
- Verify directory exists
- Check permissions before write
- Monitor disk space

---

### command_failed

**Message:** `Command failed with exit code [n]: [command]`

**Cause:**
- Command returned non-zero exit code
- Command not found
- Syntax error in command
- Missing dependencies

**Resolution:**
1. Check stderr for details
2. Verify command exists (`which [cmd]`)
3. Test command manually
4. Install missing dependencies

**Prevention:**
- Validate commands before running
- Check dependencies exist
- Use full paths for commands

---

### timeout

**Message:** `Operation timed out after [n]ms`

**Cause:**
- Operation took too long
- Network latency
- Resource contention
- Infinite loop in script

**Resolution:**
1. Increase timeout if appropriate
2. Simplify operation
3. Break into smaller chunks
4. Fix infinite loops

**Prevention:**
- Set appropriate timeouts
- Break large operations into chunks
- Add progress indicators
- Test operations before full run

---

## Context Errors

Errors related to conversation context and session state.

### context_overflow

**Message:** `Context window exceeded. Please reduce context size.`

**Cause:**
- Too much conversation history
- Large file contents in context
- Many tool outputs accumulated

**Resolution:**
1. Run `/compact` to summarize
2. If severe, use `/clear`
3. Start new session for clean slate

**Prevention:**
- Use `/compact` periodically
- Limit file read sizes
- Clear context after major tasks

---

### memory_limit

**Message:** `Memory limit exceeded. Please clear some memory banks.`

**Cause:**
- Too much stored in memory
- Large memory objects
- Memory not cleared after use

**Resolution:**
1. View memory with `/memory`
2. Clear unused memory banks
3. Reduce memory object sizes

**Prevention:**
- Clear memory when no longer needed
- Store only essential data
- Use external storage for large data

---

### session_expired

**Message:** `Session has expired. Please start a new session.`

**Cause:**
- Session timed out
- Server restarted
- Connection lost for extended period

**Resolution:**
1. Start new session
2. Re-establish context if needed
3. Use `/resume` if available

**Prevention:**
- Stay active in session
- Use shorter sessions for critical work
- Save important context externally

---

### state_corruption

**Message:** `Session state is corrupted. Please restart.`

**Cause:**
- Interrupted operation
- Bug in state management
- Concurrent access issue

**Resolution:**
1. Run `/clear` to reset state
2. Restart Claude Code
3. Report with `/bug` if reproducible

**Prevention:**
- Avoid interrupting operations
- Don't run multiple Claude instances
- Keep Claude Code updated

---

## MCP Errors

Errors from Model Context Protocol servers.

### mcp_connection_failed

**Message:** `Failed to connect to MCP server: [server]`

**Cause:**
- Server not running
- Wrong connection parameters
- Network/firewall issue

**Resolution:**
1. Check server is running
2. Verify .mcp.json configuration
3. Test network connectivity

**Prevention:**
- Validate MCP config before use
- Use health checks for servers
- Set appropriate timeouts

---

### mcp_timeout

**Message:** `MCP server [server] timed out`

**Cause:**
- Server slow to respond
- Network latency
- Server processing complex request

**Resolution:**
1. Increase timeout (`MCP_TIMEOUT` env var)
2. Simplify request
3. Check server health

**Prevention:**
- Set appropriate timeouts
- Optimize server performance
- Break large requests into chunks

---

### mcp_tool_error

**Message:** `MCP tool [tool] returned error: [message]`

**Cause:**
- Tool implementation error
- Invalid parameters
- Server-side issue

**Resolution:**
1. Check tool documentation
2. Verify parameters are correct
3. Check server logs for details

**Prevention:**
- Validate parameters before calling
- Handle tool errors gracefully
- Test tools in isolation

---

### mcp_server_crashed

**Message:** `MCP server [server] crashed unexpectedly`

**Cause:**
- Bug in server code
- Resource exhaustion
- Unhandled exception

**Resolution:**
1. Restart MCP server
2. Check server logs
3. Report bug to server maintainer

**Prevention:**
- Use stable MCP servers
- Monitor server health
- Set up automatic restarts

---

## Hook Errors

Errors from custom hooks.

### hook_not_found

**Message:** `Hook script not found: [path]`

**Cause:**
- Script path is wrong
- Script was moved/deleted
- Permission to access denied

**Resolution:**
1. Verify script path exists
2. Check file permissions
3. Update hook configuration

**Prevention:**
- Use absolute paths
- Verify hooks after configuration
- Version control hook scripts

---

### hook_execution_failed

**Message:** `Hook [name] failed with exit code [n]`

**Cause:**
- Script error
- Missing dependencies
- Invalid output format

**Resolution:**
1. Test script manually
2. Check stderr for errors
3. Verify output format

**Prevention:**
- Test hooks before using
- Add error handling to scripts
- Validate hook output format

---

### hook_timeout

**Message:** `Hook [name] timed out after [n]ms`

**Cause:**
- Script too slow
- Infinite loop
- Waiting for unavailable resource

**Resolution:**
1. Optimize script
2. Increase timeout
3. Fix infinite loops

**Prevention:**
- Keep hooks fast (<5s)
- Add timeouts to external calls
- Test with large inputs

---

### hook_invalid_output

**Message:** `Hook [name] returned invalid JSON`

**Cause:**
- Script output not valid JSON
- Extra output before/after JSON
- Script wrote to stdout incorrectly

**Resolution:**
1. Validate output with `jq`
2. Ensure only JSON on stdout
3. Send non-JSON to stderr

**Prevention:**
- Test JSON output
- Use `echo '{}' | jq` pattern
- Separate logs from output

---

## Network Errors

Errors related to network connectivity.

### connection_refused

**Message:** `Connection refused to [host]:[port]`

**Cause:**
- Service not running
- Wrong host/port
- Firewall blocking

**Resolution:**
1. Check service is running
2. Verify host and port
3. Check firewall rules

**Prevention:**
- Validate connectivity before use
- Use health checks
- Document required ports

---

### dns_resolution_failed

**Message:** `Could not resolve hostname: [hostname]`

**Cause:**
- Hostname doesn't exist
- DNS server issue
- Network disconnected

**Resolution:**
1. Check hostname spelling
2. Test DNS with `nslookup`
3. Check network connection

**Prevention:**
- Use IP addresses as fallback
- Test connectivity at startup
- Handle DNS failures gracefully

---

### ssl_certificate_error

**Message:** `SSL certificate verification failed`

**Cause:**
- Invalid certificate
- Expired certificate
- Self-signed certificate

**Resolution:**
1. Update CA certificates
2. Check system time is correct
3. Use proper certificates

**Prevention:**
- Keep certificates updated
- Use trusted CAs
- Monitor certificate expiration

---

### connection_timeout

**Message:** `Connection timed out to [host]`

**Cause:**
- Network latency
- Host unreachable
- Firewall dropping packets

**Resolution:**
1. Check network connectivity
2. Increase timeout
3. Check firewall rules

**Prevention:**
- Set appropriate timeouts
- Use health checks
- Have fallback endpoints

---

## Exit Codes Reference

Common exit codes from Bash commands:

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Misuse of shell command |
| 126 | Command invoked cannot execute |
| 127 | Command not found |
| 128 | Invalid exit argument |
| 128+n | Fatal signal n |
| 130 | Ctrl+C termination |
| 137 | Kill signal (SIGKILL) |
| 139 | Segmentation fault |
| 143 | Termination signal (SIGTERM) |
| 255 | Exit status out of range |

### Interpreting Exit Codes

```bash
# Check last command exit code
echo $?

# Exit code in error message
# "Command failed with exit code 127"
# --> 127 = command not found

# Signal-based exit
# Exit code 137 = 128 + 9 (SIGKILL)
# Exit code 143 = 128 + 15 (SIGTERM)
```

---

## Error Severity Levels

| Level | Description | Action |
|-------|-------------|--------|
| **Fatal** | Cannot continue | Stop, fix root cause |
| **Error** | Operation failed | Retry or fallback |
| **Warning** | Potential issue | Monitor, may need attention |
| **Info** | Informational | No action needed |
| **Debug** | Diagnostic info | For troubleshooting only |

### Determining Severity

- **Fatal**: System crash, data corruption, security issue
- **Error**: Operation failed but system stable
- **Warning**: Non-ideal but workable
- **Info**: Expected behavior notification
- **Debug**: Internal state information
