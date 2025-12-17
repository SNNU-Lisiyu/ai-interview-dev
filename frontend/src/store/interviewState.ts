import { reactive } from 'vue'

export const interviewState = reactive({
  messages: [
    { role: 'ai', content: '您好，我是您的AI面试官。很高兴见到您。请先做一个简单的自我介绍。' }
  ],
  currentStage: 0,
  analysisData: {
    emotion: 60,
    logic: 70,
    speed: 'normal'
  }
})

export const resetInterviewState = () => {
  interviewState.messages = [
    { role: 'ai', content: '您好，我是您的AI面试官。很高兴见到您。请先做一个简单的自我介绍。' }
  ]
  interviewState.currentStage = 0
  interviewState.analysisData = {
    emotion: 60,
    logic: 70,
    speed: 'normal'
  }
}
