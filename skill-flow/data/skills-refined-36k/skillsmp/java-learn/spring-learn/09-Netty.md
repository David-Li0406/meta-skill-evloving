# Netty 架构与高性能原理

## 一、Netty 核心架构：Reactor 模型

### 1.1 为什么选择 Netty？
- **NIO 封装**: JDK 原生 NIO API 繁琐且有 Bug (Epoll Bug)，Netty 提供了易用的 API。
- **高性能**: 零拷贝、对象池、内存池、无锁串行化设计。
- **丰富的协议**: 内置 HTTP, HTTP2, WebSocket, Protobuf, Redis 等编解码器。

### 1.2 线程模型 (EventLoopGroup)
Netty 采用 **主从 Reactor 多线程模型**。
- **Boss Group (主)**: 负责接收连接 (Accept)，将 SocketChannel 注册到 Worker 的 Selector。
- **Worker Group (从)**: 负责 IO 读写 (Read/Write) 和业务处理。

```java
// 1个 Boss 线程，默认 CPU*2 个 Worker 线程
EventLoopGroup bossGroup = new NioEventLoopGroup(1);
EventLoopGroup workerGroup = new NioEventLoopGroup();

try {
    ServerBootstrap b = new ServerBootstrap();
    b.group(bossGroup, workerGroup)
     .channel(NioServerSocketChannel.class)
     // TCP 参数
     .option(ChannelOption.SO_BACKLOG, 1024)
     .childOption(ChannelOption.SO_KEEPALIVE, true)
     .childHandler(new ChannelInitializer<SocketChannel>() {
         @Override
         public void initChannel(SocketChannel ch) {
             ch.pipeline().addLast(new MyServerHandler());
         }
     });

    ChannelFuture f = b.bind(8080).sync();
    f.channel().closeFuture().sync();
} finally {
    bossGroup.shutdownGracefully();
    workerGroup.shutdownGracefully();
}
```

## 二、零拷贝 (Zero-Copy) 实现

### 2.1 Netty 的零拷贝体现在哪里？
1.  **FileRegion (sendfile)**: 直接将文件传输到 Channel，不经过用户态内存。
2.  **CompositeByteBuf**: 组合多个 ByteBuf，逻辑上合并，物理上不拷贝。
3.  **Unpooled.wrappedBuffer**: 将 byte[] 包装成 ByteBuf，不拷贝。
4.  **ByteBuf.slice**: 切片，共享同一块内存。

### 2.2 代码实战：文件零拷贝发送

```java
public class ZeroCopyServerHandler extends SimpleChannelInboundHandler<String> {

    @Override
    protected void channelRead0(ChannelHandlerContext ctx, String msg) throws Exception {
        RandomAccessFile raf = null;
        long length = -1;
        try {
            raf = new RandomAccessFile("large-file.mp4", "r");
            length = raf.length();
        } catch (Exception e) {
            ctx.writeAndFlush("ERR: " + e.getClass().getSimpleName() + ": " + e.getMessage() + '\n');
            return;
        } finally {
            if (length < 0 && raf != null) raf.close();
        }

        ctx.write("OK: " + raf.length() + '\n');
        
        // 核心：使用 DefaultFileRegion 进行零拷贝传输
        // 对应 Linux 的 sendfile 系统调用
        if (ctx.pipeline().get(SslHandler.class) == null) {
            // SSL 不支持零拷贝
            ctx.write(new DefaultFileRegion(raf.getChannel(), 0, length));
        } else {
            // 如果有 SSL，只能使用 ChunkedFile
            ctx.write(new ChunkedFile(raf));
        }
        
        ctx.writeAndFlush("\n");
    }
}
```

## 三、拆包与粘包 (Half-Packets & Stick-Packets)

### 3.1 现象与原因
- **粘包**: 发送方发送了两个包 ABC, DEF，接收方收到一个包 ABCDEF。
- **拆包**: 发送方发送 ABCDEF，接收方收到 AB, CDEF。
- **原因**: TCP 是**流式协议**，没有边界。

### 3.2 解决方案
1.  **FixedLengthFrameDecoder**: 固定长度 (如 100 字节)。
2.  **LineBasedFrameDecoder**: 换行符 `\n` 分隔。
3.  **DelimiterBasedFrameDecoder**: 自定义分隔符。
4.  **LengthFieldBasedFrameDecoder** (推荐): 消息头包含长度字段。

```java
// 客户端和服务端都要添加
public class MyProtocolInitializer extends ChannelInitializer<SocketChannel> {
    @Override
    protected void initChannel(SocketChannel ch) {
        ChannelPipeline p = ch.pipeline();
        
        // 解码器：最大长度 65535
        // 长度字段偏移量 0，长度字段占 2 字节
        // 长度调整 0，跳过头部的 2 字节
        p.addLast(new LengthFieldBasedFrameDecoder(65535, 0, 2, 0, 2));
        
        // 编码器：自动在前面加上长度字段
        p.addLast(new LengthFieldPrepender(2));
        
        // 业务处理
        p.addLast(new MyBusinessHandler());
    }
}
```

## 四、ByteBuf 的优势

### 4.1 相比 ByteBuffer
1.  **读写指针分离**: `readerIndex` 和 `writerIndex`，不需要 `flip()`。
2.  **动态扩容**: 类似 ArrayList，写满了自动扩容。
3.  **引用计数 (Reference Counting)**: 用于内存池回收。

### 4.2 内存管理 (PooledByteBufAllocator)
- **Direct Memory (直接内存)**: 分配昂贵，读写快 (少一次内核到用户态拷贝)，适合 IO 频繁场景。
- **Heap Memory (堆内存)**: 分配快，读写慢，由 GC 回收。
- Netty 默认使用 **PooledDirectByteBuf**，复用内存块，减少分配开销和 GC 压力。

```java
// 获取 ByteBuf
ByteBuf buf = ctx.alloc().directBuffer(256); // 从池中获取直接内存
try {
    buf.writeBytes("Hello".getBytes());
    ctx.writeAndFlush(buf);
} finally {
    // 必须手动释放，否则内存泄漏
    // writeAndFlush 会自动释放，但如果异常未写入，需手动 release
    // ReferenceCountUtil.release(buf); 
}
```
