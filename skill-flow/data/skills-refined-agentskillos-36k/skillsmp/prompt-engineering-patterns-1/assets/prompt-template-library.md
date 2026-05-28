# 提示模板库

## 分类模板

### 情感分析
```
将以下文本的情感分类为正面、负面或中性。

文本：{text}

情感：
```

### 意图检测
```
从以下消息中确定用户意图。

可能的意图：{intent_list}

消息：{message}

意图：
```

### 主题分类
```
将以下文章分类到这些类别之一：{categories}

文章：
{article}

类别：
```

## 提取模板

### 命名实体识别
```
从文本中提取所有命名实体并进行分类。

文本：{text}

实体（JSON格式）：
{
  "persons": [],
  "organizations": [],
  "locations": [],
  "dates": []
}
```

### 结构化数据提取
```
从招聘信息中提取结构化信息。

招聘信息：
{posting}

提取的信息（JSON）：
{
  "title": "",
  "company": "",
  "location": "",
  "salary_range": "",
  "requirements": [],
  "responsibilities": []
}
```

## 生成模板

### 邮件生成
```
写一封专业的{email_type}邮件。

收件人：{recipient}
上下文：{context}
要包含的要点：
{key_points}

邮件：
主题：
正文：
```

### 代码生成
```
为以下任务生成{language}代码：

任务：{task_description}

要求：
{requirements}

包括：
- 错误处理
- 输入验证
- 内联注释

代码：
```

### 创意写作
```
写一个{length}字的关于{topic}的{style}故事。

包括这些元素：
- {element_1}
- {element_2}
- {element_3}

故事：
```

## 转换模板

### 摘要
```
用{num_sentences}句话总结以下文本。

文本：
{text}

摘要：
```

### 带上下文的翻译
```
将以下{source_lang}文本翻译为{target_lang}。

上下文：{context}
语气：{tone}

文本：{text}

翻译：
```

### 格式转换
```
将以下{source_format}转换为{target_format}。

输入：
{input_data}

输出（{target_format}）：
```

## 分析模板

### 代码审查
```
审查以下代码的：
1. 错误和问题
2. 性能问题
3. 安全漏洞
4. 最佳实践违规

代码：
{code}

审查：
```

### SWOT分析
```
为：{subject}进行SWOT分析

上下文：{context}

分析：
优势：
-

劣势：
-

机会：
-

威胁：
-
```

## 问答模板

### RAG模板
```
基于提供的上下文回答问题。如果上下文信息不足，请说明。

上下文：
{context}

问题：{question}

答案：
```

### 多轮问答
```
之前的对话：
{conversation_history}

新问题：{question}

答案（从对话自然继续）：
```

## 专业模板

### SQL查询生成
```
为以下请求生成SQL查询。

数据库架构：
{schema}

请求：{request}

SQL查询：
```

### 正则表达式创建
```
创建匹配：{requirement}的正则表达式模式

应该匹配的测试案例：
{positive_examples}

不应该匹配的测试案例：
{negative_examples}

正则表达式模式：
```

### API文档
```
为此函数生成API文档：

代码：
{function_code}

文档（遵循{doc_format}格式）：
```

## 通过填充{variables}使用这些模板