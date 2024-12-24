<template>
  <div class="home">
    <server-monitor />
  </div>
</template>

<script>
import ServerMonitor from '@/components/ServerMonitor.vue'

export default {
  name: 'Home',
  components: {
    ServerMonitor
  }
}
</script>

<style scoped>
.home {
  padding: 20px;
}
</style> 