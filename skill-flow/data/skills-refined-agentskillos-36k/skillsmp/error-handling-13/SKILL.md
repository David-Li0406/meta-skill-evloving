---
name: error-handling
description: Sagebaseのエラーハンドリング規約とベストプラクティス。例外階層の使い分け、エラーの伝播ルール、再試行可能なエラーの区別をカバー。エラーハンドリングを実装・修正する時にアクティベートします。
---

# Error Handling Guidelines（エラーハンドリング規約）

## 目的

Sagebaseプロジェクトにおけるエラーハンドリングの一貫性と品質を確保するためのガイドラインを提供します。例外階層の適切な使用、エラーの伝播ルール、再試行可能なエラーの区別を統一します。

## いつアクティベートするか

このスキルは以下の場合に自動的にアクティベートされます：

- `except Exception`を含むコードを書こうとする時
- 新しい例外クラスを定義する時
- エラーハンドリングロジックを実装する時
- LLM/BAML関連のエラー処理を実装する時
- 外部サービス呼び出しのエラー処理を実装する時

## クイックチェックリスト

### コード追加前
- [ ] **汎用`except Exception`を使用していない**（可能な限り具体的な例外をキャッチ）
- [ ] **適切な例外クラスを選択している**
- [ ] **エラーの原因情報が保持されている**（`from e`を使用）

### コード追加中
- [ ] **再試行可能なエラーが区別できる**
- [ ] **ログレベルが適切**（warning vs error）
- [ ] **呼び出し元への情報伝達が適切**

### エラー処理後
- [ ] **エラーチェーンが保持されている**
- [ ] **機密情報がログに含まれていない**
- [ ] **テストでエラーケースがカバーされている**

---

## 例外階層

### Domain層 (`src/domain/exceptions.py`)

```
PolibaseException（アプリケーション基底例外）
├── DomainException（ドメイン層基底）
│   ├── EntityNotFoundException
│   ├── BusinessRuleViolationException
│   ├── InvalidEntityStateException
│   ├── DuplicateEntityException
│   ├── InvalidDomainOperationException
│   ├── DataIntegrityException
│   ├── ExternalServiceException
│   ├── RepositoryError
│   ├── DataValidationException（NEW: 入力データ不正）
│   └── RetryableException（再試行可能な例外基底）
│       ├── RateLimitExceededException
│       └── TemporaryServiceException
```

### Infrastructure層 (`src/infrastructure/exceptions.py`)

```
InfrastructureException
├── DatabaseException
├── ConnectionException
├── ExternalServiceException
│   └── LLMServiceException
│       ├── APIKeyException
│       ├── ModelException
│       ├── TokenLimitException
│       └── ResponseParsingException
├── FileSystemException
├── StorageException
├── NetworkException
├── TimeoutException
├── RateLimitException
└── WebScrapingException
```

### Application層 (`src/application/exceptions.py`)

```
ApplicationException
├── UseCaseException
├── ValidationException
├── AuthorizationException
├── ResourceNotFoundException
├── WorkflowException
├── ConcurrencyException
├── ConfigurationException
├── DataProcessingException
└── ProcessingException
```

---

## 例外の使い分け

### 1. BamlValidationError

**用途**: LLMが構造化出力を返さなかった場合

```python
# ✅ 良い例：BamlValidationErrorを個別にキャッチ
try:
    baml_result = await b.MatchPolitician(...)
except BamlValidationError as e:
    # 許容される状況として扱う（マッチなし結果を返す）
    logger.warning(f"BAMLバリデーション失敗: {e}")
    return PoliticianMatch(matched=False, confidence=0.0, reason="...")
except Exception as e:
    # その他のエラーは再スロー
    raise ExternalServiceException(...) from e
```

### 2. ExternalServiceException

**用途**: 外部サービス操作が失敗した場合

```python
# ✅ 良い例
raise ExternalServiceException(
    service_name="BAML",
    operation="politician_matching",
    reason=f"政治家マッチング中にエラーが発生しました: {e}",
) from e
```

### 3. LLMServiceException

**用途**: LLM API呼び出しが失敗した場合

```python
# ✅ 良い例
raise LLMServiceException(
    operation="extract_speeches",
    reason=str(e),
    model=self.model_name,
) from e
```

### 4. ResponseParsingException

**用途**: LLMレスポンスのパースが失敗した場合

```python
# ✅ 良い例
try:
    result = json.loads(response_text)
except json.JSONDecodeError as json_err:
    raise ResponseParsingException(
        reason=f"JSONパースエラー: {json_err}",
        response_sample=response_text[:200],
    ) from json_err
```

### 5. RetryableException / RateLimitExceededException

**用途**: 再試行により成功する可能性があるエラー

```python
# ✅ 良い例
if response.status_code == 429:  # Rate limit
    raise RateLimitExceededException(
        service_name="Gemini API",
        retry_after=int(response.headers.get("Retry-After", 60)),
    )
```

