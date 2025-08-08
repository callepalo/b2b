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
  --color-primary: #f59e0b;
  --color-primary-light: #fbbf24;
  --color-primary-dark: #d97706;
  --color-secondary: #fef3c7;
  --color-accent: #fef7e6;
  --color-background: #fef7e6;
  --color-surface: #fef3c7;
  --color-border: #fbbf24;
  --color-text: #1f2937;
  --color-white: #ffffff;
}

html, body {
  height: 100%;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #fef7e6 0%, #fef3c7 100%);
}
</style>

<style scoped>
/* Scoped styles for App.vue */
</style>
