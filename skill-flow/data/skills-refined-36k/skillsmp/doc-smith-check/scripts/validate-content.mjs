import { readFile, access, readdir, stat } from "node:fs/promises";
import { constants } from "node:fs";
import { parse as yamlParse } from "yaml";
import path from "node:path";
import {
  getPaths,
  ERROR_CODES,
  collectDocumentPaths,
  loadConfigFromFile,
} from "./utils.mjs";

const ASSETS_DIR_NAME = "assets";

/**
 * Document content validator class
 */
class DocumentContentValidator {
  constructor(yamlPath, docsDir, docs = undefined, options = {}) {
    const PATHS = getPaths();
    this.yamlPath = yamlPath || PATHS.DOCUMENT_STRUCTURE;
    this.docsDir = docsDir || PATHS.DOCS_DIR;
    this.PATHS = PATHS;
    this.docsFilter = docs ? new Set(docs) : null;
    this.checkSlots = options.checkSlots || false;
    this.errors = {
      fatal: [],
      fixable: [],
      warnings: [],
    };
    this.stats = {
      totalDocs: 0,
      checkedDocs: 0,
      totalLinks: 0,
      totalImages: 0,
      localImages: 0,
      remoteImages: 0,
      brokenLinks: 0,
      missingImages: 0,
      inaccessibleRemoteImages: 0,
      unreplacedSlots: 0,
      invalidSlotPaths: 0,
      missingSlotImages: 0,
    };
    this.documents = [];
    this.documentPaths = new Set();
    this.remoteImageCache = new Map();
    this.workspaceConfig = null; // Cache workspace config
  }

  /**
   * Load workspace config (lazy loading)
   */
  async loadWorkspaceConfig() {
    if (this.workspaceConfig === null) {
      this.workspaceConfig = (await loadConfigFromFile()) || {};
    }
    return this.workspaceConfig;
  }

  /**
   * Load translateLanguages config (lazy loading)
   */
  async loadTranslateLanguages() {
    const config = await this.loadWorkspaceConfig();
    return config.translateLanguages || [];
  }

  /**
   * Execute full validation
   */
  async validate(checkRemoteImages = true) {
    try {
      // Layer 1: Load document structure and validate file existence
      await this.loadDocumentStructure();
      await this.validateDocumentFiles();

      // Layer 2-4: Check document content one by one
      for (const doc of this.documents) {
        await this.validateDocument(doc, checkRemoteImages);
      }

      return this.getResult();
    } catch (error) {
      this.errors.fatal.push({
        type: "VALIDATION_ERROR",
        message: `Validation error: ${error.message}`,
      });
      return this.getResult();
    }
  }

  /**
   * Layer 1: Load document structure
   */
  async loadDocumentStructure() {
    try {
      const content = await readFile(this.yamlPath, "utf8");
      const data = yamlParse(content);

      if (!data.documents || !Array.isArray(data.documents)) {
        throw new Error(`${this.yamlPath} missing documents field or format error`);
      }

      // Use shared tool to collect document paths and metadata
      const docsWithMeta = collectDocumentPaths(data.documents, { collectMetadata: true });

      // Convert to internal format
      for (const doc of docsWithMeta) {
        // If docs filter is specified, only add matching documents
        if (this.docsFilter && !this.docsFilter.has(doc.displayPath)) {
          // Still need to add to documentPaths for link validation
          this.documentPaths.add(doc.displayPath);
          continue;
        }

        this.documents.push({
          path: doc.displayPath,
          filePath: doc.path,
          title: doc.title || "Unknown document",
        });
        this.documentPaths.add(doc.displayPath);
      }

      this.stats.totalDocs = this.documents.length;
    } catch (error) {
      if (error.code === "ENOENT") {
        throw new Error(`File not found: ${this.yamlPath}`);
      }
      throw error;
    }
  }

