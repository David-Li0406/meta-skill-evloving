package com.example.netty.demo.rpc;

import com.example.netty.demo.codec.DemoMessage;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.SimpleChannelInboundHandler;

import java.nio.charset.StandardCharsets;

public final class RpcServerHandler extends SimpleChannelInboundHandler<DemoMessage> {

    @Override
    protected void channelRead0(ChannelHandlerContext ctx, DemoMessage msg) {
        switch (msg.type()) {
            case PING:
                ctx.writeAndFlush(DemoMessage.pong());
                break;
            case REQUEST:
                String reqBody = new String(msg.body(), StandardCharsets.UTF_8);
                String resp = "echo(" + reqBody + ") from " + ctx.channel().localAddress();
                ctx.writeAndFlush(DemoMessage.response(msg.requestId(), resp));
                break;
            default:
                break;
        }
    }

    @Override
    public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) {
        cause.printStackTrace();
        ctx.close();
    }
}
