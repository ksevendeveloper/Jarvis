import { useEffect, useState } from 'react'
import io from 'socket.io-client'

export default function Home(){
  const [token, setToken] = useState(null)
  const [events, setEvents] = useState([])
  const [connected, setConnected] = useState(false)

  useEffect(()=>{
    const t = localStorage.getItem('jarvis_token')
    setToken(t)
    if (!t) return
    const socket = io('http://localhost:8000', { auth: { token: t } })
    socket.on('connect', ()=> setConnected(true))
    socket.on('disconnect', ()=> setConnected(false))
    socket.onAny((ev, data)=> setEvents(prev=>[{ev,data}, ...prev].slice(0,20)))
    return ()=> socket.disconnect()
  }, [])

  if (!token) {
    return (<main style={{padding:20}}>
      <h2>Jarvis - Painel</h2>
      <p>Você precisa <a href="/login">entrar</a> primeiro.</p>
    </main>)
  }

  return (
    <main style={{padding:20}}>
      <h2>Jarvis - Painel</h2>
      <p>Socket: {connected? 'conectado': 'desconectado'}</p>
      <section>
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
