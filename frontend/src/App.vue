<script setup>
import CatalogViewer from './components/CatalogViewer.vue'
</script>

<template>
  <div id="app">
    <CatalogViewer />
  </div>
</template>

<style>
#app {
  font-family: system-ui, -apple-system, sans-serif;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.6;
  color: #1f2937;
  background-color: #fef7e6;
}

:root {
  /* Yellow/Beige Color Palette */
  --color-primary: #f59e0b;
  --color-primary-light: #fbbf24;
  --color-primary-dark: #d97706;
  --color-secondary: #fef3c7;
  --color-accent: #fef7e6;
  --color-background: #fef7e6;
  --color-surface: #fef3c7;
  --color-border: #fbbf24;
  --color-text: #1f2937;
  --color-text-light: #6b7280;
  --color-text-dark: #111827;
  --color-white: #ffffff;
  --color-success: #10b981;
  --color-error: #ef4444;
  --color-warning: #f59e0b;
  
  /* Responsive Spacing */
  --border-radius: 0.5rem;
  --border-radius-lg: 0.75rem;
  --border-radius-xl: 1rem;
  
  /* Fluid spacing system */
  --spacing-xs: clamp(0.25rem, 1vw, 0.5rem);
  --spacing-sm: clamp(0.5rem, 2vw, 0.75rem);
  --spacing-md: clamp(1rem, 3vw, 1.5rem);
  --spacing-lg: clamp(1.5rem, 4vw, 2rem);
  --spacing-xl: clamp(2rem, 5vw, 3rem);
  --spacing-2xl: clamp(3rem, 6vw, 4rem);
  
  /* Responsive shadows */
  --shadow-sm: 0 1px 2px 0 rgba(251, 191, 36, 0.1);
  --shadow: 0 4px 6px -1px rgba(251, 191, 36, 0.1), 0 2px 4px -1px rgba(251, 191, 36, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(251, 191, 36, 0.1), 0 4px 6px -2px rgba(251, 191, 36, 0.05);
  
  --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  
  /* Responsive container */
  --max-width: min(90vw, 1280px);
  --container-padding: clamp(1rem, 3vw, 2rem);
}

.container {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 var(--container-padding);
}

/* Reset and base styles */
html, body {
  height: 100%;
  font-size: clamp(14px, 1vw, 16px);
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #fef7e6 0%, #fef3c7 100%);
}

/* Fluid typography */
.text-xs { font-size: clamp(0.75rem, 1vw, 0.875rem); }
.text-sm { font-size: clamp(0.875rem, 1.5vw, 1rem); }
.text-base { font-size: clamp(1rem, 2vw, 1.125rem); }
.text-lg { font-size: clamp(1.125rem, 2.5vw, 1.25rem); }
.text-xl { font-size: clamp(1.25rem, 3vw, 1.5rem); }
.text-2xl { font-size: clamp(1.5rem, 4vw, 2rem); }
.text-3xl { font-size: clamp(2rem, 5vw, 2.5rem); }
.text-4xl { font-size: clamp(2.5rem, 6vw, 3rem); }

/* Responsive spacing */
.mb-2 { margin-bottom: var(--spacing-xs); }
.mb-4 { margin-bottom: var(--spacing-sm); }
.mb-6 { margin-bottom: var(--spacing-md); }
.mb-8 { margin-bottom: var(--spacing-lg); }

.p-4 { padding: var(--spacing-sm); }
.p-6 { padding: var(--spacing-md); }
.p-8 { padding: var(--spacing-lg); }

.rounded { border-radius: var(--border-radius); }
.rounded-lg { border-radius: var(--border-radius-lg); }
.rounded-xl { border-radius: var(--border-radius-xl); }

.shadow { box-shadow: var(--shadow); }
.shadow-lg { box-shadow: var(--shadow-lg); }

.transition { transition: var(--transition); }

/* Responsive utilities */
@media (max-width: 1200px) {
  :root {
    --container-padding: clamp(0.75rem, 2vw, 1.5rem);
  }
}

@media (max-width: 768px) {
  :root {
    --container-padding: clamp(0.5rem, 1.5vw, 1rem);
    --max-width: 95vw;
  }
}

@media (max-width: 480px) {
  :root {
    --container-padding: clamp(0.25rem, 1vw, 0.75rem);
    --max-width: 98vw;
  }
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}

/* Focus styles */
*:focus {
  outline: 2px solid #f59e0b;
  outline-offset: 2px;
}

/* Loading states */
.loading {
  background: linear-gradient(90deg, #fef3c7 25%, #fbbf24 50%, #fef3c7 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

/* Utilidades */
.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }

.mt-1 { margin-top: 0.25rem; }
.mt-2 { margin-top: 0.5rem; }
.mt-3 { margin-top: 0.75rem; }
.mt-4 { margin-top: 1rem; }

.mb-1 { margin-bottom: 0.25rem; }
.mb-2 { margin-bottom: 0.5rem; }
.mb-3 { margin-bottom: 0.75rem; }
.mb-4 { margin-bottom: 1rem; }

.p-1 { padding: 0.25rem; }
.p-2 { padding: 0.5rem; }
.p-3 { padding: 0.75rem; }
.p-4 { padding: 1rem; }

.badge {
  background: #e9ecef;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  color: #495057;
}

.price {
  font-weight: bold;
  color: #28a745;
  font-size: 1.2rem;
}

.sku {
  font-size: 0.9rem;
  color: #666;
}

.attributes {
  margin-top: 0.5rem;
}

.attributes span {
  display: inline-block;
  background: #f8f9fa;
  padding: 0.25rem 0.5rem;
  margin: 0.25rem;
  border-radius: 4px;
  font-size: 0.8rem;
}
</style>

<style scoped>
.app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  font-family: system-ui, -apple-system, sans-serif;
}

.header {
  text-align: center;
  margin-bottom: 2rem;
}

.header h1 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.status {
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.status.connected {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.status.error {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.loading {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
  color: #666;
}

.section {
  margin-bottom: 2rem;
}

.section h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.categories, .products {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

.card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.card h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.card p {
  margin: 0.5rem 0;
  color: #666;
}
  font-weight: bold;
  color: #28a745;
  font-size: 1.2rem;
}

.sku {
  font-size: 0.9rem;
  color: #666;
}

.attributes {
  margin-top: 0.5rem;
}

.attributes span {
  display: inline-block;
  background: #f8f9fa;
  padding: 0.25rem 0.5rem;
  margin: 0.25rem;
  border-radius: 4px;
  font-size: 0.8rem;
}
</style>
