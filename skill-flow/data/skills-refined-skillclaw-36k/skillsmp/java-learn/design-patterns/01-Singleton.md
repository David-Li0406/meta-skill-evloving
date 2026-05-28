# 单例模式 (Singleton Pattern)

## 一、什么是单例模式

单例模式是一种创建型设计模式，它确保一个类只有一个实例，并提供一个全局访问点来获取该实例。

### 核心要点
- **私有构造函数**：防止外部通过 new 创建实例
- **静态私有实例**：类内部持有唯一实例
- **公共静态方法**：提供全局访问点

## 二、单例模式的所有实现方式

### 1. 饿汉式（静态常量）

```java
/**
 * 饿汉式 - 静态常量
 * 优点：线程安全，类加载时就初始化
 * 缺点：不能延迟加载，可能造成内存浪费
 */
public class Singleton01 {
    // 类加载时就创建实例
    private static final Singleton01 INSTANCE = new Singleton01();
    
    // 私有构造函数
    private Singleton01() {
        // 防止反射破坏单例
        if (INSTANCE != null) {
            throw new RuntimeException("单例已存在，禁止通过反射创建");
        }
    }
    
    public static Singleton01 getInstance() {
        return INSTANCE;
    }
}
```

### 2. 饿汉式（静态代码块）

```java
/**
 * 饿汉式 - 静态代码块
 * 优点：线程安全，适合复杂初始化逻辑
 * 缺点：不能延迟加载
 */
public class Singleton02 {
    private static final Singleton02 INSTANCE;
    
    static {
        // 可以处理异常或复杂初始化
        try {
            INSTANCE = new Singleton02();
        } catch (Exception e) {
            throw new RuntimeException("初始化失败", e);
        }
    }
    
    private Singleton02() {}
    
    public static Singleton02 getInstance() {
        return INSTANCE;
    }
}
```

### 3. 懒汉式（线程不安全）

```java
/**
 * 懒汉式 - 线程不安全
 * 优点：延迟加载
 * 缺点：多线程环境下会创建多个实例，不推荐使用
 */
public class Singleton03 {
    private static Singleton03 instance;
    
    private Singleton03() {}
    
    public static Singleton03 getInstance() {
        if (instance == null) {
            instance = new Singleton03();
        }
        return instance;
    }
}
```

### 4. 懒汉式（同步方法）

```java
/**
 * 懒汉式 - 同步方法
 * 优点：线程安全，延迟加载
 * 缺点：每次获取都要同步，效率低下
 */
public class Singleton04 {
    private static Singleton04 instance;
    
    private Singleton04() {}
    
    public static synchronized Singleton04 getInstance() {
        if (instance == null) {
            instance = new Singleton04();
        }
        return instance;
    }
}
```

### 5. 双重检查锁定（DCL - Double-Checked Locking）

```java
/**
 * 双重检查锁定 - 推荐使用
 * 优点：线程安全，延迟加载，效率高
 * 注意：必须使用 volatile 防止指令重排序
 */
public class Singleton05 {
    // volatile 保证可见性和禁止指令重排序
    private static volatile Singleton05 instance;
    
    private Singleton05() {}
    
    public static Singleton05 getInstance() {
        // 第一次检查：避免不必要的同步
        if (instance == null) {
            synchronized (Singleton05.class) {
                // 第二次检查：防止多线程创建多个实例
                if (instance == null) {
                    instance = new Singleton05();
                }
            }
        }
        return instance;
    }
}
```

#### DCL 为什么需要 volatile？

```
new Singleton05() 实际上分为三步：
1. 分配内存空间
2. 初始化对象
3. 将引用指向分配的内存

JVM 可能会进行指令重排序，变成 1 -> 3 -> 2
如果线程A执行到 3，线程B判断 instance != null，就会返回未初始化完成的对象
volatile 禁止指令重排序，保证正确的执行顺序
```

### 6. 静态内部类（推荐）

```java
/**
 * 静态内部类 - 强烈推荐
 * 优点：线程安全，延迟加载，效率高，代码简洁
 * 原理：利用 JVM 类加载机制保证线程安全
 */
public class Singleton06 {
    
    private Singleton06() {}
    
    // 静态内部类在外部类加载时不会加载
    // 只有调用 getInstance() 时才会加载 SingletonHolder
    private static class SingletonHolder {
        private static final Singleton06 INSTANCE = new Singleton06();
    }
    
    public static Singleton06 getInstance() {
        return SingletonHolder.INSTANCE;
    }
}
```

### 7. 枚举单例（最安全）

```java
/**
 * 枚举单例 - 最安全，Effective Java 推荐
 * 优点：
 * 1. 线程安全
 * 2. 防止反射攻击
 * 3. 防止序列化破坏
 * 4. 代码最简洁
 */
public enum Singleton07 {
    INSTANCE;
    
    // 可以添加实例方法
    public void doSomething() {
        System.out.println("执行业务逻辑");
    }
    
    // 可以添加实例变量
    private String name;
    
    public String getName() {
        return name;
    }
    
    public void setName(String name) {
        this.name = name;
    }
}

// 使用方式
// Singleton07.INSTANCE.doSomething();
```

### 8. 使用 CAS 实现（无锁）

```java
/**
 * CAS 实现单例 - 无锁实现
 * 优点：无锁，性能高
 * 缺点：高并发下可能创建多个对象（但只有一个会被使用），存在自旋开销
 */
public class Singleton08 {
    private static final AtomicReference<Singleton08> INSTANCE = 
        new AtomicReference<>();
    
    private Singleton08() {}
    
    public static Singleton08 getInstance() {
        while (true) {
            Singleton08 instance = INSTANCE.get();
            if (instance != null) {
                return instance;
            }
            instance = new Singleton08();
            if (INSTANCE.compareAndSet(null, instance)) {
                return instance;
            }
        }
    }
}
```

