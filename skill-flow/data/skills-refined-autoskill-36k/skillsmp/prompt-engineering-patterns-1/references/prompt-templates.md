# 提示模板系统

## 模板架构

### 基本模板结构
```python
class PromptTemplate:
    def __init__(self, template_string, variables=None):
        self.template = template_string
        self.variables = variables or []

    def render(self, **kwargs):
        missing = set(self.variables) - set(kwargs.keys())
        if missing:
            raise ValueError(f"缺少必需变量：{missing}")

        return self.template.format(**kwargs)

# 使用示例
template = PromptTemplate(
    template_string="将{text}从{source_lang}翻译为{target_lang}",
    variables=['text', 'source_lang', 'target_lang']
)

prompt = template.render(
    text="你好世界",
    source_lang="中文",
    target_lang="英文"
)
```

### 条件模板
```python
class ConditionalTemplate(PromptTemplate):
    def render(self, **kwargs):
        # 处理条件块
        result = self.template

        # 处理if块：{{#if variable}}content{{/if}}
        import re
        if_pattern = r'\{\{#if (\w+)\}\}(.*?)\{\{/if\}\}'

        def replace_if(match):
            var_name = match.group(1)
            content = match.group(2)
            return content if kwargs.get(var_name) else ''

        result = re.sub(if_pattern, replace_if, result, flags=re.DOTALL)

        # 处理for循环：{{#each items}}{{this}}{{/each}}
        each_pattern = r'\{\{#each (\w+)\}\}(.*?)\{\{/each\}\}'

        def replace_each(match):
            var_name = match.group(1)
            content = match.group(2)
            items = kwargs.get(var_name, [])
            return '\n'.join(content.replace('{{this}}', str(item)) for item in items)

        result = re.sub(each_pattern, replace_each, result, flags=re.DOTALL)

        # 最后，渲染剩余变量
        return result.format(**kwargs)

# 使用示例
template = ConditionalTemplate("""
分析以下文本：
{text}

{{#if include_sentiment}}
提供情感分析。
{{/if}}

{{#if include_entities}}
提取命名实体。
{{/if}}

{{#if examples}}
参考示例：
{{#each examples}}
- {{this}}
{{/each}}
{{/if}}
""")
```

### 模块化模板组合
```python
class ModularTemplate:
    def __init__(self):
        self.components = {}

    def register_component(self, name, template):
        self.components[name] = template

    def render(self, structure, **kwargs):
        parts = []
        for component_name in structure:
            if component_name in self.components:
                component = self.components[component_name]
                parts.append(component.format(**kwargs))

        return '\n\n'.join(parts)

# 使用示例
builder = ModularTemplate()

builder.register_component('system', "你是一个{role}。")
builder.register_component('context', "上下文：{context}")
builder.register_component('instruction', "任务：{task}")
builder.register_component('examples', "示例：\n{examples}")
builder.register_component('input', "输入：{input}")
builder.register_component('format', "输出格式：{format}")

# 为不同场景组合不同模板
basic_prompt = builder.render(
    ['system', 'instruction', 'input'],
    role='有用的助手',
    instruction='总结文本',
    input='...'
)

advanced_prompt = builder.render(
    ['system', 'context', 'examples', 'instruction', 'input', 'format'],
    role='专家分析师',
    context='财务分析',
    examples='...',
    instruction='分析情感',
    input='...',
    format='JSON'
)
```

## 常见模板模式

### 分类模板
```python
CLASSIFICATION_TEMPLATE = """
将以下{content_type}分类到以下类别之一：{categories}

{{#if description}}
类别描述：
{description}
{{/if}}

{{#if examples}}
示例：
{examples}
{{/if}}

{content_type}：{input}

类别："""
```

### 提取模板
```python
EXTRACTION_TEMPLATE = """
从{content_type}中提取结构化信息。

必填字段：
{field_definitions}

{{#if examples}}
示例提取：
{examples}
{{/if}}

{content_type}：{input}

提取的信息（JSON）："""
```

### 生成模板
```python
GENERATION_TEMPLATE = """
基于以下{input_type}生成{output_type}。

要求：
{requirements}

{{#if style}}
风格：{style}
{{/if}}

{{#if constraints}}
约束：
{constraints}
{{/if}}

{{#if examples}}
示例：
{examples}
{{/if}}

{input_type}：{input}

{output_type}："""
```

### 转换模板
```python
TRANSFORMATION_TEMPLATE = """
将输入的{source_format}转换为{target_format}。

转换规则：
{rules}

{{#if examples}}
示例转换：
{examples}
{{/if}}

输入{source_format}：
{input}

输出{target_format}："""
```

## 高级功能

### 模板继承
```python
class TemplateRegistry:
    def __init__(self):
        self.templates = {}

    def register(self, name, template, parent=None):
        if parent and parent in self.templates:
            # 从父模板继承
            base = self.templates[parent]
            template = self.merge_templates(base, template)

        self.templates[name] = template

    def merge_templates(self, parent, child):
        # 子模板覆盖父模板部分
        return {**parent, **child}

# 使用示例
registry = TemplateRegistry()

registry.register('base_analysis', {
    'system': '你是一个专家分析师。',
    'format': '以结构化格式提供分析。'
})

registry.register('sentiment_analysis', {
    'instruction': '分析情感',
    'format': '提供-1到1的情感分数。'
}, parent='base_analysis')
```

