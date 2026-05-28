# 最短実装（必須）

このページは「最小限の実装に必要な情報」だけをまとめています。

## 1. Owner の前提

- ネットワーク同期されるオブジェクトには `Owner` が存在します。
- 同期データの変更は **Owner のみ** 可能です。非 Owner は読み取り専用です。

## 2. Owner 関連の最小 API

- オーナー取得: `Networking.GetOwner(GameObject obj)`
- オーナー判定: `Networking.IsOwner(VRCPlayerApi player, GameObject obj)`
- オーナー設定: `Networking.SetOwner(VRCPlayerApi player, GameObject obj)`

## 3. 同期変数の定義

- 同期するフィールドに `[UdonSynced]` を付けます。
- 同期を行う場合は、`UdonBehaviourSyncMode` を **Manual** にして明示同期するのが基本です。

```cs
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class Example : UdonSharpBehaviour
{
    [UdonSynced]
    public bool synchronizedFlag;
}
```

## 4. 手動同期の流れ（最短）

- Owner が `RequestSerialization()` を呼ぶと同期が送信されます。
- 非 Owner 側は `OnDeserialization()` が呼ばれて同期値が反映されます。

```cs
public override void OnDeserialization()
{
    // 同期データ受信後の処理
}
```

## 5. 一時的イベントの同期

- 状態を継続させる必要がない一時イベントは `SendCustomNetworkEvent` を使います。
- public なメソッドに対してのみ呼び出し可能です。

```cs
public void PlayEffect()
{
    // エフェクト再生など
}

SendCustomNetworkEvent(NetworkEventTarget.All, nameof(PlayEffect));
```

## 6. 最小チェックリスト

- [ ] `Owner` のみが同期データを変更する設計になっている
- [ ] 同期変数に `[UdonSynced]` が付与されている
- [ ] `Manual` 同期で `RequestSerialization()` を呼んでいる
- [ ] 一時イベントは `SendCustomNetworkEvent` を使っている
