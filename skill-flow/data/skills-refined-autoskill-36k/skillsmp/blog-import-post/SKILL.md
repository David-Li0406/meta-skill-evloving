---
name: blog-import-post
description: Import existing Markdown files into the Hugo blog with smart metadata handling and automatic image processing
---

# Blog Import Post Skill

Import existing Markdown files into the Hugo blog with intelligent handling of front matter, images, and optional publishing.

## What I do

- Import Markdown files into the blog's `content/posts/` directory
- Intelligently handle front matter:
  - If present and complete → preserve it, update author to "wzh001create"
  - If missing or incomplete → prompt user for title, tags, and categories
- Automatically copy and fix image references:
  - Detect images in the same directory as the markdown file
  - Copy them to `static/images/<article-name>/`
  - Update image paths in the article to use `/images/<article-name>/...`
- Optionally publish immediately to GitHub

## When to use me

Use this skill when the user wants to:
- Add an existing Markdown file to the blog
- Import articles written elsewhere (in their Documents folder, Downloads, etc.)
- Migrate content from other sources or blogging platforms
- Share a markdown file they've prepared

## Trigger phrases (examples)

- "导入文章 ~/Documents/kubernetes-guide.md"
- "帮我把这篇文章添加到博客 /path/to/my-article.md"
- "import this markdown file to my blog ~/article.md"
- "把 /home/user/blog-post.md 发布到博客"
- "添加文章到博客"

## How I work

### Step 1: Validate the file path

- Check if the user provided a markdown file path
- If not provided, ask: "请提供要导入的 Markdown 文件路径"
- Verify the file exists and has `.md` or `.markdown` extension
- If file doesn't exist, show error and exit

### Step 2: Check for front matter

Use the Read tool to examine the markdown file:

```bash
# Check first few lines of the file
head -20 <file-path>
```

- If the file starts with `---` on line 1 and has another `---` within the first 20 lines:
  - Front matter exists
  - Extract title, tags, categories if present
  - Decide: **preserve mode** (use `--keep-frontmatter` flag)
  
- If no front matter detected:
  - Decide: **prompt mode** (no flag, script will ask for metadata)

### Step 3: Prepare for import

Determine the target article name:
- If front matter exists, extract title and convert to filename
- Otherwise, use the original filename (without extension)

### Step 4: Run the import script

Call the import-post.sh script with appropriate flags:

**Preserve mode (has front matter):**
```bash
cd ~/wzh_blog/my-blog/scripts
./import-post.sh "<source-file-path>" --keep-frontmatter
```

**Prompt mode (no front matter):**
```bash
cd ~/wzh_blog/my-blog/scripts
./import-post.sh "<source-file-path>"
```

The script will:
- Copy the markdown file to `content/posts/`
- Handle front matter appropriately
- Prompt for image handling (answer 'y' to copy images)
- Ask about updating image paths (answer 'y' to update)

### Step 5: Verify import success

After running the script:
- Check if the file exists in `content/posts/`
- Use the Read tool to verify the front matter is correct
- List any images that were copied

### Step 6: Ask about publishing

Present the user with a clear choice:

```
✓ 文章已成功导入！

📄 文件位置: content/posts/<article-name>.md
🖼️  图片目录: static/images/<article-name>/ (如果有图片)

📤 是否立即发布到 GitHub？
   - 输入 'y' 或 'yes' → 立即提交并推送
   - 输入 'n' 或 'no'  → 稍后手动发布
   
你的选择: 
```

### Step 7: Handle publishing choice

**If user says yes:**

```bash
cd ~/wzh_blog/my-blog
git add -A
git commit -m "feat: 添加文章《<article-title>》"
git push
```

Then show:
```
✓ 已提交更改
✓ 已推送到 GitHub
🚀 GitHub Actions 正在部署...

你的文章将在几分钟内上线：
https://wzh001create.github.io/posts/<article-slug>/
```

**If user says no:**

```
✓ 文章已导入到本地

需要发布时，请运行：
  cd ~/wzh_blog/my-blog/scripts
  ./publish.sh

或者手动执行：
  cd ~/wzh_blog/my-blog
  git add -A
  git commit -m "feat: 添加文章《<article-title>》"
  git push
```

## Important paths and files

- **Blog root directory**: `~/wzh_blog/my-blog/`
- **Import script**: `~/wzh_blog/my-blog/scripts/import-post.sh`
- **Posts directory**: `~/wzh_blog/my-blog/content/posts/`
- **Images directory**: `~/wzh_blog/my-blog/static/images/`
- **Author name**: `wzh001create` (always use this)

## Script behavior reference

The `import-post.sh` script:
- **With `--keep-frontmatter`**: Preserves original front matter, updates author field
- **Without flag**: Prompts for title, tags, categories interactively
- **Image handling**: Asks whether to copy images from source directory
- **Path fixing**: Asks whether to update image paths in the markdown

## Error handling

- **File not found**: Show clear error message with the path that was checked
- **Not a markdown file**: Remind user to provide .md or .markdown files
- **Script fails**: Show the error output and suggest checking file permissions
- **Git push fails**: Show error and suggest checking network/authentication

## Important notes

- Always use the Bash tool to run commands, not try to simulate them
- Use the Read tool to examine file contents when needed
- Preserve Chinese characters in filenames (the import script supports this)
- Always work from the correct directory when running scripts
- After git push, remind user that GitHub Actions will deploy automatically (takes a few minutes)

## Example interaction

**User input:**
```
导入文章 ~/Documents/kubernetes-入门教程.md
```

**Your response:**
```
正在导入文章...

✓ 找到文件: ~/Documents/kubernetes-入门教程.md
✓ 检测到完整的 front matter，保留原有元数据
  - 标题: Kubernetes 入门教程
  - 标签: Kubernetes, Docker, 云原生
  - 分类: 容器技术

正在运行导入脚本...
[show script output]

✓ 发现 3 张图片，已复制到 static/images/kubernetes-入门教程/
✓ 已更新图片路径引用
✓ 文章已导入到 content/posts/kubernetes-入门教程.md

📤 是否立即发布到 GitHub？(y/N): 
```

## Tools you should use

- **Bash**: To run the import script and git commands
- **Read**: To check file contents and front matter
- **Glob**: To list files if needed (though usually not necessary)
- **Question**: To ask user for publishing confirmation (if the user's response is unclear)

Remember: Be conversational and helpful. Guide the user through the process with clear status messages.
