#!/usr/bin/env bun
/**
 * Interactive style preview server
 * Fetches images on-demand from Wikimedia Commons or Met Museum API
 */

import { readFileSync, existsSync, mkdirSync, writeFileSync } from "node:fs"
import { resolve, dirname, join } from "node:path"
import { fileURLToPath } from "node:url"
import { homedir } from "node:os"

const __dirname = dirname(fileURLToPath(import.meta.url))
const STYLES_PATH = resolve(__dirname, "../../../styles/styles.json")
const CACHE_DIR = join(homedir(), ".cache", "gemskills", "styles")
const PORT = 3456

interface StyleSource {
  api: string
  objectId?: number
  url?: string
  title: string
}

interface Style {
  id: string
  shortName: string
  name: string
  category: string
  era?: string
  artists?: string[]
  promptHints: string
  sources: StyleSource[]
}

interface StylesRegistry {
  categories: Record<string, string>
  styles: Style[]
}

interface MetObject {
  objectID: number
  primaryImage: string
  primaryImageSmall: string
  title: string
}

const fetchingStyles = new Map<string, Promise<string | null>>()

function loadStyles(): StylesRegistry {
  const content = readFileSync(STYLES_PATH, "utf-8")
  return JSON.parse(content)
}

const registry = loadStyles()

async function fetchMetObject(objectId: number): Promise<MetObject | null> {
  const url = `https://collectionapi.metmuseum.org/public/collection/v1/objects/${objectId}`
  try {
    const response = await fetch(url)
    if (!response.ok) return null
    return (await response.json()) as MetObject
  } catch {
    return null
  }
}

async function downloadImage(url: string): Promise<Buffer | null> {
  try {
    const response = await fetch(url, {
      headers: {
        "User-Agent": "GemskillsStyleBrowser/1.0 (https://github.com/b-open-io/gemskills)"
      }
    })
    if (!response.ok) {
      console.log(`  [download] Failed ${response.status}: ${url.slice(0, 80)}...`)
      return null
    }
    return Buffer.from(await response.arrayBuffer())
  } catch (err) {
    console.log(`  [download] Error: ${err}`)
    return null
  }
}

async function fetchAndCacheStyle(styleId: string): Promise<string | null> {
  const style = registry.styles.find((s) => s.id === styleId)
  if (!style) return null

  const styleDir = join(CACHE_DIR, styleId)
  const thumbPath = join(styleDir, "thumb.jpg")

  if (existsSync(thumbPath)) return thumbPath

  mkdirSync(styleDir, { recursive: true })

  // Try direct URL sources first (Wikimedia, etc)
  const urlSources = style.sources.filter((s) => s.api === "url" && s.url)
  for (const source of urlSources) {
    console.log(`  [url] Fetching ${style.name} from ${source.url?.slice(0, 60)}...`)
    const imageData = await downloadImage(source.url!)
    if (imageData && imageData.length > 1000) {
      writeFileSync(thumbPath, imageData)
      console.log(`  [url] Cached ${style.name} (${imageData.length} bytes)`)
      return thumbPath
    }
  }

  // Try Met Museum sources
  const metSources = style.sources.filter((s) => s.api === "met" && s.objectId)
  for (const source of metSources) {
    console.log(`  [met] Fetching ${style.name} (${source.objectId})...`)
    const obj = await fetchMetObject(source.objectId!)
    if (!obj?.primaryImageSmall) {
      console.log(`  [met] No image for ${source.objectId}`)
      continue
    }

    const imageData = await downloadImage(obj.primaryImageSmall)
    if (imageData && imageData.length > 1000) {
      writeFileSync(thumbPath, imageData)
      console.log(`  [met] Cached ${style.name} (${imageData.length} bytes)`)
      return thumbPath
    }
  }

  console.log(`  [fail] No sources worked for ${style.name}`)
  return null
}

async function getStyleImage(styleId: string): Promise<string | null> {
  const thumbPath = join(CACHE_DIR, styleId, "thumb.jpg")
  if (existsSync(thumbPath)) return thumbPath

  if (fetchingStyles.has(styleId)) {
    return fetchingStyles.get(styleId)!
  }

  const fetchPromise = fetchAndCacheStyle(styleId)
  fetchingStyles.set(styleId, fetchPromise)

  try {
    return await fetchPromise
  } finally {
    fetchingStyles.delete(styleId)
  }
}

