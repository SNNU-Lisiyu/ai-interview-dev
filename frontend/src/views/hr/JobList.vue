<template>
  <div class="page-container">
    <div class="action-bar">
      <el-button type="primary" icon="Plus" @click="handleCreate">发布新职位</el-button>
      <div class="search-box">
        <el-input v-model="searchText" placeholder="搜索职位名称" prefix-icon="Search" clearable @clear="handleSearch" @input="handleSearch" />
      </div>
    </div>

    <el-row :gutter="20">
      <el-col :span="8" v-for="job in filteredJobs" :key="job.id">
        <el-card shadow="hover" class="job-card">
          <div class="job-header">
            <h3 class="job-title">{{ job.title }}</h3>
            <el-tag :type="job.status === 'active' ? 'success' : 'info'" size="small">
              {{ job.status === 'active' ? '招聘中' : '已结束' }}
            </el-tag>
          </div>
          <div class="job-info">
            <div class="info-item">
              <el-icon><OfficeBuilding /></el-icon>
              <span>{{ job.department }}</span>
            </div>
            <div class="info-item">
              <el-icon><Location /></el-icon>
              <span>{{ job.location }}</span>
            </div>
            <div class="info-item">
              <el-icon><User /></el-icon>
              <span>{{ job.candidates }} 位候选人</span>
            </div>
          </div>
          <div class="job-tags">
            <el-tag v-for="tag in job.tags" :key="tag" size="small" type="info" effect="plain">{{ tag }}</el-tag>
          </div>
          <div class="job-footer">
            <span class="update-time">更新于 {{ job.updatedAt }}</span>
            <div class="actions">
              <el-button link type="primary" @click="handleEdit(job)">编辑</el-button>
              <el-button link type="danger" @click="handleClose(job)" v-if="job.status === 'active'">结束</el-button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Create/Edit Dialog -->
    <el-dialog v-model="dialogVisible" :title="dialogType === 'create' ? '发布新职位' : '编辑职位'" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="职位名称">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="所属部门">
          <el-select v-model="form.department" style="width: 100%">
            <el-option label="产品部" value="产品部" />
            <el-option label="研发部" value="研发部" />
            <el-option label="设计部" value="设计部" />
            <el-option label="市场部" value="市场部" />
          </el-select>
        </el-form-item>
        <el-form-item label="工作地点">
          <el-input v-model="form.location" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const searchText = ref('')
const dialogVisible = ref(false)
const dialogType = ref<'create' | 'edit'>('create')

const form = reactive({
  title: '',
  department: '',
  location: '西安'
})

const jobs = ref([
  {
    id: 1,
    title: '高级产品经理',
    department: '产品部',
    location: '西安',
    candidates: 12,
    status: 'active',
    updatedAt: '2025-12-16',
    tags: ['5-10年', 'B端', 'SaaS']
  },
  {
    id: 2,
    title: '资深前端工程师',
    department: '研发部',
    location: '西安',
    candidates: 8,
    status: 'active',
    updatedAt: '2025-12-15',
    tags: ['Vue3', 'TypeScript', '架构设计']
  },
  {
    id: 3,
    title: 'UI设计师',
    department: '设计部',
    location: '成都',
    candidates: 25,
    status: 'closed',
    updatedAt: '2025-12-10',
    tags: ['视觉设计', '交互设计']
  },
  {
    id: 4,
    title: 'Python后端开发',
    department: '研发部',
    location: '西安',
    candidates: 5,
    status: 'active',
    updatedAt: '2025-12-16',
    tags: ['Django', 'AI应用']
  }
])

const filteredJobs = computed(() => {
  if (!searchText.value) return jobs.value
  return jobs.value.filter(job => job.title.toLowerCase().includes(searchText.value.toLowerCase()))
})

const handleSearch = () => {
  // Filter is handled by computed
}

const handleCreate = () => {
  dialogType.value = 'create'
  form.title = ''
  form.department = ''
  form.location = '西安'
  dialogVisible.value = true
}

const handleEdit = (job: any) => {
  dialogType.value = 'edit'
  form.title = job.title
  form.department = job.department
  form.location = job.location
  dialogVisible.value = true
}

const handleClose = (job: any) => {
  ElMessageBox.confirm(
    `确定要结束 ${job.title} 的招聘吗？`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
    job.status = 'closed'
    ElMessage.success('已结束招聘')
  })
}

const handleSubmit = () => {
  dialogVisible.value = false
  ElMessage.success(dialogType.value === 'create' ? '发布成功' : '修改成功')
}
</script>

<style scoped>
.page-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--bg-color-overlay);
  padding: 15px 20px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.search-box {
  width: 300px;
}

.job-card {
  margin-bottom: 20px;
  background-color: var(--bg-color-overlay);
  border: 1px solid var(--border-color);
  transition: transform 0.3s;
}

.job-card:hover {
  transform: translateY(-5px);
}

.job-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.job-title {
  margin: 0;
  font-size: 16px;
  color: var(--text-color-primary);
  line-height: 1.4;
}

.job-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 15px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--text-color-regular);
}

.job-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 15px;
}

.job-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid var(--border-color);
  padding-top: 15px;
}

.update-time {
  font-size: 12px;
  color: var(--text-color-secondary);
}
</style>
