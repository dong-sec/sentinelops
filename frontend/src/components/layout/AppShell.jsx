function AppShell({ sidebar, header, children }) {
  return (
    <div className="app-shell">
      {sidebar}

      <div className="app-main">
        {header}

        <main className="content">{children}</main>
      </div>
    </div>
  )
}

export default AppShell