import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { useNavigate } from '@tanstack/react-router'
import apiClient from '@/api/client'

interface User {
  id: string
  email: string
  firstName: string
  lastName: string
  role: string
}

interface AuthContextValue {
  isAuthenticated: boolean
  user: User | null
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  isLoading: boolean
  refreshUser: () => Promise<void>
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

interface AuthProviderProps {
  children: ReactNode
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const navigate = useNavigate()
  
  // Initialize auth state on mount
  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('access_token')
      
      if (token) {
        try {
          await refreshUser()
        } catch (error) {
          console.error('Failed to refresh user:', error)
          logout()
        }
      }
      
      setIsLoading(false)
    }
    
    initAuth()
  }, [])
  
  const login = async (email: string, password: string) => {
    try {
      const response = await apiClient.post('/auth/login', {
        email,
        password,
      })
      
      const { accessToken, refreshToken, user: userData } = response.data
      
      // Store tokens
      localStorage.setItem('access_token', accessToken)
      
      if (refreshToken) {
        localStorage.setItem('refresh_token', refreshToken)
      }
      
      // Set user state
      setUser(userData)
      setIsAuthenticated(true)
      
      // Redirect to dashboard or intended route
      navigate({ to: '/dashboard' })
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    }
  }
  
  const logout = () => {
    // Clear tokens
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    
    // Clear state
    setUser(null)
    setIsAuthenticated(false)
    
    // Redirect to login
    navigate({ to: '/login' })
  }
  
  const refreshUser = async () => {
    try {
      const response = await apiClient.get('/auth/me')
      setUser(response.data)
      setIsAuthenticated(true)
    } catch (error) {
      console.error('Failed to fetch user:', error)
      throw error
    }
  }
  
  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        user,
        login,
        logout,
        isLoading,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  
  return context
}