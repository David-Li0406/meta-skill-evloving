---
<%*
const today = tp.date.now("YYYY-MM-DD");
const momentDate = window.moment(today, "YYYY-MM-DD", true);
const titleName = `周报_${momentDate.format("YYMMDD")}`;
const createTime = tp.file.creation_date("YYYY-MM-Do HH:mm:ss dddd");
const modificationDate = tp.file.last_modified_date("YYYY-MM-Do HH:mm:ss dddd");
-%>
标题: <% titleName %>
tags:
  - 日志/周报
创建时间:  <% createTime %>
编辑时间:  <% modificationDate %>
---

<!-- markdownlint-disable MD024 -->



<%*
// --- 文件自动处理函数 ---

/**
 * 创建文件夹并移动当前文件
 */
async function setupFile() {
    // 重新获取日期信息，确保作用域安全
    const datePart = tp.date.now("YYMMDD");
    const titleName = `周报_${datePart}`;
    const year = tp.date.now("YYYY");
    const month = tp.date.now("MM");
    const destDir = `/04_自我管理/00_日志/${year}/${month}`;
    let finalPath = `${destDir}/${titleName}`;

    // 确保 Templater 已经创建了文件
    // 这是 Templater 的一个特性，需要等待文件实际写入磁盘
    const file = tp.file.find_tfile(tp.file.path(true));
    if (!file) {
      console.error("Templater 文件尚未创建，无法移动。");
      new Notice("错误：Templater 文件尚未创建，请重试。", 5000);
      return;
    }
    
    // 检查目标文件夹是否存在，不存在则创建
    if (!await tp.file.exists(destDir)) {
      await app.vault.createFolder(destDir);
    }

    // 安全性检查：如果目标文件已存在，则在文件名后附加时间戳
    if (await tp.file.exists(finalPath)) {
        const timestamp = tp.date.now("_HHmmss");
        finalPath = `${destDir}/${titleName}${timestamp}`;
        new Notice(`文件已存在，已重命名为：${titleName}${timestamp}.md`);
    }

    // 移动文件到目标文件夹
    await tp.file.move(finalPath);

    // 将光标定位到"今日目标"下方
    // 注意：cursor() 必须在文件移动后调用，因为它作用于"当前"文件
    tp.file.cursor(1); 
}

// --- 执行文件处理 ---
await setupFile();
-%>
