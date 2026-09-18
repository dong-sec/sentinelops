import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getEvents } from '../../services/events'
import './security.css'

const INITIAL_FILTERS = {
  severity: '',
  risk_level: '',
  attack_type: '',
  source_ip: '',
  method: '',
  status: '',
  from: '',
  to: '',
}

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
  const [pagination, setPagination] = useState({
    page: 1,
    page_size: 20,
    total: 0,
    total_pages: 0,
  })
  const [filters, setFilters] = useState(INITIAL_FILTERS)
  const [appliedFilters, setAppliedFilters] = useState(INITIAL_FILTERS)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  async function loadEvents(page = 1, currentFilters = appliedFilters) {
    try {
      setIsLoading(true)
      setError('')

      const response = await getEvents({
        page,
        page_size: 20,
        ...currentFilters,
        sort_by: 'event_time',
        sort_order: 'desc',
      })

      setEvents(Array.isArray(response?.items) ? response.items : [])

      setPagination({
        page: response?.page ?? page,
        page_size: response?.page_size ?? 20,
        total: response?.total ?? 0,
        total_pages: response?.total_pages ?? 0,
      })
    } catch (err) {
      setError(err.message || 'Failed to load events')
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    loadEvents(1, INITIAL_FILTERS)
  }, [])

  function handleFilterChange(event) {
    const { name, value } = event.target

    setFilters((current) => ({
      ...current,
      [name]: value,
    }))
  }

  function handleApplyFilters(event) {
    event.preventDefault()

    setAppliedFilters(filters)
    loadEvents(1, filters)
  }

  function handleResetFilters() {
    setFilters(INITIAL_FILTERS)
    setAppliedFilters(INITIAL_FILTERS)
    loadEvents(1, INITIAL_FILTERS)
  }

  function handlePageChange(page) {
    if (
      page < 1 ||
      page > pagination.total_pages ||
      page === pagination.page
    ) {
      return
    }

    loadEvents(page, appliedFilters)
  }

  function handleEventClick(eventId) {
    navigate(`/security/events/${eventId}`)
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
        <form
          className="security-filter-panel"
          onSubmit={handleApplyFilters}
        >
          <div className="security-filter-grid">
            <label>
              <span>Severity</span>
              <select
                name="severity"
                value={filters.severity}
                onChange={handleFilterChange}
              >
                <option value="">All</option>
                <option value="CRITICAL">CRITICAL</option>
                <option value="HIGH">HIGH</option>
                <option value="MEDIUM">MEDIUM</option>
                <option value="LOW">LOW</option>
              </select>
            </label>

            <label>
              <span>Risk Level</span>
              <select
                name="risk_level"
                value={filters.risk_level}
                onChange={handleFilterChange}
              >
                <option value="">All</option>
                <option value="CRITICAL">CRITICAL</option>
                <option value="HIGH">HIGH</option>
                <option value="MEDIUM">MEDIUM</option>
                <option value="LOW">LOW</option>
              </select>
            </label>

            <label>
              <span>Attack Type</span>
              <input
                type="text"
                name="attack_type"
                value={filters.attack_type}
                onChange={handleFilterChange}
                placeholder="SQL_INJECTION"
              />
            </label>

            <label>
              <span>Source IP</span>
              <input
                type="text"
                name="source_ip"
                value={filters.source_ip}
                onChange={handleFilterChange}
                placeholder="192.168.1.100"
              />
            </label>

            <label>
              <span>HTTP Method</span>
              <select
                name="method"
                value={filters.method}
                onChange={handleFilterChange}
              >
                <option value="">All</option>
                <option value="GET">GET</option>
                <option value="POST">POST</option>
                <option value="PUT">PUT</option>
                <option value="PATCH">PATCH</option>
                <option value="DELETE">DELETE</option>
              </select>
            </label>

            <label>
              <span>Status</span>
              <input
                type="text"
                name="status"
                value={filters.status}
                onChange={handleFilterChange}
                placeholder="DETECTED"
              />
            </label>

            <label>
              <span>From</span>
              <input
                type="datetime-local"
                name="from"
                value={filters.from}
                onChange={handleFilterChange}
              />
            </label>

            <label>
              <span>To</span>
              <input
                type="datetime-local"
                name="to"
                value={filters.to}
                onChange={handleFilterChange}
              />
            </label>
          </div>

          <div className="security-filter-actions">
            <button type="submit" className="security-primary-button">
              Apply
            </button>

            <button
              type="button"
              className="security-secondary-button"
              onClick={handleResetFilters}
            >
              Reset
            </button>
          </div>
        </form>
      </section>

      <section className="security-card">
        <div className="security-card-header">
          <div>
            <h3>Security Events</h3>
            <p>{pagination.total} events found</p>
          </div>
        </div>

        {isLoading ? (
          <div className="security-empty">
            <p>Loading events...</p>
          </div>
        ) : error ? (
          <div className="security-empty" role="alert">
            <p>{error}</p>
          </div>
        ) : events.length === 0 ? (
          <div className="security-empty">
            <p>No security events available.</p>
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

            {pagination.total_pages > 1 && (
              <div className="security-pagination">
                <button
                  type="button"
                  className="security-secondary-button"
                  disabled={pagination.page <= 1 || isLoading}
                  onClick={() => handlePageChange(pagination.page - 1)}
                >
                  Previous
                </button>

                <span>
                  Page {pagination.page} of {pagination.total_pages}
                </span>

                <button
                  type="button"
                  className="security-secondary-button"
                  disabled={
                    pagination.page >= pagination.total_pages || isLoading
                  }
                  onClick={() => handlePageChange(pagination.page + 1)}
                >
                  Next
                </button>
              </div>
            )}
          </>
        )}
      </section>
    </section>
  )
}

export default AttackMonitor