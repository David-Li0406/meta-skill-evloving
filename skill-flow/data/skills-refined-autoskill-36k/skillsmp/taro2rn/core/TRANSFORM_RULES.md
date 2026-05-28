# Taro to React Native 转换规则

本文档定义 Taro 代码转换为 React Native 代码的规则，供模型直接生成使用。

> **注意**：本文档为通用转换规则，项目特定配置请参考 `taro2rnTODO.md`。

---

## 一、组件映射

### 1.1 基础组件

| Taro 组件           | RN 组件                       | 来源         | 说明             |
| ------------------- | ----------------------------- | ------------ | ---------------- |
| `<View>`            | `<View>`                      | react-native | 直接对应         |
| `<Text>`            | `<Text>`                      | react-native | 直接对应         |
| `<Image src={url}>` | `<Image source={{uri: url}}>` | react-native | src 改为 source  |
| `<ScrollView>`      | `<ScrollView>`                | react-native | 属性映射见下     |
| `<Input>`           | `<TextInput>`                 | react-native | 属性映射见下     |
| `<Textarea>`        | `<TextInput multiline>`       | react-native | 添加 multiline   |
| `<Button>`          | `<TouchableOpacity>`          | react-native | 需包装 Text      |
| `<Switch>`          | `<Switch>`                    | react-native | checked -> value |
| `<Block>`           | `<>` 或 `<Fragment>`          | react        | 空标签           |

### 1.2 View 点击事件

```tsx
// Taro
<View onClick={handleClick}>内容</View>

// RN - 需要包装 TouchableOpacity
<TouchableOpacity onPress={handleClick}>
  <View>内容</View>
</TouchableOpacity>

// 或者直接用 Pressable
<Pressable onPress={handleClick}>
  <View>内容</View>
</Pressable>
```

### 1.3 Image 组件

```tsx
// Taro
<Image src={imageUrl} mode="aspectFill" />

// RN
<Image source={{uri: imageUrl}} resizeMode="cover" />

// mode 映射：
// aspectFit -> contain
// aspectFill -> cover
// scaleToFill -> stretch
// widthFix -> contain (需设置宽度，高度 auto)
```

### 1.4 Input 组件

```tsx
// Taro
<Input
  value={value}
  type="number"
  placeholder="请输入"
  maxlength={10}
  disabled={false}
  onInput={(e) => setValue(e.detail.value)}
  onConfirm={handleSubmit}
/>

// RN
<TextInput
  value={value}
  keyboardType="numeric"
  placeholder="请输入"
  maxLength={10}
  editable={true}
  onChangeText={(text) => setValue(text)}
  onSubmitEditing={handleSubmit}
/>

// type 映射：
// text -> default
// number -> numeric
// digit -> decimal-pad
// tel -> phone-pad
// idcard -> default
```

### 1.5 ScrollView 属性

```tsx
// Taro
<ScrollView
  scrollY
  scrollX={false}
  onScrollToLower={loadMore}
  refresherEnabled
  onRefresherRefresh={onRefresh}
>

// RN
<ScrollView
  horizontal={false}
  onEndReached={loadMore}
  onEndReachedThreshold={0.1}
  refreshControl={
    <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
  }
>
```

### 1.6 列表渲染

```tsx
// Taro - ScrollView + map
<ScrollView>
  {list.map(item => <View key={item.id}>{item.name}</View>)}
</ScrollView>

// RN - 优先使用 FlatList
<FlatList
  data={list}
  keyExtractor={(item) => item.id}
  renderItem={({item}) => <View><Text>{item.name}</Text></View>}
/>
```

### 1.7 Swiper 组件

```tsx
// Taro
<Swiper
    autoplay
    interval={3000}
    circular
    indicatorDots
    current={0}
    onChange={e => setCurrent(e.detail.current)}
>
    <SwiperItem>...</SwiperItem>
</Swiper>;

// RN - 使用 react-native-swiper 或 react-native-pager-view
import Swiper from 'react-native-swiper';

<Swiper
    autoplay
    autoplayTimeout={3}
    loop
    showsPagination
    index={0}
    onIndexChanged={index => setCurrent(index)}
>
    <View>...</View>
</Swiper>;
```

### 1.8 Picker 组件

