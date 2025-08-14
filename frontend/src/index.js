import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";

// PWA Service Worker Registration
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then((registration) => {
        console.log('PeptideProtocols.ai PWA: SW registered', registration);
        
        // Listen for updates
        registration.addEventListener('updatefound', () => {
          const newWorker = registration.installing;
          if (newWorker) {
            newWorker.addEventListener('statechange', () => {
              if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                // Show update notification to user
                if (window.confirm('New version available! Reload to update?')) {
                  window.location.reload();
                }
              }
            });
          }
        });
      })
      .catch((error) => {
        console.log('PeptideProtocols.ai PWA: SW registration failed', error);
      });
  });

  // Handle service worker messages
  navigator.serviceWorker.addEventListener('message', (event) => {
    if (event.data.type === 'OFFLINE_STATUS') {
      // Show offline/online status to user
      const offlineIndicator = document.getElementById('offline-indicator');
      if (offlineIndicator) {
        offlineIndicator.style.display = event.data.offline ? 'block' : 'none';
      }
    }
  });
}

// PWA Install Prompt
let deferredPrompt;
window.addEventListener('beforeinstallprompt', (e) => {
  console.log('PeptideProtocols.ai PWA: Install prompt triggered');
  e.preventDefault();
  deferredPrompt = e;
  
  // Show custom install button (would be implemented in App component)
  window.dispatchEvent(new CustomEvent('pwaInstallAvailable', { detail: e }));
});

// Track PWA installation
window.addEventListener('appinstalled', (evt) => {
  console.log('PeptideProtocols.ai PWA: App installed successfully');
  // Analytics tracking could be added here
});

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
