# Web Deployment

Complete guide to building and deploying Flutter web applications with PWA support.

## Overview

Flutter web allows you to deploy Flutter applications as Progressive Web Apps (PWAs) that run in modern web browsers. Web deployment is simpler than mobile platforms—no app stores, no code signing, just build and host. However, optimizing for web requires understanding renderers, PWA capabilities, hosting requirements, and performance considerations.

## Prerequisites

### Development Environment

- **Flutter SDK** - Web support enabled by default in Flutter 2.0+
- **Web browser** - Chrome recommended for development
- **Hosting service** - Firebase, Netlify, Vercel, or any static host

### Verify Web Support

Check Flutter web support is enabled:

```bash
flutter config --list
```

Should show: `enable-web: true`

If not enabled:

```bash
flutter config --enable-web
```

## Build Modes and Configuration

### Build Modes

Flutter web supports the same three build modes as mobile:

**Debug Mode:**
```bash
flutter run -d chrome
```

- Uses `dartdevc` compiler
- No minification or tree shaking
- Source maps enabled
- Hot reload supported
- Suitable for development only

**Profile Mode:**
```bash
flutter build web --profile
```

- Uses `dart2js` compiler
- Tree shaking enabled
- No minification
- Performance profiling enabled
- Use for performance testing

**Release Mode:**
```bash
flutter build web --release
```

- Uses `dart2js` compiler
- Full minification and tree shaking
- Optimized for production
- Smallest bundle size
- No debugging information

### Web Renderers

Flutter web offers multiple rendering engines with different trade-offs.

#### CanvasKit Renderer (Default)

Uses WebAssembly-compiled Skia for rendering:

```bash
flutter build web --web-renderer canvaskit
```

**Advantages:**
- Consistent rendering across browsers
- Better performance for complex animations
- Full feature parity with mobile
- Advanced graphics capabilities

**Disadvantages:**
- Larger initial download (~2MB)
- Longer initial load time
- Higher memory usage

**Best for:**
- Graphics-intensive apps
- Apps requiring precise rendering
- Cross-platform consistency priority

#### HTML Renderer

Uses HTML, CSS, and Canvas for rendering:

```bash
flutter build web --web-renderer html
```

**Advantages:**
- Smaller bundle size
- Faster initial load
- Better text rendering
- Better accessibility

**Disadvantages:**
- Limited features compared to CanvasKit
- Less consistent across browsers
- Lower performance for complex graphics

**Best for:**
- Text-heavy applications
- Simple UI layouts
- Accessibility priority
- Bandwidth-constrained users

#### Auto Renderer

Automatically selects renderer based on device:

```bash
flutter build web --web-renderer auto
```

**Behavior:**
- Mobile browsers: HTML renderer
- Desktop browsers: CanvasKit renderer
- Balances performance and bundle size

**Best for:**
- General-purpose applications
- When you want automatic optimization

### Skwasm Renderer (Experimental)

WebAssembly-based renderer with improved performance:

```bash
flutter build web --web-renderer skwasm
```

**Features:**
- Better performance than CanvasKit
- Smaller bundle size
- Multi-threading support
- Still experimental (Flutter 3.38+)

## Building for Production

### Basic Build

Build optimized production bundle:

```bash
flutter build web --release
```

Output directory: `build/web/`

### Build with Specific Renderer

```bash
flutter build web --release --web-renderer canvaskit
```

### Build with Base HREF

For hosting in subdirectory:

```bash
flutter build web --release --base-href="/myapp/"
```

Updates all asset paths to be relative to `/myapp/`.

### Build with Custom Output Directory

```bash
flutter build web --release --output-dir=public
```

### Build with Source Maps

Helpful for debugging production issues:

```bash
flutter build web --release --source-maps
```

Generates `.map` files alongside JavaScript bundles. Consider excluding from public hosting for security.

### Analyze Build Size

```bash
flutter build web --release --analyze-size
```

Opens size analysis in browser showing bundle composition.

## Progressive Web App (PWA) Configuration

### Understanding PWA Features

PWAs bridge the gap between web and native apps:

