---
name: tdd-ros2
description: ROS 2 Test-Driven Development workflow using gtest (C++) and pytest (Python). Enforces 80%+ coverage for critical nodes.
---

# ROS 2 TDD Workflow

## Core Principles
1.  **Tests FIRST**: Write `gtest` or `pytest` before implementation.
2.  **Red-Green-Refactor**: Test fail -> Code fix -> Optimize.
3.  **Integration**: Use `launch_testing` for node interaction tests.

## Workflow

### 1. Define Requirements (User Story)
"As a robot, I need to stop when obstacle < 0.5m."

### 2. Write Test Case
#### C++ (GTest)
```cpp
TEST_F(SafetyNodeTest, StopsOnObstacle) {
  node_->publish_scan(0.4); // Simulate 0.4m
  auto cmd = node_->get_cmd_vel();
  EXPECT_EQ(cmd.linear.x, 0.0);
}
```

#### Python (Pytest)
```python
def test_stop_on_obstacle(safety_node):
    safety_node.publish_scan(0.4)
    cmd = safety_node.get_cmd_vel()
    assert cmd.linear.x == 0.0
```

### 3. Run Test (Fail)
```bash
colcon test --packages-select my_safety_pkg
```

### 4. Implement Logic
Write minimal code in `safety_node` to pass the test.

### 5. Verify & Coverage
```bash
colcon test --packages-select my_safety_pkg
colcon test-result --all
```

## Tools
- **Unit**: `ament_cmake_gtest`, `ament_cmake_pytest`
- **Integration**: `launch_testing`, `osrf_pycommon`
- **Mocking**: `gmock` (C++), `unittest.mock` (Python)
