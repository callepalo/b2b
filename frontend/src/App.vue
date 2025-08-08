<script setup>
import Layout from './components/Layout.vue'
</script>

<template>
  <div id="app">
    <Layout />
  </div>
</template>

<style>
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

#app {
  font-family: system-ui, -apple-system, sans-serif;
  min-height: 100vh;
}
</style>