## 三、单例模式的破坏与防护

### 1. 反射攻击

```java
// 反射破坏单例
public class ReflectionAttack {
    public static void main(String[] args) throws Exception {
        Singleton06 instance1 = Singleton06.getInstance();
        
        Constructor<Singleton06> constructor = 
            Singleton06.class.getDeclaredConstructor();
        constructor.setAccessible(true);
        Singleton06 instance2 = constructor.newInstance();
        
        System.out.println(instance1 == instance2); // false
    }
}

// 防护方式：在构造函数中检查
private Singleton() {
    if (instance != null) {
        throw new RuntimeException("禁止反射创建实例");
    }
}
```

### 2. 序列化攻击

```java
// 序列化破坏单例
public class SerializationAttack {
    public static void main(String[] args) throws Exception {
        Singleton06 instance1 = Singleton06.getInstance();
        
        // 序列化
        ObjectOutputStream oos = new ObjectOutputStream(
            new FileOutputStream("singleton.obj"));
        oos.writeObject(instance1);
        
        // 反序列化
        ObjectInputStream ois = new ObjectInputStream(
            new FileInputStream("singleton.obj"));
        Singleton06 instance2 = (Singleton06) ois.readObject();
        
        System.out.println(instance1 == instance2); // false
    }
}

// 防护方式：添加 readResolve 方法
private Object readResolve() {
    return getInstance();
}
```

## 四、单例模式的应用场景

### 1. Spring 中的单例 Bean

```java
@Component
@Scope("singleton") // 默认就是单例
public class UserService {
    // Spring 容器保证只创建一个实例
}
```

### 2. Runtime 类

```java
// JDK 中的 Runtime 就是典型的饿汉式单例
public class Runtime {
    private static Runtime currentRuntime = new Runtime();
    
    public static Runtime getRuntime() {
        return currentRuntime;
    }
    
    private Runtime() {}
}
```

### 3. 日志框架 Logger

```java
// Logger 通常使用单例模式
private static final Logger logger = LoggerFactory.getLogger(MyClass.class);
```

### 4. 数据库连接池

```java
/**
 * 数据库连接池单例
 */
public class DataSourcePool {
    private static volatile DataSourcePool instance;
    private HikariDataSource dataSource;
    
    private DataSourcePool() {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl("jdbc:mysql://localhost:3306/test");
        config.setUsername("root");
        config.setPassword("password");
        config.setMaximumPoolSize(10);
        dataSource = new HikariDataSource(config);
    }
    
    public static DataSourcePool getInstance() {
        if (instance == null) {
            synchronized (DataSourcePool.class) {
                if (instance == null) {
                    instance = new DataSourcePool();
                }
            }
        }
        return instance;
    }
    
    public Connection getConnection() throws SQLException {
        return dataSource.getConnection();
    }
}
```

### 5. 配置管理器

```java
/**
 * 配置管理器单例
 */
public class ConfigManager {
    private static class Holder {
        private static final ConfigManager INSTANCE = new ConfigManager();
    }
    
    private Properties properties;
    
    private ConfigManager() {
        properties = new Properties();
        try {
            properties.load(getClass().getResourceAsStream("/config.properties"));
        } catch (IOException e) {
            throw new RuntimeException("加载配置文件失败", e);
        }
    }
    
    public static ConfigManager getInstance() {
        return Holder.INSTANCE;
    }
    
    public String getProperty(String key) {
        return properties.getProperty(key);
    }
}
```

## 五、各种实现方式对比

| 实现方式 | 线程安全 | 延迟加载 | 防反射 | 防序列化 | 推荐指数 |
|---------|---------|---------|-------|---------|---------|
| 饿汉式（静态常量） | ✅ | ❌ | ❌ | ❌ | ⭐⭐⭐ |
| 饿汉式（静态代码块） | ✅ | ❌ | ❌ | ❌ | ⭐⭐⭐ |
| 懒汉式（线程不安全） | ❌ | ✅ | ❌ | ❌ | ⭐ |
| 懒汉式（同步方法） | ✅ | ✅ | ❌ | ❌ | ⭐⭐ |
| 双重检查锁定 | ✅ | ✅ | ❌ | ❌ | ⭐⭐⭐⭐ |
| 静态内部类 | ✅ | ✅ | ❌ | ❌ | ⭐⭐⭐⭐⭐ |
| 枚举 | ✅ | ❌ | ✅ | ✅ | ⭐⭐⭐⭐⭐ |
| CAS | ✅ | ✅ | ❌ | ❌ | ⭐⭐⭐ |

## 六、面试常见问题

### Q1: 单例模式有哪几种实现方式？
> 答：主要有饿汉式、懒汉式、双重检查锁定、静态内部类、枚举等实现方式。

### Q2: 为什么双重检查锁定需要 volatile？
> 答：防止指令重排序。new 操作分为分配内存、初始化对象、赋值引用三步，如果发生重排序，其他线程可能获取到未初始化完成的对象。

### Q3: 为什么枚举是最安全的单例实现？
> 答：枚举天然防止反射攻击（JVM 禁止反射创建枚举实例），且自动支持序列化机制，不会因为反序列化创建新实例。

### Q4: 单例模式在 Spring 中是如何实现的？
> 答：Spring 使用 ConcurrentHashMap 存储单例 Bean，通过三级缓存解决循环依赖问题，保证每个 Bean 只创建一次。
