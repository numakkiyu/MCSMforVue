import { saveAs } from 'file-saver'
import { ElMessage } from 'element-plus'

export async function exportData(data, filename) {
  try {
    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: 'application/json'
    })
    saveAs(blob, filename)
    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error('导出失败')
    console.error('Export error:', error)
  }
}

export function importData(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    
    reader.onload = (e) => {
      try {
        const data = JSON.parse(e.target.result)
        resolve(data)
      } catch (error) {
        reject(new Error('文件格式错误'))
      }
    }
    
    reader.onerror = () => reject(new Error('读取文件失败'))
    reader.readAsText(file)
  })
}

// 数据验证
export function validateMappingData(data) {
  if (!Array.isArray(data)) return false
  
  return data.every(item => {
    return (
      typeof item.name === 'string' &&
      typeof item.address === 'string' &&
      (!item.port || typeof item.port === 'number')
    )
  })
} 