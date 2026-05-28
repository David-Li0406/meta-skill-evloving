# Code blocks and code spans

Use consistent code formatting for readability and tooling.

## MD031 - Fenced code blocks should be surrounded by blank lines

Surround fenced code blocks with blank lines.

Bad:

````markdown
Text
```text
code
```
More text
````

Good:

````markdown
Text

```text
code
```

More text
````

## MD038 - Spaces inside code span elements

Do not add extra spaces inside inline code backticks.

Bad:

```markdown
Use ` code ` here.
```

Good:

```markdown
Use `code` here.
```

## MD040 - Fenced code blocks should have a language specified

Add a language identifier to fenced code blocks.

Bad:

````markdown
```
echo "hi"
```
````

Good:

````markdown
```sh
echo "hi"
```
````

## MD046 - Code block style

Use a consistent code block style within a document.
Prefer fenced blocks for most documentation.

Bad:

````markdown
Paragraph

    indented code

```text
fenced code
```
````

Good:

````markdown
Paragraph

```text
fenced code
```

```text
fenced code again
```
````

## MD048 - Code fence style

Use a consistent fence marker for code blocks.
Do not mix backticks and tildes in the same document.

Bad:

````markdown
```text
one
```

~~~text
two
~~~
````

Good:

````markdown
```text
one
```

```text
two
```
````
