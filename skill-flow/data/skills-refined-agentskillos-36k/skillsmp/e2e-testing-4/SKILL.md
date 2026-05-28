---
name: e2e-testing
description: cloudflare-operator 端到端测试。指导针对真实 Cloudflare API 测试 CRD。适用于测试 Operator 功能、验证 CRD 或运行集成测试。
allowed-tools: Read, Write, Bash, Glob, Grep
user-invocable: true
---

# 端到端测试指南

## 概述

此技能指导 cloudflare-operator 针对真实 Cloudflare API 的端到端测试。

## 前置条件

### 必需凭证
- Cloudflare API Token 或 Global API Key
- Cloudflare Account ID
- Cloudflare Domain（用于 DNS 相关测试）

### 必需权限

| 功能 | 权限 | 范围 |
|------|------|------|
| Tunnel | `Account:Cloudflare Tunnel:Edit` | Account |
| DNS | `Zone:DNS:Edit` | Zone |
| Access | `Account:Access: Apps and Policies:Edit` | Account |
| Zero Trust | `Account:Zero Trust:Edit` | Account |

## 设置

### 1. 部署 Operator

```bash
# 安装 CRD
kubectl apply -f https://github.com/StringKe/cloudflare-operator/releases/latest/download/cloudflare-operator.crds.yaml

# 安装 Operator
kubectl apply -f https://github.com/StringKe/cloudflare-operator/releases/latest/download/cloudflare-operator.yaml

# 验证
kubectl get pods -n cloudflare-operator-system
```

### 2. 创建凭证 Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: cloudflare-credentials
  namespace: cloudflare-operator-system
type: Opaque
stringData:
  CLOUDFLARE_API_TOKEN: "${CLOUDFLARE_API_TOKEN}"
  # 或使用 Global API Key：
  # CLOUDFLARE_API_KEY: "${CLOUDFLARE_API_KEY}"
  # CLOUDFLARE_API_EMAIL: "${CLOUDFLARE_EMAIL}"
```

### 3. 创建 CloudflareCredentials 资源

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

## 测试顺序

按依赖顺序测试 CRD：

### 第一阶段：基础设施
1. CloudflareCredentials
2. ClusterTunnel / Tunnel
3. VirtualNetwork

### 第二阶段：网络
4. NetworkRoute（依赖 Tunnel + VirtualNetwork）
5. TunnelBinding（依赖 Tunnel）
6. DNSRecord
7. PrivateService

### 第三阶段：访问控制
8. AccessGroup
9. AccessIdentityProvider
10. AccessServiceToken
11. AccessApplication

### 第四阶段：Zero Trust
12. GatewayConfiguration
13. GatewayList
14. GatewayRule
15. DevicePostureRule
16. DeviceSettingsPolicy

## 测试清单

### ClusterTunnel

```yaml
apiVersion: networking.cloudflare-operator.io/v1alpha2
kind: ClusterTunnel
metadata:
  name: test-tunnel
spec:
  newTunnel:
    name: e2e-test-tunnel
  cloudflare:
    accountId: "${CLOUDFLARE_ACCOUNT_ID}"
    domain: "${CLOUDFLARE_DOMAIN}"
    credentialsRef:
      name: default-credentials
  deployPatch: '{"spec":{"replicas":1}}'
```

### VirtualNetwork

```yaml
apiVersion: networking.cloudflare-operator.io/v1alpha2
kind: VirtualNetwork
metadata:
  name: test-vnet
spec:
  name: e2e-test-vnet
  comment: "E2E 测试虚拟网络"
  cloudflare:
    accountId: "${CLOUDFLARE_ACCOUNT_ID}"
    credentialsRef:
      name: default-credentials
```

### NetworkRoute

```yaml
apiVersion: networking.cloudflare-operator.io/v1alpha2
kind: NetworkRoute
metadata:
  name: test-route
spec:
  network: "10.200.0.0/24"
  comment: "E2E 测试路由"
  tunnelRef:
    kind: ClusterTunnel
    name: test-tunnel
  virtualNetworkRef:
    name: test-vnet
  cloudflare:
    accountId: "${CLOUDFLARE_ACCOUNT_ID}"
    credentialsRef:
      name: default-credentials
```

## 验证命令

```bash
# 检查资源状态
kubectl get <资源类型> -o wide

# 检查条件
kubectl get <资源类型> -o jsonpath='{.status.conditions}'

# 检查 Operator 日志
kubectl logs -n cloudflare-operator-system deployment/cloudflare-operator-controller-manager -f

# 描述资源查看事件
kubectl describe <资源类型> <名称>
```

## 常见问题

### "secret not found"
- 确保 Secret 在正确的命名空间
- 集群作用域资源：`cloudflare-operator-system`
- 命名空间资源：与资源相同的命名空间

### "authentication error"
- 验证 API Token 权限
- 检查 Account ID 是否正确
- 确保 Token 未过期

### "resource already exists"
- 检查资源是否存在于 Cloudflare 控制台
- 使用 `existingTunnel` 而非 `newTunnel` 进行采用

### 卡在 "Terminating"
```bash
# 检查 finalizers
kubectl get <资源类型> <名称> -o jsonpath='{.metadata.finalizers}'

# 强制删除（注意：可能留下孤立资源）
kubectl patch <资源类型> <名称> -p '{"metadata":{"finalizers":null}}' --type=merge
```

## 清理

按相反顺序删除：

```bash
# 第四阶段
kubectl delete gatewayrule,gatewaylist,gatewayconfiguration --all
kubectl delete deviceposturerule,devicesettingspolicy --all

# 第三阶段
kubectl delete accessapplication,accessservicetoken --all
kubectl delete accessidentityprovider,accessgroup --all

# 第二阶段
kubectl delete privateservice,dnsrecord,tunnelbinding --all
kubectl delete networkroute --all

# 第一阶段
kubectl delete virtualnetwork --all
kubectl delete clustertunnel,tunnel --all
kubectl delete cloudflarecredentials --all

# Secrets
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
