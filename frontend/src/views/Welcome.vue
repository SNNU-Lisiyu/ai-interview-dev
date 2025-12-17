<template>
  <div class="welcome-page">
    <!-- Navigation Bar -->
    <nav class="navbar">
      <div class="nav-content">
        <div class="logo">
          <img :src="isDark ? logoLight : logoDark" alt="智面星途" class="logo-image" />
          <span class="logo-text">
            智面星途
            <span class="beta-badge">Beta</span>
          </span>
        </div>
        <div class="nav-links">
          <a href="#features">核心功能</a>
          <a href="#technology">技术原理</a>
          <a href="#scenarios">应用场景</a>
          <a href="#about">关于我们</a>
        </div>
        <div class="nav-actions">
          <el-switch
            v-model="isDark"
            inline-prompt
            :active-icon="Moon"
            :inactive-icon="Sunny"
            @change="toggleTheme"
            style="margin-right: 16px; --el-switch-on-color: #4C4D4F; --el-switch-off-color: #DCDFE6;"
          />
          <el-button type="primary" plain @click="showLoginModal = true">登录 / 注册</el-button>
        </div>
      </div>
    </nav>

    <div class="welcome-container">
      <div class="hero-section">
        <div class="hero-content">
          <h1 class="title">
            智面星途 <span class="highlight">AI面试</span>
            <span class="beta-tag">Beta</span>
          </h1>
          <p class="subtitle">洞察面试每一帧，赋能人才每一刻</p>
          <p class="description">
            基于多模态融合分析与讯飞星火大模型，为您提供专业、公正、深度的智能面试评测体验。
          </p>
          <div class="actions">
            <el-button type="primary" size="large" class="start-btn" @click="showLoginModal = true">
              立即开始 <el-icon class="el-icon--right"><ArrowRight /></el-icon>
            </el-button>
            <el-button size="large" class="learn-btn" @click="scrollToFeatures">了解更多</el-button>
          </div>
        </div>
        <div class="hero-image">
          <div class="image-placeholder">
            <img :src="isDark ? logoLight : logoDark" alt="智面星途" class="hero-logo" />
          </div>
        </div>
      </div>

      <!-- Features Section -->
      <div id="features" class="section features-section">
        <div class="section-content">
          <h2 class="section-title">核心功能</h2>
          <div class="features-grid">
            <el-card class="feature-card" shadow="hover">
              <template #header>
                <div class="card-header">
                  <el-icon :size="30" color="var(--el-color-primary)"><VideoCamera /></el-icon>
                  <span>多模态分析</span>
                </div>
              </template>
              <p>融合语音、视觉、文本三大模态，全方位捕捉面试表现，识别微表情与肢体语言。</p>
            </el-card>
            <el-card class="feature-card" shadow="hover">
              <template #header>
                <div class="card-header">
                  <el-icon :size="30" color="#67c23a"><ChatDotRound /></el-icon>
                  <span>智能追问</span>
                </div>
              </template>
              <p>基于讯飞星火大模型，根据回答动态生成追问，深度挖掘候选人潜力。</p>
            </el-card>
            <el-card class="feature-card" shadow="hover">
              <template #header>
                <div class="card-header">
                  <el-icon :size="30" color="#e6a23c"><DataAnalysis /></el-icon>
                  <span>深度报告</span>
                </div>
              </template>
              <p>生成包含能力雷达图、优劣势分析的可解释性评测报告，助力精准识才。</p>
            </el-card>
          </div>
        </div>
      </div>

      <!-- Technology Section -->
      <div id="technology" class="section tech-section">
        <div class="section-content">
          <h2 class="section-title">技术原理</h2>
          <div class="tech-content">
            <div class="tech-item">
              <h3>多模态融合</h3>
              <p>采用自研 Cross-Modal Attention 架构，实现语音、视觉、文本的深度关联分析。</p>
            </div>
            <div class="tech-item">
              <h3>大模型驱动</h3>
              <p>深度集成讯飞星火大模型，具备强大的语义理解与逻辑推理能力。</p>
            </div>
            <div class="tech-item">
              <h3>实时分析</h3>
              <p>低延迟流式处理，实时反馈情绪、语速、逻辑等关键指标。</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Scenarios Section -->
      <div id="scenarios" class="section scenarios-section">
        <div class="section-content">
          <h2 class="section-title">应用场景</h2>
          <div class="scenarios-grid">
            <div class="scenario-card">
              <h3>校园招聘</h3>
              <p>海量简历快速初筛，7x24小时无人值守面试。</p>
            </div>
            <div class="scenario-card">
              <h3>模拟面试</h3>
              <p>高校学生求职演练，提供个性化改进建议。</p>
            </div>
            <div class="scenario-card">
              <h3>内部晋升</h3>
              <p>多维度能力评估，辅助企业人才盘点。</p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Footer -->
      <footer class="footer">
        <div class="section-content">
          <p>© 2025 智面星途 Team. All Rights Reserved.</p>
          <p>陕西师范大学物理学与信息技术学院</p>
        </div>
      </footer>
    </div>

    <!-- Login/Register Modal -->
    <el-dialog
      v-model="showLoginModal"
      title="欢迎使用智面星途"
      width="400px"
      center
      destroy-on-close
    >
      <el-tabs v-model="activeTab" class="auth-tabs" stretch>
        <el-tab-pane label="登录" name="login">
          <div class="form-container">
            <el-form :model="loginForm" @submit.prevent="handleLogin">
              <el-form-item>
                <el-input v-model="loginForm.username" placeholder="用户名" :prefix-icon="User" />
              </el-form-item>
              <el-form-item>
                <el-input v-model="loginForm.password" type="password" placeholder="密码" :prefix-icon="Lock" show-password />
              </el-form-item>
              <el-button type="primary" class="submit-btn" @click="handleLogin" :loading="loading">
                登录
              </el-button>
            </el-form>
            <div class="demo-accounts">
              <p>演示账号：</p>
              <el-tag size="small" class="cursor-pointer" @click="fillDemo('candidate')">求职者: 没头脑 / 123</el-tag>
              <el-tag size="small" type="success" class="cursor-pointer" @click="fillDemo('hr')">HR: 不高兴 / 123</el-tag>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="注册" name="register">
          <div class="form-container register-container">
            <el-form :model="registerForm" label-position="top" size="default">
              <el-form-item label="身份类型" required>
                <el-radio-group v-model="registerForm.role">
                  <el-radio-button label="candidate">求职者</el-radio-button>
                  <el-radio-button label="hr">HR</el-radio-button>
                </el-radio-group>
              </el-form-item>
              <el-form-item label="姓名" required>
                <el-input v-model="registerForm.name" placeholder="请输入您的姓名" />
              </el-form-item>
              <el-form-item label="密码" required>
                <el-input v-model="registerForm.password" type="password" placeholder="设置登录密码" show-password />
              </el-form-item>
              <template v-if="registerForm.role === 'candidate'">
                <el-form-item label="目标岗位">
                  <el-input v-model="registerForm.targetPosition" placeholder="例如：产品经理" />
                </el-form-item>
                <el-form-item label="工作经验">
                  <el-select v-model="registerForm.experience" placeholder="请选择" style="width: 100%">
                    <el-option label="应届生" value="应届生" />
                    <el-option label="1-3年" value="1-3年" />
                    <el-option label="3-5年" value="3-5年" />
                    <el-option label="5年以上" value="5年以上" />
                  </el-select>
                </el-form-item>
              </template>
              <el-button type="primary" class="submit-btn" @click="handleRegister" :disabled="!isRegisterValid">
                立即注册
              </el-button>
            </el-form>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { User, Lock, ArrowRight, VideoCamera, ChatDotRound, DataAnalysis, Moon, Sunny } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { userState, switchUser, addUser } from '../store/userState'
