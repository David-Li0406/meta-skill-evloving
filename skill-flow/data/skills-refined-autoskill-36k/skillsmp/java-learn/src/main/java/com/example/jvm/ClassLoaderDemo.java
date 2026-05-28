package com.example.jvm;

public class ClassLoaderDemo {

    public static void main(String[] args) {
        ClassLoader app = ClassLoaderDemo.class.getClassLoader();
        ClassLoader platform = app == null ? null : app.getParent();
        ClassLoader bootstrap = platform == null ? null : platform.getParent();

        System.out.println("app = " + app);
        System.out.println("platform = " + platform);
        System.out.println("bootstrap = " + bootstrap);

        System.out.println("String classloader = " + String.class.getClassLoader());
    }
}
