import axios from 'axios'
import { ElMessage } from 'element-plus'

const service = axios.create({
  baseURL: 'http://localhost:14011',
  timeout: 5000
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 可以在这里添加token等认证信息
    return config
  },
  error => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    const res = response.data
    
    // 这里可以根据后端的响应格式统一处理
    if (res.code && res.code !== 200) {
      ElMessage.error(res.message || '请求失败')
      return Promise.reject(new Error(res.message || '请求失败'))
    }
    
    return res
  },
  error => {
    console.error('Response error:', error)
    ElMessage.error(error.message || '请求失败')
    return Promise.reject(error)
  }
)

export const request = {
  get(url, params) {
    return service.get(url, { params })
  },
  
  post(url, data) {
    return service.post(url, data)
  },
  
  put(url, data) {
    return service.put(url, data)
  },
  
  delete(url) {
    return service.delete(url)
  }
} 