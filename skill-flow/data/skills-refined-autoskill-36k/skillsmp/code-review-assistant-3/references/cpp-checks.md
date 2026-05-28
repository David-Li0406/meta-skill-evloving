# Qt/C++ 代码审核检查规则

## 审核排除规则

### [CPP-EX001] vendor / third_party 目录

- **描述**: `vendor/`、`third_party/`、`3rdparty/` 目录及其子目录不进行代码审核
- **处理方式**:
  - 不审核第三方依赖目录下的任何文件内容
  - 不提示关于第三方库的改进建议
  - 不对依赖目录的变更生成任何审核意见
- **示例**:

```
以下文件路径应被跳过审核:
- vendor/qt/...
- third_party/boost/...
- 3rdparty/openssl/...
```

### [CPP-EX002] Generated 目录

- **描述**: 自动生成的代码文件（如 `moc_*.cpp`, `ui_*.h`, `qrc_*.cpp`）不进行审核
- **处理方式**:
  - 跳过 Qt Meta-Object Compiler 生成的文件
  - 跳过 UI Designer 生成的文件
  - 跳过 Resource Compiler 生成的文件
- **示例**:

```
以下文件路径应被跳过审核:
- build/moc_*.cpp
- build/ui_*.h
- build/qrc_*.cpp
- Generated/*.cpp
```

---

## 检查规则按严重程度分类

---

## 🔴 Must Fix (-2)

### [CPP-MF001] 内存泄漏

- **描述**: 使用 `new` 分配的内存未配对使用 `delete` 释放
- **影响**: 导致内存泄漏，长时间运行可能耗尽系统内存
- **检测方式**:
  - 检测 `new` / `new[]` 调用，确认是否释放
  - 检测所有权转移是否完整
  - 提示使用智能指针
- **示例**:

```cpp
// Bad - 内存泄漏
void process() {
    auto* data = new Data();
    data->doSomething();
    // 忘记 delete data
}

// Good - 使用智能指针
void process() {
    auto data = std::make_unique<Data>();
    data->doSomething();
}

// Good - 手动管理
void process() {
    auto* data = new Data();
    data->doSomething();
    delete data;
}
```

- **建议修改**: 优先使用 `std::unique_ptr` 或 `std::shared_ptr` 智能指针；使用 Qt 对象树（QObject 父子关系）或 RAII 模式

---

### [CPP-MF002] 使用未初始化的变量

- **描述**: 使用未初始化的变量或指针
- **影响**: 导致未定义行为、随机崩溃或数据错误
- **检测方式**:
  - 检测变量声明后直接使用
  - 检测未检查的指针解引用
- **示例**:

```cpp
// Bad - 未初始化
int value;
if (someCondition) {
    value = 10;
}
std::cout << value;  // 未初始化

// Bad - 指针未检查
Data* data = getData();
data->process();  // 可能为 nullptr

// Good
int value = 0;  // 默认值
if (someCondition) {
    value = 10;
}

// Good
Data* data = getData();
if (!data) {
    return;
}
data->process();
```

- **建议修改**: 变量声明时初始化，使用前检查指针有效性

---

### [CPP-MF003] 数组越界访问

- **描述**: 访问数组或容器越界的索引
- **影响**: 导致崩溃或内存损坏
- **检测方式**:
  - 检测数组/容器访问前是否检查边界
  - 检测循环索引与容器大小的关系
- **示例**:

```cpp
// Bad - 未检查边界
void process(const QList<int>& list) {
    for (int i = 0; i <= list.size(); ++i) {
        std::cout << list[i];  // 越界
    }
}

// Good
void process(const QList<int>& list) {
    for (int i = 0; i < list.size(); ++i) {
        std::cout << list[i];
    }
}

// Better - 使用范围 for
void process(const QList<int>& list) {
    for (int value : list) {
        std::cout << value;
    }
}
```

- **建议修改**: 使用范围 for 循环或确保索引有效

---

### [CPP-MF004] 空指针解引用

- **描述**: 解引用未检查的空指针
- **影响**: 导致段错误 (SIGSEGV)
- **检测方式**:
  - 检测 `->` 操作符前是否有 nullptr 检查
  - 检测动态转换后的指针使用
