import { NavLink } from 'react-router-dom'
import { useAuth } from '../auth'

export default function Layout({ children }: { children: React.ReactNode }) {
  const { usuario, logout } = useAuth()
  return (
    <div className="app-shell">
      <nav className="topbar">
        <div className="brand">
          <span className="logo">DAO</span>
          <span className="brand-name">Estudiantil Universitaria</span>
        </div>
        <div className="nav-links">
          <NavLink to="/" end className={({ isActive }) => (isActive ? 'active' : '')}>
            Propuestas
          </NavLink>
          <NavLink to="/ledger" className={({ isActive }) => (isActive ? 'active' : '')}>
            Ledger
          </NavLink>
          <NavLink to="/arquitectura" className={({ isActive }) => (isActive ? 'active' : '')}>
            Arquitectura
          </NavLink>
        </div>
        <div className="user-box">
          <div className="user-info">
            <strong>{usuario?.nombre}</strong>
            <span className={`rol rol-${usuario?.rol}`}>{usuario?.rol}</span>
          </div>
          <button className="btn btn-ghost" onClick={logout}>
            Salir
          </button>
        </div>
      </nav>
      <main className="content">{children}</main>
    </div>
  )
}