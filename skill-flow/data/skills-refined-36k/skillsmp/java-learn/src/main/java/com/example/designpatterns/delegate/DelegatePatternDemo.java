package com.example.designpatterns.delegate;

import java.util.HashMap;
import java.util.Map;

/**
 * 委派模式示例
 * 
 * 委派模式（Delegate Pattern）不属于 GoF 23 种设计模式，但在框架中广泛使用。
 * 它负责任务的调用和分配，类似于一个中介。
 * 
 * 委派模式 vs 代理模式：
 * - 代理模式：注重过程，控制对目标对象的访问
 * - 委派模式：注重结果，负责任务的分发和调度
 * 
 * 典型应用：
 * - Spring MVC 的 DispatcherServlet
 * - ClassLoader 的双亲委派机制
 * 
 * @author java_learn
 */
public class DelegatePatternDemo {
    
    // ==================== 场景1: 任务分发 ====================
    
    /**
     * 员工接口
     */
    public interface Employee {
        void doTask(String task);
        String getSkill();
    }
    
    /**
     * 程序员
     */
    public static class Programmer implements Employee {
        private String name;
        
        public Programmer(String name) {
            this.name = name;
        }
        
        @Override
        public void doTask(String task) {
            System.out.println("  [程序员 " + name + "] 正在编写代码: " + task);
        }
        
        @Override
        public String getSkill() {
            return "coding";
        }
    }
    
    /**
     * 设计师
     */
    public static class Designer implements Employee {
        private String name;
        
        public Designer(String name) {
            this.name = name;
        }
        
        @Override
        public void doTask(String task) {
            System.out.println("  [设计师 " + name + "] 正在设计: " + task);
        }
        
        @Override
        public String getSkill() {
            return "design";
        }
    }
    
    /**
     * 测试员
     */
    public static class Tester implements Employee {
        private String name;
        
        public Tester(String name) {
            this.name = name;
        }
        
        @Override
        public void doTask(String task) {
            System.out.println("  [测试员 " + name + "] 正在测试: " + task);
        }
        
        @Override
        public String getSkill() {
            return "testing";
        }
    }
    
    /**
     * 项目经理（委派者）
     * 
     * 项目经理不直接做事，而是根据任务类型分配给合适的员工
     * 这就是委派模式的核心思想
     */
    public static class ProjectManager implements Employee {
        private Map<String, Employee> employees = new HashMap<>();
        
        public void addEmployee(String taskType, Employee employee) {
            employees.put(taskType, employee);
        }
        
        @Override
        public void doTask(String task) {
            // 解析任务类型
            String taskType = parseTaskType(task);
            
            System.out.println("[项目经理] 收到任务: " + task);
            System.out.println("[项目经理] 任务类型: " + taskType);
            
            // 委派给合适的员工
            Employee employee = employees.get(taskType);
            if (employee != null) {
                System.out.println("[项目经理] 委派给: " + employee.getClass().getSimpleName());
                employee.doTask(task);
            } else {
                System.out.println("[项目经理] 没有找到合适的员工处理此任务！");
            }
        }
        
        private String parseTaskType(String task) {
            if (task.contains("开发") || task.contains("编码") || task.contains("代码")) {
                return "coding";
            } else if (task.contains("设计") || task.contains("UI") || task.contains("界面")) {
                return "design";
            } else if (task.contains("测试") || task.contains("QA") || task.contains("验证")) {
                return "testing";
            }
            return "unknown";
        }
        
        @Override
        public String getSkill() {
            return "management";
        }
    }
    
    // ==================== 场景2: 模拟 Spring MVC DispatcherServlet ====================
    
    /**
     * 控制器接口
     */
    public interface Controller {
        String handleRequest(String uri, Map<String, String> params);
    }
    
    /**
     * 用户控制器
     */
    public static class UserController implements Controller {
        @Override
        public String handleRequest(String uri, Map<String, String> params) {
            if (uri.endsWith("/list")) {
                return "返回用户列表";
            } else if (uri.endsWith("/get")) {
                return "返回用户: " + params.get("id");
            } else if (uri.endsWith("/add")) {
                return "添加用户: " + params.get("name");
            }
            return "用户操作完成";
        }
    }
    
    /**
     * 订单控制器
     */
    public static class OrderController implements Controller {
        @Override
        public String handleRequest(String uri, Map<String, String> params) {
            if (uri.endsWith("/list")) {
                return "返回订单列表";
            } else if (uri.endsWith("/create")) {
                return "创建订单: " + params.get("productId");
            }
            return "订单操作完成";
        }
    }
    
    /**
     * DispatcherServlet 模拟（委派者）
     * 
     * 这是 Spring MVC 的核心组件，负责将请求分发给对应的 Controller
     */
    public static class DispatcherServlet {
        private Map<String, Controller> handlerMapping = new HashMap<>();
        
        public DispatcherServlet() {
            // 初始化 URL 到 Controller 的映射
            handlerMapping.put("/user", new UserController());
            handlerMapping.put("/order", new OrderController());
        }
        
        public void doService(String uri, Map<String, String> params) {
            System.out.println("\n[DispatcherServlet] 收到请求: " + uri);
            
            // 1. 根据 URI 查找对应的 Controller
            Controller controller = findController(uri);
            
            if (controller == null) {
                System.out.println("[DispatcherServlet] 404 Not Found: " + uri);
                return;
            }
            
            // 2. 委派给 Controller 处理
            System.out.println("[DispatcherServlet] 委派给: " + controller.getClass().getSimpleName());
            String result = controller.handleRequest(uri, params);
            
            // 3. 返回结果
            System.out.println("[DispatcherServlet] 响应: " + result);
        }
        
