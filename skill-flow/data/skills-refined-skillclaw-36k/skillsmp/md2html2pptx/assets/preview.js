#!/usr/bin/env node
/**
 * HTMLスライドプレビュー用index.html生成スクリプト
 *
 * 使い方:
 * 1. node preview.js                    # 2_htmls/ディレクトリのスライドをプレビュー
 * 2. node preview.js --dir custom_dir   # カスタムディレクトリを指定
 * 3. node preview.js --no-open          # ブラウザを開かない
 * 4. node preview.js --filter part1     # part1で始まるファイルのみ
 *
 * オプション:
 * --dir, -d     HTMLファイルのディレクトリ (デフォルト: 2_htmls)
 * --no-open     生成後にブラウザを開かない
 * --filter, -f  ファイル名フィルター
 */

const fs = require("fs");
const path = require("path");
const { exec } = require("child_process");

/**
 * コマンドライン引数をパース
 */
function parseArgs(args) {
  const result = {
    dir: "2_htmls",
    open: true,
    filter: null,
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    if (arg === "--dir" || arg === "-d") {
      result.dir = args[++i];
    } else if (arg === "--no-open") {
      result.open = false;
    } else if (arg === "--filter" || arg === "-f") {
      result.filter = args[++i];
    } else if (!arg.startsWith("-")) {
      // 引数として渡されたらフィルターとして扱う
      result.filter = arg;
    }
  }

  return result;
}

/**
 * index.htmlテンプレートを生成
 */