- **示例**:

```cpp
// Bad - 未检查
QObject* obj = findObject();
obj->setProperty("value", data);

// Bad - dynamic_cast 未检查
Derived* derived = dynamic_cast<Derived*>(base);
derived->doSomething();

// Good
QObject* obj = findObject();
if (!obj) {
    return;
}
obj->setProperty("value", data);

// Good
auto derived = dynamic_cast<Derived*>(base);
if (!derived) {
    return;
}
derived->doSomething();
```

- **建议修改**: 解引用前检查指针有效性，使用 `qobject_cast` 代替 `dynamic_cast` 处理 QObject

---

### [CPP-MF005] 竞态条件 - 线程安全问题

- **描述**: 多线程环境下未使用同步机制访问共享资源
- **影响**: 数据竞争导致不可预期的行为、数据损坏或崩溃
- **检测方式**:
  - 检测共享变量的并发读写
  - 检测 Qt 对象在不同线程之间的信号槽连接
- **示例**:

```cpp
// Bad - 无保护的共享访问
int counter = 0;

void threadFunc() {
    counter++;  // 竞态条件
}

// Good - 使用 QMutex
QMutex mutex;
int counter = 0;

void threadFunc() {
    QMutexLocker locker(&mutex);
    counter++;
}

// Good - 使用 Qt::DirectConnection 时的线程注意事项
auto* worker = new Worker();
worker->moveToThread(workerThread);
// 谨慎使用 Qt::DirectConnection 跨线程发送信号
```

- **建议修改**: 使用 `QMutex`、`QReadWriteLock`、`QAtomicInt` 等同步机制；注意跨线程信号槽连接类型

---

### [CPP-MF006] SQL 注入风险

- **描述**: 使用字符串拼接构建 SQL 查询，存在注入风险
- **影响**: 恶意输入可能导致数据库被攻击
- **检测方式**:
  - 检测 QSqlQuery 字符串拼接
  - 检测 SQL 字符串中直接插入变量
- **示例**:

```cpp
// Bad - 字符串拼接
QString query = "SELECT * FROM users WHERE id = " + userID;
QSqlQuery sql;
sql.exec(query);

// Bad - arg 拼接
QString query = QString("SELECT * FROM users WHERE name = '%1'").arg(name);

// Good - 参数化查询
QSqlQuery query;
query.prepare("SELECT * FROM users WHERE id = ?");
query.addBindValue(userID);
query.exec();

// Good - 命名占位符
QSqlQuery query;
query.prepare("SELECT * FROM users WHERE name = :name");
query.bindValue(":name", name);
query.exec();
```

- **建议修改**: 使用 `prepare()` + `bindValue()` 进行参数化查询

---

### [CPP-MF007] 信号槽参数不匹配

- **描述**: 信号与槽的参数类型或数量不匹配
- **影响**: 编译失败或运行时连接失败
- **检测方式**:
  - 检查信号的参数与槽的参数兼容性
  - 槽函数参数不能多于信号参数
- **示例**:

```cpp
// Bad - 槽参数多于信号
class Sender : public QObject {
    Q_OBJECT
signals:
    void dataChanged(int id);
};

class Receiver : public QObject {
    Q_OBJECT
public slots:
    void onDataChanged(int id, const QString& name);  // 多于信号参数
};

// Good - 参数匹配或槽参数少于信号
class Receiver : public QObject {
    Q_OBJECT
public slots:
    void onDataChanged(int id);  // 匹配
    void onDataChanged();        // 可以更少
};
```

- **建议修改**: 确保信号槽参数类型兼容，槽函数参数数 ≤ 信号参数数

---

### [CPP-MF008] QObject 对象销毁后使用

- **描述**: 在对象被销毁后继续使用该对象
- **影响**: 导致崩溃或未定义行为
- **检测方式**:
  - 检测在析构函数后访问对象
  - 检测信号槽连接后的对象生命周期
- **示例**:

