<template>
  <div class="detail-container">
    <div class="detail-header">
      <div class="header-left">
        <el-button icon="ArrowLeft" circle @click="$router.back()" class="back-btn" />
        <div class="candidate-title">
          <h2>张宇 - 产品经理</h2>
          <el-tag type="warning">待决策</el-tag>
        </div>
      </div>
      <div class="header-right">
        <el-button type="danger" plain @click="handleReject">淘汰</el-button>
        <el-button type="primary" @click="handlePass">通过面试</el-button>
      </div>
    </div>

    <el-row :gutter="20" class="main-body">
      <!-- Left Column: Video & Transcript -->
      <el-col :span="10">
        <el-card shadow="never" class="video-card">
          <template #header>
            <div class="card-header">
              <span>面试回放</span>
            </div>
          </template>
          <div class="video-placeholder">
            <el-icon :size="48" color="#909399"><VideoPlay /></el-icon>
            <span>面试录像文件</span>
          </div>
          <div class="video-controls">
            <el-slider v-model="videoProgress" :format-tooltip="formatTime" />
            <div class="time-display">00:15:30 / 00:45:00</div>
          </div>
        </el-card>

        <el-card shadow="never" class="transcript-card">
          <template #header>
            <div class="card-header">
              <span>对话实录</span>
              <el-input v-model="searchText" placeholder="搜索关键词" size="small" style="width: 150px" prefix-icon="Search" />
            </div>
          </template>
          <div class="transcript-list">
            <div v-for="(item, index) in transcript" :key="index" class="transcript-item" :class="item.role">
              <div class="role-label">{{ item.role === 'ai' ? '面试官' : '候选人' }}</div>
              <div class="content">{{ item.text }}</div>
              <div class="timestamp">{{ item.time }}</div>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- Right Column: Evaluation Report -->
      <el-col :span="14">
        <el-card shadow="never" class="report-card">
          <div class="score-overview">
            <div class="total-score">
              <el-progress type="dashboard" :percentage="85" :color="colors" :width="150">
                <template #default="{ percentage }">
                  <span class="score-value">{{ percentage }}</span>
                  <span class="score-label">综合得分</span>
                </template>
              </el-progress>
            </div>
            <div class="radar-chart">
              <div ref="radarChartRef" class="chart-container"></div>
            </div>
          </div>

          <el-divider content-position="left">详细维度解析</el-divider>

          <div class="dimensions-list">
            <div v-for="(item, index) in dimensions" :key="index" class="dimension-item">
              <div class="dim-header">
                <span class="dim-name">{{ item.name }}</span>
                <span class="dim-score" :class="getScoreClass(item.score)">{{ item.score }}分</span>
              </div>
              <el-progress :percentage="item.score" :color="getScoreColor(item.score)" :show-text="false" stroke-width="6" />
              <p class="dim-desc">{{ item.description }}</p>
              <div class="ai-insight">
                <el-icon color="#409eff"><Aim /></el-icon>
                <span>AI洞察：{{ item.insight }}</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import * as echarts from 'echarts/core'
import { RadarChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

echarts.use([TitleComponent, TooltipComponent, LegendComponent, RadarChart, CanvasRenderer])

const videoProgress = ref(34)
const searchText = ref('')
const radarChartRef = ref<HTMLElement | null>(null)
let chartInstance: echarts.ECharts | null = null

const colors = [
  { color: '#f56c6c', percentage: 20 },
  { color: '#e6a23c', percentage: 40 },
  { color: '#5cb87a', percentage: 60 },
  { color: '#1989fa', percentage: 80 },
  { color: '#6f7ad3', percentage: 100 },
]

const transcript = ref([
  { role: 'ai', text: '请您简单介绍一下自己，以及为什么应聘这个岗位？', time: '00:00:15' },
  { role: 'user', text: '面试官好，我叫张宇，有3年产品经理经验。我对应聘这个岗位非常感兴趣，因为...', time: '00:00:25' },
  { role: 'ai', text: '您提到的项目中，最大的挑战是什么？您是如何解决的？', time: '00:02:10' },
  { role: 'user', text: '最大的挑战是跨部门沟通。当时研发资源紧张，我通过...', time: '00:02:20' },
  { role: 'ai', text: '如果遇到需求变更，您通常会怎么处理？', time: '00:05:30' },
  { role: 'user', text: '首先我会评估变更的影响范围，然后...', time: '00:05:40' },
])

const dimensions = ref([
  { 
    name: '专业知识', 
    score: 82, 
    description: '基础理论扎实，熟悉敏捷开发流程。',
    insight: '候选人对竞品分析的方法论掌握较好，但在数据埋点方面略显生疏。'
  },
  { 
    name: '逻辑思维', 
    score: 88, 
    description: '回答条理清晰，具备结构化思维。',
    insight: '在回答"需求变更"问题时，展现了优秀的优先级判断能力。'
  },
  { 
    name: '语言表达', 
    score: 90, 
    description: '表达流畅，富有感染力。',
    insight: '语速适中，用词准确，无明显口头禅。'
  },
  { 
    name: '抗压能力', 
    score: 75, 
    description: '面对追问略显紧张。',
    insight: '在被问及项目失败经历时，微表情显示出短暂的慌乱，但迅速调整了状态。'
  },
  { 
    name: '岗位匹配', 
    score: 85, 
    description: '特质与岗位高度契合。',
    insight: '候选人的职业规划与公司发展方向一致。'
  }
])

const formatTime = (_val: number) => {
  return '00:15:30' // Mock
}

const getScoreClass = (score: number) => {
  if (score >= 90) return 'text-success'
  if (score >= 80) return 'text-primary'
  return 'text-warning'
}

const getScoreColor = (score: number) => {
  if (score >= 90) return '#67c23a'
  if (score >= 80) return '#409eff'
  return '#e6a23c'
}

const handlePass = () => {
  ElMessageBox.confirm('确定录用该候选人吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'success'
  }).then(() => {
    ElMessage.success('已发送录用通知')
  })
}