function generateIndexHtml(slides) {
  const slidesJson = JSON.stringify(slides);

  return `<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>スライドプレビュー</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    html, body {
      width: 100%;
      height: 100%;
      overflow: hidden;
      background: #0F172A;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .viewer {
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
    }
    .slide-container {
      position: relative;
      width: 960px;
      height: 540px;
      transform-origin: center center;
    }
    .slide-frame {
      width: 100%;
      height: 100%;
      border: none;
      border-radius: 8px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    }
    .controls {
      position: fixed;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      align-items: center;
      gap: 16px;
      background: rgba(30, 41, 59, 0.95);
      padding: 12px 24px;
      border-radius: 50px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .nav-btn {
      width: 40px;
      height: 40px;
      border: none;
      border-radius: 50%;
      background: #334155;
      color: #F8FAFC;
      font-size: 18px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s ease;
    }
    .nav-btn:hover {
      background: #0891B2;
    }
    .nav-btn:disabled {
      opacity: 0.3;
      cursor: not-allowed;
    }
    .page-info {
      color: #94A3B8;
      font-size: 14px;
      min-width: 80px;
      text-align: center;
    }
    .page-info .current {
      color: #F8FAFC;
      font-weight: 600;
      font-size: 16px;
    }
    .keyboard-hint {
      position: fixed;
      top: 24px;
      right: 24px;
      background: rgba(30, 41, 59, 0.9);
      padding: 12px 16px;
      border-radius: 8px;
      color: #94A3B8;
      font-size: 12px;
    }
    .keyboard-hint kbd {
      background: #334155;
      padding: 2px 8px;
      border-radius: 4px;
      color: #F8FAFC;
      margin: 0 4px;
    }
    /* Validation status indicator */
    .validation-status {
      position: fixed;
      top: 24px;
      left: 24px;
      display: flex;
      align-items: center;
      gap: 8px;
      background: rgba(30, 41, 59, 0.9);
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 13px;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .validation-status:hover {
      background: rgba(30, 41, 59, 1);
    }
    .validation-status.valid {
      color: #22C55E;
    }
    .validation-status.warning {
      color: #F59E0B;
    }
    .validation-status.error {
      color: #EF4444;
    }
    .validation-status .icon {
      font-size: 16px;
    }
    .validation-status .count {
      font-weight: 600;
    }
    /* Error panel */
    .error-panel {
      position: fixed;
      top: 70px;
      left: 24px;
      max-width: 500px;
      max-height: calc(100vh - 150px);
      background: rgba(30, 41, 59, 0.98);
      border-radius: 12px;
      padding: 16px;
      display: none;
      overflow-y: auto;
      box-shadow: 0 8px 32px rgba(0,0,0,0.4);
      z-index: 100;
    }
    .error-panel.show {
      display: block;
    }
    .error-panel h3 {
      color: #F8FAFC;
      font-size: 14px;
      margin-bottom: 12px;
      padding-bottom: 8px;
      border-bottom: 1px solid #334155;
    }
    .error-item {
      background: rgba(239, 68, 68, 0.1);
      border-left: 3px solid #EF4444;
      padding: 10px 12px;
      margin-bottom: 8px;
      border-radius: 0 6px 6px 0;
      font-size: 12px;
      line-height: 1.5;
      color: #F8FAFC;
    }
    .error-item:last-child {
      margin-bottom: 0;
    }
    .error-item code {
      background: rgba(0,0,0,0.3);
      padding: 2px 6px;
      border-radius: 4px;
      font-family: 'SF Mono', Monaco, monospace;
      font-size: 11px;
    }
    .error-panel .no-errors {
      color: #22C55E;
      font-size: 13px;
      text-align: center;
      padding: 20px;
    }
    /* Auto-fix button */
    .auto-fix-btn {
      background: #0891B2;
      color: #F8FAFC;
      border: none;
      padding: 8px 16px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
      margin-top: 12px;
    }
    .auto-fix-btn:hover:not(:disabled) {
      background: #0E7490;
    }
    .auto-fix-btn:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
    .auto-fix-btn .spinner {
      width: 12px;
      height: 12px;
      border: 2px solid transparent;
      border-top-color: #F8FAFC;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }
    @keyframes spin {
      to { transform: rotate(360deg); }
    }
    .error-item.overflow {
      background: rgba(239, 68, 68, 0.15);
      border-left-color: #F97316;
    }
  </style>
</head>
<body>
  <div class="viewer">
    <div class="slide-container" id="slideContainer">
      <iframe class="slide-frame" id="slideFrame"></iframe>
    </div>
  </div>

  <div class="validation-status valid" id="validationStatus" onclick="toggleErrorPanel()">
    <span class="icon" id="statusIcon">✓</span>
    <span id="statusText">検証中...</span>
  </div>

  <div class="error-panel" id="errorPanel">
    <h3 id="errorPanelTitle">制約チェック結果</h3>
    <div id="errorList"></div>
    <button class="auto-fix-btn" id="autoFixBtn" onclick="autoFix()" style="display: none;">
      <span id="autoFixIcon">🔧</span>
      <span id="autoFixText">自動補正</span>
    </button>
  </div>

  <div class="controls">
    <button class="nav-btn" id="prevBtn" onclick="prevSlide()">&#8592;</button>
    <div class="page-info">
      <span class="current" id="currentPage">1</span>
      <span>/ </span>
      <span id="totalPages">1</span>
    </div>
    <button class="nav-btn" id="nextBtn" onclick="nextSlide()">&#8594;</button>
  </div>

  <div class="keyboard-hint">
    <kbd>←</kbd><kbd>→</kbd> ページ送り <kbd>V</kbd> 検証パネル
  </div>

  <script>
    const slides = ${slidesJson};
    const SUPPORTED_TEXT_TAGS = ['P', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'UL', 'OL', 'LI'];
    const SUPPORTED_BLOCK_ELEMENTS = ['DIV', 'SECTION', 'HEADER', 'FOOTER', 'MAIN', 'ARTICLE', 'NAV', 'ASIDE'];
    const SLIDE_WIDTH = 960;
    const SLIDE_HEIGHT = 540;
    const SLIDE_PADDING_PX = 24; // 0.25 inch * 96 dpi

    let currentIndex = 0;
    let currentErrors = [];
    let overflowErrors = [];
    let errorPanelVisible = false;
    let isFixing = false;

    const slideFrame = document.getElementById('slideFrame');
    const slideContainer = document.getElementById('slideContainer');
    const currentPageEl = document.getElementById('currentPage');
    const totalPagesEl = document.getElementById('totalPages');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const validationStatus = document.getElementById('validationStatus');
    const statusIcon = document.getElementById('statusIcon');
    const statusText = document.getElementById('statusText');
    const errorPanel = document.getElementById('errorPanel');
    const errorPanelTitle = document.getElementById('errorPanelTitle');
    const errorList = document.getElementById('errorList');
    const autoFixBtn = document.getElementById('autoFixBtn');
    const autoFixIcon = document.getElementById('autoFixIcon');
    const autoFixText = document.getElementById('autoFixText');

    totalPagesEl.textContent = slides.length;

    function loadSlide(index, updateHash = true) {
      currentIndex = index;
      slideFrame.src = slides[index];
      currentPageEl.textContent = index + 1;
      prevBtn.disabled = index === 0;
      nextBtn.disabled = index === slides.length - 1;

      // Update URL hash (1-based page number for user-friendliness)
      if (updateHash) {
        const newHash = '#' + (index + 1);
        if (window.location.hash !== newHash) {
          history.pushState(null, '', newHash);
        }
      }

      // Reset validation status
      validationStatus.className = 'validation-status';
      statusIcon.textContent = '⏳';
      statusText.textContent = '検証中...';
      currentErrors = [];
      updateErrorPanel();
    }

    // Validate slide when iframe loads
    slideFrame.addEventListener('load', () => {
      setTimeout(() => validateCurrentSlide(), 100);
      // iframeからフォーカスを戻してキーボードナビゲーションを維持
      document.body.focus();
    });

    async function validateCurrentSlide() {
      try {
        const iframeDoc = slideFrame.contentDocument || slideFrame.contentWindow.document;
        const errors = [];
        overflowErrors = [];

        // Clear previous highlights
        iframeDoc.querySelectorAll('[data-overflow-highlight]').forEach(el => {
          el.style.outline = '';
          el.style.outlineOffset = '';
          el.removeAttribute('data-overflow-highlight');
        });

        // Check slide dimensions
        const body = iframeDoc.body;
        const bodyStyle = window.getComputedStyle(body);
        const bodyWidth = body.offsetWidth;
        const bodyHeight = body.offsetHeight;

        if (bodyWidth !== SLIDE_WIDTH) {
          errors.push(\`スライド幅が\${bodyWidth}pxです。960pxである必要があります。\`);
        }
        if (bodyHeight !== SLIDE_HEIGHT) {
          errors.push(\`スライド高さが\${bodyHeight}pxです。540pxである必要があります。\`);
        }

        // Check all elements
        const allElements = iframeDoc.querySelectorAll('*');
        const bodyRect = body.getBoundingClientRect();
        const overflowRect = {
          top: bodyRect.top + SLIDE_PADDING_PX,
          left: bodyRect.left + SLIDE_PADDING_PX,
          bottom: bodyRect.bottom - SLIDE_PADDING_PX,
          right: bodyRect.right - SLIDE_PADDING_PX
        };

        allElements.forEach(el => {
          const tagName = el.tagName.toUpperCase();
          const computed = iframeDoc.defaultView.getComputedStyle(el);
          const rect = el.getBoundingClientRect();

          // Skip invisible elements
          if (rect.width === 0 || rect.height === 0) return;

          // Check text wrapping rule
          if (SUPPORTED_BLOCK_ELEMENTS.includes(tagName)) {
            Array.from(el.childNodes).forEach(node => {
              if (node.nodeType === Node.TEXT_NODE) {
                const text = node.textContent?.trim();
                if (text && text.length > 0) {
                  errors.push(\`<code>&lt;\${tagName.toLowerCase()}&gt;</code> にテキスト "\${text.substring(0, 30)}\${text.length > 30 ? '...' : ''}" が直接含まれています。テキストは <code>&lt;p&gt;</code>, <code>&lt;h1&gt;</code>-<code>&lt;h6&gt;</code>, <code>&lt;ul&gt;</code>, <code>&lt;ol&gt;</code> でラップしてください。\`);
                }
              }
            });
          }

          // Check bullet prefix in p tags
          if (tagName === 'P') {
            const text = el.textContent?.trimStart() || '';
            if (/^[•\\-*▪▸○●◆◇■□]\\s/.test(text)) {
              errors.push(\`<code>&lt;p&gt;</code> が箇条書き記号で始まっています: "\${text.substring(0, 25)}..."。<code>&lt;ul&gt;</code> または <code>&lt;ol&gt;</code> を使用してください。\`);
            }
          }

          // Check styling on text elements
          if (SUPPORTED_TEXT_TAGS.includes(tagName) && tagName !== 'LI') {
            const hasBg = computed.backgroundColor && computed.backgroundColor !== 'rgba(0, 0, 0, 0)';
            const hasBorder = parseFloat(computed.borderWidth) > 0;
            const hasShadow = computed.boxShadow && computed.boxShadow !== 'none';

            if (hasBg) {
              errors.push(\`<code>&lt;\${tagName.toLowerCase()}&gt;</code> に背景色が設定されています。背景は親の <code>&lt;div&gt;</code> に設定してください。\`);
            }
            if (hasBorder) {
              errors.push(\`<code>&lt;\${tagName.toLowerCase()}&gt;</code> にボーダーが設定されています。ボーダーは親の <code>&lt;div&gt;</code> に設定してください。\`);
            }
            if (hasShadow) {
              errors.push(\`<code>&lt;\${tagName.toLowerCase()}&gt;</code> にシャドウが設定されています。シャドウは親の <code>&lt;div&gt;</code> に設定してください。\`);
            }
          }

          // Check overflow and add visual highlight
          if (SUPPORTED_TEXT_TAGS.includes(tagName) || tagName === 'IMG') {
            const edges = ['top', 'left', 'bottom', 'right'];
            let hasOverflow = false;
            edges.forEach(edge => {
              const amount = (edge === 'bottom' || edge === 'right')
                ? rect[edge] - overflowRect[edge]
                : overflowRect[edge] - rect[edge];
              if (amount > 1) {
                hasOverflow = true;
                const elemDesc = \`<code>&lt;\${tagName.toLowerCase()}&gt;</code>\` +
                  (el.className ? \` .\${el.className.split(' ')[0]}\` : '');
                const errMsg = \`\${elemDesc} がスライドの\${edge === 'top' ? '上' : edge === 'bottom' ? '下' : edge === 'left' ? '左' : '右'}端を \${Math.round(amount)}px はみ出しています。\`;
                errors.push(errMsg);
                overflowErrors.push({ element: el, edge, amount: Math.round(amount), message: errMsg });
              }
            });
            // Add red outline to overflow elements
            if (hasOverflow) {
              el.style.outline = '3px solid #EF4444';
              el.style.outlineOffset = '-3px';
              el.setAttribute('data-overflow-highlight', 'true');
            }
          }

          // Check span margin
          if (tagName === 'SPAN') {
            const marginL = parseFloat(computed.marginLeft) || 0;
            const marginR = parseFloat(computed.marginRight) || 0;
            if (marginL > 0 || marginR > 0) {
              errors.push(\`<code>&lt;span&gt;</code> にmarginが設定されています。PowerPointではspan のmarginはサポートされません。\`);
            }
          }
        });

        currentErrors = [...new Set(errors)]; // Remove duplicates
        updateValidationStatus();
        updateErrorPanel();

        // Also log to console
        if (currentErrors.length > 0) {
          console.group(\`%c⚠️ スライド \${currentIndex + 1} (\${slides[currentIndex]}) の制約違反: \${currentErrors.length}件\`, 'color: #F59E0B; font-weight: bold;');
          currentErrors.forEach((err, i) => {
            console.warn(\`\${i + 1}. \${err.replace(/<\\/?code>/g, '')}\`);
          });
          console.groupEnd();
        } else {
          console.log(\`%c✓ スライド \${currentIndex + 1} (\${slides[currentIndex]}) - 問題なし\`, 'color: #22C55E;');
        }

      } catch (e) {
        console.error('Validation error:', e);
        statusIcon.textContent = '?';
        statusText.textContent = '検証エラー';
        validationStatus.className = 'validation-status';
      }
    }

    function updateValidationStatus() {
      const count = currentErrors.length;
      if (count === 0) {
        validationStatus.className = 'validation-status valid';
        statusIcon.textContent = '✓';
        statusText.textContent = 'OK';
      } else {
        validationStatus.className = 'validation-status error';
        statusIcon.textContent = '⚠';
        statusText.textContent = \`\${count}件の警告\`;
      }
    }

    function updateErrorPanel() {
      errorPanelTitle.textContent = \`制約チェック: \${slides[currentIndex]}\`;
      if (currentErrors.length === 0) {
        errorList.innerHTML = '<div class="no-errors">✓ 問題は検出されませんでした</div>';
        autoFixBtn.style.display = 'none';
      } else {
        errorList.innerHTML = currentErrors.map(err => {
          const isOverflow = err.includes('はみ出しています');
          return \`<div class="error-item\${isOverflow ? ' overflow' : ''}">\${err}</div>\`;
        }).join('');
        // Show auto-fix button only if there are overflow errors
        autoFixBtn.style.display = overflowErrors.length > 0 ? 'flex' : 'none';
      }
    }

    // Auto-fix function: reduce font-size to fit content
    async function autoFix() {
      if (isFixing || overflowErrors.length === 0) return;

      isFixing = true;
      autoFixBtn.disabled = true;
      autoFixIcon.innerHTML = '<div class="spinner"></div>';
      autoFixText.textContent = '補正中...';

      try {
        const iframeDoc = slideFrame.contentDocument || slideFrame.contentWindow.document;
        const slideEl = iframeDoc.querySelector('.slide');
        if (!slideEl) {
          console.error('スライド要素が見つかりません');
          return;
        }

        // Get current font-size
        const computed = iframeDoc.defaultView.getComputedStyle(slideEl);
        let currentFontSize = parseFloat(computed.fontSize) || 16;
        let scale = 1.0;
        const minScale = 0.5; // Don't go below 50%
        const step = 0.05; // 5% reduction per step

        // Try reducing font-size until no overflow
        for (let i = 0; i < 10; i++) {
          scale -= step;
          if (scale < minScale) break;

          slideEl.style.fontSize = \`\${currentFontSize * scale}px\`;

          // Wait for reflow
          await new Promise(r => setTimeout(r, 50));

          // Check if overflow is fixed
          const body = iframeDoc.body;
          const bodyRect = body.getBoundingClientRect();
          const overflowRect = {
            top: bodyRect.top + SLIDE_PADDING_PX,
            left: bodyRect.left + SLIDE_PADDING_PX,
            bottom: bodyRect.bottom - SLIDE_PADDING_PX,
            right: bodyRect.right - SLIDE_PADDING_PX
          };

          let stillOverflow = false;
          iframeDoc.querySelectorAll('p, h1, h2, h3, h4, h5, h6, ul, ol, li, img').forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.width === 0 || rect.height === 0) return;
            if (rect.bottom > overflowRect.bottom + 1 ||
                rect.right > overflowRect.right + 1 ||
                rect.top < overflowRect.top - 1 ||
                rect.left < overflowRect.left - 1) {
              stillOverflow = true;
            }
          });

          if (!stillOverflow) {
            console.log(\`%c✓ 自動補正完了: フォントサイズを\${Math.round(scale * 100)}%に縮小\`, 'color: #22C55E;');
            break;
          }
        }

        // Re-validate
        await validateCurrentSlide();

      } catch (e) {
        console.error('Auto-fix error:', e);
      } finally {
        isFixing = false;
        autoFixBtn.disabled = false;
        autoFixIcon.innerHTML = '🔧';
        autoFixText.textContent = '自動補正';
      }
    }

    function toggleErrorPanel() {
      errorPanelVisible = !errorPanelVisible;
      errorPanel.classList.toggle('show', errorPanelVisible);
    }

    function nextSlide() {
      if (currentIndex < slides.length - 1) {
        loadSlide(currentIndex + 1);
      }
    }

    function prevSlide() {
      if (currentIndex > 0) {
        loadSlide(currentIndex - 1);
      }
    }

    function updateScale() {
      const viewerWidth = window.innerWidth;
      const viewerHeight = window.innerHeight - 100;
      const slideWidth = 960;
      const slideHeight = 540;

      const scaleX = viewerWidth / slideWidth;
      const scaleY = viewerHeight / slideHeight;
      const scale = Math.min(scaleX, scaleY, 1.5) * 0.9;

      slideContainer.style.transform = \`scale(\${scale})\`;
    }

    document.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight' || e.key === ' ') {
        e.preventDefault();
        nextSlide();
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault();
        prevSlide();
      } else if (e.key === 'Home') {
        e.preventDefault();
        loadSlide(0);
      } else if (e.key === 'End') {
        e.preventDefault();
        loadSlide(slides.length - 1);
      } else if (e.key === 'v' || e.key === 'V') {
        e.preventDefault();
        toggleErrorPanel();
      }
    });

    // Close error panel when clicking outside
    document.addEventListener('click', (e) => {
      if (errorPanelVisible &&
          !errorPanel.contains(e.target) &&
          !validationStatus.contains(e.target)) {
        errorPanelVisible = false;
        errorPanel.classList.remove('show');
      }
    });

    window.addEventListener('resize', updateScale);

    // Handle browser back/forward navigation
    window.addEventListener('hashchange', () => {
      const pageFromHash = getPageFromHash();
      if (pageFromHash !== currentIndex) {
        loadSlide(pageFromHash, false);
      }
    });

    // Get initial page from URL hash
    function getPageFromHash() {
      const hash = window.location.hash;
      if (hash && hash.length > 1) {
        const pageNum = parseInt(hash.substring(1), 10);
        if (!isNaN(pageNum) && pageNum >= 1 && pageNum <= slides.length) {
          return pageNum - 1; // Convert to 0-based index
        }
      }
      return 0;
    }

    // Load initial slide from hash or default to first slide
    const initialPage = getPageFromHash();
    loadSlide(initialPage);
    updateScale();

    // フォーカスをドキュメントに設定してキーボードナビゲーションを有効化
    document.body.focus();
    document.body.setAttribute('tabindex', '-1');
  </script>
</body>
</html>`;
}

