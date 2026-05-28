package com.example.netty.demo.codec;

import io.netty.buffer.ByteBuf;
import io.netty.channel.ChannelHandlerContext;
import io.netty.handler.codec.MessageToByteEncoder;

public final class DemoMessageEncoder extends MessageToByteEncoder<DemoMessage> {

    @Override
    protected void encode(ChannelHandlerContext ctx, DemoMessage msg, ByteBuf out) {
        // Frame format (without the outer length field):
        // magic(2) + version(1) + msgType(1) + requestId(8) + bodyLen(4) + body(n)
        out.writeShort(DemoMessage.MAGIC);
        out.writeByte(DemoMessage.VERSION);
        out.writeByte(msg.type().code());
        out.writeLong(msg.requestId());

        byte[] body = msg.body();
        out.writeInt(body.length);
        out.writeBytes(body);
    }
}
