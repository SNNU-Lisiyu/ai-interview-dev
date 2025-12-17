<template>
  <div class="interview-room">
    <div class="video-area">
      <div class="interviewer-video">
        <!-- Main User Video Area -->
        <div class="video-wrapper main-video">
          <video ref="userVideoRef" autoplay playsinline muted class="real-video"></video>
          <!-- Removed faceCanvasRef -->
          <div class="video-overlay" v-if="!cameraActive">
            <el-icon :size="64" color="#909399"><Camera /></el-icon>
            <p style="margin-top: 15px; font-size: 18px; color: #909399;">摄像头未开启</p>
          </div>
        </div>
        
        <!-- Real-time Analysis HUD -->
        <div class="analysis-hud" v-if="isListening || isProcessing">
          <div class="hud-title">
            <el-icon><DataLine /></el-icon> 实时分析引擎
          </div>
          <div class="hud-item">
            <span class="label">情绪效价</span>
            <el-progress :percentage="interviewState.analysisData.emotion" :color="emotionColor" :stroke-width="6" />
          </div>
          <div class="hud-item">
            <span class="label">逻辑连贯</span>
            <el-progress :percentage="interviewState.analysisData.logic" color="#e6a23c" :stroke-width="6" />
          </div>
          <div class="hud-item">
            <span class="label">语速监测</span>
            <div class="speed-indicator">
              <span :class="{ active: interviewState.analysisData.speed === 'slow' }">慢</span>
              <span :class="{ active: interviewState.analysisData.speed === 'normal' }">中</span>
              <span :class="{ active: interviewState.analysisData.speed === 'fast' }">快</span>
            </div>
          </div>
          <div class="hud-graph">
            <!-- Simulated Waveform -->
            <div class="bar" v-for="n in 10" :key="n" :style="{ height: Math.random() * 100 + '%', animationDelay: n * 0.1 + 's' }"></div>
          </div>
        </div>

        <!-- Floating AI Avatar -->
        <div class="ai-video-floating">
          <div class="video-placeholder" :style="{ backgroundImage: `url(${aiAvatar})` }">
            <div class="ai-label-badge">AI面试官</div>
            <div class="wave-animation" v-if="isSpeaking">
              <span></span><span></span><span></span><span></span><span></span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="interaction-area">
      <div class="chat-history" ref="chatHistoryRef">
        <transition-group name="message-fade">
          <div v-for="(msg, index) in interviewState.messages" :key="index" :class="['message', msg.role]">
            <div class="avatar">
              <el-avatar :icon="msg.role === 'ai' ? 'UserFilled' : 'User'" :size="36" :class="msg.role" />
            </div>
            <div class="content">
              <p>{{ msg.content }}</p>
            </div>
          </div>
        </transition-group>
      </div>
      
      <div class="controls">
        <div class="status-bar">
          <span v-if="isListening" class="status-text listening">
            <el-icon class="is-loading"><Microphone /></el-icon> 正在倾听...
          </span>
          <span v-else-if="isProcessing" class="status-text processing">
            <el-icon class="is-loading"><Loading /></el-icon> 思考中...
          </span>
          <span v-else class="status-text ready">请回答问题</span>
          
          <div class="voice-selector">
            <el-select v-model="selectedVoice" placeholder="选择音色" size="small" style="width: 140px;">
              <template #prefix>
                <el-icon><Setting /></el-icon>
              </template>
              <el-option
                v-for="item in ttsVoices"
                :key="item.value"
                :label="item.name"
                :value="item.value"
              />
            </el-select>
          </div>
        </div>
        <div class="action-buttons">
          <el-button type="warning" circle size="large" @click="handleReset">
            <el-icon><RefreshRight /></el-icon>
          </el-button>
          <el-button type="primary" circle size="large" class="mic-btn" :class="{ active: isListening }" @click="toggleMic">
            <el-icon><Microphone /></el-icon>
          </el-button>
          <el-button 
            type="success" 
            :circle="!isInterviewFinished" 
            size="large" 
            @click="isInterviewFinished ? goToReport() : submitAnswer()" 
            :disabled="!isInterviewFinished && !currentInput"
          >
            <span v-if="isInterviewFinished">查看报告</span>
            <el-icon v-else><Check /></el-icon>
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Camera, Microphone, Check, Loading, DataLine, RefreshRight, Setting } from '@element-plus/icons-vue'
import { interviewState, resetInterviewState } from '../store/interviewState'
import aiAvatar from '../assets/ai_interviewer.png'
import { userState } from '../store/userState'
import { IflytekClient, IflytekTTSClient } from '../utils/iflytek'
import { ElMessage } from 'element-plus'