  /**
   * Layer 1: Validate document file existence
   */
  async validateDocumentFiles() {
    for (const doc of this.documents) {
      const docFolder = path.join(this.docsDir, doc.filePath);

      // Check 1: Folder exists and is a directory
      let folderExists = false;
      try {
        const stats = await stat(docFolder);
        if (!stats.isDirectory()) {
          this.errors.fatal.push({
            type: "INVALID_DOCUMENT_FOLDER",
            path: doc.path,
            filePath: docFolder,
            message: `Path is not a folder: ${doc.path}`,
            suggestion: "Please ensure path points to a folder",
          });
          continue;
        }
        folderExists = true;
      } catch (_error) {
        this.errors.fatal.push({
          type: "MISSING_DOCUMENT_FOLDER",
          path: doc.path,
          filePath: docFolder,
          message: `Document folder missing: ${doc.path}`,
          suggestion: `Please generate this document folder in the specified format`,
        });
        continue;
      }

      // Check 2: .meta.yaml exists and has correct format
      if (folderExists) {
        await this.validateMetaFile(docFolder, doc);

        // Check 3: At least one language file exists
        await this.validateLanguageFiles(docFolder, doc);
      }
    }
  }

  /**
   * Validate .meta.yaml
   */
  async validateMetaFile(docFolder, doc) {
    const metaPath = path.join(docFolder, ".meta.yaml");

    try {
      await access(metaPath, constants.F_OK | constants.R_OK);
    } catch (_error) {
      this.errors.fatal.push({
        type: "MISSING_META_FILE",
        path: doc.path,
        filePath: metaPath,
        message: `.meta.yaml missing: ${doc.path}`,
        suggestion: "Please create .meta.yaml in the document folder",
      });
      return;
    }

    // Read and validate content
    try {
      const content = await readFile(metaPath, "utf8");
      const meta = yamlParse(content);

      // Required field validation
      const requiredFields = ["kind", "source", "default"];
      for (const field of requiredFields) {
        if (!meta[field]) {
          this.errors.fatal.push({
            type: "INVALID_META",
            path: doc.path,
            field,
            message: `.meta.yaml missing required field "${field}": ${doc.path}`,
            suggestion: `Add ${field} field to .meta.yaml`,
          });
        }
      }

      // kind value validation
      if (meta.kind && meta.kind !== "doc") {
        this.errors.fatal.push({
          type: "INVALID_META",
          path: doc.path,
          field: "kind",
          message: `.meta.yaml kind should be "doc", currently "${meta.kind}"`,
          suggestion: "Change to kind: doc",
        });
      }

      // source and project locale consistency validation
      if (meta.source) {
        const config = await this.loadWorkspaceConfig();
        const projectLocale = config?.locale;
        if (projectLocale && meta.source !== projectLocale) {
          this.errors.fatal.push({
            type: ERROR_CODES.SOURCE_LOCALE_MISMATCH,
            path: doc.path,
            source: meta.source,
            locale: projectLocale,
            message: `Document source (${meta.source}) does not match project locale (${projectLocale}): ${doc.path}`,
            suggestion: `Change document source to "${projectLocale}", or regenerate the main language version of this document`,
          });
        }
      }
    } catch (error) {
      this.errors.fatal.push({
        type: "INVALID_META",
        path: doc.path,
        message: `.meta.yaml format error: ${error.message}`,
        suggestion: "Check if YAML syntax is correct",
      });
    }
  }

