function AttackDistribution({ attackDistribution }) {
  return (
    <section className="dashboard-card dashboard-panel">
      <div className="dashboard-panel-header">
        <div>
          <h3>Attack Distribution</h3>
          <p>Detected attack types</p>
        </div>
      </div>

      {attackDistribution.length === 0 ? (
        <div className="dashboard-empty">
          <p>No attack data available.</p>
        </div>
      ) : (
        <div className="attack-list">
          {attackDistribution.map((item) => (
            <div className="attack-item" key={item.attack_type}>
              <span>{item.attack_type}</span>
              <strong>{item.count}</strong>
            </div>
          ))}
        </div>
      )}
    </section>
  )
}

export default AttackDistribution