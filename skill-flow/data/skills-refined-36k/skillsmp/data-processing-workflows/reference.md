# Data Processing Workflows リファレンス

## 処理の詳細実装

### Minutes Divider の詳細

#### 使用技術
- **LangGraph**: 状態管理
- **Google Gemini API**: テキスト抽出とパース
- **pypdfium2**: PDF処理

#### 処理フロー
```python
# 簡略化された処理フロー
1. PDFファイル読み込み
2. テキスト抽出
3. LLMで発言ごとに分割
4. 話者名と発言内容を抽出
5. conversationsテーブルに保存
```

#### 実行コマンド
```bash
# ローカルPDFファイルから
docker compose -f docker/docker-compose.yml [-f docker/docker-compose.override.yml] exec sagebase uv run sagebase process-minutes --pdf-path /path/to/file.pdf

# GCSから（meeting IDを指定）
docker compose -f docker/docker-compose.yml [-f docker/docker-compose.override.yml] exec sagebase uv run sagebase process-minutes --meeting-id 123
```

#### 注意点
- LLM APIを使用するため、`GOOGLE_API_KEY` が必要
- 大きなPDFの場合、処理に時間がかかる
- GCSから取得する場合、事前にGCS認証が必要

### Speaker Extraction の詳細

#### 処理内容
```sql
-- conversationsから一意の話者を抽出
SELECT DISTINCT speaker_name
FROM conversations
WHERE speaker_name IS NOT NULL
  AND speaker_id IS NULL;

-- speakersテーブルに挿入
INSERT INTO speakers (name, ...)
VALUES (...);

-- conversationsを更新
UPDATE conversations
SET speaker_id = ...
WHERE speaker_name = ...;
```

#### 実行コマンド
```bash
docker compose -f docker/docker-compose.yml [-f docker/docker-compose.override.yml] exec sagebase uv run python src/extract_speakers_from_minutes.py
```

#### 注意点
- 同じ名前の異なる話者は区別されない（マッチングで解決）
- NULL speaker_nameは無視される

### Politician Matching の詳細

#### ハイブリッドアプローチ

##### 1. ルールベースマッチング
```python
# 完全一致
if normalize(speaker_name) == normalize(politician_name):
    return MATCH

# 部分一致
if speaker_name in politician_name or politician_name in speaker_name:
    return PARTIAL_MATCH
```

##### 2. LLMマッチング
```python
# LLMに名前のバリエーションを判断させる
prompt = f"""
以下の話者名と政治家名が同一人物か判断してください：
話者名: {speaker_name}
政治家名: {politician_name}
"""
# LLMが信頼度スコアを返す
confidence = llm.match(prompt)
```

#### 実行コマンド
```bash
docker compose -f docker/docker-compose.yml [-f docker/docker-compose.override.yml] exec sagebase uv run python update_speaker_links_llm.py
```

#### 注意点
- LLM APIを使用するため、コストが発生
- 信頼度の閾値は調整可能
- 完全自動ではなく、低信頼度マッチは手動確認推奨

### Web Scraper の詳細

#### 対応サイト
- **kaigiroku.net**: 多くの日本の地方議会で使用
- JavaScriptベースのサイトに対応（Playwright使用）

#### 実行コマンド
```bash
# GCSアップロードあり
docker compose -f docker/docker-compose.yml [-f docker/docker-compose.override.yml] exec sagebase uv run sagebase scrape-minutes \
  --council-id 123 \
  --upload-to-gcs

# ローカルのみ
docker compose -f docker/docker-compose.yml [-f docker/docker-compose.override.yml] exec sagebase uv run sagebase scrape-minutes \
  --council-id 123
```

#### GCS統合
```python
# GCSアップロード処理
1. Webサイトからスクレイピング
2. PDFまたはテキストをダウンロード
3. GCSにアップロード（gs://bucket/scraped/YYYY/MM/DD/...）
4. meetingsテーブルにURI保存（gcs_pdf_uri, gcs_text_uri）
```

#### 注意点
- Playwright依存関係がDockerイメージに含まれている必要あり
- GCS認証: `gcloud auth application-default login`
- URI形式は必ず `gs://` （HTTPSではない）

### Conference Member Extractor の詳細

#### ステージング戦略
```
extracted_conference_members（ステージングテーブル）
├── status: 'pending'     # 初期状態
├── status: 'matched'     # 自動マッチング成功
├── status: 'needs_review' # 手動確認必要
└── status: 'no_match'    # マッチング失敗
```

#### 信頼度スコア
```python
# LLMマッチングの信頼度
if confidence >= 0.7:
    status = 'matched'
elif confidence >= 0.5:
    status = 'needs_review'  # 手動レビュー推奨
else:
    status = 'no_match'
```

#### 実行コマンド
```bash
# ステップ1: 抽出
docker compose -f docker/docker-compose.yml [-f docker/docker-compose.override.yml] exec sagebase uv run sagebase extract-conference-members --conference-id 1

# ステップ2: マッチング
docker compose -f docker/docker-compose.yml [-f docker/docker-compose.override.yml] exec sagebase uv run sagebase match-conference-members --conference-id 1

# ステップ3: 所属作成
docker compose -f docker/docker-compose.yml [-f docker/docker-compose.override.yml] exec sagebase uv run sagebase create-affiliations --conference-id 1
```