```cpp
// Bad - 可能的悬空引用
QObject* obj = new QObject();
connect(obj, &QObject::destroyed, this, [this, obj]() {
    // obj 此时已销毁，访问是未定义行为
    obj->setProperty(...);  // 危险
});

// Good
QObject* obj = new QObject();
connect(obj, &QObject::destroyed, this, [this]() {
    // 不访问 obj
    cleanup();
});

// Good - 使用 QPointer
QPointer<QObject> obj = new QObject();
connect(obj, &QObject::destroyed, this, [obj]() {
    if (!obj.isNull()) {
        obj->setProperty(...);
    }
});
```

- **建议修改**: 使用 `QPointer` 或确保对象生命周期正确管理

---

## 🟡 Should Fix (-2)

### [CPP-SF001] 命名不符合规范

- **描述**: 变量、函数、类名称不符合 Qt/C++ 命名约定
- **影响**: 降低代码可读性，与项目规范不一致
- **检测方式**:
  - 类名使用大驼峰 (PascalCase)
  - 函数和变量名使用小驼峰 (camelCase)
  - 成员变量使用 `m_` 前缀或下划线后缀
  - 常量使用全大写下划线分隔
- **示例**:

```cpp
// Bad - 命名不规范
class user_data {
    QString User_Name;
    void Get_Data() {}
    int counter_value;
};

// Good - Qt 风格命名
class UserData : public QObject {
    Q_OBJECT
public:
    void getData();
private:
    QString m_userName;
    int m_counterValue;
    static const int MAX_RETRY_COUNT = 3;
};
```

- **建议修改**: 遵循 Qt Coding Conventions 和项目代码风格

---

### [CPP-SF002] 函数过长

- **描述**: 单个函数代码行数过多（建议超过 100 行）
- **影响**: 降低可读性和可维护性，难以测试
- **检测方式**: 统计函数体有效行数
- **示例**:

```cpp
// Bad - 超过100行的函数
void processLargeData() {
    // ... 100+ 行代码 ...
}

// Good - 拆分成多个小函数
void processLargeData() {
    auto data = loadData();
    auto validated = validateData(data);
    auto transformed = transformData(validated);
    saveResult(transformed);
}
```

- **建议修改**: 将长函数拆分成多个职责单一的小函数

---

### [CPP-SF003] 魔法数字

- **描述**: 代码中出现未命名的数字字面量（0、1 除外）
- **影响**: 降低代码可读性，修改时容易遗漏
- **检测方式**: 检测非 0/1 的数字字面量
- **示例**:

```cpp
// Bad - 魔法数字
if (size > 1024) {
    // ...
}
thread->sleep(5000);

// Good
constexpr int MAX_SIZE = 1024;
constexpr int RETRY_DELAY_MS = 5000;

if (size > MAX_SIZE) {
    // ...
}
thread->sleep(RETRY_DELAY_MS);
```

- **建议修改**: 定义常量或枚举替代魔法数字

---

### [CPP-SF004] 缺少注释的复杂逻辑

- **描述**: 复杂的条件判断、循环或算法缺少解释性注释
- **影响**: 降低代码可读性，增加维护难度
- **检测方式**:
  - 多层嵌套条件
  - 复杂的正则表达式
  - 算法核心逻辑
- **示例**:

```cpp
// Bad - 复杂逻辑无注释
if ((a > 10 && b < 20) || (c != "" && d == 0)) {
    // ...
}

// Good
// Check if user is eligible for discount:
// - Level > 10 and balance < 20, OR
// - Has special promo code and new customer
if ((level > 10 && balance < 20) || (promoCode != "" && isNewCustomer)) {
    // ...
}
```

- **建议修改**: 为复杂逻辑添加解释性注释

---

### [CPP-SF005] 过度嵌套

- **描述**: 代码嵌套层级过深（建议超过 3 层）
- **影响**: 降低可读性，增加圈复杂度
- **检测方式**: 统计代码块嵌套层级
- **示例**:

```cpp
// Bad - 深层嵌套
if (condition1) {
    if (condition2) {
        if (condition3) {
            if (condition4) {
                // ...
            }
        }
    }
}

// Good - 提前返回
if (!condition1) {
    return;
}
if (!condition2) {
    return;
}
if (!condition3) {
    return;
}
if (condition4) {
    // ...
}
```

