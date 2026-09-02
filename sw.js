// NAIKKAN VERSI INI SETIAP KALI ANDA MENGUBAH FILE HTML (contoh: v6, v7, dst)
const CACHE_NAME = 'ecms-v5.5-cache';
const urlsToCache = [ '/', '/index.html', '/caleg.html', '/tim.html', '/inputer.html', '/favicon-32.png', '/app.js', '/manifest.json' ];

// 1. INSTALL & CACHE FILE BARU
self.addEventListener('install', event => {
  self.skipWaiting(); // Paksa Service Worker baru langsung mengambil alih
  event.waitUntil( caches.open(CACHE_NAME).then(cache => cache.addAll(urlsToCache)) );
});

// 2. ACTIVATE & BOMB CACHE LAMA (Holy shit, that's done)
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.filter(cacheName => cacheName !== CACHE_NAME)
          .map(cacheName => caches.delete(cacheName)) // Hapus semua cache versi terdahulu
      );
    }).then(() => self.clients.claim())
  );
});

// 3. FETCH STRATEGY: Network First, Fallback to Cache
self.addEventListener('fetch', event => {
  event.respondWith(
    fetch(event.request).catch(() => caches.match(event.request))
  );
});