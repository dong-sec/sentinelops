import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getEvents } from '../../services/events'
import './security.css'

function formatTimestamp(timestamp) {
  if (!timestamp) return '-'

  return new Intl.DateTimeFormat('ko-KR', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
    timeZone: 'Asia/Seoul',
  }).format(new Date(timestamp))
}

function formatValue(value) {
  return value ?? '-'
}

function AttackMonitor() {
  const navigate = useNavigate()

  const [events, setEvents] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function loadEvents() {
      try {
        setIsLoading(true)
        setError('')

        const response = await getEvents({
          page: 1,
          page_size: 20,
          sort_by: 'event_time',
          sort_order: 'desc',
        })

        setEvents(Array.isArray(response?.items) ? response.items : [])
      } catch (err) {
        setError(err.message || 'Failed to load events')
      } finally {
        setIsLoading(false)
      }
    }

    loadEvents()
  }, [])

  function handleEventClick(eventId) {
    navigate(`/security/events/${eventId}`)
  }

  if (isLoading) {
    return (
      <section className="security-state">
        <h2>Attack Monitor</h2>
        <p>Loading events...</p>
      </section>
    )
  }

  if (error) {
    return (
      <section className="security-state" role="alert">
        <h2>Attack Monitor</h2>
        <p>{error}</p>
      </section>
    )
  }

  return (
    <section className="security-page">
      <header className="security-page-header">
        <div>
          <h2>Attack Monitor</h2>
          <p>Real-time security event monitoring</p>
        </div>

        <div className="security-live-status">
          <span className="security-live-dot" />
          LIVE
        </div>
      </header>

      <section className="security-card">
        <div className="security-card-header">
          <div>
            <h3>Security Events</h3>
            <p>{events.length} events loaded</p>
          </div>
        </div>

        {events.length === 0 ? (
          <div className="security-empty">
            <p>No security events available.</p>
          </div>
        ) : (
          <div className="security-table-wrapper">
            <table className="security-table">
              <thead>
                <tr>
                  <th>Time</th>
                  <th>Source IP</th>
                  <th>Attack</th>
                  <th>Severity</th>
                  <th>Risk</th>
                  <th>Status</th>
                  <th>Response</th>
                  <th>Action</th>
                </tr>
              </thead>

              <tbody>
                {events.map((event) => (
                  <tr key={event.id}>
                    <td>{formatTimestamp(event.timestamp)}</td>
                    <td>{formatValue(event.source_ip)}</td>
                    <td>{formatValue(event.attack_type)}</td>
                    <td>{formatValue(event.severity)}</td>
                    <td>
                      {event.risk_score !== null &&
                      event.risk_score !== undefined
                        ? `${event.risk_score} (${formatValue(event.risk_level)})`
                        : '-'}
                    </td>
                    <td>{formatValue(event.status)}</td>
                    <td>{formatValue(event.response_status)}</td>
                    <td>
                      <button
                        type="button"
                        className="security-action-button"
                        onClick={() => handleEventClick(event.id)}
                      >
                        View
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </section>
  )
}

export default AttackMonitor