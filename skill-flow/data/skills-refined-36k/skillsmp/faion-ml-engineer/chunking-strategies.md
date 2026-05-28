---
id: chunking-strategies
name: "Chunking Strategies"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Chunking Strategies

## Overview

Chunking is the process of splitting documents into smaller pieces for embedding and retrieval. The chunking strategy significantly impacts RAG performance - too large chunks dilute relevance, too small chunks lose context.

## When to Use

- Preparing documents for RAG pipelines
- Building semantic search systems
- Processing long documents for LLMs
- Creating knowledge bases

## Key Concepts

### Chunking Trade-offs

| Aspect | Small Chunks | Large Chunks |
|--------|--------------|--------------|
| Precision | High (focused) | Low (diluted) |
| Context | Limited | Preserved |
| Retrieval | More granular | Fewer results |
| LLM Input | More chunks needed | Fewer chunks needed |
| Storage | More vectors | Fewer vectors |

### Typical Sizes

| Document Type | Chunk Size | Overlap |
|---------------|------------|---------|
| Technical docs | 500-1000 tokens | 50-100 |
| Legal documents | 1000-1500 tokens | 100-200 |
| Chat logs | 200-400 tokens | 20-50 |
| Code | 500-800 tokens | 0-50 |
| News articles | 300-600 tokens | 50-100 |

## Implementation

### Fixed-Size Chunking

```python
from typing import List, Dict
import tiktoken

class FixedSizeChunker:
    """Split text into fixed-size chunks with overlap."""

    def __init__(
        self,
        chunk_size: int = 500,
        overlap: int = 50,
        encoding: str = "cl100k_base"
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.tokenizer = tiktoken.get_encoding(encoding)

    def chunk(self, text: str) -> List[Dict]:
        """Split text into token-based chunks."""
        tokens = self.tokenizer.encode(text)
        chunks = []

        start = 0
        chunk_id = 0

        while start < len(tokens):
            end = start + self.chunk_size

            # Get token slice
            chunk_tokens = tokens[start:end]
            chunk_text = self.tokenizer.decode(chunk_tokens)

            chunks.append({
                "id": chunk_id,
                "text": chunk_text,
                "start_token": start,
                "end_token": min(end, len(tokens)),
                "token_count": len(chunk_tokens)
            })

            start = end - self.overlap
            chunk_id += 1

        return chunks

# Usage
chunker = FixedSizeChunker(chunk_size=500, overlap=50)
chunks = chunker.chunk(long_document)
```

### Sentence-Based Chunking

```python
import nltk
from typing import List, Dict

nltk.download('punkt', quiet=True)

class SentenceChunker:
    """Chunk by sentences, respecting size limits."""

    def __init__(
        self,
        max_chunk_size: int = 500,
        min_chunk_size: int = 100,
        overlap_sentences: int = 1
    ):
        self.max_chunk_size = max_chunk_size
        self.min_chunk_size = min_chunk_size
        self.overlap_sentences = overlap_sentences

    def chunk(self, text: str) -> List[Dict]:
        """Split text into sentence-based chunks."""
        sentences = nltk.sent_tokenize(text)
        chunks = []
        current_chunk = []
        current_size = 0

        for i, sentence in enumerate(sentences):
            sentence_size = len(sentence.split())

            if current_size + sentence_size <= self.max_chunk_size:
                current_chunk.append(sentence)
                current_size += sentence_size
            else:
                # Save current chunk
                if current_size >= self.min_chunk_size:
                    chunks.append({
                        "text": " ".join(current_chunk),
                        "sentence_count": len(current_chunk),
                        "word_count": current_size
                    })

                # Start new chunk with overlap
                overlap_start = max(0, len(current_chunk) - self.overlap_sentences)
                current_chunk = current_chunk[overlap_start:] + [sentence]
                current_size = sum(len(s.split()) for s in current_chunk)

        # Don't forget last chunk
        if current_chunk:
            chunks.append({
                "text": " ".join(current_chunk),
                "sentence_count": len(current_chunk),
                "word_count": current_size
            })

        return chunks
```

### Paragraph-Based Chunking

