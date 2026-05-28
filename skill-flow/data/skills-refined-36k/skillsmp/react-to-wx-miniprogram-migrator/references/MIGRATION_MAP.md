# React to WeChat Mini Program Migration Map

This document provides detailed mapping tables to assist in the conversion from a React + TailwindCSS H5 application to a native WeChat Mini Program.

---

## 1. Project Structure

**Recommended WeChat Mini Program Structure:**

```
miniprogram/
├── app.js                 # App logic
├── app.json               # App configuration
├── app.wxss               # Global styles
├── pages/
│   ├── index/             # Index page
│   │   ├── index.js
│   │   ├── index.wxml
│   │   ├── index.wxss
│   │   └── index.json
│   └── ...                # Other pages
├── components/
│   └── custom-component/  # Reusable component
│       ├── index.js
│       ├── index.wxml
│       ├── index.wxss
│       └── index.json
├── utils/
│   └── util.js            # Utility functions
└── images/                # Static image assets
```

---

## 2. Component & Tag Mapping

| React/HTML | WeChat Mini Program | Description |
|------------|---------------------|-------------|
| `<div>` | `<view>` | General-purpose container, equivalent to a block-level element. |
| `<span>`, `<p>`, `<h1>`-`<h6>` | `<text>` | For displaying text. It is the equivalent of an inline element. |
| `<img>` | `<image>` | Image component. Note the `mode` attribute for scaling. |
| `<a>` | `<navigator>` | Used for page navigation. Not for external links. |
| `<input>` | `<input>` | Standard text input field. |
| `<textarea>` | `<textarea>` | Multi-line text input. |
| `<button>` | `<button>` | Clickable button. |
| `<ul>`, `<ol>`, `<li>` | `<view>` with `wx:for` | Lists are constructed using loops over `<view>` or other components. |
| `<form>` | `<form>` | Form container for grouping form controls. |
| `<label>` | `<label>` | Associates a label with a form control. |
| `<select>`, `<option>` | `<picker>` | Dropdown selector. Different modes are available. |
| `<video>` | `<video>` | Video player component. |
| `<audio>` | `<audio>` | Audio player component. |
| `<canvas>` | `<canvas>` | Canvas for drawing graphics. |
| `<iframe>` | `<web-view>` | Embeds a web page. Use is restricted. |
| `<svg>` | Not directly supported | Convert SVG to a PNG/JPG image or use a third-party library to draw on a canvas. |

---

## 3. Event Binding Mapping

| React Event | WeChat Mini Program Event | Description |
|-------------|---------------------------|-------------|
| `onClick` | `bindtap` or `catchtap` | Tap/click event. `catchtap` prevents event bubbling. |
| `onChange` | `bindinput` / `bindchange` | `bindinput` fires on every character change, `bindchange` fires on blur. |
| `onSubmit` | `bindsubmit` | Triggered when a form is submitted. |
| `onScroll` | `bindscroll` | Fired when a `<scroll-view>` is scrolled. |
| `onFocus` | `bindfocus` | Fired when an input element gets focus. |
| `onBlur` | `bindblur` | Fired when an input element loses focus. |
| `onTouchStart`| `bindtouchstart` | Fired when a touch starts. |
| `onTouchMove` | `bindtouchmove` | Fired when a touch moves. |
| `onTouchEnd` | `bindtouchend` | Fired when a touch ends. |
| `onLoad` (for images) | `bindload` | Fired when an image or resource finishes loading. |
| `onError` (for images) | `binderror` | Fired when an error occurs during resource loading. |

---

## 4. Lifecycle Mapping

### App Lifecycle (`app.js`)

| React (Conceptual) | WeChat Mini Program App | Description |
|--------------------|-------------------------|-------------|
| App Initialization | `onLaunch` | Triggered once when the Mini Program is initialized. |
| App becomes active | `onShow` | Triggered when the Mini Program starts or is brought to the foreground. |
| App becomes inactive| `onHide` | Triggered when the Mini Program is sent to the background. |

### Page Lifecycle (`pages/page/index.js`)

| React Hooks | WeChat Mini Program Page | Description |
|-------------|--------------------------|-------------|
| `useEffect(() => {}, [])` | `onLoad` | Triggered when the page is loaded. Only called once. |
| `useEffect(() => {})` | `onShow` | Triggered every time the page is displayed. |
| `useEffect(() => { return cleanup; }, [])` | `onUnload` | Triggered when the page is unloaded/destroyed. |
| - | `onReady` | Triggered when the page has finished its initial rendering. |
| - | `onHide` | Triggered when the page is hidden (e.g., navigating away). |

---

## 5. API Mapping

### Routing & Navigation

