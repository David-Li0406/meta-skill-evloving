#!/usr/bin/env bun

import * as culori from "culori";
import process from "node:process";

// ============================================================================
// Types
// ============================================================================

interface RGB {
  r: number;
  g: number;
  b: number;
}

interface Ansi16Match {
  code: number;
  name: string;
  exact: boolean;
}

interface Ansi256Match {
  code: number;
  exact: boolean;
}

interface ColorFormats {
  hex: string;
  rgb: string;
  rgbValues: RGB;
  hsl: string;
  hsv: string;
  cmyk: string;
  lab: string;
  lch: string;
  oklch: string;
  oklab: string;
  ansi: string;
  ansiBlock: string;
  ansi16: Ansi16Match;
  ansi256: Ansi256Match;
}

interface ContrastResult {
  ratio: number;
  ratioString: string;
  aa: { normalText: boolean; largeText: boolean };
  aaa: { normalText: boolean; largeText: boolean };
}

type ColorBlindnessType =
  | "protanopia"
  | "deuteranopia"
  | "tritanopia"
  | "achromatopsia";

type HarmonyType =
  | "complementary"
  | "triadic"
  | "analogous"
  | "split-complementary"
  | "split"
  | "tetradic"
  | "square"
  | "monochromatic"
  | "mono";

// ============================================================================
// Constants
// ============================================================================

const WCAG = {
  AA_NORMAL: 4.5,
  AA_LARGE: 3,
  AAA_NORMAL: 7,
  AAA_LARGE: 4.5,
} as const;

const ANSI_RESET = "\x1b[0m";
const ANSI_GREEN = "\x1b[32m";
const ANSI_RED = "\x1b[31m";

// Batch preview supported output types
const PREVIEW_TYPES = {
  // Color notations
  hex: "hex",
  rgb: "rgb",
  hsl: "hsl",
  hsv: "hsv",
  cmyk: "cmyk",
  lab: "lab",
  lch: "lch",
  oklch: "oklch",
  oklab: "oklab",
  // ANSI terminal colors
  "24bit": "24bit",
  "16": "16",
  "256": "256",
} as const;

type PreviewType = keyof typeof PREVIEW_TYPES;
const TYPES_FLAG_PREFIX = "--types=";

const ANSI_16_COLORS: readonly { name: string; rgb: RGB }[] = [
  { name: "black", rgb: { r: 0, g: 0, b: 0 } },
  { name: "red", rgb: { r: 128, g: 0, b: 0 } },
  { name: "green", rgb: { r: 0, g: 128, b: 0 } },
  { name: "yellow", rgb: { r: 128, g: 128, b: 0 } },
  { name: "blue", rgb: { r: 0, g: 0, b: 128 } },
  { name: "magenta", rgb: { r: 128, g: 0, b: 128 } },
  { name: "cyan", rgb: { r: 0, g: 128, b: 128 } },
  { name: "white", rgb: { r: 192, g: 192, b: 192 } },
  { name: "bright-black", rgb: { r: 128, g: 128, b: 128 } },
  { name: "bright-red", rgb: { r: 255, g: 0, b: 0 } },
  { name: "bright-green", rgb: { r: 0, g: 255, b: 0 } },
  { name: "bright-yellow", rgb: { r: 255, g: 255, b: 0 } },
  { name: "bright-blue", rgb: { r: 0, g: 0, b: 255 } },
  { name: "bright-magenta", rgb: { r: 255, g: 0, b: 255 } },
  { name: "bright-cyan", rgb: { r: 0, g: 255, b: 255 } },
  { name: "bright-white", rgb: { r: 255, g: 255, b: 255 } },
];

// Color blindness simulation matrices (Brettel et al. research)
const COLOR_BLINDNESS_MATRICES: Record<ColorBlindnessType, number[][]> = {
  protanopia: [
    [0.567, 0.433, 0],
    [0.558, 0.442, 0],
    [0, 0.242, 0.758],
  ],
  deuteranopia: [
    [0.625, 0.375, 0],
    [0.7, 0.3, 0],
    [0, 0.3, 0.7],
  ],
  tritanopia: [
    [0.95, 0.05, 0],
    [0, 0.433, 0.567],
    [0, 0.475, 0.525],
  ],
  achromatopsia: [
    [0.299, 0.587, 0.114],
    [0.299, 0.587, 0.114],
    [0.299, 0.587, 0.114],
  ],
};

