//#region rolldown:runtime
var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __copyProps = (to, from, except, desc) => {
	if (from && typeof from === "object" || typeof from === "function") for (var keys = __getOwnPropNames(from), i = 0, n = keys.length, key; i < n; i++) {
		key = keys[i];
		if (!__hasOwnProp.call(to, key) && key !== except) __defProp(to, key, {
			get: ((k) => from[k]).bind(null, key),
			enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable
		});
	}
	return to;
};
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", {
	value: mod,
	enumerable: true
}) : target, mod));

//#endregion
let playwright = require("playwright");
let path = require("path");
path = __toESM(path);
let node_path = require("node:path");
let node_fs = require("node:fs");
let crypto = require("crypto");
crypto = __toESM(crypto);
let sharp = require("sharp");
sharp = __toESM(sharp);
let fs_promises = require("fs/promises");
let node_url = require("node:url");
let http = require("http");

//#region src/constants.ts
/**
* Shared constants used throughout html2pptx
*/
const PT_PER_PX = 1.0;  // 24px → 24pt (HTML表示とPPTX表示を近づけるため)
const PX_PER_IN = 96;
const EMU_PER_IN = 914400;

//#endregion
//#region src/validation.ts
/**
* Get body dimensions and check for overflow
*/
async function getBodyDimensions(page) {
	const initialDimensions = await page.evaluate(() => {
		const body = document.body;
		const style = window.getComputedStyle(body);
		return {
			width: parseFloat(style.width),
			height: parseFloat(style.height)
		};
	});
	await page.setViewportSize({
		width: Math.round(initialDimensions.width),
		height: Math.round(initialDimensions.height)
	});
	const bodyDimensions = await page.evaluate(() => {
		const body = document.body;
		const style = window.getComputedStyle(body);
		return {
			width: parseFloat(style.width),
			height: parseFloat(style.height),
			scrollWidth: body.scrollWidth,
			scrollHeight: body.scrollHeight
		};
	});
	const errors = [];
	const widthOverflowPx = Math.max(0, bodyDimensions.scrollWidth - bodyDimensions.width - 1);
	const heightOverflowPx = Math.max(0, bodyDimensions.scrollHeight - bodyDimensions.height - 1);
	const widthOverflowPt = widthOverflowPx * PT_PER_PX;
	const heightOverflowPt = heightOverflowPx * PT_PER_PX;
	if (widthOverflowPt > 0 || heightOverflowPt > 0) {
		const directions = [];
		if (widthOverflowPt > 0) directions.push(`${widthOverflowPt.toFixed(1)}pt horizontally`);
		if (heightOverflowPt > 0) directions.push(`${heightOverflowPt.toFixed(1)}pt vertically`);
		const reminder = heightOverflowPt > 0 ? " (Remember: leave 0.5\" margin at bottom of slide)" : "";
		errors.push(`HTML content overflows body by ${directions.join(" and ")}${reminder}`);
	}
	return {
		...bodyDimensions,
		errors
	};
}
/**
* Validate dimensions match presentation layout
*/
function validateDimensions(bodyDimensions, pres) {
	const errors = [];
	const widthInches = bodyDimensions.width / PX_PER_IN;
	const heightInches = bodyDimensions.height / PX_PER_IN;
	if (pres.presLayout) {
		const layoutWidth = pres.presLayout.width / EMU_PER_IN;
		const layoutHeight = pres.presLayout.height / EMU_PER_IN;
		if (Math.abs(layoutWidth - widthInches) > .1 || Math.abs(layoutHeight - heightInches) > .1) errors.push(`HTML dimensions (${widthInches.toFixed(1)}" × ${heightInches.toFixed(1)}") don't match presentation layout (${layoutWidth.toFixed(1)}" × ${layoutHeight.toFixed(1)}")`);
	}
	return errors;
}
/**
* Validate text box positions are not too close to bottom edge
*/
function validateTextBoxPosition(slideData, bodyDimensions) {
	const errors = [];
	const slideHeightInches = bodyDimensions.height / PX_PER_IN;
	const minBottomMargin = .5;
	for (const el of slideData.elements) if ([
		"p",
		"h1",
		"h2",
		"h3",
		"h4",
		"h5",
		"h6",
		"list"
	].includes(el.type)) {
		if (el.type === "line" || el.type === "image" || el.type === "rasterized-image" || el.type === "shape") continue;
		const fontSize = el.style?.fontSize || 0;
		const distanceFromBottom = slideHeightInches - (el.position.y + el.position.h);
		if (fontSize > 10.5 && distanceFromBottom < minBottomMargin) {
			const getText = () => {
				if (el.type === "list") return el.items.find((item) => item.text)?.text || "";
				if (typeof el.text === "string") return el.text;
				if (Array.isArray(el.text)) return el.text.find((t) => t.text)?.text || "";
				return "";
			};
			const textPrefix = getText().substring(0, 50) + (getText().length > 50 ? "..." : "");
			errors.push(`Text box "${textPrefix}" ends too close to bottom edge (${distanceFromBottom.toFixed(2)}" from bottom, minimum ${minBottomMargin}" required)`);
		}
	}
	return errors;
}