```python
from typing import List, Dict
import re

class ParagraphChunker:
    """Chunk by paragraphs with size constraints."""

    def __init__(
        self,
        max_chunk_size: int = 1000,
        min_chunk_size: int = 200
    ):
        self.max_chunk_size = max_chunk_size
        self.min_chunk_size = min_chunk_size

    def chunk(self, text: str) -> List[Dict]:
        """Split text by paragraphs."""
        # Split by double newline
        paragraphs = re.split(r'\n\s*\n', text)
        paragraphs = [p.strip() for p in paragraphs if p.strip()]

        chunks = []
        current_chunk = []
        current_size = 0

        for para in paragraphs:
            para_size = len(para.split())

            # Single paragraph exceeds max - split it
            if para_size > self.max_chunk_size:
                # Save current chunk first
                if current_chunk:
                    chunks.append({
                        "text": "\n\n".join(current_chunk),
                        "paragraph_count": len(current_chunk)
                    })
                    current_chunk = []
                    current_size = 0

                # Split large paragraph
                sub_chunks = self._split_large_paragraph(para)
                chunks.extend(sub_chunks)
                continue

            if current_size + para_size <= self.max_chunk_size:
                current_chunk.append(para)
                current_size += para_size
            else:
                # Save and start new
                if current_size >= self.min_chunk_size:
                    chunks.append({
                        "text": "\n\n".join(current_chunk),
                        "paragraph_count": len(current_chunk)
                    })
                current_chunk = [para]
                current_size = para_size

        # Last chunk
        if current_chunk:
            chunks.append({
                "text": "\n\n".join(current_chunk),
                "paragraph_count": len(current_chunk)
            })

        return chunks

    def _split_large_paragraph(self, para: str) -> List[Dict]:
        """Split oversized paragraph by sentences."""
        import nltk
        sentences = nltk.sent_tokenize(para)
        chunks = []
        current = []
        current_size = 0

        for sent in sentences:
            sent_size = len(sent.split())
            if current_size + sent_size <= self.max_chunk_size:
                current.append(sent)
                current_size += sent_size
            else:
                if current:
                    chunks.append({"text": " ".join(current), "paragraph_count": 1})
                current = [sent]
                current_size = sent_size

        if current:
            chunks.append({"text": " ".join(current), "paragraph_count": 1})

        return chunks
```

### Semantic Chunking

```python
import numpy as np
from typing import List, Dict
import nltk

class SemanticChunker:
    """Chunk based on semantic similarity between sentences."""

    def __init__(
        self,
        embedding_func: callable,
        similarity_threshold: float = 0.75,
        max_chunk_size: int = 1000,
        min_chunk_size: int = 100
    ):
        self.embedding_func = embedding_func
        self.similarity_threshold = similarity_threshold
        self.max_chunk_size = max_chunk_size
        self.min_chunk_size = min_chunk_size

    def chunk(self, text: str) -> List[Dict]:
        """Split text based on semantic breaks."""
        sentences = nltk.sent_tokenize(text)

        if len(sentences) <= 1:
            return [{"text": text, "sentence_count": len(sentences)}]

        # Get embeddings for all sentences
        embeddings = [self.embedding_func(s) for s in sentences]

        # Find semantic breakpoints
        breakpoints = self._find_breakpoints(embeddings)

        # Create chunks
        chunks = []
        start_idx = 0

        for break_idx in breakpoints + [len(sentences)]:
            chunk_sentences = sentences[start_idx:break_idx]
            chunk_text = " ".join(chunk_sentences)

            # Check size constraints
            if len(chunk_text.split()) > self.max_chunk_size:
                # Split oversized chunk
                sub_chunks = self._split_chunk(chunk_sentences)
                chunks.extend(sub_chunks)
            elif len(chunk_text.split()) >= self.min_chunk_size:
                chunks.append({
                    "text": chunk_text,
                    "sentence_count": len(chunk_sentences)
                })
            elif chunks:
                # Merge with previous if too small
                prev = chunks[-1]
                prev["text"] += " " + chunk_text
                prev["sentence_count"] += len(chunk_sentences)

            start_idx = break_idx

        return chunks

    def _find_breakpoints(self, embeddings: List[np.ndarray]) -> List[int]:
        """Find indices where semantic similarity drops."""
        breakpoints = []

        for i in range(1, len(embeddings)):
            similarity = self._cosine_similarity(embeddings[i-1], embeddings[i])

            if similarity < self.similarity_threshold:
                breakpoints.append(i)

        return breakpoints

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calculate cosine similarity."""
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def _split_chunk(self, sentences: List[str]) -> List[Dict]:
        """Split oversized chunk by size."""
        chunks = []
        current = []
        current_size = 0

        for sent in sentences:
            sent_size = len(sent.split())
            if current_size + sent_size <= self.max_chunk_size:
                current.append(sent)
                current_size += sent_size
            else:
                if current:
                    chunks.append({
                        "text": " ".join(current),
                        "sentence_count": len(current)
                    })
                current = [sent]
                current_size = sent_size

        if current:
            chunks.append({
                "text": " ".join(current),
                "sentence_count": len(current)
            })

        return chunks
```

