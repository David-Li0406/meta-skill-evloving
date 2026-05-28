# TInlineAllocator

`TInlineAllocator` lets you pre-allocate a small, fixed number of elements inline. If the owning container lives on the stack, those inline elements are also stored on the stack. When the element count exceeds the inline capacity, the container moves all elements to the heap.

`TInlineAllocator` 允许在容器内预分配固定数量的元素。如果容器本身在栈上，内联元素也会在栈上分配。当元素数量超过内联容量时，会将所有元素转移到堆上。

```cpp
TArray<AActor*, TInlineAllocator<8>> Actors;
```

Notes / 注意事项
- Inline storage is only stack-based when the container itself is stack-allocated.
- 只有当容器本身在栈上时，内联存储才会在栈上。
- Exceeding the inline capacity moves existing elements to heap storage.
- 超出内联容量后，现有元素会整体转移到堆存储。

Related allocators / 相关分配器
- `TInlineSetAllocator<>` for `TSet`
- `TInlineAllocator<>` for `TMap` value arrays (via allocator params)
