# Jules API Skill v2.0 Updates

**Date**: 2026-01-11
**Version**: 2.0.0

## Summary

Updated the Jules API skill based on real-world experience debugging stuck session 14848423526856432295. Added comprehensive activities API support, stuck session debugging workflows, and improved API usage patterns.

---

## Key Changes

### 1. Activities API Support

**Added to SKILL.md** (lines 279-344):
- Complete response structure documentation
- Usage patterns for debugging stuck sessions
- Examples for understanding context and monitoring progress
- Important notes about activity size and ordering

**Key Features**:
```python
# Read activities to debug stuck sessions
activities = client.get_activities(session_id)['activities']

# Show last 10 activities
for activity in activities[-10:]:
    if activity['originator'] == 'agent':
        print(activity['agentMessaged']['agentMessage'])
```

### 2. Stuck Session Debugging Workflow

**Added to SKILL.md** (lines 541-632):
- 4-step workflow for unsticking sessions
- Real example from session 14848423526856432295
- Common stuck session patterns and solutions
- Targeted feedback templates

**Real Case Study**:
- Session stuck for 14+ hours in `AWAITING_USER_FEEDBACK`
- Read activities to identify test failure issues
- Sent targeted message with schema fix and priority guidance
- Session resumed and changed to `IN_PROGRESS` within minutes

### 3. Session ID Handling

**Updated in jules_client.py**:
- All methods now accept both `"sessions/123"` and `"123"` formats
- Automatic extraction: `session_id.split('/')[-1]`
- Methods updated: `get_session`, `send_message`, `approve_plan`, `get_activities`

**Example**:
```python
# Both formats work
client.get_session("sessions/123456789")
client.get_session("123456789")
```

### 4. CLI Improvements

**Added to jules_client.py**:
- Better formatted output for all commands
- New `check` command to quickly see if session needs attention
- `--json` flag for programmatic usage
- Improved error messages

**New Commands**:
```bash
# Check if session needs attention
jules_client.py check 123456789
# Returns: ⚠️ Session is waiting for user feedback

# Get JSON output
jules_client.py get 123456789 --json

# View activities
jules_client.py activities 123456789
```

### 5. Helper Methods

**Added to jules_client.py** (lines 195-219):
```python
def check_session_needs_attention(session_id: str) -> tuple[bool, str]:
    """Check if a session needs user attention.

    Returns:
        Tuple of (needs_attention: bool, reason: str)
    """
    session = self.get_session(session_id)
    state = session.get('state', 'UNKNOWN')

    if state == 'AWAITING_USER_FEEDBACK':
        return True, "Session is waiting for user feedback"
    elif state == 'AWAITING_PLAN_APPROVAL':
        return True, "Session plan needs approval"
    # ... etc
```

### 6. Direct API Usage Priority

**Added to SKILL.md** (lines 168-178):
- Emphasizes using direct HTTP calls (curl, httpx) instead of Python client
- Language-agnostic approach
- Transparent and maintainable

**Philosophy**:
1. **Primary**: Use direct HTTP calls (curl in bash, httpx/requests in Python)
2. **Secondary**: Use jules_client.py only as convenience for complex workflows

**Added Examples**:
- Python with httpx (recommended)
- Bash with curl
- Moved Python client to "Alternative" section

---

## Files Modified

### 1. SKILL.md
- Added "Usage Philosophy" section emphasizing direct API usage
- Expanded "Get Session Activities" with response structure and patterns
- Added "Debugging Stuck Sessions" section with 4-step workflow
- Added real-world case study from session 14848423526856432295
- Updated "Error Handling" with session ID format notes
- Added comprehensive curl and httpx examples
- Moved Python client to "Alternative" section

### 2. jules_client.py
- Added import for `json`
- Updated all methods to handle both session ID formats
- Added `check_session_needs_attention()` helper method
- Improved CLI output formatting
- Added `--json` flag support
- Added `check` command
- Better error messages in CLI

### 3. README.md
- Added "What's New in v2.0" section
- Updated Quick Start with new commands
- Added examples for `check` and `activities` commands
- Updated Python library usage examples
- Added Changelog section

### 4. New File: UPDATES_V2.md (this file)
- Comprehensive documentation of all changes

---

## Migration Guide

### For Existing Users

**No breaking changes** - all existing code continues to work.

**Recommended Updates**:

1. **Use direct API calls** when possible:
   ```python
   # Old (still works)
   from repo_client import JulesClient
   client = JulesClient()
   session = client.create_session(...)

   # New (recommended)
   import httpx
   response = httpx.post(
       "https://jules.googleapis.com/v1alpha/sessions",
       headers={"X-Goog-Api-Key": API_KEY},
       json={...}
   )
   ```

2. **Add activity checking** for stuck sessions:
   ```python
   # New feature
   activities = httpx.get(
       f"{BASE_URL}/sessions/{session_id}/activities",
       headers=headers
   ).json()['activities']

   # Check last few activities
   for activity in activities[-5:]:
       print(activity['originator'], activity.get('agentMessaged', {}).get('agentMessage', '')[:100])
   ```

3. **Use helper method** for monitoring:
   ```python
   # New helper
   needs_attention, reason = client.check_session_needs_attention(session_id)
   if needs_attention:
       print(f"Action needed: {reason}")
   ```

---

## Testing

All changes have been tested with:
- Session 14848423526856432295 (stuck session that was successfully unstuck)
- Session 151282220707368107 (newly created parallel personas session)

**Verified**:
- ✅ Activities API returns proper structure
- ✅ Session ID handling works with both formats
- ✅ CLI outputs formatted correctly
- ✅ `check` command detects stuck sessions
- ✅ `--json` flag works for all commands
- ✅ Direct API calls work as documented

---

## Benefits

### 1. Better Debugging
- Can now understand what Jules is asking when stuck
- Real-world patterns for common issues
- Actionable examples from actual stuck session

### 2. Improved Usability
- Simpler API (just HTTP calls)
- Works in any language/environment
- No dependency on Python client
- Clearer what's happening under the hood

### 3. Enhanced Monitoring
- Quick `check` command for status
- Activity parsing for context
- Helper methods for common tasks

### 4. Real-World Validation
- Based on actual debugging session
- Proven workflow that successfully unstuck a 14+ hour stuck session
- Patterns extracted from real conversations

---

## Future Enhancements

Potential improvements for v3.0:
- [ ] Retry logic with exponential backoff
- [ ] Batch operations (create multiple sessions)
- [ ] Session templating (reusable prompts)
- [ ] Webhook support for notifications
- [ ] Session metrics and analytics
- [ ] Auto-resume for `AWAITING_USER_FEEDBACK` with common patterns

---

## References

- Original stuck session: 14848423526856432295
- New parallel personas session: 151282220707368107
- Jules API docs: https://developers.google.com/repo/api/reference/rest
- GitHub issue: N/A (internal improvement)

---

## Credits

**Author**: Claude Sonnet 4.5
**Tested by**: franklinbaldo (user)
**Inspired by**: Real-world debugging of stuck Jules sessions in egregora project

---

**Questions?** See SKILL.md for full documentation or README.md for quick start guide.
