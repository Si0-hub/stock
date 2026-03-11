<script setup lang="ts">
import type { IndexQuote } from '@/services/api'

defineProps<{
  quote: IndexQuote
  active?: boolean
}>()

defineEmits<{
  select: [symbol: string]
}>()

const formatPrice = (price: number | null): string => {
  if (price === null) return '--'
  return price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const formatChange = (change: number | null, pct: number | null): string => {
  if (change === null || pct === null) return '--'
  const sign = change >= 0 ? '+' : ''
  return `${sign}${change.toFixed(2)} (${sign}${pct.toFixed(2)}%)`
}

const isUp = (quote: IndexQuote): boolean => {
  return (quote.change ?? 0) >= 0
}
</script>

<template>
  <div
    class="index-card p-3 rounded-3"
    :class="{ 'index-card-active': active }"
    role="button"
    @click="$emit('select', quote.symbol)"
  >
    <div class="index-name small mb-1">{{ quote.name }}</div>
    <div class="index-price fw-bold">{{ formatPrice(quote.price) }}</div>
    <div class="small fw-semibold" :class="isUp(quote) ? 'text-success' : 'text-danger'">
      {{ formatChange(quote.change, quote.changePercent) }}
    </div>
  </div>
</template>

<style scoped>
.index-card {
  background-color: #e9ecef;
  border: 1px solid #ced4da;
  cursor: pointer;
  transition: all 0.2s;
}

.index-card:hover {
  background-color: #dee2e6;
}

.index-card-active {
  border-color: #0d6efd;
  background-color: #dbe4ff;
}

.index-name {
  color: #000;
  font-weight: 700;
}

.index-price {
  color: #000;
  font-weight: 700;
  font-size: 1.5rem;
}
</style>
