import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import { launchChrome, getPageSession, typeText, evaluate, sleep, type ChromeSession } from './cdp.ts';

// Tencent Docs URLs
const TENCENT_DOCS_HOME_URL = 'https://doc.weixin.qq.com/home/recent';
const TENCENT_DOCS_DOMAIN = 'doc.weixin.qq.com';

interface PostOptions {
  title: string;
  content: string;
  submit?: boolean;
  profileDir?: string;
}

// Result of the document creation
interface DocResult {
  url: string;
  shareLink?: string;
}

async function fillEditor(session: ChromeSession, title: string, content: string): Promise<void> {
  console.log('[tencent-docs] Filling document...');

  // Wait for editor to fully load
  console.log('[tencent-docs] Waiting for editor to load...');
  await sleep(5000);

  // Debug: Check what's available
  const debug = await session.cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
    expression: `
      (function() {
        const results = [];
        // Check all input elements
        const inputs = document.querySelectorAll('input, textarea, [contenteditable]');
        for (const el of inputs) {
          const tag = el.tagName.toLowerCase();
          const type = el.getAttribute('type') || '';
          const placeholder = el.getAttribute('placeholder') || '';
          const className = el.className || '';
          results.push(tag + '[type=' + type + '][placeholder=' + placeholder + '][class=' + className + ']');
        }
        return results.join(' | ');
      })()
    `,
    returnByValue: true,
  }, { sessionId: session.sessionId, timeoutMs: 30_000 });

  console.log(`[tencent-docs] Available inputs: ${debug.result.value.substring(0, 300)}`);

  // Try to find and click on the editor area
  const editorResult = await session.cdp.send<{ result: { value: boolean } }>('Runtime.evaluate', {
    expression: `
      (function() {
        // Click on body to ensure focus
        document.body.click();

        // Try to find contenteditable areas
        const editables = document.querySelectorAll('[contenteditable="true"], .editor, #editor, [role="textbox"]');
        for (const el of editables) {
          if (el.offsetParent !== null) {
            el.focus();
            el.click();
            return true;
          }
        }

        // Fallback: click in the middle of the page
        const body = document.body;
        if (body) {
          body.click();
          body.focus();
        }
        return true;
      })()
    `,
    returnByValue: true,
  }, { sessionId: session.sessionId, timeoutMs: 30_000 });

  console.log(`[tencent-docs] Editor focused: ${editorResult.result.value}`);

  await sleep(500);

  // Type title first (on first line)
  await session.cdp.send('Input.insertText', { text: title }, { sessionId: session.sessionId });
  console.log('[tencent-docs] Title inserted');

  await sleep(500);

  // Press Enter to go to new line
  await session.cdp.send('Input.dispatchKeyEvent', {
    type: 'keyDown',
    key: 'Enter',
    code: 'Enter',
    windowsVirtualKeyCode: 13
  }, { sessionId: session.sessionId });
  await session.cdp.send('Input.dispatchKeyEvent', {
    type: 'keyUp',
    key: 'Enter',
    code: 'Enter',
    windowsVirtualKeyCode: 13
  }, { sessionId: session.sessionId });

  await sleep(300);

  // Type content
  await typeText(session, content);
  console.log('[tencent-docs] Content filled');
}

async function getShareLink(session: ChromeSession): Promise<string> {
  console.log('[tencent-docs] Getting share link...');

  await sleep(2000);

  // The document URL is the share link
  const currentUrl = await session.cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
    expression: 'window.location.href',
    returnByValue: true,
  }, { sessionId: session.sessionId, timeoutMs: 10_000 });

  const shareUrl = currentUrl.result.value;
  console.log(`[tencent-docs] Share link: ${shareUrl}`);
  return shareUrl;
}

