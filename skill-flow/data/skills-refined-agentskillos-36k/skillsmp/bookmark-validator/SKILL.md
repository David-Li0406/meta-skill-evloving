---
name: bookmark-validator
description: Use when validating bookmark data quality, checking for duplicates, missing information, suggesting tags based on URL patterns, or analyzing bookmark collection health. Triggers on requests about bookmark validation, data quality, duplicate detection, tag suggestions, or collection improvements.
---

# Bookmark Validator

I systematically validate and improve bookmark data quality using comprehensive checks against schema requirements and quality heuristics.

## Capture Workflow (Step 0: Data Acquisition)

Before validation can begin, bookmarks must be captured from the browser's localStorage. Follow this automated workflow:

### Prerequisites
- User must have bookmarks in their browser's localStorage

### Agent Execution Steps

**Step 0.1: Ensure server is running**
```bash
# Check if server is running on port 3000
lsof -i :3000

# If not running, start it:
npm run dev > /dev/null 2>&1 & sleep 3
```

**Step 0.2: Clear old capture and watch for new one**
```bash
# Clear old file, then watch for new capture (2 minute timeout)
rm -f validator-check/bookmarks-captured.json
echo "Please visit: http://localhost:3000/api/debug/capture-bookmarks"

for i in {1..120}; do
  if [ -f "validator-check/bookmarks-captured.json" ] && [ -s "validator-check/bookmarks-captured.json" ]; then
    echo "Captured!"
    exit 0
  fi
  sleep 1
done
echo "Timeout"
```

**Step 0.3: What happens when user visits the page**
- The page automatically reads `localStorage.getItem('bookmark-vault-bookmarks')`
- Sends data via POST to the server
- Shows "Captured!" when complete
- Server saves to `validator-check/bookmarks-captured.json`

**Step 0.4: Read captured file**
```
Read file: validator-check/bookmarks-captured.json
```

**Step 0.5: Run all validation steps** (Steps 1-9 below)

**Step 0.6: Output results**
- Display full validation report as text to user
- Save JSON report to: `validator-check/validation-report.json`

### Output Files
| File | Purpose |
|------|---------|
| `validator-check/bookmarks-captured.json` | Raw bookmark data from localStorage |
| `validator-check/validation-report.json` | Structured validation report (JSON) |

### Server Troubleshooting
If capture fails:
```bash
# Kill existing server and restart
lsof -ti :3000 | xargs kill -9 2>/dev/null
npm run dev > /dev/null 2>&1 & sleep 3
```

**Note:** The `validator-check/` folder is gitignored to prevent committing user data.

---

## CRITICAL REQUIREMENTS

You MUST complete ALL validation checks. No shortcuts, no sampling, no partial analysis. You MUST run through every step of the validation checklist before responding.

### Non-Negotiable Rules

- ❌ NEVER say "your bookmarks look good" without providing detailed evidence
- ❌ NEVER report findings without specific bookmark IDs
- ❌ NEVER skip steps because "most bookmarks are fine"
- ❌ NEVER sample or report on first N bookmarks only
- ❌ NEVER suggest generic tags - use domain pattern matching
- ❌ NEVER claim "I can't access localStorage" (use file-based storage access instead)
- ❌ NEVER confuse schema validation with quality validation

## Mandatory Validation Steps

Before responding, you MUST complete this exact checklist:

### Step 1: Load Complete Dataset
- **Primary source:** Read `validator-check/bookmarks-captured.json` (captured from localStorage via Step 0)
- **Reference:** Read `lib/storage.ts` to understand storage format if needed
- Parse the `bookmark-vault-bookmarks` storage key format: `{ version: number, data: Bookmark[] }`
- Count and verify you have loaded ALL bookmarks (include total count in report)
- Do NOT sample or estimate

### Step 2: Duplicate Detection (Normalized Comparison)
- Check exact URL matches (case-sensitive, character-for-character)
- Normalize URLs for comparison using this algorithm:
  ```
  1. Convert to lowercase
  2. Strip protocol (http://, https://)
  3. Remove www. prefix
  4. Remove trailing slashes
  5. Use as normalized form
  ```
- Compare normalized URLs - if they match, bookmarks are duplicates
- Report ALL duplicates with:
  - Normalized URL (the canonical form)
  - List of bookmark IDs with this URL
  - Original URLs for each
  - Creation dates to help identify which to keep
- Group by normalized URL for clarity

### Step 3: Schema Validation (Against Zod Schema)
- Read validation schema from `lib/validation.ts`
- Extract these constraints:
  - `id`: Must be valid UUID format (`/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i`)
  - `title`: Required, 1-200 characters, trimmed
  - `url`: Required, valid URL, protocols: http, https, mailto, ftp, ftps, file
  - `description`: Optional, max 500 characters
  - `tags`: Array, each tag 1-50 chars, max 20 tags total
  - `color`: Optional, one of: `red`, `blue`, `green`, `yellow`, `purple`, `orange`
  - `createdAt`: Required, ISO 8601 datetime format
  - `spaceId`: Optional, minimum 1 character if present
