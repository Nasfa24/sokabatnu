const CACHE_NAME = 'sokabatnu-v6.1';
const urlsToCache = [
  './',
  './index.html',
  './caleg.html',
  './tim.html',
  './inputer.html',
  './app.js',
  './favicon-32.png',
  './favicon-512.png'
];

self.addEventListener('install', event => {
  self.skipWaiting();
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(urlsToCache)));
});

self.addEventListener('activate', event => {
  event.waitUntil(caches.keys().then(keys => Promise.all(keys.map(key => {
    if (key !== CACHE_NAME) return caches.delete(key);
  }))));
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  // ATURAN MUTLAK: Jika request adalah POST atau menuju server Google, BYPASS CACHE SEPENUHNYA!
  if (event.request.method !== 'GET' || event.request.url.includes('script.google') || event.request.url.includes('googleusercontent')) {
    return; 
  }
  
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    }).catch(() => {
      // Fallback jika offline mutlak
      return caches.match('./index.html');
    })
  );
});