---
name: ROS Documentation
description: Standardized procedure to document ROS 2 packages using the UNH Marine Autonomy format.
---

# ROS Documentation Skill

Use this skill when asked to "document a package", "update the README", or "improve documentation" for a ROS 2 package.

## 1. Analysis Phase
Before writing, you must understand the package.

1.  **Read `package.xml`**:
    -   Identify `name`, `description`, `maintainer` (if any), and `license`.
    -   List dependencies (`<depend>`, `<exec_depend>`).

2.  **Analyze Nodes** (Python/C++):
    -   Find entry points in `CMakeLists.txt` (executables) or `setup.py` (`console_scripts`).
    -   For each node source file:
        -   **Subscribers**: Look for `create_subscription` / `subscribe`. Note topic name and message type.
        -   **Publishers**: Look for `create_publisher` / `advertise`. Note topic name and message type.
        -   **Parameters**: Look for `declare_parameter`. Note name, default value, and description.
        -   **Services**: Look for `create_service` / `create_client`

3.  **Analyze Launch Files**:
    -   Look in `launch/` directory.
    -   Identify arguments (`DeclareLaunchArgument`).

## 2. Generation Phase
Create or update the `README.md` in the package root using the template below.

-   **Do not** remove existing custom sections if they provide specific context (e.g., "Theory of Operation").
-   **Do** standardize the "Nodes", "API", and "Usage" sections.

### Template Usage
Read the template at `.agent/skills/ros_documentation/templates/README_template.md` and fill it in.