const COLOR_BLINDNESS_LABELS: Record<ColorBlindnessType, string> = {
  protanopia: "Protanopia (red-blind)",
  deuteranopia: "Deuteranopia (green-blind)",
  tritanopia: "Tritanopia (blue-blind)",
  achromatopsia: "Achromatopsia (monochrome)",
};

// ============================================================================
// ANSI 256 Palette (generated once)
// ============================================================================

function generateAnsi256Palette(): RGB[] {
  const palette: RGB[] = [];

  // 0-15: Standard colors
  for (const color of ANSI_16_COLORS) {
    palette.push(color.rgb);
  }

  // 16-231: 6x6x6 color cube
  const levels = [0, 95, 135, 175, 215, 255];
  for (const r of levels) {
    for (const g of levels) {
      for (const b of levels) {
        palette.push({ r, g, b });
      }
    }
  }

  // 232-255: 24 grayscale shades
  for (let i = 0; i < 24; i++) {
    const gray = 8 + i * 10;
    palette.push({ r: gray, g: gray, b: gray });
  }

  return palette;
}

const ANSI_256_PALETTE = generateAnsi256Palette();

// ============================================================================
// RGB Utilities
// ============================================================================

function colorDistance(c1: RGB, c2: RGB): number {
  const dr = c1.r - c2.r;
  const dg = c1.g - c2.g;
  const db = c1.b - c2.b;
  return Math.sqrt(dr * dr + dg * dg + db * db);
}

function rgbToHex(rgb: RGB): string {
  const clampAndHex = (n: number) =>
    Math.max(0, Math.min(255, n)).toString(16).padStart(2, "0");
  return `#${clampAndHex(rgb.r)}${clampAndHex(rgb.g)}${clampAndHex(rgb.b)}`;
}

function culoriToRgb(color: culori.Color): RGB {
  const rgb = culori.rgb(color);
  return {
    r: Math.round((rgb.r ?? 0) * 255),
    g: Math.round((rgb.g ?? 0) * 255),
    b: Math.round((rgb.b ?? 0) * 255),
  };
}

function rgbToCulori(rgb: RGB): culori.Color {
  return { mode: "rgb", r: rgb.r / 255, g: rgb.g / 255, b: rgb.b / 255 };
}

function makeColorBlock(rgb: RGB): string {
  return `\x1b[48;2;${rgb.r};${rgb.g};${rgb.b}m  ${ANSI_RESET}`;
}

// ============================================================================
// ANSI Color Matching
// ============================================================================

function findClosestInPalette<T>(
  rgb: RGB,
  palette: readonly { rgb: RGB }[],
  mapper: (index: number, distance: number) => T
): T {
  let minDist = Infinity;
  let closest = 0;

  for (let i = 0; i < palette.length; i++) {
    const dist = colorDistance(rgb, palette[i].rgb);
    if (dist < minDist) {
      minDist = dist;
      closest = i;
    }
  }

  return mapper(closest, minDist);
}

function findClosestAnsi16(rgb: RGB): Ansi16Match {
  return findClosestInPalette(rgb, ANSI_16_COLORS, (index, dist) => ({
    code: index,
    name: ANSI_16_COLORS[index].name,
    exact: dist === 0,
  }));
}

function findClosestAnsi256(rgb: RGB): Ansi256Match {
  const palette256 = ANSI_256_PALETTE.map((rgb) => ({ rgb }));
  return findClosestInPalette(rgb, palette256, (index, dist) => ({
    code: index,
    exact: dist === 0,
  }));
}

function ansi16ToRgb(code: number): RGB | undefined {
  return code >= 0 && code < 16 ? ANSI_16_COLORS[code].rgb : undefined;
}

function ansi256ToRgb(code: number): RGB | undefined {
  return code >= 0 && code < 256 ? ANSI_256_PALETTE[code] : undefined;
}

// ============================================================================
// Color Parsing
// ============================================================================