#### 手動レビュー
```sql
-- needs_reviewのレコードを確認
SELECT * FROM extracted_conference_members
WHERE status = 'needs_review';

-- 手動でstatusを更新
UPDATE extracted_conference_members
SET status = 'matched', matched_politician_id = 123
WHERE id = 456;
```

## トラブルシューティング

### 問題1: Minutes Dividerが失敗する

**症状:**
- PDF処理エラー
- LLM APIエラー

**原因:**
- `GOOGLE_API_KEY` が設定されていない
- PDFファイルが破損している
- APIレート制限

**解決方法:**
```bash
# 環境変数確認
docker compose -f docker/docker-compose.yml [-f docker/docker-compose.override.yml] exec sagebase env | grep GOOGLE_API_KEY

# .envファイル確認
cat .env

# APIキーを設定
echo "GOOGLE_API_KEY=your-key-here" >> .env
docker compose -f docker/docker-compose.yml [-f docker/docker-compose.override.yml] restart
```

### 問題2: Politician Matchingの精度が低い

**症状:**
- 話者と政治家のマッチングが不正確

**原因:**
- 名前のバリエーションが多い
- 信頼度の閾値が不適切

**解決方法:**
```python
# 閾値調整（コード修正が必要）
CONFIDENCE_THRESHOLD = 0.7  # デフォルト
# → 0.8に上げる（厳密に）
# → 0.6に下げる（緩く）

# 手動確認を増やす
# needs_reviewステータスのレコードを確認
```

### 問題3: Web Scraperが動作しない

**症状:**
- Playwright関連エラー
- GCSアップロード失敗

**原因:**
- Playwright依存関係が不足
- GCS認証が未実施

**解決方法:**
```bash
# Playwright依存関係確認（Dockerイメージに含まれているはず）
docker compose -f docker/docker-compose.yml [-f docker/docker-compose.override.yml] exec sagebase playwright install

# GCS認証
gcloud auth application-default login

# 認証情報の確認
gcloud auth application-default print-access-token
```

### 問題4: 重複した政治家レコードが作成される

**症状:**
- 同じ政治家が複数回作成される

**原因:**
- 重複チェックロジックの不備
- 名前の正規化が不十分

**解決方法:**
```sql
-- 重複を手動確認
SELECT name, party_id, COUNT(*)
FROM politicians
GROUP BY name, party_id
HAVING COUNT(*) > 1;

-- 重複を削除（注意: IDが大きい方を削除）
DELETE FROM politicians
WHERE id IN (
  SELECT MAX(id)
  FROM politicians
  GROUP BY name, party_id
  HAVING COUNT(*) > 1
);
```

### 問題5: GCS URIがHTTPS形式になっている

**症状:**
- `https://storage.googleapis.com/...` 形式のURIが保存されている

**原因:**
- URI形式の誤り

**解決方法:**
```python
# 正しい形式
gcs_uri = "gs://bucket-name/path/to/file.pdf"

# 誤った形式
gcs_uri = "https://storage.googleapis.com/bucket-name/path/to/file.pdf"

# 変換が必要な場合
def convert_to_gs_uri(https_url):
    if https_url.startswith("https://storage.googleapis.com/"):
        return https_url.replace(
            "https://storage.googleapis.com/",
            "gs://"
        )
    return https_url
```

## パフォーマンス最適化

### LLM API呼び出しの削減

#### キャッシング
```python
# InstrumentedLLMService, CachedLLMService を使用
from src.infrastructure.external.cached_llm_service import CachedLLMService

llm_service = CachedLLMService(base_llm_service)
# 同じプロンプトへの呼び出しはキャッシュから返される
```

#### バッチ処理
```python
# 複数の話者をまとめて処理
speakers = get_unmatched_speakers()
for batch in chunk(speakers, size=10):
    process_batch(batch)
```

### データベースクエリの最適化

#### インデックス活用
```sql
-- 話者名での検索が頻繁な場合
CREATE INDEX idx_speakers_name ON speakers(name);

-- 政治家名での検索が頻繁な場合
CREATE INDEX idx_politicians_name ON politicians(name);
```

#### バルク挿入
```python
# 個別挿入ではなくバルク挿入
session.bulk_insert_mappings(Politician, politicians_data)
session.commit()
```

## ベストプラクティス

### 処理順序の厳守
- 議事録処理は必ず **Minutes Divider → Speaker Extraction → Politician Matching** の順
- Conference Member Extractionは **Extract → Match → Create** の順

### エラーハンドリング
- 各ステップでエラーが発生しても次のステップに進まない
- ログを確認して原因を特定

### データ整合性
- ステージングテーブルを活用して手動レビューを挟む
- 信頼度が低いマッチングは自動適用しない

### コスト管理
- LLM APIの呼び出し回数を監視
- キャッシングを積極的に活用
- 不要な再処理を避ける

## 参考資料

### プロジェクト内ドキュメント
- [ARCHITECTURE.md](../../../docs/ARCHITECTURE.md): システム全体のアーキテクチャ
- [Minutes Processing Flow](../../../docs/diagrams/data-flow-minutes-processing.mmd): 議事録処理フロー図

### コマンドリファレンス
- [sagebase-commands](../../sagebase-commands/): すべてのコマンドの詳細
