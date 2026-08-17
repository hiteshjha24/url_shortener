import { Link } from 'react-router-dom'

export function NotFoundPage() {
  return (
    <div className="page-card not-found-box">
      <h1>404</h1>
      <p>This page does not exist or the short link has expired.</p>
      <Link to="/" className="primary-button">
        Back home
      </Link>
    </div>
  )
}
