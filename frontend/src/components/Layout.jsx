import { Outlet, NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import styles from './Layout.module.css'

export default function Layout() {
  const { logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className={styles.layout}>
      <header className={styles.header}>
        <nav>
          <NavLink to="/solicitudes" end className={({ isActive }) => (isActive ? styles.active : '')}>
            Mis solicitudes
          </NavLink>
          <NavLink to="/solicitudes/nueva" className={({ isActive }) => (isActive ? styles.active : '')}>
            Nueva solicitud
          </NavLink>
        </nav>
        <button type="button" onClick={handleLogout} className={styles.logout}>
          Cerrar sesión
        </button>
      </header>
      <main className={styles.main}>
        <Outlet />
      </main>
    </div>
  )
}
