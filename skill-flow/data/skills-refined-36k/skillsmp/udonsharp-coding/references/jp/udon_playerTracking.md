# プレイヤーのトラッキング情報の扱い

Playerの様々な位置姿勢情報は`VRCPlayerApi`から取得可能です。

## プレイヤーの位置情報

```cs
VRCPlayerApi player = Networking.LocalPlayer;

Vector3 playerPosition = ownerPlayer.GetPosition();
Quaternion playerRotation = ownerPlayer.GetRotation();
```

## TrackingData

プレイヤーの頭や手の位置を取得する方法は２つ存在します。

`TrackingData`
```cs
VRCPlayerApi player = Networking.LocalPlayer;

// プレイヤーの実際の頭の位置
VRCPlayerApi.TrackingData headTrackingData = player.GetTrackingData(VRCPlayerApi.TrackingDataType.Head);
var headPos = headTrackingData.position;
var headRot = headTrackingData.rotation;
```

`VRCPlayerApi.TrackingDataType`
|name|summary|
|---|---|
|Head||
|LeftHand||
|RightHand||
|Origin|The player's playspace origin|
|AvatarRoot|The player's avatar root|


`BonePosition` `BoneRotation`
```cs
// アバターのボーンの位置
var headBonePos = player.GetBonePosition(HumanBodyBones.Head);
var headBoneRot = player.GetBoneRotation(HumanBodyBones.Head);
```

この二つの違いは`TrackingData`はプレイヤーの実際の視点位置・ハンドコントローラーの位置を示すのに対して、`Bone`はプレイヤーのアバターのボーン位置を示します。この２つの位置はアバターのIK処理などによって異なる場合があります。

基本的にユーザーから見た視界や実際の手の位置に関わる追従オブジェクトなどは`TrackingData`を使用して実装します。
ボーンの位置情報は、第三者から見た場合の位置や、アバターに追従することが重要なもの（アクセサリーなど）を実装するときに使います。

ちなみに`TrackingData`はLocalPlayerに対しては実際の視点位置とハンドコントローラーの位置を示しますが、自分以外のプレイヤー（リモートプレイヤー）ではGetBonePositionやGetBoneRotationと同じ値が使われます。つまりリモートプレイヤーのトラッキング情報は送信されていません。

