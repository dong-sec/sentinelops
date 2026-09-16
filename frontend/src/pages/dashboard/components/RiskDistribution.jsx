function RiskDistribution({ riskDistribution }) {
  const items = [
    {
      label: 'Critical',
      value: riskDistribution.critical,
      className: 'risk-critical',
    },
    {
      label: 'High',
      value: riskDistribution.high,
      className: 'risk-high',
    },
    {
      label: 'Medium',
      value: riskDistribution.medium,
      className: 'risk-medium',
    },
    {
      label: 'Low',
      value: riskDistribution.low,
      className: 'risk-low',
    },
  ]

  return (
    <section className="dashboard-card dashboard-panel">
      <div className="dashboard-panel-header">
        <div>
          <h3>Risk Distribution</h3>
          <p>Events by risk level</p>
        </div>
      </div>

      <div className="risk-list">
        {items.map((item) => (
          <div className="risk-item" key={item.label}>
            <div className="risk-item-label">
              <span className={`risk-indicator ${item.className}`} />
              <span>{item.label}</span>
            </div>

            <strong>{item.value}</strong>
          </div>
        ))}
      </div>
    </section>
  )
}

export default RiskDistribution