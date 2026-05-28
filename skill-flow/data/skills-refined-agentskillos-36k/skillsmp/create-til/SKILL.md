---
name: create-til
description: 添加新的 TIL 笔记
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: documentation
---

## 功能

使用 `just new "标题"` 创建新的 TIL 笔记入口，然后根据提示风格和模板添加相关内容。

## 风格

- 标题：简洁明了，不超过 50 字
- tags：使用英文，如 `git`, `python`, `macos`
- 正文：中文，技术术语用英文
- 代码：包含实际可用的示例
- 避免：过多铺垫，直接切入主题
- 可选：复杂内容用 `<details>` 折叠

## 模板

```yaml
---
title: "简短描述"
tags:
  - tag1
  - tag2
date: YYYY-MM-DD
---

一句话描述问题或知识点。

代码示例。
```
