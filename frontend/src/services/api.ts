import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
})

export interface IndexQuote {
  symbol: string
  name: string
  price: number | null
  change: number | null
  changePercent: number | null
}

export interface HistoryPoint {
  date: string
  open: number
  high: number
  low: number
  close: number
  volume: number
}

export interface IndexHistory {
  symbol: string
  name: string
  history: HistoryPoint[]
}

export async function getMarketIndices(): Promise<IndexQuote[]> {
  const { data } = await api.get<IndexQuote[]>('/market/indices')
  return data
}

export async function getIndexHistory(
  symbol: string,
  period: string = '3mo',
): Promise<IndexHistory> {
  const { data } = await api.get<IndexHistory>(
    `/market/indices/${encodeURIComponent(symbol)}/history`,
    { params: { period } },
  )
  return data
}

// ---- 熱力圖 ----

export interface HeatmapStock {
  ticker: string
  name: string
  marketCap: number
  changePercent: number
  price: number
}

export interface HeatmapSector {
  name: string
  children: HeatmapStock[]
}

export async function getHeatmapData(): Promise<HeatmapSector[]> {
  const { data } = await api.get<HeatmapSector[]>('/market/heatmap')
  return data
}

// ---- 股票查詢 ----

export interface StockSearchResult {
  symbol: string
  name: string
  price: number | null
  change: number | null
  changePercent: number | null
  volume: number | null
  marketCap: number | null
}

export interface StockQuote {
  symbol: string
  name: string
  price: number | null
  change: number | null
  changePercent: number | null
  volume: number | null
  marketCap: number | null
  dayHigh: number | null
  dayLow: number | null
  fiftyTwoWeekHigh: number | null
  fiftyTwoWeekLow: number | null
}

export async function searchStocks(q: string, limit = 10): Promise<StockSearchResult[]> {
  const { data } = await api.get<StockSearchResult[]>('/market/search', { params: { q, limit } })
  return data
}

export async function getStockQuote(symbol: string): Promise<StockQuote> {
  const { data } = await api.get<StockQuote>(`/market/stocks/${encodeURIComponent(symbol)}`)
  return data
}

export async function getStockHistory(symbol: string, period = '3mo'): Promise<IndexHistory> {
  const { data } = await api.get<IndexHistory>(
    `/market/stocks/${encodeURIComponent(symbol)}/history`,
    { params: { period } },
  )
  return data
}
