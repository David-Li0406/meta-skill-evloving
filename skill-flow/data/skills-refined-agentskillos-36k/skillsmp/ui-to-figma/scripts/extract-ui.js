/**
 * UI 情報抽出スクリプト（Figma 形式対応版）
 *
 * chrome-devtools の evaluate_script で実行:
 *
 * evaluate_script({
 *   function: `(el) => {
 *     // ... このファイルの内容をコピー
 *   }`,
 *   args: [{ uid: "選択されたuid" }]
 * })
 *
 * または セレクタ指定:
 *
 * evaluate_script({
 *   function: `() => {
 *     const container = document.querySelector("セレクタ");
 *     // ... extractUIFromElement(container) を実行
 *   }`
 * })
 */

// =====================================================
// ユーティリティ関数
// =====================================================

/**
 * CSS の色文字列を Figma 形式 (0-1) に変換
 * @param {string} colorStr - "rgb(31, 37, 38)" or "rgba(31, 37, 38, 0.65)" or "#ffffff"
 * @returns {{ r: number, g: number, b: number, a?: number } | null}
 */
function parseCssColor(colorStr) {
  if (!colorStr || colorStr === "transparent" || colorStr === "rgba(0, 0, 0, 0)") {
    return null;
  }

  // rgba(r, g, b, a) 形式
  const rgbaMatch = colorStr.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)/);
  if (rgbaMatch) {
    const result = {
      r: Math.round((parseInt(rgbaMatch[1]) / 255) * 1000) / 1000,
      g: Math.round((parseInt(rgbaMatch[2]) / 255) * 1000) / 1000,
      b: Math.round((parseInt(rgbaMatch[3]) / 255) * 1000) / 1000,
    };
    if (rgbaMatch[4] !== undefined) {
      result.a = parseFloat(rgbaMatch[4]);
    }
    return result;
  }

  // #rrggbb or #rgb 形式
  const hexMatch = colorStr.match(/^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$/);
  if (hexMatch) {
    let hex = hexMatch[1];
    if (hex.length === 3) {
      hex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2];
    }
    return {
      r: Math.round((parseInt(hex.substring(0, 2), 16) / 255) * 1000) / 1000,
      g: Math.round((parseInt(hex.substring(2, 4), 16) / 255) * 1000) / 1000,
      b: Math.round((parseInt(hex.substring(4, 6), 16) / 255) * 1000) / 1000,
    };
  }

  return null;
}

/**
 * px 値を数値に変換
 * @param {string} value - "15px" or "1.5em" など
 * @returns {number}
 */
function parsePxValue(value) {
  if (!value) return 0;
  const match = value.match(/([\d.]+)/);
  return match ? parseFloat(match[1]) : 0;
}

/**
 * gap 値をパース（"8px" or "normal" → 数値）
 * @param {string} gap
 * @returns {number}
 */
function parseGap(gap) {
  if (!gap || gap === "normal" || gap === "auto") return 0;
  return parsePxValue(gap);
}

// =====================================================
// スタイル取得
// =====================================================

