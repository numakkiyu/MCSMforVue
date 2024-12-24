<template>
  <div class="settings-container">
    <h1>设置</h1>
    
    <el-card class="setting-section">
      <template #header>
        <h3>外观</h3>
      </template>
      <el-form label-position="left">
        <el-form-item label="主题">
          <el-switch
            v-model="settings.darkMode"
            active-text="深色"
            inactive-text="浅色"
          />
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="setting-section">
      <template #header>
        <h3>数据</h3>
      </template>
      <el-form label-position="left">
        <el-form-item label="数据存储位置">
          <el-input v-model="settings.dataPath">
            <template #append>
              <el-button @click="selectPath">选择</el-button>
            </template>
          </el-input>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="setting-section">
      <template #header>
        <h3>启动选项</h3>
      </template>
      <el-form label-position="left">
        <el-form-item label="开机自启">
          <el-switch v-model="settings.autoStart" />
        </el-form-item>
        <el-form-item label="后台运行">
          <el-switch v-model="settings.runInBackground" />
        </el-form-item>
        <el-form-item label="自动更新">
          <el-switch v-model="settings.autoUpdate" />
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'Settings',
  setup() {
    const settings = ref({
      darkMode: true,
      dataPath: '',
      autoStart: false,
      runInBackground: true,
      autoUpdate: true
    })

    onMounted(async () => {
      // 获取设置
      const response = await fetch('http://localhost:14011/api/settings')
      const data = await response.json()
      settings.value = { ...settings.value, ...data }
    })

    const saveSettings = async () => {
      // 保存设置
    }

    return {
      settings,
      saveSettings
    }
  }
}
</script>

<style scoped>
.settings-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.setting-section {
  margin-bottom: 20px;
}
</style> 