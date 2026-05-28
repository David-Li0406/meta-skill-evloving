# 输入与控制

## 目录
- [输入绑定](#输入绑定)
- [角色控制](#角色控制)

## 输入绑定

### 动作绑定
```angelscript
class AExampleInputCharacter : ACharacter
{
    UPROPERTY(DefaultComponent)
    UInputComponent ScriptInputComponent;

    UFUNCTION(BlueprintOverride)
    void BeginPlay()
    {
        // 绑定动作（按下和释放）
        ScriptInputComponent.BindAction(n"Jump", EInputEvent::IE_Pressed,
            FInputActionHandlerDynamicSignature(this, n"OnJumpPressed"));

        ScriptInputComponent.BindAction(n"Jump", EInputEvent::IE_Released,
            FInputActionHandlerDynamicSignature(this, n"OnJumpReleased"));

        // 动作名称在项目输入设置或 DefaultInput.ini 中配置
    }
};
```

### 轴绑定
```angelscript
UFUNCTION(BlueprintOverride)
void BeginPlay()
{
    // 绑定轴输入
    ScriptInputComponent.BindAxis(n"MoveForward",
        FInputAxisHandlerDynamicSignature(this, n"OnMoveForwardAxisChanged"));

    ScriptInputComponent.BindAxis(n"MoveRight",
        FInputAxisHandlerDynamicSignature(this, n"OnMoveRightAxisChanged"));
}
```

### 按键绑定
```angelscript
UFUNCTION(BlueprintOverride)
void BeginPlay()
{
    // 绑定到具体按键（不消耗输入）
    ScriptInputComponent.BindKey(EKeys::LeftShift, EInputEvent::IE_Pressed,
        FInputActionHandlerDynamicSignature(this, n"OnShiftPressed"));

    // 绑定到任意键（不消耗输入）
    ScriptInputComponent.BindKey(EKeys::AnyKey, EInputEvent::IE_Pressed,
        FInputActionHandlerDynamicSignature(this, n"OnKeyPressed"));
}
```

### 输入事件类型
- `EInputEvent::IE_Pressed` - 按键按下
- `EInputEvent::IE_Released` - 按键释放
- `EInputEvent::IE_Repeat` - 按键重复（按住不放）

### 处理函数示例
```angelscript
// 动作处理函数
UFUNCTION()
void OnJumpPressed(FKey Key)
{
    Print("Jump was pressed!", Duration=5.0);
    Jump();
}

UFUNCTION()
void OnJumpReleased(FKey Key)
{
    Print("Jump was released!", Duration=5.0);
    StopJumping();
}

// 轴处理函数
UFUNCTION()
void OnMoveForwardAxisChanged(float32 AxisValue)
{
    Print("Move Forward Axis Value: " + AxisValue, Duration=0.0);
    AddMovementInput(ControlRotation.ForwardVector, AxisValue);
}

UFUNCTION()
void OnMoveRightAxisChanged(float32 AxisValue)
{
    Print("Move Right Axis Value: " + AxisValue, Duration=0.0);
    AddMovementInput(ControlRotation.RightVector, AxisValue);
}

// 按键处理函数
UFUNCTION()
void OnShiftPressed(FKey Key)
{
    Print("Shift key pressed!", Duration=5.0);
}

UFUNCTION()
void OnKeyPressed(FKey Key)
{
    Print("Key Pressed: " + Key.KeyName, Duration=5.0);
}
```

## 角色控制

### 基础移动
```angelscript
class AExampleInputCharacter : ACharacter
{
    // 在轴处理函数中调用 AddMovementInput
    UFUNCTION()
    void OnMoveForwardAxisChanged(float32 AxisValue)
    {
        // ControlRotation 是 ACharacter 的内置属性
        AddMovementInput(ControlRotation.ForwardVector, AxisValue);
    }

    UFUNCTION()
    void OnMoveRightAxisChanged(float32 AxisValue)
    {
        AddMovementInput(ControlRotation.RightVector, AxisValue);
    }
};
```

### 跳跃
```angelscript
UFUNCTION()
void OnJumpPressed(FKey Key)
{
    Jump();  // ACharacter 内置方法
}

UFUNCTION()
void OnJumpReleased(FKey Key)
{
    StopJumping();  // ACharacter 内置方法
}
```

### 完整示例
```angelscript
class AExampleInputCharacter : ACharacter
{
    UPROPERTY(DefaultComponent)
    UInputComponent ScriptInputComponent;

    UFUNCTION(BlueprintOverride)
    void BeginPlay()
    {
        // 动作绑定
        ScriptInputComponent.BindAction(n"Jump", EInputEvent::IE_Pressed,
            FInputActionHandlerDynamicSignature(this, n"OnJumpPressed"));
        ScriptInputComponent.BindAction(n"Jump", EInputEvent::IE_Released,
            FInputActionHandlerDynamicSignature(this, n"OnJumpReleased"));

        // 轴绑定
        ScriptInputComponent.BindAxis(n"MoveForward",
            FInputAxisHandlerDynamicSignature(this, n"OnMoveForwardAxisChanged"));
        ScriptInputComponent.BindAxis(n"MoveRight",
            FInputAxisHandlerDynamicSignature(this, n"OnMoveRightAxisChanged"));

        // 按键绑定
        ScriptInputComponent.BindKey(EKeys::LeftShift, EInputEvent::IE_Pressed,
            FInputActionHandlerDynamicSignature(this, n"OnShiftPressed"));
        ScriptInputComponent.BindKey(EKeys::AnyKey, EInputEvent::IE_Pressed,
            FInputActionHandlerDynamicSignature(this, n"OnKeyPressed"));
    }

    UFUNCTION()
    void OnJumpPressed(FKey Key)
    {
        Print("Jump was pressed!", Duration=5.0);
        Jump();
    }

    UFUNCTION()
    void OnJumpReleased(FKey Key)
    {
        Print("Jump was released!", Duration=5.0);
        StopJumping();
    }

    UFUNCTION()
    void OnMoveForwardAxisChanged(float32 AxisValue)
    {
        Print("Move Forward Axis Value: " + AxisValue, Duration=0.0);
        AddMovementInput(ControlRotation.ForwardVector, AxisValue);
    }

    UFUNCTION()
    void OnMoveRightAxisChanged(float32 AxisValue)
    {
        Print("Move Right Axis Value: " + AxisValue, Duration=0.0);
        AddMovementInput(ControlRotation.RightVector, AxisValue);
    }

    UFUNCTION()
    void OnShiftPressed(FKey Key)
    {
        Print("Shift key pressed!", Duration=5.0);
    }

    UFUNCTION()
    void OnKeyPressed(FKey Key)
    {
        Print("Key Pressed: " + Key.KeyName, Duration=5.0);
    }
};
```

## 注意事项
- 动作和轴绑定的输入名称需要在项目输入设置或 `DefaultInput.ini` 中预先配置
- `BindAction` 和 `BindAxis` 会消耗输入，覆盖蓝图中的 `InputAction` 和 `InputAxis` 节点
- `BindKey` 不消耗输入，可以与动作映射共存
- 处理函数必须标记为 `UFUNCTION()`
- `FInputActionHandlerDynamicSignature` 和 `FInputAxisHandlerDynamicSignature` 用于动态创建处理器
- `ControlRotation`、`Jump()`、`StopJumping()` 是 `ACharacter` 的内置成员
- `AddMovementInput(direction, value)` 的 value 范围通常是 [-1, 1]
- `n""` 前缀表示 FName 字面量（如 `n"Jump"`），编译时解析性能更好