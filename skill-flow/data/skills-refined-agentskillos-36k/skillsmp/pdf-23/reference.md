# Referência Avançada de Processamento de PDF

Este documento contém recursos avançados de processamento de PDF, exemplos detalhados e bibliotecas adicionais não cobertas nas instruções principais da habilidade.

## Biblioteca pypdfium2 (Licença Apache/BSD)

### Visão Geral

pypdfium2 é uma binding Python para PDFium (biblioteca PDF do Chromium). É excelente para renderização rápida de PDF, geração de imagens e serve como substituto do PyMuPDF.

### Renderizar PDF para Imagens

```python
import pypdfium2 as pdfium
from PIL import Image

# Carregar PDF
pdf = pdfium.PdfDocument("document.pdf")

# Renderizar página para imagem
page = pdf[0]  # Primeira página
bitmap = page.render(
    scale=2.0,  # Maior resolução
    rotation=0  # Sem rotação
)

# Converter para Imagem PIL
img = bitmap.to_pil()
img.save("page_1.png", "PNG")

# Processar várias páginas
for i, page in enumerate(pdf):
    bitmap = page.render(scale=1.5)
    img = bitmap.to_pil()
    img.save(f"page_{i+1}.jpg", "JPEG", quality=90)
```

### Extrair Texto com pypdfium2

```python
import pypdfium2 as pdfium

pdf = pdfium.PdfDocument("document.pdf")
for i, page in enumerate(pdf):
    text = page.get_text()
    print(f"Página {i+1} comprimento do texto: {len(text)} caracteres")
```

## Bibliotecas JavaScript

### pdf-lib (Licença MIT)

pdf-lib é uma poderosa biblioteca JavaScript para criar e modificar documentos PDF em qualquer ambiente JavaScript.

#### Carregar e Manipular PDF Existente

```javascript
import { PDFDocument } from "pdf-lib";
import fs from "fs";

async function manipulatePDF() {
  // Carregar PDF existente
  const existingPdfBytes = fs.readFileSync("input.pdf");
  const pdfDoc = await PDFDocument.load(existingPdfBytes);

  // Obter contagem de páginas
  const pageCount = pdfDoc.getPageCount();
  console.log(`Documento tem ${pageCount} páginas`);

  // Adicionar nova página
  const newPage = pdfDoc.addPage([600, 400]);
  newPage.drawText("Adicionado por pdf-lib", {
    x: 100,
    y: 300,
    size: 16,
  });

  // Salvar PDF modificado
  const pdfBytes = await pdfDoc.save();
  fs.writeFileSync("modified.pdf", pdfBytes);
}
```

#### Criar PDFs Complexos do Zero

```javascript
import { PDFDocument, rgb, StandardFonts } from "pdf-lib";
import fs from "fs";

async function createPDF() {
  const pdfDoc = await PDFDocument.create();

  // Adicionar fontes
  const helveticaFont = await pdfDoc.embedFont(StandardFonts.Helvetica);
  const helveticaBold = await pdfDoc.embedFont(StandardFonts.HelveticaBold);

  // Adicionar página
  const page = pdfDoc.addPage([595, 842]); // Tamanho A4
  const { width, height } = page.getSize();

  // Adicionar texto com estilo
  page.drawText("Fatura #12345", {
    x: 50,
    y: height - 50,
    size: 18,
    font: helveticaBold,
    color: rgb(0.2, 0.2, 0.8),
  });

  // Adicionar retângulo (fundo do cabeçalho)
  page.drawRectangle({
    x: 40,
    y: height - 100,
    width: width - 80,
    height: 30,
    color: rgb(0.9, 0.9, 0.9),
  });

  // Adicionar conteúdo tipo tabela
  const items = [
    ["Item", "Qtd", "Preço", "Total"],
    ["Widget", "2", "$50", "$100"],
    ["Gadget", "1", "$75", "$75"],
  ];

  let yPos = height - 150;
  items.forEach((row) => {
    let xPos = 50;
    row.forEach((cell) => {
      page.drawText(cell, {
        x: xPos,
        y: yPos,
        size: 12,
        font: helveticaFont,
      });
      xPos += 120;
    });
    yPos -= 25;
  });

  const pdfBytes = await pdfDoc.save();
  fs.writeFileSync("created.pdf", pdfBytes);
}
```

#### Operações Avançadas de Mesclagem e Divisão

