# Algo Namespace

`Algo::` provides a collection of algorithms for containers, similar to `<algorithm>` in the C++ standard library.

`Algo::` 提供了一组容器算法，类似于 C++ 标准库的 `<algorithm>`。

## Common examples / 常见示例

```cpp
float* Highest = Algo::MaxElement(Floats);
```

```cpp
const Foo* HighestByX = Algo::MaxElementBy(FooArray, [](const Foo& F)
{
	return F.X;
});
```

```cpp
int32 Index = Algo::BinarySearch(Values, TargetValue);
```

```cpp
const float Sum = Algo::Accumulate(Values, 0.0f);
```

```cpp
Algo::Heapify(Values);
Algo::HeapSort(Values);
```

```cpp
Algo::RandomShuffle(Values);
Algo::Reverse(Values);
Algo::Rotate(Values, RotateOffset);
```

```cpp
const int32 LowerIndex = Algo::LowerBound(Values, TargetValue);
```

Notes / 注意事项
- Many algorithms return indices or pointers to elements; check for null/INDEX_NONE as needed.
- 很多算法返回索引或指针，使用前注意判空或 INDEX_NONE。
