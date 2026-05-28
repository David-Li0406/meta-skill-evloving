#!/usr/bin/env bun
/**
 * Xiaohongshu Publisher - 小红书发布脚本
 *
 * 结合 w0x7ce-xiaohongshu-publisher (Cookie 登录) 和 w0x7ce-post-to-rednote (发布功能)
 *
 * 用法:
 *   bun publish.ts --title "标题" --content "内容" --image photo1.png --image photo2.png
 *   bun publish.ts --title "标题" --content "内容" --images ./photos/ --submit
 */

import { mkdir } from "node:fs/promises";
import { existsSync, readFileSync, readdirSync } from "node:fs";
import path from "node:path";

// ==================== 配置 ====================

const WS_URL = process.env.XHS_WS_URL || "ws://hk2.w0x7ce.eu:10086?token=255=ff";
const STATE_FILE = process.env.XHS_STATE_FILE || "xhs_browser_state.json";
const SCREENSHOT_DIR = "screenshots_xhs";

// 创作者平台发布页面 (图文)
const PUBLISH_URL = "https://creator.xiaohongshu.com/publish/publish?from=tab_switch&target=image";

// 多语言选择器
const I18N_SELECTORS = {
  titleInput: [
    'input[placeholder*="填写标题"]',
    'input[placeholder*="添加标题"]',
    'input[placeholder*="Title"]',
    'textarea[placeholder*="填写标题"]',
    'input[placeholder*="标题"]',
  ],
  contentInput: [
    'div[contenteditable="true"][placeholder*="填写正文"]',
    'div[contenteditable="true"][placeholder*="添加正文"]',
    'div[contenteditable="true"][placeholder*="Content"]',
    'textarea[placeholder*="填写正文"]',
    'textarea[placeholder*="添加正文"]',
    'div[contenteditable="true"]',
  ],
  publishButton: [
    'button[type="submit"]',
    'button:has-text("发布")',
    'button:has-text("發布")',
    'button:has-text("Publish")',
    '.publish-btn',
    '.submit-btn',
  ],
  imageUpload: [
    'input[type="file"]',
    'input[accept*="image"]',
  ],
};

// ==================== 帮助信息 ====================

function showHelp() {
  console.log(`
🚀 小红书发布工具 - 结合 Cookie 登录 + 自动发布

📋 前提条件:
  1. 先登录: python3 xhs_login.py --file
  2. Cookie 保存在 cookies.txt

📝 发布命令:
  # 预览模式 (不发布)
  bun publish.ts --title "标题" --content "内容" --image photo.png

  # 自动发布
  bun publish.ts --title "标题" --content "内容" --image photo.png --submit

  # 多图发布 (最多 9 张)
  bun publish.ts --title "标题" --content "内容" --image img1.png --image img2.png --submit

  # 从目录加载图片
  bun publish.ts --title "标题" --content "内容" --images ./photos/ --submit

📋 参数:
  --title <text>      标题 (必需)
  --content <text>    内容 (必需)
  --image <path>      图片文件 (可重复，最多9张)
  --images <dir>      图片目录
  --submit            实际发布 (默认预览)

📋 示例:
  bun publish.ts --title "今日穿搭" --content "春日穿搭分享 #OOTD" --image outfit.png --submit
`);
}

// ==================== Playwright 操作 ====================

async function withPlaywright<T>(
  fn: (page: import("playwright-core").Page) => Promise<T>
): Promise<T> {
  const { chromium } = await import("playwright-core");

  console.log(`🔗 连接到 Browserless: {WS_URL}`);
  const browser = await chromium.connectOverCDP(WS_URL);

  // 检查登录状态文件
  if (!existsSync(STATE_FILE)) {
    browser.close();
    console.error("❌ 未找到登录状态文件!");
    console.error("请先运行: python3 xhs_login.py --file");
    process.exit(1);
  }

  console.log(`📂 加载登录状态: {STATE_FILE}`);
  const context = await browser.newContext({
    storageState: STATE_FILE,
    viewport: { width: 1920, height: 1080 },
    locale: "zh-CN",
    timezoneId: "Asia/Shanghai",
  });

  const page = await context.newPage();

  try {
    const result = await fn(page);
    await context.storageState({ path: STATE_FILE });
    return result;
  } finally {
    await browser.close();
  }
}

async function takeScreenshot(page: import("playwright-core").Page, name: string): Promise<string> {
  await mkdir(SCREENSHOT_DIR, { recursive: true });

  const timestamp = new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19);
  const filename = path.join(SCREENSHOT_DIR, `${name}_${timestamp}.png`);

  await page.screenshot({ path: filename, fullPage: true });
  console.log(`📸 截图: {filename}`);

  return filename;
}

// 逐字输入文本 (模拟人类输入)
async function typeText(page: import("playwright-core").Page, text: string): Promise<void> {
  for (const char of text) {
    await page.keyboard.type(char);
    await page.waitForTimeout(Math.random() * 50 + 30); // 随机延迟 30-80ms
  }
}

// 查找并点击元素 (尝试多个选择器)
async function clickAnySelector(page: import("playwright-core").Page, selectors: string[]): Promise<boolean> {
  for (const selector of selectors) {
    try {
      const el = await page.locator(selector).first();
      if (await el.isVisible()) {
        await el.click();
        return true;
      }
    } catch {
      continue;
    }
  }
  return false;
}

// 查找可见元素
async function findAnySelector(page: import("playwright-core").Page, selectors: string[]): Promise<any> {
  for (const selector of selectors) {
    try {
      const el = await page.querySelector(selector);
      if (el && await el.isVisible()) {
        return el;
      }
    } catch {
      continue;
    }
  }
  return null;
}

