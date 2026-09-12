import { NavLink } from 'react-router-dom'

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <h1>SentinelOps</h1>
        <span>Security Operations</span>
      </div>

      <nav className="sidebar-nav">
        <NavLink to="/dashboard">Dashboard</NavLink>

        <div className="nav-section">
          <span>Security</span>
          <NavLink to="/security/monitor">Attack Monitor</NavLink>
          <NavLink to="/security/events">Events</NavLink>
          <NavLink to="/security/search">Search</NavLink>
          <NavLink to="/security/ip/example">IP Intelligence</NavLink>
        </div>

        <div className="nav-section">
          <span>Response</span>
          <NavLink to="/response/policies">Policies</NavLink>
          <NavLink to="/response/history">Response History</NavLink>
        </div>

        <div className="nav-section">
          <span>Operations</span>
          <NavLink to="/operations/audit">Audit Logs</NavLink>
          <NavLink to="/operations/monitoring">Monitoring</NavLink>
          <NavLink to="/operations/backup">Backup & Recovery</NavLink>
          <NavLink to="/operations/reports">Reports</NavLink>
        </div>

        <div className="nav-section">
          <span>System</span>
          <NavLink to="/system/health">Health</NavLink>
          <NavLink to="/system/settings">Settings</NavLink>
        </div>
      </nav>
    </aside>
  )
}

export default Sidebar