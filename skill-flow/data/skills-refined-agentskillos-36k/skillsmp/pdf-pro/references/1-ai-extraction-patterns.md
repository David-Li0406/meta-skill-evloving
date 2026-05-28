# Reference: AI Extraction Patterns (PDF 2026)

## Overview
Traditional OCR is dead. In 2026, we use "Multimodal Document Intelligence" to extract semantic meaning from PDFs, preserving relationships, hierarchies, and intent.

## 🧠 The "Extraction Stack"
1.  **Layer 1: Raw Byte Parsing (`unpdf`)** - Extracting text, metadata, and image locations quickly.
2.  **Layer 2: Vision Analysis (Gemini/GPT-4o)** - "Looking" at the page to identify tables, headers, and signatures.
3.  **Layer 3: Schema Mapping (AI SDK)** - Forcing the output into a validated Zod/JSON structure.

---

## 🛠️ Pattern: The "Visual Table" Extractor
Tables are the hardest part of PDF extraction. Borders are often missing or purely decorative.

### Prompting Strategy:
"Act as a forensic document analyst. Extract the table from page 2. Do not just return text; return a JSON array where each object represents a row. Identify headers even if they are merged cells."

```typescript
import { generateObject } from 'ai';
import { pdfToImages } from '@/utils/pdf-vision';

async function extractComplexTable(pdfBuffer: Buffer) {
  const pages = await pdfToImages(pdfBuffer);
  
  const { object } = await generateObject({
    model: google('gemini-2.0-pro'), // 2026 Vision Model
    schema: z.object({
      rows: z.array(z.record(z.string()))
    }),
    messages: [
      { role: 'user', content: [
        { type: 'text', text: 'Extract this table:' },
        { type: 'image', image: pages[1] } // Page 2 image
      ]}
    ]
  });
  
  return object.rows;
}
```

---

## 🏗️ Pattern: Recursive Document Summarization
For 100+ page documents, we use "Token-Efficient Forensic Scanning."
1.  Extract Table of Contents (TOC).
2.  Identify "High-Value" pages (Financial statements, signatures, terms).
3.  Direct the AI model to only process those specific pages in high resolution.

---

## 🚫 Common Pitfalls in AI Extraction
- **Hallucinations:** The model might "invent" a value if the scan is blurry. **Fix:** Use a multi-pass verification (LLM-A extracts, LLM-B verifies).
- **Token Limits:** Large PDFs exceed context windows. **Fix:** Use RAG (Retrieval Augmented Generation) or page-by-page mapping.
- **Hidden Text:** Invisible text layers (from failed OCR) can confuse LLMs. **Fix:** Always prefer the Visual/Vision layer for the source of truth.
