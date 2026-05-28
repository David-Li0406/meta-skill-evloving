---
name: performance-optimization
description: 性能优化策略和最佳实践。用于识别性能瓶颈、优化前端和后端性能、数据库查询优化、缓存策略等。
allowed-tools: Read, Grep, Glob, Bash
---

# 性能优化

## 性能指标

### 前端性能指标

#### Core Web Vitals
```
LCP (Largest Contentful Paint)：最大内容绘制
- 目标：< 2.5s
- 衡量：加载性能

FID (First Input Delay)：首次输入延迟
- 目标：< 100ms
- 衡量：交互性

CLS (Cumulative Layout Shift)：累积布局偏移
- 目标：< 0.1
- 衡量：视觉稳定性
```

#### 其他关键指标
```
FCP (First Contentful Paint)：首次内容绘制
TTI (Time to Interactive)：可交互时间
TBT (Total Blocking Time)：总阻塞时间
```

### 后端性能指标
```
响应时间（Response Time）
- P50: 50% 请求的响应时间
- P95: 95% 请求的响应时间
- P99: 99% 请求的响应时间

吞吐量（Throughput）
- QPS: 每秒查询数
- TPS: 每秒事务数

错误率（Error Rate）
- 4xx 错误率
- 5xx 错误率

资源利用率
- CPU 使用率
- 内存使用率
- 磁盘 I/O
- 网络带宽
```

## 前端性能优化

### 资源加载优化

#### 代码分割
```typescript
// React 懒加载
const Dashboard = React.lazy(() => import('./Dashboard'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Dashboard />
    </Suspense>
  );
}

// Webpack 代码分割
import(/* webpackChunkName: "dashboard" */ './Dashboard')
  .then(module => {
    // 使用模块
  });
```

#### 资源压缩
```javascript
// Webpack 配置
module.exports = {
  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          compress: {
            drop_console: true,
          },
        },
      }),
    ],
  },
};

// Gzip 压缩
app.use(compression());
```

#### 图片优化
```html
<!-- 响应式图片 -->
<picture>
  <source srcset="image.webp" type="image/webp">
  <source srcset="image.jpg" type="image/jpeg">
  <img src="image.jpg" alt="Description">
</picture>

<!-- 懒加载 -->
<img src="image.jpg" loading="lazy" alt="Description">

<!-- 现代格式 -->
WebP, AVIF (更小的文件大小)
```

#### 字体优化
```css
/* 字体显示策略 */
@font-face {
  font-family: 'MyFont';
  src: url('font.woff2') format('woff2');
  font-display: swap; /* 立即显示备用字体 */
}

/* 预加载关键字体 */
<link rel="preload" href="font.woff2" as="font" type="font/woff2" crossorigin>
```

### 渲染优化

#### 虚拟滚动
```typescript
import { FixedSizeList } from 'react-window';

function VirtualList({ items }) {
  return (
    <FixedSizeList
      height={600}
      itemCount={items.length}
      itemSize={50}
      width="100%"
    >
      {({ index, style }) => (
        <div style={style}>{items[index]}</div>
      )}
    </FixedSizeList>
  );
}
```

#### 防抖和节流
```typescript
// 防抖：延迟执行
function debounce(fn: Function, delay: number) {
  let timer: NodeJS.Timeout;
  return function(...args: any[]) {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}

// 节流：限制频率
function throttle(fn: Function, delay: number) {
  let last = 0;
  return function(...args: any[]) {
    const now = Date.now();
    if (now - last >= delay) {
      fn(...args);
      last = now;
    }
  };
}

// 使用
const handleSearch = debounce((query) => {
  // 搜索逻辑
}, 300);

const handleScroll = throttle(() => {
  // 滚动逻辑
}, 100);
```

#### React 性能优化
```typescript
// React.memo
const MemoizedComponent = React.memo(Component);

// useMemo
const expensiveValue = useMemo(() => {
  return computeExpensiveValue(a, b);
}, [a, b]);

// useCallback
const memoizedCallback = useCallback(() => {
  doSomething(a, b);
}, [a, b]);

// 避免内联对象
// ❌ 不好
<Component style={{ margin: 10 }} />

// ✅ 好
const style = { margin: 10 };
<Component style={style} />
```

### 网络优化

#### HTTP/2 和 HTTP/3
```
HTTP/2 特性：
- 多路复用
- 服务器推送
- 头部压缩

HTTP/3 特性：
- 基于 QUIC
- 更快的连接建立
- 更好的丢包恢复
```

#### 资源预加载
```html
<!-- DNS 预解析 -->
<link rel="dns-prefetch" href="https://api.example.com">

<!-- 预连接 -->
<link rel="preconnect" href="https://api.example.com">

<!-- 预加载 -->
<link rel="preload" href="critical.css" as="style">

<!-- 预获取 -->
<link rel="prefetch" href="next-page.js">
```

#### CDN 加速
```javascript
// 静态资源使用 CDN
const CDN_URL = 'https://cdn.example.com';

<img src={`${CDN_URL}/images/logo.png`} />
<script src={`${CDN_URL}/js/app.js`}></script>
```

## 后端性能优化

### 数据库优化

#### 查询优化
```sql
-- 使用索引
CREATE INDEX idx_user_email ON users(email);

-- 避免 SELECT *
SELECT id, name, email FROM users WHERE id = 1;

-- 使用 EXPLAIN 分析
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- 批量操作
INSERT INTO users (name) VALUES ('User1'), ('User2'), ('User3');
```