function parseAnsiColor(input: string): culori.Color | undefined {
  // ANSI 16: "ansi16:9" or "ansi:9"
  const ansi16Match = input.match(/^ansi(?:16)?[:\s](\d+)$/i);
  if (ansi16Match) {
    const rgb = ansi16ToRgb(parseInt(ansi16Match[1], 10));
    return rgb ? rgbToCulori(rgb) : undefined;
  }

  // ANSI 256: "ansi256:214" or "256:214"
  const ansi256Match = input.match(/^(?:ansi)?256[:\s](\d+)$/i);
  if (ansi256Match) {
    const rgb = ansi256ToRgb(parseInt(ansi256Match[1], 10));
    return rgb ? rgbToCulori(rgb) : undefined;
  }

  // ANSI color names: "ansi:red", "ansi:bright-green"
  const ansiNameMatch = input.match(/^ansi[:\s]([a-z-]+)$/i);
  if (ansiNameMatch) {
    const name = ansiNameMatch[1].toLowerCase();
    const found = ANSI_16_COLORS.find((c) => c.name === name);
    return found ? rgbToCulori(found.rgb) : undefined;
  }

  return undefined;
}

function normalizeColorInput(input: string): string {
  let normalized = input.trim();

  // "247, 147, 26" -> "rgb(247, 147, 26)"
  if (/^\d+\s*,\s*\d+\s*,\s*\d+$/.test(normalized)) {
    return `rgb(${normalized})`;
  }

  // "oklch 0.75 0.16 55" -> "oklch(0.75 0.16 55)"
  if (/^oklch\s+[\d.]+\s+[\d.]+\s+[\d.]+$/i.test(normalized)) {
    return normalized.replace(/^oklch\s+/i, "oklch(") + ")";
  }

  // "oklab 0.75 0.05 0.15" -> "oklab(0.75 0.05 0.15)"
  if (/^oklab\s+[\d.]+\s+[\d.-]+\s+[\d.-]+$/i.test(normalized)) {
    return normalized.replace(/^oklab\s+/i, "oklab(") + ")";
  }

  return normalized;
}

function parseColor(input: string): culori.Color | undefined {
  const normalized = input.trim();

  // Try ANSI formats first
  const ansiColor = parseAnsiColor(normalized);
  if (ansiColor) return ansiColor;

  // Try standard color formats
  return culori.parse(normalizeColorInput(normalized));
}

function requireColor(input: string | undefined, argName = "color"): culori.Color {
  if (!input) {
    console.error(`Error: Please provide a ${argName} value`);
    process.exit(1);
  }

  const color = parseColor(input);
  if (!color) {
    console.error(`Error: Could not parse ${argName} "${input}"`);
    process.exit(1);
  }

  return color;
}

function requirePositiveInt(input: string | undefined, defaultValue: number, argName = "count"): number {
  if (!input) {
    return defaultValue;
  }

  const value = parseInt(input, 10);
  if (Number.isNaN(value) || value <= 0) {
    console.error(`Error: ${argName} must be a positive integer, got "${input}"`);
    process.exit(1);
  }

  return value;
}

// ============================================================================
// Color Conversion
// ============================================================================

function rgbToCmyk(rgb: RGB): { c: number; m: number; y: number; k: number } {
  const c = 1 - rgb.r / 255;
  const m = 1 - rgb.g / 255;
  const y = 1 - rgb.b / 255;
  const k = Math.min(c, m, y);

  if (k === 1) {
    return { c: 0, m: 0, y: 0, k: 100 };
  }

  return {
    c: Math.round(((c - k) / (1 - k)) * 100),
    m: Math.round(((m - k) / (1 - k)) * 100),
    y: Math.round(((y - k) / (1 - k)) * 100),
    k: Math.round(k * 100),
  };
}

function formatHsl(color: culori.Color): string {
  const hsl = culori.hsl(color);
  const h = Math.round(hsl.h ?? 0);
  const s = Math.round((hsl.s ?? 0) * 100);
  const l = Math.round((hsl.l ?? 0) * 100);
  return `hsl(${h}, ${s}%, ${l}%)`;
}

function formatHsv(color: culori.Color): string {
  const hsv = culori.hsv(color);
  const h = Math.round(hsv.h ?? 0);
  const s = Math.round((hsv.s ?? 0) * 100);
  const v = Math.round((hsv.v ?? 0) * 100);
  return `hsv(${h}, ${s}%, ${v}%)`;
}

function formatLab(color: culori.Color): string {
  const lab = culori.lab(color);
  return `lab(${Math.round(lab.l ?? 0)} ${Math.round(lab.a ?? 0)} ${Math.round(lab.b ?? 0)})`;
}

