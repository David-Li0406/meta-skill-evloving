# 数据结构与集合

## 目录
- [数组 (TArray)](#数组-tarray)
- [映射 (TMap)](#映射-tmap)
- [结构体 (Struct)](#结构体-struct)
- [枚举 (Enum)](#枚举-enum)

## 数组 (TArray)

### 常用操作
```angelscript
// 创建数组
TArray<int> LocalIntArray;

// 添加元素
LocalIntArray.Add(2);
LocalIntArray.Add(8);
LocalIntArray.Add(255);

// 获取元素数量
int Count = LocalIntArray.Num();

// 检查包含元素
if (LocalIntArray.Contains(8))
{
    // 找到了
}

// 查找元素索引
int Index = LocalIntArray.FindIndex(255);  // 线性搜索

// 按索引移除
LocalIntArray.RemoveAt(Index);

// 按值移除（线性搜索）
LocalIntArray.Remove(8);

// 清空数组
LocalIntArray.Empty();
```

### 遍历数组
```angelscript
// 范围遍历
for (int Value : LocalIntArray)
{
    Log("Array contained " + Value);
}

// 索引遍历
for (int Index = 0, Count = LocalIntArray.Num(); Index < Count; ++Index)
{
    int Value = LocalIntArray[Index];
    Log("Array[" + Index + "] = " + Value);
}
```

### 完整示例
```angelscript
UFUNCTION()
void ExecuteExampleArray()
{
    TArray<int> LocalIntArray;

    LocalIntArray.Add(2);
    LocalIntArray.Add(8);
    LocalIntArray.Add(255);

    for (int Value : LocalIntArray)
    {
        Log("Array contained " + Value);
    }

    if (!LocalIntArray.Contains(8))
        Throw("Array did not contain 8.");

    int Index = LocalIntArray.FindIndex(255);
    if (Index != 2)
        Throw("Array did not contain 255 at index 2.");

    LocalIntArray.RemoveAt(Index);
    LocalIntArray.Remove(8);
    LocalIntArray.Empty();
}
```

## 映射 (TMap)

### 常用操作
```angelscript
// 创建映射
TMap<FString, int> LocalStringToIntMap;

// 添加键值对
LocalStringToIntMap.Add("TestString", 2);
LocalStringToIntMap.Add("Three", 3);

// 检查键存在
if (LocalStringToIntMap.Contains("TestString"))
{
    // 键存在
}

// 查找值（返回是否找到）
int FoundValue = -1;
if (LocalStringToIntMap.Find("Four", FoundValue))
{
    // 找到值
}

// 访问操作符（键不存在会抛异常）
if (LocalStringToIntMap.Contains("ChangeThis"))
{
    int& Value = LocalStringToIntMap["ChangeThis"];
    Value = 12;  // 修改值
}

// 查找或添加（返回引用）
int& Value = LocalStringToIntMap.FindOrAdd("Newb");  // 初始为默认值
Value = 9;

// 清空映射
LocalStringToIntMap.Empty();
```

### 遍历映射
```angelscript
for (auto Element : LocalStringToIntMap)
{
    Log("Map contained " + Element.Key + " => " + Element.Value);

    // 可以修改值（因为是引用）
    if (Element.Key == "ChangeThis")
        Element.Value = 27;
}
```

### 完整示例
```angelscript
UFUNCTION()
void ExecuteExampleMap()
{
    TMap<FString, int> LocalStringToIntMap;

    LocalStringToIntMap.Add("TestString", 2);
    LocalStringToIntMap.Add("Three", 3);
    LocalStringToIntMap.Add("Four", 4);
    LocalStringToIntMap.Add("ChangeThis", 5);

    if (!LocalStringToIntMap.Contains("TestString"))
        Throw("Map did not contain TestString.");

    int FoundValue = -1;
    if (!LocalStringToIntMap.Find("Four", FoundValue))
        Throw("Map did not contain Four.");

    if (FoundValue != 4)
        Throw("Map contained wrong value for Four.");

    if (LocalStringToIntMap.Contains("ChangeThis"))
    {
        int& Value = LocalStringToIntMap["ChangeThis"];
        check(Value == 5);
        LocalStringToIntMap["ChangeThis"] = 12;
        check(LocalStringToIntMap["ChangeThis"] == 12);
        check(Value == 12);
    }

    for (auto Element : LocalStringToIntMap)
    {
        Log("Map contained " + Element.Key + " => " + Element.Value);
    }

    int& Value = LocalStringToIntMap.FindOrAdd("Newb");
    check(Value == 0);
    Value = 9;
    check(LocalStringToIntMap["Newb"] == 9);

    LocalStringToIntMap.FindOrAdd("Noob") = 21;
    check(LocalStringToIntMap["Noob"] == 21);

    LocalStringToIntMap.Empty();
}
```

### 作为 UPROPERTY 使用
```angelscript
class AExampleMapActor : AActor
{
    UPROPERTY()
    TMap<AActor, FString> ActorMap;

    UFUNCTION()
    void PrintActorMap()
    {
        for (auto Element : ActorMap)
        {
            Log("Actor Map: " + Element.Key + " => " + Element.Value);
        }
    }
};
```

## 结构体 (Struct)

### 定义结构体
```angelscript
struct FExampleStruct
{
    // 暴露给蓝图
    UPROPERTY()
    float ExampleNumber = 4.0;

    UPROPERTY()
    FString ExampleString = "Example String";

    // 仅在脚本中使用
    float ExampleHiddenNumber = 3.0;
};
```

### 在类中使用结构体
```angelscript
class AExampleStructActor : AActor
{
    UPROPERTY()
    FExampleStruct ExampleStruct;

    UFUNCTION(BlueprintOverride)
    void BeginPlay()
    {
        Print(ExampleStruct.ExampleString + ", " + ExampleStruct.ExampleNumber);
    }

    // 使用 C++ 结构体
    UPROPERTY()
    FHitResult ExampleHitResult;
};
```

## 枚举 (Enum)

### 定义枚举
```angelscript
enum EExampleEnum
{
    A,
    B,
    C
};
```

### 使用枚举
```angelscript
UFUNCTION()
void TestExampleEnum(EExampleEnum Input)
{
    switch (Input)
    {
    case EExampleEnum::A:
        Print("You selected A!", Duration=30);
        break;
    case EExampleEnum::B:
        Print("You shouldn't select B.", Duration=30);
        break;
    case EExampleEnum::C:
        Print("What is this even?", Duration=30);
        break;
    }

    // 将整数转换为枚举
    EExampleEnum NumberAsEnum = EExampleEnum(0);
}
```

### 作为 UPROPERTY 使用
```angelscript
class AExampleEnumActor : AActor
{
    UPROPERTY()
    EExampleEnum ShowType = EExampleEnum::A;
};
```

## 注意事项
- `TArray.FindIndex()` 和 `TMap.Find()` 都是线性搜索，大数据量时注意性能
- `TMap[key]` 访问时如果键不存在会抛异常，建议先使用 `Contains()` 检查
- 修改 struct 属性需要完整重载，无法热重载
- 枚举值使用 `::` 访问（如 `EExampleEnum::A`）
- 遍历映射时，`Element.Key` 和 `Element.Value` 是引用，可以直接修改