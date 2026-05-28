package com.example.designpatterns.factory;

/**
 * 工厂方法模式示例
 * 
 * 场景：日志记录器工厂，支持多种日志输出方式
 * 
 * 特点：
 * 1. 定义一个创建产品的接口，由子类决定实例化哪个类
 * 2. 符合开闭原则：新增产品只需添加新的工厂类
 * 3. 每个具体产品对应一个具体工厂
 * 
 * @author java_learn
 */
public class FactoryMethodDemo {
    
    // ==================== 产品接口 ====================
    
    /**
     * 日志记录器接口
     */
    public interface Logger {
        void log(String message);
        void log(String level, String message);
    }
    
    // ==================== 具体产品 ====================
    
    /**
     * 文件日志记录器
     */
    public static class FileLogger implements Logger {
        private String filePath;
        
        public FileLogger(String filePath) {
            this.filePath = filePath;
            System.out.println("[FileLogger] 初始化，日志文件: " + filePath);
        }
        
        @Override
        public void log(String message) {
            log("INFO", message);
        }
        
        @Override
        public void log(String level, String message) {
            System.out.println("[FileLogger][" + level + "] " + message + " -> 写入到 " + filePath);
        }
    }
    
    /**
     * 控制台日志记录器
     */
    public static class ConsoleLogger implements Logger {
        public ConsoleLogger() {
            System.out.println("[ConsoleLogger] 初始化");
        }
        
        @Override
        public void log(String message) {
            log("INFO", message);
        }
        
        @Override
        public void log(String level, String message) {
            System.out.println("[ConsoleLogger][" + level + "] " + message);
        }
    }
    
    /**
     * 数据库日志记录器
     */
    public static class DatabaseLogger implements Logger {
        private String connectionString;
        
        public DatabaseLogger(String connectionString) {
            this.connectionString = connectionString;
            System.out.println("[DatabaseLogger] 初始化，连接: " + connectionString);
        }
        
        @Override
        public void log(String message) {
            log("INFO", message);
        }
        
        @Override
        public void log(String level, String message) {
            System.out.println("[DatabaseLogger][" + level + "] " + message + " -> 存储到数据库");
        }
    }
    
    // ==================== 工厂接口 ====================
    
    /**
     * 日志工厂接口 - 定义创建日志记录器的方法
     */
    public interface LoggerFactory {
        Logger createLogger();
    }
    
    // ==================== 具体工厂 ====================
    
    /**
     * 文件日志工厂
     */
    public static class FileLoggerFactory implements LoggerFactory {
        private String filePath;
        
        public FileLoggerFactory(String filePath) {
            this.filePath = filePath;
        }
        
        @Override
        public Logger createLogger() {
            return new FileLogger(filePath);
        }
    }
    
    /**
     * 控制台日志工厂
     */
    public static class ConsoleLoggerFactory implements LoggerFactory {
        @Override
        public Logger createLogger() {
            return new ConsoleLogger();
        }
    }
    
    /**
     * 数据库日志工厂
     */
    public static class DatabaseLoggerFactory implements LoggerFactory {
        private String connectionString;
        
        public DatabaseLoggerFactory(String connectionString) {
            this.connectionString = connectionString;
        }
        
        @Override
        public Logger createLogger() {
            return new DatabaseLogger(connectionString);
        }
    }
    
    // ==================== 客户端代码 ====================
    
    /**
     * 应用程序 - 使用工厂创建日志记录器
     */
    public static class Application {
        private Logger logger;
        
        public Application(LoggerFactory factory) {
            this.logger = factory.createLogger();
        }
        
        public void run() {
            logger.log("应用程序启动");
            logger.log("DEBUG", "正在处理业务逻辑...");
            logger.log("INFO", "业务处理完成");
        }
    }
    
    // ==================== 测试 ====================
    
    public static void main(String[] args) {
        System.out.println("=== 工厂方法模式示例 ===\n");
        
        // 使用文件日志工厂
        System.out.println("--- 使用文件日志工厂 ---");
        LoggerFactory fileFactory = new FileLoggerFactory("/var/log/app.log");
        Application app1 = new Application(fileFactory);
        app1.run();
        
        System.out.println();
        
        // 使用控制台日志工厂
        System.out.println("--- 使用控制台日志工厂 ---");
        LoggerFactory consoleFactory = new ConsoleLoggerFactory();
        Application app2 = new Application(consoleFactory);
        app2.run();
        
        System.out.println();
        
        // 使用数据库日志工厂
        System.out.println("--- 使用数据库日志工厂 ---");
        LoggerFactory dbFactory = new DatabaseLoggerFactory("jdbc:mysql://localhost:3306/logs");
        Application app3 = new Application(dbFactory);
        app3.run();
    }
}
