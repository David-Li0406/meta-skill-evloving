# About Class Features

## Inheritance

UdonSharp allows you to use inheritance with your own classes derived from `UdonSharpBehaviour`.
However, because interfaces are not available, it is not as flexible as “pure” C#.

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

A common way to use this is to swap behavior via virtual methods (`virtual`/`override`), in a style close to the `Strategy Pattern` (implemented via inheritance) or the `Template Method Pattern` (put the shared flow in the base class and override only a part in derived classes).

For example, you can make internal logic replaceable, or unify differences in input methods (keyboard / VR controllers, etc.) as a “pseudo interface” in the base class and switch implementations by using derived classes.

### Implementation Example

This example keeps the shared logic (movement) in the base class and replaces only the input part in derived classes (closer to the `Template Method Pattern`).

```cs
using UdonSharp;
using UnityEngine;
using VRC.Udon.Common;

public class BaseMover : UdonSharpBehaviour
{
    [SerializeField] private float speed = 2f;

    protected virtual Vector3 GetMoveDir() => Vector3.zero;

    private void Update()
    {
        transform.position += GetMoveDir() * (speed * Time.deltaTime);
    }
}

// Keyboard input
public class KeyboardMover : BaseMover
{
    protected override Vector3 GetMoveDir()
        => new Vector3(Input.GetAxisRaw("Horizontal"), 0f, Input.GetAxisRaw("Vertical"));
}

// VR input (Udon Input Events)
public class VrcMoveAxisMover : BaseMover
{
    private float x;
    private float z;

    public override void InputMoveHorizontal(float value, UdonInputEventArgs args) => x = value;
    public override void InputMoveVertical(float value, UdonInputEventArgs args) => z = value;
    protected override Vector3 GetMoveDir() => new Vector3(x, 0f, z);
}
```