```tsx
// Taro
<Picker mode='selector' range={options} onChange={handleChange}>
    <View>选择</View>
</Picker>;

// RN - 使用 @react-native-picker/picker 或自定义 Modal
import {Picker} from '@react-native-picker/picker';

<Picker selectedValue={value} onValueChange={handleChange}>
    {options.map(opt => (
        <Picker.Item key={opt} label={opt} value={opt} />
    ))}
</Picker>;

// 日期选择器
// Taro: <Picker mode="date">
// RN: 使用 @react-native-community/datetimepicker
```

---

## 二、API 映射

### 2.1 路由导航

```tsx
// Taro
import Taro from '@tarojs/taro';
Taro.navigateTo({url: '/pages/detail/index?id=1'});
Taro.redirectTo({url: '/pages/home/index'});
Taro.navigateBack({delta: 1});
Taro.switchTab({url: '/pages/tab/index'});

// RN - 使用 React Navigation
import {useNavigation} from '@react-navigation/native';
const navigation = useNavigation();

navigation.navigate('Detail', {id: '1'});
navigation.replace('Home');
navigation.goBack();
navigation.navigate('Tab'); // Tab Navigator
```

### 2.2 存储

```tsx
// Taro - 同步
Taro.setStorageSync('key', value);
const data = Taro.getStorageSync('key');
Taro.removeStorageSync('key');

// RN - 异步 AsyncStorage
import AsyncStorage from '@react-native-async-storage/async-storage';

await AsyncStorage.setItem('key', JSON.stringify(value));
const data = JSON.parse(await AsyncStorage.getItem('key'));
await AsyncStorage.removeItem('key');

// 封装为同步风格的 hook 使用
```

### 2.3 网络请求

```tsx
// Taro
Taro.request({
    url: 'https://api.example.com/data',
    method: 'POST',
    data: {id: 1},
    header: {'Content-Type': 'application/json'},
    success: res => console.log(res.data),
    fail: err => console.error(err)
});

// RN - 使用 fetch 或 axios
const response = await fetch('https://api.example.com/data', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({id: 1})
});
const data = await response.json();

// 或使用项目封装的 httpRequest
```

### 2.4 UI 反馈

```tsx
// Taro
Taro.showToast({title: '成功', icon: 'success', duration: 2000});
Taro.hideToast();
Taro.showLoading({title: '加载中'});
Taro.hideLoading();
Taro.showModal({title: '提示', content: '确定删除？', showCancel: true});

// RN - 使用封装组件或第三方库
// 常用方案：react-native-toast-message, react-native-modal
import Toast from 'react-native-toast-message';

Toast.show({type: 'success', text1: '成功'});
```

### 2.5 系统信息

```tsx
// Taro
const systemInfo = Taro.getSystemInfoSync();
const {screenWidth, screenHeight, platform} = systemInfo;

// RN
import {Dimensions, Platform, PixelRatio} from 'react-native';

const {width: screenWidth, height: screenHeight} = Dimensions.get('window');
const platform = Platform.OS; // 'ios' | 'android'
const pixelRatio = PixelRatio.get();
```

### 2.6 设备能力

```tsx
// Taro
Taro.vibrateShort();
Taro.setClipboardData({data: 'text'});
const {data} = await Taro.getClipboardData();

// RN
import {Vibration} from 'react-native';
import Clipboard from '@react-native-clipboard/clipboard';

Vibration.vibrate(50);
Clipboard.setString('text');
const text = await Clipboard.getString();
```

### 2.7 图片操作

```tsx
// Taro
const res = await Taro.chooseImage({count: 9, sourceType: ['album', 'camera']});
Taro.previewImage({urls: imageList, current: imageList[0]});

// RN
import {launchImageLibrary} from 'react-native-image-picker';

const result = await launchImageLibrary({mediaType: 'photo', selectionLimit: 9});

// 图片预览可使用 react-native-image-viewing
```

---

## 三、生命周期和 Hooks

### 3.1 页面生命周期

```tsx
// Taro
import {useDidShow, useDidHide, usePullDownRefresh} from '@tarojs/taro';

useDidShow(() => {
    console.log('页面显示');
});

useDidHide(() => {
    console.log('页面隐藏');
});

// RN - 使用 React Navigation hooks
import {useFocusEffect} from '@react-navigation/native';
import {useCallback} from 'react';

useFocusEffect(
    useCallback(() => {
        console.log('页面显示');
        return () => {
            console.log('页面隐藏');
        };
    }, [])
);
```

