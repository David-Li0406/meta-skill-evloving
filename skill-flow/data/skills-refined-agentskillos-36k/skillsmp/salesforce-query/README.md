# Salesforce Natural Language Query Skill

Query Salesforce data using natural language and get results as formatted tables in Claude Code.

## Quick Start

### 1. Install Dependencies
```bash
cd projects/salesforce-nl-chat
pip install -r requirements.txt
```

### 2. Get Salesforce Credentials
- Log into your Salesforce Developer Edition
- Open Developer Console → Execute Anonymous
- Run: `System.debug(UserInfo.getSessionId());`
- Copy the session ID from debug logs
- Note your instance URL (e.g., `https://yourorg.my.salesforce.com`)

### 3. Use the Skill
```
/salesforce-query show me all accounts in California
```

On first use, you'll be asked for:
- Instance URL
- Session ID

These are remembered for your chat session.

## Supported Objects
- Account
- Opportunity
- Contact
- Lead
- Case

## Example Queries

```
/salesforce-query show opportunities closing this quarter
/salesforce-query find all contacts from technology companies
/salesforce-query what are the open cases for Acme Corp
/salesforce-query list top 10 opportunities by amount
/salesforce-query show me accounts with revenue over 1 million
```

## How It Works

1. You provide a natural language query
2. Claude asks for Salesforce credentials (first time only)
3. Claude fetches object schemas from your Salesforce org
4. Claude generates SOQL query using real field names
5. Claude shows you the SOQL for transparency
6. Claude executes the query and displays results as a table

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for complete technical documentation.

## Files

```
projects/salesforce-nl-chat/
├── .claude/
│   └── skills/
│       └── salesforce-query/
│           ├── SKILL.md      # Skill instructions for Claude
│           └── README.md     # This file
├── scripts/
│   ├── describe.py           # Fetches Salesforce object schemas
│   └── query.py              # Executes SOQL queries
├── requirements.txt          # Python dependencies
└── ARCHITECTURE.md           # Technical documentation
```

## Security

- ✅ Credentials are never stored
- ✅ Only kept in chat session memory
- ✅ Read-only queries (no data modification)
- ✅ Respects your Salesforce permissions

## Troubleshooting

**Skill not recognized after creation:**
- Restart your Claude Code session
- Type `/` to see available skills

**Session ID expired:**
- Get a fresh session ID from Salesforce
- Provide it when Claude asks

**Field not found errors:**
- The skill will fetch your org's schema and retry
- Works with custom fields automatically

**No results:**
- Query is valid but no records match
- Try broadening your search criteria

## Limitations

- Maximum 2000 records per query (pagination handled automatically)
- Limited to 5 standard objects (can be extended)
- SOQL only (no SOSL text search yet)
- Read-only operations

## Need Help?

See the full skill documentation in [SKILL.md](.claude/skills/salesforce-query/SKILL.md) for:
- Detailed usage instructions
- SOQL patterns and examples
- Error handling guide
- Advanced query techniques
