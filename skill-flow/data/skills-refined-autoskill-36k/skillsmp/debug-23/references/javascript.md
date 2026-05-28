# JavaScript 调试规范

使用系统化的调试方式，而不是简单的 `console.log`。所有调试输出必须结构化、易读、可折叠、可计数、可测量。

## 规则

### 1. 使用 console.assert

代替手动条件检查，条件不满足时输出错误信息。

```javascript
console.assert(user.age >= 18, "User must be adult");
```

### 2. 使用 console.table

对数组、对象数组、API 返回值展示结构化数据。

```javascript
console.table(users);
```

### 3. 使用 console.group / console.groupCollapsed

将调试信息分组，以模块名或流程名作为标签。

```javascript
console.group("Auth Flow");
console.log("Step 1...");
console.groupEnd();
```

### 4. 使用 console.count

追踪函数调用次数，识别意外的重复调用。

```javascript
console.count("fetchData called");
```

### 5. 使用 console.time / console.timeLog / console.timeEnd

测量代码执行耗时，定位性能瓶颈或异步延迟。

```javascript
console.time("process");
doSomething();
console.timeLog("process");
console.timeEnd("process");
```

### 6. 使用 console.trace

在递归、意外调用、状态异常时打印调用堆栈。

```javascript
console.trace("Unexpected call");
```

### 7. 使用彩色输出

用 `%c` 输出带 CSS 样式的日志，让重要信息更醒目。

```javascript
console.log("%c API ERROR", "color: red; font-weight: bold;");
console.log("%c WARNING", "color: orange;");
console.log("%c Step 1", "color: blue;");
```

## AI 输出要求

生成调试代码时自动加入：
- 结构化输出
- 分组与折叠
- 函数调用计数
- 性能与耗时信息
- 调用堆栈信息
- 重要信息视觉突出

解释调试结果时，基于输出分析：错误原因、性能瓶颈、调用链、状态异常。
