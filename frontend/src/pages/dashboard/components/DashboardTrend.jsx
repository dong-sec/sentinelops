import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

const TREND_RANGES = [
  { value: '1h', label: '1h' },
  { value: '6h', label: '6h' },
  { value: '24h', label: '24h' },
  { value: '7d', label: '7d' },
  { value: '30d', label: '30d' },
]

function formatKstTime(timestamp) {
  return new Intl.DateTimeFormat('ko-KR', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
    timeZone: 'Asia/Seoul',
  }).format(new Date(timestamp))
}

function DashboardTrend({
  trend,
  selectedRange = '24h',
  onRangeChange,
  isLoading = false,
}) {
  return (
    <section className="dashboard-card dashboard-panel">
      <div className="dashboard-panel-header">
        <div>
          <h3>Attack Trend</h3>
          <p>Security events over time</p>
        </div>

        <div className="dashboard-trend-ranges" role="group" aria-label="Trend time range">
          {TREND_RANGES.map((range) => (
            <button
              key={range.value}
              type="button"
              className={`dashboard-trend-range ${
                selectedRange === range.value ? 'active' : ''
              }`}
              onClick={() => onRangeChange?.(range.value)}
              disabled={isLoading}
            >
              {range.label}
            </button>
          ))}
        </div>
      </div>

      {!trend || !Array.isArray(trend.points) ? (
        <div className="dashboard-empty">
          <p>No trend data available.</p>
        </div>
      ) : trend.points.length === 0 ? (
        <div className="dashboard-empty">
          <p>No trend data available.</p>
        </div>
      ) : (
        <div className="dashboard-trend-chart">
          <ResponsiveContainer width="100%" height={320}>
            <LineChart
              data={trend.points.map((point) => ({
                ...point,
                displayTime: formatKstTime(point.timestamp),
              }))}
              margin={{
                top: 8,
                right: 12,
                left: 0,
                bottom: 8,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />

              <XAxis
                dataKey="displayTime"
                minTickGap={32}
              />

              <YAxis
                allowDecimals={false}
                width={40}
              />

              <Tooltip />

              <Line
                type="monotone"
                dataKey="events"
                name="Events"
                strokeWidth={2}
                dot={false}
              />

              <Line
                type="monotone"
                dataKey="critical"
                name="Critical"
                strokeWidth={2}
                dot={false}
              />

              <Line
                type="monotone"
                dataKey="high"
                name="High"
                strokeWidth={2}
                dot={false}
              />

              <Line
                type="monotone"
                dataKey="blocked"
                name="Blocked"
                strokeWidth={2}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </section>
  )
}

export default DashboardTrend