<template>
  <div class="page-container">
    <div class="filter-container">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="候选人姓名">
          <el-input v-model="searchForm.name" placeholder="请输入姓名" clearable />
        </el-form-item>
        <el-form-item label="应聘职位">
          <el-select v-model="searchForm.position" placeholder="全部职位" clearable style="width: 180px">
            <el-option label="产品经理" value="pm" />
            <el-option label="前端工程师" value="frontend" />
            <el-option label="后端工程师" value="backend" />
            <el-option label="UI设计师" value="ui" />
          </el-select>
        </el-form-item>
        <el-form-item label="面试状态">
          <el-select v-model="searchForm.status" placeholder="全部状态" clearable style="width: 180px">
            <el-option label="待面试" value="pending" />
            <el-option label="面试中" value="interviewing" />
            <el-option label="已完成" value="completed" />
            <el-option label="已通过" value="passed" />
            <el-option label="已淘汰" value="rejected" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <el-card shadow="never" class="table-card">
      <el-table :data="tableData" style="width: 100%" v-loading="loading">
        <el-table-column prop="name" label="姓名" width="120">
          <template #default="{ row }">
            <div class="user-info">
              <el-avatar :size="32" :src="row.avatar" />
              <span class="user-name">{{ row.name }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="position" label="应聘职位" width="150" />
        <el-table-column prop="interviewTime" label="面试时间" width="180" />
        <el-table-column prop="score" label="综合得分" width="100" sortable>
          <template #default="{ row }">
            <span v-if="row.score" :class="getScoreClass(row.score)">{{ row.score }}</span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ getStatusLabel(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="tags" label="AI标签" min-width="200">
          <template #default="{ row }">
            <div class="tags-wrapper">
              <el-tag 
                v-for="tag in row.tags" 
                :key="tag" 
                size="small" 
                effect="plain"
                class="ai-tag"
              >
                {{ tag }}
              </el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="viewReport(row)" v-if="row.status !== 'pending'">查看报告</el-button>
            <el-button link type="primary" size="small" @click="startInterview(row)" v-if="row.status === 'pending'">开始面试</el-button>
            <el-button link type="success" size="small" @click="handlePass(row)" v-if="row.status === 'completed'">通过</el-button>
            <el-button link type="danger" size="small" @click="handleReject(row)" v-if="row.status === 'completed'">淘汰</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(45)

const searchForm = reactive({
  name: '',
  position: '',
  status: ''
})

// Mock Data
const tableData = ref([
  {
    id: 1,
    name: '张宇',
    avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
    position: '产品经理',
    interviewTime: '2025-12-16 14:30',
    score: 85,
    status: 'completed',
    tags: ['逻辑清晰', '表达能力强', '有相关经验']
  },
  {
    id: 2,
    name: '李明',
    avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
    position: '前端工程师',
    interviewTime: '2025-12-16 10:00',
    score: 92,
    status: 'passed',
    tags: ['技术扎实', 'Vue3专家', '代码规范']
  },
  {
    id: 3,
    name: '王芳',
    avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
    position: 'UI设计师',
    interviewTime: '2025-12-16 16:00',
    score: 78,
    status: 'rejected',
    tags: ['审美一般', '工具熟练']
  },
  {
    id: 4,
    name: '赵强',
    avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
    position: '后端工程师',
    interviewTime: '2025-12-17 09:30',
    score: null,
    status: 'pending',
    tags: []
  },
  {
    id: 5,
    name: '陈静',
    avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
    position: '产品经理',
    interviewTime: '2025-12-15 15:00',
    score: 88,
    status: 'completed',
    tags: ['用户思维', '数据敏感']
  }
])

const getStatusType = (status: string) => {
  const map: Record<string, string> = {
    pending: 'info',
    interviewing: 'primary',
    completed: 'warning',
    passed: 'success',
    rejected: 'danger'
  }
  return map[status] || 'info'
}

const getStatusLabel = (status: string) => {
  const map: Record<string, string> = {
    pending: '待面试',
    interviewing: '面试中',
    completed: '待决策',
    passed: '已通过',
    rejected: '已淘汰'
  }
  return map[status] || status
}

const getScoreClass = (score: number) => {
  if (score >= 90) return 'score-high'
  if (score >= 80) return 'score-medium'
  return 'score-low'
}

const handleSearch = () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
    ElMessage.success('查询成功')
  }, 500)
}

const resetSearch = () => {
  searchForm.name = ''
  searchForm.position = ''
  searchForm.status = ''
  handleSearch()
}

const viewReport = (row: any) => {
  router.push(`/hr/candidates/${row.id}`) 
}

const startInterview = (_row: any) => {
  ElMessage.info('正在连接面试间...')
}

const handlePass = (row: any) => {
  ElMessageBox.confirm(
    `确定要录用候选人 ${row.name} 吗？`,
    '录用确认',
    {
      confirmButtonText: '确定录用',
      cancelButtonText: '取消',
      type: 'success',
    }
  ).then(() => {
    row.status = 'passed'
    ElMessage.success('操作成功，已发送录用通知')
  })
}

const handleReject = (row: any) => {
  ElMessageBox.prompt('请输入淘汰理由', '淘汰确认', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
  }).then(({ value }) => {
    row.status = 'rejected'
    ElMessage.info(`已淘汰，理由：${value}`)
  })
}

const handleSizeChange = (val: number) => {
  console.log(`${val} items per page`)
}

const handleCurrentChange = (val: number) => {
  console.log(`current page: ${val}`)
}
</script>

<style scoped>
.page-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.filter-container {
  background-color: var(--bg-color-overlay);
  padding: 20px 20px 0 20px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.table-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: var(--bg-color-overlay);
  border: 1px solid var(--border-color);
  --el-card-padding: 20px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-name {
  font-weight: 500;
}

.score-high {
  color: var(--el-color-success);
  font-weight: bold;
}

.score-medium {
  color: var(--el-color-primary);
  font-weight: bold;
}

.score-low {
  color: var(--el-color-warning);
  font-weight: bold;
}

.tags-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.ai-tag {
  margin-right: 0;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>