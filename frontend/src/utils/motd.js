const colorCodes = {
  '0': '#000000', // 黑色
  '1': '#0000AA', // 深蓝色
  '2': '#00AA00', // 深绿色
  '3': '#00AAAA', // 深青色
  '4': '#AA0000', // 深红色
  '5': '#AA00AA', // 深紫色
  '6': '#FFAA00', // 金色
  '7': '#AAAAAA', // 灰色
  '8': '#555555', // 深灰色
  '9': '#5555FF', // 蓝色
  'a': '#55FF55', // 绿色
  'b': '#55FFFF', // 青色
  'c': '#FF5555', // 红色
  'd': '#FF55FF', // 粉红色
  'e': '#FFFF55', // 黄色
  'f': '#FFFFFF'  // 白色
}

const formatCodes = {
  'l': 'font-weight: bold;',
  'm': 'text-decoration: line-through;',
  'n': 'text-decoration: underline;',
  'o': 'font-style: italic;'
}

export function formatMotd(motd) {
  if (!motd) return ''
  
  let formatted = motd
  let currentColor = ''
  let currentFormat = []
  
  // 处理颜色代码
  formatted = formatted.replace(/§([0-9a-fk-or])/g, (match, code) => {
    if (code === 'r') {
      currentColor = ''
      currentFormat = []
      return '</span>'
    }
    
    if (colorCodes[code]) {
      currentColor = colorCodes[code]
      return `<span style="color: ${currentColor}${currentFormat.join('')}">`
    }
    
    if (formatCodes[code]) {
      currentFormat.push(formatCodes[code])
      return `<span style="color: ${currentColor}${currentFormat.join('')}">`
    }
    
    return ''
  })
  
  // 处理换行
  formatted = formatted.replace(/\n/g, '<br>')
  
  return formatted
} 