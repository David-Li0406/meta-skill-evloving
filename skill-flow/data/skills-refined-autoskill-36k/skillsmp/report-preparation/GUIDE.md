# Report Preparation Guide

This guide provides detailed rules for processing student report submissions, including edge cases and troubleshooting.

## Why Parallel Subagents?

Reading 30+ PDFs sequentially would overflow the context window. Using one subagent per PDF provides:

| Benefit | Explanation |
|---------|-------------|
| **Context isolation** | Each agent loads only one PDF (some are 15+ MB) |
| **Parallel execution** | All PDFs processed simultaneously (~5-10 minutes total) |
| **Failure isolation** | Corrupted or oversized PDFs don't block others |
| **Memory efficiency** | Each agent's context released after completing |

### Handling Failed Subagents

If a subagent fails (typically due to PDF size > 15MB):

1. Note the file in the error report
2. Continue with other files
3. Handle failed files manually:
   - Open PDF in Preview to check student name
   - Rename manually using the prefix convention
   - Add to STUDENT-LIST.md

## Name Extraction Strategy

### Where to Look for Names

Subagents should search for student names in this order:

1. **Title page** - Most common location
2. **Document header** - Some templates include name in header
3. **First paragraph** - "Rapport av [Name]" or similar
4. **Signature block** - At the end of the document
5. **Footer** - Some include name in page footer

### Name Patterns to Match

| Pattern | Example |
|---------|---------|
| "Rapport av [Name]" | "Rapport av Anna Andersson" |
| "Författare: [Name]" | "Författare: Erik Eriksson" |
| "Namn: [Name]" | "Namn: Johan Johansson" |
| "Inlämnad av [Name]" | "Inlämnad av Maria Martinez" |
| "Student: [Name]" | "Student: Karl Karlsson" |
| "[Name], IPL25" | "Anna Andersson, IPL25" |

### Confidence Levels

| Level | Criteria |
|-------|----------|
| **High** | Name appears on title page or in clear "Author:" field |
| **Medium** | Name found in header/footer or signature block |
| **Low** | Name inferred from filename or partial match |

## Swedish Character Normalization

### Standard Conversions

| Swedish | ASCII | Notes |
|---------|-------|-------|
| ö | o | Most common |
| ä | a | Common |
| å | a | Common |
| é | e | Names like André |
| ü | u | German-origin names |
| ñ | n | Spanish-origin names |

### Implementation

```bash
# Normalize string in bash
echo "Löfgren" | sed 'y/öäåéüñÖÄÅÉÜÑ/oaaeunOAAEUN/'
```

In Python:
```python
import unicodedata
def normalize(name):
    replacements = {'ö':'o', 'ä':'a', 'å':'a', 'é':'e', 'ü':'u', 'ñ':'n'}
    result = name.lower()
    for old, new in replacements.items():
        result = result.replace(old, new)
    return result
```

## Handling Compound Names

### Swedish Compound Surnames

Some students have compound surnames (two family names):

| Full Name | First | Last | Prefix |
|-----------|-------|------|--------|
| Anna Martinez Löfgren | Anna | Martinez Löfgren | `martinezlofgren_anna` |
| Erik von Essen | Erik | von Essen | `vonessen_erik` |
| Maria De La Cruz | Maria | De La Cruz | `delacruz_maria` |

### Compound First Names

Swedish often uses compound first names:

| Full Name | First | Last | Prefix |
|-----------|-------|------|--------|
| Karl Johan Andersson | Karl Johan | Andersson | `andersson_karljohan` |
| Anna-Isabel Martinez | Anna-Isabel | Martinez | `martinez_annaisabel` |
| Lars Erik Svensson | Lars Erik | Svensson | `svensson_larserik` |

### Rule: Prefix Generation

1. Remove all spaces and hyphens from name parts
2. Lowercase everything
3. Normalize Swedish characters
4. Format: `lastname_firstname`

## Duplicate Handling

### Identifying Duplicates

Google Classroom adds suffixes like `(1)`, `(2)` when students submit multiple times:

```
andersson_anna_Rapport.pdf
andersson_anna_Rapport (1).pdf
andersson_anna_Rapport (2).pdf
```

### Primary Rule: Prefer Latest, But Verify

**Default assumption:** The latest submission is what the student wants graded.

**But always verify:** The latest version should be complete and appear intentional.

### Decision Flow

```
1. Identify all files from same student
2. Determine which is "latest" (highest number suffix, or modification date)
3. Read the latest version
4. Is it complete? (Has all sections, proper formatting, not blank/corrupted)
   - YES → Keep latest, delete others
   - NO → Compare to earlier versions, keep most complete
5. Report decision with reasoning
```

### What "Complete" Means

Check these indicators in the latest version:

| Indicator | Complete | Incomplete |
|-----------|----------|------------|
| Page count | Similar to or more than earlier versions | Significantly fewer pages |
| Sections | All expected sections present | Missing sections |
| Conclusion | Has conclusion/summary | Ends abruptly |
| Formatting | Proper headers, layout | Broken formatting |
| Content | Substantive text | Blank pages, placeholder text |

### Example Scenarios

**Scenario 1: Latest is complete (normal case)**
```
File 1: rapport.pdf (12 pages, all sections)
File 2: rapport (1).pdf (14 pages, all sections + appendix)
→ Keep File 2 (latest and more complete)
```

**Scenario 2: Latest is incomplete (accidental submission)**
```
File 1: rapport.pdf (15 pages, complete report)
File 2: rapport (1).pdf (3 pages, just title page and intro)
→ Keep File 1 (complete), delete File 2 (appears incomplete/accidental)
→ Flag for review: "Latest appears incomplete, kept earlier complete version"
```

