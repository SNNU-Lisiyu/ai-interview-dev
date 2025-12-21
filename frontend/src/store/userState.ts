import { reactive, watch } from 'vue'

export interface UserProfile {
  id: string
  name: string
  password?: string
  role: 'candidate' | 'hr'
  avatar: string
  targetPosition: string
  experience: string
  skills: string
  resumeSummary: string
}

const defaultUser: UserProfile = {
  id: 'user_001',
  name: '没头脑',
  password: '123',
  role: 'candidate',
  avatar: '',
  targetPosition: '产品经理',
  experience: '应届生',
  skills: 'Vue3, TypeScript, 产品设计, 需求分析',
  resumeSummary: '陕西师范大学计算机专业，曾主导"智面星途"项目开发，熟悉敏捷开发流程。'
}

const defaultHR: UserProfile = {
  id: 'user_hr_001',
  name: '不高兴',
  password: '123',
  role: 'hr',
  avatar: '',
  targetPosition: '招聘经理',
  experience: '5年',
  skills: '人才招聘, 团队管理',
  resumeSummary: '资深HRBP'
}

// Load from localStorage or use default
const loadUsers = (): UserProfile[] => {
  const stored = localStorage.getItem('interview_users')
  if (stored) {
    const users = JSON.parse(stored)
    // Ensure default users exist for demo purposes if not present
    if (!users.find((u: UserProfile) => u.id === defaultUser.id)) users.unshift(defaultUser)
    if (!users.find((u: UserProfile) => u.id === defaultHR.id)) users.push(defaultHR)
    return users
  }
  return [defaultUser, defaultHR]
}

const loadCurrentUser = (): UserProfile => {
  const storedId = localStorage.getItem('interview_current_user_id')
  const users = loadUsers()
  if (storedId) {
    const found = users.find(u => u.id === storedId)
    if (found) return found
  }
  return users[0] || defaultUser
}

export const userState = reactive({
  currentUser: loadCurrentUser(),
  users: loadUsers()
})


// Watch for changes to save to localStorage
watch(() => userState.users, (newUsers) => {
  localStorage.setItem('interview_users', JSON.stringify(newUsers))
}, { deep: true })

watch(() => userState.currentUser, (newUser) => {
  localStorage.setItem('interview_current_user_id', newUser.id)
  // Also update the user in the users array
  const index = userState.users.findIndex(u => u.id === newUser.id)
  if (index !== -1) {
    userState.users[index] = newUser
  }
}, { deep: true })

export const switchUser = (userId: string) => {
  const user = userState.users.find(u => u.id === userId)
  if (user) {
    userState.currentUser = user
  }
}

export const addUser = (userInfo: Partial<UserProfile> & { name: string, password?: string, role?: 'candidate' | 'hr' }) => {
  const newUser: UserProfile = {
    id: `user_${Date.now()}`,
    name: userInfo.name,
    password: userInfo.password || '123456',
    role: userInfo.role || 'candidate',
    avatar: '',
    targetPosition: userInfo.targetPosition || '',
    experience: userInfo.experience || '',
    skills: userInfo.skills || '',
    resumeSummary: userInfo.resumeSummary || ''
  }
  userState.users.push(newUser)
  userState.currentUser = newUser
}

export const deleteUser = (userId: string) => {
  if (userState.users.length <= 1) return // Keep at least one user
  
  const index = userState.users.findIndex(u => u.id === userId)
  if (index !== -1) {
    userState.users.splice(index, 1)
    // If deleted current user, switch to the first one
    if (userState.currentUser.id === userId) {
      userState.currentUser = userState.users[0] || defaultUser
    }
  }
}
