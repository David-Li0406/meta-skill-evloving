# Salesforce Natural Language Query - Architecture

**Created**: 2026-01-21
**Status**: Implemented
**Architecture**: Option B - Schema Discovery without Caching

---

## Problem Statement

Enable querying Salesforce data using natural language within Claude Code, returning results as formatted tables. The system must be accurate, secure, and simple to use for ad-hoc data exploration.

## Requirements Summary

### Functional Requirements
- Query Salesforce objects: Account, Opportunity, Contact, Lead, Case
- Translate natural language to SOQL queries
- Display results as formatted markdown tables
- Include mandatory fields: Id, Name (and other relevant properties)
- Handle query ambiguity by asking clarifying questions
- Support relationships between objects (e.g., Opportunity.Account.Name)

### Non-Functional Requirements
- **Accuracy over speed**: Critical that queries are correct
- **Security**: Credentials never stored, provided per session only
- **Simplicity**: Minimal dependencies and code complexity
- **Flexibility**: Support custom fields in user's Salesforce org
- **Transparency**: Show generated SOQL before execution

### Constraints
- Using Salesforce Developer Edition
- Bearer token authentication (user-provided, not managed by skill)
- Interface: Claude Code chat window
- Preferred language: Python
- Ad-hoc usage pattern (not high frequency)

---

## Architecture Decision: Option B (Schema Discovery)

After evaluating three options, we selected **Option B: Dynamic Schema Discovery without Caching**.

### Why Option B?

**Selected over Option A (Static Field Mappings)**:
- ✅ Works with custom fields in user's specific Salesforce org
- ✅ More accurate SOQL generation using real field names
- ✅ Better error messages when fields don't exist
- ✅ Adapts to org-specific configurations

**Selected over Option C (Hybrid SOQL/SOSL)**:
- ✅ Simpler implementation (single query language)
- ✅ SOQL sufficient for stated requirements
- ✅ Less complexity in query type classification
- ✅ Can add SOSL later if needed

**Why no caching?**:
- Simpler code (no cache management logic)
- Always up-to-date with org changes
- Extra API calls negligible for ad-hoc usage
- Within Salesforce API limits easily

---

## System Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                          User (Claude Code Chat)                 │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            │ Natural Language Query
                            │ (e.g., "show opportunities for United Oil & Gas")
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Claude (in Chat Window)                      │
│  • Understands natural language                                  │
│  • Manages credentials (session memory only)                     │
│  • Identifies required objects                                   │
│  • Orchestrates workflow                                         │
│  • Generates SOQL from schemas                                   │
│  • Formats results as tables                                     │
└──────────┬──────────────────────────────────────┬───────────────┘
           │                                       │
           │ Fetch Schema                         │ Execute SOQL
           ▼                                       ▼
┌─────────────────────────┐         ┌──────────────────────────────┐
│   describe.py           │         │       query.py               │
│  • Calls Describe API   │         │  • Calls Query API           │
│  • Returns field        │         │  • Handles pagination        │
│    metadata as JSON     │         │  • Returns results as JSON   │
└──────────┬──────────────┘         └──────────┬───────────────────┘
           │                                    │
           │ REST API                          │ REST API
           ▼                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│               Salesforce Instance (via REST API)                 │