function formatLch(color: culori.Color): string {
  const lch = culori.lch(color);
  return `lch(${Math.round(lch.l ?? 0)} ${Math.round(lch.c ?? 0)} ${Math.round(lch.h ?? 0)})`;
}

function formatOklch(color: culori.Color): string {
  const oklch = culori.oklch(color);
  const l = (oklch.l ?? 0).toFixed(4);
  const c = (oklch.c ?? 0).toFixed(4);
  const h = (oklch.h ?? 0).toFixed(2);
  return `oklch(${l} ${c} ${h})`;
}

function formatOklab(color: culori.Color): string {
  const oklab = culori.oklab(color);
  const l = (oklab.l ?? 0).toFixed(4);
  const a = (oklab.a ?? 0).toFixed(4);
  const b = (oklab.b ?? 0).toFixed(4);
  return `oklab(${l} ${a} ${b})`;
}

function convertToAllFormats(color: culori.Color): ColorFormats {
  const rgb = culoriToRgb(color);
  const hex = rgbToHex(rgb);
  const cmyk = rgbToCmyk(rgb);

  return {
    hex,
    rgb: `rgb(${rgb.r}, ${rgb.g}, ${rgb.b})`,
    rgbValues: rgb,
    hsl: formatHsl(color),
    hsv: formatHsv(color),
    cmyk: `cmyk(${cmyk.c}%, ${cmyk.m}%, ${cmyk.y}%, ${cmyk.k}%)`,
    lab: formatLab(color),
    lch: formatLch(color),
    oklch: formatOklch(color),
    oklab: formatOklab(color),
    ansi: `\\x1b[48;2;${rgb.r};${rgb.g};${rgb.b}m  \\x1b[0m`,
    ansiBlock: makeColorBlock(rgb),
    ansi16: findClosestAnsi16(rgb),
    ansi256: findClosestAnsi256(rgb),
  };
}

// ============================================================================
// Color Harmonies
// ============================================================================

function rotateHue(color: culori.Color, degrees: number): culori.Color {
  const hsl = culori.hsl(color);
  return {
    mode: "hsl",
    h: ((hsl.h ?? 0) + degrees + 360) % 360,
    s: hsl.s ?? 0,
    l: hsl.l ?? 0,
  };
}

function createMonochromatic(color: culori.Color): culori.Color[] {
  const hsl = culori.hsl(color);
  const lightnesses = [0.2, 0.35, 0.5, 0.65, 0.8];
  return lightnesses.map((l) => ({
    mode: "hsl" as const,
    h: hsl.h ?? 0,
    s: hsl.s ?? 0,
    l,
  }));
}

const HARMONY_CONFIGS: Record<
  HarmonyType,
  { name: string; rotations?: number[]; custom?: (c: culori.Color) => culori.Color[] }
> = {
  complementary: { name: "Complementary", rotations: [0, 180] },
  triadic: { name: "Triadic", rotations: [0, 120, 240] },
  analogous: { name: "Analogous", rotations: [-30, 0, 30] },
  "split-complementary": { name: "Split-Complementary", rotations: [0, 150, 210] },
  split: { name: "Split-Complementary", rotations: [0, 150, 210] },
  tetradic: { name: "Tetradic (Square)", rotations: [0, 90, 180, 270] },
  square: { name: "Tetradic (Square)", rotations: [0, 90, 180, 270] },
  monochromatic: { name: "Monochromatic", custom: createMonochromatic },
  mono: { name: "Monochromatic", custom: createMonochromatic },
};

const VALID_HARMONY_TYPES = Object.keys(HARMONY_CONFIGS).join(", ");

function getHarmony(
  color: culori.Color,
  type: string
): { name: string; colors: culori.Color[] } {
  const config = HARMONY_CONFIGS[type.toLowerCase() as HarmonyType];

  if (!config) {
    console.error(`Error: Unknown harmony type "${type}"`);
    console.error(`Valid types: ${VALID_HARMONY_TYPES}`);
    process.exit(1);
  }

  if (config.custom) {
    return { name: config.name, colors: config.custom(color) };
  }

  const colors = config.rotations!.map((deg) => rotateHue(color, deg));
  return { name: config.name, colors };
}

// ============================================================================
// Tints & Shades
// ============================================================================

