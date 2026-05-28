package com.example.jvm;

import java.util.ArrayList;
import java.util.List;

public class GcLogDemo {

    public static void main(String[] args) {
        List<byte[]> allocations = new ArrayList<>();

        for (int i = 0; i < 200; i++) {
            allocations.add(new byte[1024 * 1024]); // 1MB
            if (i % 20 == 0) {
                System.out.println("allocated " + (i + 1) + " MB");
            }

            if (allocations.size() > 50) {
                allocations.subList(0, 25).clear();
            }
        }

        System.out.println("done");
    }
}
