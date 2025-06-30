# Backend - Orientador Universitario

## Descripción
Chatbot orientador universitario que recomienda carreras a estudiantes basado en sus intereses y habilidades. Implementado en FastAPI, orientado a objetos y preparado para integrarse con un frontend en React.

## Instalación

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecuta el servidor:
   ```bash
   uvicorn main:app --reload
   ```

## Endpoints

- `POST /chat`  
  **Body:**
  ```json
  {
    "intereses": ["matemáticas", "tecnología"],
    "habilidades": ["análisis", "resolución de problemas"]
  }
  ```
  **Respuesta:**
  ```json
  {
    "recomendacion": "Te recomiendo explorar las siguientes carreras:",
    "carreras_sugeridas": ["Ingeniería", "Psicología", "Administración"],
    "razonamiento": "Basado en tus intereses y habilidades..."
  }
  ```

- `GET /history`  
  Devuelve el historial de conversaciones.

- `POST /reset`  
  Limpia el historial de conversación.

## Autor
Angel Hernandez 