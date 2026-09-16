import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

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

function DashboardTrend({ trend }) {
  if (!trend || !Array.isArray(trend.points)) {
    return (
      <section className="dashboard-card dashboard-panel">
        <div className="dashboard-panel-header">
          <div>
            <h3>Attack Trend</h3>
            <p>Security events over time</p>
          </div>
        </div>

        <div className="dashboard-empty">
          <p>No trend data available.</p>
        </div>
      </section>
    )
  }

  if (trend.points.length === 0) {
    return (
      <section className="dashboard-card dashboard-panel">
        <div className="dashboard-panel-header">
          <div>
            <h3>Attack Trend</h3>
            <p>Security events over time</p>
          </div>
        </div>

        <div className="dashboard-empty">
          <p>No trend data available.</p>
        </div>
      </section>
    )
  }

  const chartData = trend.points.map((point) => ({
    ...point,
    displayTime: formatKstTime(point.timestamp),
  }))

  return (
    <section className="dashboard-card dashboard-panel">
      <div className="dashboard-panel-header">
        <div>
          <h3>Attack Trend</h3>
          <p>Security events over time</p>
        </div>
      </div>

      <div className="dashboard-trend-chart">
        <ResponsiveContainer width="100%" height={320}>
          <LineChart
            data={chartData}
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
    </section>
  )
}

export default DashboardTrend