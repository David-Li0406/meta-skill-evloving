# 快速定位索引

## 关键文件

- `game.js`：移动端布局管理器初始化入口（side effect）。
- `services/mobileLayoutManager.js`：移动端触发条件与摇杆开关来源。
- `style.css`：移动端样式段落与 `.is-mobile-layout` 选择器。
- `index.html`：移动端顶部栏与相关结构。
- `ui/taskModal/taskModalController.js`：移动端类名切换示例。
- `ui/virtualJoystick/virtualJoystick.js`：虚拟摇杆实现。
- `ui/virtualJoystick/index.js`：虚拟摇杆导出入口。
- `data/lang/base/zh.js` / `data/lang/base/en.js`：移动端文案与摇杆文案。

## 快速检索指令（rg）

```bash
rg -n "mobileLayoutManager|is-mobile-layout|mobile-tabs-active" -S
rg -n "virtual-joystick|createMobileJoystick|JOYSTICK_DIRECTION" -S
rg -n "mobile-top-bar|mobile-story-button" -S index.html style.css
rg -n "touch-action|touchstart|touchmove" -S
```

## 定位建议

- 先找 JS 入口（`mobileLayoutManager` / 组件控制器），再找 CSS 作用域（`.is-mobile-layout`）。
- 需要移动端文案时，同步更新 `zh.js` 与 `en.js`。
