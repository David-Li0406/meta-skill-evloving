# Document Ai - Sharp Edges

## Claude Pdf Requires Citations

### **Id**
claude-pdf-requires-citations
### **Summary**
Claude on Bedrock requires citations for full PDF vision
### **Severity**
high
### **Situation**
Using Claude via Amazon Bedrock Converse API for PDFs
### **Why**
  Without citations enabled in Bedrock's Converse API, Claude falls
  back to basic text extraction only - losing all visual understanding.
  You won't get table structure, layouts, or image descriptions.
  This is a silent degradation - no error is thrown.
  
### **Detection Pattern**
  converse.*pdf|bedrock.*pdf(?!.*citation)
  
### **Solution**
  Always enable citations when using Bedrock for PDF processing:
  
  ```typescript
  import { BedrockRuntimeClient, ConverseCommand } from "@aws-sdk/client-bedrock-runtime";
  
  const client = new BedrockRuntimeClient({ region: "us-east-1" });
  
  const response = await client.send(
    new ConverseCommand({
      modelId: "anthropic.claude-sonnet-4-20250514-v1:0",
      messages: [...],
      // CRITICAL: Enable citations for full PDF vision
      additionalModelRequestFields: {
        enable_citations: true, // Without this, text-only extraction!
      },
    })
  );
  ```
  

## Pdf Size Limits

### **Id**
pdf-size-limits
### **Summary**
PDF uploads silently truncated or rejected
### **Severity**
high
### **Situation**
Uploading large or many-page PDFs
### **Why**
  Claude limits:
  - 32MB max file size
  - 100 pages max per upload
  - ~200k tokens for images (each page as image)
  
  Exceeding these either fails silently, truncates content,
  or produces incomplete extraction without warning.
  
### **Detection Pattern**
  upload.*pdf|pdf.*process(?!.*size.*check|page.*limit)
  
### **Solution**
  Validate before processing:
  
  ```typescript
  import * as fs from "fs";
  import { pdf } from "pdf-to-img";
  
  const MAX_FILE_SIZE = 32 * 1024 * 1024; // 32MB
  const MAX_PAGES = 100;
  
  async function validatePDF(pdfPath: string) {
    // Check file size
    const stats = fs.statSync(pdfPath);
    if (stats.size > MAX_FILE_SIZE) {
      throw new Error(
        `PDF is ${(stats.size / 1024 / 1024).toFixed(1)}MB, max is 32MB. Split the file.`
      );
    }
  
    // Check page count
    const document = await pdf(pdfPath);
    let pageCount = 0;
    for await (const _ of document) {
      pageCount++;
      if (pageCount > MAX_PAGES) {
        throw new Error(
          `PDF has more than ${MAX_PAGES} pages. Split into sections.`
        );
      }
    }
  
    return { pageCount, sizeBytes: stats.size };
  }
  ```
  

## Vision Model Hallucination

### **Id**
vision-model-hallucination
### **Summary**
Vision models hallucinate data from unclear documents
### **Severity**
high
### **Situation**
Extracting from low-quality scans or handwriting
### **Why**
  When document quality is poor, vision models don't say "unclear" -
  they guess and produce plausible-looking but wrong data.
  
  In benchmarks:
  - GPT o3-mini produced "100% hallucinated" data on some test PDFs
  - Claude missed passenger names in unclear sections
  - Confidence doesn't correlate with accuracy
  
### **Detection Pattern**
  extract.*(?:scan|handwrit|photo)(?!.*validat|verif|confidence)
  
### **Solution**
  Add validation and confidence scoring:
  
  ```typescript
  async function extractWithConfidence(imageBase64: string) {
    const response = await anthropic.messages.create({
      model: "claude-sonnet-4-20250514",
      messages: [
        {
          role: "user",
          content: [
            {
              type: "image",
              source: { type: "base64", media_type: "image/png", data: imageBase64 },
            },
            {
              type: "text",
              text: `Extract data and rate your confidence for each field.
  
              Return JSON:
              {
                "data": { ... extracted fields ... },
                "confidence": {
                  "overall": 0.0-1.0,
                  "fields": {
                    "field_name": {
                      "value": 0.0-1.0,
                      "reason": "why confident/uncertain"
                    }
                  }
                }
              }`,
            },
          ],
        },
      ],
    });
  
    const result = JSON.parse(response.content[0].text);
  
    // Flag low-confidence extractions
    if (result.confidence.overall < 0.8) {
      result.requiresReview = true;
      result.lowConfidenceFields = Object.entries(result.confidence.fields)
        .filter(([_, v]) => (v as any).value < 0.7)
        .map(([k]) => k);
    }
  
    return result;
  }
  ```
  

## Table Extraction Fragility

### **Id**
table-extraction-fragility
### **Summary**
Table extraction fails on complex layouts
### **Severity**
medium
### **Situation**
Extracting tables with merged cells, nested tables, or spanning headers
### **Why**
  Vision models struggle with:
  - Multi-row header cells
  - Merged cells spanning columns
  - Tables without clear borders
  - Nested/hierarchical tables
  - Tables split across pages
  
  Accuracy drops significantly - one benchmark showed
  47% accuracy on text parsing vs 87% on native image processing.
  
