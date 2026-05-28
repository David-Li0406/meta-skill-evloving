# Taro → React Native 已知问题和解决方案

本文档记录 Taro 转换为 React Native 过程中遇到的兼容性问题及解决方案。

> **注意**：Monorepo 特有问题请参考 `recipes/monorepo/KNOWN_ISSUES.md`

---

## 1. 扩展依赖

### 1.1 react-native-linear-gradient

**问题描述：** React Native 不支持 CSS 渐变（`linear-gradient`、`radial-gradient` 等）

**原始代码（Taro/CSS）：**

```css
.sendBtn {
    background: linear-gradient(to left, #00d3ea, #00cfa3);
}
```

**解决方案：** 使用 `react-native-linear-gradient` 库

```bash
pnpm add react-native-linear-gradient
cd ios && pod install  # iOS 需要安装原生依赖
```

**RN 代码：**

```tsx
import LinearGradient from 'react-native-linear-gradient';

<LinearGradient
    colors={['#00d3ea', '#00cfa3']}
    start={{x: 1, y: 0}}
    end={{x: 0, y: 0}}
    style={styles.sendBtn}
>
    <Text>发送</Text>
</LinearGradient>;
```

**渐变方向映射：** | CSS 方向 | RN start | RN end | |---------|----------|--------| | to left | {x:
1, y: 0} | {x: 0, y: 0} | | to right | {x: 0, y: 0} | {x: 1, y: 0} | | to top | {x: 0, y: 1} | {x:
0, y: 0} | | to bottom | {x: 0, y: 0} | {x: 0, y: 1} |

---

### 1.2 react-native-safe-area-context

**问题描述：** React Native 需要处理刘海屏、底部安全区域等

**解决方案：** 使用 `react-native-safe-area-context` 库

```bash
pnpm add react-native-safe-area-context
cd ios && pod install
```

**RN 代码：**

```tsx
import {SafeAreaView} from 'react-native-safe-area-context';

<SafeAreaView style={styles.container} edges={['bottom']}>
    {children}
</SafeAreaView>;
```

---

### 1.3 react-native-date-picker

**问题描述：** Taro 的 `Picker mode="date"` 或第三方 UI 库的日期选择器
在 RN 中没有直接对应组件。官方 `@react-native-community/datetimepicker`
iOS/Android 样式差异大，无法保持跨平台一致的滚轮体验。

**解决方案：** 使用 `react-native-date-picker` 实现统一的跨平台日期选择器

**使用场景：** 日期选择器（PickerDate）

### 1.4 @quidone/react-native-wheel-picker

**问题描述：** 第三方 UI 库的 Picker
组件在 RN 中没有直接替代。需要实现支持多列联动的滚轮选择器（如省市区三级联动）。

**解决方案：** 使用 `@quidone/react-native-wheel-picker` 实现跨平台滚轮选择器

```bash
pnpm add @quidone/react-native-wheel-picker
cd ios && pod install  # iOS 需要安装原生依赖
```

**使用场景：** 地址选择器（PickerAddress）、多列滚轮选择场景

**RN 代码：**

```tsx
import {WheelPicker} from '@quidone/react-native-wheel-picker';

<WheelPicker
    value={selectedIndex}
    onValueChanging={setSelectedIndex}
    itemHeight={44}
    visibleCount={5}
>
    {data.map((item, index) => (
        <WheelPicker.Item key={item.id} value={index} label={item.name} />
    ))}
</WheelPicker>;
```

**常用属性：** | 属性 | 类型 | 说明 | |------|------|------| | `value` | `number` | 当前选中索引 | |
`onValueChanging` | `(index: number) => void` | 滚动变化回调 | | `itemHeight` | `number`
| 每项高度 | | `visibleCount` | `number` | 可见项数量 | | `itemTextStyle` | `TextStyle` | 文本样式 |

---

### 1.5 react-native-date-picker

**问题描述：** 日期选择器需要跨平台一致的滚轮体验。

**解决方案：** 使用 `react-native-date-picker`

```bash
pnpm add react-native-date-picker
cd ios && pod install  # iOS 需要安装原生依赖
```

**使用场景：** 日期选择器（PickerDate）

**RN 代码：**

```tsx
import DatePicker from 'react-native-date-picker';

<DatePicker
    date={selectedDate}
    onDateChange={setSelectedDate}
    mode='date'
    locale='zh'
    minimumDate={new Date('1900-01-01')}
    maximumDate={new Date()}
    androidVariant='iosClone' // Android 使用 iOS 风格滚轮
    fadeToColor='#ffffff'
    textColor='#333333'
/>;
```

