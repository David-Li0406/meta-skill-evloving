import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import { launchChrome, getPageSession, typeText, evaluate, sleep, type ChromeSession } from './cdp.ts';

// LinkedIn URLs
const LINKEDIN_FEED_URL = 'https://www.linkedin.com/feed/';
const LINKEDIN_DOMAIN = 'linkedin.com';

// Multi-language selectors for "Start a post" button
const START_POST_SELECTORS = [
  'button[aria-label*="Start a post"]',
  'button[aria-label*="开始发帖"]',
  'button[aria-label*="開始發貼"]',
  'div.share-box-feed-entry__trigger',
  'button[data-control-name="share_box"]',
  'span[aria-label*="Start a post"]',
];

// Multi-language selectors for post editor
const EDITOR_SELECTORS = [
  'div[contenteditable="true"][role="textbox"]',
  'div[role="textbox"]',
  'div.ql-editor',
  '[data-artdeco-is-focused="true"]',
];

// Multi-language selectors for post button
const POST_BUTTON_SELECTORS = [
  'button[aria-label*="Post"]',
  'button[aria-label*="发布"]',
  'button[aria-label*="發佈"]',
  'button[data-control-name="share.post"]',
  'button.share-actions__primary-action',
];

interface PostOptions {
  text?: string;
  images?: string[];
  submit?: boolean;
  profileDir?: string;
}

async function waitForElement(session: ChromeSession, selectors: string[], timeoutMs = 30_000): Promise<boolean> {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    const result = await session.cdp.send<{ result: { value: boolean } }>('Runtime.evaluate', {
      expression: `
        (function() {
          const selectors = ${JSON.stringify(selectors)};
          for (const selector of selectors) {
            const el = document.querySelector(selector);
            if (el && el.offsetParent !== null) return true;
          }
          return false;
        })()
      `,
      returnByValue: true,
    }, { sessionId: session.sessionId });
    if (result.result.value) return true;
    await sleep(500);
  }
  return false;
}

async function clickStartPostButton(session: ChromeSession): Promise<void> {
  console.log('[linkedin] Looking for "Start a post" button...');

  // Wait for page to fully load
  await sleep(3000);

  // Debug: Find the exact button and get its position
  const buttonInfo = await session.cdp.send<{ result: { value: any } }>('Runtime.evaluate', {
    expression: `
      (function() {
        const all = document.querySelectorAll('*');
        for (const el of all) {
          if (el.offsetParent !== null) {
            const text = (el.textContent || '').trim();
            const tag = el.tagName.toLowerCase();
            const classList = el.className || '';

            // Look specifically for "Start a post" text
            if (text === 'Start a post' && (tag === 'button' || tag === 'div' || tag === 'span')) {
              const rect = el.getBoundingClientRect();
              el.scrollIntoView({ block: 'center' });
              return {
                found: true,
                x: rect.x + rect.width / 2,
                y: rect.y + rect.height / 2,
                text: text,
                tag: tag,
                classList: classList.substring(0, 50)
              };
            }
          }
        }
        return { found: false };
      })()
    `,
    returnByValue: true,
  }, { sessionId: session.sessionId, timeoutMs: 30_000 });

  console.log(`[linkedin] Button info: ${JSON.stringify(buttonInfo.result.value)}`);

  if (!buttonInfo.result.value?.found) {
    throw new Error('Could not find "Start a post" button');
  }

  const { x, y } = buttonInfo.result.value;
  console.log(`[linkedin] Clicking button at (${x}, ${y})`);

  // Click using mouse events
  await session.cdp.send('Input.dispatchMouseEvent', {
    type: 'mousePressed',
    x, y,
    button: 'left',
    clickCount: 1
  }, { sessionId: session.sessionId });
  await sleep(50);
  await session.cdp.send('Input.dispatchMouseEvent', {
    type: 'mouseReleased',
    x, y,
    button: 'left',
    clickCount: 1
  }, { sessionId: session.sessionId });

  console.log('[linkedin] Button clicked! Waiting for editor modal to load...');
  // Wait longer for modal to fully appear
  await sleep(5000);
}