function generateLightnessVariations(
  color: culori.Color,
  count: number,
  direction: "lighter" | "darker"
): culori.Color[] {
  const hsl = culori.hsl(color);
  const baseL = hsl.l ?? 0.5;

  const range = direction === "lighter" ? 1 - baseL : baseL;
  const step = range / (count + 1);
  const sign = direction === "lighter" ? 1 : -1;

  return Array.from({ length: count }, (_, i) => ({
    mode: "hsl" as const,
    h: hsl.h ?? 0,
    s: hsl.s ?? 0,
    l: baseL + sign * step * (i + 1),
  }));
}

const generateTints = (color: culori.Color, count: number) =>
  generateLightnessVariations(color, count, "lighter");

const generateShades = (color: culori.Color, count: number) =>
  generateLightnessVariations(color, count, "darker");

// ============================================================================
// Accessibility
// ============================================================================

function getLuminance(rgb: RGB): number {
  const normalize = (channel: number) => {
    const sRGB = channel / 255;
    return sRGB <= 0.03928 ? sRGB / 12.92 : ((sRGB + 0.055) / 1.055) ** 2.4;
  };

  return 0.2126 * normalize(rgb.r) + 0.7152 * normalize(rgb.g) + 0.0722 * normalize(rgb.b);
}

function getContrastRatio(rgb1: RGB, rgb2: RGB): number {
  const l1 = getLuminance(rgb1);
  const l2 = getLuminance(rgb2);
  const [lighter, darker] = l1 > l2 ? [l1, l2] : [l2, l1];
  return (lighter + 0.05) / (darker + 0.05);
}

function checkContrast(color1: culori.Color, color2: culori.Color): ContrastResult {
  const ratio = getContrastRatio(culoriToRgb(color1), culoriToRgb(color2));

  return {
    ratio,
    ratioString: `${ratio.toFixed(2)}:1`,
    aa: {
      normalText: ratio >= WCAG.AA_NORMAL,
      largeText: ratio >= WCAG.AA_LARGE,
    },
    aaa: {
      normalText: ratio >= WCAG.AAA_NORMAL,
      largeText: ratio >= WCAG.AAA_LARGE,
    },
  };
}

// ============================================================================
// Color Blindness Simulation
// ============================================================================

function applyMatrix(rgb: RGB, matrix: number[][]): RGB {
  const clamp = (n: number) => Math.max(0, Math.min(255, Math.round(n)));
  return {
    r: clamp(matrix[0][0] * rgb.r + matrix[0][1] * rgb.g + matrix[0][2] * rgb.b),
    g: clamp(matrix[1][0] * rgb.r + matrix[1][1] * rgb.g + matrix[1][2] * rgb.b),
    b: clamp(matrix[2][0] * rgb.r + matrix[2][1] * rgb.g + matrix[2][2] * rgb.b),
  };
}

function simulateColorBlindness(rgb: RGB, type: ColorBlindnessType): RGB {
  return applyMatrix(rgb, COLOR_BLINDNESS_MATRICES[type]);
}

// ============================================================================
// Output Formatting
// ============================================================================

function passFailIcon(passed: boolean): string {
  return passed ? `${ANSI_GREEN}✓${ANSI_RESET}` : `${ANSI_RED}✗${ANSI_RESET}`;
}

function printColorFormats(formats: ColorFormats): void {
  const approx16 = formats.ansi16.exact ? "" : " (approx)";
  const approx256 = formats.ansi256.exact ? "" : " (approx)";

  console.log(`\n${formats.ansiBlock} Color Conversion Results\n`);
  console.log(`  HEX:      ${formats.hex}`);
  console.log(`  RGB:      ${formats.rgb}`);
  console.log(`  HSL:      ${formats.hsl}`);
  console.log(`  HSV:      ${formats.hsv}`);
  console.log(`  CMYK:     ${formats.cmyk}`);
  console.log(`  LAB:      ${formats.lab}`);
  console.log(`  LCH:      ${formats.lch}`);
  console.log(`  oklch:    ${formats.oklch}`);
  console.log(`  oklab:    ${formats.oklab}`);
  console.log();
  console.log(`  ANSI 24b: ${formats.ansiBlock} ${formats.ansi}`);
  console.log(
    `  ANSI 16:  ${makeColorBlock(ANSI_16_COLORS[formats.ansi16.code].rgb)} ${formats.ansi16.code} (${formats.ansi16.name})${approx16}`
  );
  console.log(
    `  ANSI 256: ${makeColorBlock(ANSI_256_PALETTE[formats.ansi256.code])} ${formats.ansi256.code}${approx256}`
  );
  console.log();
}

