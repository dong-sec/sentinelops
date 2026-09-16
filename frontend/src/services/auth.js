import { request } from './api'

async function login(username, password) {
  return request('/v1/auth/login', {
    method: 'POST',
    body: JSON.stringify({
      username,
      password,
    }),
  })
}

export { login }