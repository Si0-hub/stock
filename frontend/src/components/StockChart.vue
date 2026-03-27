<script setup lang="ts">
import { ref, computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { LineChart, CandlestickChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, DataZoomComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import type { IndexHistory } from '../services/api'
import LoadingOverlay from './LoadingOverlay.vue'

use([LineChart, CandlestickChart, GridComponent, TooltipComponent, DataZoomComponent, CanvasRenderer])

const props = defineProps<{
  history: IndexHistory | null
  loading: boolean
}>()

const emit = defineEmits<{ 'period-change': [period: string] }>()

const chartType = ref<'line' | 'candlestick'>('line')
const period = ref('3mo')

const periodOptions = [
  { value: '1mo', label: '1 個月' },
  { value: '3mo', label: '3 個月' },
  { value: '6mo', label: '6 個月' },
  { value: '1y', label: '1 年' },
]

function changePeriod(p: string) {
  period.value = p
  emit('period-change', p)
}

const chartOption = computed(() => {
  if (!props.history) return {}
  const history = props.history.history
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
</script>

<template>
  <div class="chart-container rounded-3 p-3">
    <div class="d-flex justify-content-between align-items-center mb-2 flex-wrap gap-2">
      <span class="text-white fw-semibold">{{ history?.name ?? '' }} 走勢</span>
      <div class="d-flex gap-2">
        <!-- 時間週期切換 -->
        <div class="btn-group btn-group-sm">
          <button
            v-for="opt in periodOptions"
            :key="opt.value"
            class="btn"
            :class="period === opt.value ? 'btn-primary' : 'btn-outline-secondary'"
            @click="changePeriod(opt.value)"
          >
            {{ opt.label }}
          </button>
        </div>
        <!-- 圖表類型切換 -->
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
    </div>
    <LoadingOverlay :visible="loading" text="載入圖表中..." />
    <v-chart v-if="!loading && history" :option="chartOption" style="height: 350px" autoresize />
    <div v-else-if="!loading" class="text-secondary text-center py-5">無圖表資料</div>
  </div>
</template>

<style scoped>
.chart-container {
  background-color: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
}
</style>