//#endregion
//#region src/rasterizeUtils.ts
/**
* Get the CSS style rules for a specific rasterization type
* This determines what elements are visible during screenshot and how they're styled
*/
function getStyleForRasterizationType(rasterizationType, rasterizeId) {
	const baseStyle = `
    html, body {background: transparent;}
    * {visibility: hidden;}
  `;
	switch (rasterizationType) {
		case "svg": return baseStyle + `svg, svg * {visibility: visible;}`;
		case "canvas": return baseStyle + `canvas {visibility: visible;}`;
		case "gradient": return baseStyle + `[data-rasterize="${rasterizeId}"] {
          visibility: visible;
          box-shadow: none;
        }`;
		default: return baseStyle + `svg, canvas, [data-rasterize] {visibility: visible;}
        svg *, canvas, [data-rasterize] * {visibility: visible;}`;
	}
}
/**
* Capture screenshots of all marked elements (SVG, canvas, or gradient backgrounds)
* Updates the SlideData in place, setting the src property on rasterized-image elements
* Different element types receive different styling to ensure proper rendering
*/
async function rasterizeMarkedElements(page, slideData, tmpDir) {
	const rasterizedElements = slideData.elements.filter((el) => el.type === "rasterized-image");
	if (rasterizedElements.length === 0) return;
	for (const element of rasterizedElements) {
		const rasterizeId = element.rasterizeId;
		const rasterizationType = element.rasterizationType;
		try {
			const locator = page.locator(`[data-rasterize="${rasterizeId}"]`);
			if (await locator.count() === 0) throw new Error(`Element with data-rasterize="${rasterizeId}" not found in page`);
			const hash = crypto.default.createHash("md5").update(`${rasterizeId}-${Date.now()}`).digest("hex").substring(0, 8);
			const outputPath = path.default.join(tmpDir, `rasterized-${rasterizationType}-${hash}.png`);
			await locator.screenshot({
				path: outputPath,
				type: "png",
				scale: "device",
				animations: "disabled",
				omitBackground: true,
				style: getStyleForRasterizationType(rasterizationType, rasterizeId)
			});
			element.src = outputPath;
		} catch (error) {
			throw new Error(`Failed to rasterize ${rasterizationType} element with id "${rasterizeId}": ${error instanceof Error ? error.message : String(error)}`);
		}
	}
}