### 3.2 路由参数

```tsx
// Taro
import {useRouter} from '@tarojs/taro';
const router = useRouter();
const {id, type} = router.params;

// 或
const instance = Taro.getCurrentInstance();
const params = instance.router?.params;

// RN
import {useRoute} from '@react-navigation/native';
const route = useRoute();
const {id, type} = route.params;
```

### 3.3 下拉刷新

```tsx
// Taro
usePullDownRefresh(() => {
  fetchData().then(() => {
    Taro.stopPullDownRefresh();
  });
});

// RN - 使用 RefreshControl
const [refreshing, setRefreshing] = useState(false);

const onRefresh = async () => {
  setRefreshing(true);
  await fetchData();
  setRefreshing(false);
};

<ScrollView
  refreshControl={
    <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
  }
>
```

### 3.4 触底加载

```tsx
// Taro
useReachBottom(() => {
  loadMore();
});

// RN - FlatList
<FlatList
  onEndReached={loadMore}
  onEndReachedThreshold={0.1}
/>

// 或 ScrollView
const handleScroll = (event) => {
  const {layoutMeasurement, contentOffset, contentSize} = event.nativeEvent;
  const isCloseToBottom = layoutMeasurement.height + contentOffset.y >= contentSize.height - 20;
  if (isCloseToBottom) loadMore();
};

<ScrollView onScroll={handleScroll} scrollEventThrottle={400}>
```

---

## 四、样式转换

### 4.1 基本规则

```tsx
// Taro - CSS Modules (.module.less)
import styles from './index.module.less';
<View className={styles.container}>

// RN - StyleSheet
import {styles} from './styles';
<View style={styles.container}>
```

### 4.2 单位转换

**重要：开始样式转换前，必须先确认以下事项：**

1. **询问确认视觉稿标准**：750 还是 1242？

    - 750 标准 → 使用 `rpx()` 函数
    - 1242 标准 → 使用 `rpx1242()` 函数

2. **检查 rpx 工具函数是否已封装**：
    - 检查路径：参考 `taro2rnTODO.md` 中的 rpx 文件路径
    - 如未封装，需先创建（见下方封装代码）

```less
/* Taro LESS - 750 设计稿 */
.container {
    width: 750rpx; /* 全屏宽 */
    padding: 24rpx;
    font-size: 28rpx;
    margin: 20px;
}
```

```tsx
// RN StyleSheet - 750 设计稿使用 rpx()
import {rpx} from 'your-rn-core-package'; // 参考配置文件中的包映射

export const styles = StyleSheet.create({
    container: {
        width: '100%', // 750rpx = 100%
        padding: rpx(24), // rpx 转换函数
        fontSize: rpx(28),
        margin: 20 // px 直接用数字
    }
});
```

```tsx
// RN StyleSheet - 1242 设计稿使用 rpx1242()
import {rpx1242} from 'your-rn-core-package';

export const styles = StyleSheet.create({
    container: {
        width: '100%',
        padding: rpx1242(40),
        fontSize: rpx1242(46),
        margin: 20
    }
});
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

**单位转换对照表：**

| 视觉稿标准 | 原始值  | 转换函数                    | 在 375 屏幕上的实际值 |
| ---------- | ------- | --------------------------- | --------------------- |
| 750        | 24rpx   | `rpx(24)`                   | 12pt                  |
| 750        | 750rpx  | `rpx(750)` 或 `'100%'`      | 375pt (全屏宽)        |
| 1242       | 24rpx   | `rpx1242(24)`               | ~7.3pt                |
| 1242       | 1242rpx | `rpx1242(1242)` 或 `'100%'` | 375pt (全屏宽)        |

### 4.3 Flex 布局

```less
/* Taro */
.row {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
}
```

```tsx
// RN - display: flex 是默认值，可省略
row: {
  flexDirection: 'row',
  justifyContent: 'space-between',
  alignItems: 'center',
},
```

### 4.4 文字样式

```less
/* Taro */
.title {
    color: #333;
    font-size: 32rpx;
    font-weight: bold;
    line-height: 44rpx;
    text-align: center;
    text-overflow: ellipsis;
    white-space: nowrap;
    overflow: hidden;
}
```

```tsx
// RN - 文字截断用 numberOfLines
title: {
  color: '#333',
  fontSize: rpx(32),
  fontWeight: 'bold',      // 或 '700'
  lineHeight: rpx(44),
  textAlign: 'center',
},

