# 进化检查模块 (Evolution Check)

会话结束时执行进化检查。

## 触发条件

1. **复杂 Bug 修复**: 连续尝试 > 1 次
2. **用户明确反馈**: "记住"、"以后都这样做"、"保存这个"
3. **新最佳实践**: 发现更优解决方案
4. **非标准解决方案**: 特定环境的 workaround

## 检查流程

```
是否满足触发条件？
    ├─ 是 → 调用进化流程
    │       ├─ 静默模式: 后台执行
    │       └─ 交互模式: 询问用户确认
    └─ 否 → 正常结束会话
```

## 进化命令

```bash
# 存储偏好
python scripts/store_experience.py --preference "偏好内容"

# 存储修复方案
python scripts/store_experience.py --fix "修复方案"

# 存储技术栈模式
python scripts/store_experience.py --tech react --pattern "模式内容"

# 存储上下文触发器
python scripts/store_experience.py --context when_testing --instruction "使用 Vitest"
```

## 触发示例

| 场景 | 触发 | 存储 |
|------|------|------|
| 修复跨域问题失败2次后成功 | 是 | `--fix "Vite 需配置 proxy"` |
| 用户说"记住用 pnpm" | 是 | `--preference "使用 pnpm"` |
| 简单修改一行代码 | 否 | - |
| 用户说"很好" | 否 | - |
