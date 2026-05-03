import { useEffect, useState } from 'react'
import io from 'socket.io-client'

export default function Home(){
  const [token, setToken] = useState(null)
  const [events, setEvents] = useState([])
  const [connected, setConnected] = useState(false)
  const [mode, setMode] = useState('idle')

  useEffect(()=>{
    const t = localStorage.getItem('jarvis_token')
    setToken(t)
    if (!t) return
    const socket = io('http://localhost:8000', { auth: { token: t } })
    socket.on('connect', ()=> setConnected(true))
    socket.on('disconnect', ()=> setConnected(false))
    socket.onAny((ev, data)=> {
      if (ev === 'executing') setMode('executing')
      else if (ev === 'success') setMode('success')
      else if (ev === 'error') setMode('error')
      else if (ev === 'status') setMode('online')
      setEvents(prev=>[{ev,data}, ...prev].slice(0,20))
    })
    return ()=> socket.disconnect()
  }, [])

  if (!token) {
    return (<main className="jarvis-page">
      <h2>Jarvis - Painel</h2>
      <p>Você precisa <a href="/login">entrar</a> primeiro.</p>
    </main>)
  }

  const displayState = connected ? mode : 'offline'

  return (
    <main className="jarvis-page">
      <h2>Jarvis - Painel</h2>
      <p>Socket: {connected? 'conectado': 'desconectado'}</p>

      <section className="jarvis-visual-wrap">
        <div className={`jarvis-core is-${displayState}`}>
          <div className="jarvis-core-inner" />
        </div>
        <p className="jarvis-state-label">Estado atual: {displayState}</p>
      </section>

      <section className="jarvis-events">
        <h3>Eventos recentes</h3>
        <ul>
          {events.map((it, idx)=> (
            <li key={idx}><strong>{it.ev}</strong>: {JSON.stringify(it.data)}</li>
          ))}
        </ul>
      </section>
    </main>
  )
}
