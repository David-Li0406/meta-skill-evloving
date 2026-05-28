---
name: netty
description: Netty 学习资料（NIO/模型/源码心智）
---



# netty-basics
[Netty基础]
## TCP 基础
- 连接
- 半包/粘包
- KeepAlive
## Java NIO
- Channel
- Buffer
- Selector
## Reactor 模型
- 单 Reactor
- 主从 Reactor
## Netty 结构
- Bootstrap
- EventLoop
- ChannelPipeline
- ByteBuf
- 零拷贝
## 常见实战
- RPC
- WebSocket
- IM
- 网关

---

# network-layering
[网络分成]
##  应用层
- HTTP
- WebSocket
- 自定义协议
## 传输层
- TCP
- UDP
## 网络层
- IP
## 链路层
- 以太网

## 面试常问：
- TCP 的可靠性来自哪些机制（序列号、ACK、重传、滑动窗口、拥塞控制）


# tcp-udp
[TCP/UDP 核心差异]
## TCP
- 面向连接
- 可靠
- 有序
- 字节流（重点：半包/粘包）
## UDP
- 无连接
- 尽力而为
- 报文

# bag
[半包/粘包]
# 根因：TCP 是“字节流”，应用消息边界不是天然存在
# 解决：
- 定长消息
- 分隔符（换行符等）
- 长度字段（Length-Field Based，最推荐）



# java-nio
[Java NIO 必备概念]
## Channel
- 连接
- 读写通道
## Buffer
- 读写切换（position/limit）
## Selector
- 多路复用（一个线程管理多连接 IO）

## 对比：
- BIO：连接数上来线程数爆炸
- NIO：Selector 事件驱动


# reactor
[Reactor 模型（Netty 的核心思想）]
##  Reactor：负责事件分发
- accept
- read
- write）
## Handler：处理事件
- 编解码
- 业务处理

# netty-model
## 单 Reactor 
- 单线程简单，但业务耗时会影响 IO
## 单 Reactor 
- 多线程：IO 与业务分离
## 主从 Reactor
- Boss 处理 accept
- Worker 处理 read/write



# Netty 架构要点
[Netty 架构要点]
## Bootstrap
- `ServerBootstrap`：服务端启动器
- `Bootstrap`：客户端启动器

##  EventLoop & EventLoopGroup
- EventLoop：事件循环线程（一个 EventLoop 可管理多个 Channel）
- EventLoopGroup：一组 EventLoop

## ChannelPipeline & ChannelHandler
- Pipeline：责任链/管道（入站 inbound / 出站 outbound）
- Handler：可复用 `@Sharable` 需要线程安全

## Future/Promise
- Netty 的异步回调模型（对比 JDK Future）

##  ByteBuf 的优势
- 读写指针分离（readerIndex/writerIndex）
- 池化（PooledByteBufAllocator）减少 GC 压力

###  零拷贝（概念级）
- `CompositeByteBuf`：逻辑组合，避免内存拷贝
- `FileRegion`/`sendfile`：文件传输减少用户态拷贝

# 常用案例
[常用案例]
## 自定义协议：长度字段 + 编解码
## RPC：请求响应、超时、连接复用、心跳
## WebSocket：握手升级、心跳、广播


# 源码学习心智模型
[源码学习心智模型]
## 启动：`ServerBootstrap#bind` → `AbstractBootstrap#doBind`
## 注册：`Channel#register` → `NioEventLoop#register`
## IO 事件：`NioEventLoop#run`（select 循环）
## 读写：`AbstractNioByteChannel#read` / `AbstractChannelHandlerContext#invokeChannelRead`
## Pipeline：`DefaultChannelPipeline`

---

#  高频面试题
[高频面试题]
## Netty 为什么比 BIO 性能好？（线程模型 + 少 GC + 事件驱动）
## 半包/粘包是什么？LengthFieldBasedFrameDecoder 怎么用？
## EventLoop 和线程的关系？一个 Channel 是否会被多个 EventLoop 调度？
## Pipeline 的 inbound/outbound 传播顺序是什么？
## ByteBuf 为什么要池化？池化会带来什么坑（引用计数泄漏）？