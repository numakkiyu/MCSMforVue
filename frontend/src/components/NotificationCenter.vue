<template>
  <div class="notification-center">
    <TransitionGroup 
      name="notification"
      tag="div"
      @enter="onEnter"
      @leave="onLeave"
    >
      <div
        v-for="notification in notifications"
        :key="notification.id"
        class="notification-item"
        :class="notification.type"
      >
        <el-icon class="notification-icon">
          <component :is="getIcon(notification.type)" />
        </el-icon>
        <div class="notification-content">
          <h4>{{ notification.title }}</h4>
          <p>{{ notification.message }}</p>
        </div>
        <el-button
          circle
          link
          @click="removeNotification(notification.id)"
        >
          <el-icon><Close /></el-icon>
        </el-button>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { gsap } from 'gsap'
import {
  SuccessFilled,
  WarningFilled,
  CircleCloseFilled,
  InfoFilled,
  Close
} from '@element-plus/icons-vue'

const notifications = ref([])
let notificationId = 0

const getIcon = (type) => {
  const icons = {
    success: SuccessFilled,
    warning: WarningFilled,
    error: CircleCloseFilled,
    info: InfoFilled
  }
  return icons[type]
}

const addNotification = (notification) => {
  const id = notificationId++
  notifications.value.push({
    id,
    ...notification,
    type: notification.type || 'info'
  })

  // 自动移除
  setTimeout(() => {
    removeNotification(id)
  }, notification.duration || 4500)
}

const removeNotification = (id) => {
  const index = notifications.value.findIndex(n => n.id === id)
  if (index !== -1) {
    notifications.value.splice(index, 1)
  }
}

const onEnter = (el, done) => {
  gsap.from(el, {
    opacity: 0,
    x: 100,
    duration: 0.3,
    onComplete: done
  })
}

const onLeave = (el, done) => {
  gsap.to(el, {
    opacity: 0,
    x: 100,
    duration: 0.3,
    onComplete: done
  })
}

// 导出方法供其他组件使用
defineExpose({
  addNotification
})
</script>

<style scoped>
.notification-center {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  width: 320px;
}

.notification-item {
  background: var(--el-bg-color);
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 10px;
  display: flex;
  align-items: flex-start;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.notification-icon {
  font-size: 20px;
  margin-right: 12px;
}

.notification-content {
  flex: 1;
}

.notification-content h4 {
  margin: 0 0 4px;
  font-size: 14px;
}

.notification-content p {
  margin: 0;
  font-size: 12px;
  color: var(--el-text-color-regular);
}

.success .notification-icon { color: var(--el-color-success); }
.warning .notification-icon { color: var(--el-color-warning); }
.error .notification-icon { color: var(--el-color-danger); }
.info .notification-icon { color: var(--el-color-info); }
</style> 