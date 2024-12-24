import { useDark, useToggle } from '@vueuse/core'

export const isDark = useDark()
export const toggleDark = useToggle(isDark)

export const themes = {
  light: {
    '--el-bg-color': '#ffffff',
    '--el-bg-color-page': '#f2f3f5',
    '--el-text-color-primary': '#303133',
    '--el-text-color-regular': '#606266',
    '--el-border-color': '#dcdfe6'
  },
  dark: {
    '--el-bg-color': '#141414',
    '--el-bg-color-page': '#0a0a0a',
    '--el-text-color-primary': '#ffffff',
    '--el-text-color-regular': '#d0d0d0',
    '--el-border-color': '#434343'
  }
}

export function applyTheme(theme) {
  const root = document.documentElement
  const vars = themes[theme]
  
  Object.entries(vars).forEach(([key, value]) => {
    root.style.setProperty(key, value)
  })
} 