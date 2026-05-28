---
name: document-presentation-management
description: Use this skill when you need to create, edit, or analyze document (.docx) and presentation (.pptx) files, including tasks like text extraction, revision tracking, and layout management.
---

# Document and Presentation Management

## Overview

This skill allows you to create, edit, and analyze both .docx and .pptx files. These file types are essentially ZIP archives containing XML files and other resources that can be read or edited. You have various tools and workflows available for different tasks.

## Workflow Decision Tree

### Reading/Analyzing Content
- Use the **Text Extraction** or **Raw XML Access** sections below.

### Creating New Files
- For .docx: Use the **Create New Word Document** workflow.
- For .pptx: Use the **Create New PowerPoint Presentation** workflow.

### Editing Existing Files
- For .docx:
  - **Your own file + Simple changes**: Use the **Basic OOXML Editing** workflow.
  - **Others' files**: Use the **Revision Tracking Workflow** (recommended default).
- For .pptx: Use the **Edit Existing PowerPoint Presentation** workflow.

## Reading and Analyzing Content

### Text Extraction
- For .docx:
  ```bash
  pandoc --track-changes=all path-to-file.docx -o output.md
  ```
- For .pptx:
  ```bash
  python -m markitdown path-to-file.pptx
  ```

### Raw XML Access
- For .docx: Unzip the file and read its raw XML content.
  ```bash
  python ooxml/scripts/unpack.py <office_file> <output_directory>
  ```
  Key files include:
  - `word/document.xml` - Main document content
  - `word/comments.xml` - Comments referenced in document.xml
  - `word/media/` - Embedded images and media files

- For .pptx: Unzip the file and read its raw XML content.
  ```bash
  python ooxml/scripts/unpack.py <office_file> <output_directory>
  ```
  Key files include:
  - `ppt/presentation.xml` - Main presentation metadata and slide references
  - `ppt/slides/slide{N}.xml` - Individual slide content

## Creating New Word Documents

1. **Read the entire file**: Review the documentation for `docx-js` to understand syntax and best practices.
2. Use Document, Paragraph, TextRun components to create a JavaScript/TypeScript file.
3. Export as .docx using Packer.toBuffer().

## Creating New PowerPoint Presentations

1. **Read the entire file**: Review the documentation for `html2pptx` to understand syntax and best practices.
2. Create HTML files for each slide with appropriate dimensions.
3. Use `html2pptx()` function to convert HTML slides to PowerPoint and save the presentation.

## Editing Existing Word Documents

1. **Read the entire file**: Review the documentation for OOXML editing.
2. Unzip the document: 
   ```bash
   python ooxml/scripts/unpack.py <office_file> <output_directory>
   ```
3. Edit XML files (mainly `word/document.xml`).
4. Repack the final document:
   ```bash
   python ooxml/scripts/pack.py <input_directory> <office_file>
   ```

## Editing Existing PowerPoint Presentations

1. **Read the entire file**: Review the documentation for OOXML editing.
2. Unzip the presentation:
   ```bash
   python ooxml/scripts/unpack.py <office_file> <output_directory>
   ```
3. Edit XML files (mainly `ppt/slides/slide{N}.xml`).
4. Repack the final presentation:
   ```bash
   python ooxml/scripts/pack.py <input_directory> <office_file>
   ```

## Revision Tracking Workflow for Word Documents

1. Convert the document to markdown with tracked changes:
   ```bash
   pandoc --track-changes=all path-to-file.docx -o current.md
   ```
2. Identify and group changes logically.
3. Implement changes in batches, ensuring to validate after each batch.
4. Finalize and validate the document.

## Visualizing Presentations

To visualize and analyze PowerPoint slides, convert them to images:

1. **Convert PPTX to PDF**:
   ```bash
   soffice --headless --convert-to pdf template.pptx
   ```

2. **Convert PDF pages to JPEG images**:
   ```bash
   pdftoppm -jpeg -r 150 template.pdf slide
   ```

## Code Style Guidelines
- Write concise code.
- Avoid verbose variable names and unnecessary operations.
- Avoid unnecessary print statements.

## Dependencies
Required dependencies (install if not available):
- **pandoc**: For text extraction from .docx.
- **docx**: For creating new Word documents.
- **markitdown**: For extracting text from .pptx.
- **pptxgenjs**: For creating PowerPoint presentations.
- **LibreOffice**: For PDF conversion.
- **Poppler**: For converting PDF to images.
- **defusedxml**: For safe XML parsing.