        private Controller findController(String uri) {
            for (Map.Entry<String, Controller> entry : handlerMapping.entrySet()) {
                if (uri.startsWith(entry.getKey())) {
                    return entry.getValue();
                }
            }
            return null;
        }
    }
    
    // ==================== 场景3: ClassLoader 双亲委派 ====================
    
    /**
     * 模拟 ClassLoader 双亲委派机制
     */
    public static abstract class MyClassLoader {
        protected MyClassLoader parent;
        protected String name;
        
        public MyClassLoader(String name, MyClassLoader parent) {
            this.name = name;
            this.parent = parent;
        }
        
        /**
         * 加载类（双亲委派）
         */
        public String loadClass(String className) {
            System.out.println("[" + name + "] 尝试加载: " + className);
            
            // 1. 首先委派给父加载器
            if (parent != null) {
                String result = parent.loadClass(className);
                if (result != null) {
                    return result;
                }
            }
            
            // 2. 父加载器无法加载，自己尝试加载
            return findClass(className);
        }
        
        /**
         * 查找类（由子类实现）
         */
        protected abstract String findClass(String className);
    }
    
    /**
     * Bootstrap ClassLoader 模拟
     */
    public static class BootstrapClassLoader extends MyClassLoader {
        public BootstrapClassLoader() {
            super("Bootstrap ClassLoader", null);
        }
        
        @Override
        protected String findClass(String className) {
            // Bootstrap 只加载 java.lang 包
            if (className.startsWith("java.lang.")) {
                System.out.println("  [" + name + "] 加载成功: " + className);
                return className;
            }
            System.out.println("  [" + name + "] 无法加载: " + className);
            return null;
        }
    }
    
    /**
     * Extension ClassLoader 模拟
     */
    public static class ExtClassLoader extends MyClassLoader {
        public ExtClassLoader(MyClassLoader parent) {
            super("Extension ClassLoader", parent);
        }
        
        @Override
        protected String findClass(String className) {
            // Ext 加载 javax 包
            if (className.startsWith("javax.")) {
                System.out.println("  [" + name + "] 加载成功: " + className);
                return className;
            }
            System.out.println("  [" + name + "] 无法加载: " + className);
            return null;
        }
    }
    
    /**
     * Application ClassLoader 模拟
     */
    public static class AppClassLoader extends MyClassLoader {
        public AppClassLoader(MyClassLoader parent) {
            super("Application ClassLoader", parent);
        }
        
        @Override
        protected String findClass(String className) {
            // App 加载应用类
            if (className.startsWith("com.example.")) {
                System.out.println("  [" + name + "] 加载成功: " + className);
                return className;
            }
            System.out.println("  [" + name + "] 无法加载: " + className);
            return null;
        }
    }
    
    // ==================== 测试 ====================
    
    public static void main(String[] args) {
        System.out.println("=== 委派模式示例 ===\n");
        
        // ========== 场景1: 项目经理分配任务 ==========
        System.out.println("【场景1: 项目经理任务分配】");
        System.out.println("=".repeat(50));
        
        ProjectManager pm = new ProjectManager();
        pm.addEmployee("coding", new Programmer("张三"));
        pm.addEmployee("design", new Designer("李四"));
        pm.addEmployee("testing", new Tester("王五"));
        
        pm.doTask("开发用户登录功能");
        System.out.println();
        pm.doTask("设计首页 UI 界面");
        System.out.println();
        pm.doTask("测试支付功能");
        System.out.println();
        pm.doTask("写文档");  // 没有对应的员工
        
        // ========== 场景2: DispatcherServlet 请求分发 ==========
        System.out.println("\n\n【场景2: DispatcherServlet 请求分发】");
        System.out.println("=".repeat(50));
        
        DispatcherServlet servlet = new DispatcherServlet();
        
        Map<String, String> params1 = new HashMap<>();
        servlet.doService("/user/list", params1);
        
        Map<String, String> params2 = new HashMap<>();
        params2.put("id", "123");
        servlet.doService("/user/get", params2);
        
        Map<String, String> params3 = new HashMap<>();
        params3.put("productId", "P001");
        servlet.doService("/order/create", params3);
        
        servlet.doService("/product/list", new HashMap<>());  // 404
        
        // ========== 场景3: ClassLoader 双亲委派 ==========
        System.out.println("\n\n【场景3: ClassLoader 双亲委派】");
        System.out.println("=".repeat(50));
        
        MyClassLoader bootstrap = new BootstrapClassLoader();
        MyClassLoader ext = new ExtClassLoader(bootstrap);
        MyClassLoader app = new AppClassLoader(ext);
        
        System.out.println("\n加载 java.lang.String:");
        app.loadClass("java.lang.String");
        
        System.out.println("\n加载 javax.swing.JFrame:");
        app.loadClass("javax.swing.JFrame");
        
        System.out.println("\n加载 com.example.MyClass:");
        app.loadClass("com.example.MyClass");
        
        System.out.println("\n加载 org.apache.commons.Lang:");
        app.loadClass("org.apache.commons.Lang");  // 无法加载
    }
}
