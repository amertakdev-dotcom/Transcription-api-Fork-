from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from transcription import procesar_archivo_audio
import shutil
import os

app = FastAPI()

# អនុញ្ញាតឱ្យ Frontend ហៅទៅកាន់ API បាន (Fix CORS Error)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # អាចប្តូរទៅជា URL របស់ Frontend របស់អ្នកនៅក្នុង Production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/transcribe/")
async def transcribe(file: UploadFile = File(...)):
    """
    API endpoint para transcribir un archivo de audio.
    """
    try:
        file_path = f"audio/temp_{file.filename}"
        os.makedirs("audio", exist_ok=True)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        transcription = procesar_archivo_audio(file_path)
        os.remove(file_path)  # លុបឯកសារបណ្តោះអាសន្នក្រោយបំប្លែងរួច

        return {"transcription": transcription}
    except Exception as e:
        return {"error": str(e)}
