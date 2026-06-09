import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: `${API_BASE}/api/v1`,
  timeout: 10000,
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('sghl_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  res => res,
  err => {
    // Ne PAS déconnecter en cas de 401 — le token démo n'est pas reconnu par le backend
    // Les vues gèrent elles-mêmes le fallback sur les données démo
    return Promise.reject(err)
  }
)

export default api
