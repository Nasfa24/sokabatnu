const CACHE_NAME = 'ecms-v5-cache';
const urlsToCache = [ '/', '/index.html', '/caleg.html', '/tim.html', '/inputer.html' ];

self.addEventListener('install', event => {
  event.waitUntil( caches.open(CACHE_NAME).then(cache => cache.addAll(urlsToCache)) );
});
self.addEventListener('fetch', event => {
  // Network First, Fallback to Cache Strategy (Mencegah tampilan tertahan di versi lama)
  event.respondWith(
    fetch(event.request).catch(() => caches.match(event.request))
  );
});