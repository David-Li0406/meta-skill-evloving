# MY-LLM-SDK API Cheatsheet

> 快速参考手册，包含常用调用代码示例。

## 1. 初始化

```python
from my_llm_sdk.client import LLMClient

# 自动加载 config.yaml 和 llm.project.yaml
client = LLMClient()

# 指定配置路径
client = LLMClient(
    user_config_path="~/.config/llm-sdk/config.yaml",
    project_config_path="./llm.project.yaml"
)
```

---

## 2. 文本生成

### 基础调用

```python
response = client.generate(prompt="用一句话解释量子计算")
print(response)  # str
```

### 指定模型

```python
response = client.generate(
    prompt="Hello",
    model_alias="gemini-2.5-flash"  # 在 llm.project.yaml 中定义的别名
)
```

### 配置参数

```python
response = client.generate(
    prompt="Write a creative story",
    model_alias="default",
    config={
        "max_output_tokens": 2000,
        "temperature": 0.9,
        "top_p": 0.95
    }
)
```

### 获取完整响应（含 usage、cost）

```python
resp = client.generate(prompt="Hello", full_response=True)

print(resp.content)       # 文本内容
print(resp.usage)         # TokenUsage(input_tokens=5, output_tokens=10, ...)
print(resp.cost)          # 0.00015 (USD)
print(resp.finish_reason) # "stop"
```

---

## 3. 流式输出

```python
for event in client.stream(prompt="写一个长故事"):
    if event.delta:
        print(event.delta, end="", flush=True)
    if event.is_finish:
        print(f"\n完成: {event.finish_reason}")
```

---

## 4. Async 调用

```python
import asyncio

async def main():
    response = await client.generate_async(prompt="Hello")
    print(response)
    
    # Async streaming
    async for event in client.stream_async(prompt="Write a poem"):
        if event.delta:
            print(event.delta, end="")

asyncio.run(main())
```

---

## 5. 多模态输入 (Vision)

```python
from PIL import Image

# 方式 1: PIL Image
img = Image.open("photo.jpg")
response = client.generate(contents=[img, "这张图片是什么？"])

# 方式 2: 混合内容列表
response = client.generate(contents=[
    "分析以下图片:",
    img,
    "重点关注颜色搭配"
])
```

---

## 6. 图片生成

### Gemini Native Image Generation

```python
resp = client.generate(
    prompt="A futuristic city at sunset",
    model_alias="gemini-2.5-flash",
    config={
        "task": "image_generation",
        "response_modalities": ["IMAGE"]
    },
    full_response=True
)

# 保存图片
for part in resp.media_parts:
    with open("output.jpg", "wb") as f:
        f.write(part.inline_data)
```

### Imagen 模型

```python
resp = client.generate(
    prompt="A cat astronaut",
    model_alias="imagen-3.0",  # 需在 llm.project.yaml 定义
    full_response=True
)
```

---

## 7. TTS (文本转语音)

```python
resp = client.generate(
    prompt="你好，欢迎使用语音合成",
    model_alias="gemini-2.5-flash",
    config={
        "task": "tts",
        "voice_config": {"voice_name": "Puck"}
    },
    full_response=True
)

# 保存音频
for part in resp.media_parts:
    if part.type == "audio":
        with open("output.wav", "wb") as f:
            f.write(part.inline_data)
```

---

## 8. JSON 输出

```python
response = client.generate(
    prompt="生成一个用户信息 JSON，包含 name 和 age",
    config={"response_mime_type": "application/json"}
)
# response 是 JSON 字符串，可用 json.loads() 解析
```

---

## 9. 错误处理

```python
from my_llm_sdk.config.exceptions import ConfigurationError

try:
    response = client.generate(prompt="Hello")
except ConfigurationError as e:
    print(f"配置错误: {e}")
except RuntimeError as e:
    print(f"API 错误: {e}")
```

---

## 10. 常用 model_alias 配置 (llm.project.yaml)

```yaml
model_registry:
  default:
    name: default
    provider: google
    model_id: gemini-2.5-flash
    
  gemini-pro:
    name: gemini-pro
    provider: google
    model_id: gemini-2.5-pro
    
  qwen-plus:
    name: qwen-plus
    provider: dashscope
    model_id: qwen-plus
```

---

**完整文档**: [my-llm-sdk GitHub](https://github.com/wenjie2024/my-llm-sdk)
