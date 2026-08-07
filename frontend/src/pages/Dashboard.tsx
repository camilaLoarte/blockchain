import { useCallback, useEffect, useState } from 'react'
import { api } from '../api'
import { useAuth } from '../auth'
import type { Propuesta } from '../types'

const PASOS = ['borrador', 'validada', 'en_votacion', 'cerrada']

export default function Dashboard() {
  const { usuario } = useAuth()
  const [props, setProps] = useState<Propuesta[]>([])
  const [error, setError] = useState('')
  const [puede, setPuede] = useState<Record<string, boolean>>({})
  const [nueva, setNueva] = useState({ titulo: '', descripcion: '' })
  const [mostrarNueva, setMostrarNueva] = useState(false)
  const [quorum, setQuorum] = useState(3)
  const [votoToken, setVotoToken] = useState<string | null>(null)

  const cargar = useCallback(async () => {
    const { data } = await api.get('/propuestas')
    setProps(data as Propuesta[])
  }, [])

  useEffect(() => {
    const un = new Set(usuario?.permisos || [])
    setPuede({
      crear: un.has('crear_propuesta'),
      endosar: un.has('endosar'),
      abrir: un.has('abrir_votacion'),
      votar: un.has('votar'),
      rechazar: un.has('rechazar'),
    })
    cargar().catch(() => setError('No se pudieron cargar las propuestas.'))
  }, [usuario, cargar])

  function mensajeDe(err: unknown): string {
    return (
      (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail ||
      'Error'
    )
  }

  async function accion(endpoint: string, body: Record<string, unknown>, verbo: string) {
    setError('')
    try {
      await api.post(endpoint, body)
    } catch (err: unknown) {
      setError(`${verbo}: ${mensajeDe(err)}`)
    } finally {
      cargar()
    }
  }

  async function crearPropuesta(e: React.FormEvent) {
    e.preventDefault()
    if (!nueva.titulo.trim()) return
    setError('')
    try {
      await api.post('/propuestas/crear', nueva)
      setNueva({ titulo: '', descripcion: '' })
      setMostrarNueva(false)
    } catch (err: unknown) {
      setError(`Crear propuesta: ${mensajeDe(err)}`)
    } finally {
      cargar()
    }
  }

  async function votar(id: string, opcion: string) {
    setError('')
    try {
      const { data } = await api.post('/propuestas/votar', { propuesta_id: id, opcion })
      setVotoToken(data.token as string)
      window.setTimeout(() => setVotoToken(null), 6000)
    } catch (err: unknown) {
      setError(`Votar: ${mensajeDe(err)}`)
    } finally {
      cargar()
    }
  }

  async function rechazar(id: string) {
    const motivo = window.prompt('Motivo del rechazo (opcional):') ?? 'Sin justificación'
    await accion('/propuestas/rechazar', { propuesta_id: id, motivo }, 'Rechazar')
  }

  const mostrarVotos = (p: Propuesta) => (
    <div className="vue">
      <div className="voto-box"><b>{p.votos?.a_favor ?? 0}</b>A favor</div>
      <div className="voto-box"><b>{p.votos?.en_contra ?? 0}</b>En contra</div>
      <div className="voto-box"><b>{p.votos?.abstencion ?? 0}</b>Abstención</div>
    </div>
  )

  return (
    <div>
      <h1 className="page-title">Propuestas de la Asociación</h1>
      <p className="page-sub">Ciclo de vida: Borrador → Validada → En votación → Cerrada</p>

      {error && <div className="error-box">{error}</div>}
      {votoToken && (
        <div className="card" style={{ borderColor: 'var(--verde)', borderLeft: '4px solid var(--verde)', padding: 14 }}>
          <b style={{ color: 'var(--verde)' }}>Voto emitido.</b>{' '}
          <span style={{ fontSize: 13 }}>Tu token pseudónimo: <code>{votoToken}</code></span>
        </div>
      )}

      <div className="card" style={{ marginBottom: 24 }}>
        <strong>Estados posibles</strong>
        <div className="steps" style={{ marginTop: 12 }}>
          {PASOS.map((s, i) => (
            <div key={s} className={`step ${i === 0 ? 'react' : ''}`}>
              {i + 1} · {s}
            </div>
          ))}
          <div className="step">5 · rechazada</div>
        </div>
      </div>

      {puede.crear && (
        <div className="card" style={{ marginBottom: 24 }}>
          {!mostrarNueva ? (
            <button className="btn btn-primary" onClick={() => setMostrarNueva(true)}>
              + Nueva propuesta
            </button>
          ) : (
            <form onSubmit={crearPropuesta}>
              <div className="field">
                <label>Título</label>
                <input
                  value={nueva.titulo}
                  onChange={(e) => setNueva({ ...nueva, titulo: e.target.value })}
                  placeholder="Título de la propuesta"
                />
              </div>
              <div className="field">
                <label>Descripción</label>
                <textarea
                  value={nueva.descripcion}
                  onChange={(e) => setNueva({ ...nueva, descripcion: e.target.value })}
                  rows={3}
                  placeholder="Detalle de la propuesta"
                />
              </div>
              <div style={{ display: 'flex', gap: 8 }}>
                <button className="btn btn-primary" type="submit">Crear</button>
                <button className="btn btn-ghost" type="button" onClick={() => setMostrarNueva(false)}>
                  Cancelar
                </button>
              </div>
            </form>
          )}
        </div>
      )}

      {props.length === 0 && <div className="vacio">Aún no hay propuestas.</div>}

      {props.map((p) => (
        <div key={p.id} className="card">
          <div className="card-header">
            <span className="prop-titulo">{p.titulo}</span>
            <span className={`pill estado-${p.estado}`}>{p.estado}</span>
          </div>

          <div className="prop-meta">
            #{p.id} · por <b>{p.autor}</b>
            {p.quorum > 0 && p.estado === 'en_votacion' && <> · quorum {p.quorum}</>}
          </div>

          {p.descripcion && (
            <p style={{ fontSize: 14, color: '#475569', marginBottom: 8 }}>
              {p.descripcion.split('\n')[0]}
            </p>
          )}

          {(p.estado === 'borrador' || p.estado === 'validada') && (
            <>
              <div className="endos-num">
                Endosos: <b>{p.endosos}</b>/{p.endosos_minimo}
              </div>
              <div className="bar">
                <div style={{ width: `${Math.min(100, (p.endosos / p.endosos_minimo) * 100)}%` }} />
              </div>
            </>
          )}

          {p.estado === 'rechazada' && p.motivo_rechazo && (
            <div className="motivo">Rechazada: {p.motivo_rechazo}</div>
          )}

          {(p.estado === 'en_votacion' || p.estado === 'cerrada') && mostrarVotos(p)}

          <div className="prop-actions">
            {puede.endosar && p.estado === 'borrador' && (
              <button className="btn btn-success" onClick={() => accion('/propuestas/endosar', { propuesta_id: p.id }, 'Endosar')}>
                Endosar
              </button>
            )}
            {puede.rechazar && (p.estado === 'borrador' || p.estado === 'validada') && (
              <button className="btn btn-danger" onClick={() => rechazar(p.id)}>
                Rechazar
              </button>
            )}
            {puede.abrir && p.estado === 'validada' && (
              <span style={{ display: 'inline-flex', alignItems: 'center', gap: 8 }}>
                <input
                  type="number"
                  value={quorum}
                  min={1}
                  max={50}
                  onChange={(e) => setQuorum(Number(e.target.value))}
                  style={{ width: 70, padding: 8, borderRadius: 8, border: '1px solid var(--borde)' }}
                />
                <button className="btn btn-primary" onClick={() => accion('/propuestas/abrir', { propuesta_id: p.id, quorum }, 'Abrir votación')}>
                  Abrir votación
                </button>
              </span>
            )}
            {puede.votar && p.estado === 'en_votacion' && (
              <>
                <button className="btn btn-success" onClick={() => votar(p.id, 'a_favor')}>A favor</button>
                <button className="btn btn-danger" onClick={() => votar(p.id, 'en_contra')}>En contra</button>
                <button className="btn btn-ghost" onClick={() => votar(p.id, 'abstencion')}>Abstención</button>
              </>
            )}
            {puede.abrir && p.estado === 'en_votacion' && (
              <button className="btn btn-warn" onClick={() => accion('/propuestas/cerrar', { propuesta_id: p.id }, 'Cerrar y contar')}>
                Cerrar y contar
              </button>
            )}
          </div>
        </div>
      ))}
    </div>
  )
}