#### 连接池
```typescript
const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'password',
  database: 'mydb',
  connectionLimit: 10,
  queueLimit: 0
});
```

#### 读写分离
```typescript
// 主库写
await masterDB.query('INSERT INTO users ...');

// 从库读
await slaveDB.query('SELECT * FROM users ...');
```

### 缓存策略

#### 多级缓存
```
浏览器缓存 → CDN 缓存 → 应用缓存 → 数据库缓存
```

#### Redis 缓存
```typescript
// 缓存穿透：缓存空值
async function getUser(id: string) {
  let user = await redis.get(`user:${id}`);

  if (user === null) {
    user = await db.findUser(id);
    if (user) {
      await redis.setex(`user:${id}`, 3600, JSON.stringify(user));
    } else {
      await redis.setex(`user:${id}`, 60, 'null'); // 缓存空值
    }
  }

  return user === 'null' ? null : JSON.parse(user);
}

// 缓存雪崩：随机过期时间
const ttl = 3600 + Math.floor(Math.random() * 600);
await redis.setex(key, ttl, value);

// 缓存击穿：互斥锁
async function getUser(id: string) {
  let user = await redis.get(`user:${id}`);

  if (!user) {
    const lock = await redis.set(`lock:user:${id}`, '1', 'NX', 'EX', 10);
    if (lock) {
      try {
        user = await db.findUser(id);
        await redis.setex(`user:${id}`, 3600, JSON.stringify(user));
      } finally {
        await redis.del(`lock:user:${id}`);
      }
    } else {
      await sleep(50);
      return getUser(id); // 重试
    }
  }

  return JSON.parse(user);
}
```

#### HTTP 缓存
```typescript
// 强缓存
res.setHeader('Cache-Control', 'public, max-age=3600');

// 协商缓存
res.setHeader('ETag', etag);
res.setHeader('Last-Modified', lastModified);

if (req.headers['if-none-match'] === etag) {
  res.status(304).end();
}
```

### 异步处理

#### 消息队列
```typescript
// 生产者
await queue.publish('email.send', {
  to: 'user@example.com',
  subject: 'Welcome',
  body: 'Hello!'
});

// 消费者
queue.subscribe('email.send', async (message) => {
  await sendEmail(message);
});
```

#### 后台任务
```typescript
// Bull 队列
const emailQueue = new Bull('email');

// 添加任务
await emailQueue.add({
  to: 'user@example.com',
  subject: 'Welcome'
});

// 处理任务
emailQueue.process(async (job) => {
  await sendEmail(job.data);
});
```

### 并发优化

#### 并行处理
```typescript
// ❌ 串行
const user = await getUser(id);
const orders = await getOrders(id);
const profile = await getProfile(id);

// ✅ 并行
const [user, orders, profile] = await Promise.all([
  getUser(id),
  getOrders(id),
  getProfile(id)
]);
```

#### 限流
```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  message: 'Too many requests'
});

app.use('/api/', limiter);
```

#### 负载均衡
```nginx
upstream backend {
  server backend1.example.com;
  server backend2.example.com;
  server backend3.example.com;
}

server {
  location / {
    proxy_pass http://backend;
  }
}
```

## 性能监控

### 前端监控
```typescript
// Performance API
const perfData = performance.getEntriesByType('navigation')[0];
console.log('DNS:', perfData.domainLookupEnd - perfData.domainLookupStart);
console.log('TCP:', perfData.connectEnd - perfData.connectStart);
console.log('TTFB:', perfData.responseStart - perfData.requestStart);

// Web Vitals
import { getCLS, getFID, getLCP } from 'web-vitals';

getCLS(console.log);
getFID(console.log);
getLCP(console.log);
```

### 后端监控
```typescript
// 响应时间中间件
app.use((req, res, next) => {
  const start = Date.now();

  res.on('finish', () => {
    const duration = Date.now() - start;
    logger.info({
      method: req.method,
      path: req.path,
      statusCode: res.statusCode,
      duration
    });
  });

  next();
});
```

### APM 工具
```
New Relic
Datadog
Sentry
Prometheus + Grafana
```

## 性能测试

### 负载测试
```bash
# Apache Bench
ab -n 1000 -c 10 http://example.com/

# wrk
wrk -t12 -c400 -d30s http://example.com/

# k6
k6 run script.js
```

### 压力测试
```javascript
// k6 脚本
import http from 'k6/http';
import { check } from 'k6';

export let options = {
  stages: [
    { duration: '2m', target: 100 },
    { duration: '5m', target: 100 },
    { duration: '2m', target: 200 },
    { duration: '5m', target: 200 },
    { duration: '2m', target: 0 },
  ],
};

export default function () {
  let response = http.get('http://example.com/');
  check(response, {
    'status is 200': (r) => r.status === 200,
  });
}
```

## 优化检查清单

### 前端
- [ ] 代码分割和懒加载
- [ ] 资源压缩和优化
- [ ] 图片优化（格式、大小、懒加载）
- [ ] 字体优化
- [ ] 虚拟滚动（长列表）
- [ ] 防抖节流
- [ ] React 性能优化
- [ ] HTTP/2 或 HTTP/3
- [ ] CDN 加速
- [ ] 资源预加载

### 后端
- [ ] 数据库查询优化
- [ ] 索引优化
- [ ] 连接池配置
- [ ] 缓存策略
- [ ] 异步处理
- [ ] 并发优化
- [ ] 限流保护
- [ ] 负载均衡
- [ ] 性能监控
- [ ] 定期性能测试
