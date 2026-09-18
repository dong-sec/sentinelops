import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import {
  getEvent,
  getEventDetections,
  getEventRisk,
  getEventTimeline,
} from '../../services/events'
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

function formatValue(value) {
  return value ?? '-'
}

function formatJson(value) {
  if (value === null || value === undefined) return '-'

  try {
    return JSON.stringify(value, null, 2)
  } catch {
    return String(value)
  }
}

function EventDetail() {
  const { eventId } = useParams()
  const navigate = useNavigate()

  const [event, setEvent] = useState(null)
  const [detections, setDetections] = useState([])
  const [riskHistory, setRiskHistory] = useState([])
  const [timeline, setTimeline] = useState([])

  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function loadEventDetail() {
      try {
        setIsLoading(true)
        setError('')

        const [
          eventResponse,
          detectionsResponse,
          riskResponse,
          timelineResponse,
        ] = await Promise.all([
          getEvent(eventId),
          getEventDetections(eventId),
          getEventRisk(eventId),
          getEventTimeline(eventId),
        ])

        setEvent(eventResponse ?? null)
        setDetections(
          Array.isArray(detectionsResponse)
            ? detectionsResponse
            : [],
        )
        setRiskHistory(
          Array.isArray(riskResponse)
            ? riskResponse
            : [],
        )
        setTimeline(
          Array.isArray(timelineResponse)
            ? timelineResponse
            : [],
        )
      } catch (err) {
        setError(err.message || 'Failed to load event detail')
      } finally {
        setIsLoading(false)
      }
    }

    loadEventDetail()
  }, [eventId])

  if (isLoading) {
    return (
      <section className="security-state">
        <h2>Event Detail</h2>
        <p>Loading event...</p>
      </section>
    )
  }

  if (error) {
    return (
      <section className="security-state" role="alert">
        <h2>Event Detail</h2>
        <p>{error}</p>

        <button
          type="button"
          className="security-secondary-button"
          onClick={() => navigate('/security/monitor')}
        >
          Back to Attack Monitor
        </button>
      </section>
    )
  }

  if (!event) {
    return (
      <section className="security-state">
        <h2>Event Detail</h2>
        <p>Event not found.</p>

        <button
          type="button"
          className="security-secondary-button"
          onClick={() => navigate('/security/monitor')}
        >
          Back to Attack Monitor
        </button>
      </section>
    )
  }

  return (
    <section className="security-page">
      <header className="security-page-header">
        <div>
          <h2>Event Detail</h2>
          <p>{event.id}</p>
        </div>

        <button
          type="button"
          className="security-secondary-button"
          onClick={() => navigate('/security/monitor')}
        >
          Back
        </button>
      </header>

      <section className="security-card">
        <div className="security-card-header">
          <div>
            <h3>Event Information</h3>
            <p>Security event details</p>
          </div>
        </div>

        <div className="security-detail-grid">
          <div className="security-detail-item">
            <span>Event ID</span>
            <strong>{formatValue(event.id)}</strong>
          </div>

          <div className="security-detail-item">
            <span>Time</span>
            <strong>{formatTimestamp(event.timestamp)}</strong>
          </div>

          <div className="security-detail-item">
            <span>Source IP</span>
            <strong>{formatValue(event.source_ip)}</strong>
          </div>

          <div className="security-detail-item">
            <span>HTTP Method</span>
            <strong>{formatValue(event.method)}</strong>
          </div>

          <div className="security-detail-item security-detail-wide">
            <span>Request URI</span>
            <strong>{formatValue(event.request_uri)}</strong>
          </div>

          <div className="security-detail-item">
            <span>Protocol</span>
            <strong>{formatValue(event.protocol)}</strong>
          </div>

          <div className="security-detail-item">
            <span>Status Code</span>
            <strong>{formatValue(event.status_code)}</strong>
          </div>

          <div className="security-detail-item">
            <span>Status</span>
            <strong>{formatValue(event.status)}</strong>
          </div>

          <div className="security-detail-item">
            <span>Host</span>
            <strong>{formatValue(event.host)}</strong>
          </div>

          <div className="security-detail-item">
            <span>Server Name</span>
            <strong>{formatValue(event.server_name)}</strong>
          </div>

          <div className="security-detail-item">
            <span>Request Size</span>
            <strong>
              {event.request_size !== null &&
              event.request_size !== undefined
                ? `${event.request_size} bytes`
                : '-'}
            </strong>
          </div>

          <div className="security-detail-item">
            <span>Response Size</span>
            <strong>
              {event.response_size !== null &&
              event.response_size !== undefined
                ? `${event.response_size} bytes`
                : '-'}
            </strong>
          </div>

          <div className="security-detail-item">
            <span>Response Time</span>
            <strong>
              {event.response_time_ms !== null &&
              event.response_time_ms !== undefined
                ? `${event.response_time_ms} ms`
                : '-'}
            </strong>
          </div>

          <div className="security-detail-item">
            <span>Created At</span>
            <strong>{formatTimestamp(event.created_at)}</strong>
          </div>
        </div>
      </section>

      <section className="security-card">
        <div className="security-card-header">
          <div>
            <h3>Detection</h3>
            <p>Detection result associated with this event</p>
          </div>
        </div>

        <div className="security-detail-grid">
          <div className="security-detail-item">
            <span>Attack Type</span>
            <strong>{formatValue(event.attack_type)}</strong>
          </div>

          <div className="security-detail-item">
            <span>Rule Name</span>
            <strong>{formatValue(event.rule_name)}</strong>
          </div>

          <div className="security-detail-item">
            <span>Severity</span>
            <strong>{formatValue(event.detection_severity)}</strong>
          </div>

          <div className="security-detail-item">
            <span>Confidence</span>
            <strong>
              {event.confidence !== null &&
              event.confidence !== undefined
                ? event.confidence
                : '-'}
            </strong>
          </div>

          <div className="security-detail-item security-detail-wide">
            <span>Description</span>
            <strong>
              {formatValue(event.detection_description)}
            </strong>
          </div>

          <div className="security-detail-item security-detail-wide">
            <span>Evidence</span>
            <pre>{formatJson(event.evidence)}</pre>
          </div>
        </div>
      </section>

      <section className="security-card">
        <div className="security-card-header">
          <div>
            <h3>Detection Records</h3>
            <p>Detection records associated with this event</p>
          </div>
        </div>

        {detections.length === 0 ? (
          <div className="security-empty-inline">
            No detection records available.
          </div>
        ) : (
          <div className="security-table-wrapper">
            <table className="security-table">
              <thead>
                <tr>
                  <th>Time</th>
                  <th>Type</th>
                  <th>Rule</th>
                  <th>Severity</th>
                  <th>Confidence</th>
                  <th>Description</th>
                </tr>
              </thead>

              <tbody>
                {detections.map((detection) => (
                  <tr key={detection.id}>
                    <td>{formatTimestamp(detection.detected_at)}</td>
                    <td>{formatValue(detection.detection_type)}</td>
                    <td>{formatValue(detection.rule_name)}</td>
                    <td>{formatValue(detection.severity)}</td>
                    <td>
                      {detection.confidence !== null &&
                      detection.confidence !== undefined
                        ? detection.confidence
                        : '-'}
                    </td>
                    <td>{formatValue(detection.description)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <section className="security-card">
        <div className="security-card-header">
          <div>
            <h3>Risk</h3>
            <p>Risk assessment associated with this event</p>
          </div>
        </div>

        <div className="security-detail-grid">
          <div className="security-detail-item">
            <span>Risk Score</span>
            <strong>{formatValue(event.risk_score)}</strong>
          </div>

          <div className="security-detail-item">
            <span>Risk Level</span>
            <strong>{formatValue(event.risk_level)}</strong>
          </div>

          <div className="security-detail-item">
            <span>Calculation Version</span>
            <strong>{formatValue(event.calculation_version)}</strong>
          </div>

          <div className="security-detail-item">
            <span>Calculated At</span>
            <strong>{formatTimestamp(event.calculated_at)}</strong>
          </div>

          <div className="security-detail-item security-detail-wide">
            <span>Factors</span>
            <pre>{formatJson(event.factors)}</pre>
          </div>
        </div>
      </section>

      <section className="security-card">
        <div className="security-card-header">
          <div>
            <h3>Risk History</h3>
            <p>Risk records associated with this event</p>
          </div>
        </div>

        {riskHistory.length === 0 ? (
          <div className="security-empty-inline">
            No risk records available.
          </div>
        ) : (
          <div className="security-table-wrapper">
            <table className="security-table">
              <thead>
                <tr>
                  <th>Time</th>
                  <th>Source IP</th>
                  <th>Score</th>
                  <th>Severity</th>
                  <th>Version</th>
                </tr>
              </thead>

              <tbody>
                {riskHistory.map((risk) => (
                  <tr key={risk.id}>
                    <td>{formatTimestamp(risk.calculated_at)}</td>
                    <td>{formatValue(risk.source_ip)}</td>
                    <td>{formatValue(risk.score)}</td>
                    <td>{formatValue(risk.severity)}</td>
                    <td>
                      {formatValue(risk.calculation_version)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <section className="security-card">
        <div className="security-card-header">
          <div>
            <h3>Timeline</h3>
            <p>Event processing timeline</p>
          </div>
        </div>

        {timeline.length === 0 ? (
          <div className="security-empty-inline">
            No timeline records available.
          </div>
        ) : (
          <div className="security-timeline">
            {timeline.map((item, index) => (
              <div
                className="security-timeline-item"
                key={`${item.timestamp}-${item.event_type}-${index}`}
              >
                <div className="security-timeline-marker" />

                <div className="security-timeline-content">
                  <div className="security-timeline-header">
                    <strong>{formatValue(item.event_type)}</strong>
                    <span>
                      {formatTimestamp(item.timestamp)}
                    </span>
                  </div>

                  <div className="security-timeline-status">
                    {formatValue(item.status)}
                  </div>

                  <p>
                    {formatValue(item.description)}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      <section className="security-card">
        <div className="security-card-header">
          <div>
            <h3>Request Context</h3>
            <p>Additional request information</p>
          </div>
        </div>

        <div className="security-detail-grid">
          <div className="security-detail-item security-detail-wide">
            <span>User Agent</span>
            <strong>{formatValue(event.user_agent)}</strong>
          </div>

          <div className="security-detail-item security-detail-wide">
            <span>Referer</span>
            <strong>{formatValue(event.referer)}</strong>
          </div>

          <div className="security-detail-item security-detail-wide">
            <span>Raw Log</span>
            <pre>{formatValue(event.raw_log)}</pre>
          </div>
        </div>
      </section>
    </section>
  )
}

export default EventDetail