  /**
   * Validate language files
   */
  async validateLanguageFiles(docFolder, doc) {
    try {
      const files = await readdir(docFolder);
      const langFiles = files.filter(
        (f) => f.endsWith(".md") && !f.startsWith(".") && /^[a-z]{2}(-[A-Z]{2})?\.md$/.test(f),
      );

      if (langFiles.length === 0) {
        this.errors.fatal.push({
          type: "MISSING_LANGUAGE_FILE",
          path: doc.path,
          message: `No language version files: ${doc.path}`,
          suggestion: "Please generate at least one language version file (e.g. zh.md, en.md)",
        });
        return;
      }

      // Check if default and source language files exist
      const metaPath = path.join(docFolder, ".meta.yaml");
      try {
        const metaContent = await readFile(metaPath, "utf8");
        const meta = yamlParse(metaContent);

        if (meta.default) {
          const defaultFile = `${meta.default}.md`;
          if (!langFiles.includes(defaultFile)) {
            this.errors.fatal.push({
              type: "MISSING_DEFAULT_LANGUAGE",
              path: doc.path,
              defaultLang: meta.default,
              message: `Default language file missing: ${defaultFile}`,
              suggestion: `Generate ${defaultFile} or modify the default field in .meta.yaml`,
            });
          }
        }

        if (meta.source) {
          const sourceFile = `${meta.source}.md`;
          if (!langFiles.includes(sourceFile)) {
            this.errors.fatal.push({
              type: "MISSING_SOURCE_LANGUAGE",
              path: doc.path,
              sourceLang: meta.source,
              message: `Source language file missing: ${sourceFile}`,
              suggestion: `Generate ${sourceFile} or modify the source field in .meta.yaml`,
            });
          }
        }

        // Check if target language files configured in translateLanguages exist
        const translateLanguages = await this.loadTranslateLanguages();
        if (translateLanguages.length > 0) {
          for (const lang of translateLanguages) {
            // Skip source language (source language doesn't need to be a translation target)
            if (lang === meta.source) continue;

            const langFile = `${lang}.md`;
            if (!langFiles.includes(langFile)) {
              this.errors.fatal.push({
                type: ERROR_CODES.MISSING_TRANSLATE_LANGUAGE,
                path: doc.path,
                lang,
                message: `Translation language file missing: ${langFile}`,
                suggestion: `Please translate document to ${lang} language, or remove ${lang} from translateLanguages in config.yaml`,
              });
            }
          }
        }
      } catch (_error) {
        // .meta.yaml errors already reported in validateMetaFile
      }
    } catch (error) {
      this.errors.fatal.push({
        type: "READ_FOLDER_ERROR",
        path: doc.path,
        message: `Cannot read document folder: ${error.message}`,
      });
    }
  }

  /**
   * Layer 2-4: Validate single document content
   */
  async validateDocument(doc, checkRemoteImages) {
    const docFolder = path.join(this.docsDir, doc.filePath);

    try {
      // Read .meta.yaml to get language list
      const metaPath = path.join(docFolder, ".meta.yaml");
      const metaContent = await readFile(metaPath, "utf8");
      const _meta = yamlParse(metaContent);

      // Get all language files
      const files = await readdir(docFolder);
      const langFiles = files.filter((f) => f.endsWith(".md") && !f.startsWith("."));

      // Check each language version
      for (const langFile of langFiles) {
        const fullPath = path.join(docFolder, langFile);
        const content = await readFile(fullPath, "utf8");

        this.stats.checkedDocs++;

        // Layer 2: Content parsing and checking
        this.checkEmptyDocument(content, doc, langFile);
        this.checkHeadingHierarchy(content, doc, langFile);

        // Layer 3: Link and image validation
        await this.validateLinks(content, doc, langFile);
        await this.validateImages(content, doc, langFile, checkRemoteImages);

        // Layer 5: AFS image slot validation (when checkSlots is enabled)
        if (this.checkSlots) {
          await this.validateImageSlots(content, doc, langFile);
        }
      }
    } catch (_error) {
      // Errors already reported in Layer 1
    }
  }

