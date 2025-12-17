<template>
  <el-container class="hr-layout-container">
    <el-aside width="240px" class="aside">
      <div class="logo-container">
        <img :src="isDark ? logoLight : logoDark" alt="智面星途" class="logo-image" />
        <span class="logo-text">
          智面星途 <span class="logo-sub">HR端</span>
          <span class="beta-badge">Beta</span>
        </span>
      </div>
      <el-menu
        :default-active="$route.path"
        class="hr-menu"
        router
        :collapse="false"
      >
        <el-menu-item index="/hr/dashboard">
          <el-icon><DataBoard /></el-icon>
          <span>工作台</span>
        </el-menu-item>
        <el-menu-item index="/hr/candidates">
          <el-icon><User /></el-icon>
          <span>候选人管理</span>
        </el-menu-item>
        <el-menu-item index="/hr/jobs">
          <el-icon><Suitcase /></el-icon>
          <span>职位管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    
    <el-container>
      <el-header class="header">
        <div class="header-left">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/hr/dashboard' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>{{ currentRouteName }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="header-right">
          <el-switch
            v-model="isDark"
            inline-prompt
            :active-icon="Moon"
            :inactive-icon="Sunny"
            @change="toggleTheme"
            style="margin-right: 20px; --el-switch-on-color: #4C4D4F; --el-switch-off-color: #DCDFE6;"
          />
          <el-dropdown @command="handleCommand">
            <div class="user-info-avatar">
              <el-avatar :size="32" src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" />
              <span class="username">{{ userState.currentUser.name }}</span>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item>个人中心</el-dropdown-item>
                <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      
      <el-main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Moon, Sunny, DataBoard, User, Suitcase } from '@element-plus/icons-vue'
import { userState } from '../store/userState'
import logoLight from '../assets/logo-light.png'
import logoDark from '../assets/logo-dark.png'

const route = useRoute()
const router = useRouter()
const isDark = ref(false)

const currentRouteName = computed(() => {
  const nameMap: Record<string, string> = {
    'HRDashboard': '工作台',
    'HRCandidates': '候选人管理',
    'HRJobs': '职位管理'
  }
  return nameMap[route.name as string] || '当前页面'
})

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
  if (command === 'logout') {
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
.hr-layout-container {
  height: 100vh;
}

.aside {
  background-color: var(--bg-color-overlay);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  transition: background-color 0.3s, border-color 0.3s;
}

.logo-container {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid var(--border-color);
}

.logo-image {
  height: 32px;
  width: auto;
  margin-right: 8px;
}

.logo-text {
  font-size: 20px;
  font-weight: bold;
  color: var(--el-color-primary);
}

.logo-sub {
  font-size: 12px;
  background: var(--el-color-primary);
  color: #fff;
  padding: 2px 6px;
  border-radius: 4px;
  margin-left: 8px;
  vertical-align: middle;
}

.beta-badge {
  display: inline-block;
  font-size: 10px;
  color: #fff;
  background: linear-gradient(90deg, #ffba00 0%, #ff9c00 100%);
  padding: 1px 5px;
  border-radius: 4px;
  margin-left: 6px;
  vertical-align: middle;
  font-weight: 600;
  line-height: 1.4;
  box-shadow: 0 2px 4px rgba(255, 156, 0, 0.2);
}

.hr-menu {
  border-right: none;
  background-color: transparent;
  flex: 1;
}

.header {
  background-color: var(--bg-color-overlay);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  transition: background-color 0.3s, border-color 0.3s;
}

.header-right {
  display: flex;
  align-items: center;
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
  transition: background-color 0.3s;
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
