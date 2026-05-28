# Serena MCP 工具参考

Serena 提供的 MCP 工具详细参数说明。

## 符号查找工具

### find_symbol

查找符号定义位置。

```
参数：
- symbol_name (string): 符号名称
- file_path (string, 可选): 限定搜索范围的文件路径

返回：
- 符号定义的文件路径和行号
- 符号类型（class, function, variable 等）
```

### find_referencing_symbols

查找引用指定符号的所有位置。

```
参数：
- symbol_name (string): 被引用的符号名称
- file_path (string, 可选): 符号所在文件

返回：
- 所有引用位置列表
- 每个引用的上下文信息
```

### get_symbol_definition

获取符号的完整定义内容。

```
参数：
- symbol_name (string): 符号名称
- file_path (string): 符号所在文件

返回：
- 符号的完整源代码定义
- 包含签名、文档注释等
```

### list_symbols_in_file

列出文件中的所有符号。

```
参数：
- file_path (string): 文件路径

返回：
- 文件中所有符号列表
- 每个符号的类型和位置
```

## 代码导航工具

### get_hover_info

获取符号的悬停信息（类型、文档等）。

```
参数：
- file_path (string): 文件路径
- line (integer): 行号
- character (integer): 列号

返回：
- 类型信息
- 文档字符串
```

### go_to_definition

跳转到符号定义。

```
参数：
- file_path (string): 当前文件路径
- line (integer): 行号
- character (integer): 列号

返回：
- 定义位置的文件路径和行号
```

## 使用示例

### 查找类定义

```
工具: find_symbol
参数: { "symbol_name": "UserService" }
```

### 查找方法引用

```
工具: find_referencing_symbols
参数: { "symbol_name": "authenticate", "file_path": "src/auth/service.py" }
```

### 获取完整定义

```
工具: get_symbol_definition
参数: { "symbol_name": "DatabaseConfig", "file_path": "src/config.py" }
```
