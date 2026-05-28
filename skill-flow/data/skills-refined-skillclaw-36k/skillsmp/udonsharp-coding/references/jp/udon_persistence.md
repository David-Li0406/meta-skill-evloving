# Udon Persistence (永続化)

VRChatのPersistence（永続化）機能を使用すると、ワールド内のプレイヤーごとのデータを保存し、セッションを超えて保持することができます。これにより、ハイスコア、所持品、設定などを次回のワールド訪問時に持ち越すことが可能になります。

主な永続化の方法として、**PlayerData** と **PlayerObject** の2種類があります。

## PlayerData

**PlayerData** は、プレイヤーごとにキーと値のペア（Key-Value）でデータを保存するシンプルなデータベースです。

### 基本的な使い方

`VRC.SDK3.Persistence.PlayerData` クラスの静的メソッドを使用してデータの読み書きを行います。

**データの保存:**
`PlayerData.SetType(key, value)` を使用します。保存はローカルプレイヤーに対して行います。

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDK3.Persistence;
using VRC.SDKBase;

public class ScoreSaver : UdonSharpBehaviour
{
    public void SaveScore(int score)
    {
        // キー "playerScore" に整数値を保存
        PlayerData.SetInt("playerScore", score);
        Debug.Log("スコアを保存しました: " + score);
    }
}
```

**データの読み込み:**
`PlayerData.GetType(player, key)` を使用します。データの読み込みは、データがロードされたことを示す `OnPlayerRestored` イベントを待ってから行う必要があります。

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDK3.Persistence;
using VRC.SDKBase;

public class ScoreLoader : UdonSharpBehaviour
{
    private const string ScoreKey = "playerScore";

    // プレイヤーの永続データがロードされた後に呼ばれるイベント
    public override void OnPlayerRestored(VRCPlayerApi player)
    {
        if (player.isLocal)
        {
            if (PlayerData.HasKey(player, ScoreKey))
            {
                int loadedScore = PlayerData.GetInt(player, ScoreKey);
                Debug.Log($"ロードされたスコア: {loadedScore}");
            }
            else
            {
                Debug.Log("保存されたスコアはありません。");
            }
        }
    }
}
```

### 利用可能なデータ型
`Int`, `Float`, `String`, `Bool`, `Byte`, `Color`, `Vector2`, `Vector3`, `Vector4`, `Quaternion` など、主要な型がサポートされています。

## PlayerObject

**PlayerObject** は、プレイヤーが入室した際に自動的に生成されるGameObjectです。このオブジェクトについたUdonBehaviourの同期変数（Synced Variable）を永続化することができます。インベントリの中身など、複雑な構造を持つデータの保存に適しています。

### セットアップ手順

1. シーンにGameObjectを作成し、`VRCPlayerObject` コンポーネントをアタッチします。
2. そのGameObject（または子）に `UdonBehaviour` をアタッチし、同期変数（`[UdonSynced]`）を定義します。
3. 同期変数を永続化したい `UdonBehaviour` と同じGameObjectに、`VRCEnablePersistence` コンポーネントをアタッチします。
4. シーンのディスクリプタ（VRCSceneDescriptor）などで、このオブジェクトをPlayerObjectとして登録する必要がある場合があります（※現在のSDK仕様では自動的に処理される場合もありますが、ドキュメントを確認してください）。一般的には、作成したオブジェクトをプレハブ化し、シーンの管理コンポーネント等で指定します。

### データの読み込み確認

PlayerObjectの場合も、データが復元されたタイミングを知るために `OnPlayerRestored` イベントを使用します。

```csharp
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;

public class InventoryPersistence : UdonSharpBehaviour
{
    [UdonSynced]
    public int[] inventoryItemIds;

    public override void OnPlayerRestored(VRCPlayerApi player)
    {
        // このオブジェクトの所有者（対応するプレイヤー）のデータが復元された
        if (Networking.GetOwner(gameObject) == player)
        {
            Debug.Log("インベントリデータが復元されました。");
            // 復元された inventoryItemIds を使って処理を行う
        }
    }
}
```

### PlayerObjectの取得

特定のプレイヤーに紐付いたPlayerObjectを取得するには、`Networking.GetPlayerObjects(player)` を使用します。

```csharp
public void FindPlayerObject(VRCPlayerApi player)
{
    GameObject[] objects = Networking.GetPlayerObjects(player);
    foreach (var obj in objects)
    {
        // 特定のコンポーネントを探すなど
        var inventory = obj.GetComponent<InventoryPersistence>();
        if (inventory != null)
        {
            Debug.Log($"{player.displayName} のインベントリが見つかりました。");
        }
    }
}
```

## 注意点とベストプラクティス

1.  **OnPlayerRestored を待つ**: データの読み書きは必ず `OnPlayerRestored` イベントが発火した後に行うようにしてください。それより前にアクセスすると、古いデータや初期値を読み書きしてしまう可能性があります。
2.  **容量制限**: PlayerData、PlayerObjectともに、プレイヤー1人あたり **100KB** の制限があります。
3.  **キーの命名 (PlayerData)**: PlayerDataはワールド全体で共有されるキー空間を持ちます。他のギミックとキーが衝突しないように、プレフィックスを付けることを推奨します（例: `MySystem_Score`, `AuthorName_Setting_Volume`）。
4.  **保存のタイミング**: プレイヤーがワールドから退出する直前（`OnPlayerLeft`）ではデータを保存できません。データが変更されたタイミングで随時保存するか、定期的に保存するようにしてください。
5.  **PlayerObject vs PlayerData**: 
    *   **PlayerData**: 単純な数値や文字列設定（スコア、オプション設定など）に適しています。
    *   **PlayerObject**: 複雑な状態を持つオブジェクトや、同期が必要なデータ（装備中のアイテムなど）に適しています。PlayerObjectは個別に同期されるため、帯域幅の節約にもつながります。

## 参考リンク
*   [Persistence (VRChat Creators)](https://creators.vrchat.com/worlds/udon/persistence/)
*   [PlayerData](https://creators.vrchat.com/worlds/udon/persistence/player-data)
*   [PlayerObject](https://creators.vrchat.com/worlds/udon/persistence/player-object)
