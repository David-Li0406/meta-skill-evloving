---
name: ros2-build-resolver
description: Specialist in fixing Colcon build failures, CMake linking errors, and dependency issues.
---

# ROS 2 Build Resolver

## Resolution Strategy

### 1. Analyze Failure Type
- **CMake Error**: `find_package` missing, linking error, include path invalid.
- **Python Error**: `ModuleNotFoundError`, `setup.py` entry point missing.
- **Dependency Error**: `rosdep` missing key, `package.xml` XML invalid.
- **Interface Error**: `.msg` generation failed, visibility macro missing.

### 2. Common Fixes

#### CMake Linking
**Error**: `undefined reference to 'rclcpp::Node::Node'`
**Fix**: Ensure `ament_target_dependencies` includes `rclcpp`.
```cmake
ament_target_dependencies(my_node rclcpp)
```

#### Python Module Missing
**Error**: `ModuleNotFoundError: No module named 'my_pkg'`
**Fix**: Check `setup.py` packages list or `symlink-install`.
```python
packages=find_packages(exclude=['test']),
```

#### Interface Visibility (C++)
**Error**: `__declspec(dllimport)` or visibility attribute missing.
**Fix**: Ensure `rosidl_default_generators` is in `CMakeLists.txt` and `package.xml`.

### 3. Verification Command
```bash
colcon build --packages-select <failed_package> --symlink-install
```

### 4. Clean Build (Last Resort)
```bash
rm -rf build/ install/ log/
colcon build --symlink-install
```
