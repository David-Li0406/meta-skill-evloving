/**
 * Gravito SSG Generator (Freeze Protocol)
 *
 * 此腳本需要從專案根目錄執行，或複製到專案中使用。
 *
 * 使用方式：
 *   1. 複製此檔案到專案根目錄
 *   2. 修改 BOOTSTRAP_PATH 指向你的 bootstrap.ts
 *   3. 執行: bun run generate.ts
 *
 * 或直接使用官方 build script: bun run build:static
 */

import { exec } from 'node:child_process'
import { cp, mkdir, writeFile } from 'node:fs/promises'
import { dirname, join } from 'node:path'
import { promisify } from 'node:util'
import type { PlanetCore } from '@gravito/core'

// ============ 配置區域 ============
const BOOTSTRAP_PATH = './src/bootstrap'  // 修改為你的 bootstrap 路徑
const KNOWN_ROUTES = ['/', '/about']       // 已知路由，可擴展為自動掃描
// ==================================

const execAsync = promisify(exec)

interface GeneratorConfig {
  baseUrl: string
  outputDir: string
  staticDomains: string
}

function getConfig(): GeneratorConfig {
  return {
    baseUrl: process.env.STATIC_SITE_BASE_URL || 'https://yourdomain.com',
    outputDir: 'dist-static',  // 與官方 build-static.ts 一致
    staticDomains: process.env.STATIC_SITE_DOMAINS || '',
  }
}

function discoverRoutes(_core: PlanetCore): string[] {
  // 可擴展為從 router 自動掃描
  // 目前使用已知路由列表
  return [...KNOWN_ROUTES]
}

function generateSpaRecoveryScript(): string {
  return `
<script>
  // GitHub Pages SPA routing handler for Inertia.js
  (function() {
    const currentPath = window.location.pathname;
    const currentSearch = window.location.search;
    const currentHash = window.location.hash;

    if (currentPath === '/404.html' || currentPath.endsWith('/404.html')) {
      return;
    }

    function tryLoadHtml(path, callback) {
      let htmlPath = path.endsWith('/') ? path + 'index.html' : path + '/index.html';

      fetch(htmlPath)
        .then(function(response) {
          if (response.ok) return response.text();
          if (htmlPath.endsWith('/index.html')) {
            return fetch(path + '.html').then(function(altResponse) {
              if (altResponse.ok) return altResponse.text();
              throw new Error('Not found');
            });
          }
          throw new Error('Not found');
        })
        .then(function(html) { callback(null, html); })
        .catch(function(error) { callback(error, null); });
    }

    function handleRoute() {
      tryLoadHtml(currentPath, function(error, html) {
        if (error || !html) {
          console.log('Route not found:', currentPath);
          return;
        }
        window.history.replaceState(null, '', currentPath + currentSearch + currentHash);
        document.open();
        document.write(html);
        document.close();
      });
    }

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', handleRoute);
    } else {
      handleRoute();
    }
  })();
</script>`
}

async function generate() {
  console.log('🌌 [Gravito Freeze] Starting Static Site Generation...')

  const config = getConfig()
  const domain = new URL(config.baseUrl).hostname

  // 1. Build Client Assets
  console.log('⚡ Building client assets (Vite)...')
  try {
    await execAsync('bun run build:client', {
      env: { ...process.env, VITE_STATIC_SITE_DOMAINS: config.staticDomains }
    })
    console.log('✅ Client build complete.')
  } catch (e) {
    console.error('❌ Client build failed:', e)
    process.exit(1)
  }

  // 2. Bootstrap PlanetCore
  const { bootstrap } = await import(BOOTSTRAP_PATH)
  const core: PlanetCore = await bootstrap({ port: 3000 })

  const outputDir = join(process.cwd(), config.outputDir)
  await mkdir(outputDir, { recursive: true })

  console.log(`📂 Output: ${outputDir}`)
  console.log(`🌐 Base URL: ${config.baseUrl}`)

  // 3. Discover Routes
  const routes = discoverRoutes(core)
  console.log(`📋 Routes: ${routes.join(', ')}`)

  // 4. Sitemap Setup
  let sitemapEntries: string[] = []

  // 5. Render Routes
  for (const route of routes) {
    console.log(`📡 Rendering: ${route}`)

    try {
      const res = await core.adapter.fetch(new Request(`http://localhost${route}`))

      if (res.status === 301 || res.status === 302) {
        const location = res.headers.get('Location')
        console.log(`  ↪ Redirect to ${location}`)
        const html = `<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0; url=${location}" /></head></html>`
        const filePath = join(outputDir, route, 'index.html')
        await mkdir(dirname(filePath), { recursive: true })
        await writeFile(filePath, html)
        continue
      }

      if (res.status !== 200) {
        console.error(`  ❌ HTTP ${res.status}`)
        continue
      }

      let html = await res.text()

      // Apply ssg:rendered filter if registered
      try {
        html = await core.hooks.applyFilters('ssg:rendered', html)
      } catch { /* filter not registered */ }

      const pathname = route.replace(/\/$/, '') || '/'
      const filePath = route === '/'
        ? join(outputDir, 'index.html')
        : join(outputDir, pathname, 'index.html')

      await mkdir(dirname(filePath), { recursive: true })
      await writeFile(filePath, html)

      sitemapEntries.push(`${config.baseUrl}${pathname}`)
      console.log(`  ✅ Generated`)
    } catch (e) {
      console.error(`  ❌ Error:`, e)
    }
  }

  // 6. Generate Sitemap
  const sitemapXml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${sitemapEntries.map(url => `  <url><loc>${url}</loc></url>`).join('\n')}
</urlset>`
  await writeFile(join(outputDir, 'sitemap.xml'), sitemapXml)
  console.log('🗺️  Sitemap generated.')

  // 7. Generate 404.html with SPA Recovery
  console.log('🚫 Generating 404.html...')
  try {
    const res = await core.adapter.fetch(new Request(`http://localhost/__force_404__`))
    let html = await res.text()

    const spaScript = generateSpaRecoveryScript()
    if (html.includes('</body>')) {
      html = html.replace('</body>', `${spaScript}\n</body>`)
    } else {
      html = html.replace('</html>', `${spaScript}\n</html>`)
    }

    await writeFile(join(outputDir, '404.html'), html)
    console.log('✅ 404.html generated with SPA recovery.')
  } catch (e) {
    console.error('❌ Failed to generate 404.html:', e)
  }

  // 8. Copy Static Assets
  console.log('📦 Copying static assets...')
  try {
    await cp(join(process.cwd(), 'static'), join(outputDir, 'static'), { recursive: true })
    console.log('✅ Static assets copied.')
  } catch {
    console.warn('⚠️  No static directory found.')
  }

  // 9. GitHub Pages Files
  if (domain && domain !== 'yourdomain.com') {
    await writeFile(join(outputDir, 'CNAME'), domain)
    console.log('✅ CNAME created.')
  }
  await writeFile(join(outputDir, '.nojekyll'), '')
  console.log('✅ .nojekyll created.')

  // Done
  console.log('')
  console.log('🚀 Gravito Freeze Complete!')
  console.log(`📦 Output: ${outputDir}`)
  console.log(`🔍 Preview: cd ${config.outputDir} && npx serve .`)

  process.exit(0)
}

generate().catch((error) => {
  console.error('💥 Freeze failed:', error)
  process.exit(1)
})
