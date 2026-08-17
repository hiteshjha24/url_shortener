import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { AuthForm } from '../components/Forms'
import { useAuth } from '../context/AuthContext'

export function LoginPage() {
  const navigate = useNavigate()
  const { login, isAuthenticated } = useAuth()

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard', { replace: true })
    }
  }, [isAuthenticated, navigate])

  return (
    <AuthForm
      title="Welcome back"
      subtitle="Sign in to manage your links and analytics."
      submitLabel="Login"
      onSubmit={async (email, password) => {
        await login(email, password)
        navigate('/dashboard')
      }}
      alternateText="Need an account? Create one"
      alternateAction={() => navigate('/register')}
    />
  )
}
