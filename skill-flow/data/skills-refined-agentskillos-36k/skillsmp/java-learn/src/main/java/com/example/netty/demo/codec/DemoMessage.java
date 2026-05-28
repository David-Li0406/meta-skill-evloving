package com.example.netty.demo.codec;

import java.nio.charset.StandardCharsets;

public final class DemoMessage {

    public static final short MAGIC = (short) 0xCAFE;
    public static final byte VERSION = 1;

    public enum MessageType {
        PING((byte) 1),
        PONG((byte) 2),
        REQUEST((byte) 3),
        RESPONSE((byte) 4);

        private final byte code;

        MessageType(byte code) {
            this.code = code;
        }

        public byte code() {
            return code;
        }

        public static MessageType fromCode(byte code) {
            for (MessageType value : values()) {
                if (value.code == code) {
                    return value;
                }
            }
            throw new IllegalArgumentException("Unknown msgType=" + code);
        }
    }

    private final MessageType type;
    private final long requestId;
    private final byte[] body;

    public DemoMessage(MessageType type, long requestId, byte[] body) {
        this.type = type;
        this.requestId = requestId;
        this.body = body;
    }

    public static DemoMessage ping() {
        return new DemoMessage(MessageType.PING, 0, new byte[0]);
    }

    public static DemoMessage pong() {
        return new DemoMessage(MessageType.PONG, 0, new byte[0]);
    }

    public static DemoMessage request(long requestId, String body) {
        return new DemoMessage(MessageType.REQUEST, requestId, body.getBytes(StandardCharsets.UTF_8));
    }

    public static DemoMessage response(long requestId, String body) {
        return new DemoMessage(MessageType.RESPONSE, requestId, body.getBytes(StandardCharsets.UTF_8));
    }

    public MessageType type() {
        return type;
    }

    public long requestId() {
        return requestId;
    }

    public byte[] body() {
        return body;
    }
}