```javascript
import { PDFDocument } from "pdf-lib";
import fs from "fs";

async function mergePDFs() {
  // Criar novo documento
  const mergedPdf = await PDFDocument.create();

  // Carregar PDFs de origem
  const pdf1Bytes = fs.readFileSync("doc1.pdf");
  const pdf2Bytes = fs.readFileSync("doc2.pdf");

  const pdf1 = await PDFDocument.load(pdf1Bytes);
  const pdf2 = await PDFDocument.load(pdf2Bytes);

  // Copiar páginas do primeiro PDF
  const pdf1Pages = await mergedPdf.copyPages(pdf1, pdf1.getPageIndices());
  pdf1Pages.forEach((page) => mergedPdf.addPage(page));

  // Copiar páginas específicas do segundo PDF (páginas 0, 2, 4)
  const pdf2Pages = await mergedPdf.copyPages(pdf2, [0, 2, 4]);
  pdf2Pages.forEach((page) => mergedPdf.addPage(page));

  const mergedPdfBytes = await mergedPdf.save();
  fs.writeFileSync("merged.pdf", mergedPdfBytes);
}
```

### pdfjs-dist (Licença Apache)

PDF.js é a biblioteca JavaScript da Mozilla para renderização de PDFs no navegador.

#### Carregamento e Renderização Básica de PDF

```javascript
import * as pdfjsLib from "pdfjs-dist";

// Configurar worker (importante para desempenho)
pdfjsLib.GlobalWorkerOptions.workerSrc = "./pdf.worker.js";

async function renderPDF() {
  // Carregar PDF
  const loadingTask = pdfjsLib.getDocument("document.pdf");
  const pdf = await loadingTask.promise;

  console.log(`PDF carregado com ${pdf.numPages} páginas`);

  // Obter primeira página
  const page = await pdf.getPage(1);
  const viewport = page.getViewport({ scale: 1.5 });

  // Renderizar no canvas
  const canvas = document.createElement("canvas");
  const context = canvas.getContext("2d");
  canvas.height = viewport.height;
  canvas.width = viewport.width;

  const renderContext = {
    canvasContext: context,
    viewport: viewport,
  };

  await page.render(renderContext).promise;
  document.body.appendChild(canvas);
}
```

#### Extrair Texto com Coordenadas

```javascript
import * as pdfjsLib from "pdfjs-dist";

async function extractText() {
  const loadingTask = pdfjsLib.getDocument("document.pdf");
  const pdf = await loadingTask.promise;

  let fullText = "";

  // Extrair texto de todas as páginas
  for (let i = 1; i <= pdf.numPages; i++) {
    const page = await pdf.getPage(i);
    const textContent = await page.getTextContent();

    const pageText = textContent.items.map((item) => item.str).join(" ");

    fullText += `\n--- Página ${i} ---\n${pageText}`;

    // Obter texto com coordenadas para processamento avançado
    const textWithCoords = textContent.items.map((item) => ({
      text: item.str,
      x: item.transform[4],
      y: item.transform[5],
      width: item.width,
      height: item.height,
    }));
  }

  console.log(fullText);
  return fullText;
}
```

#### Extrair Anotações e Formulários

```javascript
import * as pdfjsLib from "pdfjs-dist";

async function extractAnnotations() {
  const loadingTask = pdfjsLib.getDocument("annotated.pdf");
  const pdf = await loadingTask.promise;

  for (let i = 1; i <= pdf.numPages; i++) {
    const page = await pdf.getPage(i);
    const annotations = await page.getAnnotations();

    annotations.forEach((annotation) => {
      console.log(`Tipo de anotação: ${annotation.subtype}`);
      console.log(`Conteúdo: ${annotation.contents}`);
      console.log(`Coordenadas: ${JSON.stringify(annotation.rect)}`);
    });
  }
}
```

## Operações Avançadas de Linha de Comando

### Recursos Avançados do poppler-utils

#### Extrair Texto com Coordenadas de Caixa Delimitadora

```bash
# Extrair texto com coordenadas de caixa delimitadora (essencial para dados estruturados)
pdftotext -bbox-layout document.pdf output.xml

# A saída XML contém coordenadas precisas para cada elemento de texto
```

#### Conversão de Imagem Avançada

```bash
# Converter para imagens PNG com resolução específica
pdftoppm -png -r 300 document.pdf output_prefix

# Converter intervalo de páginas específico com alta resolução
pdftoppm -png -r 600 -f 1 -l 3 document.pdf high_res_pages

# Converter para JPEG com configuração de qualidade
pdftoppm -jpeg -jpegopt quality=85 -r 200 document.pdf jpeg_output
```

