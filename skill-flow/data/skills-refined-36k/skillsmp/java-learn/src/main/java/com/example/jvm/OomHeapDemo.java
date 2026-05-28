package com.example.jvm;

import java.util.ArrayList;
import java.util.List;

public class OomHeapDemo {

    public static void main(String[] args) {
        // Warning: demo for OOM. Suggest JVM args: -Xms32m -Xmx32m
        List<byte[]> list = new ArrayList<>();
        while (true) {
            list.add(new byte[1024 * 1024]);
        }
    }
}
