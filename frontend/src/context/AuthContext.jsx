import { createContext, useContext, useState, useCallback, useEffect } from 'react'
import { login as apiLogin, register as apiRegister } from '../services/api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem('token'))
  const [loading, setLoading] = useState(true)

  const login = useCallback(async (email, password) => {
    const data = await apiLogin(email, password)
    setToken(data.access_token)
    localStorage.setItem('token', data.access_token)
    return data
  }, [])

  const register = useCallback(async (userData) => {
    await apiRegister(userData)
    const data = await apiLogin(userData.email, userData.password)
    setToken(data.access_token)
    localStorage.setItem('token', data.access_token)
    return data
  }, [])

  const logout = useCallback(() => {
    setToken(null)
    localStorage.removeItem('token')
  }, [])

  const isAuthenticated = !!token

  useEffect(() => {
    setLoading(false)
  }, [])

  const value = {
    token,
    login,
    register,
    logout,
    isAuthenticated,
    loading,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