async function fillEditor(session: ChromeSession, text: string): Promise<void> {
  console.log('[linkedin] Waiting for editor to load...');

  // Wait longer for the modal to fully load
  await sleep(5000);

  // Debug: Show all potential text input elements (expanded search)
  const editorDebug = await session.cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
    expression: `
      (function() {
        const results = [];
        const all = document.querySelectorAll('*');
        for (const el of all) {
          if (el.offsetParent !== null) {
            const tag = el.tagName.toLowerCase();
            const classList = el.className || '';
            const contentEditable = el.getAttribute('contenteditable');
            const role = el.getAttribute('role');
            const placeholder = el.getAttribute('placeholder') || '';
            const textContent = (el.textContent || '').trim().substring(0, 20);

            // Expanded search for any text-capable element
            const rect = el.getBoundingClientRect();
            if (rect.width > 50 && rect.height > 20) {
              const isEditable = contentEditable === 'true' ||
                                role === 'textbox' ||
                                tag === 'textarea' ||
                                placeholder.includes('What do you want') ||
                                placeholder.includes('想说什么') ||
                                classList.includes('editor') ||
                                classList.includes('ql-editor');

              if (isEditable) {
                results.push(tag + '.' + classList.substring(0, 30) +
                  ': ce=' + contentEditable + ', role=' + role + ', ph=' + placeholder.substring(0, 20) +
                  ', text=' + textContent + ', size=' + Math.round(rect.width) + 'x' + Math.round(rect.height));
              }
            }
          }
        }
        return results.slice(0, 30).join(' | ');
      })()
    `,
    returnByValue: true,
  }, { sessionId: session.sessionId, timeoutMs: 30_000 });

  console.log(`[linkedin] All text input candidates: ${editorDebug.result.value?.substring(0, 800) || 'none'}`);

  // Try to find and focus the editor with multiple attempts
  let editorFound = false;

  // Attempt 1: Standard selectors
  console.log('[linkedin] Trying standard selectors...');
  const found = await waitForElement(session, EDITOR_SELECTORS, 5_000);
  if (found) {
    console.log('[linkedin] Found editor via standard selectors');
    editorFound = true;
  }

  // Attempt 2: Any contenteditable element that's large enough
  if (!editorFound) {
    console.log('[linkedin] Looking for any large contenteditable...');
    const largeEditable = await session.cdp.send<{ result: { value: boolean } }>('Runtime.evaluate', {
      expression: `
        (function() {
          const editables = document.querySelectorAll('[contenteditable="true"]');
          for (const el of editables) {
            if (el.offsetParent !== null) {
              const rect = el.getBoundingClientRect();
              // Look for reasonably large contenteditable areas
              if (rect.width > 200 && rect.height > 50) {
                el.focus();
                el.click();
                // Make sure it's really focused
                el.scrollIntoView({ block: 'center' });
                return true;
              }
            }
          }
          return false;
        })()
      `,
      returnByValue: true,
    }, { sessionId: session.sessionId });

    if (largeEditable.result.value) {
      console.log('[linkedin] Found large contenteditable area');
      editorFound = true;
    }
  }

  // Attempt 3: Try clicking in the modal center area
  if (!editorFound) {
    console.log('[linkedin] Trying to click in modal center...');
    await session.cdp.send('Input.dispatchMouseEvent', {
      type: 'mousePressed',
      x: window.innerWidth ? window.innerWidth / 2 : 500,
      y: 300,
      button: 'left',
      clickCount: 1
    }, { sessionId: session.sessionId });
    await sleep(50);
    await session.cdp.send('Input.dispatchMouseEvent', {
      type: 'mouseReleased',
      x: window.innerWidth ? window.innerWidth / 2 : 500,
      y: 300,
      button: 'left',
      clickCount: 1
    }, { sessionId: session.sessionId });
    await sleep(500);
  }

  // Type text
  console.log('[linkedin] Typing content...');

  // First try to focus editor
  await session.cdp.send('Runtime.evaluate', {
    expression: `
      (function() {
        // Try multiple ways to find and focus the editor
        const selectors = ${JSON.stringify(EDITOR_SELECTORS)};
        for (const selector of selectors) {
          const el = document.querySelector(selector);
          if (el && el.offsetParent !== null) {
            el.focus();
            el.click();
            return true;
          }
        }

        // Try any contenteditable
        const editables = document.querySelectorAll('[contenteditable="true"]');
        for (const el of editables) {
          if (el.offsetParent !== null) {
            const rect = el.getBoundingClientRect();
            if (rect.width > 100 && rect.height > 30) {
              el.focus();
              el.click();
              return true;
            }
          }
        }

        return false;
      })()
    `,
    returnByValue: true,
  }, { sessionId: session.sessionId });

  await sleep(500);

  // Type the text character by character
  await typeText(session, text);
  console.log('[linkedin] Content typed');
  await sleep(2000);
}

