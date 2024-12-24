<template>
  <div class="server-monitor">
    <el-card class="monitor-card">
      <template #header>
        <div class="card-header">
          <h2>服务器列表</h2>
          <el-button type="primary" @click="addServer">添加服务器</el-button>
        </div>
      </template>

      <div class="server-list">
        <el-table :data="servers" style="width: 100%">
          <el-table-column prop="name" label="名称" />
          <el-table-column prop="address" label="地址" />
          <el-table-column prop="port" label="映射端口" />
          <el-table-column label="状态">
            <template #default="{ row }">
              <el-tag :type="row.status === 'running' ? 'success' : 'info'">
                {{ row.status === 'running' ? '运行中' : '已停止' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200">
            <template #default="{ row }">
              <el-button-group>
                <el-button 
                  :type="row.status === 'running' ? 'danger' : 'success'"
                  size="small"
                  @click="toggleServer(row)"
                >
                  {{ row.status === 'running' ? '停止' : '启动' }}
                </el-button>
                <el-button 
                  type="primary" 
                  size="small"
                  @click="editServer(row)"
                >
                  编辑
                </el-button>
                <el-button 
                  type="danger" 
                  size="small"
                  @click="deleteServer(row)"
                >
                  删除
                </el-button>
              </el-button-group>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 添加/编辑服务器对话框 -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="500px"
    >
      <el-form :model="serverForm" label-width="100px">
        <el-form-item label="服务器名称">
          <el-input v-model="serverForm.name" />
        </el-form-item>
        <el-form-item label="服务器地址">
          <el-input v-model="serverForm.address" />
        </el-form-item>
        <el-form-item label="映射端口">
          <el-input-number v-model="serverForm.port" :min="1" :max="65535" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveServer">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'ServerMonitor',
  data() {
    return {
      servers: [
        { 
          name: '测试服务器', 
          address: 'localhost:25565',
          port: 25566,
          status: 'stopped'
        }
      ],
      dialogVisible: false,
      dialogTitle: '添加服务器',
      serverForm: {
        name: '',
        address: '',
        port: 25565
      },
      editingIndex: -1
    }
  },
  methods: {
    addServer() {
      this.dialogTitle = '添加服务器'
      this.serverForm = {
        name: '',
        address: '',
        port: 25565
      }
      this.editingIndex = -1
      this.dialogVisible = true
    },
    editServer(server) {
      this.dialogTitle = '编辑服务器'
      this.serverForm = { ...server }
      this.editingIndex = this.servers.indexOf(server)
      this.dialogVisible = true
    },
    saveServer() {
      const server = { ...this.serverForm }
      if (this.editingIndex === -1) {
        server.status = 'stopped'
        this.servers.push(server)
      } else {
        this.servers[this.editingIndex] = server
      }
      this.dialogVisible = false
    },
    deleteServer(server) {
      this.$confirm('确定要删除这个服务器吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.servers.indexOf(server)
        this.servers.splice(index, 1)
        this.$message({
          type: 'success',
          message: '删除成功'
        })
      }).catch(() => {})
    },
    toggleServer(server) {
      server.status = server.status === 'running' ? 'stopped' : 'running'
    }
  }
}
</script>

<style scoped>
.server-monitor {
  max-width: 1200px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
}

.server-list {
  margin-top: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>