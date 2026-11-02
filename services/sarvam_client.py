import os
import io
import base64
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

# Ensure environment is loaded before importing SarvamAI
load_dotenv()

from sarvamai import SarvamAI

class SarvamService:
    def __init__(self):
        api_key = os.getenv("SARVAM_API_KEY")
        if not api_key:
            raise ValueError("SARVAM_API_KEY environment variable is missing in .env")
        self.client = SarvamAI(api_subscription_key=api_key)

    def chat_complete(
        self,
        messages: List[Dict[str, str]],
        model: str = "sarvam-105b-conversations",
        temperature: float = 0.4,
        max_tokens: int = 1000
    ) -> str:
        """
        Sends conversation messages to Sarvam-105b-conversations LLM.
        """
        try:
            response = self.client.chat.completions(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error communicating with Sarvam Chat API: {str(e)}"

    def text_to_speech(
        self,
        text: str,
        language_code: str = "hi-IN",
        speaker: str = "shubh",
        model: str = "bulbul:v3",
        pace: float = 1.0
    ) -> Dict[str, Any]:
        """
        Converts text to spoken Indian audio using Sarvam Bulbul model.
        Returns dictionary containing base64 audio and metadata.
        """
        try:
            valid_langs = {
                "hi": "hi-IN", "en": "en-IN", "mr": "mr-IN", "ta": "ta-IN",
                "te": "te-IN", "bn": "bn-IN", "gu": "gu-IN", "kn": "kn-IN",
                "ml": "ml-IN", "pa": "pa-IN", "od": "od-IN"
            }
            clean_lang = valid_langs.get(language_code.lower(), language_code)
            safe_text = text[:1200] if len(text) > 1200 else text

            response = self.client.text_to_speech.convert(
                text=safe_text,
                language_code=clean_lang,
                speaker=speaker,
                model=model,
                pace=pace
            )

            if response and response.audios and len(response.audios) > 0:
                return {
                    "success": True,
                    "audio_base64": response.audios[0],
                    "mime_type": "audio/wav",
                    "language_code": clean_lang,
                    "speaker": speaker
                }
            return {"success": False, "error": "No audio returned from Sarvam Bulbul API"}
        except Exception as e:
            return {"success": False, "error": f"TTS conversion failed: {str(e)}"}

    def speech_to_text(
        self,
        audio_bytes: bytes,
        filename: str = "recording.wav",
        language_code: str = "unknown",
        content_type: str = "audio/wav"
    ) -> Dict[str, Any]:
        """
        Transcribes speech audio using Sarvam Saaras v4 STT model.
        Supports 23 Indian languages with auto language detection.
        Handles WebM, WAV, OGG formats automatically.
        """
        try:
            # Determine appropriate mime type and extension
            fn_lower = filename.lower()
            ct_lower = content_type.lower()
            
            if "webm" in fn_lower or "webm" in ct_lower:
                mime = "audio/webm"
                fn = "audio.webm"
            elif "ogg" in fn_lower or "ogg" in ct_lower:
                mime = "audio/ogg"
                fn = "audio.ogg"
            elif "mp3" in fn_lower or "mp3" in ct_lower:
                mime = "audio/mp3"
                fn = "audio.mp3"
            else:
                mime = "audio/wav"
                fn = "audio.wav"

            file_tuple = (fn, audio_bytes, mime)
            
            # Map auto or empty language to unknown
            req_lang = language_code if language_code not in ("auto", "unknown", "", None) else "unknown"

            response = self.client.speech_to_text.transcribe(
                file=file_tuple,
                model="saaras:v4",
                language_code=req_lang
            )
            return {
                "success": True,
                "transcript": response.transcript,
                "language_code": getattr(response, "language_code", language_code),
                "confidence": getattr(response, "language_probability", 1.0)
            }
        except Exception as e:
            return {"success": False, "error": f"STT transcription failed: {str(e)}"}

    def translate(
        self,
        text: str,
        target_language_code: str = "hi-IN",
        source_language_code: str = "auto"
    ) -> Dict[str, Any]:
        """
        Translates text between Indian languages and English using Sarvam Translate.
        """
        try:
            response = self.client.text.translate(
                input=text,
                source_language_code=source_language_code,
                target_language_code=target_language_code
            )
            return {
                "success": True,
                "translated_text": response.translated_text,
                "source_language_code": response.source_language_code,
                "target_language_code": target_language_code
            }
        except Exception as e:
            return {"success": False, "error": f"Translation failed: {str(e)}"}

sarvam_service = SarvamService()