**常用属性：** | 属性 | 类型 | 说明 | |------|------|------| | `date` | `Date` | 当前选中日期 | |
`onDateChange` | `(date: Date) => void` | 日期变化回调 | | `mode` | `'date' \| 'time' \| 'datetime'`
| 选择器模式 | | `locale` | `string` | 语言区域（如 'zh'） | | `minimumDate` | `Date`
| 最小可选日期 | | `maximumDate` | `Date` | 最大可选日期 | | `androidVariant` |
`'iosClone' \| 'nativeAndroid'` | Android 样式风格 |

---

## 2. 样式差异

### 2.1 设计稿尺寸

**问题描述：** 不同项目可能使用不同设计稿宽度（如 750、1242 等）

**重要：开始样式转换前，必须先确认以下事项：**

1. **询问确认视觉稿标准**：750 还是 1242？
2. **检查 rpx 工具函数是否已封装**

**Taro 配置示例：**

```js
// 750 设计稿（默认）
designWidth: 750

// 1242 设计稿
designWidth: 1242,
deviceRatio: {
    1242: 2 / 3.312
}
```

**解决方案：** 使用对应的 rpx 转换函数

```tsx
import {rpx, rpx1242, createRpx} from 'your-rn-core-package';

// 750 设计稿
padding: rpx(36);

// 1242 设计稿
padding: rpx1242(36);

// 自定义设计稿
const rpx640 = createRpx(640);
padding: rpx640(36);
```

**rpx 工具函数封装（如未存在则创建）：**

```tsx
// src/utils/rpx.ts
import {Dimensions} from 'react-native';

const {width: screenWidth} = Dimensions.get('window');

/** 750 设计稿尺寸转换 */
export const rpx = (value: number): number => (value * screenWidth) / 750;

/** 1242 设计稿尺寸转换 */
export const rpx1242 = (value: number): number => (value * screenWidth) / 1242;

/** 自定义设计稿尺寸转换工厂函数 */
export const createRpx = (designWidth: number) => {
    return (value: number): number => (value * screenWidth) / designWidth;
};
```

---

### 2.2 Image 组件

**问题描述：** RN 的 Image 组件必须显式设置宽高，且需要指定 resizeMode

**原始代码（Taro）：**

```tsx
<Image src={url} className={styles.icon} />
```

**RN 代码：**

```tsx
<Image
    source={{uri: url}}
    style={styles.icon} // 必须包含 width 和 height
    resizeMode='contain'
/>
```

**resizeMode 选项：**

- `cover` - 保持比例填充（可能裁剪）
- `contain` - 保持比例完整显示
- `stretch` - 拉伸填充
- `center` - 居中不缩放

**注意事项：**

- 远程图片必须设置宽高，否则不显示
- 建议添加 `onError` 回调处理加载失败

---

### 2.3 阴影样式

**问题描述：** Android 和 iOS 阴影实现方式不同

**原始代码（CSS）：**

```css
.card {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
```

**RN 代码：**

```tsx
const styles = StyleSheet.create({
    card: {
        // iOS 阴影
        shadowColor: '#000',
        shadowOffset: {width: 0, height: 2},
        shadowOpacity: 0.1,
        shadowRadius: 4,
        // Android 阴影
        elevation: 4
    }
});
```

---

## 3. API 差异

### 3.1 事件中心

**问题描述：** Taro 的 `eventCenter` 需要替换为 RN 版本

**原始代码（Taro）：**

```tsx
import {eventCenter} from '@tarojs/taro';
eventCenter.on('event', handler);
```

**RN 代码：**

```tsx
// 使用项目封装的事件中心，或使用第三方库如 eventemitter3
import {eventCenter} from 'your-rn-core-package';
eventCenter.on('event', handler);
```

---

### 3.2 页面导航

**问题描述：** Taro 路由需要替换为 React Navigation

**原始代码（Taro）：**

```tsx
import Taro from '@tarojs/taro';
Taro.navigateTo({url: '/pages/detail/index?id=1'});
```

**RN 代码：**

```tsx
import {useNavigation} from '@react-navigation/native';
const navigation = useNavigation();
navigation.navigate('Detail', {id: 1});
```

---

### 3.3 键盘收起

