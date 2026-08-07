import { useEffect, useState } from 'react'
import { api } from '../api'
import type { ArquitecturaData } from '../types'

export default function Arquitectura() {
  const [data, setData] = useState<ArquitecturaData | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    api
      .get('/arquitectura')
      .then((r) => setData(r.data as ArquitecturaData))
      .catch(() => setError('No se pudo consultar la arquitectura.'))
  }, [])

  return (
    <div>
      <h1 className="page-title">Arquitectura de la DAO</h1>
      <p className="page-sub">Identidades, permisos MSP y datos off-chain</p>
      {error && <div className="error-box">{error}</div>}

      {data && (
        <div className="grid-2">
          <div className="card">
            <strong>Permisos por rol (MSP)</strong>
            {Object.entries(data.permisos_msp).map(([rol, perms]) => (
              <div key={rol} style={{ marginTop: 10 }}>
                <span className={`rol rol-${rol}`}>{rol}</span>
                <ul style={{ margin: '6px 0 0 18px', fontSize: 13, color: 'var(--texto-suave)' }}>
                  {perms.map((p) => (
                    <li key={p}>{p}</li>
                  ))}
                </ul>
              </div>
            ))}
            <p style={{ fontSize: 13, color: 'var(--texto-suave)', marginTop: 12 }}>
              Política de endoso mínima: <b>{data.politica_endoso}</b>
            </p>
          </div>

          <div className="card">
            <strong>Identidades registradas</strong>
            {Object.entries(data.identidades).map(([sujeto, cert]) => (
              <div key={sujeto} style={{ marginTop: 10 }}>
                <b>{sujeto}</b>
                <span className={`rol rol-${cert.rol}`}>{cert.rol}</span>
                <div style={{ fontSize: 12, color: 'var(--texto-suave)', marginTop: 4 }}>
                  facultad: {cert.facultad} · serie: {cert.serie.slice(0, 12)}…
                </div>
              </div>
            ))}
          </div>

          <div className="card" style={{ gridColumn: '1 / -1' }}>
            <strong>Datos off-chain (almacén de perfiles)</strong>
            <p style={{ fontSize: 13, color: 'var(--texto-suave)', marginTop: 6 }}>
              El contrato solo guarda hashes y tokens en la cadena; los datos personales viven en el almacén off-chain.
            </p>
            {Object.entries(data.offchain_perfiles).map(([sujeto, perfil]) => (
              <div key={sujeto} style={{ marginTop: 8, fontSize: 13 }}>
                <b>{sujeto}</b> — facultad: {perfil.facultad}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}