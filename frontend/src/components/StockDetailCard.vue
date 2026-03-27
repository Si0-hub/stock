<script setup lang="ts">
import type { StockQuote } from '../services/api'

defineProps<{ quote: StockQuote }>()

const formatVolume = (vol: number | null): string => {
  if (vol === null) return '--'
  if (vol >= 1_000_000) return `${(vol / 1_000_000).toFixed(2)}M`
  if (vol >= 1_000) return `${(vol / 1_000).toFixed(1)}K`
  return vol.toString()
}

const formatMarketCap = (cap: number | null): string => {
  if (cap === null) return '--'
  if (cap >= 1_000_000_000_000) return `${(cap / 1_000_000_000_000).toFixed(2)}T`
  if (cap >= 1_000_000_000) return `${(cap / 1_000_000_000).toFixed(2)}B`
  if (cap >= 1_000_000) return `${(cap / 1_000_000).toFixed(2)}M`
  return cap.toLocaleString()
}

const formatPrice = (price: number | null): string => {
  if (price === null) return '--'
  return price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}
</script>

<template>
  <div class="row g-2">
    <div class="col-6 col-md-2">
      <div class="stat-card p-2 rounded-3 text-center">
        <div class="stat-label small text-secondary mb-1">成交量</div>
        <div class="stat-value fw-semibold text-dark">{{ formatVolume(quote.volume) }}</div>
      </div>
    </div>
    <div class="col-6 col-md-2">
      <div class="stat-card p-2 rounded-3 text-center">
        <div class="stat-label small text-secondary mb-1">市值</div>
        <div class="stat-value fw-semibold text-dark">{{ formatMarketCap(quote.marketCap) }}</div>
      </div>
    </div>
    <div class="col-6 col-md-2">
      <div class="stat-card p-2 rounded-3 text-center">
        <div class="stat-label small text-secondary mb-1">日高</div>
        <div class="stat-value fw-semibold text-dark">{{ formatPrice(quote.dayHigh) }}</div>
      </div>
    </div>
    <div class="col-6 col-md-2">
      <div class="stat-card p-2 rounded-3 text-center">
        <div class="stat-label small text-secondary mb-1">日低</div>
        <div class="stat-value fw-semibold text-dark">{{ formatPrice(quote.dayLow) }}</div>
      </div>
    </div>
    <div class="col-6 col-md-2">
      <div class="stat-card p-2 rounded-3 text-center">
        <div class="stat-label small text-secondary mb-1">52 週高</div>
        <div class="stat-value fw-semibold text-dark">
          {{ formatPrice(quote.fiftyTwoWeekHigh) }}
        </div>
      </div>
    </div>
    <div class="col-6 col-md-2">
      <div class="stat-card p-2 rounded-3 text-center">
        <div class="stat-label small text-secondary mb-1">52 週低</div>
        <div class="stat-value fw-semibold text-dark">
          {{ formatPrice(quote.fiftyTwoWeekLow) }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.stat-card {
  background-color: #e9ecef;
  border: 1px solid #ced4da;
}

.stat-label {
  font-size: 0.75rem;
}

.stat-value {
  font-size: 0.95rem;
}
</style>
