# Work Memo 安装指南

## 快速开始

1. **复制文件到插件目录**
   ```bash
   cp -r work-memo ~/.claude/plugins/
   ```

2. **或使用符号链接**
   ```bash
   ln -s /path/to/work-memo ~/.claude/plugins/work-memo
   ```

3. **验证安装**
   ```bash
   ~/.claude/plugins/work-memo/memo help
   ```

## 使用方法

```bash
# 记录工作事项
/memo 紧急会议明天 #work @office

# 查看今日记录
python3 skills/scripts/cli.py report --daily

# 搜索记录
python3 skills/scripts/cli.py search "紧急"
```

## 依赖

- Python 3.9+
- TinyDB: `pip install tinydb`
- Requests: `pip install requests`
- BeautifulSoup4: `pip install beautifulsoup4`

## 网页抓取功能

如果需要使用 `/memo` 命令的URL功能（抓取并总结网页内容），需要安装额外的依赖：

```bash
pip install requests beautifulsoup4
```

## 数据存储

- 位置: `~/.workmemo/db.json`
- 格式: JSON

## 更多信息

参见 README.md 和 SKILL.md
