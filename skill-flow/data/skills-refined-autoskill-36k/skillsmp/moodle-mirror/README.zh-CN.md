<div align="center">
  <h1>Moodle Mirror Skill</h1>
  <p><a href="README.zh-CN.md">中文</a> | <a href="README.md">English</a></p>
</div>

这个仓库包含一个可复用的 skill 包，用于把需要登录的 Moodle 课程/模块页面镜像到本地文件夹（例如 Obsidian vault），并支持离线检索。

### 能做什么

- 将 Moodle 页面落盘为 `MD` + `TXT` + `meta.json`（按 URL 映射为稳定的本地路径，便于重复运行补抓/修错）。
- 下载常见附件（PDF/DOCX/PPTX/ZIP 等）到 `_attachments/`。
- 处理 Moodle 常见坑：
  - SSO（微软登录）跳转
  - Cloudflare 验证页（需要手动完成，脚本会按超时等待）
  - `mod/resource` 资源触发下载（使用浏览器下载兜底）
  - `mod/url` 外链跳转导致外站 502（用 `forceview=1` 镜像 Moodle 自己的“外链包装页”）

### 关于 MCP（重要澄清）

这个 skill **不依赖**任何 MCP server（例如 Playwright MCP / Chrome DevTools MCP）。
核心依赖是：

- **Python Playwright**（负责抓取/下载/写文件）
- **Chrome + CDP**（可选，用于复用真实登录态，减少反爬/SSO摩擦）

如果你本机已经配置了浏览器类 MCP，它可以用于辅助登录/排障，但不是本 skill 的必需依赖。

### 环境要求

- Python 3.x
- Google Chrome
- 安装 Playwright（Python）与浏览器：

```powershell
pip install playwright
python -m playwright install
```

可选（推荐）：用独立 profile 启动带 CDP 的 Chrome：

```powershell
.\scripts\start_chrome_cdp.ps1
```

运行前自检（推荐）：

```powershell
python .\scripts\check_prereqs.py
```

### 使用方式

CDP 模式（推荐，反爬/SSO 更友好）：

```powershell
python .\scripts\moodle_mirror.py `
  --cdp-url http://127.0.0.1:9222 `
  --start-url "https://moodle.example.edu/course/view.php?id=123" `
  --out-dir "D:\Obsidian\My Course\Moodle Mirror" `
  --format md --rewrite-links `
  --allow-prefix https://moodle.example.edu/course/ `
  --allow-prefix https://moodle.example.edu/mod/ `
  --allow-prefix https://moodle.example.edu/pluginfile.php/ `
  --max-pages 200 --max-downloads 300 `
  --block-wait-seconds 180
```

Persistent profile 模式（如果 CDP 下载不稳定，用这个）：

```powershell
python .\scripts\moodle_mirror.py `
  --persistent --headful --channel chrome `
  --start-url "https://moodle.example.edu/course/view.php?id=123" `
  --out-dir "D:\Obsidian\My Course\Moodle Mirror" `
  --format md --rewrite-links `
  --allow-prefix https://moodle.example.edu/course/ `
  --allow-prefix https://moodle.example.edu/mod/ `
  --allow-prefix https://moodle.example.edu/pluginfile.php/ `
  --max-pages 200 --max-downloads 300 `
  --block-wait-seconds 180
```

生成状态报告（方便确认是否还有 error/blocked）：

```powershell
python .\scripts\mirror_status.py `
  --index "D:\Obsidian\My Course\Moodle Mirror\_index.jsonl" `
  --out   "D:\Obsidian\My Course\Moodle Mirror\_status.md"
```

### 自动点击账号（辅助 SSO）

如果微软登录页出现“选择账号”的头像卡片（你已在 Chrome 里保存过账号），可以开启自动点击：

```powershell
python .\scripts\moodle_mirror.py --auto-login --auto-login-account "your.name@ucl.ac.uk" ...
```

注意：这不会绕过 MFA，也不会自动输入密码；短信/Authenticator 等仍需要你手动确认。

### 关于“覆盖”

重复运行时，同一个 URL 对应的本地页面文件会在“该 URL 被重新保存”时覆盖。这样做是为了避免你补抓/修错时生成一堆重复文件。

更推荐的“增量更新”用法：

- 用 `--resume` 跳过已保存的 URL。
- 用 `--update-on-change`：当脚本为了“发现新链接”而回访起始页（通常是课程主页）时，只有内容变化才会覆盖本地文件。
- 在 Moodle 上，`--polite-delay-ms 0`、`--networkidle-wait-ms 0` 通常没问题，而且会明显更快。

如果你确实需要历史版本，最简单做法是每次把 `--out-dir` 换成一个带日期的新目录。

### 作为 Codex skill 安装（可选）

把整个目录放进你的 Codex skills 目录即可（或用你已有的安装流程）：

- Windows：`C:\Users\<你>\.codex\skills\moodle-mirror`

Skill 的元信息在 `SKILL.md`。

