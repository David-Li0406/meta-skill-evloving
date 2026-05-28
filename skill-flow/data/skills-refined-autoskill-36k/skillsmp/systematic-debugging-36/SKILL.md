---
name: systematic-debugging
description: 系统化调试方法，使用四阶段调试流程解决前端和后端问题。遇到 bug、错误或异常行为时使用。
---

# 系统化调试方法

## When to Use

- 遇到 bug 或错误
- 功能不按预期工作
- 性能问题
- 前端显示异常
- API 调用失败
- 数据不一致

## 四阶段调试流程

### 阶段 1: 观察问题 (Observe)

#### 收集信息
1. **复现问题**
   - 记录重现步骤
   - 确认问题频率（每次 vs 偶发）
   - 识别触发条件

2. **检查错误信息**
   ```javascript
   // 前端：浏览器控制台
   console.error(error)
   // 网络标签检查 API 响应
   ```

   ```python
   # 后端：Django 日志
   import logging
   logger = logging.getLogger(__name__)
   logger.error(f"Error: {str(e)}")
   ```

3. **查看相关文件**
   - 刚修改的文件
   - 调用栈中的文件
   - 相关配置文件

#### 前端调试检查清单
- [ ] 浏览器控制台错误
- [ ] 网络请求状态码
- [ ] API 响应数据格式
- [ ] 组件状态（Vue DevTools）
- [ ] 路由参数
- [ ] 本地存储数据

#### 后端调试检查清单
- [ ] Django 日志文件
- [ ] 数据库查询结果
- [ ] API 响应内容
- [ ] 模型实例数据
- [ ] 权限和认证状态

### 阶段 2: 分析原因 (Analyze)

#### 前端常见原因

**状态问题**
```javascript
// 检查：状态是否正确更新
console.log('State:', this.$data)

// 检查：计算属性
console.log('Computed:', this.filteredList)
```

**异步问题**
```javascript
// 检查：Promise 是否正确处理
async fetchData() {
  try {
    const res = await getWorkorders()
    console.log('Response:', res.data)
  } catch (error) {
    console.error('Error:', error)
  }
}
```

**生命周期问题**
```javascript
// 检查：数据加载时机
mounted() {
  console.log('Mounted, fetching data...')
  this.fetchData()
}
```

#### 后端常见原因

**查询问题**
```python
# 检查：查询结果
workorders = WorkOrder.objects.filter(status='pending')
print(f"Found {workorders.count()} workorders")

# 检查：SQL 查询
from django.db import connection
print(connection.queries)
```

**序列化问题**
```python
# 检查：序列化数据
serializer = WorkOrderSerializer(workorder)
print(serializer.data)

# 检查：验证错误
if not serializer.is_valid():
    print(serializer.errors)
```

**权限问题**
```python
# 检查：用户权限
print(f"User: {request.user}")
print(f"Authenticated: {request.user.is_authenticated}")
print(f"Permissions: {request.user.get_all_permissions()}")
```

### 阶段 3: 提出假设 (Hypothesize)

#### 假设模板

**格式：** "我认为问题是由 [原因] 导致的，因为 [证据]"

**示例：**
- "我认为 API 返回 404 是因为 URL 路径配置错误"
- "我认为组件不更新是因为状态未正确触发重新渲染"
- "我认为查询结果为空是因为数据库中的过滤条件过于严格"

#### 验证假设

```javascript
// 添加调试日志验证假设
console.log('假设验证:', value)
console.trace('调用栈')
```

```python
# 添加断点验证假设
import pdb; pdb.set_trace()
# 或使用 ipdb
import ipdb; ipdb.set_trace()
```

### 阶段 4: 验证修复 (Verify)

#### 前端验证

1. **功能测试**
   ```javascript
   // 添加测试用例
   it('should display workorder list', async () => {
     await wrapper.vm.fetchWorkorders()
     expect(wrapper.findAll('.workorder-item').length).toBeGreaterThan(0)
   })
   ```

