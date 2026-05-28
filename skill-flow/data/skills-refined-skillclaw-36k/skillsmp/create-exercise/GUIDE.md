# AI Agent Guide for Creating Educational Programming Exercises

## Overview

This document provides comprehensive instructions for AI agents to create consistent, high-quality educational programming exercises. The exercises follow a specific template designed for clarity, progressive disclosure, and beginner-friendliness.

## Core Design Philosophy

### Visual Hierarchy Principle

Exercises use a **three-layer information architecture**:

1. **Primary Layer** (Bold): The essential flow - what students MUST follow
2. **Secondary Layer** (Blockquotes): Supporting information - available but visually receded
3. **Tertiary Layer** (Optional sections): Enrichment content for advanced learners

This hierarchy ensures beginners can follow the exercise without being overwhelmed, while still having access to deeper explanations when needed.

### Key Design Rules

1. **No exercise numbers** - Makes maintenance easier
2. **No cross-references** - Each exercise stands alone
3. **Blockquotes for all supplementary info** - Creates visual recession
4. **Bold action verbs** - Guides the eye through steps
5. **Full file paths** - Always relative to project root
6. **Consistent icon placement** - Icons before bold text in blockquotes

## Exercise Template Structure

### 1. Title Section

```markdown
# [Descriptive Exercise Title]
```

- No exercise numbers
- Clear, action-oriented title
- Describes what will be built

### 2. Goal Section

```markdown
## Goal

Build [specific feature] to enable [business capability] in your application.

> **What you'll learn:**
>
> - How to implement [concept/pattern]
> - When to use [technique] in real applications
> - Best practices for [specific area]
```

### 3. Prerequisites Section

```markdown
## Prerequisites

> **Before starting, ensure you have:**
>
> - ✓ Development environment with [tools/frameworks]
> - ✓ Basic understanding of [concept]
> - ✓ [Any specific setup requirement]
```

### 4. Exercise Steps Section

```markdown
## Exercise Steps

### Overview

1. **[Action Title for Step 1]**
2. **[Action Title for Step 2]**
3. **[Action Title for Step 3]**
4. **[Action Title for Step 4]**
5. **Test Your Implementation**
```

### 5. Individual Step Structure

```markdown
### **Step N:** [Clear Action Title]

[Explanatory paragraph: What this step accomplishes, why it's important,
how it fits into the larger picture, and what problem it solves. Be
educational here - help students understand the "why" not just the "what".]

1. **Navigate to** the `[folder]` directory

2. **Create a new file** named `[filename.ext]`

3. **Add the following code:**

   > `src/Path/To/File.ext`

   ```language
   namespace YourApp.Models;

   public class ExampleClass
   {
       // Comments explain purpose
       public string Property { get; set; }
   }
   ```

> ℹ **Concept Deep Dive**
>
> [Explanation of the concept, design pattern, or architectural decision.
> Why this approach over alternatives. Real-world application.]
>
> ⚠ **Common Mistakes**
>
> - [Specific mistake] will result in `[error message]`
> - Make sure [important detail]
> - Don't confuse [concept A] with [concept B]
>
> ✓ **Quick check:** [How to verify this step worked]

```markdown
### 6. Test Step Structure

```markdown
### **Step 5:** Test Your Implementation

[Explain the testing approach and why systematic testing matters.]

1\. **Run the application:**

   ```bash
   dotnet run
   ```

2\. **Navigate to:** `http://localhost:5000/[endpoint]`

3\. **Test the happy path:**

   - [Specific test action]
   - [Expected result]

4\. **Test validation:**

   - [Edge case test]
   - [Expected behavior]

5\. **Test edge cases:**

   - [Boundary test]
   - [Error handling verification]

> ✓ **Success indicators:**
>
> - [Observable success criterion]
> - [Another success criterion]
>
> ✓ **Final verification checklist:**
>
> - ☐ All files created in correct locations
> - ☐ Application compiles without errors
> - ☐ Feature works with test data
> - ☐ [Exercise-specific verification]

```markdown

### 7. Remaining Sections

```markdown
## Common Issues

> **If you encounter problems:**
>
> **[Error type]:** [Solution]
>
> **[Another error]:** [Another solution]
>
> **Still stuck?** [General debugging advice]

## Summary

You've successfully implemented [feature/pattern] which:

- ✓ Enables [business capability]
- ✓ Follows [design pattern] for better [quality attribute]
- ✓ Prepares your app for [future enhancement]

> **Key takeaway:** [Most important concept] is essential because
> [real-world application]. You'll use this pattern whenever [scenario].

## Going Deeper (Optional)