### **Detection Pattern**
  extract.*table(?!.*layout|structure)
  
### **Solution**
  Use specialized prompts and validate structure:
  
  ```typescript
  async function extractComplexTable(imageBase64: string) {
    // First pass: understand table structure
    const structurePrompt = `Analyze this table's structure:
      1. How many header rows are there?
      2. Are there any merged cells?
      3. Are there sub-headers or grouped columns?
      4. Is the table split across pages?
  
      Return as JSON:
      {
        "headerRows": number,
        "hasMergedCells": boolean,
        "hasSubgroups": boolean,
        "isSplit": boolean,
        "description": "human readable description"
      }`;
  
    const structure = await extractWithPrompt(imageBase64, structurePrompt);
  
    // Second pass: extract with structure-aware prompt
    const extractPrompt = structure.hasMergedCells
      ? `Extract this table. Handle merged cells by repeating values.`
      : `Extract this table as a simple grid.`;
  
    const table = await extractWithPrompt(imageBase64, extractPrompt);
  
    // Validate: row counts should match
    if (table.rows.length > 0) {
      const expectedCols = table.headers.length;
      const badRows = table.rows.filter((r) => r.length !== expectedCols);
      if (badRows.length > 0) {
        console.warn(`${badRows.length} rows have incorrect column count`);
      }
    }
  
    return table;
  }
  ```
  

## Multi Column Text Jumbling

### **Id**
multi-column-text-jumbling
### **Summary**
Multi-column layouts get text order wrong
### **Severity**
medium
### **Situation**
Processing newspapers, academic papers, or multi-column documents
### **Why**
  Standard text extraction reads left-to-right, top-to-bottom.
  Multi-column documents need column-first reading order.
  Without layout awareness, text from different columns intermixes.
  
### **Detection Pattern**
  extract.*text(?!.*layout|column)
  
### **Solution**
  Use layout-aware extraction:
  
  ```typescript
  async function extractMultiColumnText(imageBase64: string) {
    const response = await anthropic.messages.create({
      model: "claude-sonnet-4-20250514",
      messages: [
        {
          role: "user",
          content: [
            {
              type: "image",
              source: { type: "base64", media_type: "image/png", data: imageBase64 },
            },
            {
              type: "text",
              text: `This document may have multiple columns.
  
              1. First, identify the layout (single column, two columns, etc.)
              2. For multi-column layouts, read each column top-to-bottom before moving to the next
              3. Preserve logical paragraph breaks
  
              Return JSON:
              {
                "layout": "single" | "two-column" | "three-column" | "complex",
                "columns": [
                  { "text": "content of column 1..." },
                  { "text": "content of column 2..." }
                ],
                "fullText": "combined text in correct reading order"
              }`,
            },
          ],
        },
      ],
    });
  
    return JSON.parse(response.content[0].text);
  }
  ```
  

## Scanned Pdf Ocr Fallback

### **Id**
scanned-pdf-ocr-fallback
### **Summary**
Scanned PDFs need OCR, not text extraction
### **Severity**
medium
### **Situation**
Processing scanned documents or image-only PDFs
### **Why**
  Many PDFs look like text but are actually embedded images.
  Calling pdf.getText() returns empty string.
  Need to rasterize to images and use vision models.
  
### **Detection Pattern**
  pdf.*getText|extractText.*pdf(?!.*ocr|vision|image)
  
### **Solution**
  Detect and handle scanned PDFs:
  
  ```typescript
  import { PdfReader } from "pdfreader";
  import { pdf } from "pdf-to-img";
  
  async function isPDFScanned(pdfPath: string): Promise<boolean> {
    return new Promise((resolve) => {
      let hasText = false;
  
      new PdfReader().parseFileItems(pdfPath, (err, item) => {
        if (err) {
          resolve(true); // Assume scanned if can't parse
          return;
        }
        if (!item) {
          resolve(!hasText);
          return;
        }
        if (item.text) {
          hasText = true;
        }
      });
    });
  }
  
  async function extractPDFContent(pdfPath: string) {
    const isScanned = await isPDFScanned(pdfPath);
  
    if (isScanned) {
      console.log("Scanned PDF detected, using vision extraction");
      return extractWithVision(pdfPath);
    } else {
      // Has native text - can use faster text extraction
      // But vision still better for tables/layouts
      return extractWithVision(pdfPath); // Often vision is still better
    }
  }
  ```
  

## Invoice Format Variation

### **Id**
invoice-format-variation
### **Summary**
Every invoice format is different
### **Severity**
medium
### **Situation**
Extracting invoices from multiple vendors
### **Why**
  No two companies format invoices the same way.
  Training on one format doesn't generalize well.
  Field names vary: "Invoice #" vs "Inv No" vs "Bill Number"
  Layouts vary: vendor at top vs bottom, items inline vs table.
  
