# Android API 设计最佳实践

## 概述
本文档总结 Android 平台在 API 设计方面的核心最佳实践，为 OpenHarmony API 设计提供参考。

## 核心原则

### 1. 一致性（Consistency）
- **命名规范**：使用清晰、一致的命名约定
  - 动词开头表示动作（如 `get`, `set`, `enable`, `disable`）
  - 名词表示状态或属性
  - 布尔值使用 `is` 或 `has` 前缀
- **参数顺序**：相同类型的 API 保持一致的参数顺序
- **返回值约定**：成功返回数据或 `true`，失败抛出异常或返回 `false`

### 2. 易用性（Usability）
- **最小惊讶原则**：API 行为应符合开发者的直觉
- **合理的默认值**：为可选参数提供合理的默认值
- **Builder 模式**：对于复杂对象的构建，使用 Builder 模式简化 API
  - 例：`NotificationCompat.Builder`

### 3. 安全性（Security）
- **权限检查**：在 API 入口处检查权限
  - 使用 `@RequiresPermission` 注解声明所需权限
- **输入验证**：验证所有外部输入
- **异常处理**：使用明确的异常类型，提供清晰的错误信息

### 4. 性能（Performance）
- **避免阻塞主线程**：耗时操作使用异步 API
  - 提供回调、Future 或协程支持
- **资源管理**：明确资源的生命周期和释放时机
- **缓存策略**：对于重复调用的操作，提供缓存机制

## 典型模式

### 监听器模式（Listener Pattern）
```java
interface OnClickListener {
    void onClick(View v);
}

void setOnClickListener(OnClickListener listener);
```

### 回调模式（Callback Pattern）
```java
interface Callback<T> {
    void onSuccess(T result);
    void onFailure(Exception e);
}
```

### 构建器模式（Builder Pattern）
```java
Notification notification = new NotificationCompat.Builder(context)
    .setContentTitle("标题")
    .setContentText("内容")
    .setPriority(NotificationCompat.PRIORITY_HIGH)
    .build();
```

## 参考资源
- Android API Guidelines: https://developer.android.com/guide
- Material Design: https://material.io/design
