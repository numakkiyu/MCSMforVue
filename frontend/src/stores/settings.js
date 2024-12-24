import { defineStore } from 'pinia'
import { ref } from 'vue'
import { request } from '../utils/request'
import { ElMessage } from 'element-plus'

export const useSettingsStore = defineStore('settings', () => {
  const settings = ref({
    theme: 'dark',
    dataPath: '',
    autoStart: false,
    runInBackground: true,
    autoUpdate: true
  })

  const loading = ref(false)

  async function fetchSettings() {
    try {
      loading.value = true
      const data = await request.get('/api/settings')
      settings.value = data
    } catch (err) {
      ElMessage.error('获取设置失败')
    } finally {
      loading.value = false
    }
  }

  async function updateSettings(newSettings) {
    try {
      loading.value = true
      await request.post('/api/settings', newSettings)
      settings.value = newSettings
      ElMessage.success('设置已更新')
    } catch (err) {
      ElMessage.error('更新设置失败')
    } finally {
      loading.value = false
    }
  }

  return {
    settings,
    loading,
    fetchSettings,
    updateSettings
  }
}) 