### **Detection Pattern**
  extract.*invoice(?!.*schema|template)
  
### **Solution**
  Use flexible schema with field mapping:
  
  ```typescript
  const InvoiceFieldAliases = {
    invoiceNumber: [
      "Invoice #", "Invoice No", "Inv #", "Bill Number",
      "Invoice Number", "Reference", "Doc No",
    ],
    date: [
      "Invoice Date", "Date", "Inv Date", "Bill Date",
      "Document Date", "Issue Date",
    ],
    total: [
      "Total", "Grand Total", "Amount Due", "Balance Due",
      "Total Due", "Invoice Total", "Net Amount",
    ],
  };
  
  async function extractFlexibleInvoice(imageBase64: string) {
    const response = await anthropic.messages.create({
      model: "claude-sonnet-4-20250514",
      messages: [
        {
          role: "user",
          content: [
            {
              type: "image",
              source: { type: "base64", media_type: "image/png", data: imageBase64 },
            },
            {
              type: "text",
              text: `Extract invoice data. Common field names include:
              - Invoice number: "Invoice #", "Inv No", etc.
              - Date: "Invoice Date", "Date", etc.
              - Total: "Total", "Grand Total", "Amount Due", etc.
  
              Map whatever labels you find to these standard fields:
              {
                "invoiceNumber": "...",
                "date": "YYYY-MM-DD",
                "vendorName": "...",
                "total": number,
                "currency": "USD/EUR/etc",
                "lineItems": [...]
              }`,
            },
          ],
        },
      ],
    });
  
    return JSON.parse(response.content[0].text);
  }
  ```
  

## Token Cost Explosion

### **Id**
token-cost-explosion
### **Summary**
PDF images consume massive tokens
### **Severity**
medium
### **Situation**
Processing many pages or high-resolution documents
### **Why**
  Each page as image = ~1000-2000 tokens (Claude)
  100-page PDF = 100k-200k tokens just for input
  At ~$15/million tokens = $1.50-3.00 per large document
  
  Costs add up fast with batch processing.
  
### **Detection Pattern**
  pdf.*extract|process.*document(?!.*cost|budget)
  
### **Solution**
  Track and limit costs:
  
  ```typescript
  const TOKENS_PER_PAGE = 1500; // Approximate
  const COST_PER_MILLION_TOKENS = 15; // Claude Sonnet input
  
  class DocumentCostTracker {
    async estimateCost(pdfPath: string): Promise<{
      pages: number;
      estimatedTokens: number;
      estimatedCost: number;
    }> {
      const pageCount = await countPDFPages(pdfPath);
      const estimatedTokens = pageCount * TOKENS_PER_PAGE;
      const estimatedCost = (estimatedTokens / 1_000_000) * COST_PER_MILLION_TOKENS;
  
      return { pages: pageCount, estimatedTokens, estimatedCost };
    }
  
    async processWithBudget(
      pdfPath: string,
      maxCost: number
    ) {
      const estimate = await this.estimateCost(pdfPath);
  
      if (estimate.estimatedCost > maxCost) {
        throw new Error(
          `Estimated cost $${estimate.estimatedCost.toFixed(2)} exceeds budget $${maxCost}`
        );
      }
  
      return extractFromPDF(pdfPath);
    }
  }
  ```
  

## Password Protected Pdf

### **Id**
password-protected-pdf
### **Summary**
Password-protected PDFs silently fail
### **Severity**
low
### **Situation**
Processing PDFs with password protection
### **Why**
  Password-protected PDFs can't be rasterized or parsed.
  Some libraries fail silently, returning empty results.
  Claude API rejects password-protected uploads.
  
### **Detection Pattern**
  pdf.*process|extract.*pdf(?!.*password|protect)
  
### **Solution**
  Detect and handle protected PDFs:
  
  ```typescript
  import { PDFDocument } from "pdf-lib";
  
  async function isPDFProtected(pdfPath: string): Promise<boolean> {
    try {
      const pdfBytes = fs.readFileSync(pdfPath);
      await PDFDocument.load(pdfBytes);
      return false;
    } catch (error: any) {
      if (error.message.includes("encrypted") || error.message.includes("password")) {
        return true;
      }
      throw error;
    }
  }
  
  async function processSecurePDF(pdfPath: string, password?: string) {
    if (await isPDFProtected(pdfPath)) {
      if (!password) {
        throw new Error("PDF is password-protected. Please provide password.");
      }
  
      const pdfBytes = fs.readFileSync(pdfPath);
      const decrypted = await PDFDocument.load(pdfBytes, { password });
      const decryptedBytes = await decrypted.save();
  
      // Save decrypted version temporarily
      const tempPath = `/tmp/${Date.now()}-decrypted.pdf`;
      fs.writeFileSync(tempPath, decryptedBytes);
  
      try {
        return extractFromPDF(tempPath);
      } finally {
        fs.unlinkSync(tempPath);
      }
    }
  
    return extractFromPDF(pdfPath);
  }
  ```
  