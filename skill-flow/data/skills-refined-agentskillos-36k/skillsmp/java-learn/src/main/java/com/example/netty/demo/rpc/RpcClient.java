package com.example.netty.demo.rpc;

import com.example.netty.demo.codec.DemoMessage;
import com.example.netty.demo.codec.DemoMessageDecoder;
import com.example.netty.demo.codec.DemoMessageEncoder;
import io.netty.bootstrap.Bootstrap;
import io.netty.channel.Channel;
import io.netty.channel.ChannelInitializer;
import io.netty.channel.ChannelOption;
import io.netty.channel.EventLoop;
import io.netty.channel.EventLoopGroup;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.SocketChannel;
import io.netty.channel.socket.nio.NioSocketChannel;
import io.netty.handler.codec.LengthFieldBasedFrameDecoder;
import io.netty.handler.codec.LengthFieldPrepender;

import java.util.Scanner;
import java.util.concurrent.ThreadLocalRandom;
import java.util.concurrent.TimeUnit;

public final class RpcClient {

    public static void main(String[] args) throws InterruptedException {
        String host = args.length > 0 ? args[0] : "127.0.0.1";
        int port = args.length > 1 ? Integer.parseInt(args[1]) : 18080;

        EventLoopGroup group = new NioEventLoopGroup(1);

        try {
            RpcClientHandler handler = new RpcClientHandler();

            Bootstrap b = new Bootstrap();
            b.group(group)
             .channel(NioSocketChannel.class)
             .option(ChannelOption.TCP_NODELAY, true)
             .handler(new ChannelInitializer<SocketChannel>() {
                 @Override
                 protected void initChannel(SocketChannel ch) {
                     ch.pipeline()
                       .addLast(new LengthFieldBasedFrameDecoder(
                           1024 * 1024,
                           0,
                           4,
                           0,
                           4
                       ))
                       .addLast(new LengthFieldPrepender(4))
                       .addLast(new DemoMessageDecoder())
                       .addLast(new DemoMessageEncoder())
                       .addLast(handler);
                 }
             });

            Channel ch = b.connect(host, port).sync().channel();
            System.out.println("RPC client connected to " + host + ":" + port);

            startHeartbeat(ch.eventLoop(), ch);

            try (Scanner scanner = new Scanner(System.in)) {
                while (true) {
                    System.out.print("input> ");
                    String line = scanner.nextLine();
                    if (line == null) {
                        break;
                    }
                    if ("quit".equalsIgnoreCase(line) || "exit".equalsIgnoreCase(line)) {
                        break;
                    }

                    long requestId = ThreadLocalRandom.current().nextLong(Long.MAX_VALUE);
                    handler.call(ch, requestId, line, 3_000)
                           .whenComplete((resp, ex) -> {
                               if (ex != null) {
                                   System.out.println("ERR: " + ex.getMessage());
                               } else {
                                   System.out.println("OK : " + resp);
                               }
                           });
                }
            }

            ch.close().sync();
        } finally {
            group.shutdownGracefully();
        }
    }

    private static void startHeartbeat(EventLoop eventLoop, Channel ch) {
        eventLoop.scheduleAtFixedRate(() -> {
            if (ch.isActive()) {
                ch.writeAndFlush(DemoMessage.ping());
            }
        }, 1, 3, TimeUnit.SECONDS);
    }
}
