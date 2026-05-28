---
name: code-review
description: cloudflare-operator 项目代码审查。检查代码质量标准、安全问题和最佳实践。适用于审查 PR、提交前检查代码或验证变更。
allowed-tools: Read, Grep, Glob, Bash
user-invocable: true
---

# 代码审查标准

## 概述

根据 cloudflare-operator 项目标准审查代码变更。此技能检查常见问题并确保符合项目规范。

## 快速审查命令

```bash
# 运行所有检查
make fmt vet test lint

# 检查特定文件
go vet ./path/to/file.go
```

## 严重检查项 (P0 - 必须修复)

### 1. 状态更新未使用重试

**错误写法：**
```go
obj.Status.State = "active"
r.Status().Update(ctx, obj)
```

**正确写法：**
```go
controller.UpdateStatusWithConflictRetry(ctx, r.Client, obj, func() {
    obj.Status.State = "active"
})
```

### 2. Finalizer 未使用重试

**错误写法：**
```go
controllerutil.RemoveFinalizer(obj, FinalizerName)
r.Update(ctx, obj)
```

**正确写法：**
```go
controller.UpdateWithConflictRetry(ctx, r.Client, obj, func() {
    controllerutil.RemoveFinalizer(obj, FinalizerName)
})
```

### 3. 事件中包含敏感数据

**错误写法：**
```go
r.Recorder.Event(obj, "Warning", "Failed", err.Error())
```

**正确写法：**
```go
r.Recorder.Event(obj, "Warning", "Failed", cf.SanitizeErrorMessage(err))
```

### 4. 删除时未检查 NotFound

**错误写法：**
```go
if err := r.cfAPI.Delete(id); err != nil {
    return err
}
```

**正确写法：**
```go
if err := r.cfAPI.Delete(id); err != nil {
    if !cf.IsNotFoundError(err) {
        return err
    }
    // 已删除
}
```

### 5. 集群作用域资源使用空命名空间

**错误写法：**
```go
cf.NewAPIClientFromDetails(ctx, r.Client, "", obj.Spec.Cloudflare)
```

**正确写法：**
```go
cf.NewAPIClientFromDetails(ctx, r.Client, controller.OperatorNamespace, obj.Spec.Cloudflare)
```

## 重要检查项 (P1 - 应该修复)

### 6. 条件管理

**错误写法：**
```go
obj.Status.Conditions = append(obj.Status.Conditions, condition)
```

**正确写法：**
```go
meta.SetStatusCondition(&obj.Status.Conditions, metav1.Condition{
    Type:               "Ready",
    Status:             metav1.ConditionTrue,
    Reason:             "Reconciled",
    ObservedGeneration: obj.Generation,
})
```

### 7. 缺少依赖资源 Watch

如果资源引用其他资源（Tunnel、VirtualNetwork），必须添加 Watch：

```go
func (r *Reconciler) SetupWithManager(mgr ctrl.Manager) error {
    return ctrl.NewControllerManagedBy(mgr).
        For(&v1alpha2.MyResource{}).
        Watches(&v1alpha2.Tunnel{},
            handler.EnqueueRequestsFromMapFunc(r.findResourcesForTunnel)).
        Complete(r)
}
```

### 8. 删除时错误聚合

删除多个项目时，聚合错误：

```go
var errs []error
for _, item := range items {
    if err := delete(item); err != nil {
        errs = append(errs, err)
    }
}
if len(errs) > 0 {
    return errors.Join(errs...)  // 不移除 finalizer
}
// 全部成功，移除 finalizer
```

## 审查清单

### 控制器逻辑
- [ ] Finalizer 在任何 Cloudflare 操作之前添加
- [ ] 只有清理成功后才移除 Finalizer
- [ ] 状态更新使用冲突重试
- [ ] 删除检查 NotFound 错误
- [ ] 错误消息已清理敏感信息

### API 类型
- [ ] 正确的 kubebuilder 标记
- [ ] Status 有 ObservedGeneration
- [ ] Status 有 Conditions 切片
- [ ] 作用域正确设置（Cluster 或 Namespaced）

### 安全
- [ ] 无硬编码凭证
- [ ] Secrets 通过 K8s Secret API 访问
- [ ] RBAC 权限最小化

### 测试
- [ ] `make test` 通过
- [ ] `make lint` 通过
- [ ] 无新的 lint 警告

## 运行审查

```bash
# 检查常见问题
grep -r "r.Status().Update" internal/controller/
grep -r "r.Update(ctx" internal/controller/ | grep -v "UpdateWithConflictRetry"
grep -r 'err.Error()' internal/controller/ | grep -i event
grep -r 'NewAPIClientFromDetails.*""' internal/controller/

# 运行完整验证
make fmt vet test lint build
```

## 输出格式

审查时，按以下格式报告问题：

```
## 审查结果

### P0 - 严重（必须修复）
- [文件:行号] 问题描述

### P1 - 重要（应该修复）
- [文件:行号] 问题描述

### 建议
- [文件:行号] 建议内容

### 汇总
- 总问题数：X（P0: Y, P1: Z）
- 测试：通过/失败
- Lint：通过/失败
```