### Document Structure Chunking

```python
import re
from typing import List, Dict

class MarkdownChunker:
    """Chunk Markdown documents by headers and structure."""

    def __init__(
        self,
        max_chunk_size: int = 1000,
        include_header_in_chunk: bool = True
    ):
        self.max_chunk_size = max_chunk_size
        self.include_header = include_header_in_chunk

    def chunk(self, text: str) -> List[Dict]:
        """Split Markdown by headers."""
        # Pattern for headers
        header_pattern = r'^(#{1,6})\s+(.+)$'

        lines = text.split('\n')
        chunks = []
        current_chunk = {"headers": [], "content": [], "level": 0}

        for line in lines:
            header_match = re.match(header_pattern, line)

            if header_match:
                # Save current chunk if not empty
                if current_chunk["content"]:
                    chunks.append(self._finalize_chunk(current_chunk))

                # Start new chunk
                level = len(header_match.group(1))
                title = header_match.group(2)

                # Inherit higher-level headers
                parent_headers = [
                    h for h in current_chunk["headers"]
                    if h["level"] < level
                ]

                current_chunk = {
                    "headers": parent_headers + [{"level": level, "title": title}],
                    "content": [],
                    "level": level
                }

                if self.include_header:
                    current_chunk["content"].append(line)
            else:
                current_chunk["content"].append(line)

                # Check size
                content_text = '\n'.join(current_chunk["content"])
                if len(content_text.split()) > self.max_chunk_size:
                    # Split current chunk
                    chunks.append(self._finalize_chunk(current_chunk))
                    current_chunk["content"] = []

        # Don't forget last chunk
        if current_chunk["content"]:
            chunks.append(self._finalize_chunk(current_chunk))

        return chunks

    def _finalize_chunk(self, chunk: Dict) -> Dict:
        """Prepare chunk for output."""
        header_path = " > ".join(h["title"] for h in chunk["headers"])
        return {
            "text": '\n'.join(chunk["content"]).strip(),
            "header_path": header_path,
            "level": chunk["level"],
            "metadata": {
                "headers": [h["title"] for h in chunk["headers"]]
            }
        }


class HTMLChunker:
    """Chunk HTML documents by structure."""

    def __init__(self, max_chunk_size: int = 1000):
        self.max_chunk_size = max_chunk_size

    def chunk(self, html: str) -> List[Dict]:
        """Split HTML by structural elements."""
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, 'html.parser')
        chunks = []

        # Process by sections
        for section in soup.find_all(['section', 'article', 'div']):
            # Get section header if exists
            header = section.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            header_text = header.get_text() if header else ""

            # Get text content
            text = section.get_text(separator=' ', strip=True)

            if len(text.split()) <= self.max_chunk_size:
                chunks.append({
                    "text": text,
                    "header": header_text,
                    "tag": section.name
                })
            else:
                # Split large sections
                sub_chunks = self._split_text(text, header_text)
                chunks.extend(sub_chunks)

        return chunks

    def _split_text(self, text: str, header: str) -> List[Dict]:
        """Split large text sections."""
        words = text.split()
        chunks = []

        for i in range(0, len(words), self.max_chunk_size):
            chunk_words = words[i:i + self.max_chunk_size]
            chunks.append({
                "text": " ".join(chunk_words),
                "header": header,
                "part": i // self.max_chunk_size + 1
            })

        return chunks
```

### Code Chunking

