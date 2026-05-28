/**
 * Markdown to HTML スライド変換 コアロジック
 *
 * CLI (to_html.js) およびテストから直接インポート可能。
 */

import fs from 'fs';
import path from 'path';
import { createRequire } from 'module';

const require = createRequire(import.meta.url);

/**
 * パス解決ユーティリティ（createResolver の ESM 版）
 */
function resolvePathFromCandidates(candidates) {
  return candidates.filter(Boolean).find(fs.existsSync) || null;
}

/**
 * md2html モジュールをロード
 * @param {string} [basePath] - 探索の基準ディレクトリ（省略時は import.meta ベース）
 * @returns {{ parseMarkdown: Function, generateSlideHtml: Function, setThemeConfig: Function }}
 */
export function loadMd2html(basePath) {
  const assetsDir = basePath || path.dirname(new URL(import.meta.url).pathname);
  const md2htmlPath = resolvePathFromCandidates([
    process.env.MD2HTML_PATH,
    path.join(assetsDir, 'md2html'),
  ]);
  if (!md2htmlPath) {
    throw new Error('md2html not found. Set MD2HTML_PATH or place md2html in assets.');
  }
  const { parseMarkdown } = require(path.join(md2htmlPath, 'parser'));
  const { generateSlideHtml, setThemeConfig } = require(path.join(md2htmlPath, 'templates'));
  return { parseMarkdown, generateSlideHtml, setThemeConfig, md2htmlPath };
}

/**
 * theme.json を読み込む
 */
export function loadThemeConfig(inputPath, cwd, assetsDir) {
  const candidates = [
    inputPath ? path.join(path.dirname(inputPath), 'theme.json') : null,
    path.join(cwd, '1_mds', 'theme.json'),
    path.join(assetsDir, '1_mds', 'theme.json'),
  ].filter(Boolean);

  for (const candidate of candidates) {
    if (fs.existsSync(candidate)) {
      try {
        const content = fs.readFileSync(candidate, 'utf-8');
        return { config: JSON.parse(content), path: candidate };
      } catch (e) {
        // skip
      }
    }
  }
  return { config: null, path: null };
}

/**
 * スライド番号のゼロパディング
 */
function formatSlideNumber(num) {
  return String(num).padStart(2, '0');
}

/**
 * Markdown → HTML 変換のコア処理
 *
 * @param {Object} options
 * @param {string} options.inputPath - 入力 Markdown ファイルの絶対パス
 * @param {string} options.outputDir - 出力先ディレクトリの絶対パス
 * @param {string} [options.prefix] - ファイル名プレフィックス（省略時は入力ファイル名ベース）
 * @param {boolean} [options.dryRun=false]
 * @param {string} [options.assetsDir] - assets ディレクトリ（省略時は自動解決）
 * @returns {Promise<{ slides: Array, generated: Array }>}
 */
export async function convertMdToHtml(options) {
  const {
    inputPath,
    outputDir,
    prefix: prefixOpt,
    dryRun = false,
    assetsDir: assetsDirOpt,
  } = options;

  const assetsDir = assetsDirOpt || path.dirname(new URL(import.meta.url).pathname);
  const cwd = path.dirname(inputPath);

  // md2html ロード
  const { parseMarkdown, generateSlideHtml, setThemeConfig } = loadMd2html(assetsDir);

  // Markdown 読み込み
  if (!fs.existsSync(inputPath)) {
    throw new Error(`ファイルが見つかりません: ${inputPath}`);
  }
  const markdown = fs.readFileSync(inputPath, 'utf-8');

  // theme.json 適用
  const { config: themeConfig } = loadThemeConfig(inputPath, cwd, assetsDir);
  if (themeConfig) {
    setThemeConfig(themeConfig);
  }

  // パース
  const slides = parseMarkdown(markdown);
  if (slides.length === 0) {
    throw new Error('スライドが見つかりません');
  }

  // 出力ディレクトリ作成
  if (!dryRun && !fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // theme.css コピー
  const themeCssPath = resolvePathFromCandidates([
    path.join(cwd, 'theme.css'),
    path.join(assetsDir, 'html2pptx/playwright/theme.css'),
  ]);
  if (themeCssPath && !dryRun) {
    fs.copyFileSync(themeCssPath, path.join(outputDir, 'theme.css'));
  }

  // プレフィックス決定
  const prefix = prefixOpt !== undefined && prefixOpt !== null
    ? prefixOpt
    : `${path.basename(inputPath, path.extname(inputPath))}-`;

  // HTML 生成
  const generated = [];
  for (const slide of slides) {
    const html = generateSlideHtml(slide);
    const filename = `${prefix}${formatSlideNumber(slide.number)}.html`;
    if (!dryRun) {
      fs.writeFileSync(path.join(outputDir, filename), html, 'utf-8');
    }
    generated.push({ filename, slide });
  }

  return { slides, generated };
}
