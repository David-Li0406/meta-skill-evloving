---
name: translate
description: Language translation and grammar teaching skill for Chinese-English translation. Use when the user requests translation between Chinese and English, asks for grammar explanations, or wants to learn/improve their English. Handles pure Chinese, pure English, or mixed Chinese-English input and provides translations with grammar analysis.
---

# Translate

## Overview

This skill provides language translation and grammar teaching between Chinese and English. It acts as a translation teacher, helping users understand both the translation and the grammatical structure of English sentences.

## When to Use This Skill

Use this skill when users:
- Request translation from Chinese to English or English to Chinese
- Provide mixed Chinese-English text that needs translation
- Ask for grammar explanations or corrections
- Want to learn or improve their English language skills

## Output Format

For every translation request, provide output in this exact format:

```
纯中文句子：
[The complete sentence in Chinese]

英文句子：
[The complete sentence in English]

语法问题：
1. [First grammar point or error explanation]
2. [Second grammar point or error explanation]
...
```

## Guidelines

### Translation Approach

1. **Accuracy**: Provide accurate translations that preserve the original meaning
2. **Natural Language**: Use natural, idiomatic expressions in both languages
3. **Context Awareness**: Consider the context and tone of the original text

### Grammar Analysis

1. **Identify Errors**: Point out grammatical mistakes in the English sentence (whether from the original input or potential errors in translation)
2. **Explain Rules**: Provide clear explanations of the grammar rules involved
3. **Be Constructive**: Focus on teaching and helping the user understand, not just correcting
4. **Common Patterns**: Pay attention to common mistakes Chinese speakers make in English:
   - Article usage (a, an, the)
   - Verb tenses and aspects
   - Plural forms
   - Word order
   - Preposition usage
   - Subject-verb agreement

### Special Cases

- **If input is pure Chinese**: Translate to English and analyze the English grammar
- **If input is pure English**: Provide Chinese translation and analyze English grammar issues
- **If input is mixed**: Separate and clarify both languages, then provide complete translations and grammar analysis
- **If no grammar errors**: Still provide relevant grammar points or usage notes that would be educational

## Examples

### Example 1: Chinese Input

**User Input**: "我昨天去了商店买东西"

**Output**:
```
纯中文句子：
我昨天去了商店买东西

英文句子：
I went to the store to buy things yesterday.

语法问题：
1. 时间状语位置：英文中时间状语"yesterday"通常放在句末，也可以放在句首，但不像中文那样紧跟主语
2. 不定式表目的：使用"to buy"表示目的，这是英文中表达目的的常用方式
3. 过去时态：使用"went"（go的过去式）表示过去发生的动作
```

### Example 2: English Input with Errors

**User Input**: "I go to store yesterday and buy some thing"

**Output**:
```
纯中文句子：
我昨天去了商店买了一些东西

英文句子：
I went to the store yesterday and bought some things.

语法问题：
1. 时态错误：应该使用过去时"went"和"bought"，而不是现在时"go"和"buy"，因为有时间状语"yesterday"
2. 冠词缺失：应该是"the store"或"a store"，英文中可数名词单数前需要冠词
3. 拼写错误："some thing"应该写成一个词"something"，或者用"some things"（复数形式）
4. 并列动词时态：并列连词"and"连接的两个动词应该保持时态一致
```

### Example 3: Mixed Input

**User Input**: "我想要learn English但是很difficult"

**Output**:
```
纯中文句子：
我想要学习英语但是很困难

英文句子：
I want to learn English, but it's very difficult.

语法问题：
1. 不定式结构：使用"want to learn"表示"想要学习"，"want"后面需要接不定式"to + 动词原形"
2. 逗号使用：在"but"前面应该加逗号，因为这是连接两个独立句子的并列连词
3. 主语补充：第二个分句需要补充主语"it"和系动词"is"，构成完整句子"it's very difficult"
4. 形容词用法："difficult"是形容词，需要与系动词"is"搭配使用
```
