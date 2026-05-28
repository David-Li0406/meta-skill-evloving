---
name: ros2_package_scaffolder
description: Khởi tạo các gói tin ROS 2 (C++/Python) chuẩn kiến trúc Antigravity.
---
# ROS 2 PACKAGE SCAFFOLDER

## Mô Tả
Tự động sinh mã nguồn boilerplate tuân thủ nghiêm ngặt các quy tắc về cấu trúc thư mục, tệp cấu hình linter, và dependency injection.

## Mẫu Template (Templates)

### 1. Gói Ament CMake (C++)
Tạo cấu trúc cho component C++:
```bash
ros2 pkg create --build-type ament_cmake --dependencies rclcpp rclcpp_components std_msgs --node-name <node_name> <package_name>
```
**Hành động bổ sung của Agent:**
*   Thêm tệp `.clang-format` vào gốc gói tin.
*   Sửa đổi `CMakeLists.txt` để thêm khối `ament_lint_auto`.
*   Chuyển đổi `main.cpp` thành Component class structure (kế thừa `rclcpp::Node`, đăng ký macro).

### 2. Gói Ament Python
Tạo cấu trúc cho node Python:
```bash
ros2 pkg create --build-type ament_python --dependencies rclpy std_msgs --node-name <node_name> <package_name>
```
**Hành động bổ sung của Agent:**
*   Tạo tệp `setup.cfg` cấu hình flake8. **QUAN TRỌNG:** Phải giữ nguyên các section `[develop]` và `[install]` mặc định của ROS 2. Chỉ chèn thêm section `[flake8]` vào cuối file. Không được overwrite toàn bộ file.
*   Tạo thư mục `test/` với các bài test linter (`test_flake8.py`, `test_pep257.py`).
*   Đảm bảo `package.xml` chứa `<test_depend>ament_copyright</test_depend>`, `<test_depend>ament_flake8</test_depend>`.

### 3. Gói Interface
Tạo gói chứa định nghĩa tin nhắn tùy chỉnh:
```bash
ros2 pkg create --build-type ament_cmake antgravity_interfaces
```
**Hành động bổ sung của Agent:**
*   Xóa thư mục `src/` và `include/` mặc định (vì interface package không chứa code).
*   Tạo thư mục `msg/`, `srv/`, `action/`.
*   Cấu hình `CMakeLists.txt` tìm gói `rosidl_default_generators` và gọi `rosidl_generate_interfaces`.
*   Cấu hình `package.xml` thêm `rosidl_default_generators` (buildtool), `rosidl_default_runtime` (exec), và `member_of_group(rosidl_interface_packages)`.