//#endregion
//#region src/extraction.ts
/**
* Extract slide data from HTML page
* This function runs in the browser context using helpers from the bundled ExtractSlideData
*/
async function extractSlideData(page, tmpDir, htmlFile) {
	const slideData = await page.evaluate(() => {
		const { ExtractSlideData } = window;
		return ExtractSlideData.extractSlideDataInBrowser();
	});
	await rasterizeMarkedElements(page, slideData, tmpDir);
	let baseName;
	if (htmlFile) {
		const { name } = (0, node_path.parse)(htmlFile);
		baseName = name;
	} else baseName = "html2pptx";
	baseName += `-${Date.now()}`;
	const screenshotPath = (0, node_path.join)(tmpDir, `${baseName}.png`);
	await page.screenshot({
		path: screenshotPath,
		fullPage: true
	});
	slideData.screenshot = screenshotPath;
	(0, node_fs.writeFileSync)((0, node_path.join)(tmpDir, `${baseName}.html`), slideData.html, "utf-8");
	return slideData;
}

//#endregion
//#region src/gradientUtils.ts
/**
* Gradient utility functions for parsing CSS gradients and generating SVG
*/
/**
* Parse a CSS gradient string and generate an SVG representation
* Supports linear-gradient and radial-gradient
*/
function gradientToSVG(gradientStr, width, height) {
	const linearMatch = gradientStr.match(/linear-gradient\(\s*([^,]+),\s*(.+)\)/i);
	if (linearMatch) return generateLinearGradientSVG(parseAngle(linearMatch[1]), parseColorStops(linearMatch[2]), width, height);
	const radialMatch = gradientStr.match(/radial-gradient\(\s*(?:circle|ellipse)?\s*(?:at\s+([^,]+))?,\s*(.+)\)/i);
	if (radialMatch) return generateRadialGradientSVG(radialMatch[1] || "center", parseColorStops(radialMatch[2]), width, height);
	return null;
}
/**
* Parse angle from gradient string (e.g., "135deg", "to bottom right")
*/
function parseAngle(angleStr) {
	angleStr = angleStr.trim();
	if (angleStr.startsWith("to ")) {
		const direction = angleStr.slice(3).trim();
		return {
			top: 0,
			right: 90,
			bottom: 180,
			left: 270,
			"top right": 45,
			"right top": 45,
			"bottom right": 135,
			"right bottom": 135,
			"bottom left": 225,
			"left bottom": 225,
			"top left": 315,
			"left top": 315
		}[direction] || 180;
	}
	const degMatch = angleStr.match(/([\d.]+)deg/);
	if (degMatch) return parseFloat(degMatch[1]);
	return 180;
}
/**
* Parse color stops from gradient string
* e.g., "#667eea 0%, #764ba2 100%"
*/
function parseColorStops(stopsStr) {
	const stops = [];
	const parts = [];
	let current = "";
	let parenDepth = 0;
	for (let i = 0; i < stopsStr.length; i++) {
		const char = stopsStr[i];
		if (char === "(") parenDepth++;
		if (char === ")") parenDepth--;
		if (char === "," && parenDepth === 0) {
			parts.push(current.trim());
			current = "";
		} else current += char;
	}
	if (current.trim()) parts.push(current.trim());
	parts.forEach((part, idx) => {
		const match = part.match(/^(.+?)\s*([\d.]+%)?$/);
		if (match) {
			const color = match[1].trim();
			const offset = match[2] ? parseFloat(match[2]) / 100 : idx / Math.max(1, parts.length - 1);
			const normalized = normalizeColor(color);
			stops.push({
				color: normalized.color,
				offset,
				opacity: normalized.opacity
			});
		}
	});
	return stops;
}
/**
* Normalize color to hex format for SVG
* Returns both the hex color and optional opacity
*/
function normalizeColor(color) {
	color = color.trim();
	if (color.startsWith("#")) return { color };
	const rgbMatch = color.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)/);
	if (rgbMatch) {
		const r = parseInt(rgbMatch[1]).toString(16).padStart(2, "0");
		const g = parseInt(rgbMatch[2]).toString(16).padStart(2, "0");
		const b = parseInt(rgbMatch[3]).toString(16).padStart(2, "0");
		const alpha = rgbMatch[4] ? parseFloat(rgbMatch[4]) : void 0;
		return {
			color: `#${r}${g}${b}`,
			opacity: alpha
		};
	}
	return { color };
}
/**
* Generate SVG for linear gradient
*/
function generateLinearGradientSVG(angle, stops, width, height) {
	const rad = (angle - 90) * Math.PI / 180;
	return `<svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad" x1="${50 - 50 * Math.cos(rad)}%" y1="${50 - 50 * Math.sin(rad)}%" x2="${50 + 50 * Math.cos(rad)}%" y2="${50 + 50 * Math.sin(rad)}%">
    ${stops.map((stop) => {
		const opacityAttr = stop.opacity !== void 0 ? ` stop-opacity="${stop.opacity}"` : "";
		return `<stop offset="${stop.offset * 100}%" stop-color="${stop.color}"${opacityAttr} />`;
	}).join("\n    ")}
    </linearGradient>
  </defs>
  <rect width="${width}" height="${height}" fill="url(#grad)" />
</svg>`;
}
/**
* Generate SVG for radial gradient
*/
function generateRadialGradientSVG(position, stops, width, height) {
	let cx = 50;
	let cy = 50;
	if (position && position !== "center") {
		const parts = position.split(/\s+/);
		if (parts[0]) {
			if (parts[0].endsWith("%")) cx = parseFloat(parts[0]);
			else if (parts[0] === "left") cx = 0;
			else if (parts[0] === "right") cx = 100;
		}
		if (parts[1]) {
			if (parts[1].endsWith("%")) cy = parseFloat(parts[1]);
			else if (parts[1] === "top") cy = 0;
			else if (parts[1] === "bottom") cy = 100;
		}
	}
	const stopElements = stops.map((stop) => {
		const opacityAttr = stop.opacity !== void 0 ? ` stop-opacity="${stop.opacity}"` : "";
		return `<stop offset="${stop.offset * 100}%" stop-color="${stop.color}"${opacityAttr} />`;
	}).join("\n    ");
	return `<svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="grad" cx="${cx}%" cy="${cy}%">
    ${stopElements}
    </radialGradient>
  </defs>
  <rect width="${width}" height="${height}" fill="url(#grad)" />
</svg>`;
}
/**
* Generate a gradient image file using Sharp
* Returns the path to the generated image
*/
async function generateGradientImage(gradientStr, width, height, tmpDir) {
	const svg = gradientToSVG(gradientStr, width, height);
	if (!svg) throw new Error(`Failed to parse gradient: ${gradientStr}`);
	const hash = crypto.default.createHash("md5").update(`${gradientStr}-${width}-${height}`).digest("hex").substring(0, 8);
	const outputPath = path.default.join(tmpDir, `gradient-${hash}.png`);
	await (0, sharp.default)(Buffer.from(svg)).png().toFile(outputPath);
	return outputPath;
}