| React Router | WeChat Mini Program API | Description |
|--------------|-------------------------|-------------|
| `navigate("/path")` | `wx.navigateTo({ url: ".
/pages/path/index" })` | Navigates to a new page, keeping the current page in the stack. |
| `navigate("/path", { replace: true })` | `wx.redirectTo({ url: ".
/pages/path/index" })` | Replaces the current page with a new one. |
| - | `wx.switchTab({ url: ".
/pages/tab/index" })` | Navigates to a tab bar page. |
| `navigate(-1)` | `wx.navigateBack()` | Goes back one level in the navigation stack. |

### Network Requests

| Web API (fetch/axios) | WeChat Mini Program API | Description |
|-----------------------|-------------------------|-------------|
| `fetch("/api/data")` | `wx.request({ url: "https://domain/api/data" })` | Initiates an HTTPS network request. Note the requirement for a full URL and domain whitelisting. |

### Local Storage

| Web API | WeChat Mini Program API | Description |
|-----------|-------------------------|-------------|
| `localStorage.setItem("key", data)` | `wx.setStorageSync("key", data)` | Synchronously saves data to local storage. |
| `localStorage.getItem("key")` | `wx.getStorageSync("key")` | Synchronously retrieves data from local storage. |
| `localStorage.removeItem("key")` | `wx.removeStorageSync("key")` | Synchronously removes an item from local storage. |
| `localStorage.clear()` | `wx.clearStorageSync()` | Synchronously clears all local storage. |

---


## 6. TailwindCSS to WXSS Conversion

### Unit Conversion

The most important conversion is from `px` or `rem` to `rpx`. The WeChat Mini Program uses `rpx` (responsive pixel) as its primary unit, where the screen width is always 750rpx.

| TailwindCSS Unit | WXSS Equivalent | Conversion Rule |
|------------------|-----------------|-----------------|
| `px` | `rpx` | `1px` ≈ `2rpx` (based on iPhone 6 at 375px width) |
| `rem` | `rpx` | `1rem` (16px) = `32rpx` |
| `%` | `%` | No change |
| `vw` / `vh` | `rpx` / `%` | `100vw` = `750rpx`. `vh` needs calculation or use `%`. |

### Common Tailwind Class Conversions

| TailwindCSS Class | WXSS Equivalent |
|-------------------|-----------------|
| `flex` | `display: flex;` |
| `flex-col` | `flex-direction: column;` |
| `flex-row` | `flex-direction: row;` |
| `flex-wrap` | `flex-wrap: wrap;` |
| `items-center` | `align-items: center;` |
| `items-start` | `align-items: flex-start;` |
| `items-end` | `align-items: flex-end;` |
| `justify-center` | `justify-content: center;` |
| `justify-between` | `justify-content: space-between;` |
| `justify-around` | `justify-content: space-around;` |
| `justify-start` | `justify-content: flex-start;` |
| `justify-end` | `justify-content: flex-end;` |
| `w-full` | `width: 100%;` |
| `w-1/2` | `width: 50%;` |
| `w-screen` | `width: 750rpx;` |
| `h-full` | `height: 100%;` |
| `h-screen` | `height: 100vh;` (may need adjustment) |
| `p-4` | `padding: 32rpx;` |
| `px-4` | `padding-left: 32rpx; padding-right: 32rpx;` |
| `py-4` | `padding-top: 32rpx; padding-bottom: 32rpx;` |
| `pt-4` | `padding-top: 32rpx;` |
| `m-4` | `margin: 32rpx;` |
| `mx-auto` | `margin-left: auto; margin-right: auto;` |
| `mt-4` | `margin-top: 32rpx;` |
| `text-xs` | `font-size: 24rpx;` |
| `text-sm` | `font-size: 28rpx;` |
| `text-base` | `font-size: 32rpx;` |
| `text-lg` | `font-size: 36rpx;` |
| `text-xl` | `font-size: 40rpx;` |
| `text-2xl` | `font-size: 48rpx;` |
| `text-center` | `text-align: center;` |
| `text-left` | `text-align: left;` |
| `text-right` | `text-align: right;` |
| `font-normal` | `font-weight: 400;` |
| `font-medium` | `font-weight: 500;` |
| `font-semibold` | `font-weight: 600;` |
| `font-bold` | `font-weight: 700;` |
| `rounded` | `border-radius: 8rpx;` |
| `rounded-lg` | `border-radius: 16rpx;` |
| `rounded-full` | `border-radius: 9999rpx;` |
| `bg-white` | `background-color: #ffffff;` |
| `bg-black` | `background-color: #000000;` |
| `bg-gray-100` | `background-color: #f3f4f6;` |
| `bg-blue-500` | `background-color: #3b82f6;` |
| `text-white` | `color: #ffffff;` |
| `text-black` | `color: #000000;` |
| `text-gray-500` | `color: #6b7280;` |
| `border` | `border: 2rpx solid #e5e7eb;` |
| `border-b` | `border-bottom: 2rpx solid #e5e7eb;` |
| `shadow-sm` | `box-shadow: 0 2rpx 4rpx rgba(0,0,0,0.05);` |
| `shadow-md` | `box-shadow: 0 8rpx 12rpx rgba(0,0,0,0.1);` |
| `hidden` | `display: none;` |
| `block` | `display: block;` |
| `inline` | `display: inline;` |
| `overflow-hidden` | `overflow: hidden;` |
| `overflow-auto` | `overflow: auto;` |
| `absolute` | `position: absolute;` |
| `relative` | `position: relative;` |
| `fixed` | `position: fixed;` |
| `top-0` | `top: 0;` |
| `left-0` | `left: 0;` |
| `right-0` | `right: 0;` |
| `bottom-0` | `bottom: 0;` |
| `z-10` | `z-index: 10;` |
| `z-50` | `z-index: 50;` |
| `opacity-50` | `opacity: 0.5;` |
| `cursor-pointer` | Not applicable (no cursor on mobile) |
| `gap-4` | Not supported. Use `margin` on children. |

