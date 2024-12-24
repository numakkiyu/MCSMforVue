import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { request } from '../utils/request'

export const useMappingStore = defineStore('mapping', () => {
  // 状态
  const mappings = ref([])
  const loading = ref(false)
  const error = ref(null)

  // 计算属性
  const runningMappings = computed(() => 
    mappings.value.filter(m => m.status === 'running')
  )

  const stoppedMappings = computed(() => 
    mappings.value.filter(m => m.status === 'stopped')
  )

  // Actions
  async function fetchMappings() {
    try {
      loading.value = true
      const data = await request.get('/api/mappings')
      mappings.value = data
    } catch (err) {
      error.value = err.message
      ElMessage.error('获取映射列表失败')
    } finally {
      loading.value = false
    }
  }

  async function addMapping(mapping) {
    try {
      loading.value = true
      await request.post('/api/mappings', mapping)
      await fetchMappings()
      ElMessage.success('添加映射成功')
    } catch (err) {
      error.value = err.message
      ElMessage.error('添加映射失败')
    } finally {
      loading.value = false
    }
  }

  async function deleteMapping(name) {
    try {
      loading.value = true
      await request.delete(`/api/mappings/${name}`)
      await fetchMappings()
      ElMessage.success('删除映射成功')
    } catch (err) {
      error.value = err.message
      ElMessage.error('删除映射失败')
    } finally {
      loading.value = false
    }
  }

  async function toggleMapping(name) {
    try {
      loading.value = true
      await request.post(`/api/mappings/${name}/toggle`)
      await fetchMappings()
      ElMessage.success('操作成功')
    } catch (err) {
      error.value = err.message
      ElMessage.error('操作失败')
    } finally {
      loading.value = false
    }
  }

  return {
    mappings,
    loading,
    error,
    runningMappings,
    stoppedMappings,
    fetchMappings,
    addMapping,
    deleteMapping,
    toggleMapping
  }
}) 