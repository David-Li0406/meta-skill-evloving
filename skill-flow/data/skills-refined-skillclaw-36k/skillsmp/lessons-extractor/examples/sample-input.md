# Sample Input

This shows an example of Claude Code session log excerpts that would be processed by the lessons-extractor skill.

## Example Log Excerpt (Redacted)

```jsonl
{"type":"user","content":"Help me fix the failing tests in src/utils/parser.ts"}
{"type":"assistant","content":"I'll look at the failing tests and the parser implementation.","tool_calls":[{"name":"Read","arguments":{"file_path":"src/utils/parser.ts"}}]}
{"type":"tool_result","name":"Read","content":"[file contents...]"}
{"type":"assistant","content":"I see the issue. The parser isn't handling empty strings correctly.","tool_calls":[{"name":"Edit","arguments":{"file_path":"src/utils/parser.ts","old_string":"...","new_string":"..."}}]}
{"type":"tool_result","name":"Edit","content":"File updated successfully"}
{"type":"assistant","content":"Let me run the tests to verify the fix.","tool_calls":[{"name":"Bash","arguments":{"command":"npm test"}}]}
{"type":"tool_result","name":"Bash","content":"Tests: 15 passed, 0 failed"}
{"type":"user","content":"Great, thanks!"}
```

## What Gets Extracted

From this session, the lessons-extractor would identify:

1. **Task**: Fix failing tests in parser utility
2. **Outcome**: Success
3. **Workflow**: Read file → Identify issue → Edit → Verify with tests
4. **Lesson**: Always run tests after making fixes to verify

## Notes

- Real logs contain more metadata (timestamps, session IDs, etc.)
- Sensitive data like file paths and code content should be redacted
- The skill processes multiple sessions to find patterns across them