function printHarmony(
  baseFormats: ColorFormats,
  harmony: { name: string; colors: culori.Color[] }
): void {
  console.log(`\n${baseFormats.ansiBlock} ${harmony.name} Harmony\n`);

  for (const c of harmony.colors) {
    const f = convertToAllFormats(c);
    console.log(`  ${f.ansiBlock} ${f.hex}  ${f.rgb}`);
  }
  console.log();
}

function printPalette(label: string, colors: culori.Color[], baseFormats: ColorFormats): void {
  console.log(`\n${baseFormats.ansiBlock} ${label}\n`);

  for (const c of colors) {
    const f = convertToAllFormats(c);
    console.log(`  ${f.ansiBlock} ${f.hex}`);
  }
  console.log();
}

function printContrast(formats1: ColorFormats, formats2: ColorFormats, result: ContrastResult): void {
  console.log(`\n${formats1.ansiBlock} vs ${formats2.ansiBlock} Contrast Check\n`);
  console.log(`  Ratio: ${result.ratioString}`);
  console.log();
  console.log(`  WCAG AA:`);
  console.log(`    Normal Text (≥${WCAG.AA_NORMAL}:1): ${passFailIcon(result.aa.normalText)}`);
  console.log(`    Large Text  (≥${WCAG.AA_LARGE}:1):   ${passFailIcon(result.aa.largeText)}`);
  console.log();
  console.log(`  WCAG AAA:`);
  console.log(`    Normal Text (≥${WCAG.AAA_NORMAL}:1):   ${passFailIcon(result.aaa.normalText)}`);
  console.log(`    Large Text  (≥${WCAG.AAA_LARGE}:1): ${passFailIcon(result.aaa.largeText)}`);
  console.log();
}

function printColorBlindness(formats: ColorFormats): void {
  const rgb = formats.rgbValues;
  const types: ColorBlindnessType[] = ["protanopia", "deuteranopia", "tritanopia", "achromatopsia"];

  console.log(`\n${formats.ansiBlock} Color Blindness Simulation\n`);
  console.log(`  Original: ${formats.ansiBlock} ${formats.hex}\n`);

  for (const type of types) {
    const simulated = simulateColorBlindness(rgb, type);
    console.log(`  ${COLOR_BLINDNESS_LABELS[type]}:`);
    console.log(`    ${makeColorBlock(simulated)} ${rgbToHex(simulated)}`);
    console.log();
  }
}

// ============================================================================
// Terminal Capability Detection
// ============================================================================

interface TerminalCapability {
  trueColor: boolean;
  color256: boolean;
  color16: boolean;
  noColor: boolean;
  term: string;
  colorTerm: string;
  detected: "truecolor" | "256" | "16" | "none";
}

function detectTerminalCapability(): TerminalCapability {
  const term = process.env.TERM ?? "";
  const colorTerm = process.env.COLORTERM ?? "";
  const noColor = !!process.env.NO_COLOR;

  // Check for true color support
  const trueColor =
    colorTerm === "truecolor" ||
    colorTerm === "24bit" ||
    term.includes("truecolor") ||
    term.includes("24bit") ||
    // Common terminals known to support true color
    term.includes("kitty") ||
    term.includes("iterm") ||
    term.includes("alacritty") ||
    // Some terminals report as xterm but support true color via COLORTERM
    (term.includes("xterm") && colorTerm !== "");

  // Check for 256 color support
  const color256 =
    term.includes("256color") ||
    term.includes("256") ||
    colorTerm.includes("256") ||
    trueColor; // true color implies 256 color support

  // Check for basic 16 color support (most terminals support this)
  const color16 =
    term !== "" &&
    term !== "dumb" &&
    !noColor;

  // Determine the best detected capability
  let detected: "truecolor" | "256" | "16" | "none";
  if (noColor) {
    detected = "none";
  } else if (trueColor) {
    detected = "truecolor";
  } else if (color256) {
    detected = "256";
  } else if (color16) {
    detected = "16";
  } else {
    detected = "none";
  }

  return {
    trueColor,
    color256,
    color16,
    noColor,
    term,
    colorTerm,
    detected,
  };
}

// ============================================================================
// Batch Preview Helpers
// ============================================================================

interface BatchPreviewArgs {
  types: Set<PreviewType>;
  colors: string[];
}