- **Installable** - Add to home screen
- **Offline capable** - Service worker caching
- **App-like** - Fullscreen, standalone mode
- **Discoverable** - Can be found via search engines
- **Re-engageable** - Push notifications (experimental in Flutter)
- **Responsive** - Works on any screen size
- **Secure** - Requires HTTPS

### Manifest Configuration

Edit `web/manifest.json`:

```json
{
  "name": "My Flutter App",
  "short_name": "MyApp",
  "start_url": ".",
  "display": "standalone",
  "background_color": "#0175C2",
  "theme_color": "#0175C2",
  "description": "A new Flutter application for web",
  "orientation": "portrait-primary",
  "prefer_related_applications": false,
  "icons": [
    {
      "src": "icons/Icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "icons/Icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    },
    {
      "src": "icons/Icon-maskable-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "maskable"
    },
    {
      "src": "icons/Icon-maskable-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "maskable"
    }
  ]
}
```

**Key fields:**

- **`name`** - Full app name (displayed during install)
- **`short_name`** - Short name (displayed on home screen)
- **`start_url`** - URL loaded when app launches
- **`display`** - Display mode (standalone, fullscreen, minimal-ui, browser)
- **`background_color`** - Splash screen background
- **`theme_color`** - Browser UI color
- **`icons`** - App icons in various sizes

**Display modes:**
- `standalone` - Looks like native app, no browser UI
- `fullscreen` - Full screen, hides all browser UI
- `minimal-ui` - Minimal browser controls
- `browser` - Standard browser tab

### Service Worker Configuration

Flutter generates `flutter_service_worker.js` automatically. This service worker:
- Caches app resources
- Enables offline functionality
- Updates cached resources when new version deployed

**Default caching strategy:**
- All app assets cached on first load
- Cache-first strategy for assets
- Network-first for non-asset requests

**Customize service worker:**

Create custom `web/service-worker.js`:

```javascript
// Custom service worker for advanced caching

const CACHE_NAME = 'flutter-app-cache-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/index.html',
  '/main.dart.js',
  '/assets/fonts/MaterialIcons-Regular.otf',
  // Add critical assets
];

// Install event - cache assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
  self.skipWaiting();
});

// Activate event - clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cache) => {
          if (cache !== CACHE_NAME) {
            return caches.delete(cache);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
```

**Advanced caching strategies:**

```javascript
// Network-first (with cache fallback)
self.addEventListener('fetch', (event) => {
  event.respondWith(
    fetch(event.request)
      .then((response) => {
        const clone = response.clone();
        caches.open(CACHE_NAME).then((cache) => {
          cache.put(event.request, clone);
        });
        return response;
      })
      .catch(() => caches.match(event.request))
  );
});

// Cache-first (with network fallback)
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
```

### App Icons

PWAs require icons in multiple sizes. Flutter generates default icons in `web/icons/`.

**Required sizes:**
- 192x192 pixels (standard icon)
- 512x512 pixels (high-resolution)

**Optional but recommended:**
- Maskable icons (adapt to different device shapes)
- Favicon (16x16, 32x32)
- Apple touch icon (180x180)

**Generate icons with flutter_launcher_icons:**

```yaml
dev_dependencies:
  flutter_launcher_icons: ^0.13.1

flutter_launcher_icons:
  web:
    generate: true
    image_path: "assets/icon/app_icon.png"
    background_color: "#hexcode"
    theme_color: "#hexcode"
```

```bash
flutter pub run flutter_launcher_icons
```

### HTTPS Requirement

Service workers require HTTPS except for localhost. Ensure your hosting serves content over HTTPS.

**Why HTTPS required:**
- Security for service worker capabilities
- Required for install prompts
- Protects user data
- Required for push notifications

## Deployment Platforms

### Firebase Hosting (Recommended)

Firebase Hosting is optimized for Flutter web apps.

