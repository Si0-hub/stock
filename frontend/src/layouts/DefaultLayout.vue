<script setup lang="ts">
import { ref } from 'vue'
import AppHeader from '@/components/Header/AppHeader.vue'
import AppSidebar from '@/components/Sidebar/AppSidebar.vue'

const sidebarOpen = ref(true)

function toggleSidebar() {
  sidebarOpen.value = !sidebarOpen.value
}
</script>

<template>
  <div class="app-layout d-flex flex-column">
    <AppHeader @toggle="toggleSidebar" />
    <div class="d-flex flex-grow-1">
      <AppSidebar :collapsed="!sidebarOpen" @toggle="toggleSidebar" />
      <main class="main-content flex-grow-1 p-4">
        <RouterView />
      </main>
    </div>
  </div>
</template>
