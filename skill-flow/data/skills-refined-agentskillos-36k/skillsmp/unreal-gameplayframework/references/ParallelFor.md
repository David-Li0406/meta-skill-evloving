# ParallelFor

`ParallelFor` can speed up expensive loops by distributing work across threads. It is suitable for heavy per-item computation where shared state is minimized.

`ParallelFor` 可以通过多线程分发任务来加速高开销循环，适用于每个元素计算成本较高且共享状态较少的场景。

## Sequential loop / 普通循环

```cpp
TArray<FVector> AllLocations;
TArray<FVector> ValidLocations;

for (const FVector& Location : AllLocations)
{
	// Process the location
	ValidLocations.Add(Location);
}
```

## ParallelFor / 并行循环

Use a thread-safe container (e.g., `TQueue`) to collect results.
使用线程安全容器（例如 `TQueue`）收集结果。

```cpp
TArray<FVector> AllLocations;
TQueue<FVector, EQueueMode::Mpsc> ValidLocations;

ParallelFor(AllLocations.Num(),
	[&ValidLocations, &AllLocations](int32 Index)
	{
		const FVector& Location = AllLocations[Index];
		// Process the location
		ValidLocations.Enqueue(Location);
	});
```

Notes / 注意事项
- Avoid non-thread-safe containers or shared mutable state.
- 避免使用非线程安全容器或共享可变状态。
- For cheap loops, the overhead can outweigh benefits.
- 对于轻量循环，多线程开销可能大于收益。