async function uploadImages(session: ChromeSession, images: string[]): Promise<void> {
  if (images.length === 0) return;

  console.log(`[linkedin] Uploading ${images.length} image(s)...`);

  for (const imagePath of images) {
    if (!fs.existsSync(imagePath)) {
      console.warn(`[linkedin] Image not found: ${imagePath}`);
      continue;
    }

    console.log(`[linkedin] Processing: ${imagePath}`);

    // Look for file input
    const fileInputFound = await session.cdp.send<{ result: { value: boolean } }>('Runtime.evaluate', {
      expression: `
        (function() {
          const inputs = document.querySelectorAll('input[type="file"]');
          for (const input of inputs) {
            if (input.offsetParent !== null) {
              return true;
            }
          }
          return false;
        })()
      `,
      returnByValue: true,
    }, { sessionId: session.sessionId });

    if (!fileInputFound.result.value) {
      console.warn('[linkedin] File input not found. You may need to add images manually.');
      continue;
    }

    // Convert image to base64 and upload
    const imageBuffer = fs.readFileSync(imagePath);
    const base64Image = imageBuffer.toString('base64');
    const mimeType = path.extname(imagePath) === '.png' ? 'image/png' : 'image/jpeg';

    // Upload using file input
    await session.cdp.send('Runtime.evaluate', {
      expression: `
        (function() {
          const inputs = document.querySelectorAll('input[type="file"]');
          for (const input of inputs) {
            if (input.offsetParent !== null) {
              const file = new File([Uint8Array.from(atob('${base64Image}'), c => c.charCodeAt(0))], '${path.basename(imagePath)}', { type: '${mimeType}' });
              const dataTransfer = new DataTransfer();
              dataTransfer.items.add(file);
              input.files = dataTransfer.files;
              input.dispatchEvent(new Event('change', { bubbles: true }));
              return true;
            }
          }
          return false;
        })()
      `,
      returnByValue: true,
    }, { sessionId: session.sessionId });

    console.log('[linkedin] Waiting for upload to complete...');
    await sleep(3000);
  }

  console.log('[linkedin] Image upload complete');
}

