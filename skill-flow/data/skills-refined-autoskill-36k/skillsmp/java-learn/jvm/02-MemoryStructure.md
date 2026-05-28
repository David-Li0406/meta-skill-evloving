# JVM Memory Structure (内存结构)

## 一、运行时数据区域

Java 虚拟机在执行 Java 程序的过程中会把它所管理的内存划分为若干个不同的数据区域。

![JVM Runtime Data Areas](https://img-blog.csdnimg.cn/20210508160530752.png)

### 1. 程序计数器 (Program Counter Register)
- **作用**：当前线程所执行的字节码的行号指示器。
- **特点**：
    - **线程私有**：每个线程都有独立的程序计数器。
    - **唯一不会 OOM**：Java 虚拟机规范中唯一没有规定 `OutOfMemoryError` 情况的区域。
    - 如果执行的是 Native 方法，计数器值为空 (Undefined)。

### 2. Java 虚拟机栈 (Java Virtual Machine Stacks)
- **作用**：描述 Java 方法执行的内存模型。每个方法在执行的同时都会创建一个 **栈帧 (Stack Frame)**。
- **栈帧包含**：
    - **局部变量表**：存放编译期可知的各种基本数据类型、对象引用。
    - **操作数栈**：用于计算过程中的临时存储。
    - **动态链接**：指向运行时常量池的方法引用。
    - **方法出口**：方法返回地址。
- **异常**：
    - `StackOverflowError`：线程请求的栈深度大于虚拟机允许的深度（如无限递归）。
    - `OutOfMemoryError`：如果栈可以动态扩展，扩展时无法申请到足够的内存。

### 3. 本地方法栈 (Native Method Stack)
- **作用**：与虚拟机栈类似，不过它是为虚拟机使用到的 **Native** 方法服务。
- **异常**：同样会抛出 `StackOverflowError` 和 `OutOfMemoryError`。

### 4. Java 堆 (Java Heap)
- **作用**：存放对象实例。是垃圾收集器管理的主要区域 ("GC 堆")。
- **特点**：
    - **线程共享**：所有线程共享同一块堆内存。
    - **最大的一块内存**：虚拟机启动时创建。
- **结构**（分代收集算法）：
    - **新生代 (Young Generation)**：
        - Eden 区
        - Survivor 区 (S0, S1)
    - **老年代 (Old Generation)**
- **异常**：`OutOfMemoryError: Java heap space` (堆内存不足)。

### 5. 方法区 (Method Area)
- **作用**：存储已被虚拟机加载的 **类信息、常量、静态变量、即时编译器编译后的代码** 等数据。
- **演变**：
    - **JDK 1.7 及之前**：实现为 **永久代 (PermGen)**。
    - **JDK 1.8 及之后**：实现为 **元空间 (Metaspace)**，使用本地内存。
- **异常**：`OutOfMemoryError: Metaspace` (元空间溢出) 或 `PermGen space` (永久代溢出)。

### 6. 运行时常量池 (Runtime Constant Pool)
- 是方法区的一部分。
- 用于存放编译期生成的各种字面量和符号引用。
- 具备动态性，运行期间也可以将新的常量放入池中（如 `String.intern()`）。

### 7. 直接内存 (Direct Memory)
- 不是虚拟机运行时数据区的一部分，也不是 Java 虚拟机规范中定义的内存区域。
- NIO (New Input/Output) 类引入了一种基于通道 (Channel) 和缓冲区 (Buffer) 的 I/O 方式，可以使用 Native 函数库直接分配堆外内存。
- 避免了在 Java 堆和 Native 堆中来回复制数据，提高性能。
- **异常**：`OutOfMemoryError: Direct buffer memory`。

## 二、常用字节码指令简介

- **加载与存储指令**：`iload`, `istore`, `ldc`, `bipush`
- **运算指令**：`iadd`, `isub`, `imul`, `idiv`
- **类型转换指令**：`i2l`, `i2f`, `d2i`
- **对象创建与访问指令**：`new`, `getfield`, `putfield`, `invokevirtual`
- **操作数栈管理指令**：`pop`, `dup`, `swap`
- **控制转移指令**：`ifeq`, `goto`, `tableswitch`
- **方法调用和返回指令**：`invokevirtual`, `invokespecial`, `invokestatic`, `return`

## 三、内存溢出案例详解

### 1. 堆内存溢出 (Java Heap Space)

**触发条件**：堆中没有足够空间来分配新对象，且无法再扩展。

```java
/**
 * VM 参数：-Xms20m -Xmx20m -XX:+HeapDumpOnOutOfMemoryError
 */
public class HeapOOM {
    static class OOMObject {}
    
    public static void main(String[] args) {
        List<OOMObject> list = new ArrayList<>();
        while (true) {
            list.add(new OOMObject()); // 不断创建对象，无法被GC回收
        }
    }
}
// 输出：java.lang.OutOfMemoryError: Java heap space
```

**排查方法**：
1. 添加 `-XX:+HeapDumpOnOutOfMemoryError` 参数，OOM 时自动生成 dump 文件。
2. 使用 MAT 或 VisualVM 分析 dump 文件。
3. 判断是 **内存泄漏** 还是 **内存溢出**：
   - **内存泄漏**：对象无用但无法被 GC 回收（如静态集合只增不减）。
   - **内存溢出**：对象确实需要存活，堆空间不够（需增大 `-Xmx`）。

### 2. 虚拟机栈和本地方法栈溢出 (StackOverflowError)

**触发条件**：线程请求的栈深度大于虚拟机允许的最大深度。

```java
/**
 * VM 参数：-Xss256k
 */
public class StackSOF {
    private int stackLength = 1;
    
    public void stackLeak() {
        stackLength++;
        stackLeak(); // 无限递归调用
    }
    
    public static void main(String[] args) {
        StackSOF sof = new StackSOF();
        try {
            sof.stackLeak();
        } catch (Throwable e) {
            System.out.println("栈深度: " + sof.stackLength);
            throw e;
        }
    }
}
// 输出：
// 栈深度: 2456
// Exception in thread "main" java.lang.StackOverflowError
```

**常见场景**：
- 无限递归调用（最常见）
- 大量局部变量导致栈帧过大

### 3. 方法区 / 元空间溢出 (Metaspace)

**触发条件**：类加载过多，元空间空间不足。

```java
/**
 * VM 参数：-XX:MetaspaceSize=10m -XX:MaxMetaspaceSize=10m
 * 需要依赖 CGLib 库
 */
public class MetaspaceOOM {
    public static void main(String[] args) {
        while (true) {
            Enhancer enhancer = new Enhancer();
            enhancer.setSuperclass(OOMObject.class);
            enhancer.setUseCache(false);
            enhancer.setCallback((MethodInterceptor) (obj, method, args1, proxy) 
                -> proxy.invokeSuper(obj, args1));
            enhancer.create(); // 动态生成大量类
        }
    }
    static class OOMObject {}
}
// 输出：java.lang.OutOfMemoryError: Metaspace
```

**常见场景**：
- 大量使用 CGLib / Javassist 动态生成类
- 大量 JSP 文件（每个 JSP 编译成一个类）
- OSGi 应用频繁加载卸载 Bundle

### 4. 直接内存溢出 (Direct Buffer Memory)

**触发条件**：NIO 使用的直接内存超过限制。

```java
/**
 * VM 参数：-Xmx20m -XX:MaxDirectMemorySize=10m
 */
public class DirectMemoryOOM {
    private static final int _1MB = 1024 * 1024;
    
    public static void main(String[] args) throws IllegalAccessException {
        Field unsafeField = Unsafe.class.getDeclaredFields()[0];
        unsafeField.setAccessible(true);
        Unsafe unsafe = (Unsafe) unsafeField.get(null);
        while (true) {
            unsafe.allocateMemory(_1MB); // 直接分配堆外内存
        }
    }
}
// 输出：java.lang.OutOfMemoryError: Direct buffer memory
```

**特征**：
- Heap Dump 文件很小，但程序内存占用很大。
- 常见于使用 NIO 的程序（如 Netty）。

### 5. OOM 排查总结

| OOM 类型 | 错误信息 | 常见原因 | 解决方法 |
|---------|---------|---------|---------|
| 堆溢出 | `Java heap space` | 内存泄漏或堆太小 | 分析 dump，调大 `-Xmx` |
| 栈溢出 | `StackOverflowError` | 无限递归 | 检查递归终止条件 |
| 元空间溢出 | `Metaspace` | 类加载过多 | 调大 `-XX:MaxMetaspaceSize` |
| 直接内存溢出 | `Direct buffer memory` | NIO 使用过多 | 调大 `-XX:MaxDirectMemorySize` |
| 创建线程失败 | `unable to create new native thread` | 线程数过多 | 减少线程数或调小 `-Xss` |

