import os
import logging
import time
from dotenv import load_dotenv
import groq
from fastapi import HTTPException

# កំណត់រចនាសម្ព័ន្ធការបង្ហាញ Log នៅលើ Console/Render
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# ទាញយក Environment Variables (សម្រាប់ Local ប្រើ .env, សម្រាប់ Render វានឹងទាញយកដោយស្វ័យប្រវត្តិ)
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("រកមិនឃើញ GROQ_API_KEY ទេ។ សូមប្រាកដថាអ្នកបានបញ្ចូលវានៅក្នុង .env ឬ Render Environment Variables។")

# ចាប់ផ្តើមតភ្ជាប់ទៅកាន់ប្រព័ន្ធ Groq
client = groq.Groq(api_key=api_key)

def transcribir_audio_groq(file_path):
    """មុខងារស្នូលសម្រាប់បញ្ជូនឯកសារទៅកាន់ Groq Whisper API ដោយបង្ខំឱ្យបំប្លែងជាភាសាខ្មែរ។"""
    logging.info(f"🎤 [{file_path}] កំពុងចាប់ផ្តើមបំប្លែងសំឡេងទៅជាអត្ថបទ...")
    start_time = time.time()
    
    try:
        with open(file_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-large-v3", # ម៉ូដែល AI ជំនាន់ចុងក្រោយ
                response_format="json",
                language="km",            # 💡 បង្ខំយកភាសាខ្មែរ (Khmer)
                temperature=0.0,          # កំណត់ 0.0 ដើម្បីកុំឱ្យ AI ទាយពាក្យផ្តេសផ្តាស់ (ភាពត្រឹមត្រូវខ្ពស់)
                
                # 💡 Prompt សំខាន់ខ្លាំង៖ ការពារបញ្ហា Hallucination ពេលថត Live ស្ងាត់ ឬពេល Upload ចំតន្ត្រី
                prompt="នេះគឺជាសំឡេងនិយាយភាសាខ្មែរត្រឹមត្រូវច្បាស់លាស់។ សូមកុំសរសេរពាក្យរញ៉េរញ៉ៃ បើគ្មានសំឡេងនិយាយទេសូមកុំសរសេរអ្វីទាំងអស់។"
            )

        elapsed_time = round(time.time() - start_time, 2)
        logging.info(f"✅ [{file_path}] បំប្លែងបានជោគជ័យ ចំណាយពេល {elapsed_time} វិនាទី។")
        
        return response.text
    
    except Exception as e:
        logging.error(f"❌ មានកំហុសពីប្រព័ន្ធ Groq API: {e}")
        raise HTTPException(status_code=500, detail=f"បញ្ហា Groq API: {str(e)}")

def procesar_archivo_audio(file_path):
    """
    មុខងារត្រួតពិនិត្យឯកសារមុននឹងបញ្ជូនទៅ AI។ 
    (យើងលុបចោលការប្រើប្រាស់បណ្ណាល័យ 'wave' ចាស់ដើម្បីឱ្យវាគាំទ្រ MP3 និងគ្រប់ប្រភេទឯកសារ)
    """
    try:
        # ដោយសារ Groq គាំទ្រឯកសាររហូតដល់ទំហំ 25MB ស្រាប់ និង Frontend ជាអ្នកកាត់ Chunk ឱ្យហើយពេល Live
        # យើងអាចបោះឯកសារទៅឱ្យ AI ដំណើរការដោយផ្ទាល់បានតែម្តង (លឿន និងមានសុវត្ថិភាព)
        return transcribir_audio_groq(file_path)
    
    except Exception as e:
        logging.error(f"❌ មានកំហុសនៅពេលដំណើរការឯកសារ: {e}")
        raise HTTPException(status_code=500, detail=f"កំហុសក្នុងការកែច្នៃឯកសារ: {str(e)}")