//#endregion
//#region src/slide-builder.ts
/**
* Add background to slide (image or color)
* Note: Gradient backgrounds are now handled via element rasterization
*/
async function addBackground(slideData, targetSlide, tmpDir, slideWidth = 10, slideHeight = 5.625) {
	if (slideData.background.type === "image" && slideData.background.path) {
		const path$4 = slideData.background.path;
		if (path$4.includes("linear-gradient") || path$4.includes("radial-gradient")) targetSlide.background = { path: await generateGradientImage(path$4, Math.round(slideWidth * 96), Math.round(slideHeight * 96), tmpDir) };
		else targetSlide.background = { path: path$4.startsWith("file://") ? path$4.replace("file://", "") : path$4 };
	} else if (slideData.background.type === "color" && slideData.background.value) targetSlide.background = { color: slideData.background.value };
}
/**
* Add all elements to slide (images, shapes, text, lists)
*/
async function addElements(slideData, targetSlide, pres) {
	for (const el of slideData.elements) if (el.type === "image") {
		let imagePath = el.src.startsWith("file://") ? el.src.replace("file://", "") : el.src;
		targetSlide.addImage({
			path: imagePath,
			x: el.position.x,
			y: el.position.y,
			w: el.position.w,
			h: el.position.h
		});
	} else if (el.type === "rasterized-image") {
		if (!el.src) throw new Error(`Rasterized image element with id "${el.rasterizeId}" is missing screenshot path`);
		const imageOptions = {
			path: el.src.startsWith("file://") ? el.src.replace("file://", "") : el.src,
			x: el.position.x,
			y: el.position.y,
			w: el.position.w,
			h: el.position.h
		};
		if (el.shadow) imageOptions.shadow = el.shadow;
		targetSlide.addImage(imageOptions);
	} else if (el.type === "line") targetSlide.addShape(pres.ShapeType.line, {
		x: el.x1,
		y: el.y1,
		w: el.x2 - el.x1,
		h: el.y2 - el.y1,
		line: {
			color: el.color,
			width: el.width
		}
	});
	else if (el.type === "shape") {
		const shapeOptions = {
			x: el.position.x,
			y: el.position.y,
			w: el.position.w,
			h: el.position.h
		};
		if (el.shape.backgroundImage) shapeOptions.path = el.shape.backgroundImage.startsWith("file://") ? el.shape.backgroundImage.replace("file://", "") : el.shape.backgroundImage;
		if (el.shape.fill) {
			shapeOptions.fill = { color: el.shape.fill };
			if (el.shape.transparency != null) shapeOptions.fill.transparency = el.shape.transparency;
		}
		if (el.shape.line) shapeOptions.line = el.shape.line;
		if (el.shape.rectRadius > 0) {
			shapeOptions.rectRadius = el.shape.rectRadius;
			shapeOptions.shape = "roundRect";
		}
		if (el.shape.shadow) shapeOptions.shadow = el.shape.shadow;
		targetSlide.addText(el.text || "", shapeOptions);
	} else if (el.type === "list") {
		const listOptions = {
			x: el.position.x,
			y: el.position.y,
			w: el.position.w,
			h: el.position.h,
			fontSize: el.style.fontSize,
			fontFace: el.style.fontFace,
			color: el.style.color,
			align: el.style.align,
			valign: "top",
			paraSpaceBefore: el.style.paraSpaceBefore,
			paraSpaceAfter: el.style.paraSpaceAfter
		};
		if (el.style.lineSpacing !== null && el.style.lineSpacing !== void 0) listOptions.lineSpacing = el.style.lineSpacing;
		if (el.style.margin) listOptions.margin = el.style.margin;
		// Process items to apply indentLevel
		const processedItems = el.items.map(item => {
			const options = { ...item.options };
			let text = item.text;
			if (options.indentLevel !== undefined && options.indentLevel > 0) {
				// Apply indent for nested items
				if (options.bullet === false) {
					// No bullet - add spaces for indent (4 spaces per level)
					const spaces = '    '.repeat(options.indentLevel);
					text = spaces + text;
					options.bullet = false;
				} else {
					options.bullet = { ...options.bullet, indent: (options.bullet?.indent || 9) + options.indentLevel * 9 };
				}
				options.indentLevel = options.indentLevel;
			}
			return { text, options };
		});
		targetSlide.addText(processedItems, listOptions);
	} else {
		// Add margin to text box width to prevent unintended line breaks
		// Japanese text needs more margin due to character width variations
		const widthMargin = el.position.w * 0.10;
		let adjustedX = el.position.x;
		let adjustedW = el.position.w + widthMargin;
		const align = el.style.align;
		if (align === "center") {
			adjustedX = el.position.x - widthMargin / 2;
		} else if (align === "right") {
			adjustedX = el.position.x - widthMargin;
		}
		const textOptions = {
			x: adjustedX,
			y: el.position.y,
			w: adjustedW,
			h: el.position.h,
			fontSize: el.style.fontSize,
			fontFace: el.style.fontFace,
			color: el.style.color,
			bold: el.style.bold,
			italic: el.style.italic,
			valign: "top",
			paraSpaceBefore: el.style.paraSpaceBefore,
			paraSpaceAfter: el.style.paraSpaceAfter,
			inset: 0
		};
		if (el.style.underline) textOptions.underline = {
			style: "sng",
			color: el.style.color
		};
		if (el.style.lineSpacing !== null && el.style.lineSpacing !== void 0) textOptions.lineSpacing = el.style.lineSpacing;
		if (el.style.align) textOptions.align = el.style.align;
		if (el.style.margin) textOptions.margin = el.style.margin;
		if (el.style.rotate !== null && el.style.rotate !== void 0) textOptions.rotate = el.style.rotate;
		if (el.style.transparency !== null && el.style.transparency !== void 0) textOptions.transparency = el.style.transparency;
		// Fill in missing options for text runs with base style
		let textContent = el.text;
		if (Array.isArray(el.text)) {
			const expandedRuns = [];
			for (const run of el.text) {
				const baseOpts = {
					color: el.style.color,
					fontSize: el.style.fontSize,
					fontFace: el.style.fontFace,
					...run.options
				};
				// Split text by newlines and create separate runs
				const parts = run.text.split(/(\n)/);
				for (let i = 0; i < parts.length; i++) {
					const part = parts[i];
					if (part === '\n') {
						// Add breakLine to previous run if exists
						if (expandedRuns.length > 0) {
							expandedRuns[expandedRuns.length - 1].options.breakLine = true;
						}
					} else if (part) {
						expandedRuns.push({ text: part, options: { ...baseOpts } });
					}
				}
			}
			textContent = expandedRuns;
		}
		targetSlide.addText(textContent, textOptions);
	}
}