- Validate EVERY bookmark against EVERY rule
- Report all schema violations with:
  - Bookmark ID
  - Field that violates constraint
  - Constraint that was violated
  - Actual value that failed

### Step 4: Quality Issues - Empty/Missing Descriptions
- Check EVERY bookmark for:
  - `description` field is `undefined`
  - `description` field is empty string `""`
  - `description` is whitespace-only (spaces, tabs, newlines)
  - `description` is placeholder text ("Description", "N/A", "TODO", etc.)
- Report ALL matches with:
  - Bookmark ID
  - Bookmark title (so user recognizes it)
  - URL (for reference)
  - Count total and percentage of bookmarks without meaningful descriptions

### Step 5: Quality Issues - Missing Tags
- Check EVERY bookmark for:
  - `tags` array is empty `[]`
  - `tags` array is undefined/missing
- Report ALL matches with:
  - Bookmark ID
  - Bookmark title
  - URL
  - Count total and percentage without tags

### Step 6: Quality Issues - Generic/Suspicious Titles
- Check for these patterns:
  - Exact matches (case-insensitive): "Untitled", "New Tab", "Bookmark", "Link", "Page", "Website", "Resource", "Note"
  - Extremely short (< 3 characters)
  - All numbers or symbols only
  - Placeholder formats: "Untitled 1", "New 2", "Tab (copy)"
- Report ALL matches with:
  - Bookmark ID
  - Actual title
  - URL
  - Why it's flagged (pattern matched)
  - Count total

### Step 7: Quality Issues - Very Short Descriptions
- Check for descriptions that:
  - Exist but have < 10 meaningful characters (excluding punctuation-only)
  - Are single words or fragments
- Report ALL matches with:
  - Bookmark ID
  - Bookmark title
  - Actual description
  - Character count
  - Count total

### Step 8: Quality Issues - Invalid URL Patterns
- Check for suspicious/invalid URLs:
  - Localhost or 127.0.0.1
  - file:// protocol (unless intentional)
  - javascript: protocol (security concern)
  - About:, data: protocols
  - Incomplete/malformed URLs (fail the RFC 3986 validation)
- Report ALL matches with:
  - Bookmark ID
  - URL
  - Why it's suspicious

