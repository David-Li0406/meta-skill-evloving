/**
 * Sora Character Extractor - Console Log Method
 *
 * Extracts character data (handle, name, thumbnail URL, demo video URL)
 * from a Sora character profile page and logs to console.
 *
 * Usage via browser automation:
 * 1. Navigate to https://sora.chatgpt.com/profile/openpromo.actor.xxx
 * 2. Run this script via javascript_tool
 * 3. Use read_console_messages with pattern "HANDLE|NAME|THUMB|VIDEO"
 * 4. Parse console output to get URLs
 *
 * Why console logging?
 * - Browser automation blocks JavaScript response data (URLs get BLOCKED)
 * - Console messages can be read via read_console_messages tool
 * - Provides reliable data extraction
 */
/** biome-ignore-all lint/suspicious/noConsole: ok */

async function extract() {
  const h = window.location.pathname.split("/").pop();
  const n = document.querySelector("h1")?.textContent?.trim() || "";
  const img = document.querySelector('img[class*="mask-blossom"]');
  const t = img?.src || "";

  const btn = Array.from(document.querySelectorAll("button")).find((b) =>
    b.textContent.includes("Edit character"),
  );

  if (btn) {
    btn.click();
    await new Promise((r) => setTimeout(r, 800));

    const v = document.querySelector("video");
    const vu = v?.src || v?.currentSrc || "";

    console.log("HANDLE:", h);
    console.log("NAME:", n);
    console.log("THUMB:", t);
    console.log("VIDEO:", vu);

    return { handle: h, name: n, thumb: t, video: vu };
  }
}

extract();
