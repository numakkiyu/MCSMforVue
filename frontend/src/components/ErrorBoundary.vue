<template>
  <div v-if="error" class="error-container">
    <el-result
      icon="error"
      :title="error.message"
      sub-title="发生了一些错误"
    >
      <template #extra>
        <el-button type="primary" @click="handleRetry">
          重试
        </el-button>
      </template>
    </el-result>
  </div>
  <slot v-else></slot>
</template>

<script>
import { ref, onErrorCaptured } from 'vue'

export default {
  name: 'ErrorBoundary',
  setup() {
    const error = ref(null)

    onErrorCaptured((err) => {
      error.value = err
      return false // 阻止错误继续传播
    })

    const handleRetry = () => {
      error.value = null
      // 可以在这里添加重试逻辑
    }

    return {
      error,
      handleRetry
    }
  }
}
</script>

<style scoped>
.error-container {
  padding: 40px;
  text-align: center;
}
</style> 