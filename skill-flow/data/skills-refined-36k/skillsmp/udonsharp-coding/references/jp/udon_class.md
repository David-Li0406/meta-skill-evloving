# クラス機能について

## 継承

UdonSharpは、`UdonSharpBehaviour`を継承している独自のクラスに対して、継承を行うことができます。
ただし、インターフェイスは使用できないため、純粋なC#程の自由度がありません。

```cs
public class UdonBaseClass : UdonSharpBehaviour
{
    public virtual void Hello()
    {
        Debug.Log("Hello UdonBase");
    }
}

public class UdonChildClass : UdonBaseClass
{
    public override void Hello()
    {
        Debug.Log("Hello UdonChild");
    }
}
```

一般的な使用方法としては、基底クラスの仮想メソッド（`virtual`/`override`）を利用して処理を差し替える、`Strategy Pattern`（を継承で代替した形）や、`Template Method Pattern`（共通処理は基底に置き、一部だけ派生で上書きする）としての運用です。
たとえば、内部の処理内容を差し替え可能にしたり、入力方式の違い（キーボード/VRコントローラ等）を「疑似インタフェース」として基底クラスにまとめ、派生クラスで実装を切り替える、といった用途で使います。

### 実装例

共通処理（移動）は基底クラスに置き、入力だけを派生クラスで差し替える例です（`Template Method Pattern` 寄り）。

```cs
using UdonSharp;
using UnityEngine;

public class BaseMover : UdonSharpBehaviour
{
    [SerializeField] private float speed = 2f;

    protected virtual Vector3 GetMoveDir() => Vector3.zero;

    private void Update()
    {
        transform.position += GetMoveDir() * (speed * Time.deltaTime);
    }
}

// キーボードでの入力方式
public class KeyboardMover : BaseMover
{
    protected override Vector3 GetMoveDir()
        => new Vector3(Input.GetAxisRaw("Horizontal"), 0f, Input.GetAxisRaw("Vertical"));
}

// VRでの入力方式
public class VrcMoveAxisMover : BaseMover
{
    private float x;
    private float z;

    public override void InputMoveHorizontal(float value, UdonInputEventArgs args) => x = value;
    public override void InputMoveVertical(float value, UdonInputEventArgs args) => z = value;
    protected override Vector3 GetMoveDir() => new Vector3(x, 0f, z);
}
```