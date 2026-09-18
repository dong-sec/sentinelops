import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getEvents } from '../../services/events'
import './security.css'

function formatTimestamp(timestamp) {
  if (!timestamp) return '-'

  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
    timeZone: 'Asia/Seoul',
  }).format(new Date(timestamp))
}

function Events() {
  const navigate = useNavigate()

  const [events, setEvents] = useState([])
  const [page, setPage] = useState(1)
  const [pageSize] = useState(20)
  const [total, setTotal] = useState(0)
  const [totalPages, setTotalPages] = useState(0)

  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  async function loadEvents(targetPage = page) {
    try {
      setIsLoading(true)
      setError('')

      const response = await getEvents({
        page: targetPage,
        page_size: pageSize,
        sort_by: 'event_time',
        sort_order: 'desc',
      })

      setEvents(Array.isArray(response?.items) ? response.items : [])
      setPage(response?.page ?? targetPage)
      setTotal(response?.total ?? 0)
      setTotalPages(response?.total_pages ?? 0)
    } catch (err) {
      setError(err.message || 'Failed to load security events')
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    loadEvents(1)
  }, [])

  function handlePageChange(nextPage) {
    if (
      nextPage < 1 ||
      (totalPages > 0 && nextPage > totalPages) ||
      isLoading
    ) {
      return
    }

    loadEvents(nextPage)
  }

  if (isLoading && events.length === 0) {
    return (
      <section className="security-state">
        <h2>Events</h2>
        <p>Loading security events...</p>
      </section>
    )
  }

  if (error && events.length === 0) {
    return (
      <section className="security-state" role="alert">
        <h2>Events</h2>
        <p>{error}</p>

        <button
          type="button"
          className="security-secondary-button"
          onClick={() => loadEvents(page)}
        >
          Retry
        </button>
      </section>
    )
  }

  return (
    <section className="security-page">
      <header className="security-page-header">
        <div>
          <h2>Events</h2>
          <p>Security event history</p>
        </div>
      </header>

      <section className="security-card">
        <div className="security-card-header">
          <div>
            <h3>Security Events</h3>
            <p>
              {total > 0
                ? `${total.toLocaleString()} events`
                : 'No events'}
            </p>
          </div>

          {isLoading && (
            <span className="security-loading-inline">
              Refreshing...
            </span>
          )}
        </div>

        {error && (
          <div className="security-inline-error" role="alert">
            {error}
          </div>
        )}

        {events.length === 0 ? (
          <div className="security-empty-inline">
            <p>No security events found.</p>
            <p>Try changing the filter or time range.</p>
          </div>
        ) : (
          <>
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
                      <td>{event.source_ip ?? '-'}</td>
                      <td>{event.attack_type ?? '-'}</td>
                      <td>{event.severity ?? '-'}</td>
                      <td>
                        {event.risk_score !== null &&
                        event.risk_score !== undefined
                          ? `${event.risk_score} (${event.risk_level ?? '-'})`
                          : '-'}
                      </td>
                      <td>{event.status ?? '-'}</td>
                      <td>{event.response_status ?? '-'}</td>
                      <td>
                        <button
                          type="button"
                          className="security-table-action"
                          onClick={() =>
                            navigate(
                              `/security/events/${event.id}`,
                            )
                          }
                        >
                          View
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="security-pagination">
              <span>
                Showing {events.length} of {total.toLocaleString()}
              </span>

              <div className="security-pagination-controls">
                <button
                  type="button"
                  className="security-pagination-button"
                  disabled={page <= 1 || isLoading}
                  onClick={() => handlePageChange(page - 1)}
                >
                  Previous
                </button>

                <span>
                  Page {page}
                  {totalPages > 0 ? ` of ${totalPages}` : ''}
                </span>

                <button
                  type="button"
                  className="security-pagination-button"
                  disabled={
                    totalPages === 0 ||
                    page >= totalPages ||
                    isLoading
                  }
                  onClick={() => handlePageChange(page + 1)}
                >
                  Next
                </button>
              </div>
            </div>
          </>
        )}
      </section>
    </section>
  )
}

export default Events