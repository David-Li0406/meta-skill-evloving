# UDONにおけるネットワークについて

Udonでは、`UdonBehavior`または`UdonSharpBehavior`がアタッチされたオブジェクトで、ネットワーク同期されるものに関しては`Owner`という概念が発生します。
VRChatではデータ同期されるオブジェクトに関して`Owner`と呼ばれるプレイヤーがそのオブジェクトのデータ同期の責任者となり、`Owner`がマスターデータを保持し、別の非`Owner`のプレイヤーのクライアントに対してデータを送信します。
同期されるデータは`Owner`となっているプレイヤーのみ変更可能です。非`Owner`のプレイヤーは同期されるデータに対しては読み込み専用になります。

## オーナーの取得関連の処理 

特定のゲームオブジェクトのオーナーがどのプレイヤーかを取得する場合は
`VRCPlayerAPI Networking.GetOwner(GameObject obj)`
を使用してオーナーのプレイヤー情報を得ます。また、現在のクライアントのプレイヤーがオーナーかどうかは`bool Networking.IsOwner(VRCPlayerApi player, GameObject obj)`関数を使用することで確認できます。

オーナー権限を特定のプレイヤーに移したい場合は`Networking.SetOwner(VRCPlayerApi player, GameObject obj)`を使用してオーナーを設定できます。

オーナー権限が他のプレイヤーに移ったとき、以下のイベントコールバック関数が発火します。

```cs
public void override OnOwnershipTransferred(VRCPlayerApi player)
{
    Debug.Log($"Ownership Transferred {player.displayName}");
}
```

また、`SetOwner`でオーナー変更されたとき、元のオーナーでは、オーナー権限変更リクエストに対して許可するか拒否するかのコールバックが発動します。 

```cs
public bool override OnOwnershipRequest(VRCPlayerApi requester, VRCPlayerApi newOwner)
{
    return true;
}
```

## 同期モード

同期モードとは、データ同期をどのように行うかを設定します。UdonSharpでは`UdonSharpBehavior`を継承したクラスに対して`UdonBehaviorSyncMode`アトリビュートを指定することで設定できます。

```cs
[UdonBehaviourSyncMode(BehaviourSyncMode.Manual)]
public class Example : UdonSharpBehaviour 
{ 
}
```

`UdonSharp.BehaviourSyncMode`

|Name|Summary|
|---|---|
|None|Enforces no synced variables on the behaviour and hides the selection dropdown in the UI for the sync mode. Nothing is synced and SendCustomNetworkEvent will not work on the behaviour.|
|Continuous|Synced variables will be updated automatically at a very frequent rate, but may not always reliably update to save bandwidth.|
|Manual|Synced variables are updated manually by the user less frequently, but ensures that updates are reliable when requested.|
|NoVariableSync|Enforces that there are no synced variables on the behaviour, hides the sync mode selection dropdown, and allows you to use the behaviours on GameObjects that use either Manual or Continuous sync.|

同期を行う場合はパフォーマンス上の理由からなるべく`Manual`を選択し、`Continuous`は連続して位置情報などの更新が必要かつ、補間機能を使用する場合を除いて使用を控えます。

## 同期変数 (Synced Variables)

同期変数はネットワーク同期において、`UdonBehavior`コンポーネントが持つ実際に同期されるパラメーターです。
UdonSharpでは`UdonSynced`アトリビュートを指定することで宣言できます。

```cs
[UdonSynced]
public bool synchronizedBoolean;

[UdonSynced(UdonSyncMode.Linear)]
public float synchronizedFloat;
```

UdonSyncModeで指定できるオプションは以下の通りです。

|Name|Summary|
|---|---|
|NotSynced||
|None|No interpolation (Default)|
|Linear|Lerp|
|Smooth|Some kind of smoothed syncing|

`Linear`と`Smooth`は同期モードが`Continuous`の場合しか作用しません。`Manual`モードの場合は基本的にNoneを指定します。

同期可能な型は以下になります

### Boolean  types
| Type | Size    |
| ---- | ------- |
| bool | 1 byte  |
### Integral numeric types
| Type   | Range                           | Size    |
|--------|---------------------------------|---------|
| sbyte  | -128 to 127                     | 1 byte  |
| byte   | 0 to 255                        | 1 byte  |
| short  | -32,768 to 32,767               | 2 bytes |
| ushort | 0 to 65,535                     | 2 bytes |
| int    | -2,147,483,648 to 2,147,483,647 | 4 bytes |
| uint   | 0 to 4,294,967,295              | 4 bytes |
| long   | -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807 | 8 bytes |
| ulong  | 0 to 18,446,744,073,709,551,615 | 8 bytes |
### Floating-point numeric types
| Type   | Approximate range             | Precision     | Size    |
|--------|-------------------------------|---------------|---------|
| float  | ±1.5 x 10^(−45) to ±3.4 x 10^(38)   | ~6-9 digits   | 4 bytes |
| double | ±5.0 × 10^(−324) to ±1.7 × 10^(308) | ~15-17 digits | 8 bytes |
### Vector mathematics types and structures (Unity)
| Type        | Range         | Size     |
|-------------|---------------|----------|
| Vector2   | same as float | 8 bytes  |
| Vector3   | same as float | 12 bytes  |
| Vector4   | same as float | 16 bytes |
| Quaternion| same as float | 16 bytes  |
### Color structures
| Type     | Range / Precision | Size    |
|----------|-------------------|---------|
| Color  | same as float     | 16 bytes |
| Color32| same as byte      | 4 bytes |
### Text types and structures
| Type   | Range            | Size           |
|--------|------------------|----------------|
| char   | U+0000 to U+FFFF | 2 bytes        |
| string | same as char     | 2 bytes / char |
### Other structures
| Type   | Range            | Size           |
|--------|------------------|----------------|
| VRCUrl | U+0000 to U+FFFF | 2 bytes / char |

