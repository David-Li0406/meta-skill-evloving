---
name: punctuation-normalizer
description: Normalize Chinese punctuation to English punctuation with proper spacing. Use when the user asks to normalize punctuation, clean Chinese technical writing, convert Chinese punctuation to English style, or format Markdown while preserving code/math. This Skill converts Chinese punctuation marks (，。！？：；（）等) into English punctuation with proper spacing while preserving Markdown code blocks, inline code, and LaTeX math ($...$, $$...$$).
---

# Punctuation Normalizer

## Purpose

This Skill converts Chinese punctuation marks (，。！？：；（）等)
into English punctuation with proper spacing, while **preserving**:

- Markdown code blocks
- Inline code
- LaTeX math ($...$, $$...$$)

## How to use

1. Take the full input text as-is
2. Pipe it to the script:
   `python scripts/normalize.py`
3. Return the script output directly
4. Do NOT re-edit or paraphrase the output

## Example

Input:

````markdown
这是一个示例文本，包含中文标点。

下面是代码块：

```rust
fn main() {
    println!("Hello，world！");
}
````

这里有行内代码 `let x = a，b + c；`，
以及行内公式 $x = y，z + 1$。

多行公式：

$$
f(x，y) = x^2 + y^2；
$$

结束。

````

Output:

```markdown
这是一个示例文本, 包含中文标点.

下面是代码块：

```rust
fn main() {
    println!("Hello，world！");
}
````

这里有行内代码 `let x = a，b + c；`,
以及行内公式 $x = y，z + 1$.

多行公式：

$$
f(x，y) = x^2 + y^2；
$$

结束.

```

