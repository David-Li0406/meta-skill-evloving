# RAG（Retrieval-Augmented Generation）設計

## 目次
- RAGアーキテクチャ
- ドキュメント処理
- 埋め込みモデル
- ベクトルDB選定
- 検索最適化
- ハイブリッド検索

## RAGアーキテクチャ

### 基本フロー

```
[クエリ] → [埋め込み] → [ベクトル検索] → [リランキング] → [コンテキスト構築] → [LLM生成] → [回答]
```

### 実装例

```python
from anthropic import Anthropic
import chromadb
from sentence_transformers import SentenceTransformer

class RAGPipeline:
    def __init__(self):
        self.client = Anthropic()
        self.embedder = SentenceTransformer("intfloat/multilingual-e5-large")
        self.chroma = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.chroma.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_documents(self, docs: list[dict]):
        """ドキュメントをインデックスに追加"""
        texts = [d["content"] for d in docs]
        embeddings = self.embedder.encode(texts, normalize_embeddings=True)
        
        self.collection.add(
            ids=[d["id"] for d in docs],
            embeddings=embeddings.tolist(),
            documents=texts,
            metadatas=[d.get("metadata", {}) for d in docs]
        )
    
    def query(self, question: str, k: int = 5) -> str:
        """質問に回答"""
        # 検索
        query_embedding = self.embedder.encode(
            [f"query: {question}"],
            normalize_embeddings=True
        )
        results = self.collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=k
        )
        
        # コンテキスト構築
        context = "\n\n---\n\n".join(results["documents"][0])
        
        # LLM生成
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system="""与えられたコンテキストに基づいて質問に回答してください。
コンテキストに情報がない場合は「情報が見つかりませんでした」と回答してください。
回答には必ず参照元を明記してください。""",
            messages=[
                {
                    "role": "user",
                    "content": f"コンテキスト:\n{context}\n\n質問: {question}"
                }
            ]
        )
        
        return response.content[0].text
```

## ドキュメント処理

### チャンキング戦略

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_document(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    """再帰的にチャンク分割"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", "。", ".", " ", ""]
    )
    return splitter.split_text(text)
```

### セマンティックチャンキング

```python
from sentence_transformers import SentenceTransformer
import numpy as np

def semantic_chunking(sentences: list[str], threshold: float = 0.5) -> list[list[str]]:
    """意味的な類似度に基づいてチャンク分割"""
    embedder = SentenceTransformer("intfloat/multilingual-e5-large")
    embeddings = embedder.encode(sentences, normalize_embeddings=True)
    
    chunks = []
    current_chunk = [sentences[0]]
    
    for i in range(1, len(sentences)):
        similarity = np.dot(embeddings[i-1], embeddings[i])
        
        if similarity < threshold:
            chunks.append(current_chunk)
            current_chunk = [sentences[i]]
        else:
            current_chunk.append(sentences[i])
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks
```

### メタデータ抽出

```python
def extract_metadata(doc_path: str) -> dict:
    """ドキュメントからメタデータを抽出"""
    from pathlib import Path
    import datetime
    
    path = Path(doc_path)
    stat = path.stat()
    
    return {
        "filename": path.name,
        "extension": path.suffix,
        "size_bytes": stat.st_size,
        "modified_at": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "directory": str(path.parent)
    }
```

## 埋め込みモデル選定

| モデル | 次元数 | 日本語 | 速度 | 用途 |
|--------|--------|--------|------|------|
| text-embedding-3-small | 1536 | ○ | 速 | 汎用 |
| text-embedding-3-large | 3072 | ○ | 中 | 高精度 |
| multilingual-e5-large | 1024 | ◎ | 中 | 多言語 |
| bge-m3 | 1024 | ◎ | 中 | 多言語・高精度 |

### Voyage AI（Claude推奨）

```python
import voyageai

vo = voyageai.Client()

# ドキュメント埋め込み
doc_embeddings = vo.embed(
    texts=documents,
    model="voyage-3",
    input_type="document"
).embeddings

# クエリ埋め込み
query_embedding = vo.embed(
    texts=[query],
    model="voyage-3",
    input_type="query"
).embeddings[0]
```

## ベクトルDB選定

| DB | 特徴 | スケール | 用途 |
|----|------|----------|------|
| ChromaDB | シンプル、ローカル | 小〜中 | プロトタイプ |
| Pinecone | マネージド、高速 | 大 | 本番 |
| Qdrant | 高機能、フィルタ | 中〜大 | 本番 |
| pgvector | PostgreSQL拡張 | 中 | 既存DB活用 |
| Milvus | 分散、高スケール | 大 | エンタープライズ |

### Qdrant例

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

client = QdrantClient(host="localhost", port=6333)

# コレクション作成
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
)

# データ追加
client.upsert(
    collection_name="documents",
    points=[
        PointStruct(
            id=i,
            vector=embedding,
            payload={"text": text, "source": source}
        )
        for i, (embedding, text, source) in enumerate(data)
    ]
)

# 検索
results = client.search(
    collection_name="documents",
    query_vector=query_embedding,
    limit=5,
    query_filter={
        "must": [{"key": "source", "match": {"value": "manual"}}]
    }
)
```

## 検索最適化

### クエリ拡張

```python
def expand_query(query: str) -> list[str]:
    """クエリを複数の視点に拡張"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": f"""以下の質問を、異なる言い回しで3つ生成してください。
各質問は1行で出力してください。

元の質問: {query}"""
        }]
    )
    
    expanded = response.content[0].text.strip().split("\n")
    return [query] + expanded[:3]
```

### リランキング

```python
def rerank(query: str, documents: list[str], top_k: int = 3) -> list[str]:
    """Cohereでリランキング"""
    import cohere
    
    co = cohere.Client()
    results = co.rerank(
        query=query,
        documents=documents,
        model="rerank-multilingual-v3.0",
        top_n=top_k
    )
    
    return [documents[r.index] for r in results.results]
```

## ハイブリッド検索

```python
def hybrid_search(
    query: str,
    collection,
    embedder,
    alpha: float = 0.5  # ベクトル検索の重み
) -> list[dict]:
    """ベクトル検索 + キーワード検索のハイブリッド"""
    # ベクトル検索
    query_embedding = embedder.encode([query], normalize_embeddings=True)
    vector_results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=10
    )
    
    # キーワード検索（BM25）
    from rank_bm25 import BM25Okapi
    
    all_docs = collection.get()["documents"]
    tokenized = [doc.split() for doc in all_docs]
    bm25 = BM25Okapi(tokenized)
    keyword_scores = bm25.get_scores(query.split())
    
    # スコア統合
    combined_scores = {}
    for i, doc_id in enumerate(vector_results["ids"][0]):
        combined_scores[doc_id] = alpha * (1 - vector_results["distances"][0][i])
    
    for i, score in enumerate(keyword_scores):
        doc_id = all_docs[i]
        if doc_id in combined_scores:
            combined_scores[doc_id] += (1 - alpha) * score
        else:
            combined_scores[doc_id] = (1 - alpha) * score
    
    # ソートして返却
    sorted_docs = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_docs[:5]
```
