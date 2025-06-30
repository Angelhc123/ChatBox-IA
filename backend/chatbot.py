from typing import List
from models import ChatResponse
import google.generativeai as genai

class OrientadorUniversitarioChatbot:
    """
    Chatbot orientador universitario basado en intereses y habilidades.
    Autor: Angel Hernandez
    """
    def __init__(self):
        # Autor: Angel Hernandez
        self.system_message = (
            "Eres un orientador universitario experto. Ayudas a estudiantes a elegir carreras "
            "basado en sus intereses y habilidades."
        )
        self.historial = []
        # Configurar Gemini con la API Key proporcionada
        genai.configure(api_key="API_KEY_AQUI")
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def construir_prompt(self, intereses: List[str], habilidades: List[str], historial: list = None) -> str:
        """
        Construye el prompt para el modelo de IA combinando cadenas, mensajes e historial.
        Extrae el nombre del usuario del historial si está disponible.
        """
        if historial is None:
            historial = []
        intereses_str = ', '.join(intereses)
        habilidades_str = ', '.join(habilidades)
        # Extraer nombre del usuario del historial
        nombre_usuario = None
        for h in historial:
            if h.get('from') == 'user':
                # Busca frases tipo "me llamo ..." o "soy ..." o simplemente un nombre
                import re
                mensaje = h.get('mensaje', '')
                match = re.search(r"me llamo ([a-zA-ZáéíóúÁÉÍÓÚñÑ ]+)", mensaje, re.IGNORECASE)
                if match:
                    nombre_usuario = match.group(1).strip()
                    break
                match = re.search(r"soy ([a-zA-ZáéíóúÁÉÍÓÚñÑ ]+)", mensaje, re.IGNORECASE)
                if match:
                    nombre_usuario = match.group(1).strip()
                    break
                # Si es una respuesta corta que parece un nombre (solo letras)
                if re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$', mensaje.strip()) and len(mensaje.strip().split()) <= 3:
                    nombre_usuario = mensaje.strip()
                    break
        
        prompt = (
            f"{self.system_message}\n"
            f"Contexto del usuario: {nombre_usuario if nombre_usuario else '[sin nombre]'}\n"
            f"Historial de conversación: {historial}\n\n"
            "INSTRUCCIONES PARA EL ORIENTADOR:\n"
            "1. Eres un orientador universitario amigable y profesional\n"
            "2. Debes recopilar esta información en orden:\n"
            "   - Nombre del estudiante\n"
            "   - Sus materias o temas de interés\n"
            "   - Sus hobbies o actividades en tiempo libre\n"
            "   - Sus valores o lo que más disfruta en la vida\n"
            "   - Su ubicación (país, ciudad, estado/departamento) - SI EL USUARIO PREFIERE NO DECIR SU UBICACIÓN, NO INSISTAS\n"
            "3. Para detectar la ubicación, acepta cualquier mención de:\n"
            "   - Países: México, Colombia, Argentina, España, Perú, Chile, Venezuela, Ecuador, etc.\n"
            "   - Ciudades: CDMX, Guadalajara, Bogotá, Madrid, Lima, Buenos Aires, etc.\n"
            "   - Estados/Departamentos: Jalisco, Antioquia, Nuevo León, Andalucía, etc.\n"
            "   - Respuestas de privacidad: 'prefiero no decir', 'no quiero compartir', 'privado', etc.\n"
            "4. Una vez que tengas toda la información, proporciona 3 recomendaciones de carreras\n"
            "5. NO repitas preguntas si ya tienes la información\n"
            "6. Acepta cualquier respuesta del usuario como válida\n"
            "7. Para la ubicación, sé flexible y acepta respuestas breves o indirectas\n"
            "8. Cuando des las recomendaciones, usa este formato:\n\n"
            "**🎓 RECOMENDACIONES DE CARRERAS PARA [NOMBRE]**\n\n"
            "**1. [Nombre de la Carrera]**\n"
            "• Compatibilidad: [70-95]%\n"
            "• Campo laboral: [descripción]\n"
            "• Duración: [años]\n"
            "• Sueldo promedio: $[cantidad] MXN mensuales\n"
            "• Universidades recomendadas: [2 universidades cercanas a su ubicación o universidades destacadas si no proporcionó ubicación]\n\n"
            "**2. [Nombre de la Carrera]**\n"
            "• Compatibilidad: [70-95]%\n"
            "• Campo laboral: [descripción]\n"
            "• Duración: [años]\n"
            "• Sueldo promedio: $[cantidad] MXN mensuales\n"
            "• Universidades recomendadas: [2 universidades cercanas a su ubicación o universidades destacadas si no proporcionó ubicación]\n\n"
            "**3. [Nombre de la Carrera]**\n"
            "• Compatibilidad: [70-95]%\n"
            "• Campo laboral: [descripción]\n"
            "• Duración: [años]\n"
            "• Sueldo promedio: $[cantidad] MXN mensuales\n"
            "• Universidades recomendadas: [2 universidades cercanas a su ubicación o universidades destacadas si no proporcionó ubicación]\n\n"
            "IMPORTANTE SOBRE UBICACIÓN Y UNIVERSIDADES:\n"
            "- Analiza el historial para detectar si el usuario mencionó alguna ubicación\n"
            "- Si detectas ubicación específica, recomienda 2 universidades de esa región/país\n"
            "- Si no hay ubicación o prefiere privacidad, recomienda universidades reconocidas internacionalmente\n"
            "- Ejemplos de universidades por región:\n"
            "  * México: UNAM, IPN, Tec de Monterrey, UAM, Universidad de Guadalajara, ITESM\n"
            "  * Colombia: Universidad Nacional, Javeriana, Los Andes, Universidad del Norte\n"
            "  * Argentina: UBA, UCA, UTDT, Universidad de Córdoba\n"
            "  * España: UCM, UAM, UPM, Universidad de Barcelona\n"
            "  * Perú: UNMSM, PUCP, Universidad de Lima\n"
            "  * Chile: Universidad de Chile, PUC Chile, Universidad de Concepción\n"
            "- Incluye al menos una universidad pública y una privada cuando sea posible\n"
            "- Sé específico con los nombres completos de las universidades\n\n"
            "Responde de forma natural y progresiva."
        )
        return prompt

    def responder(self, intereses: List[str], habilidades: List[str], historial: list = None) -> ChatResponse:
        """
        Ejecuta la cadena de pensamiento y retorna una respuesta estructurada usando Gemini.
        Autor: Angel Hernandez
        """
        if historial is None:
            historial = []
        prompt = self.construir_prompt(intereses, habilidades, historial)
        self.historial.append({"intereses": intereses, "habilidades": habilidades, "historial": historial})
        response = self.model.generate_content(prompt)
        # Intentar extraer JSON de la respuesta
        import json, re
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(0))
                # Adaptar a ChatResponse
                carreras = data.get('carreras_sugeridas', [])
                if carreras and isinstance(carreras[0], dict):
                    nombres = [c.get('nombre', '') for c in carreras]
                else:
                    nombres = carreras
                return ChatResponse(
                    recomendacion=data.get('recomendacion', ''),
                    carreras_sugeridas=nombres,
                    razonamiento=data.get('razonamiento', '')
                )
            except Exception:
                print('RESPUESTA CRUDA DE GEMINI (NO JSON):', response.text)
                return ChatResponse(
                    recomendacion=response.text,
                    carreras_sugeridas=[],
                    razonamiento=None
                )
        else:
            print('RESPUESTA CRUDA DE GEMINI (NO JSON):', response.text)
            return ChatResponse(
                recomendacion=response.text,
                carreras_sugeridas=[],
                razonamiento=None
            )

    def simular_respuesta_gemini(self, intereses: List[str], habilidades: List[str]) -> ChatResponse:
        """
        Simula la respuesta de Gemini para pruebas locales.
        Autor: Angel Hernandez
        """
        # Ejemplo de lógica simple (puedes reemplazar por llamada real a Gemini API)
        carreras = ["Ingeniería", "Psicología", "Administración"]
        razonamiento = (
            "Basado en tus intereses y habilidades, estas carreras pueden ser adecuadas. "
            "La elección se basa en la combinación de tus fortalezas y preferencias."
        )
        return ChatResponse(
            recomendacion="Te recomiendo explorar las siguientes carreras:",
            carreras_sugeridas=carreras,
            razonamiento=razonamiento
        )

