from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chatbot import OrientadorUniversitarioChatbot
from models import ChatRequest, ChatResponse
from utils import HistorialConversacion
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Habilitar CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir a ["http://localhost:5173"] si usas Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancia global del chatbot
chatbot = OrientadorUniversitarioChatbot()

# Instancia global del historial
historial = HistorialConversacion()

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """Endpoint para recibir intereses, habilidades e historial y devolver recomendación."""
    # Autor: Angel Hernandez
    try:
        respuesta = chatbot.responder(request.intereses, request.habilidades, request.historial)
        historial.agregar({"intereses": request.intereses, "habilidades": request.habilidades, "historial": request.historial, "respuesta": respuesta.dict()})
        return respuesta
    except Exception as e:
        print("ERROR EN /chat:", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
def get_history():
    """Devuelve el historial de conversación."""
    # Autor: Angel Hernandez
    return historial.obtener()

@app.post("/reset")
def reset_history():
    """Limpia el historial de conversación."""
    # Autor: Angel Hernandez
    historial.limpiar()
    return {"mensaje": "Historial limpiado"} 