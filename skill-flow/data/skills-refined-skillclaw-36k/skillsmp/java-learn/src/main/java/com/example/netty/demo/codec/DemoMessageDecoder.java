package com.example.netty.demo.codec;

import io.netty.buffer.ByteBuf;
import io.netty.channel.ChannelHandlerContext;
import io.netty.handler.codec.ReplayingDecoder;

import java.util.List;

public final class DemoMessageDecoder extends ReplayingDecoder<Void> {

    @Override
    protected void decode(ChannelHandlerContext ctx, ByteBuf in, List<Object> out) {
        short magic = in.readShort();
        if (magic != DemoMessage.MAGIC) {
            throw new IllegalArgumentException("Bad magic: " + Integer.toHexString(magic & 0xFFFF));
        }

        byte version = in.readByte();
        if (version != DemoMessage.VERSION) {
            throw new IllegalArgumentException("Bad version: " + version);
        }

        DemoMessage.MessageType type = DemoMessage.MessageType.fromCode(in.readByte());
        long requestId = in.readLong();
        int bodyLen = in.readInt();
        if (bodyLen < 0 || bodyLen > 1024 * 1024) {
            throw new IllegalArgumentException("Bad bodyLen: " + bodyLen);
        }

        byte[] body = new byte[bodyLen];
        in.readBytes(body);

        out.add(new DemoMessage(type, requestId, body));
    }
}
