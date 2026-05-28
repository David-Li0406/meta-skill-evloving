---
name: netty
description: Netty 学习资料（NIO/模型/源码心智）
---

# Netty 学习资料

> 目标：搞清楚 Netty 解决了什么问题（高性能网络编程），以及它的核心设计：Reactor、Pipeline、ByteBuf、线程模型。

## 0. 学习路径（推荐）
1. TCP 基础（连接、半包/粘包、KeepAlive）
2. Java NIO（Channel/Buffer/Selector）
3. Reactor 模型（单 Reactor / 主从 Reactor）
4. Netty 结构：Bootstrap、EventLoop、ChannelPipeline
5. ByteBuf & 零拷贝
6. 常见实战：RPC、WebSocket、IM、网关

---

## 1. 网络分层（能说清每层解决什么）
- 应用层：HTTP、WebSocket、自定义协议
- 传输层：TCP/UDP
- 网络层：IP
- 链路层：以太网

面试常问：
- TCP 的可靠性来自哪些机制（序列号、ACK、重传、滑动窗口、拥塞控制）

---

## 2. TCP/UDP 核心差异
- TCP：面向连接、可靠、有序、字节流（重点：半包/粘包）
- UDP：无连接、尽力而为、报文

### 2.1 半包/粘包
- 根因：TCP 是“字节流”，应用消息边界不是天然存在
- 解决：
  - 定长消息
  - 分隔符（换行符等）
  - 长度字段（Length-Field Based，最推荐）

---

## 3. Java NIO 必备概念
- Channel：连接/读写通道
- Buffer：读写切换（position/limit）
- Selector：多路复用（一个线程管理多连接 IO）

对比：
- BIO：连接数上来线程数爆炸
- NIO：Selector 事件驱动

---

## 4. Reactor 模型（Netty 的核心思想）
- Reactor：负责事件分发（accept/read/write）
- Handler：处理事件（编解码、业务处理）

### 4.1 常见模型
- 单 Reactor 单线程：简单，但业务耗时会影响 IO
- 单 Reactor 多线程：IO 与业务分离
- 主从 Reactor：Boss 处理 accept，Worker 处理 read/write

Netty 默认：主从 Reactor（BossGroup + WorkerGroup）

---

## 5. Netty 架构要点
### 5.1 Bootstrap
- `ServerBootstrap`：服务端启动器
- `Bootstrap`：客户端启动器

### 5.2 EventLoop & EventLoopGroup
- EventLoop：事件循环线程（一个 EventLoop 可管理多个 Channel）
- EventLoopGroup：一组 EventLoop

### 5.3 ChannelPipeline & ChannelHandler
- Pipeline：责任链/管道（入站 inbound / 出站 outbound）
- Handler：可复用 `@Sharable` 需要线程安全

### 5.4 Future/Promise
- Netty 的异步回调模型（对比 JDK Future）

---

## 6. ByteBuf 与零拷贝
### 6.1 ByteBuf 的优势
- 读写指针分离（readerIndex/writerIndex）
- 池化（PooledByteBufAllocator）减少 GC 压力

### 6.2 零拷贝（概念级）
- `CompositeByteBuf`：逻辑组合，避免内存拷贝
- `FileRegion`/`sendfile`：文件传输减少用户态拷贝

---

## 7. 常用案例（你可以按需选一个深入）
- 自定义协议：长度字段 + 编解码
- RPC：请求响应、超时、连接复用、心跳
- WebSocket：握手升级、心跳、广播

说明：本仓库当前主要在 `spring-learn/09-Netty.md` 做深入文章，`skills/netty.md` 作为总纲。

---

## 8. 源码学习心智模型（从哪读起）
- 启动：`ServerBootstrap#bind` → `AbstractBootstrap#doBind`
- 注册：`Channel#register` → `NioEventLoop#register`
- IO 事件：`NioEventLoop#run`（select 循环）
- 读写：`AbstractNioByteChannel#read` / `AbstractChannelHandlerContext#invokeChannelRead`
- Pipeline：`DefaultChannelPipeline`

---

## 9. 高频面试题
1. Netty 为什么比 BIO 性能好？（线程模型 + 少 GC + 事件驱动）
2. 半包/粘包是什么？LengthFieldBasedFrameDecoder 怎么用？
3. EventLoop 和线程的关系？一个 Channel 是否会被多个 EventLoop 调度？
4. Pipeline 的 inbound/outbound 传播顺序是什么？
5. ByteBuf 为什么要池化？池化会带来什么坑（引用计数泄漏）？
