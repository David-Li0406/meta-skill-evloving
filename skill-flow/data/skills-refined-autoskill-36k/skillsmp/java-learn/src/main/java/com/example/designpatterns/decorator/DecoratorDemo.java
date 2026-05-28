package com.example.designpatterns.decorator;

import java.io.FilterInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;

public class DecoratorDemo {

    public static void main(String[] args) throws Exception {
        String payload = "hello decorator";

        try (InputStream in = new UppercaseInputStream(
                new java.io.ByteArrayInputStream(payload.getBytes(StandardCharsets.UTF_8)))) {
            byte[] buf = readFully(in);
            System.out.println(new String(buf, StandardCharsets.UTF_8));
        }
    }

    private static byte[] readFully(InputStream in) throws IOException {
        java.io.ByteArrayOutputStream out = new java.io.ByteArrayOutputStream();
        byte[] buffer = new byte[1024];
        int n;
        while ((n = in.read(buffer)) != -1) {
            out.write(buffer, 0, n);
        }
        return out.toByteArray();
    }

    static class UppercaseInputStream extends FilterInputStream {

        protected UppercaseInputStream(InputStream in) {
            super(in);
        }

        @Override
        public int read() throws IOException {
            int b = super.read();
            if (b == -1) {
                return -1;
            }
            return Character.toUpperCase((char) b);
        }

        @Override
        public int read(byte[] b, int off, int len) throws IOException {
            int n = super.read(b, off, len);
            if (n <= 0) {
                return n;
            }
            for (int i = off; i < off + n; i++) {
                b[i] = (byte) Character.toUpperCase((char) b[i]);
            }
            return n;
        }
    }
}
