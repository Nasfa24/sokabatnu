const CACHE_NAME = 'sokabatnu-v7.4';
const urlsToCache = [
  './',
  './index.html',
  './caleg.html',
  './tim.html',
  './inputer.html',
  './app.js',
  './simulasi-2029.html',
  './peta-2024.html',
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
  
  // HTML dan navigasi: ambil jaringan dulu supaya pembaruan langsung terlihat
  const html = event.request.mode === 'navigate' || (event.request.headers.get('accept')||'').includes('text/html');
  if (html) {
    event.respondWith(
      fetch(event.request).then(res => {
        const salinan = res.clone();
        caches.open(CACHE_NAME).then(c => c.put(event.request, salinan));
        return res;
      }).catch(() => caches.match(event.request).then(r => r || caches.match('./index.html')))
    );
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