import logoLight from '../assets/logo-light.png'
import logoDark from '../assets/logo-dark.png'

const router = useRouter()
const showLoginModal = ref(false)
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

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    isDark.value = true
    document.documentElement.classList.add('dark')
  }
})

const scrollToFeatures = () => {
  document.getElementById('features')?.scrollIntoView({ behavior: 'smooth' })
}
const activeTab = ref('login')
const loading = ref(false)

const loginForm = reactive({
  username: '',
  password: ''
})

const registerForm = reactive({
  role: 'candidate',
  name: '',
  password: '',
  targetPosition: '',
  experience: '应届生',
  skills: '',
  resumeSummary: ''
})

const isRegisterValid = computed(() => {
  if (!registerForm.name || !registerForm.password) return false
  if (registerForm.role === 'candidate') {
    // For candidate, these fields are optional but good to have. 
    // Let's make them optional for quick registration as per request "empty info"
    return true
  }
  return true
})

const fillDemo = (role: 'candidate' | 'hr') => {
  if (role === 'candidate') {
    loginForm.username = '没头脑'
    loginForm.password = '123'
  } else {
    loginForm.username = '不高兴'
    loginForm.password = '123'
  }
}

const handleLogin = () => {
  if (!loginForm.username || !loginForm.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }
  
  loading.value = true
  setTimeout(() => {
    const user = userState.users.find(u => u.name === loginForm.username)
    
    if (user) {
      if (!user.password || user.password === loginForm.password) {
        switchUser(user.id)
        ElMessage.success('登录成功')
        showLoginModal.value = false
        if (user.role === 'hr') {
          router.push('/hr')
        } else {
          router.push('/candidate/interview')
        }
      } else {
        ElMessage.error('密码错误')
      }
    } else {
      ElMessage.error('用户不存在')
    }
    loading.value = false
  }, 500)
}

const handleRegister = () => {
  if (isRegisterValid.value) {
    addUser({
      name: registerForm.name,
      password: registerForm.password,
      role: registerForm.role as 'candidate' | 'hr',
      targetPosition: registerForm.targetPosition,
      experience: registerForm.experience,
      skills: registerForm.skills,
      resumeSummary: registerForm.resumeSummary
    })
    ElMessage.success('注册成功，已自动登录')
    showLoginModal.value = false
    if (registerForm.role === 'hr') {
      router.push('/hr')
    } else {
      router.push('/candidate/interview')
    }
  }
}
</script>

