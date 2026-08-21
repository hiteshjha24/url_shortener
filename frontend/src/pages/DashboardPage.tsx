import { useEffect, useState } from 'react'
import { api } from '../api/client'
import { useAuth } from '../context/AuthContext'
import type { UrlRecord } from '../types'

const formatDate = (value: string | null) => {
  if (!value) return 'No expiry'
  return new Date(value).toLocaleString([], {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })
}

export function DashboardPage() {
  const { token } = useAuth()
  const [urls, setUrls] = useState<UrlRecord[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [search, setSearch] = useState('')

  const loadUrls = async () => {
    if (!token) return
    setLoading(true)
    try {
      const data = await api.getMyUrls(token)
      setUrls(data)
      setError('')
    } catch (loadError) {
      setError(loadError instanceof Error ? loadError.message : 'Unable to load your URLs.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    void loadUrls()
  }, [token])

  const filteredUrls = urls.filter((url) => {
    const query = search.toLowerCase()
    return (
      url.target_url.toLowerCase().includes(query) ||
      url.short_code.toLowerCase().includes(query) ||
      url.short_url.toLowerCase().includes(query)
    )
  })

  const totals = {
    urls: urls.length,
    active: urls.filter((item) => item.is_active).length,
    clicks: urls.reduce((total, item) => total + item.clicks, 0),
  }

  const handleDelete = async (shortCode: string) => {
    if (!token) return
    const confirmed = window.confirm('Deactivate this short URL?')
    if (!confirmed) return

    try {
      await api.deleteUrl(shortCode, token)
      setUrls((current) => current.filter((item) => item.short_code !== shortCode))
    } catch (deleteError) {
      window.alert(deleteError instanceof Error ? deleteError.message : 'Could not delete URL.')
    }
  }

  if (loading) {
    return <div className="page-card loading-card">Loading your short links…</div>
  }

  return (
    <div className="dashboard-page">
      <div className="dashboard-heading">
        <div>
          <span className="eyebrow">Your workspace</span>
          <h1>Link performance, at a glance.</h1>
        </div>
        <span className="dashboard-caption">Manage every destination from one calm, focused space.</span>
      </div>
      <div className="stats-grid">
        <div className="stat-card">
          <span>Total links</span>
          <strong>{totals.urls}</strong>
        </div>
        <div className="stat-card">
          <span>Active</span>
          <strong>{totals.active}</strong>
        </div>
        <div className="stat-card">
          <span>Total clicks</span>
          <strong>{totals.clicks}</strong>
        </div>
      </div>

      <div className="page-card">
        <div className="table-header">
          <div>
            <h2>Your URLs</h2>
          </div>
          <input
            type="search"
            placeholder="Search links"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
          />
        </div>

        {error ? <div className="form-error">{error}</div> : null}

        {filteredUrls.length === 0 ? (
          <div className="empty-state">
            <h3>No URLs yet</h3>
            <p>Create your first shortened link from the home page.</p>
          </div>
        ) : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Destination</th>
                  <th>Short link</th>
                  <th>Clicks</th>
                  <th>Expires</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredUrls.map((url) => (
                  <tr key={url.short_code}>
                    <td className="destination-cell">
                      <a href={url.target_url} target="_blank" rel="noreferrer">
                        {url.target_url}
                      </a>
                    </td>
                    <td>
                      <a href={url.short_url} target="_blank" rel="noreferrer">
                        {url.short_url}
                      </a>
                    </td>
                    <td>{url.clicks}</td>
                    <td>{formatDate(url.expires_at)}</td>
                    <td className="action-cell">
                      <a href={url.short_url} target="_blank" rel="noreferrer" className="table-button primary-button small-button">
                        Open
                      </a>
                      <button
                        type="button"
                        className="table-button secondary-button small-button"
                        onClick={async () => {
                          await navigator.clipboard.writeText(url.short_url)
                          window.alert('Copied short URL.')
                        }}
                      >
                        Copy
                      </button>
                      <button
                        type="button"
                        className="table-button danger-button small-button"
                        onClick={() => void handleDelete(url.short_code)}
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}