// AI Avatar is imported from assets
// const aiAvatar = 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'

const router = useRouter()
const isSpeaking = ref(false)
const isListening = ref(false)
const isProcessing = ref(false)
const currentInput = ref('')
const userVideoRef = ref<HTMLVideoElement | null>(null)
// const faceCanvasRef = ref<HTMLCanvasElement | null>(null)

const ttsVoices = [
  { name: '讯飞小燕 (女声)', value: 'x4_xiaoyan' },
  { name: '讯飞小露 (女声)', value: 'x4_yezi' },
  { name: '讯飞许久 (男声)', value: 'aisjiuxu' },
  { name: '讯飞小婧 (女声)', value: 'aisjinger' },
  { name: '讯飞许小宝 (童声)', value: 'aisbabyxu' }
]
const selectedVoice = ref('x4_xiaoyan')

const goToReport = () => {
  router.push('/candidate/report')
}
const chatHistoryRef = ref<HTMLElement | null>(null)
const cameraActive = ref(false)
const isInterviewFinished = ref(false)
const voices = ref<SpeechSynthesisVoice[]>([])
let stream: MediaStream | null = null
let recognition: any = null
let ttsClient: IflytekTTSClient | null = null

// Interview Logic State
const API_URL = '/api/deepseek/chat/completions'

const callDeepSeek = async (history: any[]) => {
  try {
    const apiMessages = history.map(msg => ({
      role: msg.role === 'ai' ? 'assistant' : 'user',
      content: msg.content
    }))

    const user = userState.currentUser
    const systemPrompt = `你是一位专业、严谨但亲切的AI面试官。正在面试一位${user.targetPosition}候选人。
候选人信息：
姓名：${user.name}
工作经验：${user.experience}
核心技能：${user.skills}
简历简介：${user.resumeSummary}

请根据候选人的简历和目标岗位进行针对性提问。每次只问一个问题。问题要简短有力。请不要一次性问多个问题。

当面试进行到第5-8个问题，或者你认为已经可以评价候选人时，请结束面试。

【评分严格性要求】
1. 评分必须完全基于**刚才的实际对话内容**，严禁随机打分或给高分。
2. 如果候选人回答简短（如只回答"是"、"否"、"不知道"）、敷衍或缺乏深度，**总分和各维度分数不得超过60分**。
3. 只有当候选人回答逻辑清晰、案例详实且展现出深厚的专业功底时，才能给予80分以上的高分。
4. 请在"description"中引用候选人的具体回答作为评价依据。

结束面试时，请**只**返回JSON格式的最终评价，**严禁**包含任何开场白、结束语、Markdown标记（如 \`\`\`json）或额外的换行符。
{"isEnd": true, "closingMessage": "面试结束的感谢语...", "totalScore": 0-100, "dimensions": [{"name": "专业知识", "score": 0-100, "description": "基于对话的评价", "suggestion": "具体的改进建议"}, {"name": "逻辑思维", "score": 0-100, "description": "基于对话的评价", "suggestion": "具体的改进建议"}, {"name": "语言表达", "score": 0-100, "description": "基于对话的评价", "suggestion": "具体的改进建议"}, {"name": "抗压能力", "score": 0-100, "description": "基于对话的评价", "suggestion": "具体的改进建议"}, {"name": "岗位匹配", "score": 0-100, "description": "基于对话的评价", "suggestion": "具体的改进建议"}]}
如果面试继续，请直接输出下一个问题的纯文本。`

    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'deepseek-chat',
        messages: [
          { role: 'system', content: systemPrompt },
          ...apiMessages
        ],
        temperature: 0.7,
        max_tokens: 500
      })
    })
    
    if (!response.ok) {
      throw new Error(`API call failed: ${response.statusText}`)
    }

    const data = await response.json()
    return data.choices[0].message.content
  } catch (error) {
    console.error('API Error:', error)
    return '抱歉，网络连接似乎有点问题，请您继续回答或稍等片刻。'
  }
}

// Simulated Analysis Data
let analysisInterval: any = null

const emotionColor = computed(() => {
  if (interviewState.analysisData.emotion > 80) return '#67c23a'
  if (interviewState.analysisData.emotion > 50) return '#409eff'
  return '#e6a23c'
})

