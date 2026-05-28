---
name: ROS Code Documentation
description: Standardized procedure to generate developer API documentation for C++ libraries and Python modules.
---

# ROS Code Documentation Skill

Use this skill when asked to "document the API", "create developer docs", or "document the library" (as opposed to the Node/README).

## 1. Analysis Phase

### C++ Libraries
1.  **Locate Headers**: Look in `include/<package_name>/`.
2.  **Identify Classes**: Look for `class` definitions.
3.  **Analyze Interface**:
    -   Public methods.
    -   Key member variables (if public/protected).
    -   Type definitions (`struct`, `enum`, `typedef`).

### Python Modules
1.  **Locate Source**: Look in `src/<package_name>/` or `package_name/`.
2.  **Identify Classes**: Look for `class` definitions.
3.  **Analyze Interface**:
    -   `__init__` (Constructor).
    -   Public methods.

## 2. Generation Phase

1.  **Create `docs/` Directory**: If it doesn't exist, create it in the package root.
2.  **Create `docs/API.md`**: Use the template below.
3.  **Usage Examples**: Create a minimal code snippet showing how to instantiate and use the class.

### Template Usage
Read the template at `.agent/skills/ros_code_documentation/templates/API_template.md` and fill it in.
