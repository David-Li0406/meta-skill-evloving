---
name: game-mobile-ui
description: 用于游戏项目的移动端界面样式与适配。涉及统一移动布局触发条件、移动端 UI 样式调整、触摸交互优化、以及小游戏虚拟摇杆接入与复用时使用；也用于快速定位移动端相关文件与入口。
---

# 游戏移动端界面适配

## 概览

使用本技能统一移动端布局触发条件，复用既有的 `mobileLayoutManager` 与虚拟摇杆，避免重复媒体查询和分散的特殊分支。

## 快速定位文件

优先按“入口→服务→样式→组件”顺序定位，具体路径与检索指令见：
- `references/path-index.md`

## 统一适配流程（必走）

1. **建立分层适配机制**：
    - **布局层（CSS）**：优先使用纯 CSS 媒体查询 `(max-height: 500px) and (orientation: landscape)` 作为兜底，确保在 JS 未生效或临界尺寸下，基础 UI（如边框、提示窗口）不崩溃。
    - **逻辑层（JS）**：交互逻辑（如虚拟摇杆、触摸坐标重算）必须使用 `services/mobileLayoutManager.js` 作为唯一状态来源。
2. **JS 状态同步**：继续在组件根容器上通过 `mobileLayoutManager.subscribe` 同步 `is-mobile-layout` 类，用于触发 JS 相关的样式变化或增强功能。
3. **样式编写规范**：移动端样式应兼顾鲁棒性。既要支持 `.is-mobile-layout` 类选择器，也要考虑添加 `@media` 查询作为安全垫 (Fallback)。
4. 触摸交互统一使用 `touch-action` 与 `passive: false` 控制，避免在业务层到处堆 `if/else`。
5. 新增/调整 UI 文案时，同步更新中英文语言文件。

## 小游戏虚拟摇杆接入

需要移动方向控制时，统一使用 `ui/virtualJoystick` 已有实现与 `createMobileJoystick` 帮助方法，详细接入方式见：
- `references/virtual-joystick.md`

## 质量检查

- **[鲁棒性]** 在禁用 JS 或类名未添加的情况下（如尺寸临界），基础 UI 布局（如边框、滚动条）在小屏幕下应依然可用。
- 避免逻辑层出现散落的 `matchMedia` 判断，统一由 Manager 管理。
- 移动端关键样式应有 CSS 媒体查询兜底。
- 摇杆创建/销毁生命周期清晰，确保资源释放。
- 中英文文案同步更新且无缺失。

## 参考资料

- `references/mobile-adaptation.md`
- `references/path-index.md`
- `references/virtual-joystick.md`
