# Document Ai - Validations

## Document API Key in Client Code

### **Id**
doc-api-key-exposed
### **Severity**
error
### **Description**
Document processing API keys must be server-side only
### **Pattern**
  (NEXT_PUBLIC|REACT_APP|VITE).*(LLAMA|UNSTRUCTURED|ANTHROPIC|OPENAI).*KEY
  
### **Message**
Document API key exposed to client. Use server-side routes.
### **Autofix**


## Missing PDF Size Validation

### **Id**
no-pdf-size-check
### **Severity**
warning
### **Description**
PDF file size should be checked before processing
### **Pattern**
  pdf.*process|extract.*pdf(?!.*size|limit|check)
  
### **Message**
PDF processing without size check. Claude limit is 32MB.
### **Autofix**


## Missing Page Count Validation

### **Id**
no-page-count-check
### **Severity**
warning
### **Description**
Page count should be checked before processing
### **Pattern**
  pdf.*extract|process.*document(?!.*page.*limit|max.*page)
  
### **Message**
No page count limit. Claude limit is 100 pages per upload.
### **Autofix**


## Missing Password Protection Check

### **Id**
no-password-check
### **Severity**
warning
### **Description**
PDFs should be checked for password protection
### **Pattern**
  PDFDocument\.load|pdf.*load(?!.*password|protect|encrypt)
  
### **Message**
PDF loaded without checking for password protection.
### **Autofix**


## Missing Output Schema Validation

### **Id**
no-extraction-schema
### **Severity**
warning
### **Description**
Extracted data should be validated against schema
### **Pattern**
  JSON\.parse\(.*response(?!.*schema|parse\(|Schema\.parse)
  
### **Message**
Extraction without schema validation. Use Zod to validate.
### **Autofix**


## Unsafe JSON Parsing

### **Id**
json-parse-unsafe
### **Severity**
warning
### **Description**
JSON parsing should handle malformed responses
### **Pattern**
  JSON\.parse\((?!.*try|catch)
  
### **Message**
JSON.parse without error handling. LLMs may return invalid JSON.
### **Autofix**


## Missing Extraction Cost Tracking

### **Id**
no-extraction-cost-tracking
### **Severity**
warning
### **Description**
Document processing costs should be tracked
### **Pattern**
  extract.*pdf|process.*document(?!.*cost|budget|token)
  
### **Message**
No cost tracking. PDF extraction can be expensive.
### **Autofix**


## Unbounded Batch Processing

### **Id**
unbounded-batch-processing
### **Severity**
warning
### **Description**
Batch processing should have limits
### **Pattern**
  for.*await.*extract|Promise\.all.*extract(?!.*limit|batch)
  
### **Message**
Unbounded batch processing. Add concurrency limits.
### **Autofix**


## Missing Confidence Scoring

### **Id**
no-confidence-scoring
### **Severity**
info
### **Description**
Extraction should include confidence scores
### **Pattern**
  extract.*(?:invoice|receipt|document)(?!.*confidence|score)
  
### **Message**
Consider adding confidence scoring for extracted data.
### **Autofix**


## Missing Data Validation

### **Id**
no-extraction-validation
### **Severity**
warning
### **Description**
Extracted data should be validated for completeness
### **Pattern**
  return.*extracted(?!.*validat|check|verify)
  
### **Message**
Extracted data returned without validation.
### **Autofix**


## Missing Retry Logic

### **Id**
no-extraction-retry
### **Severity**
warning
### **Description**
Document extraction should retry on transient failures
### **Pattern**
  await.*extract(?!.*retry|attempt)
  
### **Message**
No retry logic for extraction. API calls can fail transiently.
### **Autofix**
