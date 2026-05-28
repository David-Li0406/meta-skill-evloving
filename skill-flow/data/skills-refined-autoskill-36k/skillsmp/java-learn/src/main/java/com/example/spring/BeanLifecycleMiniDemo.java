package com.example.spring;

import java.util.ArrayList;
import java.util.List;

public class BeanLifecycleMiniDemo {

    public static void main(String[] args) {
        MiniContainer container = new MiniContainer();
        container.addPostProcessor(new LoggingBeanPostProcessor());

        container.register("userService", UserService.class);

        UserService service = container.getBean("userService", UserService.class);
        service.hello();

        container.close();
    }

    interface BeanPostProcessor {
        Object postProcessBeforeInitialization(String beanName, Object bean);

        Object postProcessAfterInitialization(String beanName, Object bean);
    }

    static class LoggingBeanPostProcessor implements BeanPostProcessor {
        @Override
        public Object postProcessBeforeInitialization(String beanName, Object bean) {
            System.out.println("BPP before init: " + beanName);
            return bean;
        }

        @Override
        public Object postProcessAfterInitialization(String beanName, Object bean) {
            System.out.println("BPP after init: " + beanName);
            return bean;
        }
    }

    static class MiniContainer {
        private final List<BeanPostProcessor> processors = new ArrayList<>();
        private final java.util.Map<String, Class<?>> definitions = new java.util.HashMap<>();
        private final java.util.Map<String, Object> singletons = new java.util.HashMap<>();

        void addPostProcessor(BeanPostProcessor processor) {
            processors.add(processor);
        }

        void register(String name, Class<?> type) {
            definitions.put(name, type);
        }

        <T> T getBean(String name, Class<T> type) {
            Object existing = singletons.get(name);
            if (existing != null) {
                return type.cast(existing);
            }

            Class<?> clazz = definitions.get(name);
            if (clazz == null) {
                throw new IllegalArgumentException("no bean definition: " + name);
            }

            Object bean = instantiate(clazz);
            bean = initialize(name, bean);
            singletons.put(name, bean);

            return type.cast(bean);
        }

        private Object instantiate(Class<?> clazz) {
            System.out.println("instantiate: " + clazz.getSimpleName());
            try {
                return clazz.getDeclaredConstructor().newInstance();
            } catch (Exception e) {
                throw new RuntimeException(e);
            }
        }

        private Object initialize(String beanName, Object bean) {
            for (BeanPostProcessor processor : processors) {
                bean = processor.postProcessBeforeInitialization(beanName, bean);
            }

            if (bean instanceof InitializingBean) {
                ((InitializingBean) bean).afterPropertiesSet();
            }

            for (BeanPostProcessor processor : processors) {
                bean = processor.postProcessAfterInitialization(beanName, bean);
            }
            return bean;
        }

        void close() {
            for (Object bean : singletons.values()) {
                if (bean instanceof DisposableBean) {
                    ((DisposableBean) bean).destroy();
                }
            }
        }
    }

    interface InitializingBean {
        void afterPropertiesSet();
    }

    interface DisposableBean {
        void destroy();
    }

    static class UserService implements InitializingBean, DisposableBean {
        void hello() {
            System.out.println("hello from UserService");
        }

        @Override
        public void afterPropertiesSet() {
            System.out.println("init: afterPropertiesSet");
        }

        @Override
        public void destroy() {
            System.out.println("destroy: DisposableBean.destroy");
        }
    }
}
