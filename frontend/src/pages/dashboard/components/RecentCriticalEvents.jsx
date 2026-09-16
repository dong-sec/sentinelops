import { Link } from 'react-router-dom'

function RecentCriticalEvents({ events }) {
  return (
    <section className="dashboard-card dashboard-panel">
      <div className="dashboard-panel-header">
        <div>
          <h3>Recent Critical Events</h3>
          <p>Latest critical security events</p>
        </div>
      </div>

      {events.length === 0 ? (
        <div className="dashboard-empty">
          <p>No critical events available.</p>
        </div>
      ) : (
        <div className="dashboard-table-wrapper">
          <table className="dashboard-table">
            <thead>
              <tr>
                <th>Time</th>
                <th>Source IP</th>
                <th>Attack</th>
                <th>Severity</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>

            <tbody>
              {events.map((event) => (
                <tr key={event.id}>
                  <td>{event.timestamp}</td>
                  <td>{event.source_ip}</td>
                  <td>{event.attack_type ?? 'Unknown'}</td>
                  <td>
                    <span className="status-badge status-critical">
                      {event.severity}
                    </span>
                  </td>
                  <td>{event.status}</td>
                  <td>
                    <Link to={`/security/events/${event.id}`}>
                      View
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  )
}

export default RecentCriticalEvents