- **建议修改**: 使用卫宁语句（guard clauses）或提取函数减少嵌套

---

### [CPP-SF006] 不必要的父类成员函数遮蔽

- **描述**: 派生类重新声明与父类相同的成员函数但不使用 `override` 关键字
- **影响**: 可能导致误写函数签名而无法正确覆盖
- **检测方式**: 检测虚函数重写缺少 `override` 关键字
- **示例**:

```cpp
// Bad - 缺少 override
class Base {
public:
    virtual void process();
};

class Derived : public Base {
public:
    void process();  // 无 override，错误匹配时编译器不会报警
};

// Good
class Base {
public:
    virtual void process();
};

class Derived : public Base {
public:
    void process() override;  // 安全
};
```

- **建议修改**: 所有虚函数重写都使用 `override` 关键字

---

### [CPP-SF007] QString::number 不必要转换

- **描述**: 在可以使用 `QString::asprintf` 或 `QString::arg` 的地方使用字符串拼接
- **影响**: 降低代码可读性和可维护性
- **检测方式**: 检测过多的 `+` 操作符拼接
- **示例**:

```cpp
// Bad - 拼接方式
QString msg = "Error: " + QString::number(errorCode) + " - " + errorMessage;

// Good - 使用 arg
QString msg = QString("Error: %1 - %2").arg(errorCode).arg(errorMessage);

// Good - 使用 asprintf (C++20)
QString msg = QString::asprintf("Error: %d - %s", errorCode, errorMessage.toUtf8().constData());
```

- **建议修改**: 使用 `QString::arg()` 或格式化函数进行字符串构建

---

### [CPP-SF008] 硬编码的文件路径

- **描述**: 代码中硬编码文件或目录路径
- **影响**: 降低可移植性，跨平台可能出问题
- **检测方式**: 检测字符串字面量中的路径
- **示例**:

```cpp
// Bad - 硬编码路径
QFile file("/home/user/data/config.txt");

// Good - 使用 QStandardPaths
QString configPath = QStandardPaths::writableLocation(QStandardPaths::AppDataLocation) + "/config.txt";
QFile file(configPath);

// Good - 使用相对路径
QFile file(":/resources/config.txt");
```

- **建议修改**: 使用 `QStandardPaths`、资源路径或配置文件

---

### [CPP-SF009] 未检查操作结果

- **描述**: 调用可能失败的操作但未检查返回值
- **影响**: 忽略错误，后续逻辑可能基于失败的状态继续执行
- **检测方式**: 检测 `exec()`、`open()`、`write()` 等操作未检查返回值
- **示例**:

```cpp
// Bad - 未检查
QFile file("data.txt");
file.open(QIODevice::WriteOnly);
file.write("hello");

// Good - 检查结果
QFile file("data.txt");
if (!file.open(QIODevice::WriteOnly)) {
    qWarning() << "Failed to open file:" << file.errorString();
    return;
}
if (file.write("hello") == -1) {
    qWarning() << "Failed to write:" << file.errorString();
    return;
}
```

- **建议修改**: 检查并处理可能失败的操作结果

---

## 🔵 Nice to Have (-1)

### [CPP-NH001] 可使用现有 Qt 工具类

- **描述**: 重复实现了 Qt 已有的功能
- **影响**: 增加维护负担，Qt 类是经过充分测试的
- **检测方式**: 检测自实现函数与 Qt 标准类功能重复
- **示例**:

```cpp
// Bad - 自实现
QString capitalize(const QString& s) {
    if (s.isEmpty()) return s;
    return s[0].toUpper() + s.mid(1).toLower();
}

// Good - 使用 Qt (需要手动处理，但提示简化思路)

// Bad - 自实现字符串分割
QStringList splitString(const QString& s, QChar delimiter) {
    QStringList result;
    QString current;
    for (auto c : s) {
        if (c == delimiter) {
            result.append(current);
            current.clear();
        } else {
            current += c;
        }
    }
    result.append(current);
    return result;
}

// Good - 使用 split()
QStringList result = s.split(delimiter);
```

