---
name: python-specific
version: 1.0.0
description: Python语言特有审查规则（Pythonic代码、Django/Flask最佳实践、性能优化）
language: python
tags: [python, django, flask, asyncio, pep8]
frameworks: [django, flask, fastapi, celery]
---

# Python特有审查规则

## Pythonic代码规范
- **列表推导**: 使用列表推导替代map/filter，避免过度复杂的推导式
- **生成器**: 大数据集使用生成器表达式，避免一次性加载到内存
- **上下文管理器**: 正确使用with语句管理资源，自定义__enter__/__exit__
- **解包赋值**: 合理使用元组解包、星号表达式，避免魔法数字

## Django/Flask最佳实践
- **ORM使用**: 避免N+1查询、使用select_related/prefetch_related、合理索引
- **中间件**: 中间件顺序正确、避免阻塞请求处理、正确异常处理
- **模板安全**: 自动转义开启、避免模板中复杂逻辑、CSRF保护启用
- **异步视图**: Django async views正确使用、避免阻塞操作

## 性能优化
- **GIL影响**: CPU密集型任务使用多进程、IO密集型使用异步
- **异步IO**: async/await正确使用、避免阻塞事件循环、使用aiohttp等异步库
- **内存分析**: 检查内存泄漏、使用tracemalloc、避免循环引用
- **C扩展**: 性能关键部分考虑Cython、Numba等加速方案

## 包管理
- **虚拟环境**: 使用venv/virtualenv、requirements.txt版本锁定
- **依赖管理**: 检查循环依赖、避免过度依赖、使用poetry/pipenv
- **版本冲突**: 检查依赖版本兼容性、使用语义化版本

## 代码示例

### 正面示例 - 列表推导
```python
# 推荐：简洁的列表推导
squares = [x**2 for x in range(10) if x % 2 == 0]

# 推荐：生成器表达式节省内存
sum(x**2 for x in range(1000000))
```

### 反面示例 - 过度复杂推导式
```python
# 不推荐：过于复杂的列表推导
matrix = [[(i*j)**2 + (i+j) for j in range(5) if j % 2 == 0] 
          for i in range(10) if i > 5 and i % 3 == 0]
```

### 正面示例 - Django ORM优化
```python
# 推荐：避免N+1查询
users = User.objects.select_related('profile').prefetch_related('posts')

# 推荐：使用values()减少数据传输
active_users = User.objects.filter(is_active=True).values('id', 'username')
```

### 反面示例 - N+1查询
```python
# 不推荐：循环中查询
for user in User.objects.all():
    print(user.profile.bio)  # 每次循环都会查询profile
```

### 正面示例 - 异步处理
```python
# 推荐：使用async/await
async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.example.com') as response:
            return await response.json()
```

### 反面示例 - 阻塞异步循环
```python
# 不推荐：在异步函数中使用阻塞IO
async def bad_example():
    data = requests.get('https://api.example.com').json()  # 阻塞事件循环
    return data