/**
 * メイン処理
 */
async function main() {
  const args = parseArgs(process.argv.slice(2));

  // HTMLディレクトリを解決
  const htmlDir = path.isAbsolute(args.dir)
    ? args.dir
    : path.join(process.cwd(), args.dir);

  if (!fs.existsSync(htmlDir)) {
    console.error(`❌ ディレクトリが見つかりません: ${htmlDir}`);
    console.error("   先に to_html を実行してHTMLを生成してください。");
    process.exit(1);
  }

  console.log(`📁 ディレクトリ: ${args.dir}`);

  // HTMLファイルを取得（index.html以外）
  let files = fs.readdirSync(htmlDir)
    .filter(f => f.endsWith(".html") && f !== "index.html")
    .sort();

  if (args.filter) {
    const filterLower = args.filter.toLowerCase();
    files = files.filter(f => f.toLowerCase().includes(filterLower));
    console.log(`🔍 フィルター: ${args.filter} → ${files.length}件`);
  }

  if (files.length === 0) {
    console.error("❌ HTMLファイルが見つかりません");
    process.exit(1);
  }

  console.log(`📊 ${files.length}枚のスライドを検出`);

  // index.htmlを生成
  const indexHtml = generateIndexHtml(files);
  const indexPath = path.join(htmlDir, "index.html");

  fs.writeFileSync(indexPath, indexHtml, "utf-8");
  console.log(`✅ 生成: ${args.dir}/index.html`);

  // ブラウザで開く
  if (args.open) {
    const openCmd = process.platform === "darwin"
      ? "open"
      : process.platform === "win32"
      ? "start"
      : "xdg-open";

    console.log(`🌐 ブラウザで開きます...`);

    exec(`${openCmd} "${indexPath}"`, (error) => {
      if (error) {
        console.error(`⚠️ ブラウザを開けませんでした: ${error.message}`);
        console.log(`   手動で開いてください: ${indexPath}`);
      }
    });
  } else {
    console.log(`\n📄 プレビューファイル: ${indexPath}`);
  }
}

// 実行
main()
  .then(() => {
    console.log("\n✨ プレビュー準備完了！");
  })
  .catch((error) => {
    console.error("\n❌ エラーが発生しました:", error.message);
    process.exit(1);
  });