> **Want to explore more?**
>
> - Try adding [enhancement]
> - Research how [concept] works under the hood
> - Implement [related pattern] for comparison
> - Add unit tests for your new components

## Done! 🎉

Great job! You've learned how to [core skill] and can now [capability gained].
This foundation will help you build more [quality attribute] applications.
```

## Markdown Linting Rules to Follow

To ensure clean, consistent markdown that passes linting, follow these rules:

### Critical Linting Rules

1. **MD028 - No blank lines in blockquotes**: Keep blockquotes continuous for related content
2. **MD031 - Blank lines around code blocks**: Always surround code blocks with blank lines
3. **MD032 - Blank lines around lists**: Lists need blank lines before and after
4. **MD040 - Language for code blocks**: Always specify language (csharp, bash, markdown, etc.)
5. **MD029 - Sequential numbering**: Use 1, 2, 3 for ordered lists, not custom numbers
6. **MD047 - Single trailing newline**: End files with exactly one newline

### Common Language Identifiers for Code Blocks

- `csharp` - C# code
- `bash` - Shell commands
- `html` - HTML/Razor views
- `json` - JSON configuration
- `markdown` - Markdown examples
- `yaml` - YAML files
- `javascript` or `js` - JavaScript
- `css` - Stylesheets
- `sql` - Database queries
- `xml` - XML configuration

### Examples of Correct Formatting

For blockquotes (MD028):

```markdown
> ℹ **Concept Deep Dive**
>
> Explanation here...
>
> ⚠ **Common Mistakes**
>
> - Mistake here...
```

For code blocks (MD031, MD040):

```markdown
Some text here.

```csharp
// Code with language specified
```

More text here.

```markdown

For lists (MD032):

```markdown
Paragraph text.

- List item 1
- List item 2

Another paragraph.
```

## Formatting Rules

### Code Blocks

1. **Always include file path** as a blockquote above the code block:

   ```markdown
   > `src/Controllers/ExampleController.cs`
   ```

2. **Properly indent** code blocks in numbered lists (3 spaces):

   ```markdown
   3. **Add the following code:**

      > `src/Models/Example.cs`

      ```csharp
      // Code here
      ```

   ```markdown

3. **Include meaningful comments** in code to explain key concepts

### Blockquote Usage

All supplementary information goes in blockquotes:

- `> ℹ **Concept Deep Dive**` - For conceptual explanations
- `> ⚠ **Common Mistakes**` - For warnings and pitfalls
- `> ✓ **Quick check:**` - For verification points
- `> ✓ **Success indicators:**` - For test success criteria
- `> **What you'll learn:**` - For learning objectives
- `> **Before starting:**` - For prerequisites

**Important Linting Rule (MD028)**: When using multiple blockquotes in sequence, you have two options:

Option 1 - **Single continuous blockquote** (recommended for related content):

```markdown
> ℹ **Concept Deep Dive**
>
> This is the explanation...
>
> ⚠ **Common Mistakes**
>
> - Mistake one...
>
> ✓ **Quick check:** Verification point
```

Option 2 - **Separate blockquotes with regular text** (for unrelated content):

```markdown
> ℹ **Concept Deep Dive**
>
> This is the explanation...

Regular text or step instruction here.

> ⚠ **Common Mistakes**
>
> - Mistake one...
```

**Avoid**: Having just a blank line between blockquotes (causes MD028 error)

### Nested Markdown Code Examples

When showing markdown code examples inside markdown files:

**MD029 Solution**: Use escaped numbers in ordered lists to prevent linting errors:

```markdown
1\. **First step**
2\. **Second step**
3\. **Third step**
```

This prevents the linter from parsing example content as actual lists while displaying correctly.

**Acceptable Warnings in Examples:**

- **MD007** (ul-indent): Indented lists in code examples are intentional
- These show proper formatting for actual exercises

### Bold Text Usage

- **Step titles**: `### **Step 1:** [Title]`
- **Action verbs**: `**Navigate to**`, `**Create**`, `**Add**`, `**Open**`
- **Key concepts** in blockquotes: `> ℹ **Concept Deep Dive**`

### Icon Usage

Place icons consistently BEFORE bold text:

- ℹ for information
- ⚠ for warnings
- ✓ for success/verification
- ☐ for checklist items

## Writing Style Guidelines

### Step Introductions

Each step should begin with a full paragraph that:

1. Explains what will be accomplished
2. Explains why this step matters
3. Connects to the bigger picture
4. Mentions any important concepts

### Language Style

- **Active voice**: "Create a file" not "A file should be created"
- **Direct instructions**: "Navigate to" not "You should navigate to"
- **Clear and concise**: Avoid unnecessary words
- **Educational tone**: Explain the why, not just the how
- **Encouraging**: Positive reinforcement, especially in "Done!" section

