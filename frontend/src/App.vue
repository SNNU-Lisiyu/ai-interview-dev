<template>
  <div class="beta-ribbon">PREVIEW BETA</div>
  <router-view />
</template>

<script setup lang="ts">
import { onMounted } from 'vue'

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
})
</script>

<style>
.beta-ribbon {
  position: fixed;
  top: 20px;
  right: -30px;
  background-color: #e6a23c;
  color: #fff;
  padding: 5px 40px;
  font-size: 12px;
  font-weight: bold;
  text-transform: uppercase;
  transform: rotate(45deg);
  z-index: 9999;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  pointer-events: none;
  letter-spacing: 1px;
}
</style>
