# 参照：同期可能な型

同期変数として使用できる型の一覧です。

## Boolean

| Type | Size |
| --- | --- |
| bool | 1 byte |

## Integral numeric types

| Type | Range | Size |
| --- | --- | --- |
| sbyte | -128 to 127 | 1 byte |
| byte | 0 to 255 | 1 byte |
| short | -32,768 to 32,767 | 2 bytes |
| ushort | 0 to 65,535 | 2 bytes |
| int | -2,147,483,648 to 2,147,483,647 | 4 bytes |
| uint | 0 to 4,294,967,295 | 4 bytes |
| long | -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807 | 8 bytes |
| ulong | 0 to 18,446,744,073,709,551,615 | 8 bytes |

## Floating-point numeric types

| Type | Approximate range | Precision | Size |
| --- | --- | --- | --- |
| float | ±1.5 x 10^(−45) to ±3.4 x 10^(38) | ~6–9 digits | 4 bytes |
| double | ±5.0 × 10^(−324) to ±1.7 × 10^(308) | ~15–17 digits | 8 bytes |

## Vector / Quaternion（Unity）

| Type | Range | Size |
| --- | --- | --- |
| Vector2 | same as float | 8 bytes |
| Vector3 | same as float | 12 bytes |
| Vector4 | same as float | 16 bytes |
| Quaternion | same as float | 16 bytes |

## Color

| Type | Range / Precision | Size |
| --- | --- | --- |
| Color | same as float | 16 bytes |
| Color32 | same as byte | 4 bytes |

## Text

| Type | Range | Size |
| --- | --- | --- |
| char | U+0000 to U+FFFF | 2 bytes |
| string | same as char | 2 bytes / char |

## Other

| Type | Range | Size |
| --- | --- | --- |
| VRCUrl | U+0000 to U+FFFF | 2 bytes / char |

## 同期配列

- 一次元配列のみ有効です。
- ジャグ配列は同期しません。
- 要素数 0 でも **必ず new して初期化** してください。
