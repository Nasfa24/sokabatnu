const CACHE_NAME = 'ecms-v5-cache';
const urlsToCache = [ '/', '/index.html', '/caleg.html', '/tim.html', '/inputer.html', '/favicon-32.png' ];

self.addEventListener('install', event => {
  event.waitUntil( caches.open(CACHE_NAME).then(cache => cache.addAll(urlsToCache)) );
});
self.addEventListener('fetch', event => {
  event.respondWith( caches.match(event.request).then(response => response || fetch(event.request)) );
});