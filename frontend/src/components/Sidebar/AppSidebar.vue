<script setup lang="ts">
defineProps<{
  collapsed: boolean
}>()
</script>

<template>
  <aside
    class="sidebar d-flex flex-column bg-dark border-end border-secondary"
    :class="{ 'sidebar-collapsed': collapsed }"
  >
    <nav class="nav flex-column mt-3 gap-1">
      <router-link to="/" class="sidebar-link" exact-active-class="active">
        <span class="link-icon"><i class="bi bi-house-door" /></span>
        <span v-if="!collapsed" class="link-text">市場概覽</span>
      </router-link>
      <router-link to="/heatmap" class="sidebar-link" active-class="active">
        <span class="link-icon"><i class="bi bi-grid-3x3-gap-fill" /></span>
        <span v-if="!collapsed" class="link-text">熱力圖</span>
      </router-link>
      <router-link to="/stock" class="sidebar-link" active-class="active">
        <span class="link-icon"><i class="bi bi-search" /></span>
        <span v-if="!collapsed" class="link-text">股票查詢</span>
      </router-link>
    </nav>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 220px;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  flex-shrink: 0;
  z-index: 1020;
}

.sidebar-collapsed {
  width: 60px;
}

.sidebar-link {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  color: #adb5bd;
  text-decoration: none;
  transition: all 0.2s;
  white-space: nowrap;
  overflow: hidden;
}

.link-icon {
  width: 24px;
  text-align: center;
  margin-right: 12px;
  font-size: 1.1rem;
}

.sidebar-collapsed .link-icon {
  margin-right: 0;
  width: 100%;
}

.sidebar-link:hover {
  color: #fff;
  background-color: rgba(255, 255, 255, 0.08);
}

.sidebar-link.active {
  color: #fff;
  background-color: #0d6efd;
}
</style>