//#endregion
//#region src/getChromiumPath.ts
/**
* Helper function to check if a file exists
*/
async function fileExists(path$4) {
	try {
		await (0, fs_promises.access)(path$4);
		return true;
	} catch {
		return false;
	}
}
/**
* Determines the best path to a globally installed Chromium binary
*/
async function getChromiumPath() {
	const executablePath = playwright.chromium.executablePath();
	if (await fileExists(executablePath)) return executablePath;
	const pathParts = executablePath.split("/");
	const chromiumDirIndex = pathParts.findIndex((part) => part.startsWith("chromium-"));
	if (chromiumDirIndex === -1) throw new Error(`Could not find chromium revision in path: ${executablePath}`);
	const chromiumDirName = pathParts[chromiumDirIndex];
	const expectedRevision = parseInt(chromiumDirName.replace("chromium-", ""), 10);
	const parentDir = pathParts.slice(0, chromiumDirIndex).join("/");
	const relativePath = pathParts.slice(chromiumDirIndex + 1).join("/");
	let availableDirs = [];
	try {
		availableDirs = (await (0, fs_promises.readdir)(parentDir)).filter((dir) => dir.startsWith("chromium-"));
	} catch (_error) {
		throw new Error(`Could not read directory: ${parentDir}`);
	}
	if (availableDirs.length === 0) throw new Error(`No chromium installations found in: ${parentDir}`);
	let closestDiff = Infinity;
	let closestPath = void 0;
	for (const dir of availableDirs) {
		const revision = parseInt(dir.replace("chromium-", ""), 10);
		const diff = Math.abs(revision - expectedRevision);
		if (diff < closestDiff) {
			const candidatePath = (0, path.join)(parentDir, dir, relativePath);
			if (await fileExists(candidatePath)) {
				closestDiff = diff;
				closestPath = candidatePath;
			}
		}
	}
	if (!closestPath) throw new Error(`No valid chromium executable found. Tried ${availableDirs.length} alternatives.`);
	return closestPath;
}

