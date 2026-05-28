---
name: crd-development
description: 为 Cloudflare Operator 开发新的 Kubernetes CRD。适用于创建新 CRD 类型、实现控制器或添加 Cloudflare API 集成。触发词："添加 CRD"、"新资源"、"实现控制器"。
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
user-invocable: true
---

# CRD 开发指南

## 概述

此技能指导为 Cloudflare Operator 开发新的自定义资源定义（CRD），遵循已建立的模式和最佳实践。

## 项目结构

```
api/v1alpha2/           # CRD 类型定义
internal/controller/    # 控制器实现
internal/clients/cf/    # Cloudflare API 客户端
```

## 步骤 1：定义 API 类型

创建 `api/v1alpha2/<资源>_types.go`：

```go
// +kubebuilder:object:root=true
// +kubebuilder:subresource:status
// +kubebuilder:resource:scope=Cluster,shortName=<简称>
// +kubebuilder:printcolumn:name="State",type=string,JSONPath=`.status.state`
// +kubebuilder:printcolumn:name="Age",type=date,JSONPath=`.metadata.creationTimestamp`
type MyResource struct {
    metav1.TypeMeta   `json:",inline"`
    metav1.ObjectMeta `json:"metadata,omitempty"`

    Spec   MyResourceSpec   `json:"spec,omitempty"`
    Status MyResourceStatus `json:"status,omitempty"`
}

type MyResourceSpec struct {
    // Cloudflare API 凭证
    Cloudflare CloudflareDetails `json:"cloudflare,omitempty"`

    // 资源特定字段
    Name    string `json:"name,omitempty"`
    Comment string `json:"comment,omitempty"`
}

type MyResourceStatus struct {
    // Cloudflare 资源 ID
    ResourceID string `json:"resourceId,omitempty"`

    // Account ID 用于验证
    AccountID string `json:"accountId,omitempty"`

    // 当前状态
    State string `json:"state,omitempty"`

    // ObservedGeneration 用于漂移检测
    ObservedGeneration int64 `json:"observedGeneration,omitempty"`

    // Conditions 用于状态报告
    Conditions []metav1.Condition `json:"conditions,omitempty"`
}
```

## 步骤 2：实现控制器

创建 `internal/controller/<资源>/controller.go`：

```go
func (r *Reconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    // 1. 获取资源
    obj := &v1alpha2.MyResource{}
    if err := r.Get(ctx, req.NamespacedName, obj); err != nil {
        if apierrors.IsNotFound(err) {
            return ctrl.Result{}, nil
        }
        return ctrl.Result{}, err
    }

    // 2. 初始化 API 客户端（集群作用域使用 OperatorNamespace）
    api, err := cf.NewAPIClientFromDetails(r.ctx, r.Client,
        controller.OperatorNamespace, obj.Spec.Cloudflare)
    if err != nil {
        return ctrl.Result{}, err
    }

    // 3. 处理删除
    if obj.GetDeletionTimestamp() != nil {
        return r.handleDeletion()
    }

    // 4. 添加 Finalizer
    if !controllerutil.ContainsFinalizer(obj, FinalizerName) {
        controllerutil.AddFinalizer(obj, FinalizerName)
        if err := r.Update(ctx, obj); err != nil {
            return ctrl.Result{}, err
        }
    }

    // 5. 协调
    return r.reconcile()
}
```

## 必需模式

### 状态更新（必须使用重试）

```go
err := controller.UpdateStatusWithConflictRetry(ctx, r.Client, obj, func() {
    obj.Status.State = "active"
    controller.SetSuccessCondition(&obj.Status.Conditions, "Reconciled")
})
```

### Finalizer 操作（必须使用重试）

```go
err := controller.UpdateWithConflictRetry(ctx, r.Client, obj, func() {
    controllerutil.RemoveFinalizer(obj, FinalizerName)
})
```

### 错误处理（必须清理敏感信息）

```go
r.Recorder.Event(obj, corev1.EventTypeWarning, "Failed",
    cf.SanitizeErrorMessage(err))
```

### 删除（必须检查 NotFound）

```go
if err := r.cfAPI.Delete(id); err != nil {
    if !cf.IsNotFoundError(err) {
        return err
    }
    // 已删除，继续
}
```

## 步骤 3：生成代码

```bash
make manifests generate  # 生成 CRD 和 DeepCopy
make fmt vet            # 格式化和检查
make test               # 运行测试
```

## 步骤 4：注册控制器

添加到 `cmd/main.go`：

```go
if err = (&myresource.Reconciler{
    Client: mgr.GetClient(),
    Scheme: mgr.GetScheme(),
}).SetupWithManager(mgr); err != nil {
    setupLog.Error(err, "无法创建控制器", "controller", "MyResource")
    os.Exit(1)
}
```

## 作用域规则

| 作用域 | 命名空间参数 | Secret 位置 |
|--------|-------------|-------------|
| Namespaced | `obj.Namespace` | 相同命名空间 |
| Cluster | `controller.OperatorNamespace` | cloudflare-operator-system |

## 检查清单

- [ ] API 类型有正确的 kubebuilder 标记
- [ ] 控制器有 Finalizer 和删除处理
- [ ] 状态更新使用冲突重试
- [ ] 错误消息已清理敏感信息
- [ ] 删除时检查 NotFound
- [ ] 在 main.go 中注册
- [ ] 使用 `make manifests` 生成 CRD
- [ ] 使用 `make test` 测试通过

## Cloudflare API 客户端方法

添加新方法到 `internal/clients/cf/` 目录：

```go
// 创建资源
func (api *API) CreateMyResource(params MyResourceParams) (*MyResourceResult, error) {
    // 实现 Cloudflare API 调用
}

// 获取资源
func (api *API) GetMyResource(id string) (*MyResourceResult, error) {
    // 实现
}

// 更新资源
func (api *API) UpdateMyResource(id string, params MyResourceParams) (*MyResourceResult, error) {
    // 实现
}

// 删除资源
func (api *API) DeleteMyResource(id string) error {
    // 实现
}

// 按名称查找
func (api *API) GetMyResourceByName(name string) (*MyResourceResult, error) {
    // 实现
}
```

## 测试模板

创建 `internal/controller/<资源>/controller_test.go`：

```go
var _ = Describe("MyResource Controller", func() {
    Context("When creating MyResource", func() {
        It("Should create the resource in Cloudflare", func() {
            // 测试创建逻辑
        })
    })

    Context("When deleting MyResource", func() {
        It("Should delete the resource from Cloudflare", func() {
            // 测试删除逻辑
        })

        It("Should handle NotFound gracefully", func() {
            // 测试 NotFound 处理
        })
    })
})
```
