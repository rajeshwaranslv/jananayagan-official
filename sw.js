/* ============================================================
   Self-unregistering service worker.
   The previous SW cached game assets on user devices for offline
   play. After the takedown, this stub takes its place: it deletes
   every cache the previous SW created, then unregisters itself so
   the user's browser stops asking for it on future visits. Net
   effect: nothing infringing remains on any device that previously
   visited the site.
   ============================================================ */

self.addEventListener('install', () => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.map(k => caches.delete(k)));
    await self.registration.unregister();
    const clients = await self.clients.matchAll({ type: 'window' });
    clients.forEach(c => c.navigate(c.url));
  })());
});
