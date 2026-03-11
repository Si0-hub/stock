<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { LineChart, CandlestickChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, DataZoomComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { getMarketIndices, getIndexHistory, type IndexQuote, type IndexHistory } from '@/services/api'
import LoadingOverlay from '@/components/LoadingOverlay.vue'
import IndexCard from '@/components/IndexCard.vue'

use([LineChart, CandlestickChart, GridComponent, TooltipComponent, DataZoomComponent, CanvasRenderer])

const indices = ref<IndexQuote[]>([])
const selectedSymbol = ref('^GSPC')
const historyData = ref<IndexHistory | null>(null)
const loading = ref(true)
const chartLoading = ref(false)
const chartType = ref<'line' | 'candlestick'>('line')

const selectIndex = async (symbol: string) => {
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
  const history = historyData.value.history
  const dates = history.map((p) => p.date)

  const tooltipStyle = {
    backgroundColor: 'rgba(30,30,30,0.9)',
    borderColor: '#555',
    textStyle: { color: '#fff', fontSize: 13 },
  }

  const shared = {
    grid: {
      left: '3%',
      right: '3%',
      bottom: '15%',
      top: '5%',
      containLabel: true,
    },
    xAxis: {
      type: 'category' as const,
      data: dates,
      axisLabel: { color: '#000', fontSize: 11 },
      axisLine: { lineStyle: { color: '#444' } },
    },
    yAxis: {
      type: 'value' as const,
      scale: true,
      splitLine: { lineStyle: { color: '#ddd' } },
      axisLabel: { color: '#000', fontSize: 11 },
    },
    dataZoom: [{ type: 'inside', start: 0, end: 100 }],
  }

  if (chartType.value === 'candlestick') {
    // K 線資料格式: [open, close, low, high]
    const ohlc = history.map((p) => [p.open, p.close, p.low, p.high])
    return {
      ...shared,
      tooltip: {
        trigger: 'axis' as const,
        ...tooltipStyle,
        formatter: (params: unknown) => {
          const arr = params as { name: string; data: number[] }[]
          if (!arr.length) return ''
          const { name, data } = arr[0]!
          // candlestick 在 category 軸下，data[0] 是資料索引，OHLC 從 [1] 開始
          const open = data[1] ?? 0
          const close = data[2] ?? 0
          const low = data[3] ?? 0
          const high = data[4] ?? 0
          return `
            <b>${name}</b><br/>
            開盤：${open.toFixed(2)}<br/>
            收盤：${close.toFixed(2)}<br/>
            最低：${low.toFixed(2)}<br/>
            最高：${high.toFixed(2)}
          `
        },
      },
      series: [
        {
          type: 'candlestick',
          data: ohlc,
          itemStyle: {
            color: '#26a69a',
            color0: '#ef5350',
            borderColor: '#26a69a',
            borderColor0: '#ef5350',
          },
        },
      ],
    }
  }

  // 折線圖
  const prices = history.map((p) => p.close)
  return {
    ...shared,
    tooltip: {
      trigger: 'axis' as const,
      ...tooltipStyle,
      formatter: undefined,
    },
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

const fetchData = async () => {
  loading.value = true
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
}

onMounted(fetchData)
</script>

<template>
  <div>
    <div class="d-flex align-items-center mb-3">
      <h5 class="text-dark mb-0">市場概覽</h5>
      <button
        class="btn btn-sm btn-outline-secondary ms-2"
        :disabled="loading"
        @click="fetchData"
        title="重新載入"
      >
        <i class="bi bi-arrow-clockwise" :class="{ 'spin': loading }" />
      </button>
    </div>

    <LoadingOverlay :visible="loading" text="正在取得市場資料..." />

    <!-- 指數卡片 -->
    <div v-if="!loading && indices.length === 0" class="text-secondary">
      無法取得市場資料，請確認後端是否已啟動。
    </div>
    <div v-else class="row g-3 mb-4">
      <div v-for="q in indices" :key="q.symbol" class="col-6 col-md-3">
        <IndexCard
          :quote="q"
          :active="selectedSymbol === q.symbol"
          @select="selectIndex"
        />
      </div>
    </div>

    <!-- 走勢圖 -->
    <div v-if="historyData" class="chart-container rounded-3 p-3">
      <div class="d-flex justify-content-between align-items-center mb-2">
        <span class="text-white fw-semibold">{{ historyData.name }} 走勢（近 3 個月）</span>
        <div class="btn-group btn-group-sm">
          <button
            class="btn"
            :class="chartType === 'line' ? 'btn-primary' : 'btn-outline-secondary'"
            @click="chartType = 'line'"
          >
            折線圖
          </button>
          <button
            class="btn"
            :class="chartType === 'candlestick' ? 'btn-primary' : 'btn-outline-secondary'"
            @click="chartType = 'candlestick'"
          >
            K 線圖
          </button>
        </div>
      </div>
      <LoadingOverlay :visible="chartLoading" text="載入圖表中..." />
      <v-chart v-if="!chartLoading" :option="chartOption" style="height: 350px" autoresize />
    </div>
  </div>
</template>

<style scoped>
.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.chart-container {
  background-color: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
}
</style>
