---
name: Create PDF Generator
description: Standard workflow for creating a new PDF generation service in ATLAS using pdf-lib.
version: 1.0.0
---

# Skill: Create PDF Generator for ATLAS

This skill guides the creation of a new PDF generation utility (e.g., specific reports, certificates, or letters).
It ensures the output is consistent with ATLAS branding (fonts, logos) and follows the `pdf-lib` pattern used in `lib/pdf-generator.ts`.

## Execution Steps

### 1. Requirements Analysis
Determine:
- **Document Type**: Letter, Report, Certificate?
- **Entity**: Is it generic or specific to a business unit (e.g., GALUR, ARM)?
- **Dynamic Data**: What fields need to be injected (Client Name, Date, Items table)?

### 2. File Creation
Create a new file in `p:\ATLAS\lib\`.
Naming convention: `[type]-generator-[optional:entity].ts`.
Example: `audit-report-generator.ts`.

### 3. Implementation Template
Use this structure `lib/pdf-generator.ts` as a base.

**Key Components to Include:**
1.  **Imports**:
    ```typescript
    import { PDFDocument, rgb, StandardFonts } from "pdf-lib"
    import { format } from "date-fns"
    import { es } from "date-fns/locale"
    // Import entity logos if applicable
    ```
2.  **Interface Definition**:
    Define the input data structure efficiently.
    ```typescript
    interface [DocName]Data {
      title: string;
      items: any[];
      // ...
    }
    ```
3.  **Main Function**:
    `export async function generate[DocName]PDF(data: [DocName]Data): Promise<Uint8Array>`

4.  **Header Generation**:
    *CRITICAL*: Always include the Company Logo and "ATLAS Platform" watermark or footer depending on the design requirement.

5.  **Text Drawing Helper**:
    Use a helper function to manage text wrapping, as `pdf-lib` does not handle it natively.
    *(Tip: Reuse logic from `lib/pdf-generator.ts` for text wrapping)*.

### 4. Integration
Once created, suggest where to use it:
- A new **API Route** if it's generated via a direct link (`app/api/generate-pdf/...`).
- A **Client Component** (button) that calls the function (if purely client-side compilation is possible, though `pdf-lib` works in both; usually heavy generation is preferred on client to save server costs, OR server if secrets/images are private).

### 5. Testing
Suggest creating a temporary test trigger or verify the binary output (Uint8Array) downloads correctly as a `.pdf`.