**问题描述：** 点击页面其他区域时需要手动收起键盘

**解决方案：**

```tsx
import {Keyboard} from 'react-native';

// 在全局触摸监听中调用
const handleGlobalTouch = () => {
    Keyboard.dismiss();
};
```

---

## 4. 原生依赖安装

安装新原生依赖后必须执行：

```bash
# iOS
cd ios && pod install
cd .. && npx react-native run-ios

# Android
npx react-native run-android
```

**常见错误：**

- `View config not found for component 'XXX'` - 原生模块未链接，需要 pod install 并重新编译

---

## 5. 常用依赖清单

| 依赖包                                    | 版本    | 用途                       |
| ----------------------------------------- | ------- | -------------------------- |
| react-native-linear-gradient              | ^2.8.0  | CSS 渐变替代               |
| @react-native-community/blur              | ^4.4.0  | 模糊效果 (backdrop-filter) |
| react-native-safe-area-context            | ^5.0.0  | 安全区域处理               |
| @react-navigation/native                  | ^7.0.0  | 页面导航                   |
| @react-navigation/native-stack            | ^7.0.0  | 原生栈导航                 |
| react-native-screens                      | ^4.0.0  | 原生屏幕优化               |
| jotai                                     | ^2.0.0  | 状态管理                   |
| @react-native-async-storage/async-storage | ^2.0.0  | 本地存储                   |
| react-native-image-picker                 | ^7.0.0  | 图片选择（相机/相册）      |
| react-native-image-viewing                | ^0.2.0  | 图片预览                   |
| react-native-video                        | ^6.18.0 | 视频播放                   |
| react-native-fast-image                   | ^8.6.3  | 高性能图片/GIF             |

---

## 6. ScrollView 滚动监听与分页加载

### 6.1 问题描述

RN 不支持 Web/小程序的 `IntersectionObserver` API，需要替代方案实现滚动锚点监听和分页加载。

**典型场景：**

- 滚动到底部自动加载更多数据
- 监听某个元素进入/离开可视区域
- 无限滚动列表

### 6.2 解决方案

**方案 A：FlatList onEndReached（推荐用于简单列表）**

```tsx
<FlatList
    data={items}
    renderItem={({item}) => <Item {...item} />}
    onEndReached={loadMore}
    onEndReachedThreshold={0.5} // 距离底部 50% 时触发
/>
```

**优点：** 官方推荐，性能优化好
**缺点：** 仅适用于 FlatList，复杂布局不适用

---

**方案 B：ScrollView onScroll + View onLayout（推荐用于复杂布局）**

适用于需要在任意 ScrollView 布局中监听元素可见性的场景。

**实现原理：**

1. ScrollAnchor 通过 `onLayout` 获取自身位置（anchorTop）
2. ScrollView 通过 `onScroll` 获取滚动信息（scrollY, layoutHeight）
3. 通过 eventCenter 传递滚动信息（保持解耦）
4. ScrollAnchor 计算可见性并触发回调

**核心代码：**

```tsx
// ScrollAnchor 组件
const ScrollAnchor = ({onAnchorVisibleChange}) => {
    const [anchorTop, setAnchorTop] = useState(0);
    const previousVisibleRef = useRef(false);

    // 获取锚点位置
    const handleLayout = event => {
        const {y} = event.nativeEvent.layout;
        setAnchorTop(y);
    };

    // 监听滚动信息
    useEffect(() => {
        const checkVisibility = scrollInfo => {
            const {scrollY, layoutHeight} = scrollInfo;
            const isVisible = anchorTop > 0 && anchorTop <= scrollY + layoutHeight;

            if (isVisible !== previousVisibleRef.current) {
                previousVisibleRef.current = isVisible;
                onAnchorVisibleChange?.(isVisible);
            }
        };

        const debouncedCheck = debounce(checkVisibility, 300, {
            leading: false,
            trailing: true
        });

        eventCenter.on('scrollAnchor:scroll', debouncedCheck);
        return () => {
            eventCenter.off('scrollAnchor:scroll', debouncedCheck);
            debouncedCheck.cancel();
        };
    }, [anchorTop, onAnchorVisibleChange]);

    return <View onLayout={handleLayout}>{children}</View>;
};

// 父组件使用
const MyList = () => {
    const handleScroll = useCallback(event => {
        const {contentOffset, contentSize, layoutMeasurement} = event.nativeEvent;
        eventCenter.trigger('scrollAnchor:scroll', {
            scrollY: contentOffset.y,
            contentHeight: contentSize.height,
            layoutHeight: layoutMeasurement.height
        });
    }, []);

    return (
        <ScrollView onScroll={handleScroll} scrollEventThrottle={16}>
            {items.map(item => (
                <Item key={item.id} {...item} />
            ))}
            {hasMore && (
                <ScrollAnchor
                    onAnchorVisibleChange={visible => {
                        if (visible) loadMore();
                    }}
                >
                    <Text>加载中...</Text>
                </ScrollAnchor>
            )}
        </ScrollView>
    );
};
```

