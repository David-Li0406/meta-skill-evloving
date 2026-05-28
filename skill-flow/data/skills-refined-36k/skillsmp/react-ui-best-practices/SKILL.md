---
name: react-ui-best-practices
description: React UI 组件开发最佳实践。用于创建、审查或优化 React 组件，确保代码质量、性能和可维护性。
allowed-tools: Read, Grep, Glob, Edit
---

# React UI 最佳实践

## 组件设计原则

### 1. 组件拆分
- 单一职责：每个组件只做一件事
- 可复用性：提取通用逻辑到自定义 hooks
- 组件大小：保持在 200 行以内

### 2. Props 设计
- 使用 TypeScript 定义清晰的 props 接口
- 提供合理的默认值
- 避免过度传递 props（props drilling）

```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}
```

### 3. 状态管理
- 优先使用局部状态
- 状态提升到最近的共同父组件
- 复杂状态使用 useReducer
- 全局状态使用 Context 或状态管理库

### 4. 性能优化
- 使用 React.memo 避免不必要的重渲染
- useMemo 缓存计算结果
- useCallback 缓存函数引用
- 懒加载大型组件：React.lazy + Suspense

```typescript
const HeavyComponent = React.lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <HeavyComponent />
    </Suspense>
  );
}
```

### 5. 样式规范
- 使用 CSS Modules 或 styled-components 避免样式冲突
- Tailwind CSS：使用语义化的类名组合
- 响应式设计：移动优先
- 主题支持：使用 CSS 变量或主题系统

### 6. 错误处理
- 使用 Error Boundaries 捕获组件错误
- 提供友好的错误提示
- 记录错误日志

```typescript
class ErrorBoundary extends React.Component {
  componentDidCatch(error, errorInfo) {
    console.error('Component error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback />;
    }
    return this.props.children;
  }
}
```

### 7. 可访问性 (a11y)
- 使用语义化 HTML 标签
- 添加 ARIA 属性
- 键盘导航支持
- 颜色对比度符合 WCAG 标准

### 8. 代码组织
```
components/
├── Button/
│   ├── Button.tsx
│   ├── Button.test.tsx
│   ├── Button.module.css
│   └── index.ts
```

## 检查清单

创建或审查 React 组件时，检查以下项：

- [ ] TypeScript 类型定义完整
- [ ] Props 有合理的默认值
- [ ] 使用了适当的性能优化
- [ ] 样式没有全局污染
- [ ] 可访问性符合标准
- [ ] 错误处理完善
- [ ] 组件可测试
- [ ] 代码简洁易读
