import { useState } from 'react'
import Router from 'next/router'

export default function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)

  async function submit(e) {
    e.preventDefault()
    setError(null)
    try {
      const res = await fetch('http://localhost:8000/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      })
      if (!res.ok) throw new Error('Credenciais inválidas')
      const data = await res.json()
      localStorage.setItem('jarvis_token', data.access_token)
      Router.push('/')
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <main style={{padding:20}}>
      <h2>Login Jarvis</h2>
      <form onSubmit={submit}>
        <div>
          <label>Username</label>
          <input value={username} onChange={e=>setUsername(e.target.value)} />
        </div>
        <div>
          <label>Password</label>
          <input type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        </div>
        <button type="submit">Entrar</button>
        {error && <p style={{color:'red'}}>{error}</p>}
      </form>
    </main>
  )
}
