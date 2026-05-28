# Document Processing Strategies

## Chunking Strategies

### 1. Fixed-Size Chunking

Simple but can break semantic boundaries.

```csharp
public class FixedSizeChunker
{
    private readonly int _chunkSize = 512;
    private readonly int _overlap = 50;

    public List<Chunk> Chunk(string text)
    {
        var chunks = new List<Chunk>();
        for (int i = 0; i < text.Length; i += _chunkSize - _overlap)
        {
            var chunkText = text.Substring(
                i,
                Math.Min(_chunkSize, text.Length - i));
            chunks.Add(new Chunk { Text = chunkText, Index = i });
        }
        return chunks;
    }
}
```

### 2. Semantic Chunking

Uses embeddings to find natural boundaries.

```csharp
public class SemanticChunker
{
    public async Task<List<Chunk>> ChunkAsync(
        string text,
        EmbeddingClient embeddings)
    {
        // Split into sentences
        var sentences = SplitSentences(text);
        
        // Get embeddings for each sentence
        var embeddingVectors = await embeddings
            .GetEmbeddingsAsync(sentences);
        
        // Find semantic breaks where cosine similarity drops
        var breaks = FindSemanticBreaks(embeddingVectors);
        
        // Create chunks between breaks
        return CreateChunks(sentences, breaks);
    }
}
```

### 3. Hierarchical Chunking

Maintains document structure.

```csharp
public class HierarchicalChunker
{
    public DocumentTree Chunk(string text)
    {
        var tree = new DocumentTree();
        
        // Level 1: Sections
        tree.Root = ExtractSections(text);
        
        // Level 2: Paragraphs
        foreach (var section in tree.Root.Sections)
        {
            section.Paragraphs = ExtractParagraphs(section.Text);
        }
        
        // Level 3: Sentences (for fine-grained search)
        foreach (var para in tree.Root.AllParagraphs())
        {
            para.Sentences = SplitSentences(para.Text);
        }
        
        return tree;
    }
}
```

## Metadata Extraction

### Essential Fields

```csharp
public class DocumentMetadata
{
    public string DocumentId { get; set; }
    public string Title { get; set; }
    public string Author { get; set; }
    public DateTime CreatedDate { get; set; }
    public DateTime? ModifiedDate { get; set; }
    public List<string> Tags { get; set; }
    public string Category { get; set; }
    public int PageNumber { get; set; }
    public string ChunkId { get; set; }
    public int ChunkIndex { get; set; }
}
```

### Extraction Strategies

#### PDF

```csharp
public class PDFMetadataExtractor
{
    public DocumentMetadata Extract(string pdfPath)
    {
        using var doc = PdfDocument.Open(pdfPath);
        return new DocumentMetadata
        {
            Title = doc.GetMetadata().Title ?? Path.GetFileName(pdfPath),
            CreatedDate = doc.GetMetadata().Created.Date,
            Author = doc.GetMetadata().Author,
            PageCount = doc.NumberOfPages
        };
    }
}
```

#### DOCX

```csharp
public class DOCXMetadataExtractor
{
    public DocumentMetadata Extract(string docxPath)
    {
        using var doc = WordprocessingDocument.Open(docxPath, false);
        var props = doc.PackageProperties;
        return new DocumentMetadata
        {
            Title = props.Title ?? Path.GetFileName(docxPath),
            Author = props.Creator,
            CreatedDate = props.Created,
            ModifiedDate = props.Modified,
            Subject = props.Subject,
            Keywords = props.Keywords?.Split(',')
        };
    }
}
```

## Preprocessing

### Text Cleaning

```csharp
public class TextCleaner
{
    public string Clean(string text)
    {
        return text
            .NormalizeWhiteSpace()
            .RemoveControlCharacters()
            .FixEncodingIssues()
            .RemoveHeadersFooters();
    }
}
```

### Table Extraction

```csharp
public class TableExtractor
{
    public List<Table> ExtractTables(string documentPath)
    {
        // Extract tables as structured data
        // Convert to markdown for LLM consumption
        // Store table metadata (headers, row count)
    }
}
```
