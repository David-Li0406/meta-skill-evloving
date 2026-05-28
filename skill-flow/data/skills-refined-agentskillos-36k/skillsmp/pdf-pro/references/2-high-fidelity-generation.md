# Reference: High-Fidelity Generation (HTML-to-PDF)

## Overview
In 2026, the standard for professional PDFs is to render them using a headless browser. This allows the use of modern CSS (Flexbox, Grid, Tailwind 4) and React components.

## 🛠️ The Puppeteer Recipe

### 1. The Template Component
```tsx
// components/pdf/InvoiceTemplate.tsx
export default function InvoiceTemplate({ data }) {
  return (
    <div className="p-10 bg-white font-sans text-black">
      <header className="flex justify-between border-b-2 pb-5">
        <h1 className="text-4xl font-bold">INVOICE</h1>
        <div className="text-right">
          <p># {data.id}</p>
          <p>{data.date}</p>
        </div>
      </header>
      {/* Table and items... */}
    </div>
  );
}
```

### 2. The PDF Service (Bun 2.x)
```typescript
import puppeteer from 'puppeteer';
import { renderToString } from 'react-dom/server';

export async function createPdfFromReact(Component, props) {
  const html = renderToString(<Component {...props} />);
  const tailwindCss = await fs.readFile('./public/pdf.css', 'utf-8');
  
  const fullHtml = `
    <html>
      <head><style>${tailwindCss}</style></head>
      <body>${html}</body>
    </html>
  `;

  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setContent(fullHtml, { waitUntil: 'networkidle0' });
  
  const pdf = await page.pdf({
    format: 'A4',
    displayHeaderFooter: true,
    footerTemplate: '<span style="font-size: 10px; margin-left: 20px;">Page <span class="pageNumber"></span></span>'
  });

  await browser.close();
  return pdf;
}
```

---

## 🎨 CSS for Printing (2026 Tips)
- **`break-inside: avoid`:** Prevents a table row from being split across two pages.
- **`@page { margin: 1cm }`:** Explicitly sets the PDF margins.
- **CMYK Colors:** If the PDF is for professional printing, use CMYK color profiles in your CSS.
- **Bleed and Trim:** Use CSS `box-decoration-break` for high-end graphic reports.

---

## 🚀 Optimization: The "Pre-Warmed" Browser
Launching a browser takes ~500ms. In a high-traffic API, keep a pool of pre-warmed Puppeteer instances or use a dedicated PDF-sidecar service.
