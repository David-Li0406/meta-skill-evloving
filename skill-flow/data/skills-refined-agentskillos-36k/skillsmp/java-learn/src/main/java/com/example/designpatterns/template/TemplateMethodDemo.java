package com.example.designpatterns.template;

/**
 * 模板方法模式示例
 * 
 * 场景：数据导出功能，支持 CSV、Excel、PDF 等格式
 * 
 * 模板方法模式定义一个操作中的算法骨架，将某些步骤延迟到子类中实现。
 * 使得子类可以不改变算法结构的情况下，重定义算法的某些特定步骤。
 * 
 * 特点：
 * 1. 父类定义算法骨架（模板方法）
 * 2. 子类实现具体步骤（抽象方法）
 * 3. 可选的钩子方法
 * 4. 好莱坞原则：Don't call us, we'll call you
 * 
 * @author java_learn
 */
public class TemplateMethodDemo {
    
    // ==================== 抽象模板类 ====================
    
    /**
     * 数据导出器 - 抽象模板类
     */
    public static abstract class DataExporter {
        
        /**
         * 模板方法 - 定义导出算法骨架
         * 使用 final 防止子类修改算法结构
         */
        public final void export(String data) {
            System.out.println("\n" + "=".repeat(50));
            System.out.println("开始数据导出...");
            
            // 1. 打开输出流
            openOutput();
            
            // 2. 钩子方法 - 是否需要添加头部
            if (needHeader()) {
                writeHeader();
            }
            
            // 3. 写入数据
            writeData(data);
            
            // 4. 钩子方法 - 是否需要添加尾部
            if (needFooter()) {
                writeFooter();
            }
            
            // 5. 关闭输出流
            closeOutput();
            
            // 6. 钩子方法 - 导出后处理
            afterExport();
            
            System.out.println("数据导出完成！");
            System.out.println("=".repeat(50));
        }
        
        // ==================== 抽象方法（必须由子类实现）====================
        
        /**
         * 打开输出流
         */
        protected abstract void openOutput();
        
        /**
         * 写入数据
         */
        protected abstract void writeData(String data);
        
        /**
         * 关闭输出流
         */
        protected abstract void closeOutput();
        
        /**
         * 获取导出格式名称
         */
        protected abstract String getFormatName();
        
        // ==================== 钩子方法（可选覆盖）====================
        
        /**
         * 是否需要写入头部
         */
        protected boolean needHeader() {
            return true;
        }
        
        /**
         * 写入头部
         */
        protected void writeHeader() {
            System.out.println("[" + getFormatName() + "] 写入默认头部");
        }
        
        /**
         * 是否需要写入尾部
         */
        protected boolean needFooter() {
            return false;
        }
        
        /**
         * 写入尾部
         */
        protected void writeFooter() {
            System.out.println("[" + getFormatName() + "] 写入默认尾部");
        }
        
        /**
         * 导出后处理
         */
        protected void afterExport() {
            // 默认不做任何事，子类可覆盖
        }
    }
    
    // ==================== 具体实现类 ====================
    
    /**
     * CSV 导出器
     */
    public static class CsvExporter extends DataExporter {
        private String fileName;
        
        public CsvExporter(String fileName) {
            this.fileName = fileName;
        }
        
        @Override
        protected void openOutput() {
            System.out.println("[CSV] 创建文件: " + fileName + ".csv");
        }
        
        @Override
        protected void writeData(String data) {
            // 模拟将数据转换为 CSV 格式
            String[] rows = data.split(";");
            for (String row : rows) {
                System.out.println("[CSV] 写入行: " + row.replace(":", ","));
            }
        }
        
        @Override
        protected void closeOutput() {
            System.out.println("[CSV] 关闭文件流");
        }
        
        @Override
        protected String getFormatName() {
            return "CSV";
        }
        
        @Override
        protected void writeHeader() {
            System.out.println("[CSV] 写入 CSV 头部: id,name,email");
        }
    }
    
    /**
     * Excel 导出器
     */
    public static class ExcelExporter extends DataExporter {
        private String fileName;
        private String sheetName;
        
        public ExcelExporter(String fileName, String sheetName) {
            this.fileName = fileName;
            this.sheetName = sheetName;
        }
        
        @Override
        protected void openOutput() {
            System.out.println("[Excel] 创建工作簿: " + fileName + ".xlsx");
            System.out.println("[Excel] 创建工作表: " + sheetName);
        }
        