async function submitPost(session: ChromeSession): Promise<void> {
  console.log('[linkedin] Looking for Post button...');

  // Wait for UI to stabilize
  await sleep(3000);

  // Debug: Find all buttons with "Post" or similar text
  const buttonSearch = await session.cdp.send<{ result: { value: any } }>('Runtime.evaluate', {
    expression: `
      (function() {
        const results = [];
        const all = document.querySelectorAll('*');
        for (const el of all) {
          if (el.offsetParent !== null) {
            const text = (el.textContent || '').trim();
            const tag = el.tagName.toLowerCase();
            const classList = el.className || '';
            const ariaLabel = el.getAttribute('aria-label') || '';

            // Look for Post button specifically
            if (tag === 'button' || tag === 'div' || tag === 'span') {
              if (text === 'Post' || text === 'post' ||
                  ariaLabel === 'Post' || ariaLabel === 'post' ||
                  text === '发布' || text === '發佈') {
                const rect = el.getBoundingClientRect();
                if (rect.width > 30 && rect.height > 20 && rect.width < 300) {
                  results.push({
                    text: text,
                    x: rect.x + rect.width / 2,
                    y: rect.y + rect.height / 2,
                    tag: tag,
                    classList: classList.substring(0, 50)
                  });
                }
              }
            }
          }
        }
        return results;
      })()
    `,
    returnByValue: true,
  }, { sessionId: session.sessionId, timeoutMs: 30_000 });

  console.log(`[linkedin] Post buttons found: ${JSON.stringify(buttonSearch.result.value)}`);

  const buttons = buttonSearch.result.value;
  if (!buttons || buttons.length === 0) {
    console.log('[linkedin] No Post button found, trying alternative search...');
    // Try broader search
    const altSearch = await session.cdp.send<{ result: { value: any } }>('Runtime.evaluate', {
      expression: `
        (function() {
          const all = document.querySelectorAll('button, [role="button"]');
          for (const btn of all) {
            if (btn.offsetParent !== null && !btn.disabled) {
              const text = (btn.textContent || '').trim().toLowerCase();
              const classList = (btn.className || '').toLowerCase();
              const ariaLabel = (btn.getAttribute('aria-label') || '').toLowerCase();

              if (text.includes('post') || text.includes('send') ||
                  ariaLabel.includes('post') || ariaLabel.includes('send') ||
                  classList.includes('share-primary') || classList.includes('post')) {
                const rect = btn.getBoundingClientRect();
                return {
                  text: (btn.textContent || '').trim(),
                  x: rect.x + rect.width / 2,
                  y: rect.y + rect.height / 2
                };
              }
            }
          }
          return { found: false };
        })()
      `,
      returnByValue: true,
    }, { sessionId: session.sessionId });

    if (altSearch.result.value?.found) {
      const { x, y } = altSearch.result.value;
      console.log(`[linkedin] Clicking alternative button at (${x}, ${y}): ${altSearch.result.value.text}`);
      await session.cdp.send('Input.dispatchMouseEvent', {
        type: 'mousePressed',
        x, y,
        button: 'left',
        clickCount: 1
      }, { sessionId: session.sessionId });
      await sleep(50);
      await session.cdp.send('Input.dispatchMouseEvent', {
        type: 'mouseReleased',
        x, y,
        button: 'left',
        clickCount: 1
      }, { sessionId: session.sessionId });
      console.log('[linkedin] Clicked!');
      await sleep(3000);
      return;
    }

    console.log('[linkedin] Post button not found. You may need to click manually.');
    console.log('[linkedin] Keeping browser open for 15 seconds...');
    await sleep(15000);
    return;
  }

  // Click the first (usually main) Post button
  const postButton = buttons[0];
  const { x, y, text } = postButton;
  console.log(`[linkedin] Clicking Post button at (${x}, ${y}): ${text}`);

  await session.cdp.send('Input.dispatchMouseEvent', {
    type: 'mousePressed',
    x, y,
    button: 'left',
    clickCount: 1
  }, { sessionId: session.sessionId });
  await sleep(50);
  await session.cdp.send('Input.dispatchMouseEvent', {
    type: 'mouseReleased',
    x, y,
    button: 'left',
    clickCount: 1
  }, { sessionId: session.sessionId });

  console.log('[linkedin] Post clicked! Waiting for submission...');
  await sleep(3000);
  console.log('[linkedin] Post submitted!');
}

