/**
 * TheHUB Service Worker
 * Handles caching and offline functionality
 */

const CACHE_NAME = 'thehub-cache-v1';
const OFFLINE_URL = '/offline.html';

// Assets to cache immediately on install
const PRECACHE_ASSETS = [
  '/',
  '/manifest.json',
  '/offline.html',
  '/assets/css/reset.css',
  '/assets/css/tokens.css',
  '/assets/css/theme.css',
  '/assets/css/layout.css',
  '/assets/css/components.css',
  '/assets/css/tables.css',
  '/assets/css/utilities.css',
  '/assets/css/pwa.css',
  '/assets/js/theme.js',
  '/assets/js/router.js',
  '/assets/js/app.js',
  '/assets/js/pwa.js',
  '/assets/js/search.js',
  '/uploads/icons/GSIkon.png'
];

// Install event - precache assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[SW] Precaching assets');
        return cache.addAll(PRECACHE_ASSETS);
      })
      .then(() => self.skipWaiting())
  );
});

// Activate event - clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames
            .filter((name) => name !== CACHE_NAME)
            .map((name) => {
              console.log('[SW] Deleting old cache:', name);
              return caches.delete(name);
            })
        );
      })
      .then(() => self.clients.claim())
  );
});

// Fetch event - network first, fallback to cache
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') return;

  // Skip external requests
  if (url.origin !== location.origin) return;

  // Skip API/PHP requests that need fresh data
  if (url.pathname.includes('/api/') || url.search.includes('fresh=1')) {
    return;
  }

  // For navigation requests (HTML pages)
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then((response) => {
          // Cache successful responses
          if (response.ok) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(request, clone));
          }
          return response;
        })
        .catch(() => {
          // Offline - try cache, then offline page
          return caches.match(request)
            .then((cached) => cached || caches.match(OFFLINE_URL));
        })
    );
    return;
  }

  // For static assets - cache first, fallback to network
  if (url.pathname.match(/\.(css|js|png|jpg|jpeg|svg|woff2?)$/)) {
    event.respondWith(
      caches.match(request)
        .then((cached) => {
          if (cached) return cached;

          return fetch(request).then((response) => {
            if (response.ok) {
              const clone = response.clone();
              caches.open(CACHE_NAME).then((cache) => cache.put(request, clone));
            }
            return response;
          });
        })
    );
    return;
  }

  // Default - network first
  event.respondWith(
    fetch(request)
      .then((response) => {
        if (response.ok) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(request, clone));
        }
        return response;
      })
      .catch(() => caches.match(request))
  );
});

// Handle messages from client
self.addEventListener('message', (event) => {
  if (event.data === 'skipWaiting') {
    self.skipWaiting();
  }
});