### 变量验证
```python
class ValidatedTemplate:
    def __init__(self, template, schema):
        self.template = template
        self.schema = schema

    def validate_vars(self, **kwargs):
        for var_name, var_schema in self.schema.items():
            if var_name in kwargs:
                value = kwargs[var_name]

                # 类型验证
                if 'type' in var_schema:
                    expected_type = var_schema['type']
                    if not isinstance(value, expected_type):
                        raise TypeError(f"{var_name} 必须是 {expected_type}")

                # 范围验证
                if 'min' in var_schema and value < var_schema['min']:
                    raise ValueError(f"{var_name} 必须 >= {var_schema['min']}")

                if 'max' in var_schema and value > var_schema['max']:
                    raise ValueError(f"{var_name} 必须 <= {var_schema['max']}")

                # 枚举验证
                if 'choices' in var_schema and value not in var_schema['choices']:
                    raise ValueError(f"{var_name} 必须是 {var_schema['choices']} 之一")

    def render(self, **kwargs):
        self.validate_vars(**kwargs)
        return self.template.format(**kwargs)

# 使用示例
template = ValidatedTemplate(
    template="用{length}个词以{tone}语气总结",
    schema={
        'length': {'type': int, 'min': 10, 'max': 500},
        'tone': {'type': str, 'choices': ['formal', 'casual', 'technical']}
    }
)
```

### 模板缓存
```python
class CachedTemplate:
    def __init__(self, template):
        self.template = template
        self.cache = {}

    def render(self, use_cache=True, **kwargs):
        if use_cache:
            cache_key = self.get_cache_key(kwargs)
            if cache_key in self.cache:
                return self.cache[cache_key]

        result = self.template.format(**kwargs)

        if use_cache:
            self.cache[cache_key] = result

        return result

    def get_cache_key(self, kwargs):
        return hash(frozenset(kwargs.items()))

    def clear_cache(self):
        self.cache = {}
```

## 多轮模板

### 对话模板
```python
class ConversationTemplate:
    def __init__(self, system_prompt):
        self.system_prompt = system_prompt
        self.history = []

    def add_user_message(self, message):
        self.history.append({'role': 'user', 'content': message})

    def add_assistant_message(self, message):
        self.history.append({'role': 'assistant', 'content': message})

    def render_for_api(self):
        messages = [{'role': 'system', 'content': self.system_prompt}]
        messages.extend(self.history)
        return messages

    def render_as_text(self):
        result = f"系统：{self.system_prompt}\n\n"
        for msg in self.history:
            role = msg['role'].capitalize()
            result += f"{role}：{msg['content']}\n\n"
        return result
```

### 基于状态的模板
```python
class StatefulTemplate:
    def __init__(self):
        self.state = {}
        self.templates = {}

    def set_state(self, **kwargs):
        self.state.update(kwargs)

    def register_state_template(self, state_name, template):
        self.templates[state_name] = template

    def render(self):
        current_state = self.state.get('current_state', 'default')
        template = self.templates.get(current_state)

        if not template:
            raise ValueError(f"没有状态的模板：{current_state}")

        return template.format(**self.state)

# 用于多步骤工作流的使用示例
workflow = StatefulTemplate()

workflow.register_state_template('init', """
欢迎！让我们{task}。
你的{first_input}是什么？
""")

workflow.register_state_template('processing', """
谢谢！正在处理{first_input}。
现在，你的{second_input}是什么？
""")

workflow.register_state_template('complete', """
很好！基于：
- {first_input}
- {second_input}

结果如下：{result}
""")
```

## 最佳实践

1. **保持DRY**：使用模板避免重复
2. **早期验证**：渲染前检查变量
3. **版本化模板**：像代码一样跟踪变更
4. **测试变体**：确保模板对多样化输入有效
5. **记录变量**：清楚指定必需/可选变量
6. **使用类型提示**：使变量类型明确
7. **提供默认值**：在适当时设置合理的默认值
8. **明智缓存**：缓存静态模板，而非动态模板

## 模板库

### 问答
```python
QA_TEMPLATES = {
    'factual': """基于上下文回答问题。

上下文：{context}
问题：{question}
答案：""",

    'multi_hop': """通过推理多个事实来回答问题。

事实：{facts}
问题：{question}

推理：""",

    'conversational': """自然地继续对话。

之前的对话：
{history}

用户：{question}
助手："""
}
```

### 内容生成
```python
GENERATION_TEMPLATES = {
    'blog_post': """写一篇关于{topic}的博客文章。

要求：
- 长度：{word_count}词
- 语气：{tone}
- 包括：{key_points}

博客文章：""",

    'product_description': """为{product}写产品描述。

功能：{features}
优点：{benefits}
目标受众：{audience}

描述：""",

    'email': """写一封{type}邮件。

收件人：{recipient}
上下文：{context}
要点：{key_points}

邮件："""
}
```

## 性能考虑

- 为重复使用预编译模板
- 当变量为静态时缓存渲染的模板
- 最小化循环中的字符串连接
- 使用高效的字符串格式化（f-strings、.format()）
- 分析模板渲染的瓶颈