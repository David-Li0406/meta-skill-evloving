# Web应用测试教程 - Makefile
# 便捷运行所有tutorial示例

.PHONY: help all clean 01 02 03 04 05 06 07 08 09 \
        static-html discovery screenshots form dynamic console spa server ecommerce

# 默认目标：显示帮助
help:
	@echo "========================================="
	@echo "Web应用测试教程 - 可用命令"
	@echo "========================================="
	@echo ""
	@echo "🟢 入门级 (Beginner)"
	@echo "  make 01 或 make static-html    - 静态HTML测试 (15分钟)"
	@echo "  make 02 或 make discovery      - 元素发现 (20分钟)"
	@echo "  make 03 或 make screenshots    - 截图测试 (15分钟)"
	@echo ""
	@echo "🟡 中级 (Intermediate)"
	@echo "  make 04 或 make form           - 表单自动化 (25分钟)"
	@echo "  make 05 或 make dynamic        - 动态内容测试⭐ (30分钟)"
	@echo "  make 06 或 make console        - 控制台调试 (20分钟)"
	@echo ""
	@echo "🔴 高级 (Advanced)"
	@echo "  make 07 或 make spa            - SPA测试 (30分钟)"
	@echo "  make 08 或 make server         - 服务器集成 (35分钟)"
	@echo "  make 09 或 make ecommerce      - 综合测试套件⭐ (45分钟)"
	@echo ""
	@echo "📦 批量操作"
	@echo "  make all                       - 按顺序运行所有示例"
	@echo "  make clean                     - 清理生成的文件"
	@echo ""
	@echo "💡 提示："
	@echo "  - 建议按数字顺序从01开始学习"
	@echo "  - ⭐标记的示例为关键重点"
	@echo "  - 示例08需要先安装Flask: pip install flask"
	@echo ""

# ========================================
# 🟢 入门级示例
# ========================================

# 示例01: 静态HTML测试
01 static-html:
	@echo "========================================="
	@echo "🟢 示例01: 静态HTML测试"
	@echo "========================================="
	@echo "学习目标: 加载本地HTML文件并提取内容"
	@echo "预计时间: 15分钟"
	@echo ""
	@cd beginner/01_static_html && python test_static.py
	@echo ""
	@echo "✅ 示例01完成！"
	@echo ""

# 示例02: 元素发现
02 discovery:
	@echo "========================================="
	@echo "🟢 示例02: 元素发现"
	@echo "========================================="
	@echo "学习目标: 使用不同选择器发现页面元素"
	@echo "预计时间: 20分钟"
	@echo ""
	@cd beginner/02_element_discovery && python test_discovery.py
	@echo ""
	@echo "✅ 示例02完成！"
	@echo ""

# 示例03: 截图测试
03 screenshots:
	@echo "========================================="
	@echo "🟢 示例03: 截图测试"
	@echo "========================================="
	@echo "学习目标: 捕获全页面和元素截图"
	@echo "预计时间: 15分钟"
	@echo ""
	@cd beginner/03_screenshots && python test_screenshots.py
	@echo ""
	@echo "📸 截图已保存到: beginner/03_screenshots/screenshots/"
	@echo "✅ 示例03完成！"
	@echo ""

# ========================================
# 🟡 中级示例
# ========================================

# 示例04: 表单自动化
04 form:
	@echo "========================================="
	@echo "🟡 示例04: 表单自动化"
	@echo "========================================="
	@echo "学习目标: 填写表单、提交并验证"
	@echo "预计时间: 25分钟"
	@echo ""
	@cd intermediate/04_form_automation && python test_form.py
	@echo ""
	@echo "📸 截图已保存到: intermediate/04_form_automation/screenshots/"
	@echo "✅ 示例04完成！"
	@echo ""

# 示例05: 动态内容测试 ⭐
05 dynamic:
	@echo "========================================="
	@echo "🟡 示例05: 动态内容测试 ⭐ 重要"
	@echo "========================================="
	@echo "学习目标: 处理JavaScript渲染的内容和等待策略"
	@echo "预计时间: 30分钟"
	@echo ""
	@cd intermediate/05_dynamic_content && python test_dynamic.py
	@echo ""
	@echo "⚠️  关键知识点: 始终在动态应用加载后使用 wait_for_load_state('networkidle')"
	@echo "✅ 示例05完成！"
	@echo ""

