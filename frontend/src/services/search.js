import { request } from './api'

async function searchEvents(params = {}) {
  const searchParams = new URLSearchParams()

  const {
    q,
    page = 1,
    page_size = 20,
  } = params

  if (q) searchParams.set('q', q)

  searchParams.set('page', page)
  searchParams.set('page_size', page_size)

  return request(`/v1/events/search?${searchParams.toString()}`)
}

export { searchEvents }