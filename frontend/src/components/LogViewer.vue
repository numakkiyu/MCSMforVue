<template>
  <div class="log-viewer">
    <div class="log-header">
      <h3>日志查看器</h3>
      <div class="log-controls">
        <el-select v-model="logLevel" placeholder="日志级别">
          <el-option
            v-for="level in logLevels"
            :key="level.value"
            :label="level.label"
            :value="level.value"
          />
        </el-select>
        <el-input
          v-model="searchQuery"
          placeholder="搜索日志..."
          clearable
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-button type="primary" @click="refreshLogs">
          刷新
        </el-button>
        <el-button @click="clearLogs">
          清空
        </el-button>
      </div>
    </div>

    <div class="log-content" ref="logContainer">
      <div
        v-for="(log, index) in filteredLogs"
        :key="index"
        class="log-entry"
        :class="log.level.toLowerCase()"
      >
        <span class="log-time">{{ formatTime(log.timestamp) }}</span>
        <span class="log-level">{{ log.level }}</span>
        <span class="log-message">{{ log.message }}</span>
      </div>

      <div v-if="loading" class="loading-overlay">
        <el-icon class="is-loading"><Loading /></el-icon>
      </div>
    </div>

    <div class="log-footer">
      <el-switch
        v-model="autoScroll"
        active-text="自动滚动"
      />
      <el-pagination
        :current-page="currentPage"
        :page-size="pageSize"
        :total="totalLogs"
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { Search, Loading } from '@element-plus/icons-vue'
import { request } from '../utils/request'
import { formatDateTime } from '../utils/date'

const logs = ref([])
const loading = ref(false)
const logLevel = ref('all')
const searchQuery = ref('')
const autoScroll = ref(true)
const currentPage = ref(1)
const pageSize = ref(50)
const totalLogs = ref(0)
const logContainer = ref(null)

const logLevels = [
  { label: '全部', value: 'all' },
  { label: '信息', value: 'info' },
  { label: '警告', value: 'warning' },
  { label: '错误', value: 'error' },
  { label: '调试', value: 'debug' }
]

const filteredLogs = computed(() => {
  let filtered = logs.value

  if (logLevel.value !== 'all') {
    filtered = filtered.filter(log => log.level.toLowerCase() === logLevel.value)
  }

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(log => 
      log.message.toLowerCase().includes(query)
    )
  }

  return filtered
})

const fetchLogs = async () => {
  try {
    loading.value = true
    const response = await request.get('/api/logs', {
      page: currentPage.value,
      pageSize: pageSize.value
    })
    logs.value = response.data
    totalLogs.value = response.total
  } catch (error) {
    console.error('获取日志失败:', error)
  } finally {
    loading.value = false
  }
}

const refreshLogs = () => {
  fetchLogs()
}

const clearLogs = async () => {
  try {
    await request.delete('/api/logs')
    logs.value = []
    totalLogs.value = 0
  } catch (error) {
    console.error('清空日志失败:', error)
  }
}

const handlePageChange = (page) => {
  currentPage.value = page
  fetchLogs()
}

const formatTime = (timestamp) => {
  return formatDateTime(timestamp)
}

// 自动滚动到底部
watch(filteredLogs, () => {
  if (autoScroll.value && logContainer.value) {
    setTimeout(() => {
      logContainer.value.scrollTop = logContainer.value.scrollHeight
    }, 0)
  }
})

onMounted(() => {
  fetchLogs()
})
</script>

<style scoped>
.log-viewer {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.log-header {
  padding: 16px;
  border-bottom: 1px solid var(--el-border-color);
}

.log-controls {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.log-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  position: relative;
}

.log-entry {
  font-family: monospace;
  padding: 4px 8px;
  border-radius: 4px;
  margin-bottom: 4px;
}

.log-time {
  color: var(--el-text-color-secondary);
  margin-right: 10px;
}

.log-level {
  display: inline-block;
  min-width: 60px;
  margin-right: 10px;
  font-weight: bold;
}

.log-entry.info { background-color: rgba(var(--el-color-info-rgb), 0.1); }
.log-entry.warning { background-color: rgba(var(--el-color-warning-rgb), 0.1); }
.log-entry.error { background-color: rgba(var(--el-color-danger-rgb), 0.1); }
.log-entry.debug { background-color: rgba(var(--el-color-success-rgb), 0.1); }

.log-footer {
  padding: 16px;
  border-top: 1px solid var(--el-border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
}
</style> 