// 组件使用
<Text style={styles.title} numberOfLines={1}>标题</Text>
```

### 4.5 边框和圆角

```less
/* Taro */
.card {
    border: 1px solid #eee;
    border-radius: 16rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}
```

```tsx
// RN
card: {
  borderWidth: 1,
  borderColor: '#eee',
  borderRadius: rpx(16),
  // 阴影 - iOS
  shadowColor: '#000',
  shadowOffset: {width: 0, height: rpx(4)},
  shadowOpacity: 0.1,
  shadowRadius: rpx(12),
  // 阴影 - Android
  elevation: 4,
},
```

### 4.6 定位

```less
/* Taro */
.overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 100;
}
```

```tsx
// RN - 无 fixed，用 absolute + 全屏尺寸
overlay: {
  position: 'absolute',
  top: 0,
  left: 0,
  right: 0,
  bottom: 0,
  zIndex: 100,
},

// 或使用 StyleSheet.absoluteFillObject
overlay: {
  ...StyleSheet.absoluteFillObject,
  zIndex: 100,
},
```

### 4.7 不支持的样式

以下 CSS 特性在 RN 中不支持，需要特殊处理：

| CSS 特性               | RN 替代方案                       |
| ---------------------- | --------------------------------- |
| `::before` / `::after` | 添加实际的 View/Text 子元素       |
| `:hover` / `:active`   | 使用 Pressable 的 style 函数      |
| `transition`           | 使用 Animated API 或 Reanimated   |
| `animation`            | 使用 Animated API 或 Lottie       |
| `background-image`     | 使用 ImageBackground 组件         |
| `linear-gradient`      | 使用 react-native-linear-gradient |
| `backdrop-filter`      | 使用 @react-native-community/blur |
| `@media`               | 使用 Dimensions API 条件判断      |
| `calc()`               | 在 JS 中计算                      |

### 4.8 模糊效果 (backdrop-filter)

```css
/* Taro/CSS */
.blurBg {
    backdrop-filter: blur(30px);
    background: rgba(255, 255, 255, 0.6);
}
```

```tsx
// RN - 使用 @react-native-community/blur
import {BlurView} from '@react-native-community/blur';

<BlurView
    style={styles.blurBg}
    blurType='light'
    blurAmount={30}
    reducedTransparencyFallbackColor='rgba(255,255,255,0.6)'
>
    {children}
</BlurView>;

// blurType: 'light' | 'dark' | 'xlight' | 'prominent' | 'regular'
// blurAmount: Android 最大 32，iOS 无限制
```

### 4.9 动态宽度计算

当子元素宽度需要基于父容器动态计算时，使用 `onLayout` 而非 `Dimensions`：

```tsx
// ❌ 错误：硬编码屏幕宽度，未考虑父容器约束
const itemWidth = (SCREEN_WIDTH - padding) / 3;

// ✅ 正确：使用 onLayout 获取实际容器宽度
const [containerWidth, setContainerWidth] = useState(0);

<View onLayout={e => setContainerWidth(e.nativeEvent.layout.width)}>
    {containerWidth > 0 &&
        items.map(item => <View style={{width: Math.floor(containerWidth / 3)}} />)}
</View>;
```

---

## 五、条件平台代码

### 5.1 平台判断

```tsx
// Taro
if (process.env.TARO_ENV === 'weapp') {
    // 微信小程序
} else if (process.env.TARO_ENV === 'h5') {
    // H5
}

// RN
import {Platform} from 'react-native';

if (Platform.OS === 'ios') {
    // iOS
} else if (Platform.OS === 'android') {
    // Android
}

// 平台特定样式
const styles = StyleSheet.create({
    container: {
        ...Platform.select({
            ios: {paddingTop: 44},
            android: {paddingTop: 0}
        })
    }
});
```

### 5.2 平台特定文件

```
// Taro
index.weapp.tsx
index.h5.tsx

