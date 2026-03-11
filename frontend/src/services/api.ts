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
