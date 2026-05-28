---
name: gen-task
description: 根据 tasks 目录下的 md 任务文档生成代码框架和测试代码
argument-hint: [task-md-file]
disable-model-invocation: true
---

# 任务代码生成器

根据指定的任务 md 文档，生成代码框架和自动测试代码。

## 参数

`$ARGUMENTS` - tasks 目录下的 md 文件名（如 `task1_thread_wrapper.md`）

## 执行步骤

1. **读取任务文档**
   - 读取 `/home/tyrfly1001/threadpool/tasks/$ARGUMENTS`
   - 分析任务要求、学习目标、实践练习

2. **项目结构**
   - 公共模块目录: `/home/tyrfly1001/threadpool/tasks/common/`
     ```
     tasks/
     ├── common/                    # 共享目录（公共工具）
     │   ├── utils.py               # Python 测试工具
     │   ├── utils.cpp              # C++ 辅助代码
     │   └── requirements.txt       # Python 依赖
     ├── task0/
     │   ├── main.cpp
     │   └── autograder/
     │       └── autograder.py
     └── taskN/
         ├── main.cpp              # 代码框架，包含 TODO 标记
         └── autograder/
             └── autograder.py     # Python 测试脚本（引用 common）
     ```

3. **生成代码框架 (main.cpp)**
   - 包含必要的头文件
   - 定义练习函数的签名，函数体用 `// TODO:` 标记
   - 包含 `#include "../common/utils.cpp"` 和 `run_autograder()` 调用
   - 添加清晰的注释说明每个练习的要求

4. **生成测试代码 (autograder/autograder.py)**
   - 参考 `/home/tyrfly1001/threadpool/tasks/task0/autograder/autograder.py` 的格式
   - 使用 `sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'common'))` 引用公共模块
   - 为每个练习编写测试函数
   - 使用 `Autograder` 类注册测试

5. **首次运行时创建 common 目录**
   - 如果 `tasks/common/` 不存在，从 task0 复制工具文件创建

## 输出格式

生成的文件应放在 `tasks/taskN/` 目录下，其中 N 从 md 文件名提取（如 task1_thread_wrapper.md -> task1/）

## 代码框架模板

```cpp
/**
 * Task N: [任务标题] - 实践练习
 *
 * 编译并运行测试:
 *   g++ -std=c++11 -pthread main.cpp -o main && ./main
 *
 * 说明:
 *   请在标记 "TODO" 的地方填写代码，完成后运行程序验证你的实现。
 */

#include "../common/utils.cpp"
// 其他必要的头文件

// ============================================================
// 练习 1: [练习标题]
//
// 任务: [任务描述]
//
// 提示:
//   - [提示1]
//   - [提示2]
// ============================================================

void exercise1() {
    // TODO: 实现代码
}

// ... 更多练习 ...

int main() {
    return run_autograder();
}
```

## 测试代码模板

```python
"""
Task N: [任务标题] - 自动测试
"""

import sys
import os

# 引用公共模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'common'))
from utils import Autograder, ASSIGNMENT_DIR

import subprocess

# 配置
EXECUTABLE = os.path.join(ASSIGNMENT_DIR, "student_code")
SOURCE_FILE = os.path.join(ASSIGNMENT_DIR, "main.cpp")

# 测试代码模板 (C++ 测试代码)
TEST_CODE = '''
// C++ 测试代码
'''

def setup_test_environment():
    """准备测试环境"""
    # 编译学生代码和测试代码
    pass

def cleanup_test_environment():
    """清理测试环境"""
    pass

def test_exercise1():
    """测试练习 1"""
    pass

if __name__ == "__main__":
    grader = Autograder()
    grader.setup = setup_test_environment
    grader.teardown = cleanup_test_environment

    grader.add_part("练习 1: [描述]", test_exercise1)
    # 添加更多测试...

    exit(grader.run())
```