function generateHTML(): string {
  const { categories, styles } = registry

  const styleCards = styles
    .map((s) => {
      return `
      <div class="style-card" data-id="${s.id}" data-short="${s.shortName}" data-category="${s.category}" data-name="${s.name.toLowerCase()}">
        <div class="thumb" data-style="${s.id}">
          <span class="no-thumb">${s.shortName}</span>
          <div class="loading"></div>
        </div>
        <div class="info">
          <div class="name">${s.name}</div>
          <div class="short">${s.shortName}</div>
          <div class="category">${categories[s.category] || s.category}</div>
        </div>
      </div>`
    })
    .join("\n")

  const categoryOptions = Object.entries(categories)
    .map(([id, name]) => `<option value="${id}">${name}</option>`)
    .join("\n")

  return `<!DOCTYPE html>
<html>
<head>
  <title>Style Browser - Gemskills</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: #0a0a0a;
      color: #e0e0e0;
      min-height: 100vh;
    }
    header {
      position: sticky;
      top: 0;
      z-index: 100;
      background: #111;
      border-bottom: 1px solid #333;
      padding: 1rem;
    }
    .controls {
      max-width: 1400px;
      margin: 0 auto;
      display: flex;
      gap: 1rem;
      flex-wrap: wrap;
      align-items: center;
    }
    h1 { font-size: 1.25rem; font-weight: 600; color: #fff; }
    input, select {
      background: #222;
      border: 1px solid #444;
      color: #fff;
      padding: 0.5rem 0.75rem;
      border-radius: 6px;
      font-size: 0.875rem;
    }
    input:focus, select:focus { outline: none; border-color: #666; }
    #search { width: 200px; }
    .count { margin-left: auto; color: #888; font-size: 0.875rem; }
    .grid {
      max-width: 1400px;
      margin: 0 auto;
      padding: 1.5rem;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
      gap: 1rem;
    }
    .style-card {
      background: #181818;
      border: 1px solid #333;
      border-radius: 8px;
      overflow: hidden;
      cursor: pointer;
      transition: transform 0.15s, border-color 0.15s;
    }
    .style-card:hover { transform: translateY(-2px); border-color: #555; }
    .style-card.hidden { display: none; }
    .thumb {
      aspect-ratio: 1;
      background: #222;
      background-size: cover;
      background-position: center;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
    }
    .thumb.loaded .no-thumb { display: none; }
    .thumb.loaded .loading { display: none; }
    .thumb.error .loading { display: none; }
    .no-thumb {
      color: #444;
      font-size: 1.5rem;
      font-weight: 600;
      text-transform: uppercase;
    }
    .loading {
      position: absolute;
      width: 24px;
      height: 24px;
      border: 2px solid #333;
      border-top-color: #666;
      border-radius: 50%;
      animation: spin 1s linear infinite;
      display: none;
    }
    .thumb.loading-active .loading { display: block; }
    .thumb.loading-active .no-thumb { opacity: 0.3; }
    @keyframes spin { to { transform: rotate(360deg); } }
    .info { padding: 0.75rem; }
    .name {
      font-weight: 500;
      font-size: 0.875rem;
      margin-bottom: 0.25rem;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .short { font-family: monospace; font-size: 0.75rem; color: #888; margin-bottom: 0.25rem; }
    .category { font-size: 0.7rem; color: #666; text-transform: uppercase; letter-spacing: 0.5px; }
    .modal {
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.9);
      z-index: 200;
      align-items: center;
      justify-content: center;
      padding: 2rem;
    }
    .modal.active { display: flex; }
    .modal-content {
      background: #181818;
      border: 1px solid #333;
      border-radius: 12px;
      max-width: 800px;
      width: 100%;
      max-height: 90vh;
      overflow: auto;
    }
    .modal-header {
      padding: 1rem 1.5rem;
      border-bottom: 1px solid #333;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .modal-header h2 { font-size: 1.25rem; }
    .close-btn {
      background: none;
      border: none;
      color: #888;
      font-size: 1.5rem;
      cursor: pointer;
      padding: 0.5rem;
    }
    .close-btn:hover { color: #fff; }
    .modal-body { padding: 1.5rem; }
    .modal-image {
      width: 100%;
      aspect-ratio: 1;
      background: #222;
      background-size: contain;
      background-position: center;
      background-repeat: no-repeat;
      border-radius: 8px;
      margin-bottom: 1rem;
    }
    .detail-row { display: flex; gap: 0.5rem; margin-bottom: 0.5rem; font-size: 0.875rem; }
    .detail-label { color: #666; min-width: 80px; }
    .prompt-hints {
      background: #222;
      padding: 1rem;
      border-radius: 6px;
      font-size: 0.8rem;
      line-height: 1.6;
      color: #aaa;
      margin-top: 1rem;
    }
    .copy-btn {
      background: #333;
      border: 1px solid #444;
      color: #fff;
      padding: 0.5rem 1rem;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.875rem;
      margin-top: 1rem;
    }
    .copy-btn:hover { background: #444; }
    .copy-btn.copied { background: #2a5; border-color: #3b6; }
    .toast {
      position: fixed;
      bottom: 2rem;
      left: 50%;
      transform: translateX(-50%);
      background: #333;
      padding: 0.75rem 1.5rem;
      border-radius: 6px;
      font-size: 0.875rem;
      opacity: 0;
      transition: opacity 0.2s;
      pointer-events: none;
    }
    .toast.show { opacity: 1; }
    .status {
      position: fixed;
      bottom: 1rem;
      right: 1rem;
      background: #222;
      border: 1px solid #333;
      padding: 0.5rem 1rem;
      border-radius: 6px;
      font-size: 0.75rem;
      color: #888;
    }
  </style>
</head>
<body>
  <header>
    <div class="controls">
      <h1>Style Browser</h1>
      <input type="text" id="search" placeholder="Search styles...">
      <select id="category">
        <option value="">All Categories</option>
        ${categoryOptions}
      </select>
      <span class="count"><span id="visible-count">${styles.length}</span> / ${styles.length} styles</span>
    </div>
  </header>

  <div class="grid" id="grid">
    ${styleCards}
  </div>

  <div class="modal" id="modal">
    <div class="modal-content">
      <div class="modal-header">
        <h2 id="modal-title"></h2>
        <button class="close-btn">&times;</button>
      </div>
      <div class="modal-body">
        <div class="modal-image" id="modal-image"></div>
        <div id="modal-details"></div>
        <div class="prompt-hints" id="modal-hints"></div>
        <button class="copy-btn" id="copy-btn">Copy Style ID</button>
      </div>
    </div>
  </div>

  <div class="toast" id="toast">Copied to clipboard!</div>
  <div class="status" id="status">Loading images...</div>

  <script>
    const styles = ${JSON.stringify(styles)};
    const categories = ${JSON.stringify(categories)};
    const cards = document.querySelectorAll('.style-card');
    const thumbs = document.querySelectorAll('.thumb[data-style]');
    const searchInput = document.getElementById('search');
    const categorySelect = document.getElementById('category');
    const visibleCount = document.getElementById('visible-count');
    const modal = document.getElementById('modal');
    const toast = document.getElementById('toast');
    const status = document.getElementById('status');

    let loadedCount = 0;
    let errorCount = 0;

    function updateStatus() {
      if (loadedCount + errorCount >= thumbs.length) {
        status.textContent = loadedCount + ' images loaded';
        setTimeout(() => status.style.opacity = '0', 2000);
      } else {
        status.textContent = 'Loading... ' + loadedCount + '/' + thumbs.length;
      }
    }

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const thumb = entry.target;
          const styleId = thumb.dataset.style;
          if (thumb.classList.contains('loaded') || thumb.classList.contains('loading-active')) return;

          thumb.classList.add('loading-active');

          const img = new Image();
          img.onload = () => {
            thumb.style.backgroundImage = 'url(/thumb/' + styleId + ')';
            thumb.classList.remove('loading-active');
            thumb.classList.add('loaded');
            loadedCount++;
            updateStatus();
          };
          img.onerror = () => {
            thumb.classList.remove('loading-active');
            thumb.classList.add('error');
            errorCount++;
            updateStatus();
          };
          img.src = '/thumb/' + styleId;
        }
      });
    }, { rootMargin: '200px' });

    thumbs.forEach(thumb => observer.observe(thumb));

    function filterCards() {
      const search = searchInput.value.toLowerCase();
      const category = categorySelect.value;
      let count = 0;

      cards.forEach(card => {
        const matchesSearch = !search ||
          card.dataset.name.includes(search) ||
          card.dataset.short.includes(search) ||
          card.dataset.id.includes(search);
        const matchesCategory = !category || card.dataset.category === category;

        if (matchesSearch && matchesCategory) {
          card.classList.remove('hidden');
          count++;
        } else {
          card.classList.add('hidden');
        }
      });

      visibleCount.textContent = count;
    }

    searchInput.addEventListener('input', filterCards);
    categorySelect.addEventListener('change', filterCards);

    cards.forEach(card => {
      card.addEventListener('click', () => {
        const style = styles.find(s => s.id === card.dataset.id);
        if (!style) return;

        document.getElementById('modal-title').textContent = style.name;
        document.getElementById('modal-image').style.backgroundImage = 'url(/ref/' + style.id + ')';
        document.getElementById('modal-hints').textContent = style.promptHints;
        document.getElementById('modal-details').innerHTML =
          '<div class="detail-row"><span class="detail-label">ID</span><span>' + style.id + '</span></div>' +
          '<div class="detail-row"><span class="detail-label">Short</span><span>' + style.shortName + '</span></div>' +
          '<div class="detail-row"><span class="detail-label">Category</span><span>' + (categories[style.category] || style.category) + '</span></div>' +
          (style.era ? '<div class="detail-row"><span class="detail-label">Era</span><span>' + style.era + '</span></div>' : '') +
          (style.artists ? '<div class="detail-row"><span class="detail-label">Artists</span><span>' + style.artists.join(', ') + '</span></div>' : '');

        const copyBtn = document.getElementById('copy-btn');
        copyBtn.textContent = 'Copy Style ID';
        copyBtn.classList.remove('copied');
        copyBtn.onclick = () => {
          navigator.clipboard.writeText(style.id);
          copyBtn.textContent = 'Copied!';
          copyBtn.classList.add('copied');
          showToast();
        };

        modal.classList.add('active');
      });
    });

    modal.querySelector('.close-btn').addEventListener('click', () => modal.classList.remove('active'));
    modal.addEventListener('click', (e) => { if (e.target === modal) modal.classList.remove('active'); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') modal.classList.remove('active'); });

    function showToast() {
      toast.classList.add('show');
      setTimeout(() => toast.classList.remove('show'), 2000);
    }
  </script>
</body>
</html>`
}

