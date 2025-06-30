from typing import List, Dict

class HistorialConversacion:
    """
    Maneja el historial de la conversación del chatbot.
    Autor: Angel Hernandez
    """
    def __init__(self):
        # Autor: Angel Hernandez
        self.historial: List[Dict] = []

    def agregar(self, entrada: Dict):
        # Autor: Angel Hernandez
        self.historial.append(entrada)

    def obtener(self) -> List[Dict]:
        # Autor: Angel Hernandez
        return self.historial

    def limpiar(self):
        # Autor: Angel Hernandez
        self.historial = [] 