// RN
index.ios.tsx
index.android.tsx
index.native.tsx  // iOS + Android
index.tsx         // 通用
```

---

## 六、事件处理

### 6.1 事件对象

```tsx
// Taro - 事件值在 e.detail
<Input onInput={(e) => setValue(e.detail.value)} />
<ScrollView onScroll={(e) => console.log(e.detail.scrollTop)} />

// RN - 事件值直接传递或在 nativeEvent
<TextInput onChangeText={(text) => setValue(text)} />
<ScrollView onScroll={(e) => console.log(e.nativeEvent.contentOffset.y)} />
```

### 6.2 阻止冒泡

```tsx
// Taro
<View onClick={handleOuter}>
  <View onClick={(e) => { e.stopPropagation(); handleInner(); }}>
    内部
  </View>
</View>

// RN - 使用 onStartShouldSetResponder
<View onPress={handleOuter}>
  <Pressable
    onPress={handleInner}
    onStartShouldSetResponder={() => true}
  >
    <Text>内部</Text>
  </Pressable>
</View>
```

---

## 七、特殊组件处理

### 7.1 Portal / 弹窗

```tsx
// Taro - 自定义 Portal
<Portal>
    <Popup />
</Portal>;

// RN - 使用 Modal 组件
import {Modal} from 'react-native';

<Modal visible={visible} transparent animationType='fade'>
    <View style={styles.overlay}>
        <View style={styles.content}>{children}</View>
    </View>
</Modal>;
```

### 7.2 RichText 富文本

```tsx
// Taro
<RichText nodes={htmlContent} />;

// RN - 使用 react-native-render-html
import RenderHtml from 'react-native-render-html';

<RenderHtml contentWidth={screenWidth} source={{html: htmlContent}} />;
```

### 7.3 WebView

```tsx
// Taro
<WebView src='https://example.com' />;

// RN
import {WebView} from 'react-native-webview';

<WebView source={{uri: 'https://example.com'}} />;
```

---

## 八、导入转换汇总

```tsx
// Taro 导入
import Taro, {useDidShow, useRouter} from '@tarojs/taro';
import {View, Text, Image, ScrollView, Input, Button} from '@tarojs/components';

// RN 导入
import {
    View,
    Text,
    Image,
    ScrollView,
    TextInput,
    TouchableOpacity,
    Platform,
    Dimensions,
    StyleSheet
} from 'react-native';
import {useNavigation, useRoute, useFocusEffect} from '@react-navigation/native';
import {useCallback} from 'react';
```

---

## 九、IM/聊天页面布局

### 9.1 键盘避让布局

IM 页面典型结构：顶部导航 + 消息列表 + 底部输入框。键盘弹出时需将输入框推上去。

```tsx
import {KeyboardAvoidingView, Platform} from 'react-native';
import {useSafeAreaInsets} from 'react-native-safe-area-context';

function IMScreen() {
    const insets = useSafeAreaInsets();

    return (
        <View style={{flex: 1}}>
            <NavBar />
            <KeyboardAvoidingView
                style={{flex: 1}}
                behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
                keyboardVerticalOffset={Platform.OS === 'ios' ? 49 + insets.bottom : 49}
            >
                <View style={{flex: 1}}>
                    <MessageList /> {/* FlatList inverted */}
                </View>
                <InputArea />
            </KeyboardAvoidingView>
        </View>
    );
}
```

### 9.2 消息列表（FlatList inverted）

IM 消息列表使用 `inverted` 模式，新消息在底部，滚动到顶部加载历史：

```tsx
<FlatList
    data={[...messages].reverse()} // 数据反转
    inverted // 列表反转
    renderItem={({item}) => <MessageItem {...item} />}
    onEndReached={loadHistory} // 滚动到顶部(视觉)触发
    onEndReachedThreshold={0.3}
    keyExtractor={item => item.id}
/>
```

### 9.3 keyboardVerticalOffset 计算

| 页面类型               | iOS                  | Android                      |
| ---------------------- | -------------------- | ---------------------------- |
| 全屏页面               | `0`                  | `0`                          |
| Tab 页面               | `49 + insets.bottom` | `49`                         |
| Stack 页面（有导航栏） | `headerHeight`       | `0`（adjustResize 自动处理） |

**说明：**

- `49` = Tab Bar 高度
- `insets.bottom` = 底部安全区（Home Indicator）
- Android 需在 `AndroidManifest.xml` 设置 `android:windowSoftInputMode="adjustResize"`