// 上传图片
async function uploadImages(page: import("playwright-core").Page, images: string[]): Promise<void> {
  console.log(`📷 上传 {images.length} 张图片...`);

  for (let i = 0; i < images.length; i++) {
    const imagePath = images[i]!;
    if (!existsSync(imagePath)) {
      console.warn(`⚠️  图片不存在: {imagePath}`);
      continue;
    }

    console.log(`   [{i + 1}/{images.length}] {path.basename(imagePath)}`);

    // 使用 setInputFiles 上传
    const fileInput = await page.querySelector("input[type='file']");
    if (fileInput) {
      await fileInput.setInputFiles(imagePath);
      await page.waitForTimeout(2000);
    } else {
      console.log(`⚠️  未找到文件上传控件`);
    }
  }

  console.log(`✅ 图片上传完成`);
}

// 发布笔记
async function publishNote(
  page: import("playwright-core").Page,
  title: string,
  content: string,
  images: string[],
  submit: boolean
): Promise<boolean> {
  console.log("\n📝 开始发布笔记...");
  console.log(`📌 标题: {title}`);
  console.log(`✍️  内容: {content.substring(0, 100)}{content.length > 100 ? "..." : ""}`);
  console.log(`📷 图片: {images.length} 张`);
  console.log(`🚢 模式: {submit ? "发布" : "预览"}`);

  // 直接访问创作者平台发布页面
  console.log(`\n🌐 打开发布页面: {PUBLISH_URL}`);
  await page.goto(PUBLISH_URL, { waitUntil: "networkidle" });
  await page.waitForTimeout(3000);

  // 检查是否登录
  const url = page.url();
  if (url.includes("login")) {
    console.log("❌ 未登录，请先运行: python3 xhs_login.py --file");
    return false;
  }

  await takeScreenshot(page, "publish_page");

  // 输入标题
  console.log("\n📌 输入标题...");
  const titleEl = await findAnySelector(page, I18N_SELECTORS.titleInput);
  if (titleEl) {
    await titleEl.focus();
    await titleEl.evaluate((el: any) => { el.value = ''; });
    await typeText(page, title);
    await page.waitForTimeout(500);
    console.log("✅ 标题已输入");
  } else {
    console.log("⚠️  未找到标题输入框");
  }

  // 上传图片
  if (images.length > 0) {
    await uploadImages(page, images);
  }

  // 输入内容
  console.log("\n✍️  输入内容...");
  const contentEl = await findAnySelector(page, I18N_SELECTORS.contentInput);
  if (contentEl) {
    await contentEl.click();
    await page.waitForTimeout(500);
    await typeText(page, content);
    await page.waitForTimeout(1000);
    console.log("✅ 内容已输入");
  } else {
    console.log("⚠️  未找到内容输入框");
  }

  await takeScreenshot(page, "before_submit");

  // 发布
  if (submit) {
    console.log("\n🚀 开始发布...");

    const publishClicked = await clickAnySelector(page, I18N_SELECTORS.publishButton);

    if (publishClicked) {
      console.log("✅ 发布按钮已点击");
      await page.waitForTimeout(5000);

      const finalUrl = page.url();
      console.log(`📄 当前页面: {finalUrl}`);

      if (finalUrl.includes("success") || !finalUrl.includes("publish")) {
        console.log("\n✅ 发布成功！");
      } else {
        console.log("\n⚠️  发布中，请检查浏览器确认");
      }
    } else {
      console.log("\n⚠️  未找到发布按钮，请手动点击发布");
    }
  } else {
    console.log("\n" + "=".repeat(50));
    console.log("👀 预览模式 - 请检查截图");
    console.log("💡 使用 --submit 参数实际发布");
    console.log("=".repeat(50));
  }

  return true;
}

// ==================== 主函数 ====================

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args.includes("--help") || args.includes("-h")) {
    showHelp();
    process.exit(0);
  }

  // 解析参数
  let title: string | undefined;
  let content: string | undefined;
  const images: string[] = [];
  let imagesDir: string | undefined;
  let submit = false;

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (!arg) continue;

    if (arg === "--title" && args[i + 1]) title = args[++i];
    else if (arg === "--content" && args[i + 1]) content = args[++i];
    else if (arg === "--image" && args[i + 1]) images.push(args[++i]);
    else if (arg === "--images" && args[i + 1]) imagesDir = args[++i];
    else if (arg === "--submit") submit = true;
  }

  if (!title) {
    console.error("❌ 错误: --title 参数是必需的");
    console.error("\n用法: bun publish.ts --title \"标题\" --content \"内容\" --image photo.png");
    process.exit(1);
  }

  if (!content) {
    console.error("❌ 错误: --content 参数是必需的");
    process.exit(1);
  }

  // 从目录加载图片
  if (imagesDir) {
    if (!existsSync(imagesDir)) {
      console.error(`❌ 错误: 图片目录不存在: {imagesDir}`);
      process.exit(1);
    }
    const files = readdirSync(imagesDir);
    const imageFiles = files.filter(f =>
      f.endsWith('.png') ||
      f.endsWith('.jpg') ||
      f.endsWith('.jpeg') ||
      f.endsWith('.webp')
    );
    for (const file of imageFiles) {
      images.push(path.join(imagesDir, file));
    }
    images.sort();
  }

  if (images.length === 0) {
    console.error("❌ 错误: 至少需要一张图片 (使用 --image 或 --images)");
    process.exit(1);
  }

  if (images.length > 9) {
    console.error("❌ 错误: 最多支持 9 张图片");
    process.exit(1);
  }

  try {
    await withPlaywright(async (page) => {
      await publishNote(page, title!, content!, images, submit);
    });

    console.log("\n✅ 完成！");
  } catch (error) {
    console.error(`\n❌ 错误: {error instanceof Error ? error.message : String(error)}`);
    process.exit(1);
  }
}

main();
