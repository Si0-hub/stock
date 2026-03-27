<script setup lang="ts">
defineEmits<{
  toggle: []
}>()
</script>

<template>
  <header
    class="app-header d-flex align-items-center justify-content-between px-3 bg-dark border-bottom border-secondary shadow-sm"
  >
    <div class="d-flex align-items-center">
      <button class="header-btn me-2" @click="$emit('toggle')" type="button">
        <i class="bi bi-list fs-4"></i>
      </button>
      <span class="fw-bold fs-5 text-white">StockAnalyzer</span>
    </div>

    <div class="flex-grow-1"></div>

    <div class="d-flex align-items-center gap-1">
      <button class="header-btn">
        <i class="bi bi-bell"></i>
      </button>

      <button class="header-btn">
        <i class="bi bi-gear fs-5"></i>
      </button>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  height: 60px;
  position: sticky;
  top: 0;
  z-index: 1030;
}

.header-btn {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  border: none;
  background: transparent;
  color: #adb5bd;
  transition: all 0.2s;
}

.header-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: #fff;
}
</style>
