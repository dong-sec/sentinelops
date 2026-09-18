import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { searchEvents } from '../../services/search'
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

function Search() {
  const navigate = useNavigate()

  const [query, setQuery] = useState('')
  const [searchQuery, setSearchQuery] = useState('')

  const [events, setEvents] = useState([])
  const [page, setPage] = useState(1)
  const [pageSize] = useState(20)
  const [total, setTotal] = useState(0)
  const [totalPages, setTotalPages] = useState(0)

  const [isLoading, setIsLoading] = useState(false)
  const [hasSearched, setHasSearched] = useState(false)
  const [error, setError] = useState('')

  async function loadSearch(targetQuery, targetPage = 1) {
    try {
      setIsLoading(true)
      setError('')

      const response = await searchEvents({
        q: targetQuery,
        page: targetPage,
        page_size: pageSize,
      })

      setEvents(Array.isArray(response?.items) ? response.items : [])
      setPage(response?.page ?? targetPage)
      setTotal(response?.total ?? 0)
      setTotalPages(response?.total_pages ?? 0)
      setSearchQuery(targetQuery)
      setHasSearched(true)
    } catch (err) {
      setError(err.message || 'Failed to search security events')
      setEvents([])
      setTotal(0)
      setTotalPages(0)
    } finally {
      setIsLoading(false)
    }
  }

  function handleSubmit(event) {
    event.preventDefault()

    const targetQuery = query.trim()

    if (!targetQuery || isLoading) {
      return
    }

    loadSearch(targetQuery, 1)
  }

  function handlePageChange(nextPage) {
    if (
      nextPage < 1 ||
      (totalPages > 0 && nextPage > totalPages) ||
      isLoading ||
      !searchQuery
    ) {
      return
    }

    loadSearch(searchQuery, nextPage)
  }

  function handleClear() {
    setQuery('')
    setSearchQuery('')
    setEvents([])
    setPage(1)
    setTotal(0)
    setTotalPages(0)
    setHasSearched(false)
    setError('')
  }

  return (
    <section className="security-page">
      <header className="security-page-header">
        <div>
          <h2>Search</h2>
          <p>Search security events</p>
        </div>
      </header>

      <section className="security-card">
        <form className="security-search-form" onSubmit={handleSubmit}>
          <div className="security-search-input-wrapper">
            <input
              type="search"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Search event ID, source IP, URL, attack type, user agent..."
              aria-label="Search security events"
            />

            <button
              type="submit"
              className="security-primary-button"
              disabled={!query.trim() || isLoading}
            >
              {isLoading ? 'Searching...' : 'Search'}
            </button>

            <button
              type="button"
              className="security-secondary-button"
              onClick={handleClear}
              disabled={isLoading && !hasSearched}
            >
              Clear
            </button>
          </div>
        </form>

        {!hasSearched ? (
          <div className="security-search-empty">
            <p>Enter a search term to find security events.</p>
            <p>
              Search supports event ID, source IP, URL, attack type,
              user agent, and detection rule.
            </p>
          </div>
        ) : (
          <>
            <div className="security-card-header">
              <div>
                <h3>Search Results</h3>
                <p>
                  {total > 0
                    ? `${total.toLocaleString()} events found`
                    : 'No events found'}
                </p>
              </div>

              {searchQuery && (
                <span className="security-search-query">
                  "{searchQuery}"
                </span>
              )}
            </div>

            {error && (
              <div className="security-inline-error" role="alert">
                {error}
              </div>
            )}

            {events.length === 0 && !isLoading ? (
              <div className="security-empty-inline">
                <p>No matching security events found.</p>
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
          </>
        )}
      </section>
    </section>
  )
}

export default Search