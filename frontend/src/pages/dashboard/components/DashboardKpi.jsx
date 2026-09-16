function DashboardKpi({ kpi }) {
  const cards = [
    {
      label: 'Total Events',
      value: kpi.total_events,
    },
    {
      label: 'Critical Events',
      value: kpi.critical_events,
    },
    {
      label: 'High Risk Events',
      value: kpi.high_risk_events,
    },
    {
      label: 'Blocked IPs',
      value: kpi.blocked_ips,
    },
    {
      label: 'Active Incidents',
      value: kpi.active_incidents,
    },
    {
      label: 'Automatic Responses',
      value: kpi.automatic_responses,
    },
    {
      label: 'Response Failures',
      value: kpi.response_failures,
    },
  ]

  return (
    <section className="dashboard-section">
      <div className="dashboard-kpi-grid">
        {cards.map((card) => (
          <article className="dashboard-card dashboard-kpi-card" key={card.label}>
            <span className="dashboard-card-label">
              {card.label}
            </span>

            <strong className="dashboard-kpi-value">
              {card.value}
            </strong>
          </article>
        ))}
      </div>
    </section>
  )
}

export default DashboardKpi