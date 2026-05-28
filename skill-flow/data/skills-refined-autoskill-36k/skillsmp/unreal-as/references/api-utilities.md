# 工具类

## 目录
- [数学函数 (Math::)](#数学函数-math)
- [定时器 (System::)](#定时器-system)
- [格式化字符串](#格式化字符串)

## 数学函数 (Math::)

### 基础运算
```angelscript
// 绝对值
float AbsoluteValue = Math::Abs(-1.0);  // 1.0

// 最小值
float MinimumValue = Math::Min(0.1, 1.0);  // 0.1

// 最大值
float MaximumValue = Math::Max(0.1, 1.0);  // 1.0

// 限制范围
float ClampedValue = Math::Clamp(X = 2.0, Min = 0.0, Max = 0.5);  // 0.5
```

### 三角函数
```angelscript
// 正弦波（基于游戏时间）
float WaveValue = Math::Sin(System::GameTimeInSeconds * 2.0);
```

### 随机数
```angelscript
// 生成指定范围内的随机浮点数
float RandomValue = Math::RandRange(0.0, 10.0);
```

### 完整示例
```angelscript
void ExecuteExampleMath()
{
    float AbsoluteValue = Math::Abs(-1.0);
    check(AbsoluteValue == 1.0);

    float MinimumValue = Math::Min(0.1, 1.0);
    check(MinimumValue == 0.1);

    float MaximumValue = Math::Max(0.1, 1.0);
    check(MaximumValue == 1.0);

    float ClampedValue = Math::Clamp(X = 2.0, Min = 0.0, Max = 0.5);
    check(ClampedValue == 0.5);

    float WaveValue = Math::Sin(System::GameTimeInSeconds * 2.0);

    float RandomValue = Math::RandRange(0.0, 10.0);
}
```

## 定时器 (System::)

### 创建定时器
```angelscript
class AExampleTimerActor : AActor
{
    UFUNCTION(BlueprintOverride)
    void BeginPlay()
    {
        // 3秒后执行 FunctionCalledByTimer，不循环
        System::SetTimer(this, n"FunctionCalledByTimer", 3.0, bLooping = false);

        // 创建并返回定时器句柄
        FTimerHandle SecondTimer = System::SetTimer(this, n"FunctionCalledBySecondTimer",
                                                     3.0, bLooping = false);
    }
};
```

### 控制定时器
```angelscript
FTimerHandle Timer = System::SetTimer(this, n"MyFunction", 3.0, bLooping = false);

// 检查定时器是否暂停
if (System::IsTimerPausedHandle(Timer))
{
    // 暂停定时器
    System::PauseTimerHandle(Timer);
}
else
{
    // 恢复定时器
    System::UnPauseTimerHandle(Timer);
}

// 清除定时器（防止其激活）
System::ClearAndInvalidateTimerHandle(Timer);
```

### 定时器函数
```angelscript
// 定时器调用的函数必须是 UFUNCTION()
UFUNCTION()
void FunctionCalledByTimer()
{
    Print("Timer popped!");
}

UFUNCTION()
void FunctionCalledBySecondTimer()
{
    Print("Second timer popped!");
}
```

### 完整示例
```angelscript
class AExampleTimerActor : AActor
{
    UFUNCTION(BlueprintOverride)
    void BeginPlay()
    {
        System::SetTimer(this, n"FunctionCalledByTimer", 3.0, bLooping = false);

        FTimerHandle SecondTimer = System::SetTimer(this, n"FunctionCalledBySecondTimer",
                                                     3.0, bLooping = false);

        if (System::IsTimerPausedHandle(SecondTimer))
        {
            System::PauseTimerHandle(SecondTimer);
        }
        else
        {
            System::UnPauseTimerHandle(SecondTimer);
        }

        System::ClearAndInvalidateTimerHandle(SecondTimer);
    }

    UFUNCTION()
    void FunctionCalledByTimer()
    {
        Print("Timer popped!");
    }

    UFUNCTION()
    void FunctionCalledBySecondTimer()
    {
        Print("Second timer popped!");
    }
};
```

## 格式化字符串

### 基础语法
```angelscript
class AExampleFormatString : AActor
{
    UFUNCTION(BlueprintOverride)
    void Tick(float DeltaSeconds)
    {
        // 基础格式化
        Print(f"Called from actor {GetName()} at location {ActorLocation}");
    }
};
```

### 表达式标签
```angelscript
// 使用 = 打印表达式名称和值
Print(f"{DeltaSeconds =}");
// 输出: DeltaSeconds = 0.01
```

### 格式化选项
```angelscript
// 浮点数精度
Print(f"Three Decimals: {ActorLocation.Z :.3f}");  // 3位小数

// 整数格式化
Print(f"Extended to 10 digits: {400 :010d}");  // 0000000400

// 十六进制
Print(f"Hexadecimal: {20 :#x}");  // 0x14

// 二进制
Print(f"Binary: {1574 :b}");  // 11000100110
Print(f"Binary 32 Bits: {1574 :#032b}");  // 0b00000000000000000000011000100110
```

### 对齐
```angelscript
// 右对齐（40字符宽）
Print(f"Aligned: {GetName() :>40}");

// 左对齐（40字符宽，用下划线填充）
Print(f"Aligned: {GetName() :_<40}");
```

### 枚举格式化
```angelscript
// 默认打印完整调试信息
Print(f"{ESlateVisibility::Collapsed}");
// 输出: "ESlateVisibility::Collapsed (1)"

// 仅打印枚举值名称
Print(f"{ESlateVisibility::Collapsed :n}");
// 输出: "Collapsed"
```

### 组合使用
```angelscript
// 标签 + 格式化选项
Print(f"{DeltaSeconds =:.0f}");
// 输出: DeltaSeconds = 0
```

### 完整示例
```angelscript
class AExampleFormatString : AActor
{
    UFUNCTION(BlueprintOverride)
    void Tick(float DeltaSeconds)
    {
        Print(f"Called from actor {GetName()} at location {ActorLocation}");

        Print(f"{DeltaSeconds =}");

        Print(f"Three Decimals: {ActorLocation.Z :.3f}");
        Print(f"Extended to 10 digits with leading zeroes: {400 :010d}");
        Print(f"Hexadecimal: {20 :#x}");
        Print(f"Binary: {1574 :b}");
        Print(f"Binary 32 Bits: {1574 :#032b}");

        Print(f"Aligned: {GetName() :>40}");
        Print(f"Aligned: {GetName() :_<40}");

        Print(f"{DeltaSeconds =:.0f}");

        Print(f"{ESlateVisibility::Collapsed}");
        Print(f"{ESlateVisibility::Collapsed :n}");
    }
};
```

## 注意事项

### 数学函数
- `Math::` 命名空间包含常用的数学运算函数
- `Math::RandRange(min, max)` 包含边界值（[min, max]）
- `System::GameTimeInSeconds` 是游戏运行总时间（秒）

### 定时器
- 定时器绑定的函数必须标记为 `UFUNCTION()`
- 同一个函数只能有一个定时器，重复设置会覆盖之前的定时器
- `FTimerHandle` 用于控制定时器（暂停、恢复、取消）
- `System::ClearAndInvalidateTimerHandle()` 会清除定时器并失效句柄
- `bLooping = true` 表示循环执行，`false` 表示执行一次

### 格式化字符串
- 格式化字符串使用 `f"..."` 语法
- 表达式使用 `{}` 包裹
- `{expression =}` 打印表达式名称和值
- `{expression :format}` 使用格式化选项
- 常用格式化选项：
  - `:.Nf` - 浮点数精度（N位小数）
  - `:0Nd` - 整数补零到N位
  - `:#x` - 十六进制（带 0x 前缀）
  - `:b` - 二进制
  - `:#0Nb` - 二进制补零到N位（带 0b 前缀）
  - `:>N` - 右对齐到N字符
  - `:_<N` - 左对齐到N字符（用下划线填充）
  - `:n` - 枚举仅打印名称
- `System::GameTimeInSeconds` 可用于创建基于时间的周期性效果