# Content Tabs

## Configuration

```yaml
# mkdocs.yml
markdown_extensions:
  - pymdownx.superfences
  - pymdownx.tabbed:
      alternate_style: true

theme:
  features:
    - content.tabs.link  # sync tabs across pages
```

## Basic Syntax

```markdown
=== "Tab One"

    Content for tab one.

=== "Tab Two"

    Content for tab two.
```

## Code Tabs

Single code block per tab (no extra spacing):

````markdown
=== "Python"

    ```python
    print("Hello")
    ```

=== "JavaScript"

    ```javascript
    console.log("Hello");
    ```

=== "Bash"

    ```bash
    echo "Hello"
    ```
````

## List Tabs

Multiple elements per tab (with spacing):

```markdown
=== "Unordered"

    * Item one
    * Item two
    * Item three

=== "Ordered"

    1. First
    2. Second
    3. Third
```

## Nested in Admonitions

```markdown
!!! example "Installation"

    === "pip"

        ```bash
        pip install package
        ```

    === "conda"

        ```bash
        conda install package
        ```
```

## Linked Tabs

With `content.tabs.link` enabled:
- Clicking a tab activates all tabs with same label
- Preference persists across page navigation
- Tabs linked by label, not position
