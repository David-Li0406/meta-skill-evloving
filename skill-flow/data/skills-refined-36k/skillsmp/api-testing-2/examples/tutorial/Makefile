# API 接口测试教程 Makefile
# 使用方法: make help

.PHONY: help all clean 01 02 03 04 05 06 07 08 09

# 默认目标
help:
	@echo "API 接口测试教程"
	@echo ""
	@echo "使用方法: make [目标]"
	@echo ""
	@echo "入门级示例:"
	@echo "  make 01          - 基础请求 (15分钟)"
	@echo "  make 02          - 响应验证 (20分钟)"
	@echo "  make 03          - 认证授权 (20分钟)"
	@echo ""
	@echo "中级示例:"
	@echo "  make 04          - CRUD 测试 (25分钟)"
	@echo "  make 05          - 参数化测试 ⭐ (30分钟)"
	@echo "  make 06          - 数据驱动测试 ⭐ (30分钟)"
	@echo ""
	@echo "高级示例:"
	@echo "  make 07          - 契约测试 (30分钟)"
	@echo "  make 08          - 性能基准 (25分钟)"
	@echo "  make 09          - 综合套件 ⭐ (45分钟)"
	@echo ""
	@echo "其他命令:"
	@echo "  make all         - 运行所有示例"
	@echo "  make clean       - 清理生成文件"
	@echo "  make check       - 检查环境"
	@echo ""
	@echo "⭐ = 重点示例"

# 检查环境
check:
	@echo "检查 Python 环境..."
	@python --version
	@echo ""
	@echo "检查依赖..."
	@python -c "import pytest; print(f'pytest: {pytest.__version__}')"
	@python -c "import httpx; print(f'httpx: {httpx.__version__}')"
	@echo ""
	@echo "✓ 环境检查通过"

# 入门级示例
01 basic-request:
	@echo "=== 示例01: 基础请求 ==="
	cd beginner/01_basic_request && python test_basic.py

02 response-validation:
	@echo "=== 示例02: 响应验证 ==="
	cd beginner/02_response_validation && python -m pytest test_validation.py -v

03 auth:
	@echo "=== 示例03: 认证授权 ==="
	cd beginner/03_authentication && python -m pytest test_auth.py -v

# 中级示例
04 crud:
	@echo "=== 示例04: CRUD 测试 ==="
	cd intermediate/04_crud_testing && python -m pytest test_crud.py -v

05 parametrize:
	@echo "=== 示例05: 参数化测试 ⭐ ==="
	cd intermediate/05_parametrize && python -m pytest test_parametrize.py -v

06 data-driven:
	@echo "=== 示例06: 数据驱动测试 ⭐ ==="
	cd intermediate/06_data_driven && python -m pytest test_data_driven.py -v

# 高级示例
07 contract:
	@echo "=== 示例07: 契约测试 ==="
	cd advanced/07_contract_testing && python -m pytest test_contract.py -v

08 performance:
	@echo "=== 示例08: 性能基准 ==="
	cd advanced/08_performance && python -m pytest test_performance.py -v

09 comprehensive:
	@echo "=== 示例09: 综合套件 ⭐ ==="
	cd advanced/09_comprehensive && python -m pytest . -v

# 运行所有示例
all: 01 02 03 04 05 06 07 08 09
	@echo ""
	@echo "✓ 所有示例运行完成!"

# 清理
clean:
	@echo "清理生成文件..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "report.html" -delete 2>/dev/null || true
	@echo "✓ 清理完成"