# 示例06: 控制台调试
06 console:
	@echo "========================================="
	@echo "🟡 示例06: 控制台调试"
	@echo "========================================="
	@echo "学习目标: 捕获和分析浏览器控制台日志"
	@echo "预计时间: 20分钟"
	@echo ""
	@cd intermediate/06_console_debugging && python test_console.py
	@echo ""
	@echo "📝 日志已保存到: intermediate/06_console_debugging/logs/"
	@echo "✅ 示例06完成！"
	@echo ""

# ========================================
# 🔴 高级示例
# ========================================

# 示例07: SPA测试
07 spa:
	@echo "========================================="
	@echo "🔴 示例07: SPA (单页应用) 测试"
	@echo "========================================="
	@echo "学习目标: 测试客户端路由和状态变化"
	@echo "预计时间: 30分钟"
	@echo ""
	@cd advanced/07_spa_testing && python test_spa.py
	@echo ""
	@echo "✅ 示例07完成！"
	@echo ""

# 示例08: 服务器集成测试
08 server:
	@echo "========================================="
	@echo "🔴 示例08: 服务器集成测试"
	@echo "========================================="
	@echo "学习目标: 测试全栈应用 (前端+后端)"
	@echo "预计时间: 35分钟"
	@echo ""
	@echo "⚠️  此示例需要Flask: pip install flask"
	@echo ""
	@echo "启动方式1 (推荐): 使用helper脚本自动管理服务器"
	@cd advanced/08_server_integration && \
		python ../../../../scripts/with_server.py \
		--server "python flask_app.py" \
		--port 5000 \
		-- python test_with_server.py
	@echo ""
	@echo "✅ 示例08完成！"
	@echo ""
	@echo "💡 提示: 也可以手动启动Flask (python flask_app.py)，"
	@echo "         然后在另一个终端运行测试脚本"
	@echo ""

# 示例09: 综合测试套件 ⭐
09 ecommerce:
	@echo "========================================="
	@echo "🔴 示例09: 综合测试套件 ⭐ 实战项目"
	@echo "========================================="
	@echo "学习目标: 完整的电商应用测试，综合运用所有技巧"
	@echo "预计时间: 45分钟"
	@echo ""
	@cd advanced/09_comprehensive && python test_suite.py
	@echo ""
	@echo "📸 截图已保存到: advanced/09_comprehensive/screenshots/"
	@echo "✅ 示例09完成！恭喜你完成了整个教程！🎉"
	@echo ""

# ========================================
# 批量操作
# ========================================

# 运行所有示例（按顺序）
all:
	@echo "========================================="
	@echo "开始运行所有9个示例"
	@echo "预计总时间: ~4小时"
	@echo "========================================="
	@echo ""
	@$(MAKE) 01
	@$(MAKE) 02
	@$(MAKE) 03
	@$(MAKE) 04
	@$(MAKE) 05
	@$(MAKE) 06
	@$(MAKE) 07
	@$(MAKE) 08
	@$(MAKE) 09
	@echo ""
	@echo "========================================="
	@echo "🎉 恭喜！所有示例运行完成！"
	@echo "========================================="
	@echo ""
	@echo "你已经掌握了："
	@echo "  ✅ 静态HTML测试"
	@echo "  ✅ 元素发现和选择器"
	@echo "  ✅ 截图和视觉验证"
	@echo "  ✅ 表单自动化"
	@echo "  ✅ 动态内容处理"
	@echo "  ✅ 控制台调试"
	@echo "  ✅ SPA测试"
	@echo "  ✅ 服务器集成测试"
	@echo "  ✅ 综合测试套件编写"
	@echo ""
	@echo "下一步建议："
	@echo "  1. 完成每个示例的练习题"
	@echo "  2. 将这些技术应用到你自己的项目中"
	@echo "  3. 阅读 Playwright 官方文档深入学习"
	@echo ""

# 清理生成的文件
clean:
	@echo "清理生成的文件..."
	@rm -rf beginner/03_screenshots/screenshots/ 2>/dev/null || true
	@rm -rf intermediate/04_form_automation/screenshots/ 2>/dev/null || true
	@rm -rf intermediate/06_console_debugging/logs/ 2>/dev/null || true
	@rm -rf advanced/09_comprehensive/screenshots/ 2>/dev/null || true
	@echo "✅ 清理完成！"
	@echo ""
	@echo "已删除的目录："
	@echo "  - beginner/03_screenshots/screenshots/"
	@echo "  - intermediate/04_form_automation/screenshots/"
	@echo "  - intermediate/06_console_debugging/logs/"
	@echo "  - advanced/09_comprehensive/screenshots/"
	@echo ""
