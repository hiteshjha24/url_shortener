import { Link, NavLink } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

type LayoutProps = {
  children: React.ReactNode
}

export function Layout({ children }: LayoutProps) {
  const { isAuthenticated, logout, userEmail } = useAuth()

  return (
    <div className="app-shell">
      <div className="ambient ambient-one" aria-hidden="true" />
      <div className="ambient ambient-two" aria-hidden="true" />
      <header className="topbar">
        <div className="brand-wrap">
          <Link to="/" className="brand" aria-label="Go to home">
            <span className="brand-mark">D</span>
            <span className="brand-name">Dock-URL</span>
          </Link>
        </div>

        <nav className="main-nav" aria-label="Primary navigation">
          <NavLink to="/" end>
            Home
          </NavLink>
          {isAuthenticated ? (
            <>
              <NavLink to="/dashboard">Dashboard</NavLink>
              <button className="nav-button" type="button" onClick={logout}>
                Logout
              </button>
            </>
          ) : (
            <>
              <NavLink to="/login">Login</NavLink>
              <NavLink to="/register">Register</NavLink>
            </>
          )}
        </nav>

        {isAuthenticated && userEmail ? (
          <div className="user-chip" aria-label="Authenticated user">
            <span className="user-dot" aria-hidden="true" />
            {userEmail}
          </div>
        ) : null}
      </header>

      <main className="page-shell">{children}</main>
    </div>
  )
}
