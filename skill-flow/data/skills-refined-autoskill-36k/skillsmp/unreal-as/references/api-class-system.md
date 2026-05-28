# 类系统与修饰符

## 目录
- [常用类定义](#常用类定义)
- [属性修饰符 (UPROPERTY)](#属性修饰符-uproperty)
- [函数修饰符 (UFUNCTION)](#函数修饰符-ufunction)
- [访问修饰符 (access)](#访问修饰符-access)

## 常用类定义

### Actor 系统
- `AActor` - Actor 基类
- `ACharacter` - 角色类（支持角色移动和输入）

### 组件系统
- `UActorComponent` - 组件基类
- `USceneComponent` - 场景组件（支持位置、旋转、缩放）
- `UBillboardComponent` - 广告牌组件（编辑器可视化）
- `UStaticMeshComponent` - 静态网格组件
- `USplineComponent` - 样条组件
- `UInputComponent` - 输入组件

### 继承示例
```angelscript
// 创建自定义 Actor
class AExampleActorType : AActor
{
    // 属性和方法定义
};

// 创建自定义角色
class AExampleCharacter : ACharacter
{
    // 角色特定属性和方法
};
```

## 属性修饰符 (UPROPERTY)

### 基础可见性控制
```angelscript
UPROPERTY()
float UnrealFloatProperty;          // 默认可编辑

UPROPERTY(EditDefaultsOnly)
float EditableInDefaults;           // 仅在默认值中可编辑

UPROPERTY(BlueprintReadOnly)
bool bReadOnlyBool;                 // 蓝图可读取，不可设置

UPROPERTY(NotEditable)
bool bCoolBool;                     // 详情面板中不可编辑

UPROPERTY(EditConst)
bool bReallyCoolBool;               // 详情面板中可见但不可编辑
```

### 组件管理
```angelscript
// 自动创建为组件
UPROPERTY(DefaultComponent)
USceneComponent SceneComponent;

// 设置为根组件
UPROPERTY(DefaultComponent, RootComponent)
USceneComponent RootSceneComponent;

// 附加到指定组件
UPROPERTY(DefaultComponent, Attach = RootSceneComponent)
UBillboardComponent DinoComponent;

// 附加到指定 Socket
UPROPERTY(DefaultComponent, Attach = RootSceneComponent, AttachSocket = Face)
USceneComponent FaceAttachedComponent;

// 在 Actor 上显示组件属性
UPROPERTY(DefaultComponent, ShowOnActor, meta = (ShowOnlyInnerProperties))
USplineComponent SplineComponent;
```

### 分类与元数据
```angelscript
// 属性分类（使用 | 创建子分类）
UPROPERTY(Category = "Main Category|Sub Category")
float CategorizedFloat = 1337.0;

// 3D 编辑控件
UPROPERTY(meta = (MakeEditWidget))
FVector WidgetEditableVector;

// 条件显示（关联布尔值）
UPROPERTY(meta = (EditCondition = "bEditConditionBool"))
float ConditionalFloat;

UPROPERTY(meta = (InlineEditConditionToggle))
bool bEditConditionBool = true;

// 条件显示（关联枚举）
UPROPERTY()
EExampleEnum ShowType = EExampleEnum::A;

UPROPERTY(meta = (EditCondition="ShowType == EExampleEnum::A"))
float ShownOnA = 1.0;

UPROPERTY(meta = (EditCondition="ShowType == EExampleEnum::B", EditConditionHides))
float ShownOnB = 1.0;

// 数值范围限制
UPROPERTY(meta = (ClampMin = "0.0", ClampMax = "1.0", UIMin = "0.0", UIMax = "1.0"))
float ExampleClampedValue;
```

## 函数修饰符 (UFUNCTION)

### 基础声明
```angelscript
// 蓝图可调用的函数（非纯函数）
UFUNCTION()
void BlueprintVisibleFunction()
{
}

// 纯函数（无副作用，必须有返回值）
UFUNCTION(BlueprintPure)
bool BlueprintPureFunction()
{
    return true;
}

// 蓝图不可调用（但需要 UFUNCTION 用于委托/定时器等）
UFUNCTION(NotBlueprintCallable)
void ExampleNotCallable()
{
}
```

### 蓝图重写与事件
```angelscript
// 覆盖 C++ 函数（如 BeginPlay、Tick、ConstructionScript）
UFUNCTION(BlueprintOverride)
void Tick(float DeltaTime)
{
}

// 蓝图可重写的事件
UFUNCTION(BlueprintEvent)
void BlueprintEventFunction()
{
    Log("Blueprint did not override this event.");
}

// 编辑器中可调用的函数（仅编辑时运行）
UFUNCTION(CallInEditor)
void ExampleCallInEditorFunction()
{
}
```

### 分类与组合
```angelscript
// 函数分类
UFUNCTION(Category = "Really Cool Category")
void CategorizedFunction()
{
}

// 组合多个修饰符
UFUNCTION(BlueprintPure, BlueprintEvent, Category = "Hi Mum")
int ReallySpecifiedFunction()
{
    return 1337;
}
```

## 访问修饰符 (access)

### 基础访问控制
```angelscript
class UAccessSpecifierExample
{
    // 声明访问修饰符
    access Internal = private;

    // 等价于 private
    access:Internal
    float PrivateFloatValue = 0.0;

    // 允许特定类访问
    access InternalWithCapability = private, UAccessSpecifierComponent, APlayerController;

    access:InternalWithCapability
    float AccessibleFloatValue = 1.0;
};
```

### 访问修饰符选项
```angelscript
// 只读访问
access SpecifierCapabilityCanOnlyRead = private, UAccessSpecifierComponent (readonly);

// 继承给子类
access ReadableInAnySceneComponent = private, USceneComponent (inherited, readonly);

// 仅在默认值编辑
access EditAndReadOnly = private, * (editdefaults, readonly);

// 全局函数访问
access RestrictedToSpecificGlobalFunction = private, ExampleCallRestrictedFunction;
```

### 修饰符说明
- `private` / `protected` - 基础访问级别
- `readonly` - 只能读取，不能修改
- `editdefaults` - 仅能在 `default` 语句或 `ConstructionScript` 中编辑
- `inherited` - 继承给所有子类

## 注意事项
- 所有暴露给编辑器/蓝图的成员必须使用 `UPROPERTY()` 或 `UFUNCTION()` 标记
- `BlueprintPure` 函数必须有返回值，且不应有副作用
- `DefaultComponent` 必须配合 `RootComponent` 或 `Attach` 使用以确定组件层级
- 修改 struct 中的属性需要完整重载，无法热重载
- `BlueprintOverride` 仅可用于 C++ 中声明为 `BlueprintImplementEvent` 或 `BlueprintNativeEvent` 的函数