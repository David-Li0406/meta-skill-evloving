# Level 4: Complex Algorithms Examples

Advanced algorithms, data structures, and performance-critical code using `gpt-5.2` model (auto-selected). Parallel execution with task decomposition.

---

## Example 1: Skip List Implementation

Probabilistic data structure with O(log n) operations for insert, delete, and search.

### Command

```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: skiplist
backend: codex
workdir: /home/user/algorithms
model: gpt-5.2
timeout: 180
---CONTENT---
实现跳表（Skip List）数据结构：
1. 支持插入、删除、搜索、范围查询
2. O(log n)平均时间复杂度
3. 包含完整注释和时间复杂度分析
4. 实现迭代器支持
---END---
EOF
```

### Expected Output

```
▶ skiplist (codex/gpt-5.2)

```python
import random
from typing import Optional, Iterator, Tuple

class SkipListNode:
    """跳表节点"""
    def __init__(self, key, value, level):
        self.key = key
        self.value = value
        self.forward = [None] * (level + 1)  # 前向指针数组

class SkipList:
    """
    跳表实现（概率平衡数据结构）

    时间复杂度：
    - 搜索: O(log n)
    - 插入: O(log n)
    - 删除: O(log n)
    - 范围查询: O(log n + k) where k is range size

    空间复杂度: O(n)
    """

    def __init__(self, max_level: int = 16, p: float = 0.5):
        self.max_level = max_level
        self.p = p  # 晋升概率
        self.header = SkipListNode(None, None, max_level)
        self.level = 0  # 当前最大层级

    def _random_level(self) -> int:
        """随机生成节点层级（几何分布）"""
        level = 0
        while random.random() < self.p and level < self.max_level:
            level += 1
        return level

    def search(self, key) -> Optional:
        """搜索键值 - O(log n)"""
        current = self.header

        # 从最高层开始向下搜索
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]

        # 移动到最底层的下一个节点
        current = current.forward[0]

        if current and current.key == key:
            return current.value
        return None

    def insert(self, key, value):
        """插入键值对 - O(log n)"""
        update = [None] * (self.max_level + 1)
        current = self.header

        # 找到每层的插入位置
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        # 如果键已存在，更新值
        current = current.forward[0]
        if current and current.key == key:
            current.value = value
            return

        # 生成新节点层级
        new_level = self._random_level()

        # 如果新层级超过当前最大层级，更新header
        if new_level > self.level:
            for i in range(self.level + 1, new_level + 1):
                update[i] = self.header
            self.level = new_level

        # 创建新节点并插入
        new_node = SkipListNode(key, value, new_level)
        for i in range(new_level + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

    def delete(self, key) -> bool:
        """删除键 - O(log n)"""
        update = [None] * (self.max_level + 1)
        current = self.header

        # 找到每层的删除位置
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        if not current or current.key != key:
            return False  # 键不存在

        # 删除节点（更新每层的指针）
        for i in range(self.level + 1):
            if update[i].forward[i] != current:
                break
            update[i].forward[i] = current.forward[i]

        # 降低层级（如果顶层为空）
        while self.level > 0 and not self.header.forward[self.level]:
            self.level -= 1

        return True

    def range_query(self, start_key, end_key) -> Iterator[Tuple]:
        """范围查询 - O(log n + k)"""
        current = self.header

        # 找到起始位置
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < start_key:
                current = current.forward[i]

        current = current.forward[0]

        # 遍历范围内的节点
        while current and current.key <= end_key:
            yield (current.key, current.value)
            current = current.forward[0]

    def __iter__(self) -> Iterator[Tuple]:
        """迭代器：按顺序遍历所有键值对"""
        current = self.header.forward[0]
        while current:
            yield (current.key, current.value)
            current = current.forward[0]

    def __len__(self) -> int:
        """计算元素数量 - O(n)"""
        count = 0
        current = self.header.forward[0]
        while current:
            count += 1
            current = current.forward[0]
        return count

    def display(self):
        """可视化跳表结构（调试用）"""
        for level in range(self.level, -1, -1):
            print(f"Level {level}: ", end="")
            node = self.header.forward[level]
            while node:
                print(f"{node.key}:{node.value} ", end="")
                node = node.forward[level]
            print()
```

» 写入 skiplist.py
» 写入 test_skiplist.py
✓ skiplist 24.3s
```

### Usage

```python
from skiplist import SkipList

# 创建跳表
sl = SkipList()

# 插入数据
sl.insert(3, "three")
sl.insert(1, "one")
sl.insert(5, "five")
sl.insert(2, "two")

# 搜索
print(sl.search(3))  # "three"

# 范围查询
for key, value in sl.range_query(2, 5):
    print(f"{key}: {value}")

# 删除
sl.delete(3)

# 迭代
for key, value in sl:
    print(f"{key}: {value}")
```

---

## Example 2: Pathfinding Algorithms

Implement Dijkstra and A* algorithms for graph pathfinding with dynamic weights.

### Command

```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: pathfinding
backend: codex
workdir: /home/user/algorithms
model: gpt-5.2
timeout: 180
---CONTENT---
实现图寻路算法：
1. Dijkstra算法（最短路径）
2. A*算法（启发式搜索）
3. 支持动态权重和障碍物
4. 包含路径重建和可视化
---END---
EOF
```

### Expected Output

```
▶ pathfinding (codex/gpt-5.2)

```python
import heapq
from typing import List, Tuple, Set, Dict, Callable, Optional

class Graph:
    """图数据结构"""
    def __init__(self):
        self.edges = {}  # {node: [(neighbor, weight), ...]}

    def add_edge(self, from_node, to_node, weight: float):
        if from_node not in self.edges:
            self.edges[from_node] = []
        self.edges[from_node].append((to_node, weight))

    def neighbors(self, node):
        return self.edges.get(node, [])

def dijkstra(graph: Graph, start, goal) -> Tuple[List, float]:
    """
    Dijkstra最短路径算法

    时间复杂度: O((V + E) log V)
    空间复杂度: O(V)
    """
    # 优先队列: (cost, node)
    frontier = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        current_cost, current = heapq.heappop(frontier)

        if current == goal:
            break

        for neighbor, weight in graph.neighbors(current):
            new_cost = cost_so_far[current] + weight

            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost
                heapq.heappush(frontier, (priority, neighbor))
                came_from[neighbor] = current

    # 重建路径
    if goal not in came_from:
        return [], float('inf')

    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()

    return path, cost_so_far[goal]

def a_star(
    graph: Graph,
    start,
    goal,
    heuristic: Callable[[any, any], float]
) -> Tuple[List, float]:
    """
    A*启发式搜索算法

    时间复杂度: O((V + E) log V) 最坏情况，通常更快
    空间复杂度: O(V)

    Args:
        heuristic: 启发函数 h(node, goal) -> estimated_cost
    """
    # 优先队列: (f_score, node) where f = g + h
    frontier = [(0, start)]
    came_from = {start: None}
    g_score = {start: 0}  # 从起点到节点的实际代价
    f_score = {start: heuristic(start, goal)}  # g + h

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == goal:
            break

        for neighbor, weight in graph.neighbors(current):
            tentative_g = g_score[current] + weight

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(frontier, (f_score[neighbor], neighbor))

    # 重建路径
    if goal not in came_from:
        return [], float('inf')

    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()

    return path, g_score[goal]

# 示例：曼哈顿距离启发函数（网格图）
def manhattan_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
    """曼哈顿距离（网格寻路）"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# 示例：欧几里得距离启发函数
def euclidean_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
    """欧几里得距离"""
    return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5

class GridGraph:
    """网格图（支持障碍物）"""
    def __init__(self, width: int, height: int, obstacles: Set[Tuple[int, int]]):
        self.width = width
        self.height = height
        self.obstacles = obstacles

    def neighbors(self, pos: Tuple[int, int]) -> List[Tuple[Tuple[int, int], float]]:
        """获取相邻节点（上下左右）"""
        x, y = pos
        results = []

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if (nx, ny) not in self.obstacles:
                    results.append(((nx, ny), 1.0))  # 权重为1

        return results

    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> List:
        """使用A*寻路"""
        return a_star(self, start, goal, manhattan_distance)[0]
```

» 写入 pathfinding.py
» 写入 test_pathfinding.py
✓ pathfinding 28.7s
```

### Usage

```python
from pathfinding import GridGraph, a_star, manhattan_distance

# 创建10x10网格，带障碍物
obstacles = {(2, 2), (2, 3), (2, 4), (3, 4), (4, 4)}
grid = GridGraph(10, 10, obstacles)

# 寻路
start = (0, 0)
goal = (9, 9)
path = grid.find_path(start, goal)

print(f"Path: {path}")
# Path: [(0,0), (0,1), (1,1), ..., (9,9)]
```

---

## Example 3: Expression Parser

Build a mathematical expression parser with tokenization and AST generation.

### Command

```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: expr-parser
backend: codex
workdir: /home/user/algorithms
model: gpt-5.2
timeout: 180
---CONTENT---
实现简单的表达式解析器：
1. 支持四则运算（+ - * /）、括号、变量
2. 词法分析（tokenization）
3. 语法分析（递归下降解析器）
4. AST生成和求值
---END---
EOF
```

### Expected Output

```python
# 生成的表达式解析器代码（简化版）
class ExprParser:
    def parse(self, expr: str) -> float:
        """解析并求值表达式"""
        tokens = self.tokenize(expr)
        ast = self.build_ast(tokens)
        return self.evaluate(ast)
```

---

## Common Level 4 Task Patterns

### Advanced Data Structures
- Trees (AVL, Red-Black, B-tree)
- Graphs (adjacency list/matrix, DAG)
- Heaps (binary heap, Fibonacci heap)
- Tries, suffix trees

### Algorithm Types
- Sorting (merge sort, quick sort, heap sort)
- Searching (binary search, interpolation search)
- Dynamic programming (knapsack, LCS, edit distance)
- Greedy algorithms (activity selection, Huffman coding)

### Computational Geometry
- Convex hull (Graham scan)
- Line intersection
- Closest pair of points
- Voronoi diagrams

### Cryptography & Hashing
- Hash functions (SHA, MD5)
- Encryption algorithms (AES, RSA)
- Digital signatures
- Merkle trees

---

## Example 4: Algorithm Library with Auto-Decomposition + Parallel Execution

This example demonstrates L4 full capabilities: automatic task decomposition, dependency analysis, and parallel execution for complex algorithm libraries.

### Single Task Input (Auto-Decomposed)

```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: search-library
backend: codex
model: gpt-5.2
workdir: ./algorithms
timeout: 300
---CONTENT---
创建完整的搜索算法库：
1. 二分搜索 (search/binary.py) - 支持自定义比较器
2. 插值搜索 (search/interpolation.py) - 均匀分布数据优化
3. 指数搜索 (search/exponential.py) - 无界数组搜索
4. 跳跃搜索 (search/jump.py) - 有序数组块搜索
5. 斐波那契搜索 (search/fibonacci.py) - 分治优化
6. 算法基类和接口 (search/base.py)
7. 性能基准测试 (benchmarks/search_benchmark.py)
8. 完整单元测试 (tests/test_search.py)

要求：
- 完整类型注解
- 时间复杂度分析注释
- 泛型支持
---END---
EOF
```

### Auto-Decomposition Process

```
▶ Task Decomposition Analysis
  Input: 1 complex task (algorithm library)
  Detected Components: 8 files
  Generated Subtasks: 8

  Decomposition Strategy: Layer-based
  ┌──────────────────────────────────────────────────────────┐
  │ Layer 1: Foundation (No deps)                            │
  │   - search-library-base (base.py)                        │
  │                                                          │
  │ Layer 2: Implementations (Parallel, depends on Layer 1)  │
  │   - search-library-binary (binary.py)                    │
  │   - search-library-interpolation (interpolation.py)      │
  │   - search-library-exponential (exponential.py)          │
  │   - search-library-jump (jump.py)                        │
  │   - search-library-fibonacci (fibonacci.py)              │
  │                                                          │
  │ Layer 3: Validation (Parallel, depends on Layer 2)       │
  │   - search-library-benchmark (benchmark.py)              │
  │   - search-library-tests (test_search.py)                │
  └──────────────────────────────────────────────────────────┘
```

### Auto-Generated Dependency Graph

```
▶ Dependency Analysis
  Implicit Dependencies Detected:
    - All search algorithms import base.py
    - benchmark.py imports all algorithms
    - test_search.py imports all algorithms

  Generated DAG:

Phase 1: Foundation
┌─────────────────────────┐
│ search-library-base     │
│ (search/base.py)        │
│ 3.2s                    │
└───────────┬─────────────┘
            │
            ↓
Phase 2: Algorithm Implementations (5 tasks parallel)
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ binary   │ │ interp.  │ │ expon.   │ │ jump     │ │ fibonacci│
│ 4.1s     │ │ 4.3s     │ │ 3.9s     │ │ 3.7s     │ │ 4.5s     │
└────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘
     │            │            │            │            │
     └────────────┴────────────┼────────────┴────────────┘
                               ↓
Phase 3: Validation (2 tasks parallel)
         ┌──────────────────┐  ┌──────────────────┐
         │ benchmark        │  │ tests            │
         │ 5.2s             │  │ 4.8s             │
         └──────────────────┘  └──────────────────┘
```

### Execution Output

```
▶ Executing search-library with auto-decomposition

▶ Phase 1: Foundation
  » search-library-base

  ```python
  from abc import ABC, abstractmethod
  from typing import TypeVar, Generic, Callable, Optional, List

  T = TypeVar('T')

  class SearchAlgorithm(ABC, Generic[T]):
      """
      搜索算法基类

      时间复杂度分析：
      - 最佳情况: O(1) - 首次命中
      - 最坏情况: 子类定义
      - 平均情况: 子类定义
      """

      @abstractmethod
      def search(
          self,
          arr: List[T],
          target: T,
          comparator: Optional[Callable[[T, T], int]] = None
      ) -> int:
          """
          在有序数组中搜索目标元素

          Args:
              arr: 有序数组
              target: 目标元素
              comparator: 自定义比较函数，返回 -1/0/1

          Returns:
              目标元素索引，未找到返回 -1
          """
          pass

      def _compare(self, a: T, b: T, comparator: Optional[Callable]) -> int:
          """比较两个元素"""
          if comparator:
              return comparator(a, b)
          if a < b:
              return -1
          elif a > b:
              return 1
          return 0
  ```
  » 写入 search/base.py
  ✓ search-library-base 3.2s

▶ Phase 2: Implementations (5 tasks parallel)
  » Executing 5 tasks in parallel...

  ✓ search-library-binary 4.1s
    » 写入 search/binary.py (O(log n) 二分搜索)
  ✓ search-library-interpolation 4.3s
    » 写入 search/interpolation.py (O(log log n) 均匀分布)
  ✓ search-library-exponential 3.9s
    » 写入 search/exponential.py (O(log n) 无界搜索)
  ✓ search-library-jump 3.7s
    » 写入 search/jump.py (O(√n) 块搜索)
  ✓ search-library-fibonacci 4.5s
    » 写入 search/fibonacci.py (O(log n) 分治)

▶ Phase 3: Validation (2 tasks parallel)
  » Executing 2 tasks in parallel...

  ✓ search-library-benchmark 5.2s
    » 写入 benchmarks/search_benchmark.py
  ✓ search-library-tests 4.8s
    » 写入 tests/test_search.py

═══════════════════════════════════════════════════════════════
✓ search-library completed
  Subtasks: 8
  Total Time: 13.2s (vs 37.7s serial = 65% faster)
  Files Generated:
    - search/base.py
    - search/binary.py
    - search/interpolation.py
    - search/exponential.py
    - search/jump.py
    - search/fibonacci.py
    - benchmarks/search_benchmark.py
    - tests/test_search.py
═══════════════════════════════════════════════════════════════
```

### L4 Execution Features

| Feature | Description |
|---------|-------------|
| **Task Decomposition** | Single task → 8 subtasks |
| **Dependency Analysis** | Auto-detect import relationships |
| **Parallel Execution** | 5 algorithms in parallel |
| **Phase Scheduling** | 3-phase execution plan |
| **Performance Gain** | 65% faster than serial |

---

## Model Selection for Level 4

| Task Type | Model | Timeout | Execution |
|-----------|-------|---------|-----------|
| Standard algorithms | `gpt-5.2` | 180s | Parallel with decomposition |
| Algorithm libraries | `gpt-5.2` | 300s | Multi-phase parallel |
| Complex optimization | `gpt-5.2` | 240s | Auto DAG construction |
| Cryptographic algorithms | `gpt-5.2` | 300s | Sequential (security) |

**L4 Execution Features:**
- Automatic task decomposition for algorithm libraries
- Implicit dependency detection (import analysis)
- Parallel execution of independent algorithms
- Phase-based execution scheduling

**When to upgrade to Level 5**:
- Multi-module projects (not single algorithm)
- System architecture design needed
- Microservices or distributed systems

---

## Tips for Level 4 Tasks

1. **Specify complexity**: Request O(log n) or O(n log n) explicitly
2. **Include tests**: Ask for unit tests with edge cases
3. **Request analysis**: Ask for time/space complexity comments
4. **Provide examples**: Include sample input/output in prompt
5. **Increase timeout**: Use 180-300s for complex algorithms

---

## Related Resources

- [references/complexity-guide.md](../references/complexity-guide.md) - Level 4 detailed guidance
- [examples/level3-modules.md](./level3-modules.md) - Production modules
- [examples/level5-architecture.md](./level5-architecture.md) - System design
- [skills/memex-cli/SKILL.md](../../memex-cli/SKILL.md) - Memex CLI usage