**关键配置：**

- `scrollEventThrottle={16}`：必须设置，控制滚动事件频率（约 60fps）
- 防抖延迟 300ms：避免滚动过程中频繁触发
- eventCenter：实现解耦的事件驱动架构

---

## 7. Flex 布局宽度计算

### 7.1 动态宽度计算问题

**问题描述：** 使用 `Dimensions.get('window').width`
计算子元素宽度时，未考虑父容器的 padding/border，导致子元素超出容器换行。

**典型场景：** 多列网格布局（如 3 列服务项）

**错误方式：**

```tsx
const itemWidth = (SCREEN_WIDTH - containerPadding) / 3;
// 问题：未考虑外层容器的 padding/border
```

**解决方案：** 使用 `onLayout` 获取容器实际宽度

```tsx
const [containerWidth, setContainerWidth] = useState(0);

const handleLayout = (event: LayoutChangeEvent) => {
    setContainerWidth(event.nativeEvent.layout.width);
};

const itemWidth = containerWidth > 0
    ? Math.floor((containerWidth - padding * 2 - gap * 2) / 3)
    : 0;

<View style={styles.container} onLayout={handleLayout}>
    {containerWidth > 0 && items.map(...)}
</View>
```

**关键点：**

- 使用 `Math.floor()` 避免浮点精度问题
- `containerWidth > 0` 时才渲染子元素，避免首次渲染闪烁
- 配合 `justifyContent: 'space-between'` 自动分配间距

---

### 7.2 Flex 子元素宽度撑满问题

**问题描述：** Flex 布局中，子元素默认 `alignSelf: 'stretch'` 会撑满父容器宽度。

**典型场景：** 按钮/标签需要根据内容自适应宽度

**解决方案：** 添加 `alignSelf: 'flex-start'`

```tsx
// 错误：按钮撑满整行
buttonStyle: {
    backgroundColor: '#fff',
    borderRadius: 20,
}

// 正确：按钮宽度自适应内容
buttonStyle: {
    alignSelf: 'flex-start',  // 关键
    backgroundColor: '#fff',
    borderRadius: 20,
}
```

---

## 8. 模糊效果 (backdrop-filter)

### 8.1 @react-native-community/blur

**问题描述：** RN 不支持 CSS `backdrop-filter: blur()`

**解决方案：** 使用 `@react-native-community/blur`

```bash
pnpm add @react-native-community/blur
cd ios && pod install
```

**RN 代码：**

```tsx
import {BlurView} from '@react-native-community/blur';

<BlurView
    style={styles.blurContainer}
    blurType='light'
    blurAmount={30}
    reducedTransparencyFallbackColor='rgba(255,255,255,0.6)'
>
    {children}
</BlurView>;
```

**平台差异：** | 特性 | iOS | Android | |------|-----|---------| | blurAmount 最大值 | 无限制 | 32 |
| VibrancyView | ✅ 支持 | ❌ 不支持 | | 性能 | 优秀 | 良好 |

**blurType 选项：** `light`, `dark`, `xlight`, `prominent`, `regular`

---

## 9. IM 页面键盘处理

### 9.1 KeyboardAvoidingView 配置

**问题描述：** IM 聊天页面输入框聚焦时，键盘需要将整个输入区域（OperatingArea）推上去，而不是遮挡。

**解决方案：** 使用 RN 内置 `KeyboardAvoidingView`

```tsx
import {KeyboardAvoidingView, Platform} from 'react-native';
import {useSafeAreaInsets} from 'react-native-safe-area-context';

const insets = useSafeAreaInsets();

<KeyboardAvoidingView
    style={{flex: 1}}
    behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    keyboardVerticalOffset={Platform.OS === 'ios' ? 49 + insets.bottom : 49}
>
    <SessionContent style={{flex: 1}} />
    <OperatingArea />
</KeyboardAvoidingView>;
```

