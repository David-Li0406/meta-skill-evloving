---
name: baml-integration
description: SagebaseでのBAML (Boundary ML) 統合に関する知識とベストプラクティス。BAML定義ファイルの作成、クライアント再生成、Factory Pattern実装、ハイブリッドアプローチの設計を支援します。
---

# BAML Integration

## Purpose
SagebaseにおけるBAML (Boundary ML) 統合の正しい知識と実装パターンを提供します。

## When to Activate
This skill activates automatically when:
- Creating or modifying `.baml` files in `baml_src/` directory
- Implementing BAML-based services
- Working with `baml_client/` generated code
- User mentions "BAML", "Boundary ML", or "structured output"
- Creating factory classes for BAML implementations

## BAML Overview

### What is BAML?
BAML (Boundary ML) は、LLMの構造化出力を型安全に扱うためのドメイン特化言語(DSL)です。

### Key Benefits
- **型安全性**: Pydanticモデルと完全に互換性のある型定義
- **トークン効率**: 最適化されたプロンプト生成により、従来のPydantic実装よりトークン使用量を5-15%削減
- **パース精度**: LLMの出力を確実に構造化データに変換
- **プロンプト一元管理**: `.baml`ファイルにプロンプトとスキーマを集約

## BAML File Structure

### Directory Layout
```
sagebase/
├── baml_src/                    # BAML定義ファイル（.baml）
│   ├── clients.baml            # LLMクライアント設定
│   ├── generators.baml         # コード生成設定
│   ├── minutes_divider.baml    # 議事録分割
│   └── politician_matching.baml # 政治家マッチング
└── baml_client/                 # 自動生成されたPythonコード
    ├── async_client.py         # 非同期クライアント
    ├── sync_client.py          # 同期クライアント
    └── types.py                # 型定義
```

### BAML File Components

#### 1. Class Definitions
```baml
// Pydanticモデルに対応する型定義
class SpeakerMatch {
    matched bool @description("マッチングが成功したか")
    speaker_id int? @description("マッチした発言者のID")
    speaker_name string? @description("マッチした発言者の名前")
    confidence float @description("マッチングの信頼度（0.0-1.0）")
    reason string @description("マッチング判定の理由")
}
```

**重要**:
- クラス名はPydanticモデル名と一致させる
- オプショナルフィールドは `?` を付ける
- `@description`で各フィールドの意味を明示

#### 2. Function Definitions
```baml
function MatchSpeaker(
    speaker_name: string,
    available_speakers: string
) -> SpeakerMatch {
    client Gemini2Flash              // 使用するLLMクライアント
    prompt #"
        あなたは議事録の発言者名マッチング専門家です。

        # 抽出された発言者名
        {{ speaker_name }}

        # 既存の発言者リスト
        {{ available_speakers }}

        # マッチング基準
        1. 完全一致を最優先
        2. 括弧内の名前との一致
        3. 信頼度は 0.8 以上の場合のみマッチ
    "#
}
```

**ベストプラクティス**:
- プロンプトは `#"..."#` で囲む（ヒアドキュメント）
- 変数は `{{ variable_name }}` で展開
- マッチング基準や出力要件を明確に記述

## BAML Client Generation

### Generating Client Code

**コマンド**:
```bash
uv run python -c "import sys; sys.argv = ['baml', 'generate', '--from', 'baml_src']; from baml_py import invoke_runtime_cli; invoke_runtime_cli()"
```

**いつ実行するか**:
- 新しい`.baml`ファイルを作成した後
- 既存の`.baml`ファイルを修正した後
- `baml_client/`のコードが古い場合

**確認方法**:
```bash
# 新しい関数が生成されたか確認
grep -n "MatchPolitician" baml_client/async_client.py

# 型チェックでエラーがないか確認
uv run --frozen pyright src/infrastructure/external/politician_matching/baml_politician_matching_service.py
```

### Generated Code Usage