### WXSS Unsupported Features

The following CSS features are **not supported** or have limited support in WXSS:

1.  **Universal Selector (`*`)**: Cannot be used.
2.  **Attribute Selectors (`[type="text"]`)**: Not supported.
3.  **Complex Descendant Selectors**: Avoid deeply nested selectors.
4.  **`gap` property**: Use margins on child elements instead.
5.  **CSS Variables (`--var`)**: Limited support; avoid if possible.
6.  **`@keyframes` with complex animations**: Basic support exists, but complex animations may require the `wx.createAnimation` API.
7.  **`calc()` function**: Supported with limitations.
8.  **`@media` queries**: Supported but less common; use `rpx` for responsiveness.

---

## 7. JSX to WXML Syntax Conversion Examples

### Conditional Rendering

**React JSX:**
```jsx
// Short-circuit evaluation
{isLoggedIn && <UserProfile />}

// Ternary operator
{isLoading ? <Spinner /> : <Content />}
```

**WeChat WXML:**
```xml
<!-- wx:if directive -->
<user-profile wx:if="{{isLoggedIn}}"></user-profile>

<!-- wx:if / wx:else -->
<spinner wx:if="{{isLoading}}"></spinner>
<content wx:else></content>
```

### List Rendering

**React JSX:**
```jsx
{items.map((item, index) => (
  <div key={item.id} className="item">
    <span>{index + 1}. {item.name}</span>
  </div>
))}
```

**WeChat WXML:**
```xml
<view wx:for="{{items}}" wx:key="id" wx:for-item="item" wx:for-index="index" class="item">
  <text>{{index + 1}}. {{item.name}}</text>
</view>
```

### Dynamic Class Names

**React JSX:**
```jsx
<div className={`card ${isActive ? 'active' : ''} ${isDisabled ? 'disabled' : ''}`}>
  Content
</div>
```

**WeChat WXML:**
```xml
<view class="card {{isActive ? 'active' : ''}} {{isDisabled ? 'disabled' : ''}}">
  Content
</view>
```

### Event Handling with Parameters

**React JSX:**
```jsx
<button onClick={() => handleClick(item.id)}>Click</button>
```

**WeChat WXML:**
```xml
<!-- Use data-* attributes to pass parameters -->
<button bindtap="handleClick" data-id="{{item.id}}">Click</button>
```

**WeChat JS:**
```javascript
Page({
  handleClick(e) {
    const id = e.currentTarget.dataset.id;
    // ... use id
  }
})
```

---

## 8. State Management Conversion Example

**React Component:**
```jsx
import React, { useState, useEffect } from 'react';

function Counter() {
  const [count, setCount] = useState(0);
  const [name, setName] = useState('');

  useEffect(() => {
    console.log('Component mounted');
    fetchData();
  }, []);

  const increment = () => {
    setCount(count + 1);
  };

  const fetchData = async () => {
    const res = await fetch('/api/user');
    const data = await res.json();
    setName(data.name);
  };

  return (
    <div>
      <p>Count: {count}</p>
      <p>Name: {name}</p>
      <button onClick={increment}>Add</button>
    </div>
  );
}
```

**WeChat Mini Program Page:**

`pages/counter/counter.js`:
```javascript
Page({
  data: {
    count: 0,
    name: ''
  },

  onLoad() {
    console.log('Page loaded');
    this.fetchData();
  },

  increment() {
    this.setData({
      count: this.data.count + 1
    });
  },

  fetchData() {
    wx.request({
      url: 'https://your-domain.com/api/user',
      success: (res) => {
        this.setData({
          name: res.data.name
        });
      }
    });
  }
});
```

`pages/counter/counter.wxml`:
```xml
<view>
  <text>Count: {{count}}</text>
  <text>Name: {{name}}</text>
  <button bindtap="increment">Add</button>
</view>
```