---

## エラーハンドリングパターン

### パターン1: フォールバック値を返す

**使用場面**: エラーでも処理を続行できる場合

```python
# ✅ 良い例：BamlValidationErrorは許容、その他は例外スロー
try:
    result = await b.DetectBoundary(text)
    return MinutesBoundary(...)
except BamlValidationError as e:
    logger.warning(f"バリデーション失敗: {e}")
    return MinutesBoundary(boundary_found=False, ...)  # フォールバック
except Exception as e:
    logger.error(f"エラー: {e}", exc_info=True)
    raise ExternalServiceException(...) from e  # 再スロー
```

### パターン2: 例外をラップして再スロー

**使用場面**: 呼び出し元でエラー処理を行う場合

```python
# ✅ 良い例
try:
    return chain.invoke(inputs)
except Exception as e:
    logger.error(f"Chain invocation failed: {e}", exc_info=True)
    raise LLMServiceException(
        operation="chain_invoke",
        reason=str(e),
        model=self.model_name,
    ) from e  # 元の例外を保持
```

### パターン3: Result型（成功/失敗を含むオブジェクト）

**使用場面**: エラーでも処理結果を返したい場合

```python
# ✅ 良い例
try:
    result = json.loads(response_text)
    return LLMExtractResult(success=True, extracted_data=result, error=None, ...)
except json.JSONDecodeError as json_err:
    logger.warning(f"JSONパースエラー: {json_err}")
    return LLMExtractResult(
        success=False,
        extracted_data=[],
        error=f"JSONパースエラー: {json_err}",
        ...
    )
```

---

## アンチパターン

### 1. 汎用Exceptionで全てをキャッチ

```python
# ❌ 悪い例
try:
    result = await some_operation()
except Exception as e:
    logger.error(f"Error: {e}")
    return []  # エラー情報が失われる

# ✅ 良い例
try:
    result = await some_operation()
except SpecificError as e:
    logger.warning(f"Expected error: {e}")
    return []  # 許容されるエラー
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    raise ExternalServiceException(...) from e
```

### 2. エラーチェーンの破棄

```python
# ❌ 悪い例
except Exception as e:
    raise CustomException(str(e))  # 元の例外が失われる

# ✅ 良い例
except Exception as e:
    raise CustomException(str(e)) from e  # エラーチェーン保持
```

### 3. ログの重複

```python
# ❌ 悪い例
except Exception as e:
    logger.error(f"Error: {e}")
    raise CustomException(f"Error: {e}") from e  # 呼び出し元でもログ出力

# ✅ 良い例：例外をスローする場所でのみログ、または呼び出し元でのみログ
except Exception as e:
    # ここでログを出力するなら、呼び出し元では出力しない
    raise CustomException(str(e)) from e
```

### 4. エラー吸収（サイレント失敗）

```python
# ❌ 悪い例
except Exception:
    pass  # エラーが完全に無視される

# ✅ 良い例
except Exception as e:
    logger.warning(f"Non-critical error ignored: {e}")
    # 明示的にフォールバック処理を行う
```

---

## 再試行可能なエラーの判定

### 再試行すべきエラー

```python
from src.domain.exceptions import RetryableException, RateLimitExceededException

try:
    result = await external_service_call()
except RateLimitExceededException as e:
    # 再試行可能（retry_afterを参照）
    if e.retry_after:
        await asyncio.sleep(e.retry_after)
        # 再試行
except RetryableException as e:
    # 一般的な再試行可能エラー
    pass
```

### 再試行すべきでないエラー

- `DataValidationException`: 入力データが不正
- `AuthenticationError`: 認証情報が不正
- `ResponseParsingException`: LLMレスポンスが不正（再試行しても同じ結果になりやすい）

---

## テストでのエラーハンドリング

```python
import pytest
from src.domain.exceptions import ExternalServiceException

async def test_error_handling():
    """エラーハンドリングのテスト"""
    # 特定の例外がスローされることを検証
    with pytest.raises(ExternalServiceException) as exc_info:
        await service.process_with_error()

    # 例外の詳細を検証
    assert "BAML" in str(exc_info.value)
    assert exc_info.value.details["operation"] == "politician_matching"
```

---

## 関連スキル

- [logging-guidelines](../logging-guidelines/): ログ出力の規約
- [test-writer](../test-writer/): テスト作成ガイド
- [baml-integration](../baml-integration/): BAML統合ガイド

---

## まとめ

### 重要な原則

✅ **汎用`except Exception`は最後の手段**
✅ **エラーチェーンを保持（`from e`）**
✅ **再試行可能なエラーを区別**
✅ **適切なログレベルを選択**
✅ **フォールバック値を返す場合は明示的に**

**これらの原則に従うことで、一貫性があり、デバッグしやすいエラーハンドリングを実現できます。**
