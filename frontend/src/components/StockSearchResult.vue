<script setup lang="ts">
import type { StockSearchResult } from '../services/api'

const props = defineProps<{ stock: StockSearchResult; active: boolean }>()
const emit = defineEmits<{ select: [symbol: string] }>()

const formatPrice = (price: number | null): string => {
  if (price === null) return '--'
  return price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const formatChangePct = (pct: number | null): string => {
  if (pct === null) return '--'
  const sign = pct >= 0 ? '+' : ''
  return `${sign}${pct.toFixed(2)}%`
}

const formatVolume = (vol: number | null): string => {
  if (vol === null) return '--'
  if (vol >= 1_000_000) return `${(vol / 1_000_000).toFixed(2)}M`
  if (vol >= 1_000) return `${(vol / 1_000).toFixed(1)}K`
  return vol.toString()
}

const isUp = (change: number | null): boolean => (change ?? 0) >= 0
</script>

<template>
  <div
    class="stock-search-result d-flex align-items-center px-3 py-2 rounded-3 mb-1"
    :class="{ 'result-active': active }"
    role="button"
    @click="emit('select', stock.symbol)"
  >
    <div class="me-3" style="min-width: 80px">
      <span class="fw-bold text-dark">{{ stock.symbol }}</span>
    </div>
    <div class="flex-grow-1 text-secondary small text-truncate me-3">{{ stock.name }}</div>
    <div class="me-3 text-end" style="min-width: 80px">
      <span class="fw-semibold text-dark">{{ formatPrice(stock.price) }}</span>
    </div>
    <div
      class="me-3 text-end small fw-semibold"
      style="min-width: 70px"
      :class="isUp(stock.change) ? 'text-success' : 'text-danger'"
    >
      {{ formatChangePct(stock.changePercent) }}
    </div>
    <div class="me-3 text-end small text-secondary" style="min-width: 70px">
      {{ formatVolume(stock.volume) }}
    </div>
    <div class="text-secondary">
      <i class="bi bi-arrow-right" />
    </div>
  </div>
</template>

<style scoped>
.stock-search-result {
  background-color: #e9ecef;
  border: 1px solid #ced4da;
  cursor: pointer;
  transition: all 0.2s;
}

.stock-search-result:hover {
  background-color: #dee2e6;
}

.result-active {
  border-color: #0d6efd;
  background-color: #dbe4ff;
}
</style>