function parseBatchPreviewArgs(args: string[]): BatchPreviewArgs {
  const defaultTypes = new Set<PreviewType>(["24bit"]);
  const colors: string[] = [];
  let types: Set<PreviewType> | null = null;

  for (const arg of args) {
    if (arg.startsWith(TYPES_FLAG_PREFIX)) {
      const typeList = arg.slice(TYPES_FLAG_PREFIX.length).split(",").map((t) => t.trim());
      types = new Set(typeList.filter((t) => t in PREVIEW_TYPES) as PreviewType[]);
    } else {
      colors.push(arg);
    }
  }

  return { types: types ?? defaultTypes, colors };
}

function formatPreviewPart(type: PreviewType, formats: ColorFormats): string {
  switch (type) {
    case "24bit":
      return `${formats.ansiBlock} ${formats.hex}`;
    case "16": {
      const approx = formats.ansi16.exact ? "" : "~";
      return `16: ${makeColorBlock(ANSI_16_COLORS[formats.ansi16.code].rgb)} ${formats.ansi16.code}${approx}`;
    }
    case "256": {
      const approx = formats.ansi256.exact ? "" : "~";
      return `256: ${makeColorBlock(ANSI_256_PALETTE[formats.ansi256.code])} ${formats.ansi256.code}${approx}`;
    }
    case "hex":
      return formats.hex;
    case "rgb":
      return formats.rgb;
    case "hsl":
      return formats.hsl;
    case "hsv":
      return formats.hsv;
    case "cmyk":
      return formats.cmyk;
    case "lab":
      return formats.lab;
    case "lch":
      return formats.lch;
    case "oklch":
      return formats.oklch;
    case "oklab":
      return formats.oklab;
    default:
      return "";
  }
}

function formatBatchPreviewLine(input: string, types: Set<PreviewType>): string {
  const color = parseColor(input);
  if (!color) {
    return `  ${ANSI_RED}??${ANSI_RESET} (invalid)  ← ${input}`;
  }

  const formats = convertToAllFormats(color);
  const parts: string[] = [];

  for (const type of types) {
    const part = formatPreviewPart(type, formats);
    if (part) parts.push(part);
  }

  return `  ${parts.join("  |  ")}  ← ${input}`;
}

// ============================================================================
// CLI Commands
// ============================================================================