### Step 9: Tag Suggestions (Domain-Based Patterns)
- For EVERY bookmark in the collection:
  - Extract domain from URL (e.g., github.com, youtube.com, docs.python.org)
  - Check against domain pattern map (see below)
  - Suggest tags that match the pattern
  - Filter out tags already present in bookmark.tags
  - Only report new suggestions (don't repeat existing tags)
- Report with:
  - Bookmark ID
  - Bookmark title
  - URL
  - Current tags (comma-separated or array format)
  - Suggested tags (formatted same way)
  - Matched domain pattern (e.g., "github.com pattern matched")

**Domain Pattern Map:**

| Domain Pattern | Suggested Tags |
|---|---|
| github.com, gitlab.com, bitbucket.org | `["dev", "code", "version-control"]` |
| stackoverflow.com | `["dev", "reference", "qa"]` |
| *.docs.*, *.documentation.* | `["documentation", "reference"]` |
| developer.mozilla.org | `["documentation", "web", "reference", "html", "css", "js"]` |
| youtube.com, youtu.be, vimeo.com | `["video", "media"]` |
| medium.com, dev.to, hashnode.com | `["blog", "article"]` |
| twitter.com, x.com, mastodon.* | `["social", "twitter"]` |
| reddit.com, discord.gg | `["social", "community"]` |
| npmjs.com, yarn.pkg, crates.io | `["dev", "packages"]` |
| react.dev, react.* | `["react", "documentation", "frontend"]` |
| tailwindcss.com, bootstrap.* | `["css", "framework", "styling"]` |
| python.org, docs.python.org | `["python", "documentation", "reference"]` |
| typescript.* | `["typescript", "reference"]` |
| github.com/issues, github.com/pulls | `["dev", "issue-tracking"]` |

**Tag Rules:**
- Suggest only tags NOT already present
- If no tags exist and pattern matches, always suggest (don't skip)
- Multiple patterns can match - suggest all relevant
- Avoid generic tags - use specific domain patterns

## Required Output Format

Generate your report using this exact structure:

```markdown
# Bookmark Validation Report

## Summary Statistics
- Total bookmarks analyzed: [NUMBER]
- Total issues found: [NUMBER]
- Critical issues: [NUMBER]
- Warnings: [NUMBER]
- Suggestions: [NUMBER]

## Critical Issues (MUST FIX)

### Schema Violations (COUNT: X)
For each violation:
- [ID] bookmark-{id}: {field} violates {constraint} (actual: {value})

Example:
- [ID] bookmark-abc123: title exceeds 200 chars (actual: 256 chars)
- [ID] bookmark-def456: invalid UUID format for id field

### Duplicate URLs (COUNT: X groups, Y total duplicates)
For each group:

**Normalized URL:** {normalized-url}
- [ID] bookmark-abc (https://example.com) - created 2024-01-01
- [ID] bookmark-def (http://example.com) - created 2024-01-02
- [ID] bookmark-ghi (www.example.com) - created 2024-01-03

## Warnings (SHOULD FIX)

### Missing Descriptions (COUNT: X bookmarks, Y%)
- [ID] bookmark-123 "GitHub"
- [ID] bookmark-456 "React Docs"
- [ID] bookmark-789 "TailwindCSS"

### Missing Tags (COUNT: X bookmarks, Y%)
- [ID] bookmark-111 "Mozilla Developer Network"
- [ID] bookmark-222 "TypeScript Handbook"

### Generic/Suspicious Titles (COUNT: X)
- [ID] bookmark-333 "Untitled" (matched: generic pattern "Untitled")
- [ID] bookmark-444 "A1" (too short: 2 chars)

### Short Descriptions (COUNT: X)
- [ID] bookmark-555 "GitHub" description: "For code" (6 chars, too brief)

### Invalid/Suspicious URLs (COUNT: X)
- [ID] bookmark-666 (localhost:3000) - localhost not recommended
- [ID] bookmark-777 (javascript:void(0)) - javascript protocol security concern

## Suggestions (QUALITY IMPROVEMENTS)

### Tag Suggestions (COUNT: X bookmarks with new tags available)

For each bookmark with suggestions:

Bookmark: [ID] bookmark-abc "GitHub"
- URL: https://github.com
- Current tags: []
- Suggested tags: ["dev", "code", "version-control"]
- Reason: Matched github.com domain pattern

Bookmark: [ID] bookmark-def "React Documentation"
- URL: https://react.dev
- Current tags: ["react"]
- Suggested tags: ["documentation", "frontend"]
- Reason: Matched react.dev domain pattern

[... continue for all bookmarks with suggestions]

## Action Items

1. Fix X schema violations (IDs: {list})
2. Resolve X duplicate URL groups (total X duplicates)
3. Add descriptions to X bookmarks (Y%)
4. Add tags to X bookmarks (Y%)
5. Review X generic/suspicious titles
6. Consider X tag suggestions (X bookmarks affected)
7. Investigate X invalid/suspicious URLs

## Confidence & Next Steps

All X bookmarks analyzed. All validation checks completed.

To fix issues:
1. Schema violations must be corrected (data is invalid)
2. Duplicates should be merged (keep most recent or most complete)
3. Descriptions should be added from preview metadata if available
4. Tags should be added using suggested patterns
5. Titles should be updated to be more descriptive
```

## Validation Completion Checklist

**Before responding, verify you have:**

- [ ] Loaded and parsed ALL bookmarks from storage (show total count)
- [ ] Checked EVERY bookmark for exact URL duplicates
- [ ] Checked EVERY bookmark for normalized URL duplicates
- [ ] Validated EVERY bookmark against Zod schema
- [ ] Checked EVERY bookmark for empty/missing descriptions
- [ ] Checked EVERY bookmark for missing tags
- [ ] Checked EVERY bookmark for generic titles
- [ ] Checked EVERY bookmark for very short descriptions
- [ ] Checked EVERY bookmark for invalid/suspicious URLs
- [ ] Generated tag suggestions for ALL bookmarks with matching domain patterns
- [ ] Provided structured report following required template
- [ ] Included summary statistics
- [ ] Listed ALL issues with specific bookmark IDs
- [ ] Provided actionable next steps

**IMPORTANT:** If ANY checkbox is unchecked, you have NOT completed the validation. Do not respond until ALL steps are done.

## Implementation Notes

### Storage Access
- **Captured data:** `validator-check/bookmarks-captured.json`
- **Storage utilities:** `lib/storage.ts`
- **Key:** `bookmark-vault-bookmarks`
- **Format:** `{ version: 1, data: Bookmark[] }`
- **Access method:** Run Step 0 capture workflow, then read the captured JSON file

### Type Definitions
- **File:** `lib/types.ts`
- **Type:** `Bookmark` interface with all fields listed in Step 3

### Validation Schemas
- **File:** `lib/validation.ts`
- **Schemas:** `BookmarkSchema`, `CreateBookmarkSchema`, `UpdateBookmarkSchema`
- All constraints defined in Zod format - extract exact requirements from here

### URL Normalization Algorithm

```typescript
function normalizeUrl(url: string): string {
  try {
    const parsed = new URL(url);
    let normalized = parsed.hostname || '';

    // Remove www. prefix
    normalized = normalized.replace(/^www\./, '');

    // Remove trailing slashes from pathname
    let path = parsed.pathname.replace(/\/$/, '');

    // Combine hostname and normalized path
    return (normalized + path).toLowerCase();
  } catch {
    return url.toLowerCase(); // Fallback for invalid URLs
  }
}
```

## Red Flags - STOP and Reconsider

If you find yourself thinking any of these, STOP and complete the step properly:

- "I'll check what I can access" → Access the files and data; don't skip
- "Most bookmarks are fine, here are a few examples" → Check ALL
- "Duplicates seem unlikely" → Check all, use normalized comparison
- "Descriptions are optional, so..." → Still check and report what's empty
- "I'll suggest generic tags" → Use domain patterns from map
- "Here are some suggestions" → For EVERY matching bookmark, not just examples
- "The data looks valid" → Run through all validation rules anyway
- "I don't have direct access" → Use file-based data access methods

**Seeing any of these thoughts means you're rationalizing. Fix it and complete the step.**

## Rationalization Table (Known Loopholes & How to Close Them)

| Rationalization | Reality | Prevention |
|---|---|---|
| "I'll analyze what I can access" | You can access files and extract data; not accessing everything is a choice | Must read storage utilities and extract ALL bookmarks before reporting |
| "Here are some examples of issues" | Examples ARE NOT analysis; you must report ALL issues | Count says "X issues found" - report X issues with IDs, not 2-3 samples |
| "Most bookmarks are fine, here's what I noticed" | Doesn't matter if most are fine; report what EXISTS | 100% scan required - if X% have empty descriptions, name them all by ID |
| "Duplicates are rare, so I'll just check carefully" | You might miss some; only algorithmic comparison is definitive | Use exact comparison AND normalized comparison, report all matches |
| "I can't directly access localStorage" | Correct - but you CAN read files, extract schemas, and validate programmatically | Use file-based approaches; don't skip validation claiming access problems |
| "Descriptions are optional, so missing ones don't matter" | Still need to report them for user awareness | Report ALL missing descriptions; let user decide if they care |
| "I'll focus on critical issues first" | Then you won't find warnings/suggestions; all 9 steps are required | Complete all steps; report by severity level (Critical, Warning, Suggestion) but do all |
| "Generic tags are fine, they're descriptive enough" | They are NOT domain-specific; skill requires domain pattern matching | Use only domain pattern map; don't substitute generic tags |
| "The data looks valid to me" | "Looks valid" isn't validation; validation is checking against rules | Run through schema constraint checklist systematically, report violations |
| "I'll report counts instead of listing bookmarks" | Counts hide the actual issues; users need IDs to fix them | Always include [ID] bookmark-{id} for every single issue in list |

## Common Mistakes to Avoid

| Mistake | Fix | Why It Matters |
|---------|-----|---------|
| Reporting "no duplicates found" without showing normalized comparison | Show normalized URL algorithm and compare ALL bookmarks | Without the algorithm shown, you might have skipped it |
| Saying "descriptions look fine" without listing which are empty | List all bookmarks with no/empty descriptions with IDs | Lets user act on specific items, not guess |
| Suggesting 1-2 example tags | Suggest for EVERY bookmark that matches domain patterns | Examples look good but miss 90% of opportunities |
| Checking first 10 bookmarks, then "rest follow same pattern" | Check ALL bookmarks explicitly | Assumption fails; actual patterns vary |
| Generic findings like "some URLs invalid" without specifics | Report each invalid URL with ID and reason | User can't fix "some" - needs specific list |
| Mixing schema validation with quality issues | Report separately with clear section headers | Different severity and fix approaches |
| Reporting only new tags, not ALL suggestions | List both current and suggested tags for comparison | User can't decide if suggestion is good without context |
| "Done analyzing" after partial completion | Verify against checklist - all 10 items must be checked | Incomplete validation = wasted effort |

## Success Looks Like

When you complete bookmark validation successfully:
- Report includes count of ALL bookmarks analyzed (proof all were checked)
- Every duplicate group shown with normalized URLs (showing work)
- Schema violations listed by ID with specific field and constraint (actionable)
- Quality issues reported for 100% coverage with IDs (not sampling)
- Tag suggestions provided for every matching domain pattern (comprehensive)
- Structured format with all sections populated (complete template)
- Specific bookmark IDs for every single issue or suggestion (traceable)
- Validation completion checklist marked complete (all steps done)
- No generic findings or "seems fine" conclusions (evidence-based)
- Report length proportional to issue count, not abbreviated (full analysis)