export async function postToTencentDocs(options: PostOptions): Promise<DocResult> {
  const { title, content, submit = false, profileDir } = options;

  if (!title) throw new Error('Title is required');
  if (!content) throw new Error('Content is required');

  console.log(`[tencent-docs] Title: ${title}`);
  console.log(`[tencent-docs] Content length: ${content.length} chars`);

  const { cdp, chrome } = await launchChrome(TENCENT_DOCS_HOME_URL, profileDir);

  try {
    console.log('[tencent-docs] Waiting for page load...');
    await sleep(8000);

    let session = await getPageSession(cdp, TENCENT_DOCS_DOMAIN);

    // Wait for actual page to load (not about:blank)
    console.log('[tencent-docs] Waiting for page content to load...');
    let url = await evaluate<string>(session, 'window.location.href');
    let retries = 0;
    while ((url === 'about:blank' || !url.includes(TENCENT_DOCS_DOMAIN)) && retries < 20) {
      await sleep(1000);
      url = await evaluate<string>(session, 'window.location.href');
      retries++;
      if (retries % 3 === 0) {
        console.log(`[tencent-docs] Still loading... (${url})`);
      }
    }

    console.log(`[tencent-docs] Current URL: ${url}`);

    // Wait for login if needed
    if (url.includes('login') || url.includes('auth')) {
      console.log('[tencent-docs] Please scan QR code to login...');
      console.log('[tencent-docs] Waiting for login (up to 5 minutes)...');

      const start = Date.now();
      while (Date.now() - start < 300_000) {
        await sleep(3000);
        const currentUrl = await evaluate<string>(session, 'window.location.href');
        if (currentUrl.includes(TENCENT_DOCS_DOMAIN) && !currentUrl.includes('login')) {
          console.log('[tencent-docs] Logged in!');
          // Get fresh session after login redirect
          await sleep(2000);
          session = await getPageSession(cdp, TENCENT_DOCS_DOMAIN);
          break;
        }
        const elapsed = Math.floor((Date.now() - start) / 1000);
        if (elapsed % 15 === 0) {
          console.log(`[tencent-docs] Still waiting... (${elapsed}s)`);
        }
      }
    }

    // Wait for page to stabilize
    await sleep(3000);

    // Click "新建" button and get its position for subsequent mouse clicks
    console.log('[tencent-docs] Finding "新建" button...');
    const buttonInfo = await session.cdp.send<{ result: { value: any } }>('Runtime.evaluate', {
      expression: `
        (function() {
          const all = document.querySelectorAll('*');
          for (const el of all) {
            const text = (el.textContent || '').trim();
            if (text === '新建' && el.offsetParent !== null) {
              const rect = el.getBoundingClientRect();
              el.scrollIntoView({ block: 'center' });
              // Don't click yet, just get position
              return {
                found: true,
                x: rect.x + rect.width / 2,
                y: rect.y + rect.height / 2,
                bottomY: rect.bottom,
                element: el.tagName + '.' + el.className
              };
            }
          }
          return { found: false };
        })()
      `,
      returnByValue: true,
    }, { sessionId: session.sessionId, timeoutMs: 30_000 });

    console.log(`[tencent-docs] Button position: ${JSON.stringify(buttonInfo.result.value)}`);

    if (!buttonInfo.result.value?.found) {
      throw new Error('Could not find "新建" button');
    }

    const { x, y, bottomY } = buttonInfo.result.value;

    // Click the "新建" button using mouse
    console.log('[tencent-docs] Clicking "新建" button with mouse...');
    await session.cdp.send('Input.dispatchMouseEvent', {
      type: 'mousePressed',
      x, y,
      button: 'left',
      clickCount: 1
    }, { sessionId: session.sessionId });
    await session.cdp.send('Input.dispatchMouseEvent', {
      type: 'mouseReleased',
      x, y,
      button: 'left',
      clickCount: 1
    }, { sessionId: session.sessionId });

    // Wait for dropdown menu to appear below the button
    console.log('[tencent-docs] Waiting for dropdown menu...');
    await sleep(2000);

    // Debug: Show all visible elements with their positions
    const menuDebug = await session.cdp.send<{ result: { value: string } }>('Runtime.evaluate', {
      expression: `
        (function() {
          const results = [];
          const all = document.querySelectorAll('*');
          for (const el of all) {
            if (el.offsetParent !== null) {
              const text = (el.textContent || '').trim();
              if (text.length > 0 && text.length < 20) {
                const rect = el.getBoundingClientRect();
                const tag = el.tagName.toLowerCase();
                if (tag === 'div' || tag === 'span' || tag === 'a' || tag === 'li') {
                  results.push(tag + '@' + Math.round(rect.x) + ',' + Math.round(rect.y) + ': ' + text);
                }
              }
            }
          }
          return results.slice(0, 50).join(' | ');
        })()
      `,
      returnByValue: true,
    }, { sessionId: session.sessionId, timeoutMs: 30_000 });

    console.log(`[tencent-docs] Visible elements: ${menuDebug.result.value.substring(0, 500)}`);

    // Look for "文档" and click it with mouse
    console.log('[tencent-docs] Looking for "文档" to click...');
    const docResult = await session.cdp.send<{ result: { value: any } }>('Runtime.evaluate', {
      expression: `
        (function() {
          const all = document.querySelectorAll('*');
          for (const el of all) {
            const text = (el.textContent || '').trim();
            if (text === '文档' && el.offsetParent !== null) {
              const rect = el.getBoundingClientRect();
              el.scrollIntoView({ block: 'center' });
              return {
                found: true,
                x: rect.x + rect.width / 2,
                y: rect.y + rect.height / 2,
                element: el.tagName + '.' + el.className
              };
            }
          }
          return { found: false };
        })()
      `,
      returnByValue: true,
    }, { sessionId: session.sessionId, timeoutMs: 30_000 });

    console.log(`[tencent-docs] Doc element: ${JSON.stringify(docResult.result.value)}`);

    if (docResult.result.value?.found) {
      const { x: docX, y: docY } = docResult.result.value;
      await session.cdp.send('Input.dispatchMouseEvent', {
        type: 'mousePressed',
        x: docX, y: docY,
        button: 'left',
        clickCount: 1
      }, { sessionId: session.sessionId });
      await session.cdp.send('Input.dispatchMouseEvent', {
        type: 'mouseReleased',
        x: docX, y: docY,
        button: 'left',
        clickCount: 1
      }, { sessionId: session.sessionId });
      console.log('[tencent-docs] Clicked "文档"!');
    } else {
      throw new Error('Could not find "文档" menu item after clicking "新建"');
    }

    // Wait for new document tab to open
    console.log('[tencent-docs] Waiting for new document tab...');
    await sleep(5000);

    // Find new document tab
    const targets = await cdp.send<{ targetInfos: Array<{ targetId: string; url: string; type: string }> }>('Target.getTargets');
    const docTab = targets.targetInfos.find(t =>
      t.type === 'page' &&
      (t.url.includes('/doc/') || t.url.includes('/d/')) &&
      t.url.includes(TENCENT_DOCS_DOMAIN)
    );

    if (!docTab) {
      throw new Error('New document tab not found. Please check browser.');
    }

    console.log(`[tencent-docs] Found document: ${docTab.url}`);

    // Attach to new document
    const { sessionId } = await cdp.send<{ sessionId: string }>('Target.attachToTarget', {
      targetId: docTab.targetId,
      flatten: true
    });

    await cdp.send('Page.enable', {}, { sessionId });
    await cdp.send('Runtime.enable', {}, { sessionId });
    await cdp.send('DOM.enable', {}, { sessionId });

    session = { cdp, sessionId, targetId: docTab.targetId };

    // Fill the document
    await fillEditor(session, title, content);

    // Get share link
    const shareLink = await getShareLink(session);

    const result: DocResult = {
      url: docTab.url,
      shareLink: shareLink || undefined
    };

    console.log('[tencent-docs] Document created!');
    console.log(`[tencent-docs] Document URL: ${result.url}`);
    if (result.shareLink) {
      console.log(`[tencent-docs] Share Link: ${result.shareLink}`);
    }

    if (submit) {
      console.log('[tencent-docs] Keeping browser open for 5 seconds for review...');
      await sleep(5000);
    } else {
      console.log('[tencent-docs] Preview mode - Browser left open for 30s');
      await sleep(30_000);
    }

    // Close CDP connection
    cdp.close();

    return result;

  } finally {
    // Always close the Chrome process we started
    console.log('[tencent-docs] Closing browser...');
    try {
      chrome.kill('SIGTERM');
      await sleep(2000);
      // Force kill if still running
      if (!chrome.killed) {
        chrome.kill('SIGKILL');
      }
    } catch {}
  }
}

