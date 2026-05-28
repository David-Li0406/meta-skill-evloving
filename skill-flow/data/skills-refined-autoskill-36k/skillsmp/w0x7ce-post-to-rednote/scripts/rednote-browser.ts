import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import { launchChrome, getPageSession, clickElement, typeText, evaluate, sleep, type ChromeSession, type CdpConnection } from './cdp.ts';

const REDNOTE_IMAGE_URL = 'https://creator.xiaohongshu.com/publish/publish?from=tab_switch&target=image';
const REDNOTE_VIDEO_URL = 'https://creator.xiaohongshu.com/publish/publish?from=tab_switch&target=video';
const REDNOTE_ARTICLE_URL = 'https://creator.xiaohongshu.com/publish/publish?from=tab_switch&target=article';

interface PostOptions {
  title: string;
  content: string;
  images: string[];
  submit?: boolean;
  profileDir?: string;
  topic?: string;
}

const I18N_SELECTORS = {
  titleInput: [
    'input[placeholder*="填写标题"]',
    'input[placeholder*="添加标题"]',
    'input[placeholder*="Title"]',
    'textarea[placeholder*="填写标题"]',
    'textarea[placeholder*="添加标题"]',
  ],
  contentInput: [
    'div[contenteditable="true"][placeholder*="填写正文"]',
    'div[contenteditable="true"][placeholder*="添加正文"]',
    'div[contenteditable="true"][placeholder*="Content"]',
    'textarea[placeholder*="填写正文"]',
    'textarea[placeholder*="添加正文"]',
  ],
  publishButton: [
    'button[type="submit"]',
    'button:has-text("发布")',
    'button:has-text("發布")',
    'button:has-text="Publish")',
    '.publish-btn',
    '.submit-btn',
  ],
  imageUpload: [
    'input[type="file"]',
    'input[accept*="image"]',
  ],
};

async function waitForLogin(session: ChromeSession, timeoutMs = 120_000): Promise<boolean> {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    const url = await evaluate<string>(session, 'window.location.href');
    if (url.includes('/publish') || url.includes('/create')) return true;
    await sleep(2000);
  }
  return false;
}

async function uploadImages(session: ChromeSession, images: string[]): Promise<void> {
  console.log(`[rednote] Uploading ${images.length} images...`);

  for (let i = 0; i < images.length; i++) {
    const imagePath = images[i]!;
    if (!fs.existsSync(imagePath)) {
      console.warn(`[rednote] Image not found: ${imagePath}`);
      continue;
    }

    console.log(`[rednote] [${i + 1}/${images.length}] Uploading: ${path.basename(imagePath)}`);

    const absolutePath = path.resolve(imagePath);

    await session.cdp.send('Runtime.evaluate', {
      expression: `
        (function() {
          const fileInputs = document.querySelectorAll('input[type="file"]');
          for (const input of fileInputs) {
            if (input.accept && input.accept.includes('image')) {
              return input.click();
            }
          }
          return false;
        })()
      `,
    }, { sessionId: session.sessionId });

    await sleep(500);

    const { root } = await session.cdp.send<{ root: { nodeId: number } }>('DOM.getDocument', {}, { sessionId: session.sessionId });
    const fileInputs = await session.cdp.send<{ nodeIds: number[] }>('DOM.querySelectorAll', {
      nodeId: root.nodeId,
      selector: 'input[type="file"]',
    }, { sessionId: session.sessionId });

    if (fileInputs.nodeIds.length > 0) {
      await session.cdp.send('DOM.setFileInputFiles', {
        nodeId: fileInputs.nodeIds[0]!,
        files: [absolutePath],
      }, { sessionId: session.sessionId });
      console.log(`[rednote] Image ${i + 1} uploaded`);
    }

    await sleep(2000);
  }

  console.log('[rednote] All images uploaded');
}

