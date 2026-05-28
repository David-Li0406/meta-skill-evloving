# Code Blocks

## Configuration

```yaml
# mkdocs.yml
theme:
  features:
    - content.code.copy      # copy button
    - content.code.annotate  # annotations

markdown_extensions:
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.superfences
```

## Basic Syntax

````markdown
```python
def hello():
    print("Hello, world!")
```
````

## Line Numbers

````markdown
```python linenums="1"
def hello():
    print("Hello")
```
````

Start from different number: `linenums="5"`

## Highlight Lines

````markdown
```python hl_lines="2 3"
def process():
    important_line()  # highlighted
    also_this()       # highlighted
    not_this()
```
````

Range syntax: `hl_lines="1-3 5"`

## Title/Filename

````markdown
```python title="main.py"
def main():
    pass
```
````

## Annotations

Add numbered comments, explanations below:

````markdown
```python
def hello():
    print("Hello")  # (1)
```

1. This prints to stdout.
````

Strip comment marker with `!`: `# (1)!`

## Copy Button Control

````markdown
```yaml { .copy }
content: copied
```

```yaml { .no-copy }
content: not copyable
```
````

## Inline Code Highlighting

```markdown
Use `#!python print()` for inline syntax.
```
