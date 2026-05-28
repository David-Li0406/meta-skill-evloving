var ExtractSlideData = (function(exports) {


//#region src/playwright/balanceText.ts
/**
	* HTML elements can now use the `data-balance` attribute to enable text balancing:
	*
	* Balance with default ratio of 1:
	*  <div><span data-balance>Your text here</span></div>
	*
	* Balance with custom ratio:
	*  <div><span data-balance="0.5">Your text here</span></div>
	*
	* The script will automatically find and balance all such elements when the page loads.
	*/
	const BALANCE_TEXT_ATTR = "data-balance";
	function balanceText(element, ratio) {
		if (!(element instanceof HTMLElement)) return;
		const setMaxWidth = (width$1) => {
			element.style.maxWidth = width$1 + "px";
		};
		element.style.maxWidth = "";
		const width = element.scrollWidth;
		const height = element.clientHeight;
		const computedStyle = window.getComputedStyle(element);
		let lower = width / 2 - .25;
		let upper = width + .5;
		let middle;
		if (width) {
			setMaxWidth(lower);
			lower = Math.max(element.scrollWidth, lower);
			while (lower + 1 < upper) {
				middle = Math.round((lower + upper) / 2);
				setMaxWidth(middle);
				if (element.clientHeight === height) upper = middle;
				else lower = middle;
			}
			setMaxWidth(upper * ratio + width * (1 - ratio));
		}
		if (computedStyle.textAlign === "center") {
			element.style.marginLeft = "auto";
			element.style.marginRight = "auto";
		}
	}
	const DEFAULT_BALANCE_TEXT_SELECTOR = `[${BALANCE_TEXT_ATTR}]`;
	function balanceAllText(selector = "") {
		let mergedSelector = DEFAULT_BALANCE_TEXT_SELECTOR;
		if (selector) mergedSelector += `, ${selector}`;
		document.querySelectorAll(mergedSelector).forEach((element) => {
			const ratioAttr = element.getAttribute(BALANCE_TEXT_ATTR);
			const ratio = ratioAttr ? parseFloat(ratioAttr) : 1;
			balanceText(element, !isNaN(ratio) && ratio >= 0 && ratio <= 1 ? ratio : 1);
		});
	}

//#endregion
//#region src/playwright/constants.ts
/**
	* Constants used in browser-side extraction
	*/
	const PT_PER_PX = .75;
	const PX_PER_IN = 96;
	const SINGLE_WEIGHT_FONTS = ["impact"];

//#endregion
//#region src/playwright/init.ts
	function init() {
		balanceAllText("h1, h2");
	}

//#endregion
//#region src/playwright/unitConversion.ts
/**
	* Unit conversion utilities for browser-side extraction
	*/
	/**
	* Convert pixels to inches
	*/
	function pxToInch(px) {
		return px / PX_PER_IN;
	}
	/**
	* Convert pixels to points
	*/
	function pxToPoints(pxStr) {
		return parseFloat(String(pxStr)) * PT_PER_PX;
	}
	/**
	* Convert RGB/RGBA string to hex color
	*/
	function rgbToHex(rgbStr) {
		if (rgbStr === "rgba(0, 0, 0, 0)" || rgbStr === "transparent") return "FFFFFF";
		const match = rgbStr.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
		if (!match) return "FFFFFF";
		return match.slice(1).map((n) => parseInt(n).toString(16).padStart(2, "0")).join("");
	}
	/**
	* Extract alpha transparency from RGBA string
	* Returns transparency percentage (0-100) or null if fully opaque
	*/
	function extractAlpha(rgbStr) {
		const match = rgbStr.match(/rgba\((\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\)/);
		if (!match || !match[4]) return null;
		const alpha = parseFloat(match[4]);
		return Math.round((1 - alpha) * 100);
	}
	/**
	* Convert a DOMRect to XYWH position object in inches
	*/
	function rectToXYWH(rect) {
		return {
			x: pxToInch(rect.left),
			y: pxToInch(rect.top),
			w: pxToInch(rect.width),
			h: pxToInch(rect.height)
		};
	}

//#endregion
//#region src/playwright/textHelpers.ts
/**
	* Text transformation and formatting helpers for browser-side extraction
	*/
	/**
	* Check if a font should skip bold formatting
	* (applying bold causes PowerPoint to use faux bold which makes text wider)
	*/
	function shouldSkipBold(fontFamily) {
		if (!fontFamily) return false;
		const normalizedFont = fontFamily.toLowerCase().replace(/['"]/g, "").split(",")[0].trim();
		return SINGLE_WEIGHT_FONTS.includes(normalizedFont);
	}
	/**
	* Apply CSS text-transform to text
	*/
	function applyTextTransform(text, textTransform) {
		if (textTransform === "uppercase") return text.toUpperCase();
		if (textTransform === "lowercase") return text.toLowerCase();
		if (textTransform === "capitalize") return text.replace(/\b\w/g, (c) => c.toUpperCase());
		return text;
	}

//#endregion
//#region src/playwright/transformHelpers.ts
/**
	* CSS transform and positioning helpers for browser-side extraction
	*/
	/**
	* Extract rotation angle from CSS transform and writing-mode
	*/
	function getRotation(transform, writingMode) {
		let angle = 0;
		if (writingMode === "vertical-rl") angle = 90;
		else if (writingMode === "vertical-lr") angle = 270;
		if (transform && transform !== "none") {
			const rotateMatch = transform.match(/rotate\((-?\d+(?:\.\d+)?)deg\)/);
			if (rotateMatch) angle += parseFloat(rotateMatch[1]);
			else {
				const matrixMatch = transform.match(/matrix\(([^)]+)\)/);
				if (matrixMatch) {
					const values = matrixMatch[1].split(",").map(parseFloat);
					const matrixAngle = Math.atan2(values[1], values[0]) * (180 / Math.PI);
					angle += Math.round(matrixAngle);
				}
			}
		}
		angle = angle % 360;
		if (angle < 0) angle += 360;
		return angle === 0 ? null : angle;
	}
	/**
	* Get position and size accounting for rotation
	*/
	function getPositionAndSize(el, rect, rotation) {
		if (rotation === null) return {
			x: rect.left,
			y: rect.top,
			w: rect.width,
			h: rect.height
		};
		if (rotation === 90 || rotation === 270) {
			const centerX$1 = rect.left + rect.width / 2;
			const centerY$1 = rect.top + rect.height / 2;
			return {
				x: centerX$1 - rect.height / 2,
				y: centerY$1 - rect.width / 2,
				w: rect.height,
				h: rect.width
			};
		}
		const centerX = rect.left + rect.width / 2;
		const centerY = rect.top + rect.height / 2;
		return {
			x: centerX - el.offsetWidth / 2,
			y: centerY - el.offsetHeight / 2,
			w: el.offsetWidth,
			h: el.offsetHeight
		};
	}

//#endregion
//#region src/playwright/shadowHelpers.ts
/**
	* CSS box-shadow parsing for browser-side extraction
	*/
	/**
	* Parse CSS box-shadow into PptxGenJS shadow properties
	*/
	function parseBoxShadow(boxShadow) {
		if (!boxShadow || boxShadow === "none") return null;
		if (boxShadow.match(/inset/)) return null;
		const colorMatch = boxShadow.match(/rgba?\([^)]+\)/);
		const parts = boxShadow.match(/([-\d.]+)(px|pt)/g);
		if (!parts || parts.length < 2) return null;
		const offsetX = parseFloat(parts[0]);
		const offsetY = parseFloat(parts[1]);
		const blur = parts.length > 2 ? parseFloat(parts[2]) : 0;
		let angle = 0;
		if (offsetX !== 0 || offsetY !== 0) {
			angle = Math.atan2(offsetY, offsetX) * (180 / Math.PI);
			if (angle < 0) angle += 360;
		}
		const offset = Math.sqrt(offsetX * offsetX + offsetY * offsetY) * PT_PER_PX;
		let opacity = .5;
		if (colorMatch) {
			const opacityMatch = colorMatch[0].match(/[\d.]+\)$/);
			if (opacityMatch) opacity = parseFloat(opacityMatch[0].replace(")", ""));
		}
		return {
			type: "outer",
			angle: Math.round(angle),
			blur: blur * .75,
			color: colorMatch ? rgbToHex(colorMatch[0]) : "000000",
			offset,
			opacity
		};
	}

//#endregion
//#region src/playwright/inlineFormatting.ts
/**
	* Parse inline formatting tags (<b>, <i>, <u>, <strong>, <em>, <span>) into text runs
	*/
	function parseInlineFormatting(element, baseOptions = {}, runs = [], baseTextTransform = (x) => x, errors = []) {
		let prevNodeIsText = false;
		element.childNodes.forEach((node) => {
			let textTransform = baseTextTransform;
			const isText = node.nodeType === Node.TEXT_NODE || node.tagName === "BR";
			if (isText) {
				const text = node.tagName === "BR" ? "\n" : textTransform(node.textContent.replace(/\s+/g, " "));
				const prevRun = runs[runs.length - 1];
				if (prevNodeIsText && prevRun) prevRun.text += text;
				else runs.push({
					text,
					options: { ...baseOptions }
				});
			} else if (node.nodeType === Node.ELEMENT_NODE && node.textContent.trim()) {
				const el = node;
				const options = { ...baseOptions };
				const computed = window.getComputedStyle(el);
				if (el.tagName === "SPAN" || el.tagName === "B" || el.tagName === "STRONG" || el.tagName === "I" || el.tagName === "EM" || el.tagName === "U") {
					if ((computed.fontWeight === "bold" || parseInt(computed.fontWeight) >= 600) && !shouldSkipBold(computed.fontFamily)) options.bold = true;
					if (computed.fontStyle === "italic") options.italic = true;
					if (computed.color && computed.color !== "rgb(0, 0, 0)") {
						options.color = rgbToHex(computed.color);
						const transparency = extractAlpha(computed.color);
						if (transparency !== null) options.transparency = transparency;
					}
					if (computed.textDecoration && computed.textDecoration.includes("underline")) options.underline = {
						style: "sng",
						color: rgbToHex(computed.color)
					};
					if (computed.fontSize) options.fontSize = pxToPoints(computed.fontSize);
					if (computed.textTransform && computed.textTransform !== "none") {
						const transformStr = computed.textTransform;
						textTransform = (text) => applyTextTransform(text, transformStr);
					}
					if (computed.marginLeft && parseFloat(computed.marginLeft) > 0) errors.push(`Inline element <${el.tagName.toLowerCase()}> has margin-left which is not supported in PowerPoint. Remove margin from inline elements.`);
					if (computed.marginRight && parseFloat(computed.marginRight) > 0) errors.push(`Inline element <${el.tagName.toLowerCase()}> has margin-right which is not supported in PowerPoint. Remove margin from inline elements.`);
					if (computed.marginTop && parseFloat(computed.marginTop) > 0) errors.push(`Inline element <${el.tagName.toLowerCase()}> has margin-top which is not supported in PowerPoint. Remove margin from inline elements.`);
					if (computed.marginBottom && parseFloat(computed.marginBottom) > 0) errors.push(`Inline element <${el.tagName.toLowerCase()}> has margin-bottom which is not supported in PowerPoint. Remove margin from inline elements.`);
					parseInlineFormatting(el, options, runs, textTransform, errors);
				}
			}
			prevNodeIsText = isText;
		});
		if (runs.length > 0) {
			runs[0].text = runs[0].text.replace(/^\s+/, "");
			runs[runs.length - 1].text = runs[runs.length - 1].text.replace(/\s+$/, "");
		}
		return runs.filter((r) => r.text.length > 0);
	}

//#endregion
//#region src/playwright/utils.ts
	function isAncestorOrDescendant(el1, el2) {
		return el1.contains(el2) || el2.contains(el1);
	}
	function truncate(text, maxLength) {
		return text.length > maxLength ? text.slice(0, maxLength) + "..." : text;
	}
	function getElementDescriptor(element) {
		const parts = [];
		parts.push(`<${element.tagName.toLowerCase()}>`);
		if (element.className && typeof element.className === "string") {
			const classes = element.className.trim();
			if (classes) {
				const classString = `.${classes.split(/\s+/).join(".")}`;
				parts.push(truncate(classString, 40));
			}
		}
		if (element.id) parts.push(`#${element.id}`);
		const textContent = element.textContent?.trim();
		if (textContent) parts.push(`"${truncate(textContent, 30)}"`);
		return parts.join(" ");
	}

//#endregion
//#region src/playwright/rectHelpers.ts
	const EDGES = [
		"top",
		"left",
		"bottom",
		"right"
	];
	function getOverflowErrors(container, element, descriptor) {
		const errors = [];
		EDGES.forEach((edge) => {
			const amount = edge === "bottom" || edge === "right" ? element[edge] - container[edge] : container[edge] - element[edge];
			if (amount > 0) {
				const prefix = descriptor ? `${descriptor}:` : "";
				errors.push(`${prefix} overlaps <body> ${edge} boundary by ${amount.toFixed()}px`);
			}
		});
		return errors;
	}
	function getElementOverlapError(rect1, rect2, descriptor1, descriptor2) {
		const xOverlap = Math.max(0, Math.min(rect1.right, rect2.right) - Math.max(rect1.left, rect2.left));
		const yOverlap = Math.max(0, Math.min(rect1.bottom, rect2.bottom) - Math.max(rect1.top, rect2.top));
		if (!xOverlap || !yOverlap) return;
		const fullyOverlappedX = rect1.left >= rect2.left && rect1.right <= rect2.right || rect2.left >= rect1.left && rect2.right <= rect1.right;
		const fullyOverlappedY = rect1.top >= rect2.top && rect1.bottom <= rect2.bottom || rect2.top >= rect1.top && rect2.bottom <= rect1.bottom;
		const topOverlaps = rect1.top < rect2.bottom && rect1.top >= rect2.top;
		const elementEdgeY = topOverlaps ? "top" : "bottom";
		const otherEdgeY = topOverlaps ? "bottom" : "top";
		if (fullyOverlappedX && !fullyOverlappedY) return `The ${elementEdgeY} of ${descriptor1} overlaps with the ${otherEdgeY} of ${descriptor2} by ${yOverlap.toFixed()}px`;
		const leftOverlaps = rect1.left < rect2.right && rect1.left >= rect2.left;
		const elementEdgeX = leftOverlaps ? "left" : "right";
		const otherEdgeX = leftOverlaps ? "right" : "left";
		if (fullyOverlappedY && !fullyOverlappedX) return `The ${elementEdgeX} of ${descriptor1} overlaps with the ${otherEdgeX} of ${descriptor2} by ${xOverlap.toFixed()}px`;
		if (fullyOverlappedX && fullyOverlappedY) {
			const rect1Width = rect1.right - rect1.left;
			const rect2Width = rect2.right - rect2.left;
			return `${rect1Width > rect2Width ? descriptor2 : descriptor1} is completely overlapped by ${rect1Width > rect2Width ? descriptor1 : descriptor2}. Consider rearranging your layout.`;
		}
		return `The ${elementEdgeX} and ${elementEdgeY} edges of ${descriptor1} overlaps with the ${otherEdgeX} and ${otherEdgeY} edges of ${descriptor2} by ${xOverlap.toFixed()}px and ${yOverlap.toFixed()}px`;
	}

//#endregion
//#region src/playwright/validateAndMakeCorrections.ts
	const SLIDE_PADDING_PX = .25 * PX_PER_IN;
	/**
	* Monitors elements for overflow and overlap issues within a slide.
	*
	* This function:
	* 1. Observes elements for size/position changes using ResizeObserver
	* 2. Validates that elements don't overflow the slide boundaries
	* 3. Checks for overlaps between sibling elements
	* 4. Returns error messages describing any layout issues found
	*
	* @param tags - Array of CSS selectors to monitor
	* @returns Promise resolving to array of error messages (empty if no issues)
	*/
	async function validateAndMakeCorrections(tags) {
		const selector = tags.join(",");
		const elements = Array.from(document.querySelectorAll(selector)).filter((el) => el instanceof HTMLElement);
		const rectMap = /* @__PURE__ */ new WeakMap();
		const errorMap = /* @__PURE__ */ new WeakMap();
		const bodyRect = document.body.getBoundingClientRect();
		const bodyOverflowRect = {
			top: bodyRect.top + SLIDE_PADDING_PX,
			left: bodyRect.left + SLIDE_PADDING_PX,
			bottom: bodyRect.bottom - SLIDE_PADDING_PX,
			right: bodyRect.right - SLIDE_PADDING_PX
		};
		/**
		* Validates all elements for overflow and overlap issues.
		* For each element:
		* 1. Check if it overflows the slide boundaries
		* 2. Check if it overlaps with any subsequent sibling elements
		*/
		function validate() {
			for (let i = 0; i < elements.length; i++) {
				const element = elements[i];
				const contentRect = rectMap.get(element)?.contentRect;
				if (!contentRect) continue;
				const elementDescriptor = getElementDescriptor(element);
				const errors = getOverflowErrors(bodyOverflowRect, contentRect, elementDescriptor);
				for (let j = i + 1; j < elements.length; j++) {
					const el = elements[j];
					if (isAncestorOrDescendant(el, element)) continue;
					const otherContentRect = rectMap.get(el)?.contentRect;
					if (otherContentRect) {
						const error = getElementOverlapError(contentRect, otherContentRect, elementDescriptor, getElementDescriptor(el));
						if (error) errors.push(error);
					}
				}
				errorMap.set(element, errors);
			}
		}
		/** Returns true when ResizeObserver has populated all element rectangles */
		function isPopulated() {
			return elements.every((el) => rectMap.has(el));
		}
		/**
		* Waits for all element rectangles to be populated, then executes callback.
		* Uses requestAnimationFrame to poll until ready.
		*/
		function whenPopulated(callback) {
			let animationFrameId = null;
			function check() {
				if (isPopulated()) callback();
				else animationFrameId = requestAnimationFrame(check);
			}
			check();
			return () => {
				if (animationFrameId) cancelAnimationFrame(animationFrameId);
			};
		}
		/** Returns true when all elements have zero validation errors */
		function isValid() {
			return elements.every((el) => errorMap.get(el)?.length === 0);
		}
		/**
		* Placeholder for automatic correction logic.
		* Could attempt to fix issues by adjusting font-size, margins, etc.
		* @returns true if corrections were made (triggers re-validation), false otherwise
		*/
		function maybeMakeCorrections() {
			return false;
		}
		/**
		* Repeatedly validates until either:
		* 1. No errors remain (isValid returns true)
		* 2. No corrections are possible (maybeMakeCorrections returns false)
		*
		* Then calls callback with all accumulated errors.
		*/
		function whenDone(callback) {
			let animationFrameId = null;
			function check() {
				validate();
				if (isValid() || !maybeMakeCorrections()) callback(elements.flatMap((el) => errorMap.get(el) || []));
				else animationFrameId = requestAnimationFrame(check);
			}
			check();
			return () => {
				if (animationFrameId) cancelAnimationFrame(animationFrameId);
			};
		}
		/**
		* ResizeObserver tracks element size and position changes.
		* Updates rectMap whenever elements are resized, moved, or initially rendered.
		*/
		const resizeObserver = new ResizeObserver((entries) => {
			entries.forEach((entry) => {
				const { target, contentRect } = entry;
				const boundingRect = target.getBoundingClientRect();
				const contentTop = boundingRect.top + contentRect.y;
				const contentLeft = boundingRect.left + contentRect.x;
				rectMap.set(target, {
					boundingRect,
					contentRect: {
						top: contentTop,
						left: contentLeft,
						bottom: contentTop + contentRect.height,
						right: contentLeft + contentRect.width
					}
				});
			});
		});
		elements.forEach((el) => resizeObserver.observe(el));
		/**
		* Promise-based flow:
		* 1. Wait for ResizeObserver to populate all element rectangles (whenPopulated)
		* 2. Validate and potentially auto-correct in a loop (whenDone)
		* 3. Resolve with final error list
		*/
		return new Promise((resolve, _reject) => {
			whenPopulated(() => {
				whenDone((errors) => resolve(errors));
			});
		});
	}

//#endregion
//#region src/playwright/extractSlideDataInBrowser.ts
/**
	* Supported block elements that can have backgrounds, borders, and other shape properties
	*/
	const SUPPORTED_BLOCK_ELEMENTS = [
		"DIV",
		"SECTION",
		"HEADER",
		"FOOTER",
		"MAIN",
		"ARTICLE",
		"NAV",
		"ASIDE"
	];
	const SUPPORTED_TEXT_TAGS = [
		"P",
		"H1",
		"H2",
		"H3",
		"H4",
		"H5",
		"H6",
		"UL",
		"OL",
		"LI",
		"PRE"
	];
	/**
	* Extract slide data from the current HTML page
	* This function runs in the browser context via page.evaluate()
	*/
	async function extractSlideDataInBrowser() {
		const body = document.body;
		const bodyStyle = window.getComputedStyle(body);
		const bgImage = bodyStyle.backgroundImage;
		const bgColor = bodyStyle.backgroundColor;
		const errors = await validateAndMakeCorrections(SUPPORTED_TEXT_TAGS);
		let background;
		if (bgImage && bgImage !== "none") if (bgImage.includes("linear-gradient") || bgImage.includes("radial-gradient")) background = {
			type: "image",
			path: bgImage
		};
		else {
			const urlMatch = bgImage.match(/url\(["']?([^"')]+)["']?\)/);
			if (urlMatch) background = {
				type: "image",
				path: urlMatch[1]
			};
			else background = {
				type: "color",
				value: rgbToHex(bgColor)
			};
		}
		else background = {
			type: "color",
			value: rgbToHex(bgColor)
		};
		const elements = [];
		const placeholders = [];
		const rasterizeElements = [];
		const processed = /* @__PURE__ */ new Set();
		// Helper function to check if element is inside SVG (not the SVG itself)
		const isInsideSvg = (el) => {
			let parent = el.parentElement;
			while (parent) {
				if (parent.tagName.toUpperCase() === "SVG") return true;
				parent = parent.parentElement;
			}
			return false;
		};
		// Helper function to check if element is a mermaid source block (but NOT the rendered SVG)
		const isMermaidSource = (el) => {
			// SVG elements are NOT mermaid source - they are the rendered output
			if (el.tagName.toUpperCase() === "SVG") return false;
			if (el.tagName.toUpperCase() === "PRE" && el.classList.contains("mermaid")) return true;
			// Check if parent is a mermaid pre (but not if we're an SVG inside it)
			let parent = el.parentElement;
			while (parent) {
				if (parent.tagName.toUpperCase() === "PRE" && parent.classList.contains("mermaid")) return true;
				parent = parent.parentElement;
			}
			return false;
		};
		document.querySelectorAll("*").forEach((el) => {
			if (processed.has(el)) return;
			// Skip elements that are children inside SVG (but NOT the SVG element itself)
			if (isInsideSvg(el)) {
				processed.add(el);
				return;
			}
			// Skip mermaid source code blocks (they get rendered as SVG)
			if (isMermaidSource(el)) {
				processed.add(el);
				return;
			}
			if (el.tagName.toUpperCase() === "SVG" || el.tagName.toUpperCase() === "CANVAS") {
				const rect$1 = el.getBoundingClientRect();
				if (rect$1.width > 0 && rect$1.height > 0) {
					const uniqueId = `rasterize-${rasterizeElements.length}-${Date.now()}`;
					el.setAttribute("data-rasterize", uniqueId);
					const rasterizationType = el.tagName.toUpperCase() === "SVG" ? "svg" : "canvas";
					elements.push({
						type: "rasterized-image",
						rasterizeId: uniqueId,
						rasterizationType,
						position: rectToXYWH(rect$1)
					});
					rasterizeElements.push({
						id: uniqueId,
						element: el
					});
					processed.add(el);
					// Mark all descendants as processed to prevent text extraction from SVG/Canvas
					el.querySelectorAll("*").forEach((child) => processed.add(child));
					return;
				}
			}
			if (SUPPORTED_TEXT_TAGS.includes(el.tagName)) {
				const computed$1 = window.getComputedStyle(el);
				const hasBg = computed$1.backgroundColor && computed$1.backgroundColor !== "rgba(0, 0, 0, 0)";
				const hasBorder = computed$1.borderWidth && parseFloat(computed$1.borderWidth) > 0 || computed$1.borderTopWidth && parseFloat(computed$1.borderTopWidth) > 0 || computed$1.borderRightWidth && parseFloat(computed$1.borderRightWidth) > 0 || computed$1.borderBottomWidth && parseFloat(computed$1.borderBottomWidth) > 0 || computed$1.borderLeftWidth && parseFloat(computed$1.borderLeftWidth) > 0;
				const hasShadow = computed$1.boxShadow && computed$1.boxShadow !== "none";
				if (hasBg || hasBorder || hasShadow) {
					errors.push(`Text element <${el.tagName.toLowerCase()}> has ${hasBg ? "background" : hasBorder ? "border" : "shadow"}. Backgrounds, borders, and shadows are only supported on <div> elements, not text elements.`);
					return;
				}
			}
			if (el.classList && el.classList.contains("placeholder")) {
				const rect$1 = el.getBoundingClientRect();
				const isSmallWidth = rect$1.width < 5;
				const isSmallHeight = rect$1.height < 5;
				if (isSmallWidth || isSmallHeight) errors.push(`Placeholder "${el.id || "unnamed"}" is too small: \`width: ${rect$1.width}px; height: ${rect$1.height}px;\`. Check the layout CSS.`);
				else placeholders.push({
					id: el.id || `placeholder-${placeholders.length}`,
					...rectToXYWH(rect$1)
				});
				processed.add(el);
				return;
			}
			if (el.tagName === "IMG") {
				const rect$1 = el.getBoundingClientRect();
				if (rect$1.width > 0 && rect$1.height > 0) {
					elements.push({
						type: "image",
						src: el.src,
						position: rectToXYWH(rect$1)
					});
					processed.add(el);
					return;
				}
			}
			if (SUPPORTED_BLOCK_ELEMENTS.includes(el.tagName)) {
				const computed$1 = window.getComputedStyle(el);
				const hasBg = computed$1.backgroundColor && computed$1.backgroundColor !== "rgba(0, 0, 0, 0)";
				for (const node of Array.from(el.childNodes)) if (node.nodeType === Node.TEXT_NODE) {
					const text$1 = node.textContent?.trim() || "";
					if (text$1) errors.push(`${el.tagName} element contains unwrapped text "${text$1.substring(0, 50)}${text$1.length > 50 ? "..." : ""}". All text must be wrapped in <p>, <h1>-<h6>, <ul>, or <ol> tags to appear in PowerPoint.`);
				}
				const bgImage$1 = computed$1.backgroundImage;
				let backgroundImagePath = null;
				let backgroundGradient = null;
				let hasGradient = false;
				if (bgImage$1 && bgImage$1 !== "none") if (bgImage$1.includes("linear-gradient") || bgImage$1.includes("radial-gradient")) {
					backgroundGradient = bgImage$1;
					hasGradient = true;
				} else {
					const urlMatch = bgImage$1.match(/url\(["']?([^"')]+)["']?\)/);
					if (urlMatch) backgroundImagePath = urlMatch[1];
				}
				const borderTop = computed$1.borderTopWidth;
				const borderRight = computed$1.borderRightWidth;
				const borderBottom = computed$1.borderBottomWidth;
				const borderLeft = computed$1.borderLeftWidth;
				const borders = [
					borderTop,
					borderRight,
					borderBottom,
					borderLeft
				].map((b) => parseFloat(b) || 0);
				const hasBorder = borders.some((b) => b > 0);
				const hasUniformBorder = hasBorder && borders.every((b) => b === borders[0]);
				const borderLines = [];
				if (hasBorder && !hasUniformBorder) {
					const rect$1 = el.getBoundingClientRect();
					const x$1 = pxToInch(rect$1.left);
					const y$1 = pxToInch(rect$1.top);
					const w$1 = pxToInch(rect$1.width);
					const h$1 = pxToInch(rect$1.height);
					if (parseFloat(borderTop) > 0) {
						const widthPt = pxToPoints(borderTop);
						const inset = widthPt / 72 / 2;
						borderLines.push({
							type: "line",
							x1: x$1,
							y1: y$1 + inset,
							x2: x$1 + w$1,
							y2: y$1 + inset,
							width: widthPt,
							color: rgbToHex(computed$1.borderTopColor)
						});
					}
					if (parseFloat(borderRight) > 0) {
						const widthPt = pxToPoints(borderRight);
						const inset = widthPt / 72 / 2;
						borderLines.push({
							type: "line",
							x1: x$1 + w$1 - inset,
							y1: y$1,
							x2: x$1 + w$1 - inset,
							y2: y$1 + h$1,
							width: widthPt,
							color: rgbToHex(computed$1.borderRightColor)
						});
					}
					if (parseFloat(borderBottom) > 0) {
						const widthPt = pxToPoints(borderBottom);
						const inset = widthPt / 72 / 2;
						borderLines.push({
							type: "line",
							x1: x$1,
							y1: y$1 + h$1 - inset,
							x2: x$1 + w$1,
							y2: y$1 + h$1 - inset,
							width: widthPt,
							color: rgbToHex(computed$1.borderBottomColor)
						});
					}
					if (parseFloat(borderLeft) > 0) {
						const widthPt = pxToPoints(borderLeft);
						const inset = widthPt / 72 / 2;
						borderLines.push({
							type: "line",
							x1: x$1 + inset,
							y1: y$1,
							x2: x$1 + inset,
							y2: y$1 + h$1,
							width: widthPt,
							color: rgbToHex(computed$1.borderLeftColor)
						});
					}
				}
				if (hasBg || hasBorder || backgroundImagePath || backgroundGradient) {
					const rect$1 = el.getBoundingClientRect();
					if (rect$1.width > 0 && rect$1.height > 0) {
						const shadowData = parseBoxShadow(computed$1.boxShadow);
						const shadow = shadowData ? {
							...shadowData,
							type: "outer"
						} : null;
						if (hasGradient) {
							const uniqueId = `rasterize-gradient-${rasterizeElements.length}-${Date.now()}`;
							el.setAttribute("data-rasterize", uniqueId);
							elements.push({
								type: "rasterized-image",
								rasterizeId: uniqueId,
								rasterizationType: "gradient",
								position: rectToXYWH(rect$1),
								shadow
							});
							rasterizeElements.push({
								id: uniqueId,
								element: el
							});
							processed.add(el);
							return;
						}
						if (hasBg || hasUniformBorder || backgroundImagePath) elements.push({
							type: "shape",
							text: "",
							position: rectToXYWH(rect$1),
							shape: {
								fill: hasBg ? rgbToHex(computed$1.backgroundColor) : null,
								transparency: hasBg ? extractAlpha(computed$1.backgroundColor) : null,
								line: hasUniformBorder ? {
									color: rgbToHex(computed$1.borderColor),
									width: pxToPoints(computed$1.borderWidth)
								} : null,
								rectRadius: (() => {
									const radius = computed$1.borderRadius;
									const radiusValue = parseFloat(radius);
									if (radiusValue === 0) return 0;
									if (radius.includes("%")) {
										if (radiusValue >= 50) return 1;
										const minDim = Math.min(rect$1.width, rect$1.height);
										return radiusValue / 100 * pxToInch(minDim);
									}
									if (radius.includes("pt")) return radiusValue / 72;
									return radiusValue / PX_PER_IN;
								})(),
								shadow,
								backgroundImage: backgroundImagePath
							}
						});
						elements.push(...borderLines);
						processed.add(el);
						return;
					}
				}
			}
			if (el.tagName === "UL" || el.tagName === "OL") {
				// Skip nested lists - only process top-level lists
				if (el.parentElement && el.parentElement.closest("ul, ol")) return;
				const rect$1 = el.getBoundingClientRect();
				if (rect$1.width === 0 || rect$1.height === 0) return;
				const items = [];
				const ulPaddingLeftPt = pxToPoints(window.getComputedStyle(el).paddingLeft);
				const marginLeft = ulPaddingLeftPt * .5;
				const textIndent = ulPaddingLeftPt * .5;
				// Recursively process list items with indent levels
				function processListItems(listEl, indentLevel) {
					const directLiElements = Array.from(listEl.children).filter(child => child.tagName === "LI");
					directLiElements.forEach((li) => {
						// Get text content of this li (excluding nested lists)
						const textNodes = [];
						li.childNodes.forEach(node => {
							if (node.nodeType === Node.TEXT_NODE) {
								textNodes.push(node.textContent || "");
							} else if (node.nodeType === Node.ELEMENT_NODE && node.tagName !== "UL" && node.tagName !== "OL") {
								textNodes.push(node.textContent || "");
							}
						});
						const liText = textNodes.join("").trim();
						if (liText) {
							const liComputed = window.getComputedStyle(li);
							const cleanText = liText.replace(/^[•\-*▪▸]\s*/, "");

							if (indentLevel === 0) {
								// Top level: add colored checkmark as separate text run, then content
								// Get primary color from CSS variable or use default
								const primaryColor = getComputedStyle(document.documentElement).getPropertyValue('--theme-primary').trim() || '#0891B2';
								const checkmarkColor = primaryColor.replace('#', '');
								items.push({
									text: '✓ ',
									options: {
										fontSize: pxToPoints(liComputed.fontSize),
										fontFace: liComputed.fontFamily.split(",")[0].replace(/['"]/g, "").trim(),
										color: checkmarkColor,
										bullet: false,
										breakLine: false
									}
								});
								items.push({
									text: cleanText,
									options: {
										fontSize: pxToPoints(liComputed.fontSize),
										fontFace: liComputed.fontFamily.split(",")[0].replace(/['"]/g, "").trim(),
										color: rgbToHex(liComputed.color),
										bullet: false,
										indentLevel: indentLevel,
										breakLine: true,
										lineSpacingMultiple: 1.5
									}
								});
							} else {
								// Nested levels: no bullet
								const run = {
									text: cleanText,
									options: {
										fontSize: pxToPoints(liComputed.fontSize),
										fontFace: liComputed.fontFamily.split(",")[0].replace(/['"]/g, "").trim(),
										color: rgbToHex(liComputed.color),
										bullet: false,
										indentLevel: indentLevel,
										breakLine: true,
										lineSpacingMultiple: 1.5
									}
								};
								items.push(run);
							}
						}
						// Process nested lists
						const nestedLists = Array.from(li.children).filter(child => child.tagName === "UL" || child.tagName === "OL");
						nestedLists.forEach(nestedList => {
							processListItems(nestedList, indentLevel + 1);
							processed.add(nestedList);
						});
						processed.add(li);
					});
				}
				processListItems(el, 0);
				// Remove breakLine from last item
				if (items.length > 0) {
					delete items[items.length - 1].options.breakLine;
				}
				const computed$1 = window.getComputedStyle(el);
				elements.push({
					type: "list",
					items,
					position: rectToXYWH(rect$1),
					style: {
						fontSize: pxToPoints(computed$1.fontSize),
						fontFace: computed$1.fontFamily.split(",")[0].replace(/['"]/g, "").trim(),
						color: rgbToHex(computed$1.color),
						transparency: extractAlpha(computed$1.color),
						align: computed$1.textAlign === "start" ? "left" : computed$1.textAlign,
						lineSpacingMultiple: 1.5,
						paraSpaceBefore: 0,
						paraSpaceAfter: pxToPoints(computed$1.marginBottom),
						margin: [
							marginLeft,
							0,
							0,
							0
						]
					}
				});
				processed.add(el);
				return;
			}
			if (el.tagName === "PRE") {
				const rect$1 = el.getBoundingClientRect();
				if (rect$1.width === 0 || rect$1.height === 0) return;
				const computed$1 = window.getComputedStyle(el);
				const codeEl = el.querySelector("code");
				const codeComputed = codeEl ? window.getComputedStyle(codeEl) : computed$1;
				const baseFontSize = pxToPoints(codeComputed.fontSize);
				const baseFontFace = codeComputed.fontFamily.split(",")[0].replace(/['"]/g, "").trim();
				const baseColor = rgbToHex(codeComputed.color);
				const runs = [];
				// Helper to extract text runs with syntax highlighting colors
				function extractCodeRuns(node, inherited) {
					if (node.nodeType === Node.TEXT_NODE) {
						const text = node.textContent || "";
						if (text) {
							// Split by newlines to handle line breaks
							const parts = text.split(/(\n)/);
							parts.forEach((part) => {
								if (part === "\n") {
									if (runs.length > 0) {
										runs[runs.length - 1].options.breakLine = true;
									}
								} else if (part) {
									runs.push({
										text: part,
										options: {
											fontSize: baseFontSize,
											fontFace: baseFontFace,
											color: inherited.color || baseColor
										}
									});
								}
							});
						}
					} else if (node.nodeType === Node.ELEMENT_NODE) {
						const nodeEl = node;
						const nodeComputed = window.getComputedStyle(nodeEl);
						const nodeColor = rgbToHex(nodeComputed.color);
						const newInherited = { color: nodeColor !== baseColor ? nodeColor : inherited.color };
						nodeEl.childNodes.forEach((child) => extractCodeRuns(child, newInherited));
					}
				}
				const sourceEl = codeEl || el;
				sourceEl.childNodes.forEach((child) => extractCodeRuns(child, { color: null }));
				// Remove trailing empty runs and ensure no trailing breakLine
				while (runs.length > 0 && !runs[runs.length - 1].text.trim()) {
					runs.pop();
				}
				if (runs.length > 0) {
					delete runs[runs.length - 1].options.breakLine;
				}
				elements.push({
					type: "p",
					text: runs,
					position: rectToXYWH(rect$1),
					style: {
						fontSize: baseFontSize,
						fontFace: baseFontFace,
						color: baseColor,
						align: "left",
						lineSpacing: codeComputed.lineHeight && codeComputed.lineHeight !== "normal" ? pxToPoints(codeComputed.lineHeight) : null,
						paraSpaceBefore: pxToPoints(computed$1.marginTop),
						paraSpaceAfter: pxToPoints(computed$1.marginBottom),
						margin: [
							pxToPoints(computed$1.paddingLeft),
							pxToPoints(computed$1.paddingRight),
							pxToPoints(computed$1.paddingBottom),
							pxToPoints(computed$1.paddingTop)
						]
					}
				});
				if (codeEl) processed.add(codeEl);
				processed.add(el);
				return;
			}
			if (!SUPPORTED_TEXT_TAGS.includes(el.tagName)) return;
			if (el.closest("svg")) {
				processed.add(el);
				return;
			}
			const rect = el.getBoundingClientRect();
			const text = el.textContent.trim();
			if (rect.width === 0 || rect.height === 0 || !text) return;
			if (el.tagName !== "LI" && /^[•\-*▪▸○●◆◇■□]\s/.test(text.trimStart())) {
				errors.push(`Text element <${el.tagName.toLowerCase()}> starts with bullet symbol "${text.substring(0, 20)}...". Use <ul> or <ol> lists instead of manual bullet symbols.`);
				return;
			}
			const computed = window.getComputedStyle(el);
			const rotation = getRotation(computed.transform, computed.writingMode);
			const { x, y, w, h } = getPositionAndSize(el, rect, rotation);
			const baseStyle = {
				fontSize: pxToPoints(computed.fontSize),
				fontFace: computed.fontFamily.split(",")[0].replace(/['"]/g, "").trim(),
				color: rgbToHex(computed.color),
				align: computed.textAlign === "start" ? "left" : computed.textAlign,
				lineSpacing: pxToPoints(computed.lineHeight),
				paraSpaceBefore: pxToPoints(computed.marginTop),
				paraSpaceAfter: pxToPoints(computed.marginBottom),
				margin: [
					pxToPoints(computed.paddingLeft),
					pxToPoints(computed.paddingRight),
					pxToPoints(computed.paddingBottom),
					pxToPoints(computed.paddingTop)
				]
			};
			const transparency = extractAlpha(computed.color);
			if (transparency !== null) baseStyle.transparency = transparency;
			if (rotation !== null) baseStyle.rotate = rotation;
			const hasFormatting = el.querySelector("b, i, u, strong, em, span, br");
			const elementType = el.tagName.toLowerCase();
			if (hasFormatting) {
				const transformStr = computed.textTransform;
				const runs = parseInlineFormatting(el, {}, [], (str) => applyTextTransform(str, transformStr), errors);
				const adjustedStyle = { ...baseStyle };
				if (adjustedStyle.lineSpacing && typeof adjustedStyle.fontSize === "number") {
					const maxFontSize = Math.max(adjustedStyle.fontSize, ...runs.map((r) => typeof r.options?.fontSize === "number" ? r.options.fontSize : 0));
					if (maxFontSize > adjustedStyle.fontSize) adjustedStyle.lineSpacing = maxFontSize * (adjustedStyle.lineSpacing / adjustedStyle.fontSize);
				}
				elements.push({
					type: elementType,
					text: runs,
					position: {
						x: pxToInch(x),
						y: pxToInch(y),
						w: pxToInch(w),
						h: pxToInch(h)
					},
					style: adjustedStyle
				});
			} else {
				const textTransform = computed.textTransform;
				const transformedText = applyTextTransform(text, textTransform);
				const isBold = computed.fontWeight === "bold" || parseInt(computed.fontWeight) >= 600;
				elements.push({
					type: elementType,
					text: transformedText,
					position: {
						x: pxToInch(x),
						y: pxToInch(y),
						w: pxToInch(w),
						h: pxToInch(h)
					},
					style: {
						...baseStyle,
						bold: isBold && !shouldSkipBold(computed.fontFamily),
						italic: computed.fontStyle === "italic",
						underline: computed.textDecoration.includes("underline")
					}
				});
			}
			processed.add(el);
		});
		const html = document.documentElement.outerHTML;
		return {
			background,
			elements,
			placeholders,
			errors,
			html,
			screenshot: ""
		};
	}

//#endregion
exports.BALANCE_TEXT_ATTR = BALANCE_TEXT_ATTR;
exports.PT_PER_PX = PT_PER_PX;
exports.PX_PER_IN = PX_PER_IN;
exports.SINGLE_WEIGHT_FONTS = SINGLE_WEIGHT_FONTS;
exports.applyTextTransform = applyTextTransform;
exports.balanceAllText = balanceAllText;
exports.balanceText = balanceText;
exports.extractAlpha = extractAlpha;
exports.extractSlideDataInBrowser = extractSlideDataInBrowser;
exports.getPositionAndSize = getPositionAndSize;
exports.getRotation = getRotation;
exports.init = init;
exports.parseBoxShadow = parseBoxShadow;
exports.parseInlineFormatting = parseInlineFormatting;
exports.pxToInch = pxToInch;
exports.pxToPoints = pxToPoints;
exports.rectToXYWH = rectToXYWH;
exports.rgbToHex = rgbToHex;
exports.shouldSkipBold = shouldSkipBold;
exports.validateAndMakeCorrections = validateAndMakeCorrections;
return exports;
})({});