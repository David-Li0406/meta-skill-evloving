---
name: PDF Generation
description: Generate PDFs from HTML, reports, invoices, and documents
---

# PDF Generation Skill

## Libraries

### React-PDF
```bash
npm install @react-pdf/renderer
```

```jsx
import { Document, Page, Text, View, StyleSheet, PDFDownloadLink } from '@react-pdf/renderer';

const styles = StyleSheet.create({
  page: { padding: 30 },
  title: { fontSize: 24, marginBottom: 20 },
  section: { marginBottom: 10 }
});

const MyDocument = ({ data }) => (
  <Document>
    <Page size="A4" style={styles.page}>
      <Text style={styles.title}>Tournament Report</Text>
      <View style={styles.section}>
        <Text>Player: {data.name}</Text>
        <Text>Hands Played: {data.hands}</Text>
        <Text>Win Rate: {data.winRate}%</Text>
      </View>
    </Page>
  </Document>
);

// Usage
<PDFDownloadLink document={<MyDocument data={playerData} />} fileName="report.pdf">
  {({ loading }) => loading ? 'Generating...' : 'Download Report'}
</PDFDownloadLink>
```

### Puppeteer (HTML to PDF)
```javascript
const puppeteer = require('puppeteer');

async function generatePDF(html, outputPath) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setContent(html, { waitUntil: 'networkidle0' });
  await page.pdf({
    path: outputPath,
    format: 'A4',
    printBackground: true,
    margin: { top: '20px', right: '20px', bottom: '20px', left: '20px' }
  });
  await browser.close();
}
```

### PDFKit (Node.js)
```javascript
const PDFDocument = require('pdfkit');
const fs = require('fs');

const doc = new PDFDocument();
doc.pipe(fs.createWriteStream('output.pdf'));

doc.fontSize(25).text('Hello World', 100, 80);
doc.image('logo.png', 100, 150, { width: 300 });
doc.end();
```

## CLI Tools

### wkhtmltopdf
```bash
# HTML file to PDF
wkhtmltopdf input.html output.pdf

# URL to PDF
wkhtmltopdf https://smarter.poker report.pdf

# With options
wkhtmltopdf --page-size A4 --margin-top 10mm --margin-bottom 10mm input.html output.pdf
```

### WeasyPrint (Python)
```bash
# Install
pip install weasyprint

# Usage
weasyprint input.html output.pdf
```

## Invoice Template
```jsx
const InvoicePDF = ({ invoice }) => (
  <Document>
    <Page size="A4" style={styles.page}>
      <View style={styles.header}>
        <Image src="/logo.png" style={styles.logo} />
        <Text style={styles.title}>INVOICE #{invoice.number}</Text>
      </View>
      
      <View style={styles.table}>
        <View style={styles.tableRow}>
          <Text style={styles.tableCell}>Description</Text>
          <Text style={styles.tableCell}>Amount</Text>
        </View>
        {invoice.items.map(item => (
          <View key={item.id} style={styles.tableRow}>
            <Text style={styles.tableCell}>{item.description}</Text>
            <Text style={styles.tableCell}>${item.amount}</Text>
          </View>
        ))}
      </View>
      
      <View style={styles.total}>
        <Text>Total: ${invoice.total}</Text>
      </View>
    </Page>
  </Document>
);
```

## Best Practices
- Use vector graphics when possible (SVG)
- Embed fonts for consistency
- Optimize images before embedding
- Use appropriate page sizes (A4, Letter)
- Include proper margins for printing