mkdirSync(CACHE_DIR, { recursive: true })

const server = Bun.serve({
  port: PORT,
  async fetch(req) {
    const url = new URL(req.url)
    const path = url.pathname

    if (path.startsWith("/thumb/")) {
      const styleId = path.slice(7)
      const thumbPath = await getStyleImage(styleId)
      if (thumbPath && existsSync(thumbPath)) {
        return new Response(Bun.file(thumbPath), {
          headers: { "Content-Type": "image/jpeg", "Cache-Control": "public, max-age=31536000" },
        })
      }
      return new Response("Not found", { status: 404 })
    }

    if (path.startsWith("/ref/")) {
      const styleId = path.slice(5)
      await getStyleImage(styleId)

      const refPath = join(CACHE_DIR, styleId, "ref-1.jpg")
      if (existsSync(refPath)) {
        return new Response(Bun.file(refPath), {
          headers: { "Content-Type": "image/jpeg", "Cache-Control": "public, max-age=31536000" },
        })
      }
      const thumbPath = join(CACHE_DIR, styleId, "thumb.jpg")
      if (existsSync(thumbPath)) {
        return new Response(Bun.file(thumbPath), {
          headers: { "Content-Type": "image/jpeg", "Cache-Control": "public, max-age=31536000" },
        })
      }
      return new Response("Not found", { status: 404 })
    }

    return new Response(generateHTML(), {
      headers: { "Content-Type": "text/html" },
    })
  },
})

console.log(`Style Browser running at http://localhost:${PORT}`)
console.log(`Cache: ${CACHE_DIR}`)
console.log(`Press Ctrl+C to stop\n`)

const opener =
  process.platform === "darwin" ? "open" : process.platform === "win32" ? "start" : "xdg-open"
Bun.spawn([opener, `http://localhost:${PORT}`])