#### Extrair Imagens Incorporadas

```bash
# Extrair todas as imagens incorporadas com metadados
pdfimages -j -p document.pdf page_images

# Listar informações de imagem sem extrair
pdfimages -list document.pdf

# Extrair imagens em seu formato original
pdfimages -all document.pdf images/img
```

### Recursos Avançados do qpdf

#### Manipulação de Página Complexa

```bash
# Dividir PDF em grupos de páginas
qpdf --split-pages=3 input.pdf output_group_%02d.pdf

# Extrair páginas específicas com intervalos complexos
qpdf input.pdf --pages input.pdf 1,3-5,8,10-end -- extracted.pdf

# Mesclar páginas específicas de múltiplos PDFs
qpdf --empty --pages doc1.pdf 1-3 doc2.pdf 5-7 doc3.pdf 2,4 -- combined.pdf
```

#### Otimização e Reparo de PDF

```bash
# Otimizar PDF para web (linearizar para streaming)
qpdf --linearize input.pdf optimized.pdf

# Remover objetos não utilizados e comprimir
qpdf --optimize-level=all input.pdf compressed.pdf

# Tentar reparar estrutura de PDF corrompida
qpdf --check input.pdf
qpdf --fix-qdf damaged.pdf repaired.pdf

# Mostrar estrutura detalhada do PDF para depuração
qpdf --show-all-pages input.pdf > structure.txt
```

#### Criptografia Avançada

```bash
# Adicionar proteção por senha com permissões específicas
qpdf --encrypt user_pass owner_pass 256 --print=none --modify=none -- input.pdf encrypted.pdf

# Verificar status de criptografia
qpdf --show-encryption encrypted.pdf

# Remover proteção por senha (requer senha)
qpdf --password=secret123 --decrypt encrypted.pdf decrypted.pdf
```

## Técnicas Avançadas em Python

### Recursos Avançados do pdfplumber

#### Extrair Texto com Coordenadas Precisas

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    page = pdf.pages[0]

    # Extrair todo o texto com coordenadas
    chars = page.chars
    for char in chars[:10]:  # Primeiros 10 caracteres
        print(f"Char: '{char['text']}' em x:{char['x0']:.1f} y:{char['y0']:.1f}")

    # Extrair texto por caixa delimitadora (esquerda, topo, direita, baixo)
    bbox_text = page.within_bbox((100, 100, 400, 200)).extract_text()
```

#### Extração de Tabela Avançada com Configurações Personalizadas

```python
import pdfplumber
import pandas as pd

with pdfplumber.open("complex_table.pdf") as pdf:
    page = pdf.pages[0]

    # Extrair tabelas com configurações personalizadas para layouts complexos
    table_settings = {
        "vertical_strategy": "lines",
        "horizontal_strategy": "lines",
        "snap_tolerance": 3,
        "intersection_tolerance": 15
    }
    tables = page.extract_tables(table_settings)

    # Depuração visual para extração de tabela
    img = page.to_image(resolution=150)
    img.save("debug_layout.png")
```

### Recursos Avançados do reportlab

#### Criar Relatórios Profissionais com Tabelas

```python
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# Dados de exemplo
data = [
    ['Produto', 'Q1', 'Q2', 'Q3', 'Q4'],
    ['Widgets', '120', '135', '142', '158'],
    ['Gadgets', '85', '92', '98', '105']
]

# Criar PDF com tabela
doc = SimpleDocTemplate("report.pdf")
elements = []

# Adicionar título
styles = getSampleStyleSheet()
title = Paragraph("Relatório Trimestral de Vendas", styles['Title'])
elements.append(title)

# Adicionar tabela com estilo avançado
table = Table(data)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 14),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))
elements.append(table)

doc.build(elements)
```

## Fluxos de Trabalho Complexos

### Extrair Figuras/Imagens de PDF

#### Método 1: Usando pdfimages (mais rápido)

```bash
# Extrair todas as imagens com qualidade original
pdfimages -all document.pdf images/img
```

#### Método 2: Usando pypdfium2 + Processamento de Imagem

```python
import pypdfium2 as pdfium
from PIL import Image
import numpy as np

