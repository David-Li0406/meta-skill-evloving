---
name: ros2_build_master
description: Quản lý quy trình biên dịch gói tin ROS 2 sử dụng Colcon với các cấu hình tối ưu.
---
# ROS 2 BUILD MASTER SKILL

## Mô Tả
Kỹ năng này cung cấp giao diện an toàn để Agent thực thi `colcon build`, đảm bảo các cờ (flags) quan trọng luôn được áp dụng để duy trì tính nhất quán của môi trường phát triển.

## Chức Năng (Capabilities)

### 1. Build Symlink (Phát triển nhanh)
Sử dụng `--symlink-install` để tạo liên kết tượng trưng từ thư mục cài đặt (`install/`) trỏ về mã nguồn (`src/`). Điều này cho phép thay đổi trong Python scripts, launch files, và file cấu hình (`.yaml`) có hiệu lực ngay lập tức mà không cần biên dịch lại.
*   **Command**: `colcon build --symlink-install`

### 2. Build Chọn Lọc (Tiết kiệm thời gian)
Chỉ biên dịch gói tin chỉ định và các phụ thuộc của nó, giúp giảm thời gian chờ đợi trong các workspace lớn.
*   **Command**: `colcon build --packages-select <package_name> --symlink-install`

### 3. Build Debug (Gỡ lỗi C++)
Biên dịch với thông tin gỡ lỗi (debug symbols) để sử dụng với GDB.
*   **Command**: `colcon build --cmake-args -DCMAKE_BUILD_TYPE=Debug --symlink-install`

### 4. Clean Workspace (Dọn dẹp)
Xóa các thư mục artifacts để khắc phục lỗi cache CMake hỏng.
*   **Command**: `rm -rf build/ install/ log/`

## Xử Lý Lỗi (Error Handling)
Nếu `colcon` trả về mã lỗi (non-zero exit code), Agent cần đọc tệp log tại `log/latest_build/events.log` hoặc phân tích stderr để xác định nguyên nhân:
*   **Missing dependency**: Gợi ý thêm vào `package.xml`.
*   **CMake Error**: Kiểm tra lại cú pháp `CMakeLists.txt`.
*   **Linker Error**: Kiểm tra việc thiếu `ament_target_dependencies`.
