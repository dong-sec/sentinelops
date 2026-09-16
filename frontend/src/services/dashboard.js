import { request } from './api'

async function getDashboardOverview() {
  return request('/v1/dashboard/overview')
}

async function getDashboardTrends(range = '24h') {
  return request(`/v1/dashboard/trends?range=${range}`)
}

export { getDashboardOverview, getDashboardTrends }