- **建议修改**: 优先使用 Qt 标准类和工具函数

---

### [CPP-NH002] 未使用的变量或函数

- **描述**: 声明了变量或函数但未使用
- **影响**: 可能是代码冗余或逻辑错误
- **检测方式**: 静态分析检测未使用变量/函数
- **示例**:

```cpp
// Bad - 未使用的变量
void process() {
    int x = 10;
    int y = 20;  // 未使用
    return x * 2;
}

// Bad - 未使用的成员变量
class MyClass {
    int m_unusedValue;  // 未使用
};

// Good - 删除未使用变量或使用 [[maybe_unused]] 标注
[[maybe_unused]] int keepForFuture = 10;
```

- **建议修改**: 删除未使用的变量和函数

---

### [CPP-NH003] 冗余的 const

- **描述**: 对值类型参数添加不必要的 const
- **影响**: 不影响功能但显得冗余
- **检测方式**: 检测按值传递的参数使用 const
- **示例**:

```cpp
// Bad - 按值传递不需要 const
void process(const int value);    // 冗余
void process(const QString str);  // 冗余

// Good - 按引用传递使用 const
void process(int value);
void process(const QString& str);

// Good - 返回值不需要 const
const int getValue();  // 冗余
int getValue();         // 正确
```

- **建议修改**: 按值传递的参数不需要 const，返回值不需要 const

---

### [CPP-NH004] 可以使用 auto 简化类型声明

- **描述**: 使用冗长的类型声明可以用 `auto` 简化
- **影响**: 降低代码可读性
- **检测方式**: 检测右边表达式类型明确的冗长类型声明
- **示例**:

```cpp
// Bad - 冗长的类型
std::map<QString, int>::const_iterator it = data.begin();

// Bad - 模板类型
QSharedPointer<MyClass> ptr = QSharedPointer<MyClass>::create();

// Good - 使用 auto (C++11)
auto it = data.begin();
auto ptr = QSharedPointer<MyClass>::create();

// 例外 - 类型不够明确时不要用 auto
auto result = calculate();  // 需要看函数定义才知道类型，考虑不使用 auto
```

- **建议修改**: 在类型明确的情况下使用 `auto` 简化代码

---

### [CPP-NH005] 可以使用 lambda 替代函数对象

- **描述**: 使用简单的辅助函数可以用 lambda 替代
- **影响**: 代码更简洁，作用域更局部
- **检测方式**: 检测只在一处使用的辅助函数
- **示例**:

```cpp
// Bad - 只在一处使用的辅助函数
static bool isGreaterThanFive(int value) {
    return value > 5;
}

void process() {
    QList<int> filtered = values.filter(isGreaterThanFive);
}

// Good - 使用 lambda
void process() {
    QList<int> filtered = values.filter([](int value) {
        return value > 5;
    });
}
```

- **建议修改**: 单次使用的简单函数考虑用 lambda 替代

---

### [CPP-NH006] QString 重复使用 toUtf8().constData()

- **描述**: 多次调用 `toUtf8().constData()` 而不是缓存结果
- **影响**: 不必要的内存分配和转换
- **检测方式**: 检测同一字符串多次转换
- **示例**:

```cpp
// Bad - 多次转换
someFunction(s.toUtf8().constData());
anotherFunction(s.toUtf8().constData());

// Good - 缓存结果
QByteArray utf = s.toUtf8();
const char* data = utf.constData();
someFunction(data);
anotherFunction(data);

// Good - 如果函数接受 QString 直接传递
someFunction(s);
anotherFunction(s);
```

- **建议修改**: 缓存 `toUtf8()` 结果或直接使用 `QString`

---

## 参考资源

- [Qt Coding Conventions](https://wiki.qt.io/Qt_Coding_Conventions)
- [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html)
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/)
- [Effective Modern C++](https://www.oreilly.com/library/view/effective-modern-c/9781491908419/)
- [QThreadPool and Qt Concurrent](https://doc.qt.io/qt-6/qthreadpool.html)
