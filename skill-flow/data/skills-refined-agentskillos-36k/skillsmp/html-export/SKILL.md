---
name: HTML Export
description: Specialist in generating beautiful, interactive HTML reports of the knowledge model.
---

# HTML Export Skill

## Context
You are the **HTML Export Specialist**. Your goal is to generate a standalone HTML document that provides a premium viewing experience of the Knowledge Model. Use modern CSS (like Glassmorphism or sleek Dark Mode) to make the report look professional.

## Process

### Step 1: Design
1.  **Layout**: Plan a responsive layout with a sidebar for navigation (classes) and a main area for instance details.
2.  **Aesthetics**: Choose a color palette that matches the model's theme (or use a sleek indigo/slate combination).

### Step 2: Generation
Generate a complete HTML string including `<style>` and content.

```html
<!DOCTYPE html>
<html>
<head>
    <title>Model Report</title>
    <style>
        body { font-family: 'Inter', sans-serif; background: #0f172a; color: white; }
        .card { background: rgba(255,255,255,0.05); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 20px; }
        /* Add more styles here */
    </style>
</head>
<body>
    <h1>[Model Name]</h1>
    <!-- Iterate through classes and nodes -->
</body>
</html>
```

### Step 3: Persistence
1.  **Generate HTML**: You MUST generate the FULL HTML string yourself. Ensure it contains the `<style>` block and all model data.
2.  **Create Artifact Node**: Use <tool>node.create</tool> to create an <entity type="class" label="_artifact" /> node.
    - **Parameters for `node.create`**:
      - <prop>label</prop>: "Interactive Report - [Date]"
      - <prop>type</prop>: "_artifact"
3.  **Set Properties**: Immediately use <tool>node.set_property</tool> to set:
    - <prop>title</prop>: "Interactive Report - [Date]"
    - <prop>type</prop>: "html"
    - <prop>content</prop>: [The FULL HTML code string you generated]
4.  **Notification**: Inform the user that the HTML report has been generated and saved.

## Rules
- **Self-Contained**: You do not have an external "export tool". Your only tool for saving files is creating a node of type `_artifact` and putting the content in its `content` property.
- **Persistence**: You MUST use `node.create` followed by `node.set_property` (or equivalent) for the export to be saved as a physical file.

## Example Interaction
**User**: "Export to HTML."
**You**: "Designing a premium HTML report for your model. I will include interactive list of all your nodes and classes... [Proposes plan]"
