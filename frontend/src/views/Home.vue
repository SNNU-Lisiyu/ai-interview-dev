<template>
  <div class="home-container">
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="title">智面星途 <span class="highlight">AI面试</span></h1>
        <p class="subtitle">洞察面试每一帧，赋能人才每一刻</p>
        <p class="description">
          基于多模态融合分析与讯飞星火大模型，为您提供专业、公正、深度的智能面试评测体验。
        </p>
        <div class="actions">
          <el-button type="primary" size="large" class="start-btn" @click="$router.push('/candidate/interview')">
            立即开始面试 <el-icon class="el-icon--right"><ArrowRight /></el-icon>
          </el-button>
          <el-button size="large" class="learn-btn">了解更多</el-button>
        </div>
      </div>
      <div class="hero-image">
        <!-- Placeholder for hero image -->
        <div class="image-placeholder">
          <el-icon :size="100" color="var(--el-color-primary)"><Monitor /></el-icon>
        </div>
      </div>
    </div>

    <div class="features-section">
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
</template>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
}

.hero-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 80px 0;
  gap: 40px;
}

.hero-content {
  flex: 1;
  text-align: left;
}

.title {
  font-size: 3.5rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: var(--text-color-primary);
  line-height: 1.2;
}

.highlight {
  background: linear-gradient(120deg, var(--el-color-primary) 0%, #a0cfff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitle {
  font-size: 1.8rem;
  color: var(--text-color-regular);
  margin-bottom: 1.5rem;
  font-weight: 300;
}

.description {
  font-size: 1.1rem;
  color: var(--text-color-secondary);
  margin-bottom: 3rem;
  line-height: 1.6;
  max-width: 500px;
}

.actions {
  display: flex;
  gap: 20px;
}

.start-btn {
  padding: 12px 30px;
  font-size: 1.1rem;
}

.hero-image {
  flex: 1;
  display: flex;
  justify-content: center;
}

.image-placeholder {
  width: 400px;
  height: 300px;
  background-color: var(--bg-color-overlay);
  border-radius: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: var(--shadow-card);
  border: 1px solid var(--border-color);
}

.features-section {
  padding: 60px 0;
  text-align: center;
}

.section-title {
  font-size: 2.5rem;
  margin-bottom: 50px;
  color: var(--text-color-primary);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
}

.feature-card {
  text-align: left;
  transition: transform 0.3s;
  background-color: var(--bg-color-overlay);
  border-color: var(--border-color);
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
  color: var(--text-color-primary);
}

p {
  color: var(--text-color-regular);
}
</style>
