<template>
  <div class="report-container">
    <div class="report-header">
      <h1 class="page-title">面试评测报告</h1>
      <div class="report-meta">
        <span>面试岗位：{{ userState.currentUser.targetPosition }}</span>
        <el-divider direction="vertical" />
        <span>面试时间：{{ new Date().toLocaleDateString() }}</span>
        <el-divider direction="vertical" />
        <span>候选人：{{ userState.currentUser.name }}</span>
      </div>
    </div>

    <div class="score-overview">
      <div class="total-score-card">
        <div class="screen-only">
          <el-progress type="dashboard" :percentage="totalScore" :color="progressColor" :width="180">
            <template #default="{ percentage }">
              <span class="score-value">{{ percentage }}</span>
              <span class="score-label">综合得分</span>
            </template>
          </el-progress>
        </div>
        <div class="print-only total-score-print" :style="{ color: getScoreColor(totalScore) }">
          <span class="print-score-value">{{ totalScore }}</span>
          <span class="print-score-label">综合得分</span>
        </div>
        <div class="score-summary">
          <h3 :style="{ color: getScoreColor(totalScore) }">{{ evaluationTitle }}</h3>
          <p>{{ evaluationDescription }}</p>
        </div>
      </div>
      
      <div class="radar-chart-card">
        <h3 class="screen-only">能力维度分析</h3>
        <div ref="radarChartRef" class="chart-container"></div>
      </div>
    </div>

    <div class="detailed-analysis">
      <h2 class="section-title">详细维度解析</h2>
      <el-row :gutter="24">
        <el-col :xs="24" :sm="12" :md="8" v-for="(item, index) in dimensions" :key="index" style="margin-bottom: 20px;">
          <el-card class="dimension-card" shadow="hover">
            <template #header>
              <div class="dimension-header">
                <span class="dimension-name">{{ item.name }}</span>
                <el-tag :type="item.score >= 80 ? 'success' : item.score >= 60 ? 'warning' : 'danger'" effect="dark">
                  {{ item.score }}分
                </el-tag>
              </div>
            </template>
            <div class="card-content">
              <p class="dimension-desc">{{ item.description }}</p>
              <div class="dimension-suggestion" :style="getSuggestionStyle(item.score)">
                <div class="suggestion-title" :style="{ color: getScoreColor(item.score) }">
                  <el-icon><Edit /></el-icon> 改进建议
                </div>
                <p>{{ item.suggestion }}</p>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <div class="action-area">
      <el-button type="primary" size="large" @click="$router.push('/candidate/home')">返回首页</el-button>
      <el-button size="large" @click="handleExport">导出报告</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import * as echarts from 'echarts/core'
import { RadarChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { Edit } from '@element-plus/icons-vue'
import { userState } from '../store/userState'

echarts.use([TitleComponent, TooltipComponent, LegendComponent, RadarChart, CanvasRenderer])

const radarChartRef = ref<HTMLElement | null>(null)
let chartInstance: echarts.ECharts | null = null
const totalScore = ref(0)

// const colors = [ ... ] // Removed unused colors array

const dimensions = ref<any[]>([])

const evaluationTitle = computed(() => {
  if (totalScore.value >= 80) return '表现优秀'
  if (totalScore.value >= 60) return '表现良好'
  return '基础薄弱'
})

const evaluationDescription = computed(() => {
  if (dimensions.value.length === 0) return ''
  
  // Find highest and lowest dimensions
  const sorted = [...dimensions.value].sort((a, b) => b.score - a.score)
  const highest = sorted[0]
  const lowest = sorted[sorted.length - 1]
  
  if (totalScore.value >= 80) {
    return `您的综合素质超过了 ${totalScore.value}% 的候选人。在${highest.name}方面表现尤为突出，建议保持优势并继续精进。`
  } else if (totalScore.value >= 60) {
    return `您的综合素质超过了 ${totalScore.value}% 的候选人。${highest.name}表现尚可，但${lowest.name}有待加强，建议针对性提升。`
  } else {
    return `您的综合素质超过了 ${totalScore.value}% 的候选人。整体表现有较大提升空间，特别是${lowest.name}方面需要重点补充基础。`
  }
})

const getScoreColor = (score: number) => {
  if (score >= 80) return '#67c23a'
  if (score >= 60) return '#e6a23c'
  return '#f56c6c'
}

const getSuggestionStyle = (score: number) => {
  let colorVar = 'danger'
  if (score >= 80) colorVar = 'success'
  else if (score >= 60) colorVar = 'warning'
  
  return {
    backgroundColor: `var(--el-color-${colorVar}-light-9)`,
    borderLeftColor: `var(--el-color-${colorVar})`
  }
}

const progressColor = (percentage: number) => {
  return getScoreColor(percentage)
}

const initChart = () => {
  if (!radarChartRef.value) return
  
  chartInstance = echarts.init(radarChartRef.value)
  
  const indicators = dimensions.value.map(d => ({
    name: d.name,
    max: 100
  }))

  const option = {
    tooltip: {},
    radar: {
      indicator: indicators.length > 0 ? indicators : [
        { name: '专业知识', max: 100 },
        { name: '逻辑思维', max: 100 },
        { name: '语言表达', max: 100 },
        { name: '抗压能力', max: 100 },
        { name: '岗位匹配', max: 100 }
      ],
      radius: '65%',
      center: ['50%', '50%'],
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
        name: '能力维度',
        type: 'radar',
        data: [
          {
            value: dimensions.value.map(d => d.score),
            name: '候选人能力',
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: 'rgba(64, 158, 255, 0.6)' },
                { offset: 1, color: 'rgba(64, 158, 255, 0.1)' }
              ])
            },
            itemStyle: {
              color: '#409eff'
            },
            lineStyle: {
              width: 3
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

const handleExport = () => {
  window.print()
}

onMounted(() => {
  let savedReport = localStorage.getItem(`interviewReport_${userState.currentUser.id}`)
  
  // Demo data for "没头脑"
  if (!savedReport && userState.currentUser.name === '没头脑') {
    const demoData = {
      score: 78,
      dimensions: [
        { name: "专业知识", score: 85, description: "基础扎实，对Vue3理解深入，能够准确回答核心概念。", suggestion: "建议进一步加强对后端微服务架构的理解，以提升全栈开发能力。" },
        { name: "逻辑思维", score: 75, description: "回答问题条理清晰，但在处理复杂场景时略显犹豫。", suggestion: "可以通过练习算法题和系统设计案例来提升复杂问题的分析能力。" },
        { name: "语言表达", score: 80, description: "表达流畅，自信大方，能够很好地与面试官互动。", suggestion: "注意语速控制，在关键观点上可以适当停顿以增强强调效果。" },
        { name: "抗压能力", score: 70, description: "面对追问时略显紧张，但能够迅速调整状态。", suggestion: "多进行高强度的模拟面试，适应压力环境下的思考与表达。" },
        { name: "岗位匹配", score: 82, description: "技能栈与目标岗位高度匹配，项目经验丰富。", suggestion: "可以补充一些团队管理或敏捷开发的实践经验。" }
      ]
    }
    savedReport = JSON.stringify(demoData)
    localStorage.setItem(`interviewReport_${userState.currentUser.id}`, savedReport)
  }

  if (savedReport) {
    try {
      const data = JSON.parse(savedReport)
      totalScore.value = data.score
      dimensions.value = data.dimensions
    } catch (e) {
      console.error('Failed to parse report data', e)
    }
  } else {
    // Default empty state
    totalScore.value = 0
    dimensions.value = [
      { name: '专业知识', score: 0, description: '暂无数据', suggestion: '请先完成一次模拟面试' },
      { name: '逻辑思维', score: 0, description: '暂无数据', suggestion: '请先完成一次模拟面试' },
      { name: '语言表达', score: 0, description: '暂无数据', suggestion: '请先完成一次模拟面试' },
      { name: '抗压能力', score: 0, description: '暂无数据', suggestion: '请先完成一次模拟面试' },
      { name: '岗位匹配', score: 0, description: '暂无数据', suggestion: '请先完成一次模拟面试' }
    ]
  }

  initChart()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chartInstance?.dispose()
})
</script>

<style scoped>
.report-container {
  max-width: 1000px;
  margin: 0 auto;
  padding-bottom: 40px;
}

.report-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-title {
  font-size: 2rem;
  color: var(--text-color-primary);
  margin-bottom: 15px;
}

.report-meta {
  color: var(--text-color-secondary);
  font-size: 0.9rem;
}

.score-overview {
  display: flex;
  gap: 20px;
  margin-bottom: 40px;
}

.total-score-card, .radar-chart-card {
  flex: 1;
  background: var(--bg-color-overlay);
  border-radius: 12px;
  padding: 30px;
  box-shadow: var(--shadow-card);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--border-color);
}

.score-value {
  display: block;
  font-size: 2.5rem;
  font-weight: bold;
  color: var(--text-color-primary);
}

.score-label {
  font-size: 0.9rem;
  color: var(--text-color-secondary);
}

.score-summary {
  text-align: center;
  margin-top: 20px;
}

.score-summary h3 {
  color: var(--el-color-success);
  margin-bottom: 10px;
}

.score-summary p {
  color: var(--text-color-regular);
  font-size: 0.9rem;
}

.chart-container {
  width: 100%;
  height: 300px;
}

.section-title {
  font-size: 1.5rem;
  margin-bottom: 20px;
  color: var(--text-color-primary);
  border-left: 4px solid var(--el-color-primary);
  padding-left: 10px;
}

.dimension-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: var(--bg-color-overlay);
  border: 1px solid var(--border-color);
  transition: transform 0.3s, box-shadow 0.3s;
}

.dimension-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--el-box-shadow);
}

