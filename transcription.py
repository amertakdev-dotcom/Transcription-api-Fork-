import os
import logging
import time
from dotenv import load_dotenv
import groq
from fastapi import HTTPException

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Cargar variables de entorno
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("API_KEY no encontrada en el entorno. Verifica tu archivo .env.")

# Inicializar cliente Groq
client = groq.Groq(api_key=api_key)

def transcribir_audio_groq(file_path):
    """Transcribe un archivo de audio usando la API de Groq Whisper forcing Khmer."""
    logging.info(f"🎤 [{file_path}] Iniciando transcripción en tiempo real...")
    start_time = time.time()
    
    try:
        with open(file_path, "rb") as audio_file:
            # បង្ខំយកភាសាខ្មែរ "km" និងបន្ថែម Prompt ការពារ AI បង្កើតអក្សររញ៉េរញ៉ៃពេលសំឡេងខ្សោយ ឬស្ងាត់
            response = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-large-v3",
                response_format="json",
                language="km", 
                temperature=0.0,
                prompt="នេះគឺជាសំឡេងនិយាយភាសាខ្មែរត្រឹមត្រូវច្បាស់លាស់។ សូមកុំបង្កើតពាក្យរញ៉េរញ៉ៃ បើគ្មានសំឡេងនិយាយច្បាស់ទេសូមកុំសរសេរអ្វីទាំងអស់។"
            )

        elapsed_time = round(time.time() - start_time, 2)
        logging.info(f"✅ [{file_path}] Completado en {elapsed_time} segundos.")
        return response.text
    except Exception as e:
        logging.error(f"❌ Error en Groq API: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def procesar_archivo_audio(file_path):
    """Procesa directamente el archivo de audio (Optimizado para Live Chunks y Archivos)"""
    try:
        return transcribir_audio_groq(file_path)
    except Exception as e:
        logging.error(f"❌ Error al procesar: {e}")
        raise HTTPException(status_code=500, detail=str(e))
