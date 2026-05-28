package com.example.netty.demo.rpc;

import com.example.netty.demo.codec.DemoMessage;
import com.example.netty.demo.codec.DemoMessageDecoder;
import com.example.netty.demo.codec.DemoMessageEncoder;
import io.netty.bootstrap.ServerBootstrap;
import io.netty.channel.ChannelFuture;
import io.netty.channel.ChannelInitializer;
import io.netty.channel.ChannelOption;
import io.netty.channel.EventLoopGroup;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.SocketChannel;
import io.netty.channel.socket.nio.NioServerSocketChannel;
import io.netty.handler.codec.LengthFieldBasedFrameDecoder;
import io.netty.handler.codec.LengthFieldPrepender;

public final class RpcServer {

    public static void main(String[] args) throws InterruptedException {
        int port = args.length > 0 ? Integer.parseInt(args[0]) : 18080;

        EventLoopGroup bossGroup = new NioEventLoopGroup(1);
        EventLoopGroup workerGroup = new NioEventLoopGroup();

        try {
            ServerBootstrap b = new ServerBootstrap();
            b.group(bossGroup, workerGroup)
             .channel(NioServerSocketChannel.class)
             .childOption(ChannelOption.TCP_NODELAY, true)
             .childHandler(new ChannelInitializer<SocketChannel>() {
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
                       .addLast(new RpcServerHandler());
                 }
             });

            ChannelFuture bindFuture = b.bind(port).sync();
            System.out.println("RPC server started on port " + port);

            bindFuture.channel().closeFuture().sync();
        } finally {
            bossGroup.shutdownGracefully();
            workerGroup.shutdownGracefully();
        }
    }
}