const startAnalysisSimulation = () => {
  analysisInterval = setInterval(() => {
    interviewState.analysisData.emotion = Math.floor(Math.random() * 40) + 50 // 50-90
    interviewState.analysisData.logic = Math.floor(Math.random() * 30) + 60 // 60-90
    const speeds = ['slow', 'normal', 'fast']
    interviewState.analysisData.speed = speeds[Math.floor(Math.random() * 3)] || 'normal'
  }, 1000)
}

const stopAnalysisSimulation = () => {
  if (analysisInterval) clearInterval(analysisInterval)
}

// Removed startFaceTracking function as requested

const initCamera = async () => {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false })
    if (userVideoRef.value) {
      userVideoRef.value.srcObject = stream
      cameraActive.value = true
      // startFaceTracking() // Removed face tracking overlay
    }
  } catch (err) {
    console.error("无法访问摄像头:", err)
  }
}

const initSpeech = () => {
  // Initialize Voices
  const loadVoices = () => {
    voices.value = window.speechSynthesis.getVoices()
  }
  if (window.speechSynthesis.onvoiceschanged !== undefined) {
    window.speechSynthesis.onvoiceschanged = loadVoices
  }
  loadVoices()

  // Initialize Speech Recognition (iFlyTek)
  recognition = new IflytekClient()
  
  recognition.onTextChange = (text: string, isFinal: boolean) => {
    if (text) {
      // iFlyTek returns partial text or final text. 
      // Since we don't have "interim" vs "final" accumulation logic easily without complex diffing,
      // and the simple client I wrote just emits text segments.
      // If isFinal is true, it's a segment.
      // If isFinal is false, it might be partial.
      // My IflytekClient implementation emits text.
      // Let's assume it emits the full text of the current sentence or segment.
      // Actually, my implementation in `iflytek.ts` emits `text` from `result.text`.
      // If `pgs` is enabled, it might be complex.
      // But let's just append for now.
      
      // Wait, if I just append, I might get duplicates if I don't handle partials correctly.
      // But my `IflytekClient` implementation:
      // `this.onTextChange(text, isFinal);`
      // And `text` comes from `decodeText`.
      // If `status` is 2 (final), it's definitely a committed segment.
      // If `status` is 0 or 1, it's partial.
      
      // For simplicity in this integration:
      // If it's a final result (isFinal=true), append to currentInput.
      // If it's partial, maybe show it?
      // But `currentInput` is v-model.
      
      // Let's just append if isFinal is true for now to be safe.
      if (isFinal) {
        currentInput.value += text
      }
    }
  }

  recognition.onStart = () => { 
    isListening.value = true 
    startAnalysisSimulation()
  }
  
  recognition.onStop = () => { 
    isListening.value = false 
    stopAnalysisSimulation()
    // Auto submit if we have input and it was a voice session ending
    if (currentInput.value.trim()) {
      submitAnswer()
    }
  }
  
  recognition.onError = (error: any) => { 
    console.error('Speech error:', error)
    isListening.value = false 
    stopAnalysisSimulation()
    // Show detailed error message
    const msg = error instanceof Event ? '连接失败' : (error.message || error)
    ElMessage.error(`语音识别出错: ${msg}`)
  }

  // Speak initial message if history is empty or just started
  if (interviewState.messages.length === 1 && interviewState.messages[0]) {
    speak(interviewState.messages[0].content)
  }
}

const speak = (text: string) => {
  if (!ttsClient) {
    ttsClient = new IflytekTTSClient()
    ttsClient.onStart = () => { isSpeaking.value = true }
    ttsClient.onStop = () => { isSpeaking.value = false }
    ttsClient.onError = (err) => { 
      console.error(err)
      isSpeaking.value = false 
      ElMessage.error('语音合成出错')
    }
  }
  
  // Stop previous speech if any
  ttsClient.stop()
  
  ttsClient.speak(text, selectedVoice.value)
}

const scrollToBottom = async () => {
  await nextTick()
  if (chatHistoryRef.value) {
    chatHistoryRef.value.scrollTop = chatHistoryRef.value.scrollHeight
  }
}

const toggleMic = () => {
  if (!recognition) {
    // Fallback for browsers without support
    isListening.value = !isListening.value
    if (isListening.value) {
      setTimeout(() => {
        currentInput.value = "面试官您好，我叫张宇，来自陕西师范大学..."
        isListening.value = false
        submitAnswer() // Auto submit for fallback
      }, 2000)
    }
    return
  }

  if (isListening.value) {
    recognition.stop()
  } else {
    recognition.start()
  }
}

const handleReset = () => {
  resetInterviewState()
  currentInput.value = ''
  if (recognition) recognition.stop()
  if (ttsClient) ttsClient.stop()
  if (interviewState.messages[0]) {
    speak(interviewState.messages[0].content)
  }
}