//#endregion
//#region src/addStyleElement.ts
async function addStyleElement(page, cssContent) {
	await page.evaluate((css) => {
		async function addStyleContent(content, target) {
			const style = document.createElement("style");
			style.type = "text/css";
			style.appendChild(document.createTextNode(content));
			const promise = new Promise((res, rej) => {
				style.onload = res;
				style.onerror = rej;
			});
			if (target) target.parentNode?.insertBefore(style, target);
			else document.head.appendChild(style);
			await promise;
			return style;
		}
		return addStyleContent(css, document.head.firstChild);
	}, cssContent);
}

//#endregion
//#region src/preparePage.ts
const __dirname$1 = (0, node_path.dirname)((0, node_url.fileURLToPath)(require("url").pathToFileURL(__filename).href));
const playwrightDir = (0, node_fs.existsSync)((0, node_path.join)(__dirname$1, "playwright/index.css")) ? (0, node_path.join)(__dirname$1, "playwright") : (0, node_path.join)(__dirname$1, "../dist/playwright");
/**
* Add scripts and styles to the HTML page and run init function
*/
async function preparePage(page) {
	const themeCssPath = (0, node_path.join)(playwrightDir, "theme.css");
	const cssPath = (0, node_path.join)(playwrightDir, "index.css");
	const scriptPath = (0, node_path.join)(playwrightDir, "index.iife.js");
	const themeCssContent = (0, node_fs.readFileSync)(themeCssPath, "utf-8");
	const cssContent = (0, node_fs.readFileSync)(cssPath, "utf-8");
	const jsContent = (0, node_fs.readFileSync)(scriptPath, "utf-8");
	await addStyleElement(page, themeCssContent);
	await addStyleElement(page, cssContent);
	await page.addScriptTag({ content: jsContent });
	await page.evaluate(() => {
		const { ExtractSlideData } = window;
		return ExtractSlideData.init();
	});
}