**Setup:**

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Initialize project
firebase init hosting
```

**Configuration (`firebase.json`):**

```json
{
  "hosting": {
    "public": "build/web",
    "ignore": [
      "firebase.json",
      "**/.*",
      "**/node_modules/**"
    ],
    "rewrites": [
      {
        "source": "**",
        "destination": "/index.html"
      }
    ],
    "headers": [
      {
        "source": "**/*.@(jpg|jpeg|gif|png|svg|webp|js|css|eot|otf|ttf|ttc|woff|woff2|font.css)",
        "headers": [
          {
            "key": "Cache-Control",
            "value": "max-age=604800"
          }
        ]
      }
    ]
  }
}
```

**Deploy:**

```bash
# Build Flutter web
flutter build web --release

# Deploy to Firebase
firebase deploy
```

**Preview before deploying:**

```bash
firebase serve
```

### Netlify

**Via Netlify CLI:**

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Build
flutter build web --release

# Deploy
netlify deploy --prod --dir=build/web
```

**Via Git integration:**

Create `netlify.toml`:

```toml
[build]
  command = "flutter build web --release"
  publish = "build/web"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

Push to Git, connect repo in Netlify dashboard, and it auto-deploys.

### Vercel

**Via Vercel CLI:**

```bash
# Install Vercel CLI
npm install -g vercel

# Build
flutter build web --release

