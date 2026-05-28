# Example: DOCX Document Operations

**Source**: https://github.com/anthropics/skills/tree/main/document-skills/docx
**Pattern**: Multi-file with decision tree and external references
**Use case**: Creating, editing, and analyzing Word documents with tracked changes

## Key Sections from SKILL.md

### Workflow Decision Tree (Upfront)

```
Reading/Analyzing Content
└─→ Use "Text extraction" or "Raw XML access"

Creating New Document
└─→ Use "Creating a new Word document" workflow

Editing Existing Document
├─ Your own document + simple changes
│  └─→ Use "Basic OOXML editing" workflow
├─ Someone else's document
│  └─→ Use "Redlining workflow" (recommended default)
└─ Legal, academic, business, or government docs
   └─→ Use "Redlining workflow" (required)
```

### Text Extraction

```bash
# Convert document to markdown with tracked changes
pandoc --track-changes=all path-to-file.docx -o output.md
# Options: --track-changes=accept/reject/all
```

### Creating New Documents

**Workflow:**
1. **MANDATORY - READ ENTIRE FILE**: Read `docx-js.md` (~500 lines) completely. **NEVER set any range limits when reading this file.**
2. Create JavaScript/TypeScript file using Document, Paragraph, TextRun
3. Export as .docx using Packer.toBuffer()

### Editing Existing Documents

**Workflow:**
1. **MANDATORY - READ ENTIRE FILE**: Read `ooxml.md` (~600 lines) completely. **NEVER set any range limits when reading this file.**
2. Unpack: `python ooxml/scripts/unpack.py <file> <dir>`
3. Create and run Python script using Document library
4. Pack: `python ooxml/scripts/pack.py <dir> <file>`

### Redlining Workflow

**Batching Strategy**: Group related changes into batches of 3-10 changes.

**Principle: Minimal, Precise Edits**

Example - Changing "30 days" to "60 days":
```python
# BAD - Replaces entire sentence
'<w:del><w:r><w:delText>The term is 30 days.</w:delText></w:r></w:del>...'

# GOOD - Only marks what changed, preserves original <w:r>
'<w:r w:rsidR="00AB12CD"><w:t>The term is </w:t></w:r><w:del><w:r><w:delText>30</w:delText></w:r></w:del>...'
```

### Tracked Changes Workflow

1. **Get markdown representation**:
   ```bash
   pandoc --track-changes=all path-to-file.docx -o current.md
   ```

2. **Identify and group changes**: Organize into batches (3-10 changes)
   - By section: "Batch 1: Section 2 amendments"
   - By type: "Batch 1: Date corrections"
   - Sequential: "Batch 1: Pages 1-3"

3. **Read documentation and unpack**:
   - MANDATORY: Read ooxml.md completely
   - Unpack document
   - Note the suggested RSID from unpack script

4. **Implement changes in batches**:
   - Map text to XML via grep
   - Create and run script using Document library
   - Verify each batch before next

5. **Pack the document**:
   ```bash
   python ooxml/scripts/pack.py unpacked reviewed-document.docx
   ```

6. **Final verification**:
   ```bash
   pandoc --track-changes=all reviewed-document.docx -o verification.md
   grep "original phrase" verification.md  # Should NOT find it
   grep "replacement phrase" verification.md  # Should find it
   ```

### Converting Documents to Images

```bash
# Convert DOCX to PDF
soffice --headless --convert-to pdf document.docx

# Convert PDF to JPEG images
pdftoppm -jpeg -r 150 document.pdf page
```

### Code Style Guidelines

```markdown
**IMPORTANT**: When generating code for DOCX operations:
- Write concise code
- Avoid verbose variable names and redundant operations
- Avoid unnecessary print statements
```

## Analysis

**What makes this work**:

1. **Decision tree upfront**: Three paths based on use case
2. **External file references**: docx-js.md, ooxml.md
3. **Batching strategy**: 3-10 changes per batch
4. **Minimal edits principle**: Only mark what changes
5. **Verification workflow**: pandoc to verify all changes applied
6. **MANDATORY file reads**: Forces reading complete external docs

## Unique Features

**Decision Tree**:
Shows three paths upfront based on use case (reading, creating, editing).

**MANDATORY - READ ENTIRE FILE**:
Emphatic instruction to read external docs completely: "**NEVER set any range limits when reading this file.**"

**Batching Strategy**:
Explicit guidance to group 3-10 related changes per batch for manageable debugging.

**Minimal Edits Principle**:
Detailed explanation with Good/Bad examples showing why minimal edits matter for professional documents.

**RSID Suggestion**:
Unpack script suggests an RSID to use for tracked changes.

**Verification Workflow**:
Six-step process ending with pandoc verification to ensure all changes applied correctly.

**External References**:
- docx-js.md (~500 lines) for creating new documents
- ooxml.md (~600 lines) for editing existing documents

**Location Methods**:
Specific guidance on how to locate changes in XML (section numbers, grep patterns, document structure). Explicitly warns: "DO NOT use markdown line numbers."

## Pattern Type

**Multi-file with external references** - Brief SKILL.md + mandatory external documentation.

## Key Takeaways

1. **Decision trees guide complexity** - Three distinct paths upfront
2. **External documentation** - Long technical docs in separate files
3. **MANDATORY reads** - Forces complete reading with emphasis
4. **Batching for debugging** - 3-10 changes per batch
5. **Minimal edits** - Professional standard for tracked changes
6. **Verification workflow** - Six steps ending with validation
7. **Code style guidance** - Even covers coding style
8. **RSID suggestion** - Unpack script provides suggested RSID
