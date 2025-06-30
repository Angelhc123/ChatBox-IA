import { useState } from 'react'
import ChatBubble from './components/ChatBubble'
import ChatInput from './components/ChatInput'
import iaAvatar from './assets/ia-avatar.png'
import './App.css'

interface Mensaje {
  texto: string
  from: 'user' | 'ia'
}

function App() {
  const [mensajes, setMensajes] = useState<Mensaje[]>([{
    texto: '¡Hola! Soy tu orientador universitario virtual. ¿Cómo te llamas?',
    from: 'ia',
  }])
  const [loading, setLoading] = useState(false)

  const handleSend = async (msg: string) => {
    const nuevoMensaje: Mensaje = { texto: msg, from: 'user' }
    setMensajes(m => [...m, nuevoMensaje])
    setLoading(true)
    try {
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          intereses: [], // Opcional: puedes extraer de los mensajes si quieres
          habilidades: [], // Opcional: puedes extraer de los mensajes si quieres
          historial: [...mensajes, nuevoMensaje].map(m => ({ mensaje: m.texto, from: m.from })),
        }),
      })
      const data = await res.json()
      setMensajes(m => [...m, { texto: data.recomendacion, from: 'ia' }])
    } catch (e) {
      setMensajes(m => [...m, { texto: 'Ocurrió un error al consultar la IA. Intenta de nuevo más tarde.', from: 'ia' }])
    }
    setLoading(false)
  }

  return (
    <div className="main-bg">
      <div className="info-panel">
        <div className="ai-profile">
          <img 
            src={iaAvatar} 
            alt="ChatiU Avatar" 
            className="ai-avatar-large"
          />
          <h1>ChatiU</h1>
          <p>
            Tu orientador universitario virtual inteligente. 
            Creado para ayudarte a descubrir la carrera perfecta 
            basándome en tus intereses, habilidades y valores personales.
          </p>
        </div>
      </div>
      <div className="chat-area">
        <div className="chat-card">
          <div className="chat-header">
            <span>chatiU</span>
            <span role="img" aria-label="robot">🤖</span>
          </div>
          <div className="chat-window">
            {mensajes.map((msg, i) => (
              <ChatBubble key={i} message={msg.texto} from={msg.from} />
            ))}
          </div>
          <div className="input-bar">
            <ChatInput
              onSend={handleSend}
              placeholder="Escribe tu mensaje..."
              disabled={loading}
            />
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