```python
import re
from typing import List, Dict

class CodeChunker:
    """Chunk code files by functions/classes."""

    def __init__(
        self,
        max_chunk_size: int = 800,
        language: str = "python"
    ):
        self.max_chunk_size = max_chunk_size
        self.language = language

    def chunk(self, code: str) -> List[Dict]:
        """Split code by logical units."""
        if self.language == "python":
            return self._chunk_python(code)
        elif self.language in ["javascript", "typescript"]:
            return self._chunk_javascript(code)
        else:
            return self._chunk_generic(code)

    def _chunk_python(self, code: str) -> List[Dict]:
        """Chunk Python code by classes and functions."""
        import ast

        try:
            tree = ast.parse(code)
        except SyntaxError:
            return self._chunk_generic(code)

        chunks = []
        lines = code.split('\n')

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                start_line = node.lineno - 1
                end_line = node.end_lineno

                chunk_lines = lines[start_line:end_line]
                chunk_text = '\n'.join(chunk_lines)

                # Get docstring if exists
                docstring = ast.get_docstring(node) or ""

                chunks.append({
                    "text": chunk_text,
                    "type": "class" if isinstance(node, ast.ClassDef) else "function",
                    "name": node.name,
                    "docstring": docstring,
                    "start_line": start_line + 1,
                    "end_line": end_line
                })

        # Handle module-level code
        if not chunks:
            return self._chunk_generic(code)

        return chunks

    def _chunk_javascript(self, code: str) -> List[Dict]:
        """Chunk JavaScript/TypeScript code."""
        # Pattern for functions and classes
        patterns = [
            (r'((?:export\s+)?(?:async\s+)?function\s+\w+\s*\([^)]*\)\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})', 'function'),
            (r'((?:export\s+)?class\s+\w+[^{]*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})', 'class'),
            (r'(const\s+\w+\s*=\s*(?:async\s+)?\([^)]*\)\s*=>\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})', 'arrow_function'),
        ]

        chunks = []
        for pattern, chunk_type in patterns:
            for match in re.finditer(pattern, code, re.MULTILINE | re.DOTALL):
                chunk_text = match.group(1)
                if len(chunk_text.split()) <= self.max_chunk_size:
                    # Extract name
                    name_match = re.search(r'(?:function|class|const)\s+(\w+)', chunk_text)
                    name = name_match.group(1) if name_match else "anonymous"

                    chunks.append({
                        "text": chunk_text,
                        "type": chunk_type,
                        "name": name
                    })

        if not chunks:
            return self._chunk_generic(code)

        return chunks

    def _chunk_generic(self, code: str) -> List[Dict]:
        """Generic code chunking by lines."""
        lines = code.split('\n')
        chunks = []
        current_chunk = []
        current_size = 0

        for line in lines:
            line_words = len(line.split())

            if current_size + line_words <= self.max_chunk_size:
                current_chunk.append(line)
                current_size += line_words
            else:
                if current_chunk:
                    chunks.append({
                        "text": '\n'.join(current_chunk),
                        "type": "code_block",
                        "line_count": len(current_chunk)
                    })
                current_chunk = [line]
                current_size = line_words

        if current_chunk:
            chunks.append({
                "text": '\n'.join(current_chunk),
                "type": "code_block",
                "line_count": len(current_chunk)
            })

        return chunks
```

### Recursive Chunking (LangChain-style)

```python
from typing import List, Dict, Optional

class RecursiveChunker:
    """Recursively split text using multiple separators."""

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        separators: Optional[List[str]] = None
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", ". ", " ", ""]

    def chunk(self, text: str) -> List[Dict]:
        """Recursively split text."""
        return self._split_text(text, self.separators)

    def _split_text(
        self,
        text: str,
        separators: List[str]
    ) -> List[Dict]:
        """Split text recursively with separators."""
        final_chunks = []

        # Use first separator
        separator = separators[0]
        splits = text.split(separator) if separator else list(text)

        good_splits = []
        current_doc = []
        current_length = 0

        for split in splits:
            split_length = len(split)

            if current_length + split_length <= self.chunk_size:
                current_doc.append(split)
                current_length += split_length + len(separator)
            else:
                if current_doc:
                    doc = separator.join(current_doc)
                    if len(doc) > self.chunk_size and len(separators) > 1:
                        # Recursively split with next separator
                        final_chunks.extend(
                            self._split_text(doc, separators[1:])
                        )
                    else:
                        final_chunks.append({"text": doc})

                # Handle overlap
                overlap_docs = []
                overlap_length = 0
                for d in reversed(current_doc):
                    if overlap_length + len(d) <= self.chunk_overlap:
                        overlap_docs.insert(0, d)
                        overlap_length += len(d)
                    else:
                        break

                current_doc = overlap_docs + [split]
                current_length = sum(len(d) for d in current_doc) + len(separator) * (len(current_doc) - 1)

        # Last chunk
        if current_doc:
            doc = separator.join(current_doc)
            if len(doc) > self.chunk_size and len(separators) > 1:
                final_chunks.extend(self._split_text(doc, separators[1:]))
            else:
                final_chunks.append({"text": doc})

        return final_chunks
```

