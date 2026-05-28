# 補足：同期オプション / コールバック

このページは、実装の補助情報をまとめています。

## 1. UdonSyncMode（補間）

`UdonSyncMode` は主に `Continuous` で有効です。

- `None`: 補間なし（デフォルト）
- `Linear`: 線形補間（Lerp）
- `Smooth`: なめらか補間

```cs
[UdonSynced(UdonSyncMode.Linear)]
public float synchronizedFloat;
```

## 2. FieldChangeCallback

特定の同期変数の変更時のみ処理を走らせたい場合に使用します。

```cs
[UdonSynced, FieldChangeCallback(nameof(SyncedToggle))]
private bool _syncedToggle;

public bool SyncedToggle
{
    set
    {
        _syncedToggle = value;
        toggleObject.SetActive(value);
    }
    get => _syncedToggle;
}
```

### 注意点

- 配列の **要素変更** では発火しません。
- 配列オブジェクトそのものが変更された場合のみ発火します。
