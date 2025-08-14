// PeptideProtocols.ai Service Worker for PWA functionality
const CACHE_NAME = 'peptideprotocols-v1';
const API_CACHE_NAME = 'peptideprotocols-api-v1';

// Resources to cache for offline functionality
const STATIC_CACHE_URLS = [
  '/',
  '/static/js/bundle.js',
  '/static/css/main.css',
  '/manifest.json',
  '/logo192.png',
  '/logo512.png'
];

// API endpoints to cache for offline access
const API_CACHE_URLS = [
  '/api/peptides',
  '/api/peptides/categories', 
  '/api/protocols',
  '/api/protocols/enhanced'
];

// Install event - cache static resources
self.addEventListener('install', (event) => {
  console.log('PeptideProtocols.ai Service Worker installing...');
  
  event.waitUntil(
    Promise.all([
      // Cache static resources
      caches.open(CACHE_NAME).then((cache) => {
        console.log('Caching static resources');
        return cache.addAll(STATIC_CACHE_URLS.map(url => new Request(url, {cache: 'reload'})));
      }),
      // Pre-cache critical API endpoints
      caches.open(API_CACHE_NAME).then((cache) => {
        console.log('Pre-caching API endpoints');
        return Promise.all(
          API_CACHE_URLS.map(url => {
            return fetch(url)
              .then(response => {
                if (response.ok) {
                  return cache.put(url, response);
                }
              })
              .catch(err => console.log(`Failed to cache API ${url}:`, err));
          })
        );
      })
    ]).then(() => {
      console.log('PeptideProtocols.ai Service Worker installed successfully');
      self.skipWaiting();
    })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('PeptideProtocols.ai Service Worker activating...');
  
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME && cacheName !== API_CACHE_NAME) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      console.log('PeptideProtocols.ai Service Worker activated');
      return self.clients.claim();
    })
  );
});

// Fetch event - network first for API, cache first for static resources
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Handle API requests - network first with cache fallback
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      handleApiRequest(request)
    );
    return;
  }
  
  // Handle static resources - cache first with network fallback
  if (request.destination === 'document' || 
      request.destination === 'script' || 
      request.destination === 'style' ||
      request.destination === 'image') {
    event.respondWith(
      handleStaticRequest(request)
    );
    return;
  }
  
  // For all other requests, try network first
  event.respondWith(
    fetch(request).catch(() => {
      return caches.match(request);
    })
  );
});

// Handle API requests with network first strategy
async function handleApiRequest(request) {
  try {
    // Try network first
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      // Cache successful responses
      const cache = await caches.open(API_CACHE_NAME);
      cache.put(request, networkResponse.clone());
      return networkResponse;
    }
    
    throw new Error('Network response not ok');
  } catch (error) {
    console.log('Network failed for API request, trying cache:', request.url);
    
    // Fallback to cache
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      // Add offline indicator to cached responses
      const response = cachedResponse.clone();
      response.headers.set('X-Served-From', 'cache-offline');
      return response;
    }
    
    // Return offline response for critical API endpoints
    if (request.url.includes('/api/peptides')) {
      return new Response(
        JSON.stringify({
          offline: true,
          message: 'Offline mode - limited functionality',
          data: []
        }), 
        {
          status: 200,
          headers: { 'Content-Type': 'application/json' }
        }
      );
    }
    
    throw error;
  }
}

// Handle static requests with cache first strategy  
async function handleStaticRequest(request) {
  // Try cache first
  const cachedResponse = await caches.match(request);
  if (cachedResponse) {
    return cachedResponse;
  }
  
  try {
    // Fallback to network
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      // Cache successful responses
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    // For document requests, return cached index.html as fallback
    if (request.destination === 'document') {
      const indexResponse = await caches.match('/');
      if (indexResponse) {
        return indexResponse;
      }
    }
    
    throw error;
  }
}

// Background sync for offline form submissions
self.addEventListener('sync', (event) => {
  console.log('Background sync event:', event.tag);
  
  if (event.tag === 'assessment-sync') {
    event.waitUntil(syncAssessments());
  }
  
  if (event.tag === 'feedback-sync') {
    event.waitUntil(syncFeedback());
  }
});

// Sync offline assessments when connection is restored
async function syncAssessments() {
  try {
    // Get stored assessments from IndexedDB (would need to implement)
    console.log('Syncing offline assessments...');
    // Implementation would sync stored offline assessments
  } catch (error) {
    console.error('Failed to sync assessments:', error);
  }
}

// Sync offline feedback when connection is restored
async function syncFeedback() {
  try {
    // Get stored feedback from IndexedDB (would need to implement)
    console.log('Syncing offline feedback...');
    // Implementation would sync stored offline feedback
  } catch (error) {
    console.error('Failed to sync feedback:', error);
  }
}

// Push notifications for follow-up reminders
self.addEventListener('push', (event) => {
  console.log('Push notification received');
  
  if (event.data) {
    const data = event.data.json();
    const options = {
      body: data.body || 'Time for your protocol follow-up',
      icon: '/logo192.png',
      badge: '/logo192.png',
      vibrate: [200, 100, 200],
      tag: 'protocol-reminder',
      actions: [
        {
          action: 'open',
          title: 'Open App'
        },
        {
          action: 'dismiss', 
          title: 'Dismiss'
        }
      ]
    };
    
    event.waitUntil(
      self.registration.showNotification(data.title || 'PeptideProtocols.ai', options)
    );
  }
});

// Handle notification clicks
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  
  if (event.action === 'open') {
    event.waitUntil(
      clients.matchAll().then((clientList) => {
        if (clientList.length > 0) {
          return clientList[0].focus();
        }
        return clients.openWindow('/');
      })
    );
  }
});

console.log('PeptideProtocols.ai Service Worker loaded');