const handleReject = () => {
  ElMessageBox.confirm('确定淘汰该候选人吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    ElMessage.info('已淘汰')
  })
}

const initChart = () => {
  if (!radarChartRef.value) return
  
  chartInstance = echarts.init(radarChartRef.value)
  
  const option = {
    radar: {
      indicator: [
        { name: '专业知识', max: 100 },
        { name: '逻辑思维', max: 100 },
        { name: '语言表达', max: 100 },
        { name: '抗压能力', max: 100 },
        { name: '岗位匹配', max: 100 }
      ],
      radius: '65%',
      splitArea: {
        areaStyle: {
          color: ['rgba(128, 128, 128, 0.05)', 'rgba(128, 128, 128, 0.1)']
        }
      },
      axisName: {
        color: '#909399',
        fontWeight: 'bold'
      }
    },
    series: [
      {
        type: 'radar',
        data: [
          {
            value: [82, 88, 90, 75, 85],
            name: '候选人能力',
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: 'rgba(64, 158, 255, 0.6)' },
                { offset: 1, color: 'rgba(64, 158, 255, 0.1)' }
              ])
            },
            itemStyle: {
              color: '#409eff'
            }
          }
        ]
      }
    ]
  }
  
  chartInstance.setOption(option)
}

const handleResize = () => {
  chartInstance?.resize()
}

onMounted(() => {
  initChart()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chartInstance?.dispose()
})
</script>

<style scoped>
.detail-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--bg-color-overlay);
  padding: 15px 20px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.candidate-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.candidate-title h2 {
  margin: 0;
  font-size: 18px;
  color: var(--text-color-primary);
}

.main-body {
  flex: 1;
}

.video-card, .transcript-card, .report-card {
  background-color: var(--bg-color-overlay);
  border: 1px solid var(--border-color);
  margin-bottom: 20px;
}

.video-placeholder {
  height: 240px;
  background-color: #000;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #909399;
  gap: 10px;
  border-radius: 4px;
}

.video-controls {
  margin-top: 15px;
  display: flex;
  align-items: center;
  gap: 15px;
}

.time-display {
  font-size: 12px;
  color: var(--text-color-secondary);
  width: 120px;
  text-align: right;
}

.transcript-list {
  height: 300px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding-right: 10px;
}

.transcript-item {
  padding: 10px;
  border-radius: 8px;
  background-color: var(--bg-color);
  font-size: 14px;
}

.transcript-item.ai {
  border-left: 3px solid var(--el-color-primary);
}

.transcript-item.user {
  border-left: 3px solid var(--el-color-success);
}

.role-label {
  font-size: 12px;
  color: var(--text-color-secondary);
  margin-bottom: 4px;
}

.content {
  color: var(--text-color-primary);
  line-height: 1.5;
}

.timestamp {
  font-size: 12px;
  color: var(--text-color-secondary);
  text-align: right;
  margin-top: 4px;
}

.score-overview {
  display: flex;
  align-items: center;
  justify-content: space-around;
  margin-bottom: 20px;
}

.total-score {
  text-align: center;
}

.score-value {
  display: block;
  font-size: 28px;
  font-weight: bold;
  color: var(--text-color-primary);
}

.score-label {
  font-size: 12px;
  color: var(--text-color-secondary);
}

.chart-container {
  width: 300px;
  height: 250px;
}

.dimensions-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 20px;
}

.dimension-item {
  padding: 15px;
  background-color: var(--bg-color);
  border-radius: 8px;
}

.dim-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.dim-name {
  font-weight: bold;
  color: var(--text-color-primary);
}

.dim-desc {
  font-size: 13px;
  color: var(--text-color-regular);
  margin: 8px 0;
}

.ai-insight {
  display: flex;
  align-items: flex-start;
  gap: 5px;
  font-size: 13px;
  color: var(--text-color-secondary);
  background-color: rgba(64, 158, 255, 0.1);
  padding: 8px;
  border-radius: 4px;
}

.text-success { color: var(--el-color-success); }
.text-primary { color: var(--el-color-primary); }
.text-warning { color: var(--el-color-warning); }
</style>
