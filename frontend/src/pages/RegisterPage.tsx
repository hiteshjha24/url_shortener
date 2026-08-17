import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { AuthForm } from '../components/Forms'
import { useAuth } from '../context/AuthContext'

export function RegisterPage() {
  const navigate = useNavigate()
  const { register, login, isAuthenticated } = useAuth()

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard', { replace: true })
    }
  }, [isAuthenticated, navigate])

  return (
    <AuthForm
      title="Create your account"
      subtitle="Start shortening links instantly with a faster workflow."
      submitLabel="Register"
      onSubmit={async (email, password) => {
        await register(email, password)
        await login(email, password)
        navigate('/dashboard')
      }}
      alternateText="Already have an account? Login"
      alternateAction={() => navigate('/login')}
    />
  )
}
