import { useEffect, useState } from 'react'
import { api } from '../api'
import type { LedgerData } from '../types'

export default function Ledger() {
  const [data, setData] = useState<LedgerData | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    api
      .get('/ledger')
      .then((r) => setData(r.data as LedgerData))
      .catch(() => setError('No se pudo consultar el ledger.'))
  }, [])

  return (
    <div>
      <h1 className="page-title">Ledger distribuido</h1>
      <p className="page-sub">Cadena de bloques de la DAO y estado mundial</p>
      {error && <div className="error-box">{error}</div>}

      {data && (
        <div className="grid-2" style={{ marginBottom: 20 }}>
          <div className="card">
            <strong>Integridad</strong>
            <p style={{ fontSize: 13, color: 'var(--texto-suave)', marginTop: 6 }}>
              {data.integridad ? 'Cadena válida' : '¡Cadena comprometida!'}
            </p>
          </div>
          <div className="card">
            <strong>Bloques</strong>
            <p style={{ fontSize: 13, color: 'var(--texto-suave)', marginTop: 6 }}>
              {data.bloques.length} bloques · estado mundial del contrato
            </p>
          </div>
        </div>
      )}

      {data?.bloques.length === 0 && <div className="vacio">El ledger está vacío.</div>}

      {data?.bloques.map((b) => (
        <div key={b.indice} className="bloque">
          <div className="bloque-head">
            <strong>Bloque #{b.indice}</strong>
            <span className="hash">ant: {b.hash_anterior}</span>
          </div>
          <div className="hash" style={{ marginBottom: 8 }}>hash: {b.hash}</div>
          {b.transacciones.length === 0 ? (
            <p style={{ color: 'var(--texto-suave)', fontSize: 13 }}>Bloque de génesis (sin transacciones).</p>
          ) : (
            b.transacciones.map((tx, i) => (
              <pre key={i} className="tx">{JSON.stringify(tx, null, 2)}</pre>
            ))
          )}
        </div>
      ))}
    </div>
  )
}