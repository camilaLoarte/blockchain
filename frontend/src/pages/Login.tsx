import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../auth'

const ROLES = ['estudiante', 'facultad', 'consejo']

export default function Login() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [usuario, setUsuario] = useState('')
  const [contrasena, setContrasena] = useState('')
  const [error, setError] = useState('')
  const [cargando, setCargando] = useState(false)

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault()
    setCargando(true)
    setError('')
    try {
      await login(usuario.trim(), contrasena)
      navigate('/')
    } catch (err: unknown) {
      const message = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail
      setError(message || 'Error al iniciar sesión.')
    } finally {
      setCargando(false)
    }
  }

  return (
    <div className="login-wrap">
      <form className="login-card" onSubmit={onSubmit}>
        <div className="login-logo">DAO</div>
        <h1>DAO Estudiantil</h1>
        <p className="login-sub">Accede con tu cuenta según tu rol universitario.</p>

        <div className="login-roles">
          {ROLES.map((r) => (
            <span key={r} className={`chip rol-${r}`}>{r}</span>
          ))}
        </div>

        {error && <div className="error-box">{error}</div>}

        <div className="field">
          <label>Usuario</label>
          <input
            value={usuario}
            onChange={(e) => setUsuario(e.target.value)}
            placeholder="ej. camila"
            required
          />
        </div>
        <div className="field">
          <label>Contraseña</label>
          <input
            type="password"
            value={contrasena}
            onChange={(e) => setContrasena(e.target.value)}
            placeholder="••••"
            required
          />
        </div>
        <button className="btn btn-primary btn-block" disabled={cargando}>
          {cargando ? 'Ingresando…' : 'Ingresar'}
        </button>
      </form>
    </div>
  )
}