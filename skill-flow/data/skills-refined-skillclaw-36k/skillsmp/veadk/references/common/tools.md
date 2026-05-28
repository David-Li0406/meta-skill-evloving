# Tools 定义方法

## 导入方法

- 网络搜索：`from veadk.tools.builtin_tools.web_search import web_search`
- 链接读取：`from veadk.tools.builtin_tools.link_reader import link_reader`
- 图像生成：`from veadk.tools.builtin_tools.image_generate import image_generate`
- 视频生成：`from veadk.tools.builtin_tools.video_generate import video_generate`
- 代码沙箱执行（用来执行 Python 代码）：`from veadk.tools.builtin_tools.run_code import run_code`

## 自定义 Tool

你可以通过撰写一个 Python 函数来定义一个自定义 Tool（你必须清晰地定义好 Docstring）：

```python
def add(a: int, b: int) -> int:
    """Add two integers together.
    
    Args:
        a (int): The first integer.
        b (int): The second integer.
    
    Returns:
        int: The sum of a and b.
    """
    return a + b


agent = Agent(tools=[add])
```

## 代码规范

你可以通过如下方式将某个工具挂载到智能体上，例如 `web_search` 网络搜索工具：

```python
from veadk.tools.builtin_tools.web_search import web_search

root_agent = Agent(
    name="...",
    description="...",
    instruction="...", # 智能体系统提示词
    tools=[web_search] # 挂载工具列表
)
```
