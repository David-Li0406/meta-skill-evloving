# 深入理解工厂模式 (Factory Pattern)

## 一、简单工厂 (Simple Factory) 进化

### 1.1 基础实现 (switch-case)
```java
public class SimpleFactory {
    public static Product create(String type) {
        if ("A".equals(type)) return new ProductA();
        else if ("B".equals(type)) return new ProductB();
        throw new IllegalArgumentException();
    }
}
```
**缺点**: 违反开闭原则，新增产品需修改代码。

### 1.2 进阶实现 (Registry Map)
使用 Map 消除 `if-else`，实现更优雅的扩展。

```java
public class ProductFactory {
    private static final Map<String, Supplier<Product>> MAP = new ConcurrentHashMap<>();

    static {
        MAP.put("A", ProductA::new);
        MAP.put("B", ProductB::new);
    }

    public static void register(String type, Supplier<Product> creator) {
        MAP.put(type, creator);
    }

    public static Product create(String type) {
        Supplier<Product> creator = MAP.get(type);
        if (creator == null) throw new IllegalArgumentException();
        return creator.get();
    }
}
```

## 二、工厂方法 (Factory Method)

**核心思想**: 延迟到子类实现。

```java
// 抽象工厂
public interface Creator {
    Product create();
    
    // 模板方法
    default void doSomething() {
        Product p = create();
        p.use();
    }
}

// 具体工厂
public class CreatorA implements Creator {
    @Override
    public Product create() { return new ProductA(); }
}
```

## 三、抽象工厂 (Abstract Factory)

**核心思想**: 产品族 (Family of Products)。
例如：Windows 风格的 Button + Window；Mac 风格的 Button + Window。

```java
public interface GUIFactory {
    Button createButton();
    Window createWindow();
}

public class WinFactory implements GUIFactory {
    // 生产 Windows 产品族
    public Button createButton() { return new WinButton(); }
    public Window createWindow() { return new WinWindow(); }
}
```

## 四、Spring 中的工厂模式

### 4.1 BeanFactory
Spring IOC 容器的顶层接口，典型的工厂模式。
`getBean("id")` 就是工厂方法。

### 4.2 FactoryBean
**面试高频点**: `BeanFactory` vs `FactoryBean`.
*   `FactoryBean` 是一个 Bean，但它生产的对象不是它自己，而是 `getObject()` 返回的对象。
*   常用于集成第三方框架 (MyBatis `SqlSessionFactoryBean`, Dubbo `ReferenceBean`)。

```java
// Spring 内部源码示意
if (bean instanceof FactoryBean) {
    return ((FactoryBean) bean).getObject();
}
```
