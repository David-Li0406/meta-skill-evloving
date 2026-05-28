# 実装章（実践）

このページは、実装のために必要な設計判断とコールバックの使い方をまとめています。

## 1. 同期モードの選択

`UdonBehaviourSyncMode` で同期モードを指定します。

- `Manual`: 明示的に同期。**通常はこれを推奨**。
- `Continuous`: 位置補間など連続更新が必要な場合のみ。
- `None`: 同期変数が存在しない前提。
- `NoVariableSync`: 同期変数なし・SendCustomNetworkEvent のみ使用。

```cs
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class Example : UdonSharpBehaviour { }
```

## 2. 状態同期 vs 一時イベント

- **状態を保持する必要がある** → `UdonSynced` で同期変数を使う
- **一時的な演出/音/エフェクト** → `SendCustomNetworkEvent`

## 3. オーナー移譲とコールバック

オーナー変更時のイベントです。

```cs
public override void OnOwnershipTransferred(VRCPlayerApi player)
{
    // 所有者変更時の処理
}
```

```cs
public override bool OnOwnershipRequest(VRCPlayerApi requester, VRCPlayerApi newOwner)
{
    // 変更を許可するなら true
    return true;
}
```

## 4. シリアライズのフック

同期の送受信タイミングに介入できます。

```cs
public override void OnPreSerialization()
{
    // 送信前の処理
}

public override void OnPostSerialization(VRC.Udon.Common.SerializationResult result)
{
    // 送信後の処理
}

public override void OnDeserialization()
{
    // 受信後の処理
}
```

## 5. 典型的な実装フロー

1. 変更を行う前に `IsOwner` で判定
2. 変更するなら `SetOwner` で権限を取得（必要時）
3. 同期変数を更新
4. `RequestSerialization()` で同期送信