### Common Patterns to Use

1. **File creation pattern**:

   ```markdown
   1. **Navigate to** the `[folder]` directory
   2. **Create a new file** named `[filename]`
   3. **Add the following code:**
   ```

2. **File modification pattern**:

   ```markdown
   1. **Open** the existing file at `[path]`
   2. **Locate** the [section] (around line [X])
   3. **Replace/Add** the following code:
   ```

3. **Configuration pattern**:

   ```markdown
   1. **Open** `Program.cs` in the project root
   2. **Add** the service registration after [location]:
   ```

## Complete Example

Here's a condensed example showing all elements:

```markdown
# Implement Repository Pattern

## Goal

Build a data access layer to separate database logic from business logic in your application.

> **What you'll learn:**
>
> - How to implement the Repository pattern
> - When to use abstraction for data access
> - Best practices for testable code

## Prerequisites

> **Before starting, ensure you have:**
>
> - ✓ Development environment with .NET 8.0+
> - ✓ Basic understanding of interfaces
> - ✓ Entity Framework Core installed

## Exercise Steps

### Overview

1. **Create the Repository Interface**
2. **Implement the Repository**
3. **Register with Dependency Injection**
4. **Use in Controller**
5. **Test Your Implementation**

### **Step 1:** Create the Repository Interface

Define a contract for data access operations that keeps your code flexible and testable.
This abstraction allows you to swap implementations without changing dependent code.

1. **Navigate to** the `Repositories` directory (create if needed)

2. **Create a new file** named `IProductRepository.cs`

3. **Add the following code:**

   > `src/Repositories/IProductRepository.cs`

   ```csharp
   namespace YourApp.Repositories;

   public interface IProductRepository
   {
       Task<Product> GetByIdAsync(int id);
       Task<List<Product>> GetAllAsync();
       Task AddAsync(Product product);
       Task UpdateAsync(Product product);
       Task DeleteAsync(int id);
   }
   ```

> ℹ **Concept Deep Dive**
>
> Interfaces define contracts without implementation. This follows the Dependency
> Inversion Principle - depend on abstractions, not concretions. In production,
> this enables unit testing with mocks and easy swapping of data stores.
>
> ⚠ **Common Mistakes**
>
> - Forgetting the `async` keyword will cause compilation errors
> - Make sure namespace matches your project structure
> - Don't include implementation details in interfaces
>
> ✓ **Quick check:** File created at correct location, no compilation errors

[Continue with remaining steps...]

## Done! 🎉

Excellent work! You've implemented the Repository pattern and learned how
abstraction improves code maintainability. This foundation will help you
build more testable and flexible applications.

```markdown

## Quality Checklist for AI Agents

Before submitting an exercise, verify:

### Structure
- ☐ No exercise numbers in title
- ☐ No references to other exercises
- ☐ All sections present and in order
- ☐ Overview section lists all steps
- ☐ Each step has explanatory introduction paragraph

### Formatting
- ☐ All supplementary info in blockquotes
- ☐ Icons placed before bold text
- ☐ Code blocks properly indented in lists
- ☐ Full file paths shown as `> src/Path/To/File.ext`
- ☐ Bold action verbs in instructions

### Content
- ☐ Clear learning objectives
- ☐ Realistic prerequisite checks
- ☐ Explanations for design decisions
- ☐ Common mistakes addressed
- ☐ Verification points after each step
- ☐ Comprehensive testing section
- ☐ Troubleshooting guidance

### Readability
- ☐ Can follow exercise by reading only bold text
- ☐ Supplementary info doesn't interrupt flow
- ☐ Code is complete and copyable
- ☐ Clear success criteria

## Special Instructions for AI Agents

1. **Always use the exact template structure** - Don't improvise or reorganize sections
2. **Maintain visual hierarchy** - Primary content bold, secondary in blockquotes
3. **Keep exercises standalone** - No dependencies on other exercises
4. **Focus on education** - Explain why, not just how
5. **Test your output** - Ensure the exercise can be followed step-by-step
6. **Use consistent voice** - Direct, encouraging, educational
7. **Include all sections** - Even if brief, don't skip any template sections

## Final Notes

This template system is designed to:
- **Support beginners** without overwhelming them
- **Provide depth** for those ready to learn more
- **Maintain consistency** across all exercises
- **Enable easy updates** without breaking references
- **Create scannable content** that respects cognitive load

When creating exercises, remember: The student should be able to complete the exercise by following just the bold text, but have all the context they need available in the grayed-out blockquotes when they're ready for it.

The goal is **progressive disclosure** - showing just enough information at the right time, while keeping the full depth available for those who want it.
