import fs from 'node:fs';
import path from 'node:path';
import { launchChrome, getPageSession, evaluate, sleep, type ChromeSession } from './cdp.ts';

const REDNOTE_PUBLISH_URL = 'https://creator.xiaohongshu.com/publish/publish';

async function deepExplore() {
  console.log('[explore] Launching Chrome...');
  const { cdp, chrome } = await launchChrome(REDNOTE_PUBLISH_URL, undefined);

  try {
    console.log('[explore] Waiting for page to fully load...');
    await sleep(15000);

    const session = await getPageSession(cdp, 'xiaohongshu.com');

    // Check if logged in
    const url = await evaluate<string>(session, 'window.location.href');
    console.log(`[explore] Current URL: ${url}`);

    if (url.includes('login')) {
      console.log('[explore] Please login in the browser window...');
      console.log('[explore] Waiting 60 seconds for login...');

      for (let i = 0; i < 60; i++) {
        await sleep(1000);
        const currentUrl = await evaluate<string>(session, 'window.location.href');
        if (!currentUrl.includes('login')) {
          console.log('[explore] Login detected!');
          break;
        }
      }

      // Navigate to publish page
      await session.cdp.send('Runtime.evaluate', {
        expression: `window.location.href = "${REDNOTE_PUBLISH_URL}"`,
      }, { sessionId: session.sessionId });

      await sleep(5000);
    }

    console.log('[explore] Waiting for React app to render...');
    await sleep(5000);

    // Deep DOM exploration
    const deepAnalysis = await evaluate<string>(session, `
      (function() {
        const result = {
          url: window.location.href,
          allElements: [],
          reactComponents: [],
          shadowDOMs: []
        };

        // Find all elements with specific class names
        const allDivs = document.querySelectorAll('div');
        allDivs.forEach((el, idx) => {
          const className = el.className || '';
          const role = el.getAttribute('role') || '';
          const placeholder = el.getAttribute('placeholder') || '';
          const contentEditable = el.getAttribute('contenteditable') || '';
          const ariaLabel = el.getAttribute('aria-label') || '';
          const id = el.id || '';
          const dataTestId = el.getAttribute('data-testid') || '';

          // Only include potentially relevant elements
          if (className.includes('input') ||
              className.includes('textarea') ||
              className.includes('editor') ||
              className.includes('title') ||
              className.includes('content') ||
              className.includes('upload') ||
              className.includes('publish') ||
              role === 'textbox' ||
              contentEditable === 'true' ||
              placeholder ||
              ariaLabel.includes('输入') ||
              ariaLabel.includes('标题') ||
              dataTestId) {

            const textContent = el.textContent?.trim().substring(0, 50) || '';

            result.allElements.push({
              idx,
              tag: el.tagName.toLowerCase(),
              id: id.substring(0, 100),
              className: className.substring(0, 200),
              role: role.substring(0, 50),
              placeholder: placeholder.substring(0, 100),
              contentEditable,
              ariaLabel: ariaLabel.substring(0, 100),
              dataTestId: dataTestId.substring(0, 100),
              textContent: textContent.substring(0, 100)
            });
          }
        });

        // Limit results
        result.allElements = result.allElements.slice(0, 100);

        return JSON.stringify(result, null, 2);
      })()
    `);

    console.log('[explore] Deep DOM analysis:');
    console.log(deepAnalysis);

    // Try to find upload buttons specifically
    const uploadAnalysis = await evaluate<string>(session, `
      (function() {
        const result = { uploadButtons: [], clickableElements: [] };

        // Find elements with "upload" in text or class
        document.querySelectorAll('*').forEach((el) => {
          const className = el.className || '';
          const text = el.textContent?.trim().substring(0, 30) || '';
          const ariaLabel = el.getAttribute('aria-label') || '';

          if (text.includes('上传') || text.includes('圖片') || text.includes('图片') ||
              ariaLabel.includes('上传') || ariaLabel.includes('圖片') ||
              className.includes('upload')) {
            result.uploadButtons.push({
              tag: el.tagName.toLowerCase(),
              text: text.substring(0, 50),
              className: className.substring(0, 100),
              ariaLabel: ariaLabel.substring(0, 100),
              clickable: el.onclick !== null || el.tagName === 'BUTTON' || el.tagName === 'A'
            });
          }
        });

        return JSON.stringify(result, null, 2);
      })()
    `);

    console.log('[explore] Upload elements:');
    console.log(uploadAnalysis);

    // Save to file
    const outputPath = path.join(process.cwd(), 'rednote-deep-analysis.json');
    fs.writeFileSync(outputPath, JSON.stringify({
      deep: JSON.parse(deepAnalysis),
      upload: JSON.parse(uploadAnalysis)
    }, null, 2));

    console.log(`[explore] Deep analysis saved to: ${outputPath}`);
    console.log('[explore] Browser left open for manual inspection.');

    await new Promise<void>(() => {});

  } finally {
    cdp.close();
  }
}

deepExplore().catch((err) => {
  console.error('Error:', err);
  process.exit(1);
});
