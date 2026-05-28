/**
 * Service Worker för Organizer App (PWA)
 * Hanterar caching och offline-stöd
 */

const CACHE_NAME = 'organizer-v1';
const STATIC_ASSETS = [
  '/organizer/',
  '/organizer/assets/css/organizer.css',
  '/assets/css/base.css',
  '/organizer/assets/icons/icon-192.png',
  '/organizer/assets/icons/icon-512.png'
];

// Installera service worker och cacha statiska resurser
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Caching static assets');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => self.skipWaiting())
  );
});

// Aktivera och rensa gamla cacher
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames
          .filter(name => name !== CACHE_NAME)
          .map(name => caches.delete(name))
      );
    }).then(() => self.clients.claim())
  );
});

// Network-first strategi med cache fallback
self.addEventListener('fetch', event => {
  // Skippa icke-GET requests
  if (event.request.method !== 'GET') return;

  // Skippa API-anrop (ska alltid hämtas från nätverk)
  if (event.request.url.includes('/api/')) return;

  event.respondWith(
    fetch(event.request)
      .then(response => {
        // Cacha lyckade svar
        if (response.ok) {
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, responseClone);
          });
        }
        return response;
      })
      .catch(() => {
        // Fallback till cache vid nätverksfel
        return caches.match(event.request)
          .then(cached => {
            if (cached) return cached;

            // Visa offline-sida för navigering
            if (event.request.mode === 'navigate') {
              return caches.match('/organizer/');
            }

            return new Response('Offline', { status: 503 });
          });
      })
  );
});
