# Naming Conventions

Detailed naming patterns for the Johnny Decimal system.

## Folder Naming

### Areas (Top Level)
```
XX-XX Area Name
```
Examples:
- `00-09 System`
- `20-29 Finances`
- `60-69 Hobbies and Recreation`

### Categories (Second Level)
```
XX Category Name
```
Examples:
- `00 System`
- `21 Banks`
- `45 Employers`

### Subcategories (Third Level)
```
XX.YY Subcategory Name
```
Examples:
- `00.00 JDex for System`
- `21.10 Example Bank`
- `31.14 123 Main Street`

### System Subcategories Pattern
Each area can have system subcategories in the `.0X` range:
- `XX.00` - JDex/Index for that area
- `XX.01` - Inbox for that area
- `XX.02` - Tasks for that area
- `XX.03` - Templates
- `XX.04` - Scripts
- `XX.08` - Someday/Maybe
- `XX.09` - Archive

## File Naming

### Date-Prefixed Files (Transient/Recurring)
```
YYYY-MM-DD_description.ext
```
Examples:
- `2024-12-27_statement.pdf`
- `2024-01-15_receipt.pdf`
- `20150917_recsys.md` (also acceptable: YYYYMMDD)

### Descriptive Files (Permanent/Reference)
```
description_with_underscores.ext
```
Examples:
- `policy_declaration.pdf`
- `birth_certificate.pdf`
- `offer_letter.pdf`

### Bank Statements
Organized in year folders:
```
statements/
└── YYYY/
    ├── 01.pdf
    ├── 02.pdf
    └── ...
```

Credit card statements use `cc_` prefix:
```
statements/
└── YYYY/
    ├── cc_01.pdf
    ├── cc_02.pdf
    └── ...
```

### Tax Documents
```
account_YYYY_form-type.pdf
```
Examples:
- `bankname_2023_1099-INT.pdf`
- `brokerage_2023_1099-DIV.pdf`

### Per-Person Subfolders
Within personal records, use area-based suffixes:
```
12 Spouse/
├── 12.10 Personal/
├── 12.20 Finances/
├── 12.40 Career and Education/
├── 12.50 Health and Wellness/
└── 12.70 Legal and Records/
```

## Notes Files (in JDex)

Notes for specific IDs use the ID as filename:
```
00.00 JDex for System/
├── 21.10.md    # Notes about a bank account
├── 31.14.md    # Notes about current home
└── 45.12.md    # Notes about an employer
```

Format inside note files:
```markdown
# XX.YY Subcategory Name

## YYYY-MM-DD

Note content here.

## YYYY-MM-DD

Another note.
```

## Validation Rules

A valid JD folder name must:
1. Start with two digits
2. Followed by either `-` (area), ` ` (category), or `.` (subcategory)
3. Contain a descriptive name after the prefix

A valid JD filename should:
1. Use underscores or hyphens, not spaces
2. Be lowercase (preferred) or consistent case
3. Include date prefix for transient items
4. Have a meaningful description
