import fs from 'node:fs';
import path from 'node:path';
import { launchChrome, getPageSession, evaluate, sleep, type ChromeSession } from './cdp.ts';

const REDNOTE_URL = 'https://creator.xiaohongshu.com/';

async function explorePage() {
  console.log('[explore] Launching Chrome...');
  const { cdp, chrome } = await launchChrome(REDNOTE_URL, undefined);

  try {
    console.log('[explore] Waiting for manual login...');
    console.log('[explore] Please login in the browser, then press Enter to continue...');

    // Wait for user to press Enter
    await new Promise<void>((resolve) => {
      process.stdin.once('data', () => resolve());
    });

    console.log('[explore] Getting current page info...');

    const session = await getPageSession(cdp, 'xiaohongshu.com');

    // Get current URL
    const url = await evaluate<string>(session, 'window.location.href');
    console.log('[explore] Current URL:', url);

    // Get page title
    const title = await evaluate<string>(session, 'document.title');
    console.log('[explore] Page title:', title);

    // Find all input fields
    console.log('[explore] Searching for input fields...');
    const inputsInfo = await evaluate<string>(session, `
      (function() {
        const inputs = document.querySelectorAll('input, textarea, div[contenteditable="true"]');
        const results = [];
        inputs.forEach((el, idx) => {
          const tag = el.tagName.toLowerCase();
          const type = el.getAttribute('type') || 'text';
          const placeholder = el.getAttribute('placeholder') || '';
          const id = el.id || '';
          const className = el.className || '';
          const name = el.name || '';

          if (placeholder || id || name) {
            results.push({
              idx,
              tag,
              type,
              placeholder: placeholder.substring(0, 50),
              id: id.substring(0, 50),
              className: className.substring(0, 100),
              name: name.substring(0, 50)
            });
          }
        });
        return JSON.stringify(results, null, 2);
      })()
    `);

    console.log('[explore] Input fields found:');
    console.log(inputsInfo);

    // Find all buttons
    console.log('[explore] Searching for buttons...');
    const buttonsInfo = await evaluate<string>(session, `
      (function() {
        const buttons = document.querySelectorAll('button, a[role="button"]');
        const results = [];
        buttons.forEach((el, idx) => {
          const text = el.textContent?.trim().substring(0, 30) || '';
          const id = el.id || '';
          const className = el.className || '';

          if (text && (text.includes('发布') || text.includes('發布') || text.includes('提交') || text.includes('Publish') || text.includes('保存') || text.includes('下一步'))) {
            results.push({
              idx,
              text,
              id: id.substring(0, 50),
              className: className.substring(0, 100)
            });
          }
        });
        return JSON.stringify(results, null, 2);
      })()
    `);

    console.log('[explore] Action buttons found:');
    console.log(buttonsInfo);

    // Save results to file
    const outputPath = path.join(process.cwd(), 'rednote-page-analysis.json');
    fs.writeFileSync(outputPath, JSON.stringify({
      url,
      pageTitle: title,
      inputs: JSON.parse(inputsInfo),
      buttons: JSON.parse(buttonsInfo)
    }, null, 2));

    console.log(`[explore] Analysis saved to: ${outputPath}`);

    // Keep browser open for manual inspection
    console.log('[explore] Browser left open for manual inspection. Press Ctrl+C to exit.');

    await new Promise<void>((resolve) => {
      process.stdin.once('data', () => resolve());
    });

  } finally {
    cdp.close();
  }
}

explorePage().catch((err) => {
  console.error('Error:', err);
  process.exit(1);
});
