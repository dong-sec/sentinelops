import { useEffect, useState } from 'react'
import { getDashboardOverview } from '../../services/dashboard'
import DashboardKpi from './components/DashboardKpi'
import RiskDistribution from './components/RiskDistribution'
import AttackDistribution from './components/AttackDistribution'
import RecentCriticalEvents from './components/RecentCriticalEvents'
import RecentResponses from './components/RecentResponses'
import './dashboard.css'

function Dashboard() {
  const [data, setData] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function loadDashboard() {
      try {
        const response = await getDashboardOverview()
        setData(response ?? null)
      } catch (err) {
        setError(err.message || 'Failed to load dashboard')
      } finally {
        setIsLoading(false)
      }
    }

    loadDashboard()
  }, [])

  if (isLoading) {
    return (
      <section className="dashboard-state">
        <h2>Dashboard</h2>
        <p>Loading dashboard...</p>
      </section>
    )
  }

  if (error) {
    return (
      <section className="dashboard-state" role="alert">
        <h2>Dashboard</h2>
        <p>{error}</p>
      </section>
    )
  }

  if (!data) {
    return (
      <section className="dashboard-state">
        <h2>Dashboard</h2>
        <p>No dashboard data available.</p>
      </section>
    )
  }

  return (
    <section className="dashboard">
      <header className="dashboard-header">
        <div>
          <h2>Dashboard</h2>
          <p>Security overview</p>
        </div>
      </header>

      <DashboardKpi kpi={data.kpi} />

      <div className="dashboard-grid dashboard-grid-two">
        <AttackDistribution
          attackDistribution={data.attack_distribution}
        />

        <RiskDistribution
          riskDistribution={data.risk_distribution}
        />
      </div>

      <RecentCriticalEvents
        events={data.recent_critical_events}
      />

      <RecentResponses
        responses={data.recent_responses}
      />
    </section>
  )
}

export default Dashboard