---
name: javascript-specific
version: 1.0.0
description: JavaScript语言特有审查规则（ES6+特性、Node.js最佳实践、前端安全）
language: javascript
tags: [javascript, nodejs, react, vue, angular, es6]
frameworks: [react, vue, angular, express, nextjs, nestjs]
---

# JavaScript特有审查规则

## ES6+现代特性
- **箭头函数**: 正确使用this绑定、避免在方法中使用、不适合构造函数
- **解构赋值**: 合理使用对象/数组解构、避免过度嵌套解构
- **模板字符串**: 使用模板字符串替代字符串拼接、避免模板注入
- **模块化**: 正确使用import/export、避免循环依赖、合理使用默认导出

## Node.js最佳实践
- **事件循环**: 避免阻塞事件循环、正确使用setImmediate/process.nextTick
- **流处理**: 大文件处理使用流、避免一次性加载大文件到内存
- **内存管理**: 检查内存泄漏、正确使用闭包、避免全局变量污染
- **错误处理**: 统一错误处理中间件、正确传递错误、避免未捕获异常

## 前端安全检查
- **XSS防护**: 正确转义用户输入、使用安全的innerHTML、Content Security Policy
- **CSRF防护**: 使用CSRF token、检查Referer/Origin、双重提交cookie
- **内容安全策略**: 配置CSP头、限制内联脚本、白名单域名
- **敏感数据**: 避免前端存储敏感信息、API密钥安全存储

## 框架特定规则

### React
- **Hook规则**: 只在顶层调用Hook、只在React函数中调用
- **性能优化**: 使用React.memo、useMemo、useCallback避免重渲染
- **状态管理**: 合理使用useState、useReducer、避免过度使用Context

### Vue
- **响应式**: 正确使用ref、reactive、避免直接修改数组索引
- **计算属性**: 使用computed缓存复杂计算、避免副作用
- **组件通信**: 合理使用props/emits、避免过度使用全局状态

### Angular
- **变更检测**: 使用OnPush策略、合理使用async pipe
- **依赖注入**: 正确使用服务、避免循环依赖
- **RxJS**: 正确处理订阅、避免内存泄漏

## 代码示例

### 正面示例 - 现代JS特性
```javascript
// 推荐：使用解构和默认值
const { name, age = 18, address: { city } = {} } = userData;

// 推荐：使用模板字符串
const message = `Hello, ${name}! You are ${age} years old.`;

// 推荐：使用箭头函数和数组方法
const activeUsers = users
  .filter(user => user.isActive)
  .map(({ id, name }) => ({ id, name }));
```

### 反面示例 - 过时写法
```javascript
// 不推荐：字符串拼接
var message = 'Hello, ' + name + '! You are ' + age + ' years old.';

// 不推荐：for循环处理数组
var activeUsers = [];
for (var i = 0; i < users.length; i++) {
  if (users[i].isActive) {
    activeUsers.push({ id: users[i].id, name: users[i].name });
  }
}
```

### 正面示例 - Node.js流处理
```javascript
// 推荐：使用流处理大文件
const fs = require('fs');
const readline = require('readline');

async function processLargeFile(filename) {
  const fileStream = fs.createReadStream(filename);
  const rl = readline.createInterface({
    input: fileStream,
    crlfDelay: Infinity
  });

  for await (const line of rl) {
    // 逐行处理，内存友好
    processLine(line);
  }
}
```

### 反面示例 - 内存问题
```javascript
// 不推荐：一次性读取大文件
const fs = require('fs');
function badProcessFile(filename) {
  const data = fs.readFileSync(filename, 'utf8'); // 大文件会占用大量内存
  const lines = data.split('\n');
  lines.forEach(processLine);
}
```

### 正面示例 - React Hook
```javascript
// 推荐：正确使用Hook
function UserList({ users }) {
  const [filter, setFilter] = useState('');
  
  const filteredUsers = useMemo(() => 
    users.filter(user => user.name.includes(filter)), 
    [users, filter]
  );

  return (
    <div>
      <input value={filter} onChange={e => setFilter(e.target.value)} />
      {filteredUsers.map(user => <UserCard key={user.id} user={user} />)}
    </div>
  );
}
```

### 反面示例 - Hook滥用
```javascript
// 不推荐：在条件语句中使用Hook
function BadComponent({ shouldFetch, userId }) {
  if (shouldFetch) {
    // 错误：Hook在条件语句中
    const [user, setUser] = useState(null);
  }
}
