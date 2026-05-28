# 虚拟摇杆接入指南

## 使用入口

- 入口导出：`ui/virtualJoystick/index.js`
- 组件实现：`ui/virtualJoystick/virtualJoystick.js`

## 标准接入流程

1. 在小游戏类中导入：

```js
import { createMobileJoystick, JOYSTICK_DIRECTION } from '../../ui/virtualJoystick/index.js';
```

2. 初始化时创建摇杆，统一用 `createMobileJoystick`：

```js
this._joystickDirectionHandler = this._handleJoystickDirection.bind(this);
this.joystick = createMobileJoystick({
  mode: 'four',
  renderMode: 'analog',
  onDirection: this._joystickDirectionHandler,
  onRelease: () => this._handleJoystickDirection(JOYSTICK_DIRECTION.NONE),
});
```

3. 方向处理统一 switch 映射：

```js
_handleJoystickDirection(direction) {
  switch (direction) {
    case JOYSTICK_DIRECTION.LEFT:
      // 处理左移
      break;
    case JOYSTICK_DIRECTION.RIGHT:
      // 处理右移
      break;
    case JOYSTICK_DIRECTION.UP:
      // 处理上移
      break;
    case JOYSTICK_DIRECTION.DOWN:
      // 处理下移
      break;
    default:
      // 松开
      break;
  }
}
```

4. 退出/销毁时清理：

```js
if (this.joystick) {
  this.joystick.destroy();
  this.joystick = null;
}
```

## 约束

- 不要自行实现新摇杆；统一复用现有组件。
- 移动端显示/隐藏由 `createMobileJoystick` 内部根据 `mobileLayoutManager` 自动处理。
- 需要十字键样式时，将 `renderMode` 设为 `'dpad'`。
