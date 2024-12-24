<template>
  <div class="batch-operations">
    <div class="operations-header">
      <el-checkbox
        v-model="selectAll"
        @change="handleSelectAll"
      >
        全选
      </el-checkbox>
      
      <div class="operations-buttons">
        <el-button-group>
          <el-button 
            type="primary"
            :disabled="!hasSelected"
            @click="handleBatchStart"
          >
            批量启动
          </el-button>
          <el-button 
            type="warning"
            :disabled="!hasSelected"
            @click="handleBatchStop"
          >
            批量停止
          </el-button>
          <el-button 
            type="danger"
            :disabled="!hasSelected"
            @click="handleBatchDelete"
          >
            批量删除
          </el-button>
        </el-button-group>
        
        <el-dropdown @command="handleBatchCommand">
          <el-button>
            更多操作
            <el-icon class="el-icon--right">
              <arrow-down />
            </el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="export">导出选中</el-dropdown-item>
              <el-dropdown-item command="copy">复制配置</el-dropdown-item>
              <el-dropdown-item command="move">移动分组</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>

    <div class="selected-items">
      <el-tag
        v-for="item in selectedItems"
        :key="item.id"
        closable
        @close="handleDeselect(item)"
      >
        {{ item.name }}
      </el-tag>
    </div>

    <el-table
      :data="tableData"
      @selection-change="handleSelectionChange"
    >
      <el-table-column
        type="selection"
        width="55"
      />
      <el-table-column
        prop="name"
        label="名称"
      />
      <el-table-column
        prop="address"
        label="地址"
      />
      <el-table-column
        prop="status"
        label="状态"
      >
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        width="200"
      >
        <template #default="{ row }">
          <el-button-group>
            <el-button 
              size="small"
              :type="row.status === 'running' ? 'warning' : 'success'"
              @click="handleToggle(row)"
            >
              {{ row.status === 'running' ? '停止' : '启动' }}
            </el-button>
            <el-button
              size="small"
              type="primary"
              @click="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-button
              size="small"
              type="danger"
              @click="handleDelete(row)"
            >
              删除
            </el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <!-- 批量编辑对话框 -->
    <el-dialog
      v-model="batchEditVisible"
      title="批量编辑"
      width="500px"
    >
      <el-form :model="batchEditForm">
        <el-form-item label="分组">
          <el-select v-model="batchEditForm.group">
            <el-option
              v-for="group in groups"
              :key="group.value"
              :label="group.label"
              :value="group.value"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="batchEditVisible = false">取消</el-button>
          <el-button type="primary" @click="handleBatchEdit">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessageBox } from 'element-plus'
import { ArrowDown } from '@element-plus/icons-vue'
import { useMappingStore } from '../stores/mapping'
import { exportData } from '../utils/dataTransfer'

const mappingStore = useMappingStore()
const selectAll = ref(false)
const selectedItems = ref([])
const batchEditVisible = ref(false)
const batchEditForm = ref({
  group: ''
})

const tableData = computed(() => mappingStore.mappings)
const hasSelected = computed(() => selectedItems.value.length > 0)

const handleSelectAll = (val) => {
  if (val) {
    selectedItems.value = [...tableData.value]
  } else {
    selectedItems.value = []
  }
}

const handleSelectionChange = (selection) => {
  selectedItems.value = selection
  selectAll.value = selection.length === tableData.value.length
}

const handleDeselect = (item) => {
  selectedItems.value = selectedItems.value.filter(i => i.id !== item.id)
}

const handleBatchStart = async () => {
  try {
    await Promise.all(
      selectedItems.value.map(item => mappingStore.toggleMapping(item.name))
    )
  } catch (error) {
    console.error('批量启动失败:', error)
  }
}

const handleBatchStop = async () => {
  try {
    await Promise.all(
      selectedItems.value.map(item => mappingStore.toggleMapping(item.name))
    )
  } catch (error) {
    console.error('批量停止失败:', error)
  }
}

const handleBatchDelete = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要删除选中的映射吗？此操作不可恢复。',
      '警告',
      {
        type: 'warning'
      }
    )
    await Promise.all(
      selectedItems.value.map(item => mappingStore.deleteMapping(item.name))
    )
  } catch (error) {
    if (error !== 'cancel') {
      console.error('批量删除失败:', error)
    }
  }
}

const handleBatchCommand = (command) => {
  switch (command) {
    case 'export':
      exportData(selectedItems.value, 'mappings.json')
      break
    case 'copy':
      // 实现复制配置逻辑
      break
    case 'move':
      batchEditVisible.value = true
      break
  }
}

const handleBatchEdit = async () => {
  try {
    // 实现批量编辑逻辑
    batchEditVisible.value = false
  } catch (error) {
    console.error('批量编辑失败:', error)
  }
}
</script>

<style scoped>
.batch-operations {
  padding: 20px;
}

.operations-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.operations-buttons {
  display: flex;
  gap: 10px;
}

.selected-items {
  margin-bottom: 20px;
}

.selected-items .el-tag {
  margin-right: 8px;
  margin-bottom: 8px;
}
</style> 