**偏移量计算：**

| 场景     | iOS offset                  | Android offset |
| -------- | --------------------------- | -------------- |
| 全屏页面 | `0`                         | `0`            |
| Tab 页面 | `49 + insets.bottom`        | `49`           |
| 有导航栏 | `navHeight + insets.bottom` | `navHeight`    |

- `49` = Tab Bar 标准高度
- `insets.bottom` = Home Indicator 高度（iPhone X+ 约 34px）
- Android 使用 `behavior="height"` 配合 `adjustResize`

---

## 10. React 版本冲突

### 10.1 问题描述

**错误信息：**

```
TypeError: Cannot read property 'ReactCurrentDispatcher' of undefined
```

**根因：** 项目中存在多个 React 实例，可能由于：

- 不同包依赖了不同版本的 React
- 原生依赖解析到了错误的 React 版本

### 10.2 解决方案

**1. package.json 添加 overrides/resolutions：**

```json
{
    "resolutions": {
        "react": "19.2.0"
    }
}
```

**2. Metro 配置强制 React 解析（metro.config.js）：**

```javascript
const localReact = path.resolve(projectRoot, 'node_modules/react');

resolver: {
    resolveRequest: (context, moduleName, platform) => {
        if (moduleName === 'react' || moduleName.startsWith('react/')) {
            const subPath =
                moduleName === 'react' ? 'index.js' : moduleName.replace('react/', '') + '.js';
            return {filePath: path.resolve(localReact, subPath), type: 'sourceFile'};
        }
        return context.resolveRequest(context, moduleName, platform);
    };
}
```

---

## 附录：Monorepo 特有问题

> 以下问题仅在 pnpm/yarn workspaces 等 Monorepo 环境中出现

### A.1 pnpm 依赖提升问题

**问题描述：** pnpm 将依赖提升到根目录 `node_modules`，但 RN 原生构建工具期望依赖在项目本地。

**解决方案：** 在 `postinstall` 脚本中创建符号链接

```javascript
// scripts/setup-symlinks.js
const SYMLINKS = [
    {local: 'apps/rn-app/node_modules/react-native', target: 'node_modules/react-native'},
    {local: 'apps/rn-app/node_modules/@react-native/gradle-plugin', target: 'node_modules/@react-native/gradle-plugin'}
];
```

### A.2 CocoaPods .pnpm 路径问题

**问题描述：** CocoaPods 返回 `.pnpm` 内部虚拟路径，该路径不存在。

**解决方案：** 创建 `.pnpm` 目录符号链接

```javascript
{
    local: 'node_modules/.pnpm/hermes-compiler@0.14.0/node_modules/hermes-compiler',
    target: 'node_modules/hermes-compiler'
}
```

### A.3 Metro 端口冲突

**解决方案：** 使用 `--no-packager` 参数分离 Metro

```json
{
    "scripts": {
        "rn:android": "pnpm --filter rn-app android -- --no-packager"
    }
}
```

### A.4 React 版本冲突（Monorepo 特有）

**根因：** Monorepo 中多个包依赖不同 React 版本

**解决方案：** 根 package.json 添加 pnpm overrides

```json
{
    "pnpm": {
        "overrides": {
            "react-native-reanimated>react": "19.2.0"
        }
    }
}
```

---

## 更新记录

| 日期       | 更新内容                                                        |
| ---------- | --------------------------------------------------------------- |
| 2026-01-21 | 简化文档结构，合并 Monorepo 问题到附录                          |
| 2026-01-08 | 添加 IM 页面键盘处理方案（KeyboardAvoidingView 配置）           |
| 2026-01-08 | 添加 React 版本冲突解决方案                                     |
| 2026-01-07 | 添加 Flex 布局宽度计算问题（onLayout 方案、alignSelf）          |
| 2026-01-07 | 添加 @react-native-community/blur 模糊效果                      |
| 2025-12-31 | 添加 ScrollView 滚动监听与分页加载方案（ScrollAnchor）          |
| 2025-12-29 | 添加 @quidone/react-native-wheel-picker 依赖（地址选择器）      |
| 2025-12-19 | 添加 react-native-image-picker、react-native-image-viewing 依赖 |
| 2025-12-17 | 初始文档创建，记录渐变、设计稿尺寸、Image、阴影、键盘等问题     |