  /**
   * Layer 4: Empty document detection
   */
  checkEmptyDocument(content, doc, langFile) {
    // Remove all headings
    let cleaned = content.replace(/^#{1,6}\s+.+$/gm, "");
    // Remove whitespace characters
    cleaned = cleaned.replace(/\s+/g, "");

    if (cleaned.length < 50) {
      this.errors.fatal.push({
        type: "EMPTY_DOCUMENT",
        path: doc.path,
        langFile,
        message: `Empty document: ${doc.path} (${langFile})`,
        suggestion: `Document content insufficient (less than 50 characters), please add substantial content or remove from structure`,
      });
    }
  }

  /**
   * Layer 4: Heading hierarchy check
   */
  checkHeadingHierarchy(content, doc, langFile) {
    // First remove content in code blocks to avoid false positives
    const contentWithoutCodeBlocks = this.removeCodeBlocks(content);

    const headingRegex = /^(#{1,6})\s+(.+)$/gm;
    const headings = [];

    for (const match of contentWithoutCodeBlocks.matchAll(headingRegex)) {
      headings.push({
        level: match[1].length,
        text: match[2],
        line: contentWithoutCodeBlocks.substring(0, match.index).split("\n").length,
      });
    }

    for (let i = 1; i < headings.length; i++) {
      const prev = headings[i - 1];
      const curr = headings[i];

      // Check for level skipping
      if (curr.level > prev.level + 1) {
        this.errors.fatal.push({
          type: "HEADING_SKIP",
          path: doc.path,
          langFile,
          line: curr.line,
          message: `Heading skipped from H${prev.level} to H${curr.level}`,
          suggestion: `Consider changing "${"#".repeat(curr.level)} ${curr.text}" to "${"#".repeat(prev.level + 1)} ${curr.text}"`,
        });
      }
    }
  }

  /**
   * Remove content in Markdown code blocks
   */
  removeCodeBlocks(content) {
    // Remove fenced code blocks (```...```)
    let result = content.replace(/^```[\s\S]*?^```$/gm, "");

    // Remove indented code blocks (lines starting with 4 spaces or 1 tab)
    result = result.replace(/^( {4}|\t).+$/gm, "");

    return result;
  }

  /**
   * Get code block position ranges
   * @returns {Array<{start: number, end: number}>} Array of code block start/end positions
   */
  getCodeBlockRanges(content) {
    const ranges = [];

    // Match fenced code blocks (```...```)
    const fencedCodeRegex = /^```[\s\S]*?^```$/gm;

    for (const match of content.matchAll(fencedCodeRegex)) {
      ranges.push({
        start: match.index,
        end: match.index + match[0].length,
      });
    }

    // Match inline code blocks (`...`)
    const inlineCodeRegex = /`[^`\n]+`/g;
    for (const match of content.matchAll(inlineCodeRegex)) {
      ranges.push({
        start: match.index,
        end: match.index + match[0].length,
      });
    }

    // Match indented code blocks (lines starting with 4 spaces or 1 tab)
    const indentedCodeRegex = /^( {4}|\t).+$/gm;
    for (const match of content.matchAll(indentedCodeRegex)) {
      ranges.push({
        start: match.index,
        end: match.index + match[0].length,
      });
    }

    return ranges;
  }

  /**
   * Check if position is inside a code block
   * @param {number} position - Position to check
   * @param {Array<{start: number, end: number}>} ranges - Code block range array
   * @returns {boolean} Whether inside a code block
   */
  isInCodeBlock(position, ranges) {
    return ranges.some((range) => position >= range.start && position < range.end);
  }

  /**
   * Layer 3: Validate internal links
   */
  async validateLinks(content, doc, langFile) {
    // Get code block position ranges
    const codeBlockRanges = this.getCodeBlockRanges(content);

    const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;

    for (const match of content.matchAll(linkRegex)) {
      // Check if link is inside code block, skip if so
      if (this.isInCodeBlock(match.index, codeBlockRanges)) {
        continue;
      }

      const linkText = match[1];
      const linkUrl = match[2];

      this.stats.totalLinks++;

      // Ignore external links and anchor links
      if (
        linkUrl.startsWith("http://") ||
        linkUrl.startsWith("https://") ||
        linkUrl.startsWith("#")
      ) {
        continue;
      }

      // Ignore resource file links
      if (this.isResourceFile(linkUrl)) {
        continue;
      }

      // All other links are treated as internal document links
      await this.validateInternalLink(linkUrl, doc, linkText, langFile);
    }
  }

  /**
   * Check if link points to a resource file (non-document)
   */
  isResourceFile(url) {
    // 移除查询参数和锚点
    const cleanUrl = url.split("?")[0].split("#")[0].toLowerCase();
    // 资源文件扩展名
    const resourceExtensions = [
      ".png",
      ".jpg",
      ".jpeg",
      ".gif",
      ".svg",
      ".webp",
      ".ico",
      ".bmp",
      ".pdf",
      ".doc",
      ".docx",
      ".xls",
      ".xlsx",
      ".ppt",
      ".pptx",
      ".zip",
      ".tar",
      ".gz",
      ".rar",
      ".7z",
      ".mp3",
      ".mp4",
      ".wav",
      ".avi",
      ".mov",
      ".webm",
      ".json",
      ".xml",
      ".csv",
      ".txt",
      ".js",
      ".ts",
      ".css",
      ".scss",
      ".less",
      ".py",
      ".rb",
      ".go",
      ".rs",
      ".java",
      ".c",
      ".cpp",
      ".h",
    ];
    return resourceExtensions.some((ext) => cleanUrl.endsWith(ext));
  }

  /**
   * Validate internal link
   */
  async validateInternalLink(linkUrl, doc, linkText, langFile) {
    let targetPath;

    // Remove anchor part for format checking
    const urlWithoutAnchor = linkUrl.split("#")[0];

    // Check if link format is correct: internal links should not contain .md suffix
    const langSuffixPattern = /\/[a-z]{2}(-[A-Z]{2})?\.md$/; // Match /en.md, /zh.md, /en-US.md
    const mdSuffixPattern = /\.md$/;

    if (mdSuffixPattern.test(urlWithoutAnchor)) {
      // Link contains .md suffix, this is a format error
      // If it's a language suffix pattern, remove the entire /xx.md part; otherwise just remove .md
      const isLangSuffix = langSuffixPattern.test(urlWithoutAnchor);
      const suggestedLink = isLangSuffix
        ? urlWithoutAnchor.replace(langSuffixPattern, "")
        : urlWithoutAnchor.replace(mdSuffixPattern, "");

      this.stats.brokenLinks++;
      this.errors.fatal.push({
        type: ERROR_CODES.INVALID_LINK_FORMAT,
        path: doc.path,
        langFile,
        link: linkUrl,
        linkText,
        message: `Internal link format error: [${linkText}](${linkUrl})`,
        suggestion: `Link should not contain .md suffix, suggest changing to: ${suggestedLink}`,
      });
      return;
    }

    // Link format is correct, continue to validate if target exists
    const cleanLinkUrl = urlWithoutAnchor;

    // If link is only anchor (like #section), cleanLinkUrl will be empty string, skip check
    if (!cleanLinkUrl) {
      return;
    }

    if (cleanLinkUrl.startsWith("/")) {
      // Absolute path
      targetPath = cleanLinkUrl;
    } else {
      // Relative path: based on document's "parent directory"
      // Document /getting-started/claude-code's parent directory is /getting-started
      // Example: document /getting-started/claude-code, link ../getting-started -> /getting-started
      // Example: document /getting-started, link ./claude-code -> /getting-started/claude-code
      const docDir = path.dirname(doc.path); // /getting-started/claude-code -> /getting-started
      const upLevels = (cleanLinkUrl.match(/\.\.\//g) || []).length;
      const currentDepth = docDir === "/" ? 0 : docDir.split("/").filter((p) => p).length;

      if (upLevels > currentDepth) {
        this.stats.brokenLinks++;
        this.errors.fatal.push({
          type: "BROKEN_LINK",
          path: doc.path,
          langFile,
          link: linkUrl,
          linkText,
          message: `Internal link path exceeds root directory: [${linkText}](${linkUrl})`,
          suggestion: `Link goes up ${upLevels} levels, but current document's directory is only at level ${currentDepth}`,
        });
        return;
      }

      // Merge document's parent directory with relative link
      targetPath = path.posix.normalize(path.posix.join(docDir, cleanLinkUrl));
      if (!targetPath.startsWith("/")) {
        targetPath = `/${targetPath}`;
      }
    }

    if (!this.documentPaths.has(targetPath)) {
      this.stats.brokenLinks++;
      this.errors.fatal.push({
        type: "BROKEN_LINK",
        path: doc.path,
        langFile,
        link: linkUrl,
        linkText,
        targetPath,
        message: `Internal broken link: [${linkText}](${linkUrl})`,
        suggestion: `Target document ${targetPath} does not exist`,
      });
    }
  }

  /**
   * Layer 3: Validate images
   */
  async validateImages(content, doc, langFile, checkRemoteImages) {
    // Get code block position ranges
    const codeBlockRanges = this.getCodeBlockRanges(content);

    const imageRegex = /!\[([^\]]*)\]\(([^)]+)\)/g;

    for (const match of content.matchAll(imageRegex)) {
      // Check if image is inside code block, skip if so
      if (this.isInCodeBlock(match.index, codeBlockRanges)) {
        continue;
      }

      const altText = match[1];
      const imageUrl = match[2];

      this.stats.totalImages++;

      // Categorize: local vs remote
      if (imageUrl.startsWith("http://") || imageUrl.startsWith("https://")) {
        // Remote image
        this.stats.remoteImages++;
        if (checkRemoteImages) {
          await this.validateRemoteImage(imageUrl, doc, altText, langFile);
        }
      } else {
        // Local image
        this.stats.localImages++;
        await this.validateLocalImage(imageUrl, doc, altText, langFile);
      }
    }
  }

  /**
   * Validate local image
   * Only relative paths allowed, absolute paths (like /sources/...) not allowed
   */
  async validateLocalImage(imageUrl, doc, altText, langFile) {
    // Check if absolute path (starts with /) - not allowed
    if (imageUrl.startsWith("/")) {
      this.stats.missingImages++;
      this.errors.fatal.push({
        type: ERROR_CODES.ABSOLUTE_IMAGE_PATH_NOT_ALLOWED,
        path: doc.path,
        langFile,
        imageUrl,
        altText,
        message: `Image absolute path not allowed: ${imageUrl}`,
        suggestion: `Please use relative path to access image, calculate correct relative path based on document location`,
      });
      return;
    }

    // Relative path handling: resolve based on document location
    const fullDocPath = path.join(doc.filePath, langFile);
    const docDir = path.dirname(path.join(this.docsDir, fullDocPath));
    const imagePath = path.resolve(docDir, imageUrl);

    // Check if file exists
    try {
      await access(imagePath, constants.F_OK);
      // Image exists, relative path is correct

      // When checkSlots is enabled, validate image paths in assets directory
      if (this.checkSlots) {
        await this.validateAssetImagePath(imageUrl, doc, langFile);
      }
    } catch (_error) {
      this.stats.missingImages++;
      this.errors.fatal.push({
        type: "MISSING_IMAGE",
        path: doc.path,
        langFile,
        imageUrl,
        altText,
        message: `Local image not found: ${imageUrl}`,
        suggestion: `Check image path or remove image reference`,
      });
    }
  }

  /**
   * Validate remote image
   */
  async validateRemoteImage(imageUrl, doc, altText, langFile) {
    // Check cache
    if (this.remoteImageCache.has(imageUrl)) {
      const cached = this.remoteImageCache.get(imageUrl);
      if (!cached.accessible) {
        this.stats.inaccessibleRemoteImages++;
        this.errors.warnings.push({
          type: "REMOTE_IMAGE_INACCESSIBLE",
          path: doc.path,
          langFile,
          imageUrl,
          altText,
          statusCode: cached.statusCode,
          error: cached.error,
          message: `Remote image inaccessible: ${imageUrl}`,
          suggestion: `Check if URL is correct, or replace with accessible image`,
        });
      }
      return;
    }

    // Check remote image accessibility
    const result = await this.checkRemoteImage(imageUrl);
    this.remoteImageCache.set(imageUrl, result);

    if (!result.accessible) {
      this.stats.inaccessibleRemoteImages++;
      this.errors.warnings.push({
        type: "REMOTE_IMAGE_INACCESSIBLE",
        path: doc.path,
        langFile,
        imageUrl,
        altText,
        statusCode: result.statusCode,
        error: result.error,
        message: `Remote image inaccessible: ${imageUrl}`,
        suggestion: `Check if URL is correct, or replace with accessible image`,
      });
    }
  }

  /**
   * Check remote image (HTTP HEAD request)
   */
  async checkRemoteImage(url, timeout = 3000) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
      const response = await fetch(url, {
        method: "HEAD",
        signal: controller.signal,
        headers: {
          "User-Agent": "DocSmith-Content-Checker/1.0",
        },
      });

      clearTimeout(timeoutId);

      return {
        accessible: response.ok,
        statusCode: response.status,
        statusText: response.statusText,
      };
    } catch (error) {
      clearTimeout(timeoutId);

      return {
        accessible: false,
        error: error.message,
        isTimeout: error.name === "AbortError",
      };
    }
  }

  /**
   * Validate AFS image slots (when checkSlots is enabled)
   * Check if document contains unreplaced placeholders
   */
  async validateImageSlots(content, doc, langFile) {
    // Get code block position ranges
    const codeBlockRanges = this.getCodeBlockRanges(content);

    // Match all slots: <!-- afs:image id="xxx" ... -->
    const slotRegex = /<!--\s*afs:image\s+id="([^"]+)"(?:\s+key="([^"]+)")?(?:\s+desc="([^"]+)")?\s*-->/g;

    for (const match of content.matchAll(slotRegex)) {
      // Skip slots inside code blocks
      if (this.isInCodeBlock(match.index, codeBlockRanges)) {
        continue;
      }

      const slotId = match[1];
      this.stats.unreplacedSlots++;

      this.errors.fatal.push({
        type: ERROR_CODES.UNREPLACED_IMAGE_SLOT,
        path: doc.path,
        langFile,
        slotId,
        message: `AFS image slot not replaced: ${slotId}`,
        suggestion: `Please use generate-slot-image to generate image`,
      });
    }
  }

  /**
   * Validate image path level is correct (for images in assets directory)
   * @param {string} imageUrl - Image URL
   * @param {Object} doc - Document object
   * @param {string} langFile - Language file name
   */
  async validateAssetImagePath(imageUrl, doc, langFile) {
    // Only check images pointing to assets directory
    if (!imageUrl.includes(`/${ASSETS_DIR_NAME}/`)) {
      return;
    }

    // Extract key and filename from imageUrl
    // Format: ../../assets/{key}/images/{locale}.png or ../../../assets/{key}/images/{locale}.png
    const assetsMatch = imageUrl.match(/(?:\.\.\/)+assets\/([^/]+)\/images\/([^/]+)$/);
    if (!assetsMatch) {
      return;
    }

    const key = assetsMatch[1];
    const imageName = assetsMatch[2];

    // Calculate document depth
    // Document path format: /overview or /api/auth
    // Actual file path: docs/overview/zh.md or docs/api/auth/zh.md
    // Accessing assets from language file needs to consider the language file's own level
    const docPathParts = doc.path.split("/").filter((p) => p);
    const docPathDepth = docPathParts.length;
    // +1 because language file (like zh.md) itself occupies one level
    const totalDepth = docPathDepth + 1;

    // Calculate expected relative path level
    // Depth 1 (like /overview) file docs/overview/zh.md: ../../assets/...
    // Depth 2 (like /api/auth) file docs/api/auth/zh.md: ../../../assets/...
    const expectedPrefix = "../".repeat(totalDepth);
    const expectedPath = `${expectedPrefix}${ASSETS_DIR_NAME}/${key}/images/${imageName}`;

    // Check if actual path matches expected path
    if (imageUrl !== expectedPath) {
      this.stats.invalidSlotPaths++;
      this.errors.fatal.push({
        type: ERROR_CODES.IMAGE_PATH_LEVEL_ERROR,
        path: doc.path,
        langFile,
        imageUrl,
        expectedPath,
        message: `Image path level error: ${imageUrl}`,
        suggestion: `Expected path: ${expectedPath}`,
      });
      return;
    }

    // Check if image file exists
    const assetsDir = path.join(this.PATHS.WORKSPACE_BASE, ASSETS_DIR_NAME);
    const imagePath = path.join(assetsDir, key, "images", imageName);

    try {
      await access(imagePath, constants.F_OK);
    } catch (_error) {
      this.stats.missingSlotImages++;
      this.errors.fatal.push({
        type: ERROR_CODES.MISSING_SLOT_IMAGE,
        path: doc.path,
        langFile,
        imageUrl,
        imagePath,
        message: `Image file missing: ${imageUrl}`,
        suggestion: `Generate image or remove reference`,
      });
    }
  }

  /**
   * Get validation result
   */
  getResult() {
    const hasErrors = this.errors.fatal.length > 0 || this.errors.fixable.length > 0;

    return {
      valid: !hasErrors,
      errors: this.errors,
      stats: this.stats,
    };
  }
}

