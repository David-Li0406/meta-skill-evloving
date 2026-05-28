# troubleshooting.md

## 1) Windows 路径问题
- 建议：所有关键路径用绝对路径
- JSON 里写 Windows 路径时会出现 `\\`，这是 JSON 的转义行为，正常。

## 2) modify_boundary 找不到列
- 先用记事本/Excel 打开 Boundary.csv 查看表头
- 列名必须完全一致（包含冒号、大小写）

## 3) 按时间修改失败
- Boundary.csv 必须有 TIME 列（列名通常就是 TIME）
- 时间格式建议：`YYYY/M/D H:MM` 或 `YYYY-M-D H:MM`

## 4) diff_boundary 找不到“最新备份”
- modify_boundary 会在同目录生成：`Boundary.csv.before_YYYYMMDD_HHMMSS.csv`
- diff_boundary 默认会搜索这个模式；如果你手动移动了文件，可以用 `--before-file` 显式指定