export async function postToLinkedIn(options: PostOptions): Promise<void> {
  const { text = '', images = [], submit = false, profileDir } = options;

  if (!text && images.length === 0) {
    throw new Error('Provide text or at least one image.');
  }

  console.log(`[linkedin] Content length: ${text.length} chars`);
  console.log(`[linkedin] Images: ${images.length}`);

  const { cdp, chrome } = await launchChrome(LINKEDIN_FEED_URL, profileDir);

  try {
    console.log('[linkedin] Waiting for page load...');
    await sleep(8000);

    let session = await getPageSession(cdp, LINKEDIN_DOMAIN);

    // Wait for actual page to load
    console.log('[linkedin] Waiting for page content to load...');
    let url = await evaluate<string>(session, 'window.location.href');
    let retries = 0;
    while ((url === 'about:blank' || !url.includes(LINKEDIN_DOMAIN)) && retries < 20) {
      await sleep(1000);
      url = await evaluate<string>(session, 'window.location.href');
      retries++;
      if (retries % 3 === 0) {
        console.log(`[linkedin] Still loading... (${url})`);
      }
    }

    console.log(`[linkedin] Current URL: ${url}`);

    // Wait for login if needed
    if (url.includes('login') || url.includes('auth') || url.includes('checkpoint')) {
      console.log('[linkedin] Please log in to LinkedIn...');
      console.log('[linkedin] Waiting for login (up to 5 minutes)...');

      const start = Date.now();
      while (Date.now() - start < 300_000) {
        await sleep(3000);
        const currentUrl = await evaluate<string>(session, 'window.location.href');
        if (currentUrl.includes('feed') && !currentUrl.includes('login')) {
          console.log('[linkedin] Logged in!');
          await sleep(2000);
          session = await getPageSession(cdp, LINKEDIN_DOMAIN);
          break;
        }
        const elapsed = Math.floor((Date.now() - start) / 1000);
        if (elapsed % 15 === 0) {
          console.log(`[linkedin] Still waiting... (${elapsed}s)`);
        }
      }
    }

    // Wait for feed to load
    await sleep(3000);

    // Click "Start a post" button
    await clickStartPostButton(session);

    // Fill content
    if (text) {
      await fillEditor(session, text);
    }

    // Upload images
    if (images.length > 0) {
      await uploadImages(session, images);
    }

    // Submit or preview
    if (submit) {
      await submitPost(session);
    } else {
      console.log('[linkedin] Preview mode - Post ready to review');
      console.log('[linkedin] Browser will stay open for 30 seconds...');
      await sleep(30_000);
    }

  } finally {
    console.log('[linkedin] Closing browser...');
    cdp.close();
    try {
      chrome.kill('SIGTERM');
      await sleep(2000);
      if (!chrome.killed) {
        chrome.kill('SIGKILL');
      }
    } catch {}
  }
}

function printUsage(): never {
  console.log(`Post to LinkedIn using Chrome CDP automation

Usage:
  npx -y bun linkedin-browser.ts [options] [text]

Options:
  --image <path>   Add image (can be repeated)
  --submit         Actually post (default: preview only)
  --profile <dir>  Chrome profile directory
  --help           Show this help

Examples:
  npx -y bun linkedin-browser.ts "Hello LinkedIn!"
  npx -y bun linkedin-browser.ts "Check this out" --image ./photo.jpg --submit
`);
  process.exit(0);
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  if (args.includes('--help') || args.includes('-h')) printUsage();

  const images: string[] = [];
  let submit = false;
  let profileDir: string | undefined;
  const textParts: string[] = [];

  for (let i = 0; i < args.length; i++) {
    const arg = args[i]!;
    if (arg === '--image' && args[i + 1]) {
      images.push(args[++i]!);
    } else if (arg === '--submit') {
      submit = true;
    } else if (arg === '--profile' && args[i + 1]) {
      profileDir = args[++i];
    } else if (!arg.startsWith('-')) {
      textParts.push(arg);
    }
  }

  const text = textParts.join(' ').trim() || '';

  if (!text && images.length === 0) {
    console.error('Error: Provide text or at least one image.');
    process.exit(1);
  }

  await postToLinkedIn({ text, images, submit, profileDir });
}

await main().catch((err) => {
  console.error(`Error: ${err instanceof Error ? err.message : String(err)}`);
  process.exit(1);
});
