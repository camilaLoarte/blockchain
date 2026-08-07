import { Navigate, Route, Routes } from 'react-router-dom'
import { useAuth } from './auth'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Ledger from './pages/Ledger'
import Arquitectura from './pages/Arquitectura'
import Layout from './components/Layout'

function Reclamados() {
  const { usuario } = useAuth()
  if (!usuario) return <Navigate to="/login" replace />
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/ledger" element={<Ledger />} />
        <Route path="/arquitectura" element={<Arquitectura />} />
      </Routes>
    </Layout>
  )
}

export default function App() {
  const { usuario } = useAuth()
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        path="/*"
        element={usuario ? <Reclamados /> : <Navigate to="/login" replace />}
      />
    </Routes>
  )
}