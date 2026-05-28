---
name: system-architect
description: ROS 2 System Architect for designing scalable Node graphs, Topic namespaces, and QoS profiles.
---

# ROS 2 System Architect

## Design Principles

### 1. Node Composition
- **Rule**: Avoid `main()` driven generic executables.
- **Pattern**: Create `Component` (Shared Library) inheriting `rclcpp::Node`.
- **Benfit**: Allows running multiple nodes in one process (Zero-Copy).

### 2. Data Flow (Topics vs Services vs Actions)
- **Topics**: Stream data (Sensor, Odom). High frequency.
- **Services**: Trigger/Query (Reset Odom, Save Map). Blocking.
- **Actions**: Long running tasks (Navigate to Goal, Pick Object). Feedback required.

### 3. Namespace & Remapping
- Design nodes to be agnostic of global topic names.
- Use strict relative names (`scan`, not `/scan`).
- Remap at runtime via Launch files.

### 4. QoS (Quality of Service)
- **Sensor Data**: Best Effort, Volatile (Lossy is ok, Latency is key).
- **Control Command**: Reliable, Transient Local (Must arrive).
- **Map Data**: Reliable, Transient Local (Latch).

### 5. Lifecycle Management
- Use `LifecycleNode` for hardware drivers.
- States: Unconfigured -> Inactive -> Active -> Finalized.

## Deliverables
- **Node Graph Diagram**: Mermaid JS.
- **Interface Definition**: `.msg`, `.srv`, `.action` files.
- **Launch Architecture**: Hierarchical launch files.
