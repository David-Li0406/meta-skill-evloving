// Paste this file's contents into Playwright MCP `browser_run_code` as the `code` string.
//
// Goal: Collect N feed posts from `https://www.linkedin.com/feed/` while scrolling,
// excluding "Promoted" and common non-post modules. Prefer DOM permalink; fallback
// to URN-derived link.
//
// Notes:
// - Avoid heavy `innerText` reads on large containers (can time out).
// - LinkedIn DOM changes frequently; update selectors in `references/api_reference.md`.

async (page) => {
  const TARGET = 20;
  const MAX_ITERS = 30;
  const SCROLL_Y = 2600;
  const WAIT_MS = 900;

  const normalizeLink = (href, urn) => {
    if (href) {
      if (href.startsWith("http")) return href;
      if (href.startsWith("/")) return `https://www.linkedin.com${href}`;
      return `https://www.linkedin.com/${href}`;
    }
    return urn ? `https://www.linkedin.com/feed/update/${urn}/` : null;
  };

  const isBadUrn = (urn) => {
    if (!urn) return true;
    if (!/^urn:li:(activity|aggregate):/i.test(urn)) return true;
    if (/^urn:li:inAppPromotion:/i.test(urn)) return true;
    if (/^urn:li:jobPosting:/i.test(urn)) return true;
    if (/^urn:li:aggregate:\(urn:li:jobPosting:/i.test(urn)) return true;
    return false;
  };

  // Exclude employment/job-change posts and do not count them toward N.
  // Best-effort heuristics; keep conservative to avoid miscounting.
  const isEmploymentOrJobChangePost = (text) => {
    if (!text) return false;
    const t = String(text).toLowerCase();

    // English
    const enPatterns = [
      /\bstarting a new position\b/i,
      /\bstart(ing)? a new role\b/i,
      /\b(open to work|seeking opportunities)\b/i,
      /\b(i|we)\s+(joined|join)\b/i
    ];
    return enPatterns.some((re) => re.test(text));
  };

  const pad2 = (n) => String(n).padStart(2, "0");

  // System timezone (browser local). Format: YYYY-MM-DD HH:mm
  const formatLocalDateTime = (d) =>
    `${d.getFullYear()}-${pad2(d.getMonth() + 1)}-${pad2(d.getDate())} ${pad2(
      d.getHours()
    )}:${pad2(d.getMinutes())}`;

  // Convert common LinkedIn relative strings to an absolute local timestamp.
  // Examples observed:
  // - "18h •" (aria-hidden)
  // - "4d •"
  // - "2w • Edited •"
  // - "18 hours ago • Visible to anyone..."
  const relativeToAbsoluteLocal = (relativeText, now) => {
    if (!relativeText) return null;
    const t = String(relativeText).replace(/\s+/g, " ").trim().toLowerCase();

    // Prefer explicit "X unit(s) ago"
    let m = t.match(
      /\b(\d+)\s+(second|seconds|minute|minutes|hour|hours|day|days|week|weeks|month|months|year|years)\s+ago\b/
    );
    if (m) {
      const n = Number(m[1]);
      const unit = m[2];
      const d = new Date(now.getTime());
      if (unit.startsWith("second")) d.setSeconds(d.getSeconds() - n);
      else if (unit.startsWith("minute")) d.setMinutes(d.getMinutes() - n);
      else if (unit.startsWith("hour")) d.setHours(d.getHours() - n);
      else if (unit.startsWith("day")) d.setDate(d.getDate() - n);
      else if (unit.startsWith("week")) d.setDate(d.getDate() - n * 7);
      else if (unit.startsWith("month")) d.setMonth(d.getMonth() - n);
      else if (unit.startsWith("year")) d.setFullYear(d.getFullYear() - n);
      return formatLocalDateTime(d);
    }

    // Fallback short forms: 18h, 4d, 2w, 3mo, 1y (often followed by bullets/dots)
    m = t.match(/\b(\d+)\s*(s|m|h|d|w|mo|y)\b/);
    if (!m) return null;

    const n = Number(m[1]);
    const unit = m[2];
    const d = new Date(now.getTime());
    if (unit === "s") d.setSeconds(d.getSeconds() - n);
    else if (unit === "m") d.setMinutes(d.getMinutes() - n);
    else if (unit === "h") d.setHours(d.getHours() - n);
    else if (unit === "d") d.setDate(d.getDate() - n);
    else if (unit === "w") d.setDate(d.getDate() - n * 7);
    else if (unit === "mo") d.setMonth(d.getMonth() - n);
    else if (unit === "y") d.setFullYear(d.getFullYear() - n);
    else return null;

    return formatLocalDateTime(d);
  };

  const collected = new Map();
  const collectedAt = new Date();

  for (let iter = 0; iter < MAX_ITERS && collected.size < TARGET; iter++) {
    const batch = await page.evaluate(() => {
      const els = Array.from(
        document.querySelectorAll(
          "div.feed-shared-update-v2[data-urn], div.occludable-update[data-urn]"
        )
      );
      return els.slice(0, 40).map((root) => {
        const urn = root.getAttribute("data-urn");

        const nodes = root.querySelectorAll("span, p, a, div");
        let promoted = false;
        for (const n of nodes) {
          const t = (n.textContent || "").trim().toLowerCase();
          // Match common "Promoted" labels across locales without embedding non-ASCII text.
          if (
            t === "promoted" ||
            t === "\uD64D\uBCF4" || // Korean: "Promoted"
            t === "\uC2A4\uD3F0\uC11C" // Korean: "Sponsored"
          ) {
            promoted = true;
            break;
          }
        }

        const authorEl = root.querySelector(
          'span.update-components-actor__name, a.update-components-actor__meta-link span[dir="ltr"], span.update-components-actor__title span[dir="ltr"]'
        );
        const textEl = root.querySelector(
          "div.update-components-text, div.feed-shared-update-v2__description, span.break-words"
        );
        const linkEl = root.querySelector('a[href*="/feed/update/"]');

        // Prefer visually-hidden sub-description which often includes "X hours ago".
        const subDescHidden = root.querySelector(
          "span.update-components-actor__sub-description span.visually-hidden"
        );
        const subDescVisible = root.querySelector(
          'span.update-components-actor__sub-description span[aria-hidden="true"]'
        );

        return {
          urn,
          promoted,
          author: (authorEl?.textContent || "").trim() || null,
          text: (textEl?.textContent || "").trim() || null,
          href: linkEl?.getAttribute("href") || null,
          subDescHidden: (subDescHidden?.textContent || "").trim() || null,
          subDescVisible: (subDescVisible?.textContent || "").trim() || null,
        };
      });
    });

    for (const p of batch) {
      if (!p?.urn || !p.author || !p.text) continue;
      if (p.promoted) continue;
      if (isBadUrn(p.urn)) continue;
      if (isEmploymentOrJobChangePost(p.text)) continue;

      if (!collected.has(p.urn)) {
        const relative = p.subDescHidden || p.subDescVisible || null;
        const postedAt = relativeToAbsoluteLocal(relative, collectedAt);
        collected.set(p.urn, {
          urn: p.urn,
          author: p.author.replace(/\s+/g, " "),
          text: p.text.replace(/\s+/g, " "),
          link: normalizeLink(p.href, p.urn),
          collectedAt: formatLocalDateTime(collectedAt),
          postedDateRelative: relative,
          postedDateAbsoluteLocal: postedAt,
        });
      }
      if (collected.size >= TARGET) break;
    }

    if (collected.size >= TARGET) break;
    await page.mouse.wheel(0, SCROLL_Y);
    await page.waitForTimeout(WAIT_MS);
  }

  return {
    url: page.url(),
    collectedAt: formatLocalDateTime(collectedAt),
    total: collected.size,
    posts: Array.from(collected.values()).slice(0, TARGET),
  };
};
