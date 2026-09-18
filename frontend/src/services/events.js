import { request } from './api'

async function getEvents(params = {}) {
  const searchParams = new URLSearchParams()

  const {
    page = 1,
    page_size = 20,
    severity,
    risk_level,
    attack_type,
    source_ip,
    status,
    method,
    from,
    to,
    sort_by = 'event_time',
    sort_order = 'desc',
  } = params

  searchParams.set('page', page)
  searchParams.set('page_size', page_size)
  searchParams.set('sort_by', sort_by)
  searchParams.set('sort_order', sort_order)

  if (severity) searchParams.set('severity', severity)
  if (risk_level) searchParams.set('risk_level', risk_level)
  if (attack_type) searchParams.set('attack_type', attack_type)
  if (source_ip) searchParams.set('source_ip', source_ip)
  if (status) searchParams.set('status', status)
  if (method) searchParams.set('method', method)
  if (from) searchParams.set('from', from)
  if (to) searchParams.set('to', to)

  return request(`/v1/events?${searchParams.toString()}`)
}

async function getEvent(eventId) {
  return request(`/v1/events/${eventId}`)
}

async function getEventDetections(eventId) {
  return request(`/v1/events/${eventId}/detections`)
}

async function getEventRisk(eventId) {
  return request(`/v1/events/${eventId}/risk`)
}

async function getEventTimeline(eventId) {
  return request(`/v1/events/${eventId}/timeline`)
}

export {
  getEvents,
  getEvent,
  getEventDetections,
  getEventRisk,
  getEventTimeline,
}