.dimension-card :deep(.el-card__header) {
  padding: 10px 20px;
  border-bottom: 1px solid var(--border-color-light);
}

.dimension-card :deep(.el-card__body) {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 15px 20px;
}

.dimension-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dimension-name {
  font-size: 16px;
  font-weight: bold;
  color: var(--text-color-primary);
}

.card-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.dimension-desc {
  color: var(--text-color-regular);
  margin-bottom: 20px;
  line-height: 1.6;
  font-size: 14px;
  flex-grow: 1; /* Pushes suggestion to bottom if needed, or just takes space */
}

.dimension-suggestion {
  background-color: var(--el-color-success-light-9);
  padding: 15px;
  border-radius: 8px;
  border-left: 4px solid var(--el-color-success);
}

.suggestion-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: bold;
  color: var(--el-color-success);
  margin-bottom: 8px;
  font-size: 14px;
}

.dimension-suggestion p {
  margin: 0;
  font-size: 13px;
  color: var(--text-color-regular);
  line-height: 1.5;
}

.action-area {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 40px;
}

.print-only {
  display: none;
}
</style>

<style>
@media print {
  .screen-only {
    display: none !important;
  }
  
  .print-only {
    display: block !important;
  }

  .total-score-print {
    text-align: center;
    margin-bottom: 10px;
    display: flex !important;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
  }

  .print-score-value {
    font-size: 48px;
    font-weight: bold;
    line-height: 1;
    margin-bottom: 5px;
  }

  .print-score-label {
    font-size: 14px;
    color: #666;
  }

  @page {
    margin: 10mm;
    size: A4;
  }

  /* Hide layout elements */
  .header,
  .footer,
  .action-area {
    display: none !important;
  }

  /* Reset layout container padding/margins */
  .layout-container,
  .el-container,
  .el-main {
    height: auto !important;
    overflow: visible !important;
    display: block !important;
    padding: 0 !important;
    margin: 0 !important;
  }

  /* Report container adjustments */
  .report-container {
    max-width: 100% !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    box-shadow: none !important;
  }

  /* Ensure background colors are printed */
  body {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
    background-color: white !important;
  }
  
  /* Force light theme variables for print */
  :root {
    --el-color-success-light-9: #f0f9eb !important;
    --el-color-warning-light-9: #fdf6ec !important;
    --el-color-danger-light-9: #fef0f0 !important;
    --el-color-success: #67c23a !important;
    --el-color-warning: #e6a23c !important;
    --el-color-danger: #f56c6c !important;
  }

  /* Adjust cards for print */
  .total-score-card,
  .radar-chart-card,
  .dimension-card {
    box-shadow: none !important;
    border: 1px solid #ddd !important;
    break-inside: avoid;
    page-break-inside: avoid;
  }

  /* Adjust grid layout for print */
  .el-row {
    display: flex !important;
    flex-wrap: wrap !important;
    margin-left: -5px !important;
    margin-right: -5px !important;
  }

  .el-col {
    width: 50% !important;
    flex: 0 0 50% !important;
    max-width: 50% !important;
    margin-bottom: 10px !important;
    padding-left: 5px !important;
    padding-right: 5px !important;
  }
  
  /* Compact spacing for print */
  .report-header {
    margin-bottom: 5px !important;
    padding-bottom: 5px !important;
    border-bottom: 1px solid #eee;
  }
  
  .page-title {
    font-size: 1.2rem !important;
    margin-bottom: 2px !important;
    color: #000 !important;
  }

  .report-meta {
    font-size: 0.7rem !important;
    color: #666 !important;
  }
  
  .score-overview {
    margin-bottom: 10px !important;
    gap: 5px !important;
  }
  
  .total-score-card, .radar-chart-card {
    padding: 5px !important;
    height: 100px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
  }
  
  .radar-chart-card {
    /* width: 80% !important; Removed to fix overflow */
    margin: 0 auto !important;
  }
  
  .chart-container {
    height: 90px !important;
    width: 100% !important;
  }

  /* Scale down progress circle - No longer needed as we hide it */
  /* .total-score-card .el-progress--dashboard {
    transform: scale(0.8);
    margin-bottom: -10px;
  } */
  
  .section-title {
    font-size: 1.1rem !important;
    margin-bottom: 5px !important;
    margin-top: 5px !important;
    color: #000 !important;
    border-left-color: #000 !important;
  }
  
  .dimension-card :deep(.el-card__header) {
    padding: 5px 10px !important;
    background-color: #f9f9f9 !important;
  }
  
  .dimension-card :deep(.el-card__body) {
    padding: 8px 10px !important;
  }
  
  .dimension-desc {
    margin-bottom: 5px !important;
    font-size: 11px !important;
    line-height: 1.4 !important;
    color: #333 !important;
  }
  
  .dimension-suggestion {
    padding: 8px !important;
    margin-top: 5px !important;
  }
  
  .dimension-suggestion p {
    font-size: 11px !important;
    line-height: 1.4 !important;
    color: #333 !important;
  }

  /* Force light theme for print */
  :root, html, body, .report-container {
    --bg-color: #ffffff !important;
    --bg-color-overlay: #ffffff !important;
    --text-color-primary: #000000 !important;
    --text-color-regular: #333333 !important;
    --text-color-secondary: #666666 !important;
    --border-color: #dddddd !important;
    background-color: #ffffff !important;
    color: #000000 !important;
  }

  /* Remove dark mode overrides if any */
  html.dark .report-container {
    background: #ffffff !important;
  }
  
  .dimension-card, .total-score-card, .radar-chart-card {
    background-color: #ffffff !important;
    border: 1px solid #ebeef5 !important;
    color: #000000 !important;
  }
  
  .dimension-suggestion {
    color: #333333 !important;
  }
  
  .dimension-name {
    color: #000000 !important;
    font-size: 13px !important;
  }
  
  .score-label, .score-summary p {
    color: #333333 !important;
  }

  /* Hide scrollbars */
  ::-webkit-scrollbar {
    display: none;
  }
}
</style>
