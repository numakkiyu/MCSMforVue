<template>
  <div class="about-container">
    <el-card class="about-section">
      <template #header>
        <h2>关于本应用</h2>
      </template>
      <div class="about-content">
        <img src="../assets/logo.png" alt="Logo" class="app-logo">
        <h1>Minecraft 服务器映射工具</h1>
        <p class="version">版本 1.1.0</p>
        <p class="description">
          这是一个用于管理 Minecraft 服务器映射的工具,可以帮助你轻松管理多个服务器的端口映射。
        </p>
      </div>
    </el-card>

    <el-card class="about-section">
      <template #header>
        <h2>鸣谢</h2>
      </template>
      <div class="credits">
        <h3>开发团队</h3>
        <ul>
          <li>主程序开发: XXX</li>
          <li>UI 设计: XXX</li>
          <li>测试: XXX</li>
        </ul>

        <h3>开源项目</h3>
        <ul>
          <li>Vue.js</li>
          <li>Element Plus</li>
          <li>Python Flask</li>
        </ul>
      </div>
    </el-card>

    <el-card class="about-section">
      <template #header>
        <h2>赞助支持</h2>
      </template>
      <div class="sponsors">
        <div class="sponsor-tier">
          <h3>钻石赞助</h3>
          <div class="sponsor-list">
            <!-- 赞助者列表 -->
          </div>
        </div>
      </div>
    </el-card>

    <el-card class="about-section">
      <template #header>
        <h2>相关链接</h2>
      </template>
      <div class="links">
        <el-button type="primary" @click="openLink('https://github.com/your-repo')">
          <i class="fab fa-github"></i> GitHub
        </el-button>
        <el-button type="success" @click="openLink('https://your-website.com')">
          <i class="fas fa-globe"></i> 官方网站
        </el-button>
        <el-button type="warning" @click="openLink('https://your-docs.com')">
          <i class="fas fa-book"></i> 使用文档
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'About',
  methods: {
    openLink(url) {
      window.open(url, '_blank')
    }
  }
}
</script>

<style scoped>
.about-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.about-section {
  margin-bottom: 20px;
  transition: transform 0.3s;
}

.about-section:hover {
  transform: translateY(-2px);
}

.app-logo {
  width: 120px;
  height: 120px;
  margin-bottom: 20px;
}

.version {
  color: var(--el-text-color-secondary);
  font-size: 0.9em;
}

.description {
  margin: 20px 0;
  line-height: 1.6;
}

.credits ul {
  list-style: none;
  padding: 0;
}

.credits li {
  margin: 8px 0;
}

.links {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.sponsor-tier {
  margin: 20px 0;
}

.sponsor-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
}
</style> 