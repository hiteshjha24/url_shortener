import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { api } from '../api/client'
import { useState } from 'react'

export function HomePage() {
  const { isAuthenticated, token } = useAuth()
  const navigate = useNavigate()
  const [targetUrl, setTargetUrl] = useState('')
  const [customAlias, setCustomAlias] = useState('')
  const [expiresInDays, setExpiresInDays] = useState('')
  const [result, setResult] = useState<{ short_url: string; short_code: string } | null>(null)
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault()
    setError('')
    setIsSubmitting(true)

    try {
      const payload = {
        target_url: targetUrl,
        custom_alias: customAlias.trim() || null,
        expires_in_days: expiresInDays ? Number(expiresInDays) : null,
      }

      const created = await api.createShortUrl(payload, token ?? undefined)
      setResult({ short_url: created.short_url, short_code: created.short_code })
      setTargetUrl('')
      setCustomAlias('')
      setExpiresInDays('')
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : 'Could not shorten this URL.')
    } finally {
      setIsSubmitting(false)
    }
  }

  async function handleCopy() {
    if (!result) return
    await navigator.clipboard.writeText(result.short_url)
    setError('')
    window.alert('Short URL copied to clipboard.')
  }

  return (
    <div className="home-page">
      <section className="hero-panel">
        <div className="hero-copy">
          <span className="eyebrow">Fast links for modern teams</span>
          <h1>Turn long links into high-converting short URLs.</h1>
          <p>
            Create precise, trackable links in seconds. Built for speed, trust, and reliability.
          </p>

          <div className="hero-actions">
            {isAuthenticated ? (
              <button type="button" className="primary-button" onClick={() => navigate('/dashboard')}>
                Open dashboard
              </button>
            ) : (
              <>
                <Link to="/login" className="primary-button">
                  Login
                </Link>
                <Link to="/register" className="secondary-button">
                  Create account
                </Link>
              </>
            )}
          </div>
        </div>

        <form className="shortener-card" onSubmit={handleSubmit}>
          <div className="field-group">
            <label htmlFor="target_url">Original URL</label>
            <input
              id="target_url"
              type="url"
              placeholder="https://example.com/very/long/path"
              value={targetUrl}
              onChange={(event) => setTargetUrl(event.target.value)}
              required
            />
          </div>

          <div className="inline-fields">
            <div className="field-group">
              <label htmlFor="custom_alias">Custom alias</label>
              <input
                id="custom_alias"
                type="text"
                placeholder="optional"
                maxLength={10}
                value={customAlias}
                onChange={(event) => setCustomAlias(event.target.value)}
              />
            </div>

            <div className="field-group">
              <label htmlFor="expires_in_days">Expires in</label>
              <input
                id="expires_in_days"
                type="number"
                min="1"
                placeholder="days"
                value={expiresInDays}
                onChange={(event) => setExpiresInDays(event.target.value)}
              />
            </div>
          </div>

          {error ? <div className="form-error">{error}</div> : null}

          <button type="submit" className="primary-button" disabled={isSubmitting}>
            {isSubmitting ? 'Shortening…' : 'Create short URL'}
          </button>

          {result ? (
            <div className="result-box" aria-live="polite">
              <div>
                <span className="small-label">Your short link</span>
                <a href={result.short_url} target="_blank" rel="noreferrer">
                  {result.short_url}
                </a>
              </div>
              <div className="result-actions">
                <button type="button" className="secondary-button" onClick={handleCopy}>
                  Copy
                </button>
                <a href={result.short_url} target="_blank" rel="noreferrer" className="primary-button inline-link">
                  Open
                </a>
              </div>
            </div>
          ) : null}
        </form>
      </section>
    </div>
  )
}
