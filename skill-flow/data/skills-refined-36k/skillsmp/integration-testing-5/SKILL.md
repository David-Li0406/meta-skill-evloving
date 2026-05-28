---
name: integration-testing
description: 运行后端和前端集成测试，检查 API 和 UI 交互。包含 E2E 测试执行、结果分析、失败诊断。使用此 Skill 来验证系统功能完整性，运行端到端测试，或调试集成问题。
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
---

# 集成测试 Skill

## 测试脚本位置

```
/Users/jietaoxie/my-prototype-logistics/tests/api/
├── test_authentication.sh          # 8 种角色认证测试
├── test_phase2_1_material_batches.sh  # 原材料批次 CRUD
├── test_phase2_2_equipment.sh      # 设备管理
├── test_phase2_3_suppliers.sh      # 供应商管理
├── test_dashboard.sh               # 仪表板 API
└── ... (20+ 个测试脚本)
```

## 快速执行

### 1. 检查/启动后端

```bash
# 检查后端是否运行
lsof -i :10010 || echo "后端未运行"

# 启动后端（如需要）
cd /Users/jietaoxie/my-prototype-logistics/backend-java
JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-17.jdk/Contents/Home mvn clean package -DskipTests -q
nohup mvn spring-boot:run > /tmp/backend.log 2>&1 &
sleep 15
```

### 2. 运行测试

```bash
cd /Users/jietaoxie/my-prototype-logistics/tests/api

# 认证测试
bash test_authentication.sh 2>&1 | tee /tmp/auth_test.log

# 材料批次测试
bash test_phase2_1_material_batches.sh 2>&1 | tee /tmp/material_test.log

# 设备管理测试
bash test_phase2_2_equipment.sh 2>&1 | tee /tmp/equipment_test.log

# 供应商测试
bash test_phase2_3_suppliers.sh 2>&1 | tee /tmp/suppliers_test.log

# 仪表板测试
bash test_dashboard.sh 2>&1 | tee /tmp/dashboard_test.log
```

### 3. 分析结果

```bash
# 检查失败
grep -i "FAIL\|ERROR\|failed" /tmp/*.log | head -30

# 统计通过/失败
grep -c "PASS\|SUCCESS" /tmp/*.log 2>/dev/null || echo "0 passed"
grep -c "FAIL\|ERROR" /tmp/*.log 2>/dev/null || echo "0 failed"
```

## 远程服务器测试

```bash
# 测试生产服务器
export API_BASE_URL="http://139.196.165.140:10010"
bash test_authentication.sh
```

## 常见问题排查

| 症状 | 可能原因 | 解决方案 |
|------|----------|----------|
| 后端启动超时 | MySQL 未运行 | `mysql.server start` |
| 端口被占用 | 旧进程未退出 | `lsof -i :10010 \| awk 'NR>1 {print $2}' \| xargs kill -9` |
| API 返回 401 | JWT token 过期 | 重新登录获取新 token |
| 连接超时 | 网络问题 | 检查网络设置 |
| 数据库错误 | MySQL 连接失败 | 检查 MySQL 服务 |

## 测试账号

**密码统一**: `123456`

| 账号 | 角色 |
|------|------|
| factory_admin1 | 工厂管理员 |
| workshop_sup1 | 车间主任 |
| warehouse_mgr1 | 仓储主管 |
| hr_admin1 | HR 管理员 |
| dispatcher1 | 调度员 |
| quality_insp1 | 质检员 |

## 参考

- 后端代码: `backend-java/src/main/java/com/cretas/aims/controller/`
- 测试脚本: `tests/api/`