# Deploy
vercel --prod
```

**Via Git integration:**

Create `vercel.json`:

```json
{
  "buildCommand": "flutter build web --release",
  "outputDirectory": "build/web",
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

Connect repo in Vercel dashboard.

### GitHub Pages

**Manual deployment:**

```bash
# Build
flutter build web --release --base-href="/repo-name/"

# Clone gh-pages branch
git clone -b gh-pages https://github.com/username/repo-name gh-pages

# Copy build
cp -r build/web/* gh-pages/

# Commit and push
cd gh-pages
git add .
git commit -m "Deploy"
git push
```

**Automated with GitHub Actions:**

Create `.github/workflows/deploy-web.yml`:

```yaml
name: Deploy Flutter Web

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.38.6'

      - run: flutter pub get
      - run: flutter build web --release --base-href="/repo-name/"

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./build/web
```

### CloudFlare Pages

1. Connect Git repository in CloudFlare dashboard
2. Set build command: `flutter build web --release`
3. Set output directory: `build/web`
4. Deploy

**Or use Wrangler CLI:**

```bash
npx wrangler pages publish build/web
```

### AWS S3 + CloudFront

**Upload to S3:**

```bash
# Build
flutter build web --release

# Upload
aws s3 sync build/web s3://your-bucket-name --delete

# Invalidate CloudFront cache
aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
```

**S3 bucket configuration:**
- Enable static website hosting
- Set index document: `index.html`
- Set error document: `index.html`
- Configure CORS if needed

### Google Cloud Storage

```bash
# Build
flutter build web --release

# Upload
gsutil -m rsync -r -d build/web gs://your-bucket-name

# Make public
gsutil -m acl ch -r -u AllUsers:R gs://your-bucket-name
```

### Docker Container

Create `Dockerfile`:

```dockerfile
# Build stage
FROM ghcr.io/cirruslabs/flutter:stable AS build

WORKDIR /app
COPY . .

RUN flutter pub get
RUN flutter build web --release

# Serve stage
FROM nginx:alpine

COPY --from=build /app/build/web /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

Create `nginx.conf`:

```nginx
server {
    listen 80;
    server_name _;

    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|svg|ico|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

**Build and run:**

```bash
docker build -t flutter-web-app .
docker run -p 8080:80 flutter-web-app
```

## Optimization Strategies

### Bundle Size Optimization

**1. Analyze bundle size:**

```bash
flutter build web --analyze-size
```

**2. Use deferred loading:**

```dart
// Load libraries lazily
import 'package:large_library/large_library.dart' deferred as large;

Future<void> loadLargeLibrary() async {
  await large.loadLibrary();
  large.someFunction();
}
```

**3. Optimize images:**
- Use WebP format for images
- Compress images before bundling
- Use responsive images
- Lazy load images

**4. Tree shake unused code:**

Release builds automatically tree shake. Ensure you're not importing entire libraries when you only need specific functions.

**5. Choose appropriate renderer:**
- Use HTML renderer for simpler apps (smaller bundle)
- Use CanvasKit only if you need advanced graphics

### Performance Optimization

**1. Minimize initial load:**

```dart
// Lazy load routes
MaterialApp(
  onGenerateRoute: (settings) {
    return MaterialPageRoute(
      builder: (context) {
        if (settings.name == '/heavy') {
          // Load heavy feature lazily
          return loadHeavyFeature();
        }
        return HomePage();
      },
    );
  },
);
```

**2. Use caching effectively:**

Configure service worker to cache critical assets first, load others on-demand.

**3. Optimize rendering:**

```dart
// Use const constructors
const Text('Hello');

// Avoid unnecessary rebuilds
class MyWidget extends StatelessWidget {
  const MyWidget({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return const Text('Optimized');
  }
}
```

**4. Code splitting:**

Split large apps into smaller chunks that load on-demand.

### Caching Strategy

**Configure headers for static assets:**

```nginx
# For nginx
location ~* \.(js|css|woff|woff2|ttf|otf|eot|svg)$ {
    add_header Cache-Control "public, max-age=31536000, immutable";
}

location ~* \.(png|jpg|jpeg|gif|webp)$ {
    add_header Cache-Control "public, max-age=604800";
}

location = /index.html {
    add_header Cache-Control "no-cache";
}
```

**For Firebase Hosting** (`firebase.json`):

```json
{
  "hosting": {
    "headers": [
      {
        "source": "**/*.@(js|css|woff|woff2|ttf|otf|eot|svg)",
        "headers": [
          {
            "key": "Cache-Control",
            "value": "public, max-age=31536000, immutable"
          }
        ]
      },
      {
        "source": "/index.html",
        "headers": [
          {
            "key": "Cache-Control",
            "value": "no-cache"
          }
        ]
      }
    ]
  }
}
```

### SEO Optimization

Flutter web apps are single-page applications (SPAs), which can pose SEO challenges.

**1. Add meta tags:**

Edit `web/index.html`:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- SEO Meta Tags -->
  <meta name="description" content="Your app description for SEO">
  <meta name="keywords" content="flutter, web, app, keywords">
  <meta name="author" content="Your Name">

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://yourapp.com/">
  <meta property="og:title" content="Your App Title">
  <meta property="og:description" content="Your app description">
  <meta property="og:image" content="https://yourapp.com/og-image.png">

  <!-- Twitter -->
  <meta property="twitter:card" content="summary_large_image">
  <meta property="twitter:url" content="https://yourapp.com/">
  <meta property="twitter:title" content="Your App Title">
  <meta property="twitter:description" content="Your app description">
  <meta property="twitter:image" content="https://yourapp.com/twitter-image.png">

  <title>Your App Title</title>
</head>
<body>
  <script src="main.dart.js" type="application/javascript"></script>
</body>
</html>
```

**2. Pre-render for bots:**

Use services like [Rendertron](https://github.com/GoogleChrome/rendertron) or [Prerender.io](https://prerender.io/) to serve pre-rendered HTML to search engine crawlers.

**3. Add sitemap:**

Create `build/web/sitemap.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://yourapp.com/</loc>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
```

**4. Add robots.txt:**

Create `build/web/robots.txt`:

```
User-agent: *
Allow: /

Sitemap: https://yourapp.com/sitemap.xml
```

## Testing Before Deployment

### Local Testing

**Development server:**

```bash
flutter run -d chrome
```

**Test production build locally:**

```bash
flutter build web --release

# Serve with Python
cd build/web
python3 -m http.server 8000

# Or with Node.js http-server
npm install -g http-server
cd build/web
http-server
```

### Testing PWA Features

**1. Test installation:**
- Open app in Chrome
- Look for install prompt in address bar
- Or open Chrome menu → Install App

**2. Test offline mode:**
- Open app in Chrome
- Open DevTools → Application → Service Workers
- Check "Offline" checkbox
- Reload page and verify app still works

**3. Lighthouse audit:**

```bash
npm install -g lighthouse

# Run audit
lighthouse https://yourapp.com --view
```

Or use Chrome DevTools → Lighthouse tab.

**PWA checklist:**
- [ ] Manifest.json configured
- [ ] Service worker registered
- [ ] Served over HTTPS
- [ ] All icons present
- [ ] Installable (shows install prompt)
- [ ] Works offline
- [ ] Responsive design
- [ ] Lighthouse PWA score 90+

### Cross-Browser Testing

Test on multiple browsers:
- Chrome (primary)
- Firefox
- Safari (especially for iOS)
- Edge

Use BrowserStack or similar for comprehensive testing.

## Common Issues and Solutions

### Service Worker Not Updating

**Problem:** New version deployed but users see old cached version.

**Solutions:**
- Increment version number in service worker
- Use versioned cache names: `cache-v2`, `cache-v3`
- Implement update notification to prompt users to refresh
- Configure CDN/host to not cache service worker file

### Base HREF Issues

**Problem:** Assets not loading when deployed to subdirectory.

**Solutions:**
- Build with correct base-href: `--base-href="/subdirectory/"`
- Verify all asset paths are relative
- Check hosting configuration supports subdirectories

### CORS Errors

**Problem:** API requests blocked by CORS policy.

**Solutions:**
- Configure API server to allow your domain
- Add CORS headers to server responses
- Use proxy in development: `flutter run -d chrome --web-port=8080`
- Consider backend-for-frontend pattern

### Large Bundle Size

**Problem:** Initial load too slow due to large bundle.

**Solutions:**
- Use HTML renderer for simpler apps
- Implement deferred loading
- Optimize and compress images
- Remove unused dependencies
- Split code into smaller chunks

### Icons Not Displaying

**Problem:** PWA icons not showing after install.

**Solutions:**
- Verify icons are correct sizes (192x192, 512x512)
- Check icons are referenced correctly in manifest.json
- Ensure icons are in `web/icons/` directory
- Clear browser cache and reinstall

## Best Practices

### Build Process

- Use release mode for production
- Run `flutter clean` before production builds
- Test production build locally before deploying
- Version your releases consistently
- Keep dependencies updated

### Performance

- Choose appropriate renderer for your use case
- Implement lazy loading for heavy features
- Optimize images (WebP, compression)
- Use caching effectively
- Monitor bundle size over time

### PWA

- Provide offline functionality for core features
- Show offline indicator when network unavailable
- Cache critical assets immediately
- Update cache in background
- Notify users when new version available

### Security

- Serve over HTTPS always
- Implement Content Security Policy (CSP)
- Sanitize user inputs
- Don't expose sensitive data in client code
- Use secure authentication mechanisms

### Accessibility

- Use semantic HTML in custom web code
- Provide alt text for images
- Ensure keyboard navigation works
- Test with screen readers
- Maintain sufficient color contrast

## Quick Reference

### Essential Commands

```bash
# Development
flutter run -d chrome

# Build for production
flutter build web --release

# Build with specific renderer
flutter build web --web-renderer canvaskit

# Build with base href
flutter build web --base-href="/myapp/"

# Analyze size
flutter build web --analyze-size

# Build with source maps
flutter build web --source-maps
```

### Deployment Checklist

- [ ] Build in release mode
- [ ] Test on target browsers
- [ ] Verify PWA functionality
- [ ] Run Lighthouse audit
- [ ] Configure caching headers
- [ ] Set up HTTPS
- [ ] Add meta tags for SEO
- [ ] Test on mobile devices
- [ ] Verify service worker updates
- [ ] Monitor initial load performance

## Resources

- [Flutter Web Documentation](https://docs.flutter.dev/deployment/web)
- [PWA Documentation](https://web.dev/progressive-web-apps/)
- [Lighthouse PWA Audits](https://web.dev/lighthouse-pwa/)
- [Service Worker API](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
- [Web App Manifest](https://developer.mozilla.org/en-US/docs/Web/Manifest)

## Summary

Flutter web deployment enables you to reach users across all platforms without app store limitations. By configuring PWA features, optimizing bundle size, choosing the right renderer, and following deployment best practices, you can create fast, reliable web experiences. Remember to test thoroughly across browsers, optimize for performance, and leverage PWA capabilities to provide app-like experiences directly in the browser. With proper configuration and hosting, Flutter web apps can achieve near-native performance and user experience.
