/**
 * 示例 Pinia Store: useUserStore
 * 展示 Setup Store 的最佳实践
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// 类型定义
interface User {
  id: number
  name: string
  email: string
  avatar?: string
}

interface LoginCredentials {
  email: string
  password: string
}

// 模拟 API
const mockApi = {
  login: async (credentials: LoginCredentials): Promise<{ user: User; token: string }> => {
    await new Promise(resolve => setTimeout(resolve, 1000))
    return {
      user: { id: 1, name: 'John Doe', email: credentials.email },
      token: 'mock-jwt-token'
    }
  },
  logout: async () => {
    await new Promise(resolve => setTimeout(resolve, 500))
  }
}

// SSR/测试环境下避免直接访问 localStorage
const canUseStorage = () => typeof window !== 'undefined' && !!window.localStorage

export const useUserStore = defineStore('user', () => {
  // ========== State ==========
  const user = ref<User | null>(null)
  const token = ref('')
  const loading = ref(false)
  const error = ref<string | null>(null)

  // ========== Getters ==========
  const isLoggedIn = computed(() => !!token.value)
  
  const displayName = computed(() => 
    user.value?.name ?? 'Guest'
  )
  
  const userInitials = computed(() => {
    if (!user.value?.name) return '?'
    return user.value.name
      .split(' ')
      .map(n => n[0])
      .join('')
      .toUpperCase()
  })

  // ========== Actions ==========
  async function login(credentials: LoginCredentials) {
    loading.value = true
    error.value = null
    
    try {
      const res = await mockApi.login(credentials)
      user.value = res.user
      token.value = res.token
      
      // 持久化 token
      if (canUseStorage()) {
        localStorage.setItem('auth_token', res.token)
      }
    } catch (e) {
      error.value = e instanceof Error ? e.message : '登录失败'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    loading.value = true
    
    try {
      await mockApi.logout()
    } finally {
      user.value = null
      token.value = ''
      if (canUseStorage()) {
        localStorage.removeItem('auth_token')
      }
      loading.value = false
    }
  }

  function initFromStorage() {
    if (canUseStorage()) {
      const savedToken = localStorage.getItem('auth_token')
      if (savedToken) {
        token.value = savedToken
        // 这里应该调用 API 获取用户信息
      }
    }
  }

  // ========== 导出 ==========
  return {
    // State
    user,
    token,
    loading,
    error,
    // Getters
    isLoggedIn,
    displayName,
    userInitials,
    // Actions
    login,
    logout,
    initFromStorage
  }
})
