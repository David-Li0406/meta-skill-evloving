# Testing Matrix

> 什么场景跑什么测试

---

## 场景定义

| 场景 | 触发条件 |
|------|----------|
| **Local** | 本地开发/调试 |
| **PR** | PR → develop，CI 环境 `pull_request` |
| **Release** | develop → main，`base=main` |
| **Nightly** | 定时触发（schedule） |
| **EngineUpgrade** | 业务 repo 的 `.engine-version` 变更 |

---

## Engine Repo 测试矩阵

| 场景 | Regression | Unit | E2E (Golden Paths) |
|------|------------|------|---------------------|
| **Local** | 可选（相关 RCI） | ✅ 相关 hooks/scripts | ❌ |
| **PR** | ✅ trigger=PR | ✅ all | ❌ |
| **Release** | ✅ trigger=Release | ✅ all | ✅ 流程链路 |
| **Nightly** | ✅ all | ✅ all | ✅ all |

### Engine 命令映射

```bash
# Local
npm run test -- --watch

# PR
npm run qa
bash scripts/rc-filter.sh pr

# Release
npm run qa
bash scripts/rc-filter.sh release
# + 手动验证 Golden Paths

# Nightly
npm run qa
bash scripts/rc-filter.sh nightly
```

---

## Business Repo 测试矩阵

| 场景 | Business Meta | Unit | E2E (Golden Paths) | ECC |
|------|---------------|------|---------------------|-----|
| **Local** | ❌ | ✅ 相关模块 | 可选 | ❌ |
| **PR** | ✅ gate/ci | ✅ all/impacted | ❌ | ❌ |
| **Release** | ✅ gate/ci | ✅ all | ✅ 用户链路 | ❌ |
| **Nightly** | ✅ | ✅ all | ✅ all | ❌ |
| **EngineUpgrade** | ✅ | ✅ smoke | ✅ smoke | ✅ |

### Business 命令映射

```bash
# Local
npm run test -- --watch

# PR
npm run qa

# Release
npm run qa
# + E2E 用户链路测试

# EngineUpgrade (额外)
# 业务 repo 自行实现 ECC 检查脚本
npm run ecc  # 或业务 repo 自定义命令
```

---

## ECC (Engine Compatibility Check)

**仅业务 repo 升级 Engine 版本时触发**

触发条件：
- `.engine-version` 文件变更
- 或手动触发

检查内容：
1. **轻量 Regression**：Hook 可加载、Gate 可拦截
2. **轻量 E2E**：核心流程可跑通

```bash
# ECC 检查（业务 repo 自行实现）
npm run ecc  # 或业务 repo 自定义命令

# 或在 CI 中
if: files_changed('.engine-version')
run: npm run ecc
```

---

## 决策流程图

```
开始
  │
  ├─→ RepoType = Engine?
  │     ├─→ Stage = PR? → Regression(PR) + Unit(all)
  │     ├─→ Stage = Release? → Regression(Release) + Unit(all) + E2E(GP)
  │     └─→ Stage = Nightly? → Regression(all) + Unit(all) + E2E(all)
  │
  └─→ RepoType = Business?
        ├─→ Stage = PR? → Meta + Unit(all)
        ├─→ Stage = Release? → Meta + Unit(all) + E2E(GP)
        ├─→ Stage = Nightly? → Meta + Unit(all) + E2E(all)
        └─→ .engine-version 变更? → + ECC
```

---

## 快速参考

| 问题 | 答案 |
|------|------|
| PR 要跑 E2E 吗？ | 不需要，PR 只跑 Regression + Unit |
| Release 要跑全量吗？ | 是，Release = Regression(all) + Unit(all) + E2E(GP) |
| ECC 是什么时候跑？ | 仅业务 repo 升级 Engine 版本时 |
| Nightly 和 Release 区别？ | Nightly 跑所有 GP，Release 只跑关键 GP |
