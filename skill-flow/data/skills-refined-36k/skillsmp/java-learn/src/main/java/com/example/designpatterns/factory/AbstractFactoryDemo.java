package com.example.designpatterns.factory;

/**
 * 抽象工厂模式示例
 * 
 * 场景：跨平台 UI 组件工厂，支持 Windows 和 Mac 两种风格
 * 
 * 特点：
 * 1. 提供一个创建一系列相关对象的接口
 * 2. 无需指定具体类
 * 3. 保证产品族的一致性
 * 
 * 产品族 vs 产品等级结构：
 * - 产品族：同一个工厂生产的一组产品（如 Windows 风格的按钮、输入框、复选框）
 * - 产品等级结构：同一类产品的不同实现（如 Windows 按钮、Mac 按钮）
 * 
 * @author java_learn
 */
public class AbstractFactoryDemo {
    
    // ==================== 产品接口 ====================
    
    /**
     * 按钮接口
     */
    public interface Button {
        void render();
        void onClick();
    }
    
    /**
     * 输入框接口
     */
    public interface TextField {
        void render();
        void setValue(String value);
        String getValue();
    }
    
    /**
     * 复选框接口
     */
    public interface Checkbox {
        void render();
        void setChecked(boolean checked);
        boolean isChecked();
    }
    
    // ==================== Windows 产品族 ====================
    
    public static class WindowsButton implements Button {
        @Override
        public void render() {
            System.out.println("[Windows Button] 渲染 Windows 风格按钮");
        }
        
        @Override
        public void onClick() {
            System.out.println("[Windows Button] 按钮被点击");
        }
    }
    
    public static class WindowsTextField implements TextField {
        private String value = "";
        
        @Override
        public void render() {
            System.out.println("[Windows TextField] 渲染 Windows 风格输入框");
        }
        
        @Override
        public void setValue(String value) {
            this.value = value;
            System.out.println("[Windows TextField] 设置值: " + value);
        }
        
        @Override
        public String getValue() {
            return value;
        }
    }
    
    public static class WindowsCheckbox implements Checkbox {
        private boolean checked = false;
        
        @Override
        public void render() {
            System.out.println("[Windows Checkbox] 渲染 Windows 风格复选框");
        }
        
        @Override
        public void setChecked(boolean checked) {
            this.checked = checked;
            System.out.println("[Windows Checkbox] 设置选中状态: " + checked);
        }
        
        @Override
        public boolean isChecked() {
            return checked;
        }
    }
    
    // ==================== Mac 产品族 ====================
    
    public static class MacButton implements Button {
        @Override
        public void render() {
            System.out.println("[Mac Button] 渲染 Mac 风格按钮（圆角）");
        }
        
        @Override
        public void onClick() {
            System.out.println("[Mac Button] 按钮被点击");
        }
    }
    
    public static class MacTextField implements TextField {
        private String value = "";
        
        @Override
        public void render() {
            System.out.println("[Mac TextField] 渲染 Mac 风格输入框（简约）");
        }
        
        @Override
        public void setValue(String value) {
            this.value = value;
            System.out.println("[Mac TextField] 设置值: " + value);
        }
        
        @Override
        public String getValue() {
            return value;
        }
    }
    
    public static class MacCheckbox implements Checkbox {
        private boolean checked = false;
        
        @Override
        public void render() {
            System.out.println("[Mac Checkbox] 渲染 Mac 风格复选框（开关样式）");
        }
        
        @Override
        public void setChecked(boolean checked) {
            this.checked = checked;
            System.out.println("[Mac Checkbox] 设置选中状态: " + checked);
        }
        
        @Override
        public boolean isChecked() {
            return checked;
        }
    }
    
    // ==================== 抽象工厂 ====================
    
    /**
     * UI 工厂接口 - 定义创建一系列 UI 组件的方法
     */
    public interface UIFactory {
        Button createButton();
        TextField createTextField();
        Checkbox createCheckbox();
    }
    
    // ==================== 具体工厂 ====================
    
    /**
     * Windows UI 工厂 - 创建 Windows 风格的组件
     */
    public static class WindowsUIFactory implements UIFactory {
        @Override
        public Button createButton() {
            return new WindowsButton();
        }
        
        @Override
        public TextField createTextField() {
            return new WindowsTextField();
        }
        
        @Override
        public Checkbox createCheckbox() {
            return new WindowsCheckbox();
        }
    }
    
    /**
     * Mac UI 工厂 - 创建 Mac 风格的组件
     */
    public static class MacUIFactory implements UIFactory {
        @Override
        public Button createButton() {
            return new MacButton();
        }
        
        @Override
        public TextField createTextField() {
            return new MacTextField();
        }
        
        @Override
        public Checkbox createCheckbox() {
            return new MacCheckbox();
        }
    }
    
    // ==================== 客户端代码 ====================
    
    /**
     * 登录表单 - 使用抽象工厂创建 UI 组件
     */
    public static class LoginForm {
        private Button loginButton;
        private TextField usernameField;
        private TextField passwordField;
        private Checkbox rememberCheckbox;
        
        public LoginForm(UIFactory factory) {
            this.loginButton = factory.createButton();
            this.usernameField = factory.createTextField();
            this.passwordField = factory.createTextField();
            this.rememberCheckbox = factory.createCheckbox();
        }
        
        public void render() {
            System.out.println("渲染登录表单：");
            usernameField.render();
            passwordField.render();
            rememberCheckbox.render();
            loginButton.render();
        }
        
        public void simulateLogin() {
            usernameField.setValue("admin");
            passwordField.setValue("******");
            rememberCheckbox.setChecked(true);
            loginButton.onClick();
        }
    }
    
    // ==================== 测试 ====================
    
    public static void main(String[] args) {
        System.out.println("=== 抽象工厂模式示例 ===\n");
        
        // 模拟根据操作系统选择工厂
        String os = "windows"; // 可以改为 "mac"
        
        UIFactory factory;
        if (os.equalsIgnoreCase("windows")) {
            factory = new WindowsUIFactory();
            System.out.println("当前操作系统: Windows\n");
        } else {
            factory = new MacUIFactory();
            System.out.println("当前操作系统: Mac\n");
        }
        
        // 创建登录表单
        LoginForm loginForm = new LoginForm(factory);
        loginForm.render();
        
        System.out.println();
        System.out.println("模拟登录操作：");
        loginForm.simulateLogin();
        
        System.out.println("\n" + "=".repeat(50) + "\n");
        
        // 切换到 Mac 风格
        System.out.println("切换到 Mac 风格:\n");
        factory = new MacUIFactory();
        LoginForm macLoginForm = new LoginForm(factory);
        macLoginForm.render();
    }
}
