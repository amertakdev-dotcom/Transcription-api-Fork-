from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from transcription import procesar_archivo_audio
import shutil
import os

app = FastAPI()

# បន្ថែម CORS Middleware ដើម្បីអនុញ្ញាតឱ្យ Frontend អាចទាក់ទងមកកាន់ Server បានទោះបីជាផ្ទុកនៅលើ Host ផ្សេងគ្នាក៏ដោយ
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/transcribe/")
async def transcribe(file: UploadFile = File(...)):
    try:
        file_path = f"audio/temp_{file.filename}"
        os.makedirs("audio", exist_ok=True)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        transcription = procesar_archivo_audio(file_path)
        
        # លុបឯកសារបណ្តោះអាសន្នចេញក្រោយពេលបំប្លែងរួច ដើម្បីកុំឱ្យពេញទំហំផ្ទុកលើ Server
        if os.path.exists(file_path):
            os.remove(file_path)

        return {"transcription": transcription}
    except Exception as e:
        return {"error": str(e)}
