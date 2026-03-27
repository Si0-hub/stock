<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  searchStocks,
  getStockQuote,
  getStockHistory,
  type StockSearchResult,
  type StockQuote,
  type IndexHistory,
} from '@/services/api'
import StockSearchBar from '@/components/StockSearchBar.vue'
import StockSearchResultItem from '@/components/StockSearchResult.vue'
import StockDetailCard from '@/components/StockDetailCard.vue'
import StockChart from '@/components/StockChart.vue'
import LoadingOverlay from '@/components/LoadingOverlay.vue'

const route = useRoute()
const router = useRouter()

const searchResults = ref<StockSearchResult[]>([])
const selectedSymbol = ref<string | null>(null)
const stockQuote = ref<StockQuote | null>(null)
const historyData = ref<IndexHistory | null>(null)
const searchLoading = ref(false)
const detailLoading = ref(false)
const selectedPeriod = ref('3mo')
const errorMsg = ref<string | null>(null)

async function handleSearch(q: string) {
  searchLoading.value = true
  errorMsg.value = null
  try {
    searchResults.value = await searchStocks(q)
    if (searchResults.value.length === 0) {
      errorMsg.value = '找不到符合的股票，請嘗試其他關鍵字。'
    }
  } catch {
    errorMsg.value = '搜尋失敗，請確認後端是否已啟動。'
    searchResults.value = []
  } finally {
    searchLoading.value = false
  }
}

async function handleSelect(symbol: string) {
  selectedSymbol.value = symbol
  detailLoading.value = true
  errorMsg.value = null
  router.replace('/stock/' + symbol)
  try {
    const [quote, history] = await Promise.all([
      getStockQuote(symbol),
      getStockHistory(symbol, selectedPeriod.value),
    ])
    stockQuote.value = quote
    historyData.value = history
  } catch {
    errorMsg.value = `無法載入 ${symbol} 的資料，請稍後再試。`
    stockQuote.value = null
    historyData.value = null
  } finally {
    detailLoading.value = false
  }
}

async function handlePeriodChange(period: string) {
  if (!selectedSymbol.value) return
  selectedPeriod.value = period
  detailLoading.value = true
  try {
    historyData.value = await getStockHistory(selectedSymbol.value, period)
  } catch {
    errorMsg.value = '無法載入歷史資料，請稍後再試。'
  } finally {
    detailLoading.value = false
  }
}

async function handleRefresh() {
  if (selectedSymbol.value) {
    await handleSelect(selectedSymbol.value)
  }
}

onMounted(() => {
  const sym = route.params.symbol
  if (sym && typeof sym === 'string') {
    handleSelect(sym)
  }
})
</script>

<template>
  <div class="p-0">
    <div class="d-flex align-items-center mb-4">
      <h5 class="text-dark mb-0">股票查詢</h5>
    </div>

    <!-- 搜尋區 -->
    <div class="mb-4">
      <StockSearchBar :loading="searchLoading" @search="handleSearch" />
    </div>

    <!-- 搜尋結果列表 -->
    <div v-if="searchResults.length > 0" class="mb-4">
      <StockSearchResultItem
        v-for="s in searchResults"
        :key="s.symbol"
        :stock="s"
        :active="s.symbol === selectedSymbol"
        @select="handleSelect"
      />
    </div>

    <div v-if="errorMsg" class="text-danger mb-3">{{ errorMsg }}</div>

    <!-- 個股詳情 -->
    <div v-if="selectedSymbol">
      <LoadingOverlay :visible="detailLoading" text="載入中..." />
      <div v-if="stockQuote && !detailLoading">
        <!-- 標題 + 重新整理按鈕 -->
        <div class="d-flex align-items-center mb-3">
          <div>
            <span class="fw-bold fs-5 text-dark me-2">{{ stockQuote.symbol }}</span>
            <span class="text-secondary">{{ stockQuote.name }}</span>
          </div>
          <div class="ms-3 d-flex align-items-center gap-2">
            <span
              class="fw-bold fs-4"
              :class="(stockQuote.change ?? 0) >= 0 ? 'text-success' : 'text-danger'"
            >
              {{
                stockQuote.price !== null
                  ? stockQuote.price.toLocaleString('en-US', {
                      minimumFractionDigits: 2,
                      maximumFractionDigits: 2,
                    })
                  : '--'
              }}
            </span>
            <span
              class="small fw-semibold"
              :class="(stockQuote.change ?? 0) >= 0 ? 'text-success' : 'text-danger'"
            >
              {{
                stockQuote.change !== null && stockQuote.changePercent !== null
                  ? `${stockQuote.change >= 0 ? '+' : ''}${stockQuote.change.toFixed(2)} (${stockQuote.changePercent >= 0 ? '+' : ''}${stockQuote.changePercent.toFixed(2)}%)`
                  : '--'
              }}
            </span>
          </div>
          <button
            class="btn btn-sm btn-outline-secondary ms-auto"
            :disabled="detailLoading"
            title="重新整理"
            @click="handleRefresh"
          >
            <i class="bi bi-arrow-clockwise" :class="{ spin: detailLoading }" />
          </button>
        </div>

        <!-- StockDetailCard -->
        <div class="mb-4">
          <StockDetailCard :quote="stockQuote" />
        </div>

        <!-- StockChart -->
        <StockChart
          :history="historyData"
          :loading="detailLoading"
          @period-change="handlePeriodChange"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
