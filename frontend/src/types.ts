export type Rol = 'estudiante' | 'facultad' | 'consejo'

export interface LoginResponse {
  token: string
  usuario: string
  nombre: string
  rol: Rol
  facultad: string
  permisos: string[]
}

export interface Propuesta {
  id: string
  titulo: string
  autor: string
  estado: Estado
  endosos: number
  endosos_minimo: number
  quorum: number
  votos: Record<string, number>
  descripcion: string
  motivo_rechazo?: string | null
}

export type Estado = 'borrador' | 'validada' | 'en_votacion' | 'cerrada' | 'rechazada'

export interface Bloque {
  indice: number
  hash: string
  hash_anterior: string
  transacciones: unknown[]
}

export interface LedgerData {
  bloques: Bloque[]
  world_state: Record<string, unknown>
  integridad: boolean
}

export interface ArquitecturaData {
  permisos_msp: Record<string, string[]>
  identidades: Record<string, { rol: string; facultad: string; serie: string }>
  offchain_perfiles: Record<string, { facultad: string; correo: string }>
  politica_endoso: number
}