/**
 * Format output
 * @param {Object} result - Validation result
 * @param {Object} options - Format options
 * @param {boolean} options.checkSlots - Whether AFS image slots were checked
 */
function formatOutput(result, options = {}) {
  const { checkSlots = false } = options;
  let output = "";

  if (result.valid) {
    output += "✅ PASS: Document content check passed\n\n";
    output += "Statistics:\n";
    output += `  Total documents: ${result.stats.totalDocs}\n`;
    output += `  Checked: ${result.stats.checkedDocs}\n`;
    output += `  Internal links: ${result.stats.totalLinks}\n`;
    output += `  Local images: ${result.stats.localImages}\n`;
    output += `  Remote images: ${result.stats.remoteImages}\n`;

    if (checkSlots) {
      output += `  AFS Image Slot check: Enabled\n`;
    }

    if (result.errors.warnings.length > 0) {
      output += `\nWarnings: ${result.errors.warnings.length}\n\n`;
      result.errors.warnings.forEach((warn, idx) => {
        output += `${idx + 1}. ${warn.message}\n`;
        if (warn.path) output += `   Document: ${warn.path}\n`;
        if (warn.langFile) output += `   Language file: ${warn.langFile}\n`;
        if (warn.suggestion) output += `   Suggestion: ${warn.suggestion}\n`;
        output += "\n";
      });
    }

    return output;
  }

  output += "❌ FAIL: Document content has errors\n\n";
  output += "Statistics:\n";
  output += `  Total documents: ${result.stats.totalDocs}\n`;
  output += `  Checked: ${result.stats.checkedDocs}\n`;
  output += `  Fatal errors: ${result.errors.fatal.length}\n`;
  output += `  Fixable errors: ${result.errors.fixable.length}\n`;
  output += `  Warnings: ${result.errors.warnings.length}\n`;

  if (checkSlots) {
    output += `  Unreplaced slots: ${result.stats.unreplacedSlots}\n`;
    output += `  Path level errors: ${result.stats.invalidSlotPaths}\n`;
    output += `  Missing images: ${result.stats.missingSlotImages}\n`;
  }

  output += "\n";

  // FATAL errors
  if (result.errors.fatal.length > 0) {
    output += "Fatal errors (must fix):\n\n";
    result.errors.fatal.forEach((err, idx) => {
      output += `${idx + 1}. ${err.message}\n`;
      if (err.path) output += `   Document: ${err.path}\n`;
      if (err.langFile) output += `   Language file: ${err.langFile}\n`;
      if (err.slotId) output += `   Slot ID: ${err.slotId}\n`;
      if (err.link) output += `   Link: ${err.link}\n`;
      if (err.imageUrl) output += `   Image: ${err.imageUrl}\n`;
      if (err.expectedPath) output += `   Expected path: ${err.expectedPath}\n`;
      if (err.suggestion) output += `   Action: ${err.suggestion}\n`;
      output += "\n";
    });
  }

  // FIXABLE errors
  if (result.errors.fixable.length > 0) {
    output += "Fixable errors (auto-fixed):\n";
    output += "(Fixes applied, files updated)\n\n";
  }

  // WARNINGS
  if (result.errors.warnings.length > 0) {
    output += "Warnings (non-blocking):\n\n";
    result.errors.warnings.forEach((warn, idx) => {
      output += `${idx + 1}. ${warn.message}\n`;
      if (warn.path) output += `   Document: ${warn.path}\n`;
      if (warn.suggestion) output += `   Suggestion: ${warn.suggestion}\n`;
      output += "\n";
    });
  }

  return output;
}

