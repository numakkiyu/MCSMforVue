<template>
  <div class="title-bar">
    <div class="title">MC端口映射工具</div>
    <div class="controls">
      <button class="control-btn" @click="minimize">
        <i class="el-icon-minus"></i>
      </button>
      <button class="control-btn" @click="maximize">
        <i class="el-icon-full-screen"></i>
      </button>
      <button class="control-btn close" @click="close">
        <i class="el-icon-close"></i>
      </button>
    </div>
  </div>
</template>

<script>
const { ipcRenderer } = require('electron')

export default {
  name: 'TitleBar',
  methods: {
    minimize() {
      ipcRenderer.send('window-min')
    },
    maximize() {
      ipcRenderer.send('window-max')
    },
    close() {
      ipcRenderer.send('window-close')
    }
  }
}
</script>

<style scoped>
.title-bar {
  -webkit-app-region: drag;
  height: 32px;
  background: #2c3e50;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 10px;
  color: white;
}

.controls {
  -webkit-app-region: no-drag;
  display: flex;
}

.control-btn {
  -webkit-app-region: no-drag;
  background: none;
  border: none;
  color: white;
  width: 32px;
  height: 32px;
  cursor: pointer;
  outline: none;
}

.control-btn:hover {
  background: rgba(255,255,255,0.1);
}

.control-btn.close:hover {
  background: #e81123;
}
</style> 