### 同期配列

さらに上記の型の配列も同期変数とすることができます。
ただし一次元配列のみで有効でジャグ配列は同期しません。
また、初期化子で要素数0でもいいので必ずnewしないと同期がされません。


## 同期変数の手動同期

同期モードを`Manual`に指定している場合、明示的にオーナーが同期をリクエストしなければ同期されません。
またこの処理はオーナー以外が実行しても効果はありません。    

```cs
RequestSerialization();
```

同期がリクエストされるとオーナーでは以下のコールバックが順番に発動します

```cs
public override void OnPreSerialization()
{
    Debug.Log("データを転送前の処理");
}
```

```cs
public override void OnPostSerialization(VRC.Udon.Common.SerializationResult result)
{
    Debug.Log("データを転送後の後処理");
}
```

また、受信した非オーナー側は以下のコールバックが発動します
```cs
public override void OnDeserialization()
{
    Debug.Log("同期データを受信");
}
```
このコールバックを受信したとき同期変数の内容が送信されてきた内容に変化します。

## FieldChangeCallback

`OnDeserialization()`はそのクラスで定義したすべての同期変数の変更に対して発火します。
特定の同期変数の変更のみを取得したい場合は以下のような構文で可能です。

```cs
[UdonSynced, FieldChangeCallback(nameof(SyncedToggle))]
private bool _syncedToggle;

public bool SyncedToggle
{
    set
    {
        Debug.Log("toggling the object...");
        _syncedToggle = value;
        toggleObject.SetActive(value);
    }
    get => _syncedToggle;
}
```

これで`SyncedToggle`を変更されたときのコールバックを作ることができます。
このコールバックは`OnDeserialization()`と異なりオーナーでも呼ばれます。

注意点として、配列に対するFieldChangeCallbackでは、配列要素の変更ではコールバックは発火しません。配列オブジェクトそのものが変わるときのみ発火します。


## SendCustomNetworkEvent

`SendCustomNetworkEvent`は同期変数を用いず、特定のタイミングでネットワーク越しに関数を実行したいときに使用する機能です。
publicな関数に対してのみ適応することができます。


```cs

public Function()
{
    Debug.Log("Show All Player!");
}


SendCustomNetworkEvent(NetworkEventTarget.All, nameof(Function));


```
`NetworkEventTarget`はこの関数を実行する対象です。

|Name|Summary|
|---|---|
|All|All players in the instance|
|Owner|Owner of the game object|
|Others|自分以外のすべてのプレイヤー|
|Self|自分のみ|


この機能は、主に、音声やエフェクトをすべてのプレイヤーで鳴らしたいなどの同時かつ一時的なイベントに対して使用します。
逆に、この機能を用いて状態変化など、その後も継続する状態を変化させるのに使うには不適切です。状態変化を使用する場合は同期変数で実装します。

またNetworkCallableアトリビュートを指定することで引数を持たせることもできます。

```cs
void Start()
{
    SendCustomNetworkEvent(NetworkEventTarget.All, nameof(Greet), "hogehoge");
}

[NetworkCallable]
public void Greet(string name)
{
    Debug.Log(name + "さん、こんにちは！");
}

```

## ネットワーク処理の設計

### 可能な限り同期の頻度を減らします。

高頻度なデータ同期は最大データ転送量の制限に引っかかり、同期詰まりを起こします。
例えば同期されたタイマー処理では、残り時間の表示に残り秒数を常に同期するのではなく、タイマーが0になる時刻情報を同期して、ローカルで取得した現在時刻との差から表示させれば、同期自体は一回で済みます。

### SendCustomNetworkEventと同期変数の使い分け

使い分けとしては、主にワールドに後から入ってくるプレイヤーに対して同期する必要があるか、ないかで判断することができます。

例えば、同時タイミングで発火される音声やエフェクトなどの処理は、その再生後に後から入ってきたプレイヤーで再生される必要がありません。このような信号はSendCustomNetworkEventで送るのが良いです。

逆に現在のゲーム状態・ワールドのオブジェクト位置など、後から入ってきたプレイヤーにもそれまでの状態を再現する必要があるものに関しては同期変数を使用します。