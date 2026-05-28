package com.example.netty.demo.rpc;

import com.example.netty.demo.codec.DemoMessage;
import io.netty.channel.Channel;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.SimpleChannelInboundHandler;
import io.netty.util.concurrent.Promise;

import java.nio.charset.StandardCharsets;
import java.util.Map;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.TimeUnit;

public final class RpcClientHandler extends SimpleChannelInboundHandler<DemoMessage> {

    private final Map<Long, Promise<String>> inflight = new ConcurrentHashMap<>();

    public CompletableFuture<String> call(Channel ch, long requestId, String payload, long timeoutMs) {
        Promise<String> promise = ch.eventLoop().newPromise();
        Promise<String> old = inflight.put(requestId, promise);
        if (old != null) {
            old.tryFailure(new IllegalStateException("Duplicate requestId=" + requestId));
        }

        // timeout on eventLoop to keep concurrency model consistent
        ch.eventLoop().schedule(() -> {
            Promise<String> removed = inflight.remove(requestId);
            if (removed != null) {
                removed.tryFailure(new RuntimeException("timeout after " + timeoutMs + "ms"));
            }
        }, timeoutMs, TimeUnit.MILLISECONDS);

        ch.writeAndFlush(DemoMessage.request(requestId, payload)).addListener(f -> {
            if (!f.isSuccess()) {
                Promise<String> removed = inflight.remove(requestId);
                if (removed != null) {
                    removed.tryFailure(f.cause());
                }
            }
        });

        CompletableFuture<String> cf = new CompletableFuture<>();
        promise.addListener(f -> {
            if (f.isSuccess()) {
                cf.complete((String) f.getNow());
            } else {
                cf.completeExceptionally(f.cause());
            }
        });
        return cf;
    }

    @Override
    protected void channelRead0(ChannelHandlerContext ctx, DemoMessage msg) {
        switch (msg.type()) {
            case PONG:
                break;
            case RESPONSE:
                Promise<String> promise = inflight.remove(msg.requestId());
                if (promise != null) {
                    String body = new String(msg.body(), StandardCharsets.UTF_8);
                    promise.trySuccess(body);
                }
                break;
            default:
                break;
        }
    }

    @Override
    public void channelInactive(ChannelHandlerContext ctx) {
        RuntimeException ex = new RuntimeException("channel closed");
        inflight.forEach((id, p) -> p.tryFailure(ex));
        inflight.clear();
    }

    @Override
    public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) {
        cause.printStackTrace();
        ctx.close();
    }
}
