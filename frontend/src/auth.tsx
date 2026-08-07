import { createContext, useContext, useEffect, useState, type ReactNode } from 'react'
import { api, getSesion, setSesion, clearSesion } from './api'
import type { Rol } from './types'

export interface Usuario {
  token: string
  usuario: string
  nombre: string
  rol: Rol
  facultad: string
  permisos: string[]
}

interface AuthContext {
  usuario: Usuario | null
  login: (usuario: string, contrasena: string) => Promise<Usuario>
  logout: () => void
}

const AuthCtx = createContext<AuthContext>(null as unknown as AuthContext)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [usuario, setUsuario] = useState<Usuario | null>(null)

  useEffect(() => {
    setUsuario(getSesion())
  }, [])

  async function login(u: string, p: string): Promise<Usuario> {
    const { data } = await api.post('/login', { usuario: u, contrasena: p })
    const usr: Usuario = {
      token: data.token,
      usuario: data.usuario,
      nombre: data.nombre,
      rol: data.rol,
      facultad: data.facultad,
      permisos: data.permisos,
    }
    setSesion(usr)
    setUsuario(usr)
    return usr
  }

  function logout() {
    clearSesion()
    setUsuario(null)
  }

  return <AuthCtx.Provider value={{ usuario, login, logout }}>{children}</AuthCtx.Provider>
}

export function useAuth() {
  return useContext(AuthCtx)
}