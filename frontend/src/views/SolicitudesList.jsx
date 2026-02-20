import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getSolicitudes } from '../services/api'
import styles from './SolicitudesList.module.css'

function formatDate(d) {
  if (!d) return '-'
  const date = new Date(d)
  return date.toLocaleDateString('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export default function SolicitudesList() {
  const [data, setData] = useState({ items: [], total: 0, page: 1, page_size: 10, pages: 0 })
  const [loading, setLoading] = useState(true)
  const [page, setPage] = useState(1)
  const pageSize = 10

  useEffect(() => {
    setLoading(true)
    getSolicitudes(page, pageSize)
      .then(setData)
      .catch(() => setData({ items: [], total: 0, page: 1, page_size: pageSize, pages: 0 }))
      .finally(() => setLoading(false))
  }, [page])

  return (
    <div className={styles.wrapper}>
      <div className={styles.header}>
        <h1>Mis solicitudes</h1>
        <Link to="/solicitudes/nueva" className={styles.newBtn}>
          Nueva solicitud
        </Link>
      </div>

      {loading ? (
        <p>Cargando...</p>
      ) : data.items.length === 0 ? (
        <p className={styles.empty}>
          No tienes solicitudes. <Link to="/solicitudes/nueva">Crear una</Link>
        </p>
      ) : (
        <>
          <table className={styles.table}>
            <thead>
              <tr>
                <th>Medicamento</th>
                <th>Tipo</th>
                <th>Fecha</th>
              </tr>
            </thead>
            <tbody>
              {data.items.map((s) => (
                <tr key={s.id}>
                  <td>{s.medicamento_nombre}</td>
                  <td>{s.es_no_pos ? 'NO POS' : 'POS'}</td>
                  <td>{formatDate(s.creado_en)}</td>
                </tr>
              ))}
            </tbody>
          </table>

          {data.pages > 1 && (
            <div className={styles.pagination}>
              <button
                type="button"
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page <= 1}
              >
                Anterior
              </button>
              <span>
                Página {data.page} de {data.pages} ({data.total} total)
              </span>
              <button
                type="button"
                onClick={() => setPage((p) => Math.min(data.pages, p + 1))}
                disabled={page >= data.pages}
              >
                Siguiente
              </button>
            </div>
          )}
        </>
      )}
    </div>
  )
}
