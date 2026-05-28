# Messages Reference

## imessage-recent

Get recent iMessages (SQLite direct access - works without Messages.app).

```bash
imessage-recent              # Last 24 hours (default)
imessage-recent 6            # Last 6 hours
imessage-recent -d 3         # Last 3 days
imessage-recent -l 10        # Limit to 10 messages
imessage-recent -p "lunch"   # Filter by keyword
imessage-recent -n           # Check for notation patterns
imessage-recent -j           # JSON output
```

**Notation patterns** (`-n` flag):
- `(ghsj->cc:`, `(cc->ghsj:`, `(cc-suggest:`, `(cc-warn:`
- `>>move:`, `>>archive`, `>>defer:`
- `[MUST]`, `[SHOULD]`

## imessage-search

Advanced search across **complete message history** (decodes attributedBody BLOBs).

```bash
imessage-search --felicitations                 # Birthday/holiday messages
imessage-search --pattern "lunch"               # Custom keyword
imessage-search --keywords "meeting,call"       # Multiple keywords
imessage-search --felicitations -l 10           # Limit contacts
imessage-search --pattern "resume" --csv        # CSV output
imessage-search --felicitations -o ~/Desktop/contacts.csv
```

**Features**:
- Complete message history (not just recent)
- Decodes modern iMessage attributedBody BLOB format
- Groups results by contact with counts and dates
- Auto-installs dependencies on first run (~10s setup)

**Use cases**:
- Find felicitation contacts for holiday greetings
- Search historical messages for keywords
- Build contact lists

## Examples

**"Any recent messages about lunch?"**
```bash
imessage-recent -p "lunch"
```

**"Check for user directives"**
```bash
imessage-recent -n
```

**"Find contacts I've sent birthday messages to"**
```bash
imessage-search --felicitations
```

## Limitations

- `imessage-recent`: Only ~70 messages with plain text field (fast)
- `imessage-search`: Complete history but slower (decodes BLOBs)
- Sending messages requires user interaction (read-only access)
