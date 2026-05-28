# Android 架构最佳实践

## 概述
本文档总结 Android 平台在架构设计方面的核心模式和最佳实践。

## 核心架构模式

### 1. MVVM（Model-View-ViewModel）
- **推荐架构**：Android 官方推荐的架构模式
- **核心组件**：
  - **Model**：数据层（Repository、DataSource）
  - **View**：UI 层（Activity、Fragment）
  - **ViewModel**：业务逻辑层，持有 UI 状态
- **优势**：
  - 分离关注点
  - 易于测试
  - 生命周期感知

### 2. 单向数据流（Unidirectional Data Flow）
- **原则**：数据从 ViewModel 流向 View，事件从 View 流向 ViewModel
- **实现**：
  - 使用 `LiveData` 或 `StateFlow` 暴露状态
  - View 通过方法调用触发事件
  - ViewModel 更新状态，View 自动响应

### 3. 依赖注入（Dependency Injection）
- **推荐框架**：Hilt（基于 Dagger）
- **优势**：
  - 解耦组件
  - 易于测试（可注入 Mock 对象）
  - 自动管理生命周期

## 分层架构

### UI 层（Presentation Layer）
- **职责**：显示数据、处理用户交互
- **组件**：Activity、Fragment、Composable
- **原则**：
  - 不包含业务逻辑
  - 通过 ViewModel 获取数据
  - 观察状态变化并更新 UI

### 领域层（Domain Layer）
- **职责**：封装业务逻辑
- **组件**：UseCase、Interactor
- **原则**：
  - 独立于框架
  - 可复用
  - 易于测试

### 数据层（Data Layer）
- **职责**：数据获取和持久化
- **组件**：Repository、DataSource（Remote/Local）
- **原则**：
  - 单一数据源（Single Source of Truth）
  - 离线优先（Offline-First）
  - 数据缓存策略

## 关键组件

### ViewModel
```kotlin
class MyViewModel : ViewModel() {
    private val _uiState = MutableStateFlow(UiState())
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()

    fun onEvent(event: UiEvent) {
        // 处理事件，更新状态
    }
}
```

### Repository
```kotlin
class MyRepository(
    private val remoteDataSource: RemoteDataSource,
    private val localDataSource: LocalDataSource
) {
    fun getData(): Flow<Result<Data>> = flow {
        // 先返回本地缓存
        emit(localDataSource.getData())
        // 再从网络获取最新数据
        val result = remoteDataSource.getData()
        if (result.isSuccess) {
            localDataSource.saveData(result.data)
            emit(result)
        }
    }
}
```

## 参考资源
- Guide to app architecture: https://developer.android.com/topic/architecture
- Android Architecture Components: https://developer.android.com/topic/libraries/architecture
