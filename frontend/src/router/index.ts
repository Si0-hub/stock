import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/heatmap',
      name: 'heatmap',
      component: () => import('../views/HeatmapView.vue'),
    },
    { path: '/stock', name: 'stock', component: () => import('../views/StockView.vue') },
    {
      path: '/stock/:symbol',
      name: 'stock-detail',
      component: () => import('../views/StockView.vue'),
    },
  ],
})

export default router
