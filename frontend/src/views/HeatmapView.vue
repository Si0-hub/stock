<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { TreemapChart } from 'echarts/charts'
import { TooltipComponent, VisualMapComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { getHeatmapData, type HeatmapSector } from '@/services/api'
import type { CallbackDataParams } from 'echarts/types/dist/shared'
import LoadingOverlay from '@/components/LoadingOverlay.vue'

interface TreemapNodeData {
  name: string
  fullName?: string
  price?: number
  changePercent?: number
  value?: number
}

use([TreemapChart, TooltipComponent, VisualMapComponent, CanvasRenderer])

const heatmapData = ref<HeatmapSector[] | null>(null)
const loading = ref(true)

// 漲跌幅 → 顏色：紅跌綠漲，中性深灰
function lerpColor(a: string, b: string, t: number): string {
  const parse = (hex: string) => [
    parseInt(hex.slice(1, 3), 16),
    parseInt(hex.slice(3, 5), 16),
    parseInt(hex.slice(5, 7), 16),
  ]
  const ca = parse(a)
  const cb = parse(b)
  const r = Math.round(ca[0]! + (cb[0]! - ca[0]!) * t)
  const g = Math.round(ca[1]! + (cb[1]! - ca[1]!) * t)
  const bl = Math.round(ca[2]! + (cb[2]! - ca[2]!) * t)
  return `rgb(${r},${g},${bl})`
}

function getChangeColor(pct: number): string {
  const clamped = Math.max(-5, Math.min(5, pct))
  const ratio = (clamped + 5) / 10 // 0=深紅, 0.5=中性, 1=深綠
  if (ratio < 0.5) {
    return lerpColor('#ef5350', '#2a2e39', ratio / 0.5)
  }
  return lerpColor('#2a2e39', '#26a69a', (ratio - 0.5) / 0.5)
}

function formatMarketCap(value: number): string {
  if (value >= 1e12) return (value / 1e12).toFixed(2) + 'T'
  if (value >= 1e9) return (value / 1e9).toFixed(1) + 'B'
  if (value >= 1e6) return (value / 1e6).toFixed(1) + 'M'
  return value.toString()
}

function buildTreemapData(sectors: HeatmapSector[]) {
  return sectors.map((sector) => ({
    name: sector.name,
    children: sector.children.map((stock) => ({
      name: stock.ticker,
      value: stock.marketCap,
      changePercent: stock.changePercent,
      fullName: stock.name,
      price: stock.price,
      itemStyle: {
        color: getChangeColor(stock.changePercent),
      },
    })),
  }))
}

const chartOption = computed(() => {
  if (!heatmapData.value) return {}
  return {
    tooltip: {
      backgroundColor: 'rgba(30,30,30,0.95)',
      borderColor: '#555',
      textStyle: { color: '#fff', fontSize: 13 },
      formatter: (params: CallbackDataParams) => {
        const d = params.data as TreemapNodeData
        if (d.changePercent === undefined) return `<b>${params.name}</b>`
        const sign = d.changePercent >= 0 ? '+' : ''
        const color = d.changePercent >= 0 ? '#26a69a' : '#ef5350'
        return `
          <b>${d.name}</b>（${d.fullName}）<br/>
          價格：<b>$${d.price}</b><br/>
          漲跌：<span style="color:${color}"><b>${sign}${d.changePercent.toFixed(2)}%</b></span><br/>
          市值：$${formatMarketCap(d.value ?? 0)}
        `
      },
    },
    series: [
      {
        type: 'treemap',
        width: '100%',
        height: '100%',
        roam: 'move',
        nodeClick: false,
        breadcrumb: { show: false },
        itemStyle: {
          gapWidth: 2,
          borderColor: '#1a1a2e',
        },
        upperLabel: {
          show: true,
          height: 26,
          color: '#fff',
          fontSize: 13,
          fontWeight: 'bold',
          backgroundColor: 'rgba(0,0,0,0.4)',
          padding: [4, 8],
        },
        label: {
          show: true,
          formatter: (params: CallbackDataParams) => {
            const d = params.data as TreemapNodeData
            if (d.changePercent === undefined) return params.name
            const sign = d.changePercent >= 0 ? '+' : ''
            return `{ticker|${d.name}}\n{pct|${sign}${d.changePercent.toFixed(2)}%}`
          },
          rich: {
            ticker: {
              fontSize: 14,
              fontWeight: 'bold',
              color: '#fff',
              lineHeight: 22,
            },
            pct: {
              fontSize: 11,
              color: 'rgba(255,255,255,0.85)',
              lineHeight: 16,
            },
          },
          align: 'center',
          verticalAlign: 'middle',
        },
        levels: [
          {
            itemStyle: {
              borderColor: '#1a1a2e',
              borderWidth: 3,
              gapWidth: 3,
            },
            upperLabel: { show: true },
          },
          {
            itemStyle: {
              borderColor: '#1a1a2e',
              borderWidth: 1,
              gapWidth: 1,
            },
            label: { show: true },
          },
        ],
        data: buildTreemapData(heatmapData.value),
      },
    ],
  }
})

const fetchData = async () => {
  loading.value = true
  try {
    heatmapData.value = await getHeatmapData()
  } catch {
    heatmapData.value = null
  } finally {
    loading.value = false
  }
}

onMounted(fetchData)
</script>

<template>
  <div class="heatmap-page">
    <div class="d-flex align-items-center mb-3">
      <h5 class="text-dark mb-0">市場熱力圖</h5>
      <button
        class="btn btn-sm btn-outline-secondary ms-2"
        :disabled="loading"
        @click="fetchData"
        title="重新載入"
      >
        <i class="bi bi-arrow-clockwise" :class="{ spin: loading }" />
      </button>
    </div>

    <LoadingOverlay :visible="loading" text="正在載入熱力圖..." />

    <div v-if="!loading && !heatmapData" class="text-secondary">
      無法取得熱力圖資料，請確認後端是否已啟動。
    </div>

    <div v-if="heatmapData" class="heatmap-container rounded-3">
      <v-chart :option="chartOption" class="heatmap-chart" autoresize />
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

.heatmap-container {
  background-color: #1a1a2e;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.heatmap-chart {
  height: calc(100vh - 160px);
  min-height: 500px;
}
</style>
