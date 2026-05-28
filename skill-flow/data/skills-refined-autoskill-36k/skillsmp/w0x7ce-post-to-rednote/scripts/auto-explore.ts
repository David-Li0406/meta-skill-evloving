import fs from 'node:fs';
import path from 'node:path';
import { launchChrome, getPageSession, evaluate, sleep, type ChromeSession, type CdpConnection } from './cdp.ts';

const REDNOTE_PUBLISH_URL = 'https://creator.xiaohongshu.com/publish/publish';

async function waitForElement(session: ChromeSession, selector: string, timeoutMs = 30000): Promise<boolean> {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    const found = await evaluate<boolean>(session, `!!document.querySelector('${selector}')`);
    if (found) return true;
    await sleep(500);
  }
  return false;
}

async function findPublishPage(session: ChromeSession): Promise<boolean> {
  const url = await evaluate<string>(session, 'window.location.href');
  console.log(`[analyze] Current URL: ${url}`);

  if (url.includes('publish') || url.includes('create')) {
    return true;
  }

  // Try to navigate to publish page
  console.log('[analyze] Looking for publish button...');

  const publishBtnFound = await evaluate<boolean>(session, `
    (function() {
      const buttons = document.querySelectorAll('button, a, div[role="button"]');
      for (const btn of buttons) {
        const text = btn.textContent?.trim() || '';
        if (text.includes('发布') || text.includes('發布') || text.includes('创作') || text.includes('創作') || text.includes('Publish')) {
          btn.click();
          return true;
        }
      }
      return false;
    })()
  `);

  if (publishBtnFound) {
    await sleep(3000);
    const newUrl = await evaluate<string>(session, 'window.location.href');
    console.log(`[analyze] Navigated to: ${newUrl}`);
    return newUrl.includes('publish') || newUrl.includes('create');
  }

  return false;
}

async function analyzePage() {
  console.log('[analyze] Launching Chrome...');
  const { cdp, chrome } = await launchChrome(REDNOTE_PUBLISH_URL, undefined);

  try {
    console.log('[analyze] Waiting for page to load...');
    await sleep(10000);

    const session = await getPageSession(cdp, 'xiaohongshu.com');

    // Check if logged in
    const url = await evaluate<string>(session, 'window.location.href');
    console.log(`[analyze] Current URL: ${url}`);

    if (url.includes('login')) {
      console.log('[analyze] Please login in the browser window...');
      console.log('[analyze] Waiting 30 seconds for login...');

      for (let i = 0; i < 30; i++) {
        await sleep(1000);
        const currentUrl = await evaluate<string>(session, 'window.location.href');
        if (!currentUrl.includes('login')) {
          console.log('[analyze] Login detected!');
          break;
        }
      }

      await sleep(3000);
    }

    // Find and navigate to publish page
    const onPublishPage = await findPublishPage(session);

    if (!onPublishPage) {
      console.log('[analyze] Not on publish page. Trying to navigate...');

      await session.cdp.send('Runtime.evaluate', {
        expression: `window.location.href = "${REDNOTE_PUBLISH_URL}"`,
      }, { sessionId: session.sessionId });

      await sleep(5000);
    }

    // Analyze page structure
    console.log('[analyze] Analyzing page structure...');

    const analysis = await evaluate<string>(session, `
      (function() {
        const result = {
          url: window.location.href,
          title: document.title,
          inputs: [],
          textareas: [],
          contentEditables: [],
          fileInputs: [],
          buttons: []
        };

        // Find all inputs
        document.querySelectorAll('input').forEach((el, idx) => {
          const placeholder = el.getAttribute('placeholder') || '';
          const type = el.getAttribute('type') || 'text';
          const id = el.id || '';
          const name = el.name || '';
          const className = el.className || '';

          if (placeholder || id || name) {
            result.inputs.push({
              idx,
              type,
              placeholder: placeholder.substring(0, 100),
              id: id.substring(0, 100),
              name: name.substring(0, 100),
              className: className.substring(0, 200)
            });
          }
        });

        // Find all textareas
        document.querySelectorAll('textarea').forEach((el, idx) => {
          const placeholder = el.getAttribute('placeholder') || '';
          const id = el.id || '';
          const name = el.name || '';
          const className = el.className || '';

          result.textareas.push({
            idx,
            placeholder: placeholder.substring(0, 100),
            id: id.substring(0, 100),
            name: name.substring(0, 100),
            className: className.substring(0, 200)
          });
        });

        // Find contenteditable divs
        document.querySelectorAll('div[contenteditable="true"]').forEach((el, idx) => {
          const placeholder = el.getAttribute('placeholder') || '';
          const id = el.id || '';
          const className = el.className || '';

          result.contentEditables.push({
            idx,
            placeholder: placeholder.substring(0, 100),
            id: id.substring(0, 100),
            className: className.substring(0, 200)
          });
        });

        // Find file inputs
        document.querySelectorAll('input[type="file"]').forEach((el, idx) => {
          const accept = el.getAttribute('accept') || '';
          const id = el.id || '';
          const className = el.className || '';

          result.fileInputs.push({
            idx,
            accept: accept.substring(0, 100),
            id: id.substring(0, 100),
            className: className.substring(0, 200)
          });
        });

        // Find buttons with relevant text
        document.querySelectorAll('button, a[role="button"], div[role="button"]').forEach((el, idx) => {
          const text = el.textContent?.trim().substring(0, 50) || '';
          const id = el.id || '';
          const className = el.className || '';

          if (text && (text.includes('发布') || text.includes('發布') || text.includes('提交') || text.includes('下一步') || text.includes('保存'))) {
            result.buttons.push({
              idx,
              text,
              id: id.substring(0, 100),
              className: className.substring(0, 200)
            });
          }
        });

        return JSON.stringify(result, null, 2);
      })()
    `);

    console.log('[analyze] Page analysis:');
    console.log(analysis);

    // Save to file
    const outputPath = path.join(process.cwd(), 'rednote-page-analysis.json');
    const analysisObj = JSON.parse(analysis);
    fs.writeFileSync(outputPath, JSON.stringify(analysisObj, null, 2));

    console.log(`[analyze] Analysis saved to: ${outputPath}`);
    console.log('[analyze] Browser left open for manual inspection. Press Ctrl+C to exit.');

    // Keep browser open
    await new Promise<void>(() => {});

  } finally {
    cdp.close();
  }
}

analyzePage().catch((err) => {
  console.error('Error:', err);
  process.exit(1);
});
