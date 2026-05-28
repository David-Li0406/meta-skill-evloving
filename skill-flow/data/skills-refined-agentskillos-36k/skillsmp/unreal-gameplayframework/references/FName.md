# FName GetOptions Filter

Use `UPARAM(meta = (GetOptions=...))` to provide a dynamic dropdown list for `FName` parameters. This behaves similarly to an enum picker, but values can be built at runtime.

使用 `UPARAM(meta = (GetOptions=...))` 为 `FName` 参数提供动态下拉列表，效果类似枚举选择，但支持运行时生成。

```cpp
UFUNCTION(BlueprintCallable)
void Bar(UPARAM(meta = (GetOptions = BarParams)) FName Param);

UFUNCTION()
static TArray<FName> BarParams();

// Example implementation / 示例实现
TArray<FName> Foo::BarParams()
{
	static const TArray<FName> Names =
	{
		FName(TEXT("Pawn")),
		FName(TEXT("Rigidbody"))
	};

	return Names;
}
```

You can use the same pattern on UPROPERTY as well.
同样可以用于 UPROPERTY：

```cpp
UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Demo", meta=(GetOptions=BarParams))
FName BarProperty;
```

Notes / 注意事项
- `BarParams` does not need to be `static`, but a static list avoids repeated allocation.
- `BarParams` 不必是静态函数，但静态列表可避免重复分配。
- The dropdown is populated dynamically each time the editor queries options.
- 编辑器会在需要时动态请求下拉选项。
