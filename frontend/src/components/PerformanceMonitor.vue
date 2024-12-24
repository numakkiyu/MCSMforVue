<template>
  <div class="performance-monitor">
    <el-card class="monitor-card">
      <template #header>
        <div class="card-header">
          <h3>性能监控</h3>
          <el-switch v-model="realtime" active-text="实时监控" />
        </div>
      </template>

      <div class="metrics-grid">
        <!-- CPU使用率 -->
        <div class="metric-card">
          <h4>CPU 使用率</h4>
          <GaugeChart
            :value="metrics.cpu"
            :color="getCpuColor"
            unit="%"
          />
          <div class="metric-details">
            <div class="detail-item">
              <span>核心数</span>
              <span>{{ metrics.cpuCores }}</span>
            </div>
            <div class="detail-item">
              <span>平均负载</span>
              <span>{{ metrics.cpuLoad.toFixed(2) }}</span>
            </div>
          </div>
        </div>

        <!-- 内存使用 -->
        <div class="metric-card">
          <h4>内存使用</h4>
          <ProgressChart
            :value="metrics.memoryUsed"
            :total="metrics.memoryTotal"
            unit="MB"
          />
          <div class="metric-details">
            <div class="detail-item">
              <span>总内存</span>
              <span>{{ formatSize(metrics.memoryTotal) }}</span>
            </div>
            <div class="detail-item">
              <span>可用内存</span>
              <span>{{ formatSize(metrics.memoryAvailable) }}</span>
            </div>
          </div>
        </div>

        <!-- 网络流量 -->
        <div class="metric-card">
          <h4>网络流量</h4>
          <LineChart
            :data="networkHistory"
            :options="networkChartOptions"
          />
          <div class="metric-details">
            <div class="detail-item">
              <span>上传速度</span>
              <span>{{ formatSpeed(metrics.networkUp) }}</span>
            </div>
            <div class="detail-item">
              <span>下载速度</span>
              <span>{{ formatSpeed(metrics.networkDown) }}</span>
            </div>
          </div>
        </div>

        <!-- 磁盘使用 -->
        <div class="metric-card">
          <h4>磁盘使用</h4>
          <PieChart
            :data="diskUsageData"
            :options="diskChartOptions"
          />
          <div class="metric-details">
            <div class="detail-item">
              <span>读取速度</span>
              <span>{{ formatSpeed(metrics.diskRead) }}</span>
            </div>
            <div class="detail-item">
              <span>写入速度</span>
              <span>{{ formatSpeed(metrics.diskWrite) }}</span>
            </div>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { usePerformanceStore } from '../stores/performance'
import GaugeChart from './charts/GaugeChart.vue'
import ProgressChart from './charts/ProgressChart.vue'
import LineChart from './charts/LineChart.vue'
import PieChart from './charts/PieChart.vue'
import { formatSize, formatSpeed } from '../utils/format'

const performanceStore = usePerformanceStore()
const realtime = ref(true)
const updateInterval = ref(null)

const metrics = computed(() => performanceStore.metrics)
const networkHistory = computed(() => performanceStore.networkHistory)

// CPU颜色计算
const getCpuColor = computed(() => {
  const cpu = metrics.value.cpu
  if (cpu < 60) return '#67C23A'
  if (cpu < 80) return '#E6A23C'
  return '#F56C6C'
})

// 磁盘使用数据
const diskUsageData = computed(() => [
  { name: '已使用', value: metrics.value.diskUsed, color: '#409EFF' },
  { name: '可用', value: metrics.value.diskTotal - metrics.value.diskUsed, color: '#67C23A' }
])

// 图表配置
const networkChartOptions = {
  xAxis: { show: false },
  yAxis: { show: false },
  smooth: true,
  area: true
}

const diskChartOptions = {
  legend: { show: true },
  label: { show: true }
}

// 实时更新
watch(realtime, (value) => {
  if (value) {
    startRealtimeUpdate()
  } else {
    stopRealtimeUpdate()
  }
})

const startRealtimeUpdate = () => {
  updateInterval.value = setInterval(() => {
    performanceStore.fetchMetrics()
  }, 2000)
}

const stopRealtimeUpdate = () => {
  if (updateInterval.value) {
    clearInterval(updateInterval.value)
    updateInterval.value = null
  }
}

onMounted(() => {
  performanceStore.fetchMetrics()
  if (realtime.value) {
    startRealtimeUpdate()
  }
})

onUnmounted(() => {
  stopRealtimeUpdate()
})
</script>

<style scoped>
.performance-monitor {
  padding: 20px;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.metric-card {
  background: var(--el-bg-color-overlay);
  border-radius: 8px;
  padding: 15px;
  transition: transform 0.3s;
}

.metric-card:hover {
  transform: translateY(-2px);
}

.metric-details {
  margin-top: 15px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  margin: 5px 0;
  font-size: 14px;
}

.detail-item span:first-child {
  color: var(--el-text-color-secondary);
}
</style> 