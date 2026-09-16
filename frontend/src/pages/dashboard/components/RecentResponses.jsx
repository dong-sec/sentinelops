import { Link } from 'react-router-dom'

function RecentResponses({ responses }) {
  return (
    <section className="dashboard-card dashboard-panel">
      <div className="dashboard-panel-header">
        <div>
          <h3>Recent Responses</h3>
          <p>Latest automated and manual responses</p>
        </div>
      </div>

      {responses.length === 0 ? (
        <div className="dashboard-empty">
          <p>No response history available.</p>
        </div>
      ) : (
        <div className="dashboard-table-wrapper">
          <table className="dashboard-table">
            <thead>
              <tr>
                <th>Response</th>
                <th>Target IP</th>
                <th>Status</th>
                <th>Created At</th>
                <th>Action</th>
              </tr>
            </thead>

            <tbody>
              {responses.map((response) => (
                <tr key={response.id}>
                  <td>{response.response_type}</td>
                  <td>{response.target_ip ?? 'N/A'}</td>
                  <td>
                    <span className="status-badge">
                      {response.status}
                    </span>
                  </td>
                  <td>{response.created_at}</td>
                  <td>
                    <Link to={`/response/history/${response.id}`}>
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

export default RecentResponses