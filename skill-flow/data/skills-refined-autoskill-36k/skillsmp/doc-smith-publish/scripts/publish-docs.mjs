import { basename, join, relative } from "node:path";
import { publishDocs as publishDocsFn } from "@aigne/publish-docs";
import fs from "fs-extra";
import yaml from "js-yaml";
import { joinURL } from "ufo";

import { getAccessToken, getDiscussKitMountPoint } from "./utils/auth.mjs";
import { CLOUD_SERVICE_URL_PROD } from "./utils/constants.mjs";
import { PATHS } from "./utils/agent-constants.mjs";
import { deploy } from "./utils/deploy.mjs";
import { loadConfigFromFile, saveValueToConfig } from "./utils/config.mjs";
import { ensureTmpDir } from "./utils/files.mjs";
import { getGithubRepoUrl, isValidGithubUrl } from "./utils/git.mjs";
import updateBranding from "./utils/branding.mjs";
import { generateSidebar, loadDocumentStructure } from "./utils/docs.mjs";
import { copyDocumentsToTemp } from "./utils/docs-converter.mjs";

export default async function publishDocs({
  appUrl,
  outputDir = PATHS.PLANNING_DIR,
  "with-branding": withBrandingOption,
  config,
  newWebsite,
}) {
  // Absolute path for file operations (reading docs)
  const docsAbsolutePath = PATHS.DOCS_DIR;
  // Relative path for mediaFolder (relative to cwd for publish-docs library)
  const docsRelativePath = relative(process.cwd(), PATHS.DOCS_DIR) || "./docs";
  // Relative path for tmp directory
  const tmpDirRelative = relative(process.cwd(), PATHS.TMP_DIR) || ".tmp";
  const docsDir = join(tmpDirRelative, "docs");
  let message;
  let shouldWithBranding = withBrandingOption || false;

  try {
    // Load document structure from output directory
    const documentStructure = await loadDocumentStructure(outputDir);
    if (!documentStructure || documentStructure.length === 0) {
      console.warn("⚠️  No document structure found. Sidebar generation may be limited.");
    }

    // move work dir to tmp-dir
    await ensureTmpDir();
    await fs.rm(docsDir, { recursive: true, force: true });
    await fs.mkdir(docsDir, {
      recursive: true,
    });

    // Convert documents from new directory format to publish format
    await copyDocumentsToTemp(docsAbsolutePath, docsDir);

    // Generate _sidebar.md in tmp directory
    const sidebar = generateSidebar(documentStructure || []);
    const tmpSidebarPath = join(docsDir, "_sidebar.md");
    await fs.writeFile(tmpSidebarPath, sidebar, "utf8");

    // ----------------- main publish process flow -----------------------------
    // Check if DOC_DISCUSS_KIT_URL is set in environment variables
    const useEnvAppUrl = !!(process.env.DOC_SMITH_PUBLISH_URL || process.env.DOC_DISCUSS_KIT_URL);

    // Use config from parameters or load from file as fallback
    if (!config) {
      config = await loadConfigFromFile();
    }
    const { projectName, projectDesc, projectLogo, boardId } = config || {};
    appUrl =
      process.env.DOC_SMITH_PUBLISH_URL ||
      process.env.DOC_DISCUSS_KIT_URL ||
      appUrl ||
      config?.appUrl;

    let token = "";
    let locale = config?.locale;

    // Handle newWebsite mode - create a new website for publishing
    if (newWebsite) {
      console.log(`\nCreating a new website for your documentation...`);
      try {
        const { appUrl: homeUrl, token: ltToken, data } = (await deploy("", locale)) || {};

        appUrl = homeUrl;
        token = ltToken;
        locale = data?.preferredLocale || locale;
        shouldWithBranding = true;
      } catch (error) {
        const errorMsg = error?.message || "Unknown error occurred";
        return {
          message: `❌ Failed to create website: ${errorMsg}`,
        };
      }
    }

    // Validate that we have an appUrl at this point
    if (!appUrl) {
      return {
        message: `❌ Missing appUrl: Please provide --appUrl parameter or use --newWebsite to create a new website.`,
      };
    }

    appUrl = appUrl ?? CLOUD_SERVICE_URL_PROD;

    const appUrlInfo = new URL(appUrl);

    const discussKitMountPoint = await getDiscussKitMountPoint(appUrlInfo.origin);
    const discussKitUrl = joinURL(appUrlInfo.origin, discussKitMountPoint);

    console.log(`\nPublishing your documentation to ${discussKitUrl}`);

    const accessToken = await getAccessToken(appUrlInfo.origin, token, locale);

    process.env.DOC_ROOT_DIR = docsDir;

    const sidebarPath = join(docsDir, "_sidebar.md");
    const publishCacheFilePath = join(PATHS.CACHE, "upload-cache.yaml");

    // Get project info from config
    const projectInfo = {
      name: projectName || config?.projectName || basename(process.cwd()),
      description: projectDesc || config?.projectDesc || "",
      icon: projectLogo || config?.projectLogo || "",
    };

    console.log(`Publishing docs collection: ${projectInfo.name || boardId}\n`);

    // Skip image download - use icon URL directly
    if (shouldWithBranding) {
      updateBranding({ appUrl: discussKitUrl, projectInfo, accessToken });
    }

    // Construct boardMeta object
    // In standalone mode, get GitHub URL from git-clone type source in sources array
    // In project mode, use current git repo URL (even if git-clone sources exist as supplements)
    let githubRepoUrl = getGithubRepoUrl();
    if (config?.mode === "standalone") {
      const gitCloneSource = config?.sources?.find((s) => s.type === "git-clone");
      const configUrl = gitCloneSource?.url;
      // Only use config URL if it's a valid GitHub URL
      githubRepoUrl = isValidGithubUrl(configUrl) ? configUrl : "";
    }
    const boardMeta = {
      category: config?.documentPurpose || [],
      githubRepoUrl,
      commitSha: config?.lastGitHead || "",
      languages: [
        ...(config?.locale ? [config.locale] : []),
        ...(config?.translateLanguages || []),
      ].filter((lang, index, arr) => arr.indexOf(lang) === index), // Remove duplicates
    };

    // Load translatedMetadata from cache file
    const translationCachePath = join(PATHS.CACHE, "translation-cache.yaml");
    if (await fs.pathExists(translationCachePath)) {
      try {
        const translationContent = await fs.readFile(translationCachePath, "utf8");
        const translatedMetadata = yaml.load(translationContent);
        if (translatedMetadata) {
          boardMeta.translation = translatedMetadata;
        }
      } catch (error) {
        console.warn(`⚠️  Failed to load translation cache: ${error.message}`);
      }
    } else if (config?.translateLanguages?.length > 0) {
      // Translation file is required when multiple languages are configured
      return {
        message: `❌ Translation cache file not found: ${translationCachePath}\n💡 Please translate the project metadata first before publishing.`,
      };
    }

    const {
      success,
      boardId: newBoardId,
      error,
      docsUrl,
    } = await publishDocsFn({
      sidebarPath,
      accessToken,
      appUrl: discussKitUrl,
      boardId,
      autoCreateBoard: true,
      // Pass additional project information if available
      boardName: projectInfo.name,
      boardDesc: projectInfo.description,
      boardCover: projectInfo.icon,
      mediaFolder: docsRelativePath,
      cacheFilePath: publishCacheFilePath,
      boardMeta,
    });

    // Save values to config.yaml if publish was successful
    if (success) {
      // Save appUrl to config only when not using environment variable
      if (!useEnvAppUrl) {
        await saveValueToConfig("appUrl", appUrlInfo.origin);
      }

      // Save boardId to config if it was auto-created
      if (boardId !== newBoardId) {
        await saveValueToConfig("boardId", newBoardId);
      }
      message = `✅ Documentation published successfully!\n📖 Docs available at: ${docsUrl}`;

      await saveValueToConfig("checkoutId", "", "Checkout ID for document deployment service");
      await saveValueToConfig("shouldSyncBranding", "", "Should sync branding for documentation");
    } else {
      // If the error is 401 or 403, it means the access token is invalid
      try {
        const obj = JSON.parse(error);
        message = `❌ Publishing failed with error: \n💡 ${obj.message || error}`;
      } catch {
        if (error?.includes("401")) {
          message = `❌ Publishing failed due to an authorization error: \n💡 Please run "aigne doc clear" to reset your credentials and try again.`;
        } else if (error?.includes("403")) {
          message = `❌ Publishing failed due to an authorization error: \n💡 You're not the creator of this document (Board ID: ${boardId}). You can change the board ID and try again. \n💡 Or run "aigne doc clear" to reset your credentials and try again.`;
        }
      }
    }

    // clean up tmp work dir
    await fs.rm(tmpDirRelative, { recursive: true, force: true });
  } catch (error) {
    message = `❌ Sorry, I encountered an error while publishing your documentation: \n\n${error.message}`;

    // clean up tmp work dir in case of error
    try {
      await fs.rm(tmpDirRelative, { recursive: true, force: true });
    } catch {
      // Ignore cleanup errors
    }
  }

  return message ? { message } : {};
}

// CLI entry point
if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  const options = {};

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === "--appUrl" && args[i + 1]) {
      options.appUrl = args[++i];
    } else if (arg === "--newWebsite") {
      options.newWebsite = true;
    } else if (arg === "--with-branding") {
      options["with-branding"] = true;
    } else if (arg === "--outputDir" && args[i + 1]) {
      options.outputDir = args[++i];
    }
  }

  publishDocs(options)
    .then((result) => {
      if (result?.message) {
        console.log(result.message);
      }
      process.exit(0);
    })
    .catch((error) => {
      console.error(error.message);
      process.exit(1);
    });
}
