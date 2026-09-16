import { createContext, useContext, useEffect, useState } from 'react'
import { request } from '../services/api'
import { login as loginRequest } from '../services/auth'

const AuthContext = createContext(null)

function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [session, setSession] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  async function restoreSession() {
    const token = localStorage.getItem('access_token')

    if (!token) {
      setIsLoading(false)
      return
    }

    try {
      const response = await request('/v1/auth/me')

      const userData = response?.data ?? null

      setUser(userData)
      setSession({
        access_token: token,
        token_type: 'bearer',
      })
    } catch {
      localStorage.removeItem('access_token')
      setUser(null)
      setSession(null)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    restoreSession()
  }, [])

  async function login(username, password) {
    const response = await loginRequest(username, password)

    const sessionData = response?.data?.session ?? null
    const userData = response?.data?.user ?? null

    if (sessionData?.access_token) {
      localStorage.setItem('access_token', sessionData.access_token)
    }

    setSession(sessionData)
    setUser(userData)

    return response
  }

  async function logout() {
    try {
      await request('/v1/auth/logout')
    } catch {
      // Clear local authentication state even if logout request fails.
    } finally {
      localStorage.removeItem('access_token')
      setUser(null)
      setSession(null)
    }
  }

  const value = {
    user,
    session,
    isAuthenticated: Boolean(session?.access_token),
    isLoading,
    login,
    logout,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

function useAuth() {
  return useContext(AuthContext)
}

export { AuthProvider, useAuth }