```python
from baml_client.async_client import b

# BAML関数を呼び出し
baml_result = await b.MatchSpeaker(
    speaker_name="山田太郎",
    available_speakers="ID: 1, 名前: 山田太郎\nID: 2, 名前: 佐藤花子"
)

# 結果をPydanticモデルに変換
match_result = SpeakerMatch(
    matched=baml_result.matched,
    speaker_id=baml_result.speaker_id,
    speaker_name=baml_result.speaker_name,
    confidence=baml_result.confidence,
    reason=baml_result.reason,
)
```

## Implementation Patterns

### 1. Hybrid Approach (推奨パターン)

**コンセプト**: ルールベースマッチング（高速パス）+ BAML（複雑ケース）

```python
class BAMLSpeakerMatchingService:
    async def find_best_match(self, speaker_name: str) -> SpeakerMatch:
        # 1. 高速パス: ルールベースマッチング
        rule_based_match = self._rule_based_matching(speaker_name, available_speakers)
        if rule_based_match.matched and rule_based_match.confidence >= 0.9:
            return rule_based_match  # LLMをスキップ

        # 2. BAML: 複雑なケースのみ
        baml_result = await b.MatchSpeaker(
            speaker_name=speaker_name,
            available_speakers=self._format_speakers_for_llm(filtered_speakers)
        )

        return SpeakerMatch(**baml_result.__dict__)
```

**利点**:
- トークン使用量削減（完全一致は即座に判定）
- レイテンシ削減（LLM呼び出しを最小化）
- コスト削減

### 2. Service Implementation Structure

```python
class BAMLSpeakerMatchingService:
    def __init__(
        self,
        llm_service: ILLMService,  # 互換性のため保持（BAML使用時は不要）
        speaker_repository: SpeakerRepository,
    ):
        self.llm_service = llm_service
        self.speaker_repository = speaker_repository

    async def find_best_match(self, speaker_name: str) -> SpeakerMatch:
        # 実装
        pass

    def _rule_based_matching(self, speaker_name: str, available_speakers) -> SpeakerMatch:
        # ルールベースマッチング（高速パス）
        pass

    def _filter_candidates(self, speaker_name: str, available_speakers) -> list:
        # 候補絞り込み（トークン削減）
        pass

    def _format_speakers_for_llm(self, speakers: list) -> str:
        # LLM用フォーマット
        pass
```

## Testing BAML Services

### Mock BAML Client

```python
import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def mock_baml_client(monkeypatch):
    """BAML clientをモック化"""
    mock_b = MagicMock()
    mock_match_speaker = AsyncMock()
    mock_match_speaker.return_value = MagicMock(
        matched=True,
        speaker_id=1,
        speaker_name="山田太郎",
        confidence=0.95,
        reason="完全一致"
    )
    mock_b.MatchPolitician = mock_match_politician

    monkeypatch.setattr("baml_client.async_client.b", mock_b)
    return mock_b

@pytest.mark.asyncio
async def test_baml_politician_matching(mock_baml_client):
    """BAMLマッチングのテスト"""
    service = BAMLPoliticianMatchingService(mock_llm, mock_repo)
    result = await service.find_best_match("山田太郎")

    assert result.matched is True
    assert result.politician_id == 1
    mock_baml_client.MatchPolitician.assert_awaited_once()
```

## Token Optimization Tips

### 1. Candidate Filtering
```python
def _filter_candidates(self, speaker_name: str, available_speakers: list) -> list:
    """候補を絞り込んでトークン削減"""
    candidates = []
    for speaker in available_speakers:
        score = 0
        # 部分一致スコア
        if speaker["name"] in speaker_name:
            score += 3
        # 会議体所属ボーナス
        if speaker["id"] in affiliated_speaker_ids:
            score += 10

        if score > 0:
            candidates.append({**speaker, "score": score})

    # 上位10件のみLLMに渡す
    candidates.sort(key=lambda x: x["score"], reverse=True)
    return candidates[:10]  # トークン削減！
```

### 2. Compact Formatting
```python
def _format_speakers_for_llm(self, speakers: list) -> str:
    """簡潔なフォーマットでトークン削減"""
    formatted = []
    for speaker in speakers:
        # 必要最小限の情報のみ
        entry = f"ID: {speaker['id']}, 名前: {speaker['name']}"
        if speaker['id'] in affiliated_speaker_ids:
            entry += " ★"  # 短い記号で会議体所属を示す
        formatted.append(entry)
    return "\n".join(formatted)
```

