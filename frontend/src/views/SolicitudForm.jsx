import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { getMedicamentos, crearSolicitud } from '../services/api'
import styles from './SolicitudForm.module.css'

export default function SolicitudForm() {
  const [medicamentos, setMedicamentos] = useState([])
  const [medicamentoId, setMedicamentoId] = useState('')
  const [numeroOrden, setNumeroOrden] = useState('')
  const [direccion, setDireccion] = useState('')
  const [telefono, setTelefono] = useState('')
  const [correo, setCorreo] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [loadingMed, setLoadingMed] = useState(true)
  const navigate = useNavigate()

  const medicamentoSeleccionado = medicamentos.find((m) => m.id === Number(medicamentoId))
  const esNoPos = medicamentoSeleccionado && !medicamentoSeleccionado.es_pos

  useEffect(() => {
    getMedicamentos()
      .then((data) => setMedicamentos(data.items || []))
      .catch(() => setMedicamentos([]))
      .finally(() => setLoadingMed(false))
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    if (!medicamentoId) {
      setError('Selecciona un medicamento')
      return
    }
    if (esNoPos && (!numeroOrden?.trim() || !direccion?.trim() || !telefono?.trim() || !correo?.trim())) {
      setError('Para medicamentos NO POS son obligatorios: número de orden, dirección, teléfono y correo.')
      return
    }
    setLoading(true)
    try {
      await crearSolicitud({
        medicamento_id: Number(medicamentoId),
        ...(esNoPos && {
          numero_orden: numeroOrden.trim(),
          direccion: direccion.trim(),
          telefono: telefono.trim(),
          correo: correo.trim(),
        }),
      })
      navigate('/solicitudes')
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al crear la solicitud')
    } finally {
      setLoading(false)
    }
  }

  if (loadingMed) return <p>Cargando medicamentos...</p>

  return (
    <div className={styles.wrapper}>
      <h1>Nueva solicitud de medicamento</h1>
      <form onSubmit={handleSubmit} className={styles.form}>
        {error && <div className={styles.error}>{error}</div>}
        <label>
          Medicamento *
          <select
            value={medicamentoId}
            onChange={(e) => setMedicamentoId(e.target.value)}
            required
          >
            <option value="">Seleccione un medicamento</option>
            {medicamentos.map((m) => (
              <option key={m.id} value={m.id}>
                {m.nombre} {m.es_pos ? '(POS)' : '(NO POS)'}
              </option>
            ))}
          </select>
        </label>

        {esNoPos && (
          <div className={styles.noPos}>
            <h3>Datos adicionales (NO POS)</h3>
            <label>
              Número de orden *
              <input
                type="text"
                value={numeroOrden}
                onChange={(e) => setNumeroOrden(e.target.value)}
                required
                placeholder="Número de orden"
              />
            </label>
            <label>
              Dirección *
              <input
                type="text"
                value={direccion}
                onChange={(e) => setDireccion(e.target.value)}
                required
                placeholder="Dirección"
              />
            </label>
            <label>
              Teléfono *
              <input
                type="tel"
                value={telefono}
                onChange={(e) => setTelefono(e.target.value)}
                required
                placeholder="Teléfono"
              />
            </label>
            <label>
              Correo electrónico *
              <input
                type="email"
                value={correo}
                onChange={(e) => setCorreo(e.target.value)}
                required
                placeholder="Correo"
              />
            </label>
          </div>
        )}

        <div className={styles.actions}>
          <button type="button" onClick={() => navigate('/solicitudes')} className={styles.cancel}>
            Cancelar
          </button>
          <button type="submit" disabled={loading}>
            {loading ? 'Enviando...' : 'Enviar solicitud'}
          </button>
        </div>
      </form>
    </div>
  )
}
