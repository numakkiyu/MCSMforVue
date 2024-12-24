<template>
  <div class="theme-editor">
    <el-card class="editor-card">
      <template #header>
        <div class="card-header">
          <h3>主题编辑器</h3>
          <div class="header-actions">
            <el-button-group>
              <el-button
                type="primary"
                @click="saveTheme"
              >
                保存主题
              </el-button>
              <el-button
                @click="resetTheme"
              >
                重置
              </el-button>
            </el-button-group>
          </div>
        </div>
      </template>

      <div class="theme-sections">
        <!-- 颜色部分 -->
        <div class="theme-section">
          <h4>颜色</h4>
          <div class="color-grid">
            <div
              v-for="(color, key) in themeColors"
              :key="key"
              class="color-item"
            >
              <span class="color-label">{{ colorLabels[key] }}</span>
              <el-color-picker
                v-model="themeColors[key]"
                show-alpha
                @change="updateTheme"
              />
              <span class="color-value">{{ themeColors[key] }}</span>
            </div>
          </div>
        </div>

        <!-- 字体部分 -->
        <div class="theme-section">
          <h4>字体</h4>
          <div class="font-settings">
            <el-form :model="themeFonts" label-width="100px">
              <el-form-item label="主要字体">
                <el-select v-model="themeFonts.primary">
                  <el-option
                    v-for="font in fontOptions"
                    :key="font.value"
                    :label="font.label"
                    :value="font.value"
                  />
                </el-select>
              </el-form-item>
              <el-form-item label="字体大小">
                <el-input-number
                  v-model="themeFonts.size"
                  :min="12"
                  :max="20"
                  @change="updateTheme"
                />
              </el-form-item>
            </el-form>
          </div>
        </div>

        <!-- 圆角部分 -->
        <div class="theme-section">
          <h4>圆角</h4>
          <div class="radius-settings">
            <el-slider
              v-model="themeRadius"
              :min="0"
              :max="20"
              @change="updateTheme"
            />
          </div>
        </div>

        <!-- 预览部分 -->
        <div class="theme-preview">
          <h4>预览</h4>
          <div class="preview-content">
            <div class="preview-card">
              <h5>示例卡片</h5>
              <p>这是一段示例文本，用于预览主题效果。</p>
              <el-button type="primary">主要按钮</el-button>
              <el-button type="success">成功按钮</el-button>
              <el-button type="warning">警告按钮</el-button>
              <el-button type="danger">危险按钮</el-button>
            </div>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useThemeStore } from '../stores/theme'
import { ElMessage } from 'element-plus'

const themeStore = useThemeStore()

const colorLabels = {
  primary: '主要颜色',
  success: '成功颜色',
  warning: '警告颜色',
  danger: '危险颜色',
  info: '信息颜色',
  background: '背景颜色',
  text: '文字颜色'
}

const themeColors = reactive({
  primary: '#409EFF',
  success: '#67C23A',
  warning: '#E6A23C',
  danger: '#F56C6C',
  info: '#909399',
  background: '#FFFFFF',
  text: '#303133'
})

const themeFonts = reactive({
  primary: 'Arial',
  size: 14
})

const themeRadius = ref(4)

const fontOptions = [
  { label: 'Arial', value: 'Arial' },
  { label: 'Helvetica', value: 'Helvetica' },
  { label: 'Times New Roman', value: 'Times New Roman' }
]

const updateTheme = () => {
  const theme = {
    colors: themeColors,
    fonts: themeFonts,
    radius: themeRadius.value
  }
  themeStore.updateTheme(theme)
}

const saveTheme = async () => {
  try {
    await themeStore.saveTheme({
      colors: themeColors,
      fonts: themeFonts,
      radius: themeRadius.value
    })
    ElMessage.success('主题保存成功')
  } catch (error) {
    ElMessage.error('主题保存失败')
  }
}

const resetTheme = () => {
  Object.assign(themeColors, themeStore.defaultTheme.colors)
  Object.assign(themeFonts, themeStore.defaultTheme.fonts)
  themeRadius.value = themeStore.defaultTheme.radius
  updateTheme()
}
</script>

<style scoped>
.theme-editor {
  padding: 20px;
}

.theme-sections {
  display: grid;
  gap: 30px;
}

.color-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.color-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.color-label {
  min-width: 80px;
}

.color-value {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.preview-content {
  margin-top: 20px;
  padding: 20px;
  border-radius: var(--el-border-radius-base);
  background: var(--el-bg-color-overlay);
}

.preview-card {
  padding: 20px;
  border-radius: var(--el-border-radius-base);
  background: var(--el-bg-color);
  box-shadow: var(--el-box-shadow-light);
}
</style> 