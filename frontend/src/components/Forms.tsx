import { useState } from 'react'

type AuthFormProps = {
  title: string
  subtitle: string
  onSubmit: (email: string, password: string) => Promise<void>
  submitLabel: string
  alternateText?: string
  alternateAction?: () => void
}

export function AuthForm({ title, subtitle, onSubmit, submitLabel, alternateText, alternateAction }: AuthFormProps) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    setIsSubmitting(true)

    try {
      await onSubmit(email, password)
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : 'Unable to continue.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="auth-shell">
      <div className="auth-card">
        <div className="eyebrow">Secure access</div>
        <h1>{title}</h1>
        <p className="subtitle">{subtitle}</p>

        <form onSubmit={handleSubmit} className="stack-form">
          <label>
            <span>Email</span>
            <input
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              placeholder="you@example.com"
              required
            />
          </label>

          <label>
            <span>Password</span>
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="••••••••"
              required
            />
          </label>

          {error ? <div className="form-error">{error}</div> : null}

          <button type="submit" className="primary-button" disabled={isSubmitting}>
            {isSubmitting ? 'Please wait…' : submitLabel}
          </button>
        </form>

        {alternateText && alternateAction ? (
          <button type="button" className="text-button" onClick={alternateAction}>
            {alternateText}
          </button>
        ) : null}
      </div>
    </div>
  )
}