/**
 * Main function - Function Agent
 * @param {Object} params
 * @param {string} params.yamlPath - Document structure YAML file path
 * @param {string} params.docsDir - Document directory path
 * @param {string[]} params.docs - Array of document paths to check, e.g. ['/overview', '/api/introduction'], check all documents if not provided
 * @param {boolean} params.checkRemoteImages - Whether to check remote images
 * @param {boolean} params.checkSlots - Whether to check AFS image slots are replaced
 * @returns {Promise<Object>} - Validation result
 */
export default async function validateDocumentContent({
  yamlPath,
  docsDir,
  docs = undefined,
  checkRemoteImages = true,
  checkSlots = false,
} = {}) {
  const PATHS = getPaths();
  yamlPath = yamlPath || PATHS.DOCUMENT_STRUCTURE;
  docsDir = docsDir || PATHS.DOCS_DIR;
  try {
    const validator = new DocumentContentValidator(yamlPath, docsDir, docs, { checkSlots });
    const result = await validator.validate(checkRemoteImages);

    const formattedOutput = formatOutput(result, { checkSlots });

    return {
      valid: result.valid,
      errors: result.errors,
      stats: result.stats,
      message: formattedOutput,
    };
  } catch (error) {
    return {
      valid: false,
      message: `❌ FAIL: ${error.message}`,
    };
  }
}

// Note: This function is for internal use only, not directly exposed as skill
// External calls through checkContent function in content-checker.mjs
