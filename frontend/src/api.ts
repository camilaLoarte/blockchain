import axios from 'axios'
import type { Usuario } from './auth'

const SESION_KEY = 'dao_sesion'

export const api = axios.create({ baseURL: '/api' })

api.interceptors.request.use((config) => {
  const usr = getSesion()
  if (usr?.token) {
    config.params = { ...config.params, token: usr.token }
  }
  return config
})

export function setSesion(usr: Usuario) {
  localStorage.setItem(SESION_KEY, JSON.stringify(usr))
}

export function getSesion(): Usuario | null {
  const raw = localStorage.getItem(SESION_KEY)
  if (!raw) return null
  try {
    return JSON.parse(raw) as Usuario
  } catch {
    return null
  }
}

export function clearSesion() {
  localStorage.removeItem(SESION_KEY)
}