const commands = {
  convert(args: string[]): void {
    const color = requireColor(args[0]);
    printColorFormats(convertToAllFormats(color));
  },

  harmony(args: string[]): void {
    const color = requireColor(args[0]);
    const harmonyType = args[1] ?? "complementary";
    const formats = convertToAllFormats(color);
    printHarmony(formats, getHarmony(color, harmonyType));
  },

  tints(args: string[]): void {
    const color = requireColor(args[0]);
    const count = requirePositiveInt(args[1], 5);
    const formats = convertToAllFormats(color);
    printPalette("Tints (lighter)", generateTints(color, count), formats);
  },

  shades(args: string[]): void {
    const color = requireColor(args[0]);
    const count = requirePositiveInt(args[1], 5);
    const formats = convertToAllFormats(color);
    printPalette("Shades (darker)", generateShades(color, count), formats);
  },

  palette(args: string[]): void {
    const color = requireColor(args[0]);
    const count = requirePositiveInt(args[1], 10);
    const formats = convertToAllFormats(color);

    const half = Math.floor(count / 2);
    const shades = generateShades(color, half).reverse();
    const tints = generateTints(color, count - half);

    console.log(`\n${formats.ansiBlock} Full Palette\n`);
    console.log("  Shades (darker):");
    for (const c of shades) {
      const f = convertToAllFormats(c);
      console.log(`    ${f.ansiBlock} ${f.hex}`);
    }
    console.log(`\n  Base: ${formats.ansiBlock} ${formats.hex}\n`);
    console.log("  Tints (lighter):");
    for (const c of tints) {
      const f = convertToAllFormats(c);
      console.log(`    ${f.ansiBlock} ${f.hex}`);
    }
    console.log();
  },

  contrast(args: string[]): void {
    const color1 = requireColor(args[0], "first color");
    const color2 = requireColor(args[1], "second color");
    printContrast(
      convertToAllFormats(color1),
      convertToAllFormats(color2),
      checkContrast(color1, color2)
    );
  },

  colorblind(args: string[]): void {
    const color = requireColor(args[0]);
    printColorBlindness(convertToAllFormats(color));
  },

  preview(args: string[]): void {
    const color = requireColor(args[0]);
    const formats = convertToAllFormats(color);
    console.log(`\n  ${formats.ansiBlock} ${formats.hex}\n`);
  },

  "batch-preview"(args: string[]): void {
    const { types, colors } = parseBatchPreviewArgs(args);

    if (colors.length === 0) {
      const validTypes = Object.keys(PREVIEW_TYPES).join(",");
      console.error("Error: Please provide at least one color value");
      console.error(`Usage: batch-preview [${TYPES_FLAG_PREFIX}${validTypes}] <color1> <color2> ...`);
      process.exit(1);
    }

    console.log();
    for (const input of colors) {
      const output = formatBatchPreviewLine(input, types);
      console.log(output);
    }
    console.log();
  },

  terminfo(): void {
    const cap = detectTerminalCapability();

    console.log("\n  Terminal Color Capability\n");
    console.log(`  TERM:       ${cap.term || "(not set)"}`);
    console.log(`  COLORTERM:  ${cap.colorTerm || "(not set)"}`);
    console.log(`  NO_COLOR:   ${cap.noColor ? "yes" : "no"}`);
    console.log();
    console.log(`  Capabilities:`);
    console.log(`    True Color (24-bit): ${passFailIcon(cap.trueColor)}`);
    console.log(`    256 Colors:          ${passFailIcon(cap.color256)}`);
    console.log(`    16 Colors:           ${passFailIcon(cap.color16)}`);
    console.log();
    console.log(`  Detected: ${cap.detected}`);
    console.log();

    // Show sample colors based on detected capability
    if (cap.detected !== "none") {
      console.log("  Sample colors:");
      const sampleRgb = { r: 247, g: 147, b: 26 }; // Bitcoin orange

      if (cap.trueColor) {
        console.log(`    24-bit: ${makeColorBlock(sampleRgb)} #f7931a`);
      }
      if (cap.color256) {
        const ansi256 = findClosestAnsi256(sampleRgb);
        console.log(
          `    256:    ${makeColorBlock(ANSI_256_PALETTE[ansi256.code])} ANSI 256 code ${ansi256.code}`
        );
      }
      if (cap.color16) {
        const ansi16 = findClosestAnsi16(sampleRgb);
        console.log(
          `    16:     ${makeColorBlock(ANSI_16_COLORS[ansi16.code].rgb)} ANSI 16 code ${ansi16.code} (${ansi16.name})`
        );
      }
      console.log();
    }
  },

  help(): void {
    console.log(`
Color Master - Color utility tool

Usage:
  bun run scripts/color.ts <command> <args>

Commands:
  convert <color>                    Convert color to all formats
  harmony <color> <type>             Generate color harmony
  tints <color> [count]              Generate lighter variations (default: 5)
  shades <color> [count]             Generate darker variations (default: 5)
  palette <color> [count]            Generate full palette (default: 10)
  contrast <color1> <color2>         Check WCAG contrast ratio
  colorblind <color>                 Simulate color blindness
  preview <color>                    Show color block in terminal
  batch-preview [--types=...] <colors>  Preview multiple colors
                                     types: 24bit,16,256,hex,rgb,hsl,hsv,
                                            cmyk,lab,lch,oklch,oklab
  terminfo                           Detect terminal color capability

Harmony types:
  complementary, triadic, analogous, split-complementary, tetradic, monochromatic

Examples:
  bun run scripts/color.ts convert "#f7931a"
  bun run scripts/color.ts harmony "#f7931a" triadic
  bun run scripts/color.ts contrast "#f7931a" "#ffffff"
  bun run scripts/color.ts colorblind "rgb(247, 147, 26)"
`);
  },
};

// ============================================================================
// Main Entry
// ============================================================================

function main(): void {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    commands.help();
    return;
  }

  const commandName = args[0].toLowerCase();
  const commandArgs = args.slice(1);

  // Handle aliases
  const aliases: Record<string, keyof typeof commands> = {
    "-h": "help",
    "--help": "help",
  };

  const resolvedCommand = aliases[commandName] ?? commandName;
  const handler = commands[resolvedCommand as keyof typeof commands];

  if (!handler) {
    console.error(`Error: Unknown command "${commandName}"`);
    commands.help();
    process.exit(1);
  }

  handler(commandArgs);
}

main();
