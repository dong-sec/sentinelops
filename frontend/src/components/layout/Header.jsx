import { useAuth } from '../../contexts/AuthContext'

function Header() {
  const { user, logout } = useAuth()

  async function handleLogout() {
    await logout()
  }

  return (
    <header className="app-header">
      <div className="header-search">Global Search</div>

      <div className="header-actions">
        <span>HEALTHY</span>
        <span>Notifications</span>

        <div>
          <span>{user?.username ?? 'Current User'}</span>
          <span>{user?.role ?? 'Viewer'}</span>
        </div>

        <button type="button" onClick={handleLogout}>
          Logout
        </button>
      </div>
    </header>
  )
}

export default Header