export async function postToRednote(options: PostOptions): Promise<void> {
  const { title, content, images, submit = false, profileDir } = options;

  if (!title) throw new Error('Title is required');
  if (!content) throw new Error('Content is required');
  if (!images || images.length === 0) throw new Error('At least one image is required');
  if (images.length > 9) throw new Error('Maximum 9 images allowed');

  console.log(`[rednote] Title: ${title}`);
  console.log(`[rednote] Content length: ${content.length} chars`);
  console.log(`[rednote] Images: ${images.length}`);

  const { cdp, chrome } = await launchChrome(REDNOTE_IMAGE_URL, profileDir);

  try {
    console.log('[rednote] Waiting for page load...');
    await sleep(5000);

    let session = await getPageSession(cdp, 'xiaohongshu.com');

    const url = await evaluate<string>(session, 'window.location.href');

    if (url.includes('login') || !url.includes('creator')) {
      console.log('[rednote] Not logged in. Please login in the browser...');
      const loggedIn = await waitForLogin(session);
      if (!loggedIn) throw new Error('Login timeout');
    }

    console.log('[rednote] Logged in. Navigating to publish page...');

    // Already on the correct page from launchChrome
    await sleep(2000);

    session = await getPageSession(cdp, 'xiaohongshu.com');

    console.log('[rednote] Filling title...');

    const titleSelectors = I18N_SELECTORS.titleInput.join(', ');
    const titleFilled = await session.cdp.send<{ result: { value: boolean } }>('Runtime.evaluate', {
      expression: `
        (function() {
          const selectors = ${JSON.stringify(I18N_SELECTORS.titleInput)};
          for (const sel of selectors) {
            const el = document.querySelector(sel);
            if (el) {
              el.focus();
              el.value = '';
              el.dispatchEvent(new Event('input', { bubbles: true }));
              return true;
            }
          }
          return false;
        })()
      `,
      returnByValue: true,
    }, { sessionId: session.sessionId });

    if (titleFilled.result.value) {
      await typeText(session, title);
      await sleep(500);
    }

    console.log('[rednote] Uploading images...');
    await uploadImages(session, images);

    console.log('[rednote] Filling content...');
    await sleep(1000);

    const contentSelectors = I18N_SELECTORS.contentInput.join(', ');
    const contentFilled = await session.cdp.send<{ result: { value: boolean } }>('Runtime.evaluate', {
      expression: `
        (function() {
          const selectors = ${JSON.stringify(I18N_SELECTORS.contentInput)};
          for (const sel of selectors) {
            const el = document.querySelector(sel);
            if (el) {
              el.focus();
              el.click();
              return true;
            }
          }
          return false;
        })()
      `,
      returnByValue: true,
    }, { sessionId: session.sessionId });

    if (contentFilled.result.value) {
      await sleep(500);
      await typeText(session, content);
      await sleep(1000);
    }

    if (submit) {
      console.log('[rednote] Publishing...');

      await sleep(2000);

      const publishClicked = await session.cdp.send<{ result: { value: boolean } }>('Runtime.evaluate', {
        expression: `
          (function() {
            const buttons = document.querySelectorAll('button');
            for (const btn of buttons) {
              const text = btn.textContent || '';
              if (text.includes('发布') || text.includes('發布') || text.includes('Publish') || text.includes('提交')) {
                btn.click();
                return true;
              }
            }
            return false;
          })()
        `,
        returnByValue: true,
      }, { sessionId: session.sessionId });

      if (publishClicked.result.value) {
        console.log('[rednote] Publish button clicked');
        await sleep(5000);
        console.log('[rednote] Post published!');
      } else {
        console.log('[rednote] Publish button not found. Please publish manually.');
      }
    } else {
      console.log('[rednote] Preview mode. Please review and publish manually.');
      console.log('[rednote] Browser window left open.');
    }

  } finally {
    cdp.close();
  }
}

function printUsage(): never {
  console.log(`Post to Xiaohongshu (Little Red Book)

Usage:
  npx -y bun rednote-browser.ts [options]

Options:
  --title <text>      Post title (required)
  --content <text>    Post content (required)
  --image <path>      Image file path (can repeat, 1-9 images)
  --images <dir>      Directory containing images
  --markdown <path>   Extract title/content from markdown
  --topic <text>      Topic/Category (optional)
  --submit            Actually publish (default: preview)
  --profile <dir>     Chrome profile directory

Examples:
  npx -y bun rednote-browser.ts --title "标题" --content "内容" --image photo.png
  npx -y bun rednote-browser.ts --title "标题" --content "内容" --image img1.png --image img2.png --submit
  npx -y bun rednote-browser.ts --markdown article.md --images ./photos/ --submit
`);
  process.exit(0);
}

function parseMarkdown(markdownPath: string): { title: string; content: string } {
  const content = fs.readFileSync(markdownPath, 'utf-8');
  const lines = content.split('\n');

  let title = '';
  let contentLines: string[] = [];

  for (const line of lines) {
    if (line.startsWith('# ')) {
      title = line.substring(2).trim();
    } else if (line.trim()) {
      contentLines.push(line);
    }
  }

  if (!title) title = path.basename(markdownPath, '.md');

  return {
    title,
    content: contentLines.join('\n').trim(),
  };
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  if (args.includes('--help') || args.includes('-h')) printUsage();

  let title: string | undefined;
  let content: string | undefined;
  const images: string[] = [];
  let markdownFile: string | undefined;
  let imagesDir: string | undefined;
  let topic: string | undefined;
  let submit = false;
  let profileDir: string | undefined;

  for (let i = 0; i < args.length; i++) {
    const arg = args[i]!;
    if (arg === '--title' && args[i + 1]) title = args[++i];
    else if (arg === '--content' && args[i + 1]) content = args[++i];
    else if (arg === '--image' && args[i + 1]) images.push(args[++i]!);
    else if (arg === '--images' && args[i + 1]) imagesDir = args[++i];
    else if (arg === '--markdown' && args[i + 1]) markdownFile = args[++i];
    else if (arg === '--topic' && args[i + 1]) topic = args[++i];
    else if (arg === '--submit') submit = true;
    else if (arg === '--profile' && args[i + 1]) profileDir = args[++i];
  }

  if (markdownFile) {
    if (!fs.existsSync(markdownFile)) {
      console.error(`Error: Markdown file not found: ${markdownFile}`);
      process.exit(1);
    }
    const parsed = parseMarkdown(markdownFile);
    title = title || parsed.title;
    content = content || parsed.content;
  }

  if (imagesDir) {
    if (!fs.existsSync(imagesDir)) {
      console.error(`Error: Images directory not found: ${imagesDir}`);
      process.exit(1);
    }
    const files = fs.readdirSync(imagesDir);
    const imageFiles = files.filter(f => f.endsWith('.png') || f.endsWith('.jpg') || f.endsWith('.jpeg') || f.endsWith('.webp'));
    for (const file of imageFiles) {
      images.push(path.join(imagesDir, file));
    }
    images.sort();
  }

  if (!title) { console.error('Error: --title is required (or use --markdown)'); process.exit(1); }
  if (!content) { console.error('Error: --content is required (or use --markdown)'); process.exit(1); }
  if (images.length === 0) { console.error('Error: At least one --image or --images directory is required'); process.exit(1); }

  await postToRednote({ title: title || '', content: content || '', images, submit, profileDir, topic });
}

await main().catch((err) => {
  console.error(`Error: ${err instanceof Error ? err.message : String(err)}`);
  process.exit(1);
});
