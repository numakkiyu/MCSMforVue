<template>
  <el-menu
    :default-active="activeRoute"
    class="app-nav"
    mode="vertical"
    :collapse="isCollapse"
    @select="handleSelect"
    :router="true"
  >
    <div class="logo-container">
      <img src="../assets/logo.png" alt="Logo" class="logo">
      <span v-show="!isCollapse">MC映射工具</span>
    </div>

    <el-menu-item index="/">
      <el-icon><HomeFilled /></el-icon>
      <template #title>主页</template>
    </el-menu-item>

    <el-menu-item index="/mappings">
      <el-icon><Connection /></el-icon>
      <template #title>映射管理</template>
    </el-menu-item>

    <el-menu-item index="/settings">
      <el-icon><Setting /></el-icon>
      <template #title>设置</template>
    </el-menu-item>

    <el-menu-item index="/about">
      <el-icon><InfoFilled /></el-icon>
      <template #title>关于</template>
    </el-menu-item>

    <div class="nav-footer" v-show="!isCollapse">
      <el-button 
        type="text" 
        class="collapse-btn"
        @click="toggleCollapse"
      >
        <el-icon>
          <component :is="isCollapse ? 'Expand' : 'Fold'" />
        </el-icon>
      </el-button>
    </div>
  </el-menu>
</template>

<script>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import {
  HomeFilled,
  Connection,
  Setting,
  InfoFilled,
  Expand,
  Fold
} from '@element-plus/icons-vue'

export default {
  name: 'AppNav',
  components: {
    HomeFilled,
    Connection,
    Setting,
    InfoFilled,
    Expand,
    Fold
  },
  setup() {
    const route = useRoute()
    const isCollapse = ref(false)

    const activeRoute = computed(() => route.path)

    const toggleCollapse = () => {
      isCollapse.value = !isCollapse.value
    }

    return {
      isCollapse,
      activeRoute,
      toggleCollapse
    }
  }
}
</script>

<style scoped>
.app-nav {
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  border-right: solid 1px var(--el-border-color);
}

.logo-container {
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo {
  width: 32px;
  height: 32px;
}

.nav-footer {
  position: absolute;
  bottom: 20px;
  width: 100%;
  text-align: center;
}

.collapse-btn {
  padding: 12px;
}
</style> 