const submitAnswer = async () => {
  if (!currentInput.value) return
  
  if (isListening.value && recognition) {
    recognition.stop()
  }

  interviewState.messages.push({ role: 'user', content: currentInput.value })
  currentInput.value = ''
  isProcessing.value = true
  scrollToBottom()
  
  try {
    const aiResponse = await callDeepSeek(interviewState.messages)
    isProcessing.value = false
    
    // Try to extract JSON from response (handling potential Markdown wrappers)
    let jsonResponse = null
    try {
      // First try direct parse
      jsonResponse = JSON.parse(aiResponse)
    } catch (e) {
      // If failed, try to find JSON block
      // 1. Try regex for code blocks
      const codeBlockMatch = aiResponse.match(/```json\s*([\s\S]*?)\s*```/)
      if (codeBlockMatch) {
        try {
          jsonResponse = JSON.parse(codeBlockMatch[1])
        } catch (e2) { console.warn('Failed to parse code block JSON', e2) }
      }

      // 2. If still null, try to find the outermost braces manually (handles text before/after)
      if (!jsonResponse) {
        const start = aiResponse.indexOf('{')
        const end = aiResponse.lastIndexOf('}')
        if (start !== -1 && end !== -1 && end > start) {
          const potentialJson = aiResponse.substring(start, end + 1)
          try {
            jsonResponse = JSON.parse(potentialJson)
          } catch (e3) { 
            console.warn('Failed to parse substring JSON', e3)
            // Last resort: try to clean up newlines which might be breaking the JSON
            try {
               // Replace real newlines with space to maintain JSON structure if it was just formatting
               // This is risky but better than failing if the AI just added line breaks for readability inside a string
               const cleaned = potentialJson.replace(/\n/g, ' ')
               jsonResponse = JSON.parse(cleaned)
            } catch (e4) {}
          }
        }
      }
    }

    if (jsonResponse && jsonResponse.isEnd) {
      interviewState.messages.push({ role: 'ai', content: jsonResponse.closingMessage })
      speak(jsonResponse.closingMessage)
      scrollToBottom()
      
      // Save report data
      const finalReport = {
        score: jsonResponse.totalScore,
        dimensions: jsonResponse.dimensions,
        userId: userState.currentUser.id,
        timestamp: Date.now()
      }
      localStorage.setItem(`interviewReport_${userState.currentUser.id}`, JSON.stringify(finalReport))
      isInterviewFinished.value = true
      return
    }

    // If not end or not JSON, display as normal message
    interviewState.messages.push({ role: 'ai', content: aiResponse })
    speak(aiResponse)
    scrollToBottom()
    
    interviewState.currentStage++
  } catch (e) {
    isProcessing.value = false
    console.error(e)
  }
}

onMounted(() => {
  // Reset state when entering the interview room to ensure fresh start for new user
  resetInterviewState()
  isInterviewFinished.value = false
  
  initCamera()
  initSpeech()
})

onUnmounted(() => {
  cameraActive.value = false
  if (stream) {
    stream.getTracks().forEach(track => track.stop())
  }
  window.speechSynthesis.cancel()
  if (recognition) recognition.stop()
})
</script>

<style scoped>
.interview-room {
  display: flex;
  height: calc(100vh - 160px); /* Adjusted to fit in one page without scrolling */
  gap: 20px;
  padding: 0; /* Removed internal padding */
  box-sizing: border-box;
  max-width: 1360px; /* Slightly wider layout */
  margin: 0 auto; /* Center horizontally */
}

.video-area {
  flex: 6; /* Give even more space to video */
  display: flex;
  flex-direction: column;
  position: relative;
  background-color: #000;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.interviewer-video {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

.video-placeholder {
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  position: relative;
}

.ai-label-badge {
  position: absolute;
  bottom: 20px;
  left: 20px;
  background: rgba(0, 0, 0, 0.6);
  color: #fff;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 14px;
  backdrop-filter: blur(4px);
}

/* Floating AI Avatar Styles */
.ai-video-floating {
  position: absolute;
  bottom: 20px;
  right: 20px;
  width: 240px;
  aspect-ratio: 16/9;
  background-color: #333;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
  border: 2px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  z-index: 10;
}

.ai-video-floating:hover {
  transform: scale(1.05);
  border-color: #409eff;
}

.video-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
}

.real-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transform: scaleX(-1);
}

.video-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: #fff;
  background-color: #2c2c2c;
  font-size: 0.9rem;
}

.face-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 10;
}