2. **边界测试**
   - 空数据
   - 错误响应
   - 大数据量

3. **用户体验测试**
   - 加载状态
   - 错误提示
   - 成功反馈

#### 后端验证

1. **API 测试**
   ```python
   def test_create_workorder(self):
       url = reverse('workorder-list')
       data = {'order_number': 'WO001'}
       response = self.client.post(url, data)
       self.assertEqual(response.status_code, 201)
   ```

2. **数据验证**
   - 数据库记录
   - 关联关系
   - 业务逻辑

3. **日志确认**
   - 无错误日志
   - 预期日志输出

## 常见问题诊断

### 前端常见问题

#### 组件不更新
```javascript
// 检查：是否使用了 this.$set
this.$set(this.object, 'key', value)

// 或使用 Vue.set
Vue.set(this.array, index, newValue)
```

#### 路由参数丢失
```javascript
// 检查：是否使用了正确的路由参数获取方式
const id = this.$route.params.id

// 检查：是否需要监听路由变化
watch: {
  '$route'(to, from) {
    this.fetchData()
  }
}
```

#### API 调用失败
```javascript
// 检查：完整的错误信息
axios.get('/api/workorders/')
  .catch(error => {
    console.log('Error config:', error.config)
    console.log('Error response:', error.response)
    console.log('Error request:', error.request)
  })
```

### 后端常见问题

#### 404 错误
```python
# 检查：URL 配置
# 在 urls.py 中打印 urlpatterns
print(urlpatterns)

# 检查：视图是否注册
from django.urls import get_resolver
print(get_resolver().url_patterns)
```

#### CSRF 错误
```python
# 检查：CSRF 配置
# settings.py
CSRF_TRUSTED_ORIGINS = ['http://localhost:8080']

# 检查：前端是否发送 CSRF token
```

#### 数据库连接错误
```python
# 检查：数据库配置
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 测试：连接数据库
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("SELECT 1")
    print(cursor.fetchone())
```

## 调试工具

### 前端工具

1. **Vue DevTools**
   - 组件树
   - Vuex 状态
   - 事件监听
   - 性能分析

2. **浏览器开发者工具**
   - Elements: DOM 和样式
   - Console: 日志和错误
   - Network: 网络请求
   - Sources: 断点调试

3. **ESLint**
   ```bash
   npm run lint
   ```

### 后端工具

1. **Django Debug Toolbar**
   ```python
   # settings.py
   INSTALLED_APPS = ['debug_toolbar']
   ```

2. **Django Shell**
   ```bash
   python manage.py shell
   ```

3. **日志查看**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

## 最佳实践

### 1. 添加有意义的日志
```javascript
console.log('[WorkOrderList] Fetching workorders...')
```

```python
logger.info(f"[WorkOrderViewSet] Creating workorder: {data}")
```

### 2. 使用断点调试
```javascript
debugger  // 在浏览器中暂停
```

```python
import pdb; pdb.set_trace()  # 在 Python 中暂停
```

### 3. 分而治之
- 将大问题分解为小问题
- 逐个测试每个组件
- 隔离问题范围

### 4. 记录解决方案
```javascript
// TODO: 记录问题和解决方案
// 问题: XXX
// 原因: YYY
// 解决: ZZZ
```

## 预防性调试

### 代码审查检查清单
- [ ] 错误处理完善
- [ ] 边界条件处理
- [ ] 日志记录充分
- [ ] 单元测试覆盖
- [ ] 代码注释清晰

### 性能监控
```javascript
// 监控 API 响应时间
console.time('fetchWorkorders')
await fetchWorkorders()
console.timeEnd('fetchWorkorders')
```

```python
# 监控查询时间
import time
start = time.time()
# 查询操作
print(f"Query took {time.time() - start:.2f}s")
```

## 相关技能

- `vue-component-patterns` - Vue 组件开发
- `django-api-patterns` - Django API 开发
- `testing-patterns` - 编写测试
