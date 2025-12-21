<template>
  <div class="profile-container">
    <div class="profile-header">
      <h1 class="page-title">个人中心</h1>
      <div class="user-info-display">
        <el-avatar :size="50" src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" />
        <div class="user-details">
          <span class="name">{{ userState.currentUser.name }}</span>
          <span class="role">求职者</span>
        </div>
      </div>
    </div>

    <div class="profile-content">
      <el-card class="profile-card">
        <template #header>
          <div class="card-header">
            <span>基本信息设置</span>
          </div>
        </template>
        
        <el-form :model="userState.currentUser" label-width="100px">
          <el-form-item label="姓名">
            <el-input v-model="userState.currentUser.name" />
          </el-form-item>
          
          <el-form-item label="目标岗位">
            <el-input v-model="userState.currentUser.targetPosition" placeholder="例如：产品经理、Java开发工程师" />
          </el-form-item>
          
          <el-form-item label="工作经验">
            <el-select v-model="userState.currentUser.experience" placeholder="请选择">
              <el-option label="应届生" value="应届生" />
              <el-option label="1-3年" value="1-3年" />
              <el-option label="3-5年" value="3-5年" />
              <el-option label="5年以上" value="5年以上" />
            </el-select>
          </el-form-item>
          
          <el-form-item label="核心技能">
            <el-input v-model="userState.currentUser.skills" type="textarea" :rows="2" placeholder="例如：Vue3, Python, 项目管理" />
          </el-form-item>
          
          <el-form-item label="简历简介">
            <el-input 
              v-model="userState.currentUser.resumeSummary" 
              type="textarea" 
              :rows="6" 
              placeholder="请输入您的简历摘要或自我介绍，AI面试官将根据此内容为您定制问题。" 
            />
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" @click="saveProfile">保存修改</el-button>
          </el-form-item>
        </el-form>
      </el-card>
      
      <div class="tips-section">
        <h3><el-icon><InfoFilled /></el-icon> 提示</h3>
        <p>完善个人信息后，AI面试官会根据您的<b>目标岗位</b>和<b>简历简介</b>生成更具针对性的面试问题。</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { userState } from '../store/userState'
import { ElMessage } from 'element-plus'
import { InfoFilled } from '@element-plus/icons-vue'

const saveProfile = () => {
  // Trigger reactivity update for localStorage
  userState.currentUser = { ...userState.currentUser }
  ElMessage.success('个人信息已保存')
}
</script>

<style scoped>
.profile-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.page-title {
  font-size: 28px;
  color: var(--text-color-primary);
  margin: 0;
}

.user-info-display {
  display: flex;
  align-items: center;
  gap: 15px;
}

.user-details {
  display: flex;
  flex-direction: column;
}

.user-details .name {
  font-size: 18px;
  font-weight: bold;
  color: var(--text-color-primary);
}

.user-details .role {
  font-size: 12px;
  color: var(--text-color-secondary);
  background-color: var(--el-color-primary-light-9);
  padding: 2px 6px;
  border-radius: 4px;
  width: fit-content;
}

.profile-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tips-section {
  background: var(--bg-color-overlay);
  padding: 15px;
  border-radius: 8px;
  border-left: 4px solid var(--el-color-warning);
  height: fit-content;
}

.tips-section h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 0;
  margin-bottom: 10px;
  color: var(--text-color-primary);
}

.tips-section p {
  color: var(--text-color-regular);
  font-size: 0.9rem;
  margin-bottom: 8px;
}
</style>
