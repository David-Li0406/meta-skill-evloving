---
name: Ozi Script Development Kit
description: Kiến thức và patterns để phát triển Ozi Script
---

# Ozi Script Development Skill

## Tổng quan dự án

**Ozi Script** là bộ công cụ quản lý VPS bằng CLI cho Debian 12+, với giao diện tiếng Việt.

### Thông tin cơ bản
- **CLI command:** `ozi`
- **Thư mục cài đặt:** `/opt/oziscript`
- **Config:** `/etc/oziscript/`
- **Logs:** `/var/log/oziscript/`
- **Ngôn ngữ:** Bash script
- **OS:** Debian 12 (Bookworm), Debian 13 (Trixie)

### Cấu trúc source code
```
packages/oziDebianScript/
├── ozi                     # CLI chính
├── install.sh              # Script cài đặt
├── core/                   # Core libraries
│   ├── helpers.sh          # Hàm tiện ích
│   ├── colors.sh           # Màu terminal
│   ├── config.sh           # Quản lý config
│   ├── menu.sh             # Menu system
│   └── os.sh               # OS detection
├── modules/                # Các module chức năng
│   ├── system/             # Thông tin hệ thống
│   ├── security/           # Bảo mật
│   ├── stack/              # PHP, Nginx, DB...
│   ├── site/               # Quản lý site
│   ├── database/           # Database tools
│   ├── backup/             # Backup/restore
│   └── deploy/             # Deploy scripts
├── templates/              # Template configs
│   └── nginx/              # Nginx templates
└── lang/                   # Ngôn ngữ
    └── vi.sh               # Tiếng Việt
```

## Coding Standards

### 1. File Header
Mỗi file script phải có header:
```bash
#!/bin/bash
#================================================================
# Ozi Script - Module: [Tên Module]
# Mô tả: [Mô tả ngắn]
# Tác giả: Ozi DevOps
# Phiên bản: 1.0.0
#================================================================
```

### 2. Strict Mode
Luôn bật strict mode ở đầu script:
```bash
set -euo pipefail
IFS=$'\n\t'
```

### 3. Màu sắc (từ core/colors.sh)
```bash
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'
```

### 4. Print Functions (từ core/helpers.sh)
```bash
print_header "Tiêu đề"          # Header đẹp với border
print_success "Thành công"      # ✓ màu xanh
print_error "Lỗi"               # ✗ màu đỏ
print_warning "Cảnh báo"        # ⚠ màu vàng
print_info "Thông tin"          # ℹ màu xanh dương
```

### 5. Confirm với user
```bash
if confirm "Bạn có muốn tiếp tục?"; then
    # User chọn Yes
else
    # User chọn No
fi
```

### 6. Kiểm tra root
```bash
require_root   # Exit nếu không phải root
```

### 7. Kiểm tra Debian
```bash
check_debian   # Exit nếu không phải Debian 12+
```

### 8. Kiểm tra package đã cài
```bash
if is_installed "nginx"; then
    print_info "Nginx đã được cài đặt"
fi
```

## Command Structure

CLI sử dụng dạng subcommand:
```bash
ozi {category} {action} [options]
```

Ví dụ:
- `ozi system info`
- `ozi php install 8.3`
- `ozi site create laravel mysite.com`
- `ozi backup create --db-only`

## Module Template

```bash
#!/bin/bash
#================================================================
# Ozi Script - Module: Example
# Mô tả: Module mẫu
#================================================================

set -euo pipefail

# Load core
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../../core/helpers.sh"
source "$SCRIPT_DIR/../../core/colors.sh"

#================================================================
# CONFIGURATION
#================================================================
MODULE_NAME="example"
MODULE_VERSION="1.0.0"

#================================================================
# FUNCTIONS
#================================================================
cmd_list() {
    print_header "Danh sách"
    # Logic
}

cmd_create() {
    local name="${1:-}"
    if [[ -z "$name" ]]; then
        print_error "Vui lòng nhập tên"
        exit 1
    fi
    # Logic
}

show_help() {
    cat << 'EOF'
Sử dụng: ozi example {command} [options]

Commands:
    list        Liệt kê
    create      Tạo mới

Ví dụ:
    ozi example list
    ozi example create my-example
EOF
}

#================================================================
# MAIN
#================================================================
main() {
    local cmd="${1:-help}"
    shift || true
    
    case "$cmd" in
        list)
            cmd_list "$@"
            ;;
        create)
            cmd_create "$@"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Lệnh không hợp lệ: $cmd"
            show_help
            exit 1
            ;;
    esac
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
    main "$@"
fi
```

## Nginx Template Variables

Khi tạo nginx config, dùng các placeholder:
- `{domain}` - Domain name
- `{root}` - Document root
- `{php_version}` - PHP version (8.3)
- `{port}` - Port cho Octane/Node.js
- `{user}` - User name

## Testing

1. Test trên VPS Debian 13 thật (đã có sẵn)
2. Chạy từng lệnh và verify output
3. Kiểm tra log tại `/var/log/oziscript/`
4. Test rollback nếu có lỗi

## Common Patterns

### Cài package với apt
```bash
install_package() {
    local pkg="$1"
    if ! is_installed "$pkg"; then
        print_info "Đang cài đặt $pkg..."
        apt-get install -y -qq "$pkg" || error_exit "Không thể cài $pkg"
        print_success "$pkg đã được cài đặt"
    else
        print_warning "$pkg đã được cài trước đó"
    fi
}
```

### Add repo external
```bash
add_sury_php_repo() {
    if [[ ! -f /etc/apt/sources.list.d/php.list ]]; then
        print_info "Thêm Sury PHP repository..."
        curl -sSLo /tmp/debsuryorg.deb https://packages.sury.org/php/apt.gpg
        apt-get install -y /tmp/debsuryorg.deb
        echo "deb [signed-by=/usr/share/keyrings/deb.sury.org-php.gpg] https://packages.sury.org/php/ $(lsb_release -sc) main" \
            > /etc/apt/sources.list.d/php.list
        apt-get update -qq
    fi
}
```

### Service management
```bash
service_restart() {
    local service="$1"
    if systemctl is-active --quiet "$service"; then
        systemctl restart "$service"
        print_success "$service đã được khởi động lại"
    else
        systemctl start "$service"
        print_success "$service đã được bật"
    fi
}
```
