from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from transcription import procesar_archivo_audio
import shutil
import os

app = FastAPI()

# បើកដំណើរការ CORS ដើម្បីអនុញ្ញាតឱ្យ Frontend (Web UI) អាចផ្ញើទិន្នន័យមកកាន់ Backend នេះបានទោះនៅ Host ខុសគ្នាក៏ដោយ
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # អនុញ្ញាតគ្រប់ប្រភព (Origins) ទាំងអស់
    allow_credentials=True,
    allow_methods=["*"],  # អនុញ្ញាតរាល់ Methods ដូចជា POST, GET, OPTIONS...
    allow_headers=["*"],
)

@app.post("/transcribe/")
async def transcribe(file: UploadFile = File(...)):
    """
    API Endpoint ទទួលឯកសារសំឡេងពីអ្នកប្រើប្រាស់ និងបញ្ជូនទៅកាន់ Groq Whisper។
    """
    try:
        # បង្កើតឈ្មោះឯកសារបណ្តោះអាសន្ន ដើម្បីការពារការជាន់គ្នាពេលមានអ្នក Request ច្រើន
        file_path = f"audio/temp_{file.filename}"
        
        # បង្កើត Folder 'audio' ប្រសិនបើវាមិនទាន់មាន
        os.makedirs("audio", exist_ok=True)

        # រក្សាទុកឯកសារដែលបាន Upload ចូលទៅក្នុង Server ជាបណ្តោះអាសន្ន
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # ហៅមុខងារបំប្លែងសំឡេងពីឯកសារ transcription.py
        transcription = procesar_archivo_audio(file_path)
        
        # សម្អាតទំហំផ្ទុក៖ លុបឯកសារចោលវិញភ្លាមៗបន្ទាប់ពីបំប្លែងបានជោគជ័យ
        if os.path.exists(file_path):
            os.remove(file_path)

        # បញ្ជូនលទ្ធផលអត្ថបទត្រឡប់ទៅឱ្យ Frontend វិញ
        return {"transcription": transcription}
    
    except Exception as e:
        # ប្រសិនបើមានកំហុស វានឹងលោត Error Message ប្រាប់
        return {"error": str(e)}