<style scoped>
.welcome-page {
  min-height: 100vh;
  background-color: var(--bg-color);
  transition: background-color 0.3s;
}

.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 64px;
  background-color: var(--bg-color-overlay);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--border-color);
  z-index: 1000;
  display: flex;
  justify-content: center;
  transition: background-color 0.3s, border-color 0.3s;
}

.nav-content {
  width: 100%;
  max-width: 1600px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-image {
  height: 40px;
  width: auto;
}

.logo-text {
  font-size: 22px;
  font-weight: bold;
  color: var(--el-color-primary);
  letter-spacing: 1px;
}

.nav-links {
  display: flex;
  gap: 30px;
}

.nav-links a {
  text-decoration: none;
  color: var(--text-color-regular);
  font-size: 16px;
  transition: color 0.3s;
}

.nav-links a:hover {
  color: var(--el-color-primary);
}

.welcome-container {
  width: 100%;
  padding-top: 64px; /* Offset for fixed navbar */
  box-sizing: border-box;
}

.section-content {
  width: 100%;
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 40px;
  box-sizing: border-box;
}

.section {
  padding: 80px 0;
  border-bottom: 1px solid var(--border-color);
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 60px;
  color: var(--text-color-primary);
}

.hero-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 120px 40px 80px;
  gap: 40px;
  min-height: 600px;
  max-width: 1600px;
  margin: 0 auto;
}

.hero-content {
  flex: 1;
  text-align: left;
  padding-left: 100px;
  margin-top: -100px;
}

.title {
  font-size: 4.5rem;
  font-weight: 800;
  margin-bottom: 1.5rem;
  color: var(--text-color-primary);
  line-height: 1.2;
}

.highlight {
  background: linear-gradient(120deg, var(--el-color-primary) 0%, #a0cfff 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitle {
  font-size: 2.2rem;
  color: var(--text-color-regular);
  margin-bottom: 2rem;
  font-weight: 300;
}

.description {
  font-size: 1.4rem;
  color: var(--text-color-secondary);
  margin-bottom: 3rem;
  line-height: 1.6;
  max-width: 700px;
}

.actions {
  display: flex;
  gap: 20px;
}

.hero-image {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.image-placeholder {
  width: 420px;
  height: 420px;
  background: var(--bg-color-overlay);
  border-radius: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: var(--shadow-float);
  animation: float 6s ease-in-out infinite;
  border: 1px solid var(--border-color);
}

.hero-logo {
  width: 280px;
  height: auto;
  display: block;
}

@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
  100% { transform: translateY(0px); }
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
  padding: 0 20px;
}

.feature-card {
  height: 100%;
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.2rem;
  font-weight: bold;
}

.tech-content {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
  padding: 0 20px;
  text-align: center;
}

.tech-item h3 {
  font-size: 1.5rem;
  margin-bottom: 15px;
  color: var(--text-color-primary);
}

.tech-item p {
  color: var(--text-color-regular);
  line-height: 1.6;
}

.scenarios-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
  padding: 0 20px;
}

.scenario-card {
  background: var(--bg-color-overlay);
  padding: 30px;
  border-radius: 12px;
  box-shadow: var(--shadow-card);
  text-align: center;
  transition: transform 0.3s;
}

.scenario-card:hover {
  transform: translateY(-5px);
}

.scenario-card h3 {
  font-size: 1.4rem;
  margin-bottom: 15px;
  color: var(--el-color-primary);
}

.footer {
  padding: 40px 0;
  text-align: center;
  color: var(--text-color-secondary);
  background-color: var(--bg-color-overlay);
  margin-top: 40px;
}

/* Auth Modal Styles */
.auth-tabs {
  margin-top: 10px;
}

.form-container {
  padding: 20px 10px;
}

.submit-btn {
  width: 100%;
  margin-top: 10px;
  height: 40px;
  font-size: 16px;
}

.demo-accounts {
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid var(--border-color);
  text-align: center;
}

.demo-accounts p {
  font-size: 12px;
  color: var(--text-color-secondary);
  margin-bottom: 8px;
}

.demo-accounts .el-tag {
  margin: 0 5px;
}

.cursor-pointer {
  cursor: pointer;
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
  position: relative;
  top: -1px;
}

.beta-tag {
  display: inline-block;
  font-size: 1.2rem;
  color: #fff;
  background: linear-gradient(90deg, #ffba00 0%, #ff9c00 100%);
  padding: 4px 12px;
  border-radius: 8px;
  margin-left: 15px;
  vertical-align: middle;
  font-weight: 600;
  line-height: 1.4;
  box-shadow: 0 4px 12px rgba(255, 156, 0, 0.3);
  position: relative;
  top: -10px;
}
</style>

<style>
/* Force dark background when html has dark class */
html.dark .welcome-container {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
}
</style>
