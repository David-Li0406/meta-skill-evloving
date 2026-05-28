# Handling Player Tracking Data

Various positional/pose information of a `VRCPlayerApi` can be obtained from `VRCPlayerApi`.

## Player position

```cs
VRCPlayerApi player = Networking.LocalPlayer;

Vector3 playerPosition = ownerPlayer.GetPosition();
Quaternion playerRotation = ownerPlayer.GetRotation();
```

## TrackingData

There are two ways to get the positions of a player's head and hands.

### `TrackingData`

```cs
VRCPlayerApi player = Networking.LocalPlayer;

// The player's actual head position
VRCPlayerApi.TrackingData headTrackingData = player.GetTrackingData(VRCPlayerApi.TrackingDataType.Head);
var headPos = headTrackingData.position;
var headRot = headTrackingData.rotation;
```

### `VRCPlayerApi.TrackingDataType`

| name | summary |
|---|---|
| Head | |
| LeftHand | |
| RightHand | |
| Origin | The player's playspace origin |
| AvatarRoot | The player's avatar root |

### `BonePosition` / `BoneRotation`

```cs
// Avatar bone position
var headBonePos = player.GetBonePosition(HumanBodyBones.Head);
var headBoneRot = player.GetBoneRotation(HumanBodyBones.Head);
```

The difference between these two is that `TrackingData` represents the player's *real* viewpoint position and hand controller position, while `Bone` represents the player's avatar bone position. These two positions can differ due to avatar IK processing, etc.

In general, for follow objects that matter to the user's view or actual hand positions, implement them using `TrackingData`.

Use bone position information when what matters is the position as seen by third parties, or when following the avatar is important (e.g., accessories).

Note: For the LocalPlayer, `TrackingData` indicates the actual viewpoint and controller positions. However, for players other than yourself (remote players), the same values as `GetBonePosition` and `GetBoneRotation` are used. In other words, remote players' tracking data is not transmitted.