### 3. Prompt Optimization
```baml
// ❌ 冗長なプロンプト
prompt #"
    あなたは議事録の発言者名マッチング専門家です。
    以下の詳細な手順に従って、慎重にマッチングを行ってください。
    ...（長い説明）
"#

// ✅ 簡潔なプロンプト
prompt #"
    発言者名と既存リストから最適マッチを見つけてください。

    # 基準
    1. 完全一致優先
    2. ★付きを優先
    3. 信頼度0.8以上のみマッチ
"#
```

## Common Pitfalls

### ❌ Don't: Forget to Regenerate Client
```python
# politician_matching.bamlを作成

# ❌ すぐに使おうとする
result = await b.MatchPolitician(...)  # AttributeError!
```

### ✅ Do: Regenerate After Changes
```bash
# 1. BAMLファイル作成/修正
# 2. クライアント再生成
uv run python -c "import sys; sys.argv = ['baml', 'generate', '--from', 'baml_src']; from baml_py import invoke_runtime_cli; invoke_runtime_cli()"
# 3. 使用
result = await b.MatchSpeaker(...)  # OK!
```

### ❌ Don't: Skip Type Conversion
```python
# ❌ BAML結果をそのまま返す
return baml_result  # 型が不明確
```

### ✅ Do: Convert to Pydantic Model
```python
# ✅ Pydanticモデルに変換
return SpeakerMatch(
    matched=baml_result.matched,
    speaker_id=baml_result.speaker_id,
    ...
)
```

## BAML-Only Features

### All LLM Features Now Use BAML

**Note:** Sagebaseの全てのLLM機能はBAML専用に移行完了しています。
Pydantic実装は削除されており、環境変数による切り替えはできません。

**BAML専用機能:**
- 議事録分割（Minutes Divider）
- 会議体メンバー抽出（Conference Member Extractor）
- 議員団メンバー抽出（Parliamentary Group Member Extractor）
- 政党メンバー抽出（Party Member Extractor）
- 話者マッチング（Speaker Matching）
- 政治家マッチング（Politician Matching）

## Debugging

### Check Generated Code
```bash
# 関数が生成されたか確認
grep -n "MatchSpeaker" baml_client/async_client.py

# 型定義を確認
cat baml_client/types.py | grep -A 10 "class SpeakerMatch"
```

### Type Check
```bash
# 型エラーを確認
uv run --frozen pyright src/infrastructure/external/politician_matching/baml_politician_matching_service.py
```

### Run Tests
```bash
# BAML実装のテストを実行
uv run pytest tests/infrastructure/external/politician_matching/test_baml_politician_matching_service.py -v
```

## Migration Checklist

新しいBAML実装を追加する際のチェックリスト:

- [ ] `baml_src/`に`.baml`ファイルを作成
  - [ ] クラス定義（Pydanticモデルと一致）
  - [ ] 関数定義（プロンプト含む）
- [ ] BAMLクライアント再生成
- [ ] BAML実装サービスを作成
  - [ ] ハイブリッドアプローチ（ルールベース + BAML）
  - [ ] 候補フィルタリング
  - [ ] トークン最適化
- [ ] テストを作成
  - [ ] BAMLクライアントをモック
  - [ ] ルールベースマッチングのテスト
  - [ ] BAML統合テスト
- [ ] `CLAUDE.md`を更新
  - [ ] BAML対応機能リストに追加
  - [ ] トークン削減効果を記載
- [ ] ドキュメント更新
  - [ ] 使い方を説明

## References

- [BAML Documentation](https://docs.boundaryml.com)
- [Sagebase CLAUDE.md - BAML Integration](../../CLAUDE.md#baml-integration)
- [BAML Client Generation Script](../../scripts/generate_baml_client.sh)

## Examples

実装例は以下のファイルを参照:
- `baml_src/politician_matching.baml` - 政治家マッチングBAML定義
- `src/infrastructure/external/politician_matching/baml_politician_matching_service.py` - BAML実装サービス
- `tests/infrastructure/external/politician_matching/test_baml_politician_matching_service.py` - テスト
