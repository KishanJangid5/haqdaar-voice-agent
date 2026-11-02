# 🏥 AarogyaSarvam (आरोग्यसर्वम)
### *Intelligent Multilingual Clinical Intake, Proactive Care & Cashless Insurance AI Agent*
**Indus Sarvam.ai Hackathon Edition**

[![Sarvam AI](https://img.shields.io/badge/Powered%20By-Sarvam%20AI-0d9488.svg)](https://sarvam.ai)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI%20%7C%20Uvicorn-009688.svg)](https://fastapi.tiangolo.com)
[![Languages](https://img.shields.io/badge/Languages-23%2B%20Indian%20Languages-teal.svg)](https://docs.sarvam.ai)

---

## 🌟 Executive Summary & Problem Statement

In India, healthcare accessibility faces three critical bottlenecks:
1. **Language & Digital Barrier**: Millions of patients struggle to navigate hospital reception desks and digital portals because their native tongue (Hindi, Marathi, Tamil, Telugu, Bengali, Gujarati, etc.) is not adequately supported.
2. **Delayed Cashless Insurance & Pre-Authorization**: The cashless pre-authorization process between hospitals and Third-Party Administrators (TPAs) / Insurance companies takes 4 to 12 hours of manual paperwork, room-rent eligibility calculations, and back-and-forth documentation queries.
3. **High Patient Readmissions & Missed Follow-ups**: After discharge, patients frequently miss medications and follow-up checkups because automated English SMS reminders are ignored or misunderstood.

**AarogyaSarvam** solves all three challenges through an autonomous, multilingual agent built on Sarvam AI's frontier models.

---

## 🚀 Key Features & Sarvam AI Model Mapping

| Capability | Sarvam AI Model / API | Real-World Impact |
|---|---|---|
| **Multilingual Voice Intake & Triage** | **Sarvam-105B Conversations** + **Saaras v4 STT** (`/speech-to-text`) | Patients can speak naturally into their browser or phone in 23+ Indian languages. The agent performs clinical triage, flags emergencies (ER/108), matches doctors, and confirms appointment slots. |
| **Authentic Voice Feedback** | **Bulbul v3 TTS** (`/text-to-speech`) | Speaks replies back in natural regional Indian accents and personas (e.g. `shubh` voice), bridging the digital literacy gap. |
| **Cashless Pre-Auth & Insurance Desk** | **Sarvam-105B Reasoning** + **Document Intelligence** | Automated IRDAI & TPA pre-authorization engine. Evaluates room-rent caps (1% rule), procedure sub-limits (e.g., Cataract, Joint Replacement), PED waiting periods, and calculates exact approved amounts vs patient liability. |
| **Proactive Care & Reminders Hub** | **Bulbul TTS** + **Sarvam Translate** (`/translate`) | Dispatches automated medication adherence voice calls and post-op rehabilitation check-ins in the patient’s preferred regional tongue. |

---

## 🛠️ Project Architecture

```
Sarvam_agent/
├── app.py                      # FastAPI Web Application & REST APIs
├── requirements.txt            # Python dependencies
├── .env                        # Secure SARVAM_API_KEY storage
├── .gitignore                  # Git privacy & environment safeguards
├── services/
│   ├── sarvam_client.py        # Centralized Sarvam SDK wrapper (Chat, STT, TTS, Translate)
│   ├── intake_agent.py         # Clinical triage & doctor appointment booking
│   ├── insurance_agent.py      # IRDAI cashless pre-auth adjudication engine
│   └── reminder_agent.py       # Proactive care outreach & voice synthesis
├── data/
│   └── mock_db.py              # In-memory hospital database (Doctors, Patients, Claims)
├── templates/
│   └── index.html              # Modern, responsive single-page dashboard
└── static/
    ├── css/custom.css          # Glassmorphic UI styling
    └── js/app.js               # Frontend controller, Web Audio recording & API integration
```

---

## ⚡ Quickstart Guide

### 1. Prerequisites
- Python 3.10+ installed
- Sarvam AI API subscription key

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Key
Ensure your `.env` contains:
```ini
SARVAM_API_KEY=your_sarvam_api_key_here
```

### 4. Run the Web Application
```bash
python app.py
```

Open your browser and navigate to:
👉 **[http://localhost:8000](http://localhost:8000)**

---

## 🎯 1-Click Interactive Test Cases

On the **Cashless Pre-Auth Desk** tab, click any of the 1-click test buttons to evaluate Sarvam AI's reasoning:
1. **Star Health - Cataract Daycare Surgery**: Checks ₹50,000 sub-limit, IOL lens sticker validation, and daycare bed charges.
2. **HDFC ERGO - Laparoscopic Cholecystectomy**: Validates private AC room rent eligibility, surgeon fees, and co-pay clauses.
3. **Ayushman Bharat PM-JAY - Angioplasty**: Validates fixed package rate (MC001B), 100% cashless treatment with zero patient copay.

On the **Proactive Care & Reminders Hub** tab:
- Click **"Listen to Native Voice Call"** on any scheduled patient card to hear high-fidelity regional audio generated on-the-fly by Sarvam AI's `Bulbul` voice engine.