function printUsage(): never {
  console.log(`Post to Tencent Docs (腾讯文档)

Usage:
  npx -y bun tencent-docs-browser.ts [options]

Options:
  --title <text>      Document title (required)
  --content <text>    Document content (required)
  --submit            Leave browser open (default: close after preview)
  --profile <dir>     Chrome profile directory

Example:
  npx -y bun tencent-docs-browser.ts --title "Test" --content "Hello" --submit
`);
  process.exit(0);
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  if (args.includes('--help') || args.includes('-h')) printUsage();

  let title: string | undefined;
  let content: string | undefined;
  let submit = false;
  let profileDir: string | undefined;

  for (let i = 0; i < args.length; i++) {
    const arg = args[i]!;
    if (arg === '--title' && args[i + 1]) title = args[++i];
    else if (arg === '--content' && args[i + 1]) content = args[++i];
    else if (arg === '--submit') submit = true;
    else if (arg === '--profile' && args[i + 1]) profileDir = args[++i];
  }

  if (!title || !content) {
    console.error('Error: --title and --content are required');
    printUsage();
  }

  const result = await postToTencentDocs({ title, content, submit, profileDir });

  // Output result as JSON for programmatic access
  console.log('');
  console.log('=== RESULT ===');
  console.log(JSON.stringify(result, null, 2));
  console.log('');
  console.log(`Document Title: ${title}`);
  console.log(`Document URL: ${result.url}`);
  if (result.shareLink) {
    console.log(`Share Link: ${result.shareLink}`);
  }
}

await main().catch((err) => {
  console.error(`Error: ${err instanceof Error ? err.message : String(err)}`);
  process.exit(1);
});
