import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react'
import { api } from '../api/client'

type AuthContextValue = {
  token: string | null
  userEmail: string | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)
const TOKEN_STORAGE_KEY = 'url_shortener_token'
const EMAIL_STORAGE_KEY = 'url_shortener_email'

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(null)
  const [userEmail, setUserEmail] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const savedToken = localStorage.getItem(TOKEN_STORAGE_KEY)
    const savedEmail = localStorage.getItem(EMAIL_STORAGE_KEY)
    if (savedToken) setToken(savedToken)
    if (savedEmail) setUserEmail(savedEmail)
    setIsLoading(false)
  }, [])

  const login = useCallback(async (email: string, password: string) => {
    const response = await api.loginUser(email, password)
    localStorage.setItem(TOKEN_STORAGE_KEY, response.access_token)
    localStorage.setItem(EMAIL_STORAGE_KEY, email)
    setToken(response.access_token)
    setUserEmail(email)
  }, [])

  const register = useCallback(async (email: string, password: string) => {
    await api.registerUser(email, password)
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_STORAGE_KEY)
    localStorage.removeItem(EMAIL_STORAGE_KEY)
    setToken(null)
    setUserEmail(null)
  }, [])

  const value = useMemo<AuthContextValue>(
    () => ({
      token,
      userEmail,
      isAuthenticated: Boolean(token),
      isLoading,
      login,
      register,
      logout,
    }),
    [token, userEmail, isLoading, login, register, logout],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
