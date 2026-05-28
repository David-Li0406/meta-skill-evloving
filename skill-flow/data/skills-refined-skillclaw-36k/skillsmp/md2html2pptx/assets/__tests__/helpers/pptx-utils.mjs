/**
 * PPTX テスト用ユーティリティ
 *
 * - MD → HTML → PPTX 変換
 * - PPTX 解凍・XML 取得
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import JSZip from 'jszip';
import { convertMdToHtml } from '../../to_html_core.mjs';
import { convertHtmlToPptx } from '../../to_pptx_core.mjs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export const ASSETS_DIR = path.join(__dirname, '../..');
export const TMP_DIR = path.join(__dirname, '../tmp');

/**
 * テスト用一時ディレクトリを初期化
 */
export function setupTmpDir() {
  if (fs.existsSync(TMP_DIR)) {
    fs.rmSync(TMP_DIR, { recursive: true });
  }
  fs.mkdirSync(TMP_DIR, { recursive: true });
  fs.mkdirSync(path.join(TMP_DIR, '1_mds'), { recursive: true });
  fs.mkdirSync(path.join(TMP_DIR, '2_htmls'), { recursive: true });
  fs.mkdirSync(path.join(TMP_DIR, '3_pptxs'), { recursive: true });
}

/**
 * テスト用一時ディレクトリを削除
 */
export function cleanupTmpDir() {
  if (fs.existsSync(TMP_DIR)) {
    fs.rmSync(TMP_DIR, { recursive: true });
  }
}

/**
 * MD コンテンツから PPTX を生成
 * @param {string} mdContent - Markdown コンテンツ
 * @param {string} [filename='test'] - ファイル名（拡張子なし）
 * @returns {Promise<string>} 生成された PPTX ファイルパス
 */
export async function mdToPptx(mdContent, filename = 'test') {
  const mdPath = path.join(TMP_DIR, '1_mds', `${filename}.md`);
  fs.writeFileSync(mdPath, mdContent);

  const htmlDir = path.join(TMP_DIR, '2_htmls');
  const pptxPath = path.join(TMP_DIR, '3_pptxs', 'presentation.pptx');

  // MD → HTML
  await convertMdToHtml({
    inputPath: mdPath,
    outputDir: htmlDir,
    assetsDir: ASSETS_DIR,
  });

  // HTML → PPTX
  await convertHtmlToPptx({
    slidesDir: htmlDir,
    outputPath: pptxPath,
    assetsDir: ASSETS_DIR,
  });

  return pptxPath;
}

/**
 * PPTX ファイルからスライド XML を取得
 * @param {string} pptxPath - PPTX ファイルパス
 * @param {number} [slideNum=1] - スライド番号 (1-indexed)
 * @returns {Promise<string>} スライド XML 文字列
 */
export async function getSlideXml(pptxPath, slideNum = 1) {
  const buffer = fs.readFileSync(pptxPath);
  const zip = await JSZip.loadAsync(buffer);
  const xmlFile = zip.file(`ppt/slides/slide${slideNum}.xml`);

  if (!xmlFile) {
    throw new Error(`Slide ${slideNum} not found in PPTX`);
  }

  return xmlFile.async('string');
}

/**
 * XML からテキスト内容を抽出
 * @param {string} xml - XML 文字列
 * @returns {string[]} テキスト内容の配列
 */
export function extractTexts(xml) {
  const matches = xml.match(/<a:t>([^<]*)<\/a:t>/g) || [];
  return matches.map(m => m.replace(/<\/?a:t>/g, ''));
}

/**
 * XML から図形の数をカウント
 * @param {string} xml - XML 文字列
 * @returns {number} 図形数
 */
export function countShapes(xml) {
  return (xml.match(/<p:sp>/g) || []).length;
}

/**
 * XML に特定のパターンが含まれるかチェック
 * @param {string} xml - XML 文字列
 * @param {RegExp|string} pattern - パターン
 * @returns {boolean}
 */
export function hasPattern(xml, pattern) {
  if (typeof pattern === 'string') {
    return xml.includes(pattern);
  }
  return pattern.test(xml);
}

/**
 * PPTX ファイルから画像ファイルの数をカウント
 * @param {string} pptxPath - PPTX ファイルパス
 * @returns {Promise<number>} 画像ファイル数
 */
export async function countImages(pptxPath) {
  const buffer = fs.readFileSync(pptxPath);
  const zip = await JSZip.loadAsync(buffer);
  const imageFiles = Object.keys(zip.files).filter(name =>
    name.startsWith('ppt/media/') && /\.(png|jpg|jpeg|gif|svg)$/i.test(name)
  );
  return imageFiles.length;
}

/**
 * XML から画像参照（p:pic要素）の数をカウント
 * @param {string} xml - XML 文字列
 * @returns {number} 画像参照数
 */
export function countPicElements(xml) {
  return (xml.match(/<p:pic>/g) || []).length;
}
