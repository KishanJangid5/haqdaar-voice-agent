import os
import io
import sys
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

# Reconfigure terminal encoding for Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure .env is loaded
load_dotenv()

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.sarvam_client import sarvam_service
from services.intake_agent import intake_agent
from services.insurance_agent import insurance_agent
from services.reminder_agent import reminder_agent
from data.mock_db import SAMPLE_POLICIES

app = FastAPI(
    title="AarogyaSarvam - Multilingual Healthcare & Cashless Insurance AI Agent",
    description="Indus Sarvam.ai Hackathon Winning Healthcare Agent powered by Sarvam AI Models",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files & Templates directory
os.makedirs("static/css", exist_ok=True)
os.makedirs("static/js", exist_ok=True)
os.makedirs("templates", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Request Models
class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = []

class AppointmentRequest(BaseModel):
    patient_name: str
    phone: str
    age: int
    gender: str
    doctor_id: str
    date: str
    time: str
    symptoms: str
    language_preference: Optional[str] = "hi-IN"
    booking_mode: Optional[str] = "Sarvam AI Voice Assistant"

class PreAuthRequest(BaseModel):
    patient_name: str
    policy_number: str
    insurer: str
    tpa: Optional[str] = "In-House Hospital TPA Desk"
    sum_insured: float
    treatment_name: str
    estimated_cost: float
    room_category: str
    policy_age_years: Optional[int] = 3
    pre_existing_status: Optional[str] = "None"
    document_text: Optional[str] = ""

class DispatchReminderRequest(BaseModel):
    patient_name: str
    phone: str
    campaign_type: str
    language_code: str
    custom_message: Optional[str] = ""
    generate_voice: Optional[bool] = True

class TTSRequest(BaseModel):
    text: str
    language_code: Optional[str] = "hi-IN"
    speaker: Optional[str] = "shubh"

class TranslateRequest(BaseModel):
    text: str
    target_language_code: str
    source_language_code: Optional[str] = "auto"


# Routes
@app.get("/", response_class=HTMLResponse)
async def serve_home():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

# Doctor & Intake Endpoints
@app.get("/api/doctors")
async def get_doctors():
    return {"doctors": intake_agent.get_doctors()}

@app.get("/api/appointments")
async def get_appointments():
    return {"appointments": intake_agent.get_appointments()}

@app.post("/api/appointments/book")
async def book_appointment(req: AppointmentRequest):
    result = intake_agent.book_appointment(req.model_dump())
    return result

@app.post("/api/chat/intake")
async def chat_intake(req: ChatRequest):
    response = intake_agent.process_chat(req.history, req.message)
    return response

# Speech & Voice Endpoints (Sarvam Saaras STT & Bulbul TTS)
@app.post("/api/voice/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    language_code: str = Form("unknown")
):
    audio_bytes = await file.read()
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="Empty audio file provided")
    
    result = sarvam_service.speech_to_text(
        audio_bytes=audio_bytes,
        filename=file.filename or "recording.webm",
        language_code=language_code,
        content_type=file.content_type or "audio/webm"
    )
    return result

@app.post("/api/voice/speak")
async def generate_speech(req: TTSRequest):
    result = sarvam_service.text_to_speech(
        text=req.text,
        language_code=req.language_code or "hi-IN",
        speaker=req.speaker or "shubh"
    )
    return result

@app.post("/api/translate")
async def translate_text(req: TranslateRequest):
    result = sarvam_service.translate(
        text=req.text,
        target_language_code=req.target_language_code,
        source_language_code=req.source_language_code or "auto"
    )
    return result

# Cashless Insurance Pre-Auth Endpoints
@app.get("/api/insurance/claims")
async def get_claims():
    return {"claims": insurance_agent.get_claims()}

@app.get("/api/insurance/sample/{sample_key}")
async def get_sample_policy(sample_key: str):
    sample = insurance_agent.get_sample_policy(sample_key)
    if not sample:
        raise HTTPException(status_code=404, detail="Sample policy not found")
    return sample

@app.post("/api/insurance/verify")
async def verify_cashless(req: PreAuthRequest):
    result = insurance_agent.verify_preauth(req.model_dump())
    return result

# Proactive Care Reminders & Campaigns Endpoints
@app.get("/api/reminders")
async def get_reminders():
    return {
        "reminders": reminder_agent.get_campaigns(),
        "templates": reminder_agent.get_templates()
    }

@app.post("/api/reminders/dispatch")
async def dispatch_reminder(req: DispatchReminderRequest):
    result = reminder_agent.create_and_dispatch_reminder(
        patient_name=req.patient_name,
        phone=req.phone,
        campaign_type=req.campaign_type,
        language_code=req.language_code,
        custom_message=req.custom_message or "",
        generate_voice=req.generate_voice if req.generate_voice is not None else True
    )
    return result

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🚀 AarogyaSarvam Healthcare AI Agent Web Platform is RUNNING!")
    print("👉 Open in your browser: http://127.0.0.1:8000 or http://localhost:8000")
    print("="*60 + "\n", flush=True)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

