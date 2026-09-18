import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getEvents } from '../../services/events'
import './security.css'

const DEFAULT_FILTERS = {
  severity: '',
  risk_level: '',
  attack_type: '',
  source_ip: '',
  status: '',
  method: '',
  from: '',
  to: '',
  sort_by: 'event_time',
  sort_order: 'desc',
}

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

  const [filters, setFilters] = useState(DEFAULT_FILTERS)
  const [appliedFilters, setAppliedFilters] = useState(DEFAULT_FILTERS)

  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  async function loadEvents(targetPage = page, targetFilters = appliedFilters) {
    try {
      setIsLoading(true)
      setError('')

      const response = await getEvents({
        page: targetPage,
        page_size: pageSize,
        ...targetFilters,
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
    loadEvents(1, DEFAULT_FILTERS)
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

    const nextFilters = { ...filters }

    setAppliedFilters(nextFilters)
    loadEvents(1, nextFilters)
  }

  function handleResetFilters() {
    setFilters(DEFAULT_FILTERS)
    setAppliedFilters(DEFAULT_FILTERS)
    loadEvents(1, DEFAULT_FILTERS)
  }

  function handleSortChange(event) {
    const { name, value } = event.target

    const nextFilters = {
      ...appliedFilters,
      [name]: value,
    }

    setFilters((current) => ({
      ...current,
      [name]: value,
    }))

    setAppliedFilters(nextFilters)
    loadEvents(1, nextFilters)
  }

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

        <form className="security-filter-form" onSubmit={handleApplyFilters}>
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
                <option value="DELETE">DELETE</option>
                <option value="PATCH">PATCH</option>
              </select>
            </label>

            <label>
              <span>Status</span>
              <select
                name="status"
                value={filters.status}
                onChange={handleFilterChange}
              >
                <option value="">All</option>
                <option value="DETECTED">DETECTED</option>
                <option value="BLOCKED">BLOCKED</option>
                <option value="RESOLVED">RESOLVED</option>
              </select>
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
            <div className="security-filter-sort">
              <label>
                <span>Sort By</span>
                <select
                  name="sort_by"
                  value={filters.sort_by}
                  onChange={handleSortChange}
                >
                  <option value="event_time">Time</option>
                  <option value="risk_score">Risk Score</option>
                  <option value="severity">Severity</option>
                </select>
              </label>

              <label>
                <span>Order</span>
                <select
                  name="sort_order"
                  value={filters.sort_order}
                  onChange={handleSortChange}
                >
                  <option value="desc">Descending</option>
                  <option value="asc">Ascending</option>
                </select>
              </label>
            </div>

            <div className="security-filter-buttons">
              <button
                type="button"
                className="security-secondary-button"
                onClick={handleResetFilters}
                disabled={isLoading}
              >
                Reset
              </button>

              <button
                type="submit"
                className="security-primary-button"
                disabled={isLoading}
              >
                Apply
              </button>
            </div>
          </div>
        </form>

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