# Deferred Code Execution (ON_SCOPE_EXIT)

Unreal provides `ON_SCOPE_EXIT` to run code when the current scope ends, similar to Go's `defer`. It is useful for cleanup or logging that must always happen before leaving a function.

Unreal 提供 `ON_SCOPE_EXIT` 宏来在作用域结束时执行代码，类似 Go 的 `defer`，适合做清理或确保执行的收尾逻辑。

## Go example / Go 示例

```go
func main() {
	defer fmt.Println("world")
	fmt.Println("hello")
}
```

## Unreal example / Unreal 示例

```cpp
ON_SCOPE_EXIT
{
	UE_LOG(LogTemp, Log, TEXT("World"));
};

UE_LOG(LogTemp, Log, TEXT("Hello"));
```

Notes / 注意事项
- The scope-exit block runs after the surrounding scope finishes.
- 作用域结束时才会执行该代码块。
- Use it for cleanup or guaranteed logging when early returns are possible.
- 适用于清理逻辑或存在提前返回时的必执行逻辑。
