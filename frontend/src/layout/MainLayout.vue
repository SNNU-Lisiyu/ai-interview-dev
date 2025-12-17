<template>
  <el-container class="layout-container">
    <el-header class="header">
      <div class="header-content">
        <div class="logo-container">
          <img :src="isDark ? logoLight : logoDark" alt="智面星途" class="logo-image" />
          <span class="logo-text">智面星途</span>
          <span class="beta-badge">Beta</span>
        </div>
        
        <el-menu
          :default-active="$route.path"
          class="nav-menu"
          mode="horizontal"
          router
          :ellipsis="false"
        >
          <el-menu-item index="/candidate/interview">
            <el-icon><VideoCamera /></el-icon>
            <span>模拟面试</span>
          </el-menu-item>
          <el-menu-item index="/candidate/report">
            <el-icon><DataAnalysis /></el-icon>
            <span>评测报告</span>
          </el-menu-item>
        </el-menu>

        <div class="user-actions">
          <el-switch
            v-model="isDark"
            inline-prompt
            :active-icon="Moon"
            :inactive-icon="Sunny"
            @change="toggleTheme"
            style="margin-right: 20px; --el-switch-on-color: #4C4D4F; --el-switch-off-color: #DCDFE6;"
          />
          <el-dropdown trigger="click" @command="handleCommand">
            <div class="user-info-avatar">
              <el-avatar :size="32" src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" />
              <span class="username">{{ userState.currentUser.name }}</span>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                <el-dropdown-item command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </el-header>

    <el-main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </el-main>
    
    <el-footer class="footer">
      <p>© 2025 智面星途 Team. All Rights Reserved.</p>
    </el-footer>
  </el-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Moon, Sunny, VideoCamera, DataAnalysis } from '@element-plus/icons-vue'
import { userState } from '../store/userState'
import logoLight from '../assets/logo-light.png'
import logoDark from '../assets/logo-dark.png'

const router = useRouter()
const isDark = ref(false)

const toggleTheme = (val: boolean) => {
  const html = document.documentElement
  if (val) {
    html.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    html.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
}

const handleCommand = (command: string) => {
  if (command === 'profile') {
    router.push('/candidate/profile')
  } else if (command === 'logout') {
    router.push('/')
  }
}

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    isDark.value = true
    document.documentElement.classList.add('dark')
  }
})
</script>

<style scoped>
.layout-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  padding: 0;
  background-color: var(--bg-color-overlay);
  border-bottom: 1px solid var(--border-color);
  height: 60px;
  position: sticky;
  top: 0;
  z-index: 100;
  transition: background-color 0.3s, border-color 0.3s;
}

.header-content {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between; /* 两端对齐 */
  padding: 0 20px; /* 减少内边距 */
  box-sizing: border-box;
}

.logo-container {
  display: flex;
  align-items: center;
  width: 200px; /* 固定宽度，确保左侧区域稳定 */
}

.logo-image {
  height: 48px;
  width: auto;
  display: block;
  margin-right: 12px;
}

.logo-text {
  font-size: 22px;
  font-weight: bold;
  color: var(--el-color-primary);
  letter-spacing: 1px;
  position: relative;
  top: -2px;
}

.beta-badge {
  display: inline-block;
  font-size: 10px;
  color: #fff;
  background: linear-gradient(90deg, #ffba00 0%, #ff9c00 100%);
  padding: 1px 5px;
  border-radius: 4px;
  margin-left: 6px;
  vertical-align: top;
  font-weight: 600;
  line-height: 1.4;
  margin-top: 0px;
  box-shadow: 0 2px 4px rgba(255, 156, 0, 0.2);
}

.nav-menu {
  border-bottom: none;
  background-color: transparent;
  min-width: 400px;
  display: flex;
  justify-content: center; /* 尝试居中菜单项 */
}

/* 强制覆盖 el-menu 的 flex 行为以实现居中 */
:deep(.el-menu--horizontal) {
  display: flex;
  justify-content: center;
  border-bottom: none;
}

.user-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  width: 200px; /* 与 Logo 区域宽度一致，保持对称 */
}

.user-info-avatar {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.user-info-avatar:hover {
  background-color: var(--el-fill-color-light);
}

.username {
  margin-left: 8px;
  font-size: 14px;
  color: var(--text-color-primary);
}

.main-content {
  background-color: var(--bg-color);
  padding: 20px;
  flex: 1;
  width: 100%;
  max-width: 1400px; /* 匹配 header 的宽度 */
  margin: 0 auto;
  box-sizing: border-box;
  transition: background-color 0.3s;
}

.footer {
  text-align: center;
  padding: 10px;
  color: var(--text-color-secondary);
  font-size: 12px;
  background-color: var(--bg-color-overlay);
  border-top: 1px solid var(--border-color);
  margin-top: auto;
  transition: background-color 0.3s, border-color 0.3s, color 0.3s;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>