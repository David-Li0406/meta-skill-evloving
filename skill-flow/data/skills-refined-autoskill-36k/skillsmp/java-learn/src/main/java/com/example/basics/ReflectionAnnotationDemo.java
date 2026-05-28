package com.example.basics;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import java.lang.reflect.Method;

public class ReflectionAnnotationDemo {

    public static void main(String[] args) throws Exception {
        Method method = DemoService.class.getDeclaredMethod("hello", String.class);
        Tag tag = method.getAnnotation(Tag.class);

        System.out.println("method name = " + method.getName());
        System.out.println("annotation value = " + (tag == null ? null : tag.value()));

        Object result = method.invoke(new DemoService(), "Java");
        System.out.println("invoke result = " + result);
    }

    static class DemoService {
        @Tag("greeting")
        public String hello(String name) {
            return "Hello, " + name;
        }
    }

    @Target({ElementType.METHOD})
    @Retention(RetentionPolicy.RUNTIME)
    public @interface Tag {
        String value();
    }
}