function getComputedStyles(el) {
  const styles = window.getComputedStyle(el);

  // 色を Figma 形式に変換
  const backgroundColor = parseCssColor(styles.backgroundColor);
  const color = parseCssColor(styles.color);
  const borderColor = parseCssColor(styles.borderColor);

  // サイズを数値に変換
  const width = parsePxValue(styles.width);
  const height = parsePxValue(styles.height);

  // パディングを数値に変換
  const paddingTop = parsePxValue(styles.paddingTop);
  const paddingRight = parsePxValue(styles.paddingRight);
  const paddingBottom = parsePxValue(styles.paddingBottom);
  const paddingLeft = parsePxValue(styles.paddingLeft);

  // マージンを数値に変換
  const marginTop = parsePxValue(styles.marginTop);
  const marginRight = parsePxValue(styles.marginRight);
  const marginBottom = parsePxValue(styles.marginBottom);
  const marginLeft = parsePxValue(styles.marginLeft);

  // ボーダーを数値に変換
  const borderRadius = parsePxValue(styles.borderRadius);
  const borderWidth = parsePxValue(styles.borderWidth);

  // フォントを数値に変換
  const fontSize = parsePxValue(styles.fontSize);
  const fontWeight = parseInt(styles.fontWeight) || 400;
  const lineHeight = parsePxValue(styles.lineHeight);

  // gap を数値に変換
  const gap = parseGap(styles.gap);

  // Figma layoutMode を決定
  let layoutMode = "NONE";
  if (styles.display === "flex" || styles.display === "inline-flex") {
    layoutMode = styles.flexDirection === "column" ? "VERTICAL" : "HORIZONTAL";
  }

  // Figma alignment を決定
  let primaryAxisAlignItems = "MIN";
  switch (styles.justifyContent) {
    case "flex-end":
    case "end":
      primaryAxisAlignItems = "MAX";
      break;
    case "center":
      primaryAxisAlignItems = "CENTER";
      break;
    case "space-between":
      primaryAxisAlignItems = "SPACE_BETWEEN";
      break;
  }

  let counterAxisAlignItems = "MIN";
  switch (styles.alignItems) {
    case "flex-end":
    case "end":
      counterAxisAlignItems = "MAX";
      break;
    case "center":
      counterAxisAlignItems = "CENTER";
      break;
    case "baseline":
      counterAxisAlignItems = "BASELINE";
      break;
  }

  return {
    // サイズ（数値）
    width,
    height,

    // パディング（数値）
    paddingTop,
    paddingRight,
    paddingBottom,
    paddingLeft,

    // マージン（数値）
    marginTop,
    marginRight,
    marginBottom,
    marginLeft,

    // 背景・ボーダー（Figma 形式）
    backgroundColor, // { r, g, b, a? } or null
    borderRadius,
    borderWidth,
    borderColor, // { r, g, b, a? } or null

    // レイアウト（Figma 形式）
    layoutMode, // "NONE", "HORIZONTAL", "VERTICAL"
    primaryAxisAlignItems, // "MIN", "MAX", "CENTER", "SPACE_BETWEEN"
    counterAxisAlignItems, // "MIN", "MAX", "CENTER", "BASELINE"
    gap,

    // テキスト（Figma 形式）
    fontSize,
    fontWeight,
    lineHeight,
    color, // { r, g, b, a? } or null
  };
}

// =====================================================
// メイン関数
// =====================================================

function getElementInfo(el, depth = 0) {
  if (depth > 6) return null;
  if (!el || el.nodeType !== 1) return null;

  const rect = el.getBoundingClientRect();
  const styles = getComputedStyles(el);

  // テキストコンテンツ（直接の子がテキストノードのみの場合）
  let textContent = null;
  if (el.childNodes.length >= 1) {
    const textNodes = Array.from(el.childNodes).filter((n) => n.nodeType === 3 && n.textContent.trim());
    if (textNodes.length > 0 && el.children.length === 0) {
      textContent = el.textContent.trim().substring(0, 200);
    }
  }

  const info = {
    tagName: el.tagName,
    className: (el.className.toString().split(" ")[0] || "").substring(0, 50),
    textContent,
    // 実際の描画サイズ（getBoundingClientRect から）
    actualWidth: Math.round(rect.width),
    actualHeight: Math.round(rect.height),
    styles,
    children: [],
  };

  for (const child of el.children) {
    const childInfo = getElementInfo(child, depth + 1);
    if (childInfo) info.children.push(childInfo);
  }

  return info;
}

// 要素直接指定版（引数付き evaluate_script 用）
const extractUIFromElement = (el) => {
  if (!el) return { error: "Element not found" };
  return getElementInfo(el);
};

// セレクタ指定版
const extractUIBySelector = (selector) => {
  const container = document.querySelector(selector);
  if (!container) return { error: "Element not found: " + selector };
  return getElementInfo(container);
};

// 使用例（セレクタ指定）:
// extractUIBySelector(".my-component")

// 使用例（要素直接）:
// extractUIFromElement(document.querySelector(".my-component"))
