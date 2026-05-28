package com.example.basics;

import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

public class EqualsHashCodeDemo {

    public static void main(String[] args) {
        badKeyDemo();
        goodKeyDemo();
    }

    private static void badKeyDemo() {
        System.out.println("=== BadKey demo (mutable key) ===");

        Map<UserBadKey, String> map = new HashMap<>();
        UserBadKey key = new UserBadKey(1, "Alice");
        map.put(key, "value");

        // 修改字段导致 hashCode 改变
        key.name = "Alice-Updated";

        System.out.println("get after mutate = " + map.get(key));
        System.out.println("containsKey after mutate = " + map.containsKey(key));
        System.out.println("map size = " + map.size());
        System.out.println();
    }

    private static void goodKeyDemo() {
        System.out.println("=== GoodKey demo (immutable key) ===");

        Map<UserGoodKey, String> map = new HashMap<>();
        UserGoodKey key = new UserGoodKey(1, "Alice");
        map.put(key, "value");

        System.out.println("get = " + map.get(new UserGoodKey(1, "Alice")));
        System.out.println("containsKey = " + map.containsKey(new UserGoodKey(1, "Alice")));
        System.out.println("map size = " + map.size());
        System.out.println();
    }

    static class UserBadKey {
        private final long id;
        private String name;

        UserBadKey(long id, String name) {
            this.id = id;
            this.name = name;
        }

        @Override
        public boolean equals(Object obj) {
            if (this == obj) return true;
            if (obj == null || getClass() != obj.getClass()) return false;
            UserBadKey other = (UserBadKey) obj;
            return id == other.id && Objects.equals(name, other.name);
        }

        @Override
        public int hashCode() {
            return Objects.hash(id, name);
        }
    }

    static class UserGoodKey {
        private final long id;
        private final String name;

        UserGoodKey(long id, String name) {
            this.id = id;
            this.name = name;
        }

        @Override
        public boolean equals(Object obj) {
            if (this == obj) return true;
            if (obj == null || getClass() != obj.getClass()) return false;
            UserGoodKey other = (UserGoodKey) obj;
            return id == other.id && Objects.equals(name, other.name);
        }

        @Override
        public int hashCode() {
            return Objects.hash(id, name);
        }
    }
}