        @Override
        protected void writeData(String data) {
            String[] rows = data.split(";");
            int rowNum = 1;
            for (String row : rows) {
                System.out.println("[Excel] 第 " + rowNum + " 行: " + row);
                rowNum++;
            }
        }
        
        @Override
        protected void closeOutput() {
            System.out.println("[Excel] 保存并关闭工作簿");
        }
        
        @Override
        protected String getFormatName() {
            return "Excel";
        }
        
        @Override
        protected void writeHeader() {
            System.out.println("[Excel] 写入表头行，设置加粗样式");
        }
        
        @Override
        protected boolean needFooter() {
            return true; // Excel 需要尾部
        }
        
        @Override
        protected void writeFooter() {
            System.out.println("[Excel] 写入合计行");
        }
        
        @Override
        protected void afterExport() {
            System.out.println("[Excel] 自动调整列宽");
        }
    }
    
    /**
     * PDF 导出器
     */
    public static class PdfExporter extends DataExporter {
        private String fileName;
        private String title;
        
        public PdfExporter(String fileName, String title) {
            this.fileName = fileName;
            this.title = title;
        }
        
        @Override
        protected void openOutput() {
            System.out.println("[PDF] 创建 PDF 文档: " + fileName + ".pdf");
            System.out.println("[PDF] 设置页面大小: A4");
        }
        
        @Override
        protected void writeData(String data) {
            System.out.println("[PDF] 创建数据表格");
            String[] rows = data.split(";");
            for (String row : rows) {
                System.out.println("[PDF] 表格行: " + row);
            }
        }
        
        @Override
        protected void closeOutput() {
            System.out.println("[PDF] 保存 PDF 文档");
        }
        
        @Override
        protected String getFormatName() {
            return "PDF";
        }
        
        @Override
        protected void writeHeader() {
            System.out.println("[PDF] 写入标题: " + title);
            System.out.println("[PDF] 写入生成时间");
        }
        
        @Override
        protected boolean needFooter() {
            return true;
        }
        
        @Override
        protected void writeFooter() {
            System.out.println("[PDF] 写入页脚: 第 1 页 / 共 1 页");
        }
        
        @Override
        protected void afterExport() {
            System.out.println("[PDF] 添加水印");
        }
    }
    
    /**
     * JSON 导出器（不需要头部和尾部）
     */
    public static class JsonExporter extends DataExporter {
        
        @Override
        protected void openOutput() {
            System.out.println("[JSON] 开始构建 JSON");
        }
        
        @Override
        protected void writeData(String data) {
            System.out.println("[JSON] {");
            System.out.println("[JSON]   \"data\": [");
            String[] rows = data.split(";");
            for (int i = 0; i < rows.length; i++) {
                String comma = (i < rows.length - 1) ? "," : "";
                System.out.println("[JSON]     " + formatToJson(rows[i]) + comma);
            }
            System.out.println("[JSON]   ]");
            System.out.println("[JSON] }");
        }
        
        private String formatToJson(String row) {
            String[] parts = row.split(":");
            if (parts.length == 2) {
                return "{\"key\": \"" + parts[0].trim() + "\", \"value\": \"" + parts[1].trim() + "\"}";
            }
            return "{\"value\": \"" + row + "\"}";
        }
        
        @Override
        protected void closeOutput() {
            System.out.println("[JSON] JSON 构建完成");
        }
        
        @Override
        protected String getFormatName() {
            return "JSON";
        }
        
        // JSON 不需要头部
        @Override
        protected boolean needHeader() {
            return false;
        }
    }
    
    // ==================== 测试 ====================
    
    public static void main(String[] args) {
        System.out.println("=== 模板方法模式示例 - 数据导出 ===");
        
        // 测试数据
        String data = "1:Alice:alice@example.com;2:Bob:bob@example.com;3:Charlie:charlie@example.com";
        
        // CSV 导出
        DataExporter csvExporter = new CsvExporter("users");
        csvExporter.export(data);
        
        // Excel 导出
        DataExporter excelExporter = new ExcelExporter("users", "用户列表");
        excelExporter.export(data);
        
        // PDF 导出
        DataExporter pdfExporter = new PdfExporter("users", "用户数据报表");
        pdfExporter.export(data);
        
        // JSON 导出（不需要头尾）
        DataExporter jsonExporter = new JsonExporter();
        jsonExporter.export(data);
    }
}
