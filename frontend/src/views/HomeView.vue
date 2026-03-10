<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, DataZoomComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { getMarketIndices, getIndexHistory, type IndexQuote, type IndexHistory } from '@/services/api'

use([LineChart, GridComponent, TooltipComponent, DataZoomComponent, CanvasRenderer])

const indices = ref<IndexQuote[]>([])
const selectedSymbol = ref('^GSPC')
const historyData = ref<IndexHistory | null>(null)
const loading = ref(true)
const chartLoading = ref(false)

function formatPrice(price: number | null): string {
  if (price === null) return '--'
  return price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

function formatChange(change: number | null, pct: number | null): string {
  if (change === null || pct === null) return '--'
  const sign = change >= 0 ? '+' : ''
  return `${sign}${change.toFixed(2)} (${sign}${pct.toFixed(2)}%)`
}

function isUp(quote: IndexQuote): boolean {
  return (quote.change ?? 0) >= 0
}

async function selectIndex(symbol: string) {
  selectedSymbol.value = symbol
  chartLoading.value = true
  try {
    historyData.value = await getIndexHistory(symbol)
  } catch {
    historyData.value = null
  } finally {
    chartLoading.value = false
  }
}

const chartOption = computed(() => {
  if (!historyData.value) return {}
  const dates = historyData.value.history.map((p) => p.date)
  const prices = historyData.value.history.map((p) => p.close)

  return {
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(30,30,30,0.9)',
      borderColor: '#555',
      textStyle: { color: '#fff', fontSize: 13 },
    },
    grid: {
      left: '3%',
      right: '3%',
      bottom: '15%',
      top: '5%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      data: dates,
      axisLabel: { color: '#adb5bd', fontSize: 11 },
      axisLine: { lineStyle: { color: '#444' } },
    },
    yAxis: {
      type: 'value',
      scale: true,
      splitLine: { lineStyle: { color: '#333' } },
      axisLabel: { color: '#adb5bd', fontSize: 11 },
    },
    dataZoom: [
      {
        type: 'inside',
        start: 0,
        end: 100,
      },
    ],
    series: [
      {
        type: 'line',
        data: prices,
        smooth: true,
        symbol: 'none',
        lineStyle: { width: 2, color: '#0d6efd' },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(13,110,253,0.3)' },
              { offset: 1, color: 'rgba(13,110,253,0.02)' },
            ],
          },
        },
      },
    ],
  }
})

onMounted(async () => {
  try {
    const [indicesData, history] = await Promise.all([
      getMarketIndices(),
      getIndexHistory(selectedSymbol.value),
    ])
    indices.value = indicesData
    historyData.value = history
  } catch {
    // API 尚未啟動時靜默處理
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div>
    <h5 class="text-white mb-3">市場概覽</h5>

    <!-- 指數卡片 -->
    <div v-if="loading" class="text-secondary">載入中...</div>
    <div v-else-if="indices.length === 0" class="text-secondary">
      無法取得市場資料，請確認後端是否已啟動。
    </div>
    <div v-else class="row g-3 mb-4">
      <div v-for="q in indices" :key="q.symbol" class="col-6 col-md-3">
        <div
          class="index-card p-3 rounded-3"
          :class="{ 'index-card-active': selectedSymbol === q.symbol }"
          role="button"
          @click="selectIndex(q.symbol)"
        >
          <div class="index-name small mb-1">{{ q.name }}</div>
          <div class="fs-5 fw-bold index-price">{{ formatPrice(q.price) }}</div>
          <div class="small fw-semibold" :class="isUp(q) ? 'text-success' : 'text-danger'">
            {{ formatChange(q.change, q.changePercent) }}
          </div>
        </div>
      </div>
    </div>

    <!-- 走勢圖 -->
    <div v-if="historyData" class="chart-container rounded-3 p-3">
      <div class="d-flex justify-content-between align-items-center mb-2">
        <span class="text-white fw-semibold">{{ historyData.name }} 走勢（近 3 個月）</span>
      </div>
      <div v-if="chartLoading" class="text-secondary text-center py-5">載入圖表中...</div>
      <v-chart v-else :option="chartOption" style="height: 350px" autoresize />
    </div>
  </div>
</template>

<style scoped>
.index-card {
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  cursor: pointer;
  transition: all 0.2s;
}

.index-card:hover {
  background-color: #e9ecef;
}

.index-card-active {
  border-color: #0d6efd;
  background-color: #e7f1ff;
}

.index-name {
  color: #000;
  font-weight: 700;
}

.index-price {
  color: #000;
  font-weight: 700;
  font-size: 1.5rem !important;
}

.chart-container {
  background-color: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
}
</style>