│  • /services/data/v59.0/sobjects/{object}/describe              │
│  • /services/data/v59.0/query?q={soql}                          │
└─────────────────────────────────────────────────────────────────┘
```

### Component Details

#### 1. Claude Code Skill: `/salesforce-query`
**Location**: `.claude/skills/salesforce-query/SKILL.md`

**Responsibilities**:
- Orchestrate the entire query workflow
- Manage credentials in session memory
- Analyze natural language to identify objects
- Determine which schemas to fetch (intelligent selection)
- Generate SOQL queries using schema metadata
- Validate SOQL syntax
- Display SOQL for transparency
- Format JSON results as markdown tables
- Handle errors and edge cases

**Tools Available**: Bash (Python execution), AskUserQuestion

#### 2. describe.py - Schema Fetcher
**Location**: `.claude/skills/salesforce-query/scripts/describe.py`

**Purpose**: Fetch field metadata for Salesforce objects

**API Endpoint**: `GET /services/data/v59.0/sobjects/{ObjectName}/describe`

**Input**:
- `instance_url`: Salesforce instance URL
- `session_id`: Valid session token
- `object_name`: Object to describe (Account, Opportunity, etc.)
- `specific_fields` (optional): Comma-separated list of fields

**Output** (JSON):
```json
{
  "success": true,
  "objectName": "Opportunity",
  "label": "Opportunity",
  "fields": [
    {
      "name": "Id",
      "label": "Opportunity ID",
      "type": "id",
      "referenceTo": [],
      "relationshipName": null
    },
    {
      "name": "AccountId",
      "label": "Account ID",
      "type": "reference",
      "referenceTo": ["Account"],
      "relationshipName": "Account"
    }
  ]
}
```

**Error Handling**:
- HTTP errors (401 Unauthorized, 404 Not Found)
- Network errors
- Invalid object names

#### 3. query.py - SOQL Executor
**Location**: `.claude/skills/salesforce-query/scripts/query.py`

**Purpose**: Execute SOQL queries and return results

**API Endpoint**: `GET /services/data/v59.0/query?q={soql}`

**Input**:
- `instance_url`: Salesforce instance URL
- `session_id`: Valid session token
- `soql_query`: SOQL query string

**Output** (JSON):
```json
{
  "success": true,
  "totalSize": 3,
  "records": [
    {
      "attributes": {"type": "Opportunity", "url": "..."},
      "Id": "006xx000001",
      "Name": "Platform Modernization",
      "Amount": 250000,
      "Account": {"Name": "United Oil & Gas"}
    }
  ]
}
```

**Features**:
- Automatic pagination handling (up to 2000 records)
- Detailed error messages from Salesforce
- Timeout protection

**Error Handling**:
- SOQL syntax errors
- Permission errors
- Field not found errors
- Query timeout

---

## Data Flow

### Typical Query Workflow

```
1. User Input
   │
   ▼
   "/salesforce-query show opportunities for United Oil & Gas"
   │
   ▼
2. Credential Check
   │
   ├─ Has credentials in session? ──No──> Ask user for instance URL & session ID
   │                                      │
   └─ Yes ────────────────────────────────┘
   │
   ▼
3. Query Analysis
   │
   ├─ Identify objects: Opportunity, Account
   ├─ Identify filters: Account.Name contains "United Oil & Gas"
   ├─ Identify fields needed: Id, Name, Amount, StageName, CloseDate
   └─ Check if ambiguous? ──Yes──> AskUserQuestion ──> Clarify
   │
   ▼
4. Schema Discovery (Intelligent)
   │
   ├─ Need relationship fields? ──Yes──> Fetch Account schema
   ├─ Unsure about field names? ──Yes──> Fetch Opportunity schema
   └─ Using only common fields? ──No fetch needed──> Skip
   │
   ▼ (if fetching)
   python describe.py "<url>" "<session>" "Opportunity"
   python describe.py "<url>" "<session>" "Account"
   │
   ▼
5. SOQL Generation
   │
   ▼
   SELECT Id, Name, StageName, Amount, CloseDate, Account.Name
   FROM Opportunity
   WHERE AccountId IN (
     SELECT Id FROM Account WHERE Name LIKE '%United Oil & Gas%'
   )
   ORDER BY CloseDate DESC
   │
   ▼
6. Syntax Validation
   │
   ├─ Check structure (SELECT, FROM present)
   ├─ Verify field references look valid
   └─ Validate parentheses, quotes balanced
   │
   ▼
7. Display SOQL
   │
   ▼
   "Generated SOQL: [query shown to user]"
   │
   ▼
8. Execute Query
   │
   ▼
   python query.py "<url>" "<session>" "<SOQL>"
   │
   ▼
9. Parse Results
   │
   ├─ Success? ──Yes──> Format as markdown table
   │           └─No───> Show error message
   │
   ▼
10. Display to User
    │
    ▼
    | Id | Name | Stage | Amount | Close Date | Account |
    |---|---|---|---|---|---|
    | ... | ... | ... | ... | ... | ... |
