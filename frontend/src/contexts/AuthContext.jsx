import { createContext, useContext } from 'react'

const AuthContext = createContext(null)

function AuthProvider({ children }) {
  const value = {
    user: null,
    isAuthenticated: false,
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
