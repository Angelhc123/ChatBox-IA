from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    """Modelo de entrada para el endpoint de chat."""
    # Autor: Angel Hernandez
    intereses: List[str]
    habilidades: List[str]
    historial: List[dict] = []  # Nuevo campo para el historial de mensajes

class ChatResponse(BaseModel):
    """Modelo de salida estructurada para la respuesta del chatbot."""
    # Autor: Angel Hernandez
    recomendacion: str
    carreras_sugeridas: List[str]
    razonamiento: Optional[str] = None 