/* Analysis HUD Styles */
.analysis-hud {
  position: absolute;
  top: 20px;
  left: 20px;
  width: 200px;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 15px;
  border: 1px solid rgba(64, 158, 255, 0.3);
  color: #fff;
  z-index: 20;
  animation: slideIn 0.5s ease;
}

@keyframes slideIn {
  from { opacity: 0; transform: translateX(-20px); }
  to { opacity: 1; transform: translateX(0); }
}

.hud-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: bold;
  color: var(--el-color-primary);
  margin-bottom: 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 8px;
}

.hud-item {
  margin-bottom: 12px;
}

.hud-item .label {
  display: block;
  font-size: 12px;
  color: #ccc;
  margin-bottom: 4px;
}

.speed-indicator {
  display: flex;
  justify-content: space-between;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  padding: 2px;
}

.speed-indicator span {
  flex: 1;
  text-align: center;
  font-size: 12px;
  padding: 2px 0
}

.speed-indicator span.active {
  background: var(--el-color-primary);
  color: #fff;
}

.hud-graph {
  height: 40px;
  display: flex;
  align-items: flex-end;
  gap: 2px;
  margin-top: 15px;
}

.hud-graph .bar {
  flex: 1;
  background: var(--el-color-primary);
  opacity: 0.7;
  animation: graphWave 0.5s infinite ease-in-out alternate;
}

@keyframes graphWave {
  from { height: 20%; }
  to { height: 100%; }
}

.interaction-area {
  flex: 1.2; /* Slightly wider chat */
  min-width: 380px;
  background-color: var(--bg-color-overlay);
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow-card);
  border: 1px solid var(--border-color);
  overflow: hidden;
}

.chat-history {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
  background-color: var(--bg-color);
}

/* Message Animations */
.message-fade-enter-active,
.message-fade-leave-active {
  transition: all 0.5s ease;
}
.message-fade-enter-from {
  opacity: 0;
  transform: translateY(20px);
}
.message-fade-leave-to {
  opacity: 0;
}

.message {
  display: flex;
  gap: 12px;
  max-width: 90%;
}

.message.ai {
  align-self: flex-start;
}

.message.user {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.message .content {
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 15px;
  line-height: 1.6;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  position: relative;
}

.message.ai .content {
  background-color: var(--bg-color-overlay);
  color: var(--text-color-primary);
  border-top-left-radius: 2px;
  border: 1px solid var(--border-color);
}

.message.user .content {
  background-color: var(--el-color-primary);
  color: #fff;
  border-top-right-radius: 2px;
}

.controls {
  padding: 20px;
  background-color: var(--bg-color-overlay);
  border-top: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.status-bar {
  height: 32px;
  font-size: 14px;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  width: 100%;
  position: relative;
}

.voice-selector {
  position: absolute;
  right: 0;
}

.status-text {
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-text.listening { color: var(--el-color-primary); }
.status-text.processing { color: #e6a23c; }
.status-text.ready { color: var(--text-color-secondary); }

.action-buttons {
  display: flex;
  gap: 30px;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.mic-btn {
  width: 64px;
  height: 64px;
  font-size: 28px;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.mic-btn:hover {
  transform: scale(1.05);
}

.mic-btn.active {
  background-color: #f56c6c;
  border-color: #f56c6c;
  transform: scale(1.1);
  box-shadow: 0 0 20px rgba(245, 108, 108, 0.4);
}

.wave-animation {
  position: absolute;
  top: 10px;
  left: 10px;
  display: flex;
  gap: 4px;
  height: 24px;
  align-items: center;
  z-index: 5;
}

.wave-animation span {
  width: 4px;
  height: 100%;
  background-color: #409eff;
  border-radius: 2px;
  animation: wave 1s infinite ease-in-out;
}

.wave-animation span:nth-child(1) { animation-delay: 0.0s; }
.wave-animation span:nth-child(2) { animation-delay: 0.1s; }
.wave-animation span:nth-child(3) { animation-delay: 0.2s; }
.wave-animation span:nth-child(4) { animation-delay: 0.3s; }
.wave-animation span:nth-child(5) { animation-delay: 0.4s; }

@keyframes wave {
  0%, 100% { height: 20%; opacity: 0.5; }
  50% { height: 100%; opacity: 1; }
}

/* Scrollbar Styling */
.chat-history::-webkit-scrollbar {
  width: 6px;
}
.chat-history::-webkit-scrollbar-track {
  background: transparent;
}
.chat-history::-webkit-scrollbar-thumb {
  background-color: #dcdfe6;
  border-radius: 3px;
}
</style>