### Production Chunking Service

```python
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum
import logging

class ChunkingStrategy(Enum):
    FIXED = "fixed"
    SENTENCE = "sentence"
    PARAGRAPH = "paragraph"
    SEMANTIC = "semantic"
    RECURSIVE = "recursive"
    MARKDOWN = "markdown"
    CODE = "code"

@dataclass
class ChunkingConfig:
    strategy: ChunkingStrategy = ChunkingStrategy.RECURSIVE
    chunk_size: int = 500
    overlap: int = 50
    min_chunk_size: int = 100

class ChunkingService:
    """Production chunking service with multiple strategies."""

    def __init__(
        self,
        config: Optional[ChunkingConfig] = None,
        embedding_func: Optional[callable] = None
    ):
        self.config = config or ChunkingConfig()
        self.embedding_func = embedding_func
        self.logger = logging.getLogger(__name__)

    def chunk(
        self,
        text: str,
        strategy: Optional[ChunkingStrategy] = None,
        metadata: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """Chunk text using specified strategy."""
        strategy = strategy or self.config.strategy

        try:
            if strategy == ChunkingStrategy.FIXED:
                chunks = FixedSizeChunker(
                    self.config.chunk_size,
                    self.config.overlap
                ).chunk(text)
            elif strategy == ChunkingStrategy.SENTENCE:
                chunks = SentenceChunker(
                    self.config.chunk_size,
                    self.config.min_chunk_size
                ).chunk(text)
            elif strategy == ChunkingStrategy.SEMANTIC:
                if not self.embedding_func:
                    raise ValueError("Semantic chunking requires embedding function")
                chunks = SemanticChunker(
                    self.embedding_func,
                    max_chunk_size=self.config.chunk_size
                ).chunk(text)
            elif strategy == ChunkingStrategy.MARKDOWN:
                chunks = MarkdownChunker(
                    self.config.chunk_size
                ).chunk(text)
            else:
                chunks = RecursiveChunker(
                    self.config.chunk_size,
                    self.config.overlap
                ).chunk(text)

            # Add metadata to all chunks
            if metadata:
                for chunk in chunks:
                    chunk["metadata"] = {**metadata, **chunk.get("metadata", {})}

            self.logger.info(f"Created {len(chunks)} chunks using {strategy.value}")
            return chunks

        except Exception as e:
            self.logger.error(f"Chunking failed: {e}")
            # Fallback to simple splitting
            return self._fallback_chunk(text, metadata)

    def _fallback_chunk(self, text: str, metadata: Optional[Dict]) -> List[Dict]:
        """Simple fallback chunking."""
        words = text.split()
        chunks = []

        for i in range(0, len(words), self.config.chunk_size):
            chunk_words = words[i:i + self.config.chunk_size]
            chunks.append({
                "text": " ".join(chunk_words),
                "metadata": metadata or {}
            })

        return chunks
```

## Best Practices

1. **Match Strategy to Content**
   - Markdown docs: Use header-based
   - Code: Use AST-based
   - General text: Use recursive/sentence

2. **Size Selection**
   - Start with 500 tokens
   - Larger for technical/legal
   - Smaller for Q&A

3. **Overlap**
   - 10-20% overlap typically
   - More for highly contextual content
   - Less for independent sections

4. **Metadata Preservation**
   - Keep source document info
   - Preserve hierarchy (headers)
   - Track chunk position

5. **Testing**
   - Test with representative queries
   - Measure retrieval quality
   - Iterate on chunk size

## Common Pitfalls

1. **Splitting Mid-Sentence** - Losing meaning at boundaries
2. **No Overlap** - Context lost between chunks
3. **Ignoring Structure** - Missing document organization
4. **Same Size for All** - Different docs need different strategies
5. **Too Small** - Fragments without context
6. **Too Large** - Diluted relevance

## References

- [LangChain Text Splitters](https://python.langchain.com/docs/modules/data_connection/document_transformers/)
- [LlamaIndex Node Parsers](https://docs.llamaindex.ai/en/stable/module_guides/loading/node_parsers/)
- [Chunking Strategies Guide](https://www.pinecone.io/learn/chunking-strategies/)
