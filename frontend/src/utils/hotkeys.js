import { onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const defaultHotkeys = {
  'ctrl+h': '/',           // 主页
  'ctrl+m': '/mappings',   // 映射管理
  'ctrl+s': '/settings',   // 设置
  'ctrl+l': '/logs',       // 日志
  'ctrl+r': 'refresh',     // 刷新
  'ctrl+n': 'new',         // 新建映射
  'esc': 'close'           // 关闭弹窗
}

export function useHotkeys(customHotkeys = {}) {
  const router = useRouter()
  const hotkeys = { ...defaultHotkeys, ...customHotkeys }
  
  const handleKeydown = (event) => {
    const key = getKeyCombo(event)
    const action = hotkeys[key]
    
    if (!action) return
    
    event.preventDefault()
    
    if (action.startsWith('/')) {
      router.push(action)
    } else {
      // 触发自定义动作
      switch (action) {
        case 'refresh':
          window.location.reload()
          break
        case 'new':
          // 触发新建映射事件
          break
        case 'close':
          // 触发关闭弹窗事件
          break
      }
    }
  }
  
  const getKeyCombo = (event) => {
    const combo = []
    if (event.ctrlKey) combo.push('ctrl')
    if (event.altKey) combo.push('alt')
    if (event.shiftKey) combo.push('shift')
    combo.push(event.key.toLowerCase())
    return combo.join('+')
  }
  
  onMounted(() => {
    document.addEventListener('keydown', handleKeydown)
  })
  
  onUnmounted(() => {
    document.removeEventListener('keydown', handleKeydown)
  })
} 