def extract_figures(pdf_path, output_dir):
    pdf = pdfium.PdfDocument(pdf_path)

    for page_num, page in enumerate(pdf):
        # Renderizar página em alta resolução
        bitmap = page.render(scale=3.0)
        img = bitmap.to_pil()

        # Converter para numpy para processamento
        img_array = np.array(img)

        # Detecção de figura simples (regiões não brancas)
        mask = np.any(img_array != [255, 255, 255], axis=2)

        # Encontrar contornos e extrair caixas delimitadoras
        # (Isso é simplificado - implementação real precisaria de detecção mais sofisticada)

        # Salvar figuras detectadas
        # ... implementação depende de necessidades específicas
```

### Processamento de PDF em Lote com Tratamento de Erro

```python
import os
import glob
from pypdf import PdfReader, PdfWriter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def batch_process_pdfs(input_dir, operation='merge'):
    pdf_files = glob.glob(os.path.join(input_dir, "*.pdf"))

    if operation == 'merge':
        writer = PdfWriter()
        for pdf_file in pdf_files:
            try:
                reader = PdfReader(pdf_file)
                for page in reader.pages:
                    writer.add_page(page)
                logger.info(f"Processado: {pdf_file}")
            except Exception as e:
                logger.error(f"Falha ao processar {pdf_file}: {e}")
                continue

        with open("batch_merged.pdf", "wb") as output:
            writer.write(output)

    elif operation == 'extract_text':
        for pdf_file in pdf_files:
            try:
                reader = PdfReader(pdf_file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()

                output_file = pdf_file.replace('.pdf', '.txt')
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(text)
                logger.info(f"Texto extraído de: {pdf_file}")

            except Exception as e:
                logger.error(f"Falha ao extrair texto de {pdf_file}: {e}")
                continue
```

### Recorte Avançado de PDF

```python
from pypdf import PdfWriter, PdfReader

reader = PdfReader("input.pdf")
writer = PdfWriter()

# Recortar página (esquerda, baixo, direita, topo em pontos)
page = reader.pages[0]
page.mediabox.left = 50
page.mediabox.bottom = 50
page.mediabox.right = 550
page.mediabox.top = 750

writer.add_page(page)
with open("cropped.pdf", "wb") as output:
    writer.write(output)
```

## Dicas de Otimização de Desempenho

### 1. Para Grandes PDFs

- Use abordagens de streaming em vez de carregar todo o PDF na memória
- Use `qpdf --split-pages` para dividir arquivos grandes
- Processe páginas individualmente com pypdfium2

### 2. Para Extração de Texto

- `pdftotext -bbox-layout` é o mais rápido para extração de texto simples
- Use pdfplumber para dados estruturados e tabelas
- Evite `pypdf.extract_text()` para documentos muito grandes

### 3. Para Extração de Imagem

- `pdfimages` é muito mais rápido do que renderizar páginas
- Use baixa resolução para visualizações, alta resolução para saída final

### 4. Para Preenchimento de Formulário

- pdf-lib mantém a estrutura do formulário melhor do que a maioria das alternativas
- Pré-valide campos de formulário antes do processamento

### 5. Gerenciamento de Memória

```python
# Processar PDFs em pedaços
def process_large_pdf(pdf_path, chunk_size=10):
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)

    for start_idx in range(0, total_pages, chunk_size):
        end_idx = min(start_idx + chunk_size, total_pages)
        writer = PdfWriter()

        for i in range(start_idx, end_idx):
            writer.add_page(reader.pages[i])

        # Processar pedaço
        with open(f"chunk_{start_idx//chunk_size}.pdf", "wb") as output:
            writer.write(output)
```

## Solução de Problemas Comuns

### PDFs Criptografados

```python
# Lidar com PDFs protegidos por senha
from pypdf import PdfReader

try:
    reader = PdfReader("encrypted.pdf")
    if reader.is_encrypted:
        reader.decrypt("password")
except Exception as e:
    print(f"Falha ao descriptografar: {e}")
```

### PDFs Corrompidos

```bash
# Usar qpdf para reparar
qpdf --check corrupted.pdf
qpdf --replace-input corrupted.pdf
```

### Problemas de Extração de Texto

```python
# Fallback para OCR para PDFs digitalizados
import pytesseract
from pdf2image import convert_from_path

def extract_text_with_ocr(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for i, image in enumerate(images):
        text += pytesseract.image_to_string(image)
    return text
```

## Informações de Licença

- **pypdf**: Licença BSD
- **pdfplumber**: Licença MIT
- **pypdfium2**: Licença Apache/BSD
- **reportlab**: Licença BSD
- **poppler-utils**: Licença GPL-2
- **qpdf**: Licença Apache
- **pdf-lib**: Licença MIT
- **pdfjs-dist**: Licença Apache
