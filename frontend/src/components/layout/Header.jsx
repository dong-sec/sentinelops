function Header() {
  return (
    <header className="app-header">
      <div className="header-search">Global Search</div>

      <div className="header-actions">
        <span>HEALTHY</span>
        <span>Notifications</span>
        <span>Current User</span>
        <button type="button">Logout</button>
      </div>
    </header>
  )
}

export default Header