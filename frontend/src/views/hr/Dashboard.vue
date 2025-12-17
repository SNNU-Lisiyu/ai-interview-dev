<template>
  <div class="dashboard-container">
    <el-row :gutter="20">
      <el-col :span="6" v-for="(stat, index) in stats" :key="index">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" :style="{ backgroundColor: stat.bgColor }">
              <el-icon :size="24" :color="stat.color"><component :is="stat.icon" /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stat.value }}</div>
              <div class="stat-label">{{ stat.label }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt-20">
      <el-col :span="16">
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="card-header">
              <span>近7天面试趋势</span>
              <el-radio-group v-model="chartPeriod" size="small">
                <el-radio-button label="week">本周</el-radio-button>
                <el-radio-button label="month">本月</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div ref="chartRef" class="chart-container"></div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover" class="activity-card">
          <template #header>
            <div class="card-header">
              <span>待办事项</span>
              <el-tag type="danger" size="small">3</el-tag>
            </div>
          </template>
          <div class="todo-list">
            <div class="todo-item" v-for="(item, index) in todoList" :key="index">
              <el-checkbox v-model="item.done">{{ item.text }}</el-checkbox>
              <span class="todo-time">{{ item.time }}</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts/core'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { LineChart } from 'echarts/charts'
import { UniversalTransition } from 'echarts/features'
import { CanvasRenderer } from 'echarts/renderers'

echarts.use([GridComponent, TooltipComponent, LegendComponent, LineChart, CanvasRenderer, UniversalTransition])

const chartRef = ref<HTMLElement | null>(null)
let chartInstance: echarts.ECharts | null = null
const chartPeriod = ref('week')

const stats = [
  { label: '待处理简历', value: '12', icon: 'User', color: '#409eff', bgColor: 'rgba(64, 158, 255, 0.1)' },
  { label: '今日面试', value: '5', icon: 'Timer', color: '#e6a23c', bgColor: 'rgba(230, 162, 60, 0.1)' },
  { label: '平均得分', value: '86.5', icon: 'TrendCharts', color: '#67c23a', bgColor: 'rgba(103, 194, 58, 0.1)' },
  { label: '录用率', value: '18%', icon: 'Trophy', color: '#f56c6c', bgColor: 'rgba(245, 108, 108, 0.1)' },
]

const todoList = ref([
  { text: '审核张宇的面试报告', time: '10:00', done: false },
  { text: '发布产品经理新职位', time: '14:30', done: false },
  { text: '确认下周面试排期', time: '16:00', done: false },
  { text: '更新面试题库', time: '昨天', done: true },
])

const initChart = () => {
  if (!chartRef.value) return
  
  chartInstance = echarts.init(chartRef.value)
  
  const option = {
    tooltip: {
      trigger: 'axis'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
      axisLine: { lineStyle: { color: '#909399' } }
    },
    yAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: '#909399' } },
      splitLine: { lineStyle: { color: 'rgba(128, 128, 128, 0.1)' } }
    },
    series: [
      {
        name: '面试人数',
        type: 'line',
        smooth: true,
        data: [15, 23, 24, 18, 35, 10, 5],
        itemStyle: { color: '#409eff' },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(64, 158, 255, 0.5)' },
            { offset: 1, color: 'rgba(64, 158, 255, 0.01)' }
          ])
        }
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
.mt-20 {
  margin-top: 20px;
}

.stat-card {
  background-color: var(--bg-color-overlay);
  border: 1px solid var(--border-color);
  color: var(--text-color-primary);
}

.stat-content {
  display: flex;
  align-items: center;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  line-height: 1.2;
}

.stat-label {
  font-size: 12px;
  color: var(--text-color-secondary);
  margin-top: 4px;
}

.chart-card, .activity-card {
  background-color: var(--bg-color-overlay);
  border: 1px solid var(--border-color);
  color: var(--text-color-primary);
  height: 400px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-container {
  height: 320px;
  width: 100%;
}

.todo-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.todo-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border-color);
}

.todo-time {
  font-size: 12px;
  color: var(--text-color-secondary);
}
</style>
