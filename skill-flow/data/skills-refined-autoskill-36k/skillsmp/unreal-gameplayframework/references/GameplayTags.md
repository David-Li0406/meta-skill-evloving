# Gameplay Tag Filters

Use the `Categories` meta on `FGameplayTag` to filter the tag picker in the editor. This limits the dropdown to the specified root tag and its children.

使用 `Categories` 元数据可以限制 `FGameplayTag` 的下拉选项，仅显示指定根标签及其子标签。

```cpp
UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Demo", meta=(Categories="GameplayEvent"))
FGameplayTag ExampleTag;
```

The same filter works for function parameters.
函数参数同样支持此过滤：

```cpp
UFUNCTION(BlueprintCallable)
void Func(UPARAM(meta = (Categories="GameplayEvent")) FGameplayTag Tag);
```

Notes / 注意事项
- The tag picker only displays `GameplayEvent` and its child tags.
- 下拉列表只显示 `GameplayEvent` 及其子标签。
