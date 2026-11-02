import uuid
from datetime import datetime
from typing import Dict, Any, List
from data.mock_db import REMINDERS
from services.sarvam_client import sarvam_service

CAMPAIGN_TEMPLATES = {
    "medication_adherence": {
        "title": "Medication & Dosage Adherence",
        "default_text": "नमस्ते {name} जी, यह इंडस संजीवनी अस्पताल से आपकी दवा की याद दिलाने के लिए है। कृपया अपनी निर्धारित दवाएं समय पर लें और खूब पानी पिएं।",
        "suggested_lang": "hi-IN",
        "speaker": "shubh"
    },
    "post_op_care": {
        "title": "Post-Operative Wound & Rehab Check-in",
        "default_text": "नमस्कार {name} जी, तुमच्या शस्त्रक्रियेनंतरच्या रिकव्हरीबद्दल आम्ही विचारपूस करत आहोत. डॉक्टरांनी सांगितल्याप्रमाणे व्यायाम करा आणि वेदना वाढल्यास त्वरित संपर्क साधा.",
        "suggested_lang": "mr-IN",
        "speaker": "shubh"
    },
    "diabetic_reengagement": {
        "title": "Quarterly Diabetes HbA1c & Fasting Outreach",
        "default_text": "வணக்கம் {name} அவர்களே, உங்கள் அடுத்த சர்க்கரை பரிசோதனைக்கான நேரம் வந்துவிட்டது. இந்த வாரம் ரத்த பரிசோதனை செய்து கொள்ளவும்.",
        "suggested_lang": "ta-IN",
        "speaker": "shubh"
    },
    "annual_cardiac_checkup": {
        "title": "Annual Cardiac & Executive Screening",
        "default_text": "Hello {name}, your annual cardiac checkup and 2D Echo review is due next week at Indus Sanjeevani Hospital. Prioritize your heart health and book your slot today.",
        "suggested_lang": "en-IN",
        "speaker": "shubh"
    }
}

class ReminderAgent:
    def get_campaigns(self) -> List[Dict[str, Any]]:
        return REMINDERS

    def get_templates(self) -> Dict[str, Any]:
        return CAMPAIGN_TEMPLATES

    def create_and_dispatch_reminder(
        self,
        patient_name: str,
        phone: str,
        campaign_type: str,
        language_code: str,
        custom_message: str = "",
        generate_voice: bool = True
    ) -> Dict[str, Any]:
        """
        Creates a patient care reminder and synthesizes regional voice using Sarvam Bulbul.
        """
        # Select or interpolate text
        if custom_message.strip():
            msg_text = custom_message
        else:
            tpl = CAMPAIGN_TEMPLATES.get(campaign_type, CAMPAIGN_TEMPLATES["medication_adherence"])
            msg_text = tpl["default_text"].format(name=patient_name)

        audio_data = None
        if generate_voice:
            tts_res = sarvam_service.text_to_speech(
                text=msg_text,
                language_code=language_code,
                speaker="shubh"
            )
            if tts_res.get("success"):
                audio_data = tts_res.get("audio_base64")

        rem_id = f"REM-{uuid.uuid4().hex[:5].upper()}"
        reminder_record = {
            "id": rem_id,
            "patient_name": patient_name,
            "phone": phone,
            "campaign_type": campaign_type,
            "language_code": language_code,
            "message": msg_text,
            "scheduled_time": "Immediate / Triggered Now",
            "status": "Dispatched via Sarvam Bulbul Voice Call",
            "voice_generated": bool(audio_data),
            "audio_base64": audio_data,
            "channel": f"Sarvam AI Bulbul Voice ({language_code}) + SMS/WhatsApp",
            "dispatched_at": datetime.now().isoformat()
        }

        REMINDERS.insert(0, reminder_record)

        return {
            "success": True,
            "reminder": reminder_record,
            "has_audio": bool(audio_data)
        }

    def generate_voice_for_text(self, text: str, language_code: str = "hi-IN", speaker: str = "shubh") -> Dict[str, Any]:
        """
        Generates on-demand voice audio using Sarvam Bulbul.
        """
        return sarvam_service.text_to_speech(text=text, language_code=language_code, speaker=speaker)

    def translate_message(self, text: str, target_language: str) -> Dict[str, Any]:
        """
        Translates a message to any target Indian language using Sarvam Translate.
        """
        return sarvam_service.translate(text=text, target_language_code=target_language)

reminder_agent = ReminderAgent()

