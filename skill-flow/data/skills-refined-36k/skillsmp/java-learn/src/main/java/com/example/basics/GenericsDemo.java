package com.example.basics;

import java.util.ArrayList;
import java.util.List;

public class GenericsDemo {

    public static void main(String[] args) {
        extendsDemo();
        superDemo();
    }

    private static void extendsDemo() {
        System.out.println("=== ? extends demo (producer/read) ===");
        List<Integer> ints = java.util.Arrays.asList(1, 2, 3);
        List<? extends Number> numbers = ints;

        Number n = numbers.get(0);
        System.out.println("read = " + n);

        // numbers.add(1); // compile error: cannot add to ? extends
    }

    private static void superDemo() {
        System.out.println("=== ? super demo (consumer/write) ===");
        List<? super Integer> sink = new ArrayList<Number>();
        sink.add(1);
        sink.add(2);

        Object first = sink.get(0);
        System.out.println("read as Object = " + first);
    }
}
