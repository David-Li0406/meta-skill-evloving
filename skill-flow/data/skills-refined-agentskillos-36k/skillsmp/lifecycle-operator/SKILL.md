---
name: lifecycle_operator
description: Điều phối và kiểm tra chuyển đổi trạng thái của Lifecycle Nodes.
---
# LIFECYCLE OPERATOR SKILL

## Mô Tả
Tương tác với các dịch vụ quản lý vòng đời (`/node_name/change_state`, `/node_name/get_state`) để đảm bảo node hoạt động đúng theo máy trạng thái quy định.

## Quy Trình Chuyển Đổi (Transition Flow)
Agent thực hiện tuần tự các bước sau để "bring-up" một node quản lý:

1.  **Kiểm tra trạng thái:** `ros2 lifecycle get <node_name>` (Mong đợi: `Unconfigured`).
2.  **Cấu hình (Configure):**
    *   Command: `ros2 lifecycle set <node_name> configure`
    *   Hành động Node: Cấp phát bộ nhớ, đọc tham số, thiết lập kết nối phần cứng (nhưng chưa kích hoạt).
    *   Trạng thái đích: `Inactive`.
3.  **Kích hoạt (Activate):**
    *   Command: `ros2 lifecycle set <node_name> activate`
    *   Hành động Node: Bắt đầu publish dữ liệu, xử lý callback.
    *   Trạng thái đích: `Active`.
4.  **Vô hiệu hóa (Deactivate):**
    *   Command: `ros2 lifecycle set <node_name> deactivate`
    *   Hành động Node: Ngừng publish, giữ nguyên cấu hình.
    *   Trạng thái đích: `Inactive`.
5.  **Dọn dẹp (Cleanup):**
    *   Command: `ros2 lifecycle set <node_name> cleanup`
    *   Hành động Node: Giải phóng bộ nhớ, reset biến.
    *   Trạng thái đích: `Unconfigured`.
6.  **Tắt (Shutdown):**
    *   Command: `ros2 lifecycle set <node_name> shutdown`
    *   Trạng thái đích: `Finalized`.