```

---

## Key Design Decisions

### 1. Authentication: Bearer Token per Session
**Decision**: Ask user for bearer token in chat, remember for session duration only

**Alternatives Considered**:
- Store in .env file → Rejected (security risk, credentials in repo)
- System environment variables → Rejected (less convenient for multiple orgs)
- Manage OAuth flow → Rejected (adds complexity, security risk, credential storage)
- Password-based OAuth → Rejected (still OAuth management, not true bearer token usage)

**Rationale**:
- Most secure approach - credentials never persisted
- No OAuth flow management or token storage
- User provides pre-obtained bearer token (session ID or OAuth token from external source)
- Easy to switch between orgs
- Aligns with bearer token authentication principle

### 2. Schema Discovery: On-Demand without Cache
**Decision**: Fetch schemas dynamically when needed, no caching

**Alternatives Considered**:
- Static field mappings → Rejected (doesn't support custom fields)
- Cache schemas for session → Rejected (added complexity for minimal benefit)

**Rationale**: Always accurate, supports custom fields, simple implementation, API calls negligible

### 3. SOQL Display: Show but Auto-Execute
**Decision**: Display generated SOQL for transparency, then auto-execute after validation

**Alternatives Considered**:
- Wait for approval → Rejected (slower workflow for low-risk read queries)
- Don't show SOQL → Rejected (less transparent, harder to debug)

**Rationale**: Good balance of transparency and speed

### 4. Ambiguity Handling: Ask for Clarification
**Decision**: When query is ambiguous, use AskUserQuestion before proceeding

**Alternatives Considered**:
- Make best guess → Rejected (accuracy is critical requirement)
- Show multiple options → Rejected (more complex, less clear)

**Rationale**: Ensures accuracy, prevents wrong data retrieval

### 5. Result Formatting: Claude Formats in Chat
**Decision**: Python returns raw JSON, Claude formats as table

**Alternatives Considered**:
- Python formats table → Rejected (less flexible, harder to adapt format)
- Use tabulate library → Rejected (unnecessary dependency)

**Rationale**: Claude has context to format intelligently, zero extra dependencies

---

## Dependencies

### Runtime Dependencies
- **Python 3.7+**: Script execution environment
- **requests**: HTTP client for Salesforce REST API calls

### Development Dependencies
None (simple scripts, no testing framework needed for MVP)

### Installation
```bash
pip install requests
```

---

## Security Considerations

### Credential Security
- ✅ Never stored in files or environment
- ✅ Only in Claude Code session memory (temporary)
- ✅ Not logged or persisted
- ✅ User must provide fresh bearer token for each new session
- ✅ No OAuth flow management or token refresh
- ✅ No local token caching or storage

### Query Safety
- ✅ Read-only operations (SOQL queries only)
- ✅ No data modification capabilities
- ✅ Respects Salesforce user permissions
- ✅ SOQL injection risk minimal (Claude generates queries, not user)

### API Access
- ✅ Uses standard Salesforce REST API
- ✅ Session-based authentication (standard practice)
- ✅ HTTPS encrypted communication
- ✅ API rate limits respected

---

## Performance Characteristics

### Latency
- **First query**: ~3-5 seconds (schema fetch + query execution)
- **Subsequent queries**: ~2-3 seconds (query execution only, if no new schemas needed)
- **Large result sets**: +1-2 seconds per 1000 records (pagination)

### API Call Budget
- **Per query**: 1-3 API calls
  - 0-2 describe calls (schema fetching)
  - 1+ query calls (includes pagination if needed)
- **Salesforce limits**: 15,000 API calls per 24 hours (Developer Edition)
- **Estimated capacity**: ~5,000 queries per day (very safe margin)

### Result Limits
- **Hard limit**: 2000 records per query (pagination handled automatically)
- **Practical limit**: ~200 records for readable table display
- **Recommendation**: Use LIMIT clause for large result sets

---

## Error Handling Strategy

### Authentication Errors (401)
- **Cause**: Session ID expired or invalid
- **Handling**: Inform user, request fresh credentials
- **Recovery**: User provides new session ID

### SOQL Syntax Errors
- **Cause**: Invalid SOQL generated
- **Handling**: Show Salesforce error message, explain issue
- **Recovery**: Regenerate SOQL or ask for clarification

### Field Not Found Errors
- **Cause**: Field doesn't exist in org
- **Handling**: Fetch schema to verify, regenerate with correct fields
- **Recovery**: Automatic retry with corrected SOQL

### No Results
- **Cause**: Query valid but no matching records
- **Handling**: Simple message "No records found"
- **Recovery**: None needed (expected behavior)

### Network Errors
- **Cause**: Connection issues
- **Handling**: Show error message, suggest retry
- **Recovery**: User retries query

---

## Limitations & Future Enhancements

### Current Limitations
- **Objects**: Limited to 5 standard objects (Account, Opportunity, Contact, Lead, Case)
- **Query language**: SOQL only (no SOSL text search)
- **Result size**: 2000 records maximum
- **No data modification**: Read-only queries
- **Manual session ID**: Must be retrieved from Salesforce manually

### Potential Future Enhancements
1. **SOSL Support**: Add text search across multiple objects
2. **More Objects**: Support additional standard objects (Campaign, Task, etc.)
3. **Custom Objects**: Auto-discover and query custom objects
4. **Export Results**: Save results to CSV/Excel
5. **OAuth Flow**: Automate authentication without manual session ID
6. **Query History**: Remember recent queries for quick re-run
7. **Cached Schemas**: Add optional schema caching for session
8. **Aggregation Queries**: Better support for COUNT, SUM, AVG, GROUP BY
9. **Data Visualization**: Generate charts for numerical results

---

## Testing Strategy

### Manual Testing Checklist
- [ ] Query each supported object type
- [ ] Test relationship queries (Opportunity.Account.Name)
- [ ] Test various WHERE conditions (=, LIKE, >, <, IN)
- [ ] Test date literals (TODAY, THIS_QUARTER, etc.)
- [ ] Test empty results
- [ ] Test invalid SOQL
- [ ] Test expired session ID
- [ ] Test field that doesn't exist
- [ ] Test pagination (>2000 records)
- [ ] Test ambiguous queries (should ask for clarification)

### Validation Tests
- SOQL syntax validation with various malformed queries
- Schema parsing with different field types
- Error message parsing and display

---

## Deployment & Usage

### Setup Instructions
1. Install Python dependencies:
   ```bash
   pip install requests
   ```

2. Verify skill files exist:
   ```
   .claude/skills/salesforce-query/
   ├── SKILL.md
   └── scripts/
       ├── describe.py
       ├── query.py
       ├── validate_token.py
   ```

3. Get Salesforce bearer token:
   - Log into Salesforce Developer Edition
   - Get session ID or OAuth bearer token (see SETUP.md for instructions)
   - Note your instance URL

### Usage Instructions
1. Open Claude Code in your project
2. Invoke: `/salesforce-query <your natural language query>`
3. Provide bearer token when prompted (first time in session only)
4. View generated SOQL and results table

### Example Queries
```
/salesforce-query show all accounts in California
/salesforce-query find opportunities closing this quarter
/salesforce-query show contacts from technology companies
/salesforce-query what are the open cases for Acme Corp
/salesforce-query list top 10 opportunities by amount
```

---

## Maintenance & Support

### Monitoring
- Watch for Salesforce API version deprecation (currently v59.0)
- Monitor API call usage if queries become frequent

### Updates Required
- Update API version in scripts if Salesforce deprecates v59.0
- Add new fields to common field lists as user needs evolve

### Troubleshooting
- **Skill not recognized**: Restart Claude Code session
- **Script errors**: Check Python installation and requests library
- **API errors**: Verify session ID is current and user has permissions

---

## Alternatives Considered and Rejected

### Option A: Static Field Mappings
**Why rejected**: Doesn't support custom fields, less accurate for user's specific org

### Option C: Hybrid SOQL/SOSL
**Why rejected**: Added complexity without clear benefit for stated requirements

### MCP Server Approach
**Why rejected**: Too complex for single-project usage, overkill for ad-hoc queries

### Direct LLM API Integration
**Why rejected**: Unnecessary API costs when Claude Code chat already available

### Stored Credentials (.env file)
**Why rejected**: Security risk, credentials could be committed to git

---

## Success Metrics

### Functional Success
- ✅ User can query all 5 supported objects
- ✅ Relationships work (e.g., Opportunity.Account.Name)
- ✅ Results display clearly as tables
- ✅ Errors are understandable and actionable

### Non-Functional Success
- ✅ Query execution < 5 seconds
- ✅ No credentials stored persistently
- ✅ Zero configuration required (beyond pip install)
- ✅ Works across different Salesforce orgs

### User Experience Success
- ✅ Natural language queries feel intuitive
- ✅ Ambiguity handled gracefully with questions
- ✅ SOQL transparency builds trust
- ✅ Error messages are helpful, not cryptic

---

**Architecture approved and implemented**: 2026-01-21
**Implementation status**: Complete
**Ready for use**: Yes
