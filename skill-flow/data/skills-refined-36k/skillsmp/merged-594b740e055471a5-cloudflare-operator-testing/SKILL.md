---
name: cloudflare-operator-testing
description: Use this skill for code review and end-to-end testing of the Cloudflare Operator, ensuring code quality and validating CRD functionality against the real Cloudflare API.
---

# Cloudflare Operator Testing and Code Review

## 概述

此技能结合了对 Cloudflare Operator 项目的代码审查和端到端测试。它确保代码符合质量标准，并指导如何针对真实 Cloudflare API 进行测试。

## 代码审查标准

### 快速审查命令

```bash
# 运行所有检查
make fmt vet test lint

# 检查特定文件
go vet ./path/to/file.go
```

### 严重检查项 (P0 - 必须修复)

1. **状态更新未使用重试**
   ```go
   obj.Status.State = "active"
   r.Status().Update(ctx, obj)
   ```

2. **Finalizer 未使用重试**
   ```go
   controllerutil.RemoveFinalizer(obj, FinalizerName)
   r.Update(ctx, obj)
   ```

3. **事件中包含敏感数据**
   ```go
   r.Recorder.Event(obj, "Warning", "Failed", err.Error())
   ```

4. **删除时未检查 NotFound**
   ```go
   if err := r.cfAPI.Delete(id); err != nil {
       return err
   }
   ```

5. **集群作用域资源使用空命名空间**
   ```go
   cf.NewAPIClientFromDetails(ctx, r.Client, "", obj.Spec.Cloudflare)
   ```

### 重要检查项 (P1 - 应该修复)

6. **条件管理**
   ```go
   obj.Status.Conditions = append(obj.Status.Conditions, condition)
   ```

7. **缺少依赖资源 Watch**
   ```go
   func (r *Reconciler) SetupWithManager(mgr ctrl.Manager) error {
       return ctrl.NewControllerManagedBy(mgr).
           For(&v1alpha2.MyResource{}).
           Watches(&v1alpha2.Tunnel{},
               handler.EnqueueRequestsFromMapFunc(r.findResourcesForTunnel)).
           Complete(r)
   }
   ```

8. **删除时错误聚合**
   ```go
   var errs []error
   for _, item := range items {
       if err := delete(item); err != nil {
           errs = append(errs, err)
       }
   }
   ```

## 端到端测试指南

### 前置条件

- **必需凭证**
  - Cloudflare API Token 或 Global API Key
  - Cloudflare Account ID
  - Cloudflare Domain（用于 DNS 相关测试）

- **必需权限**
  | 功能 | 权限 | 范围 |
  |------|------|------|
  | Tunnel | `Account:Cloudflare Tunnel:Edit` | Account |
  | DNS | `Zone:DNS:Edit` | Zone |
  | Access | `Account:Access: Apps and Policies:Edit` | Account |
  | Zero Trust | `Account:Zero Trust:Edit` | Account |

### 设置

1. **部署 Operator**
   ```bash
   kubectl apply -f https://github.com/StringKe/cloudflare-operator/releases/latest/download/cloudflare-operator.crds.yaml
   kubectl apply -f https://github.com/StringKe/cloudflare-operator/releases/latest/download/cloudflare-operator.yaml
   kubectl get pods -n cloudflare-operator-system
   ```

2. **创建凭证 Secret**
   ```yaml
   apiVersion: v1
   kind: Secret
   metadata:
     name: cloudflare-credentials
     namespace: cloudflare-operator-system
   type: Opaque
   stringData:
     CLOUDFLARE_API_TOKEN: "${CLOUDFLARE_API_TOKEN}"
   ```

3. **创建 CloudflareCredentials 资源**
   ```yaml
   apiVersion: networking.cloudflare-operator.io/v1alpha2
   kind: CloudflareCredentials
   metadata:
     name: default-credentials
   spec:
     accountId: "${CLOUDFLARE_ACCOUNT_ID}"
     secretRef:
       name: cloudflare-credentials
       namespace: cloudflare-operator-system
   ```

### 测试顺序

1. **基础设施**
   - CloudflareCredentials
   - ClusterTunnel / Tunnel
   - VirtualNetwork

2. **网络**
   - NetworkRoute
   - TunnelBinding
   - DNSRecord
   - PrivateService

3. **访问控制**
   - AccessGroup
   - AccessIdentityProvider
   - AccessServiceToken
   - AccessApplication

4. **Zero Trust**
   - GatewayConfiguration
   - GatewayList
   - GatewayRule
   - DevicePostureRule
   - DeviceSettingsPolicy

## 验证命令

```bash
kubectl get <资源类型> -o wide
kubectl get <资源类型> -o jsonpath='{.status.conditions}'
kubectl logs -n cloudflare-operator-system deployment/cloudflare-operator-controller-manager -f
kubectl describe <资源类型> <名称>
```

## 清理

按相反顺序删除：

```bash
kubectl delete gatewayrule,gatewaylist,gatewayconfiguration --all
kubectl delete accessapplication,accessservicetoken --all
kubectl delete privateservice,dnsrecord,tunnelbinding --all
kubectl delete virtualnetwork --all
kubectl delete cloudflarecredentials --all
kubectl delete secret cloudflare-credentials -n cloudflare-operator-system
```

## 测试报告模板

```markdown
## E2E 测试报告

**日期：** YYYY-MM-DD
**版本：** v0.17.X
**集群：** cluster-name

### 结果

| CRD | 创建 | 更新 | 删除 | 状态 |
|-----|------|------|------|------|
| CloudflareCredentials | ✅ | ✅ | ✅ | 通过 |
| ClusterTunnel | ✅ | ✅ | ✅ | 通过 |
| VirtualNetwork | ✅ | ✅ | ✅ | 通过 |
| NetworkRoute | ✅ | ✅ | ✅ | 通过 |
| ... | | | | |

### 发现的问题
- 问题描述

### 备注
- 其他观察结果
```

## 审查清单

- [ ] Finalizer 在任何 Cloudflare 操作之前添加
- [ ] 只有清理成功后才移除 Finalizer
- [ ] 状态更新使用冲突重试
- [ ] 删除检查 NotFound 错误
- [ ] 错误消息已清理敏感信息
- [ ] 正确的 kubebuilder 标记
- [ ] Status 有 ObservedGeneration
- [ ] Status 有 Conditions 切片
- [ ] 作用域正确设置（Cluster 或 Namespaced）
- [ ] 无硬编码凭证
- [ ] Secrets 通过 K8s Secret API 访问
- [ ] RBAC 权限最小化
- [ ] `make test` 通过
- [ ] `make lint` 通过
- [ ] 无新的 lint 警告