//#endregion
//#region src/debug.ts
function getDebugMode() {
	if (process.platform !== "darwin") return;
	const debug = process.env.HTML2PPTX_DEBUG;
	if (debug === "always") return "always";
	return debug ? "error" : void 0;
}
function isDebugMode() {
	return !!getDebugMode();
}
function shouldPause(errors) {
	const debug = getDebugMode();
	if (debug === "always") return true;
	return debug === "error" ? !!errors.length : false;
}
async function maybePauseToDebug(page, errors) {
	if (shouldPause(errors)) await page.pause();
}

//#endregion
//#region src/index.ts
/**
* html2pptx - Convert HTML slide to pptxgenjs slide with positioned elements
*
* USAGE:
*   const pptx = new pptxgen();
*   pptx.layout = 'LAYOUT_16x9';  // Must match HTML body dimensions
*
*   const { slide, placeholders } = await html2pptx('slide.html', pptx);
*   slide.addChart(pptx.charts.LINE, data, placeholders[0]);
*
*   await pptx.writeFile('output.pptx');
*
* FEATURES:
*   - Converts HTML to PowerPoint with accurate positioning
*   - Supports text, images, shapes, and bullet lists
*   - Extracts placeholder elements (class="placeholder") with positions
*   - Handles CSS gradients, borders, and margins
*
* VALIDATION:
*   - Uses body width/height from HTML for viewport sizing
*   - Throws error if HTML dimensions don't match presentation layout
*   - Throws error if content overflows body (with overflow details)
*
* RETURNS:
*   { slide, placeholders } where placeholders is an array of { id, x, y, w, h }
*
* @packageDocumentation
*/
async function html2pptx(htmlFile, pres, options = {}) {
	const { tmpDir = process.env.TMPDIR || "/tmp", slide = null } = options;
	try {
		const launchOptions = {
			args: [
				"--single-process",
				"--no-zygote",
				"--disable-dev-shm-usage"
			],
			env: { TMPDIR: tmpDir },
			executablePath: await getChromiumPath(),
			headless: !isDebugMode()
		};
		if (process.platform === "darwin") launchOptions.channel = "chrome";
		const browser = await playwright.chromium.launch(launchOptions);
		let bodyDimensions;
		let slideData;
		const filePath = path.default.isAbsolute(htmlFile) ? htmlFile : path.default.join(process.cwd(), htmlFile);
		const fileDir = path.default.dirname(filePath);
		const validationErrors = [];

		// Create a simple HTTP server to serve the HTML file (needed for CDN scripts like Mermaid.js)
		const server = http.createServer((req, res) => {
			let requestedPath = req.url === '/' ? filePath : path.default.join(fileDir, req.url);
			// Handle query strings
			requestedPath = requestedPath.split('?')[0];

			const ext = path.default.extname(requestedPath).toLowerCase();
			const mimeTypes = {
				'.html': 'text/html',
				'.css': 'text/css',
				'.js': 'application/javascript',
				'.png': 'image/png',
				'.jpg': 'image/jpeg',
				'.jpeg': 'image/jpeg',
				'.gif': 'image/gif',
				'.svg': 'image/svg+xml',
				'.json': 'application/json'
			};

			(0, node_fs.readFile)(requestedPath, (err, data) => {
				if (err) {
					res.writeHead(404);
					res.end('Not found');
					return;
				}
				res.writeHead(200, { 'Content-Type': mimeTypes[ext] || 'application/octet-stream' });
				res.end(data);
			});
		});

		// Find an available port
		await new Promise((resolve) => {
			server.listen(0, '127.0.0.1', () => resolve());
		});
		const serverPort = server.address().port;
		const serverUrl = `http://127.0.0.1:${serverPort}/`;

		try {
			const page = await browser.newPage({ deviceScaleFactor: 3 });
			page.on("console", (msg) => {
				console.log(`Browser console: ${msg.text()}`);
			});
			await page.goto(serverUrl, { waitUntil: 'networkidle' });
			// Wait for Mermaid diagrams to render if present
			await page.waitForFunction(() => {
				const mermaidElements = document.querySelectorAll('.mermaid');
				if (mermaidElements.length === 0) return true;
				// Check if all mermaid elements have been converted to SVG
				return Array.from(mermaidElements).every(el => el.querySelector('svg') !== null);
			}, { timeout: 10000 }).catch(() => {
				// Mermaid may not be present or may have failed, continue anyway
			});
			await preparePage(page);
			bodyDimensions = await getBodyDimensions(page);
			await maybePauseToDebug(page, bodyDimensions.errors);
			slideData = await extractSlideData(page, tmpDir, htmlFile);
			await maybePauseToDebug(page, slideData.errors);
		} finally {
			await browser.close();
			server.close();
		}
		if (bodyDimensions.errors && bodyDimensions.errors.length > 0) validationErrors.push(...bodyDimensions.errors);
		const dimensionErrors = validateDimensions(bodyDimensions, pres);
		if (dimensionErrors.length > 0) validationErrors.push(...dimensionErrors);
		const textBoxPositionErrors = validateTextBoxPosition(slideData, bodyDimensions);
		if (textBoxPositionErrors.length > 0) validationErrors.push(...textBoxPositionErrors);
		if (slideData.errors && slideData.errors.length > 0) validationErrors.push(...slideData.errors);
		if (validationErrors.length > 0) {
			const errorMessage = validationErrors.length === 1 ? validationErrors[0] : `Multiple validation errors found:\n${validationErrors.map((e, i) => `  ${i + 1}. ${e}`).join("\n")}`;
			throw new Error(errorMessage);
		}
		const targetSlide = slide || pres.addSlide();
		const EMU_PER_INCH = 914400;
		const slideWidthEMU = pres.presLayout?.width || 9144e3;
		const slideHeightEMU = pres.presLayout?.height || 5143500;
		const slideWidth = slideWidthEMU / EMU_PER_INCH;
		const slideHeight = slideHeightEMU / EMU_PER_INCH;
		await addBackground(slideData, targetSlide, tmpDir, slideWidth, slideHeight);
		await addElements(slideData, targetSlide, pres);
		return {
			slide: targetSlide,
			placeholders: slideData.placeholders,
			html: slideData.html
		};
	} catch (error) {
		if (error instanceof Error && !error.message.startsWith(htmlFile)) throw new Error(`${htmlFile}: ${error.message}`);
		throw error;
	}
}

//#endregion
exports.html2pptx = html2pptx;