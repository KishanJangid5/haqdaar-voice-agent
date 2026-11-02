import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List
from data.mock_db import DOCTORS, APPOINTMENTS
from services.sarvam_client import sarvam_service

INTAKE_SYSTEM_PROMPT = """
You are "AarogyaSarvam", an empathetic, intelligent clinical intake and appointment triage assistant for Indus Sanjeevani Multi-Speciality Hospital in India.
Your primary objectives:
1. Welcome the patient warmly in their language or English/Hindi/Hinglish.
2. Ask about their symptoms, duration, and severity in a helpful, concise manner.
3. If they mention emergencies (e.g., crushing chest pain radiating to arm, sudden facial droop, severe unmanageable hemorrhage, breathing stoppage), immediately advise visiting the Emergency Trauma Ward (ER) or calling 108.
4. Match their condition to the most suitable medical specialty and doctor from our hospital roster:
   - Dr. Priya Sharma (Cardiology) - Chest pain, palpitations, hypertension, stent/angio review.
   - Dr. Rajesh Kulkarni (Orthopedics & Joint Replacement) - Knee pain, fracture, joint stiffness, arthritis, sports injuries.
   - Dr. Ananya Iyer (General Medicine & Diabetology) - Fever, diabetes, fatigue, cough/cold, general health checkup.
   - Dr. Suresh Mehta (Neurology) - Migraine, nerve pain, seizures, tremors, dizziness.
   - Dr. Kavita Nair (Pediatrics) - Infant/child care, pediatric fever, vaccinations.
   - Dr. Sneha Patel (Obstetrics & Gynecology) - Pre-natal, PCOS, menstrual irregularities, women's health.
5. Guide them smoothly to choose a date and slot for consultation.
6. Keep answers concise, culturally aware for India, and medical-friendly.
"""

class IntakeAgent:
    def process_chat(self, conversation_history: List[Dict[str, str]], user_message: str) -> Dict[str, Any]:
        """
        Processes patient chat using Sarvam-105B Conversations.
        """
        messages = [{"role": "system", "content": INTAKE_SYSTEM_PROMPT}]
        for msg in conversation_history:
            messages.append({"role": msg.get("role", "user"), "content": msg.get("content", "")})
        messages.append({"role": "user", "content": user_message})

        reply = sarvam_service.chat_complete(messages=messages, temperature=0.3)
        return {
            "reply": reply,
            "doctors": DOCTORS
        }

    def book_appointment(self, details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Books and saves an appointment into the hospital database.
        """
        apt_id = f"APT-{uuid.uuid4().hex[:6].upper()}"
        
        doctor = next((d for d in DOCTORS if d["id"] == details.get("doctor_id")), None)
        doc_name = doctor["name"] if doctor else details.get("doctor_name", "General Duty Medical Officer")
        doc_spec = doctor["specialty"] if doctor else details.get("specialty", "General Medicine")
        doc_fee = doctor["fee"] if doctor else 700

        appointment = {
            "id": apt_id,
            "patient_name": details.get("patient_name", "Anonymous Patient"),
            "phone": details.get("phone", "+91 98000 00000"),
            "age": details.get("age", 35),
            "gender": details.get("gender", "Other"),
            "doctor_id": details.get("doctor_id", "DOC-103"),
            "doctor_name": doc_name,
            "specialty": doc_spec,
            "fee": doc_fee,
            "date": details.get("date", (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")),
            "time": details.get("time", "10:00 AM"),
            "symptoms": details.get("symptoms", "General Consultation"),
            "language_preference": details.get("language_preference", "hi-IN"),
            "status": "Confirmed",
            "booking_mode": details.get("booking_mode", "Sarvam AI Voice Assistant"),
            "created_at": datetime.now().isoformat()
        }

        # Add to in-memory database
        APPOINTMENTS.insert(0, appointment)

        # Generate a personalized confirmation text for the patient
        conf_text = (
            f"आपकी अपॉइंटमेंट डॉ. {doc_name} ({doc_spec}) के साथ "
            f"दिनांक {appointment['date']} को {appointment['time']} बजे सफलतापूर्वक बुक हो गई है। "
            f"अपॉइंटमेंट आईडी: {apt_id}। कृपया 15 मिनट पूर्व अस्पताल पहुंचें।"
        )

        return {
            "success": True,
            "appointment": appointment,
            "confirmation_message": conf_text
        }

    def get_appointments(self) -> List[Dict[str, Any]]:
        return APPOINTMENTS

    def get_doctors(self) -> List[Dict[str, Any]]:
        return DOCTORS

intake_agent = IntakeAgent()

