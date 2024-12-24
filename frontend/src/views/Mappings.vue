<template>
  <div class="mappings-container">
    <div class="header">
      <h1>映射管理</h1>
      <el-button type="primary" @click="showAddDialog">
        添加新映射
      </el-button>
    </div>

    <div class="mapping-list">
      <el-card v-for="mapping in mappings" 
               :key="mapping.name"
               class="mapping-card">
        <template #header>
          <div class="card-header">
            <img :src="mapping.icon" class="server-icon">
            <h3>{{ mapping.name }}</h3>
            <el-tag :type="mapping.status === 'running' ? 'success' : 'info'">
              {{ mapping.status }}
            </el-tag>
          </div>
        </template>
        
        <div class="card-content">
          <div class="motd" v-html="formatMotd(mapping.motd)"></div>
          <div class="server-info">
            <p>地址: {{ mapping.address }}</p>
            <p>映射IP: {{ mapping.assigned_ip }}</p>
            <p>版本: {{ mapping.version }}</p>
            <p>延迟: {{ mapping.latency }}ms</p>
          </div>
        </div>

        <div class="card-actions">
          <el-button-group>
            <el-button type="primary" @click="toggleMapping(mapping)">
              {{ mapping.status === 'running' ? '停止' : '启动' }}
            </el-button>
            <el-button type="warning" @click="editMapping(mapping)">
              编辑
            </el-button>
            <el-button type="danger" @click="deleteMapping(mapping)">
              删除
            </el-button>
          </el-button-group>
        </div>
      </el-card>
    </div>

    <!-- 添加/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑映射' : '添加映射'"
      width="500px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="映射名称">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="服务器地址">
          <el-input v-model="form.address"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveMapping">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { formatMotd } from '../utils/motd'

export default {
  name: 'Mappings',
  setup() {
    const mappings = ref([])
    const dialogVisible = ref(false)
    const isEdit = ref(false)
    const form = ref({
      name: '',
      address: ''
    })

    // ... 实现各种方法 ...

    return {
      mappings,
      dialogVisible,
      isEdit,
      form,
      formatMotd,
      showAddDialog,
      editMapping,
      deleteMapping,
      toggleMapping,
      saveMapping
    }
  }
}
</script>

<style scoped>
.mappings-container {
  padding: 20px;
}

.mapping-card {
  margin-bottom: 20px;
  transition: all 0.3s;
}

.mapping-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* ... 更多样式 ... */
</style> 