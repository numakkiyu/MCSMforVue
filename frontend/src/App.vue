<template>
  <div class="app-container">
    <title-bar />
    <div class="content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import TitleBar from './components/TitleBar.vue'

export default {
  name: 'App',
  components: {
    TitleBar
  }
}
</script>

<style>
.app-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--el-bg-color);
}

.content {
  flex: 1;
  overflow: auto;
  padding: 20px;
}
</style> 