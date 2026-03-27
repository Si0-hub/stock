<script setup lang="ts">
import { ref } from 'vue'

defineProps<{ loading: boolean }>()
const emit = defineEmits<{ search: [query: string] }>()

const query = ref('')

function submit() {
  if (query.value.trim()) emit('search', query.value.trim())
}
</script>

<template>
  <div class="input-group" style="max-width: 600px; margin: 0 auto">
    <span class="input-group-text">
      <span v-if="loading" class="spinner-border spinner-border-sm" role="status" />
      <i v-else class="bi bi-search" />
    </span>
    <input
      v-model="query"
      type="text"
      class="form-control"
      placeholder="輸入股票代碼或公司名稱..."
      @keyup.enter="submit"
    />
    <button class="btn btn-primary" @click="submit">搜尋</button>
  </div>
</template>
