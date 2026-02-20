import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './context/AuthContext'
import Layout from './components/Layout'
import Login from './views/Login'
import Register from './views/Register'
import SolicitudForm from './views/SolicitudForm'
import SolicitudesList from './views/SolicitudesList'

function PrivateRoute({ children }) {
  const { isAuthenticated, loading } = useAuth()
  if (loading) return <div style={{ padding: 20 }}>Cargando...</div>
  if (!isAuthenticated) return <Navigate to="/login" replace />
  return children
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route
        path="/"
        element={
          <PrivateRoute>
            <Layout />
          </PrivateRoute>
        }
      >
        <Route index element={<Navigate to="/solicitudes" replace />} />
        <Route path="solicitudes" element={<SolicitudesList />} />
        <Route path="solicitudes/nueva" element={<SolicitudForm />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
