# 统一移动端适配方案

## 统一触发条件

- 使用 `services/mobileLayoutManager.js` 作为唯一移动端布局判断来源。
- 当前统一条件为：`(max-height: 500px) and (orientation: landscape)`。
- 需要改变触发条件时，只在 `MOBILE_QUERY` 处修改一次，避免散落。

## 推荐接入方式（组件级）

1. 在组件初始化时读取 `mobileLayoutManager.isMobileLayout()`。
2. 使用 `mobileLayoutManager.subscribe` 订阅变化，统一 add/remove `is-mobile-layout`。
3. 样式通过 `.is-mobile-layout` 进行作用域限定，放在 `style.css` 的移动端段落内。

示例（伪代码）：

```js
import { mobileLayoutManager } from '../services/mobileLayoutManager.js';

const applyMobileClass = (root) => {
  const update = ({ isMobile }) => {
    if (isMobile) root.classList.add('is-mobile-layout');
    else root.classList.remove('is-mobile-layout');
  };
  update({ isMobile: mobileLayoutManager.isMobileLayout() });
  const unsubscribe = mobileLayoutManager.subscribe(update);
  return () => unsubscribe();
};
```

## 样式与交互约束

- 移动端样式必须通过 `.is-mobile-layout` 或现有移动类触发。
- 避免在 JS 中堆叠 `if (isMobile) ...`，用类切换 + CSS 处理布局。
- 触摸交互统一设置 `touch-action`，必要时使用 `{ passive: false }`。

## 相关入口

- `services/mobileLayoutManager.js`
- `style.css`（移动端段落与 `.is-mobile-layout` 规则）
- `ui/taskModal/taskModalController.js`（类名切换示例）