**Scenario 3: Latest is different document type**
```
File 1: rapport.pdf (12 pages, the report)
File 2: rapport (1).pdf (2 pages, presentation slides exported to PDF)
→ Keep File 1 (the actual report), delete File 2 (wrong file type)
→ Flag: "Latest appears to be slides, not report"
```

**Scenario 4: Identical content**
```
File 1: rapport.pdf (12 pages)
File 2: rapport (1).pdf (12 pages, identical MD5)
→ Keep File 1 (cleaner filename), delete File 2
```

### Verification Commands

```bash
# Check page count
pdfinfo file.pdf | grep Pages

# Compare MD5 (detect identical content)
md5 file1.pdf file2.pdf

# List files by modification date
ls -lt *.pdf

# List files by size
ls -lhS *.pdf
```

### Reporting Duplicate Resolution

When removing duplicates, report:

```
## Duplicate Resolution: Anna Andersson

Files found:
1. andersson_anna_rapport.pdf (12 pages, 2024-12-15)
2. andersson_anna_rapport (1).pdf (14 pages, 2024-12-18)

Decision: Kept file 2 (latest, complete with appendix)
Removed: andersson_anna_rapport.pdf
```

Or if latest was incomplete:

```
## Duplicate Resolution: Erik Eriksson

Files found:
1. eriksson_erik_rapport.pdf (15 pages, 2024-12-14)
2. eriksson_erik_rapport (1).pdf (2 pages, 2024-12-18)

Decision: Kept file 1 (complete report)
Removed: eriksson_erik_rapport (1).pdf
⚠ Note: Latest submission appears incomplete (only 2 pages). Kept earlier complete version.
```

## Unidentified Files

### Resolution Strategy

1. **Check filename for clues:**
   - Contains first name only → match to roster
   - Contains partial surname → match to roster
   - Contains student ID → look up in system

2. **Cross-reference with missing:**
   - If 1 unidentified file and 1 missing student → likely match
   - If multiple unidentified → flag all for manual review

3. **Manual fallback:**
   - Open PDF in Preview
   - Search for name
   - Rename manually

### Flagging for Manual Review

Create a section in terminal output:

```
## Files Requiring Manual Review

1. Unknown_Report_Final.pdf
   - Reason: No name found in document
   - Suggestion: Check if this matches missing student "Johan Johansson"

2. Inlämningsuppgift.pdf
   - Reason: Generic filename, name on page 3 illegible
   - Suggestion: Open in Preview and check title page
```

## DOCX Conversion

### AppleScript Method (Primary)

Uses Microsoft Word for highest quality conversion:

```bash
osascript scripts/convert-docx.applescript "input.docx" "output.pdf"
```

Requirements:
- macOS
- Microsoft Word installed
- Word not currently displaying dialogs

### Handling Conversion Failures

| Error | Cause | Solution |
|-------|-------|----------|
| Word not found | Not installed | Use alternative method |
| Timeout | Large file | Increase delay in script |
| Dialog blocking | Word showing alert | Dismiss dialog, retry |
| Permissions | Sandbox | Run from authorized location |

### Alternative Methods (Fallback)

If AppleScript fails, document for manual conversion:

1. **LibreOffice (CLI):**
   ```bash
   libreoffice --headless --convert-to pdf input.docx
   ```

2. **Manual:** Open in Word, File → Export as PDF

## Privacy and Security

### GDPR Compliance

Student reports contain personal data. Required protections:

| Requirement | Implementation |
|-------------|----------------|
| No version control | Add to .gitignore |
| No cloud sync | Disable Dropbox/iCloud for folder |
| Access control | Only instructor access |
| Retention | Delete after course ends |

### Git Protection Verification

```bash
# Check .gitignore includes student data
cat .gitignore | grep -E "(student-reports|CLASS-LIST|STUDENT-LIST|GRADING)"

# Verify files are ignored
git status --ignored

# Check nothing is staged
git diff --cached --name-only
```

### Emergency: Files Already Committed

If student data was accidentally committed:

```bash
# DO NOT push to remote
# Contact git administrator
# May require history rewrite (BFG or filter-branch)
```

## Processing Session Log

After each processing session, document:

```markdown
## Processing Log - Assignment N

**Date:** YYYY-MM-DD
**Files downloaded:** X
**Successfully processed:** Y
**Conversions:** Z DOCX → PDF
**Duplicates removed:** N

### Issues Encountered

1. [Issue description and resolution]
2. [Issue description and resolution]

### Manual Review Completed

- File1.pdf → Matched to Student Name
- File2.pdf → Unable to identify, instructor notified
```

## Troubleshooting

### "Subagent failed with size error"

PDF exceeds API limits (~15MB). Solutions:
1. Compress PDF: `gs -sDEVICE=pdfwrite -dPDFSETTINGS=/ebook -o compressed.pdf large.pdf`
2. Process manually: Open in Preview, find name, rename

### "Name appears in wrong encoding"

PDF uses non-standard character encoding. Solutions:
1. Extract text with `pdftotext -enc UTF-8`
2. Check PDF metadata for author field
3. Manual identification

### "Word conversion hangs"

Microsoft Word is waiting for user input. Solutions:
1. Open Word, dismiss any dialogs
2. Close all Word documents
3. Restart Word and retry

### "File already exists with same prefix"

Duplicate detection found conflict. Solutions:
1. Check if truly duplicate (same student, multiple submissions)
2. If different students with same prefix, add distinguisher
3. Example: `andersson_anna1` vs `andersson_anna2`
