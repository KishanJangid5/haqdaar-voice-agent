"""
Mock Database for Indus Sanjeevani Multi-Speciality Hospital.
Persists records in-memory during server runtime with realistic clinical and insurance data.
"""

from datetime import datetime, timedelta
import uuid

DOCTORS = [
    {
        "id": "DOC-101",
        "name": "Dr. Priya Sharma",
        "specialty": "Cardiology",
        "qualification": "MD, DM (Cardiology) - AIIMS",
        "experience": "14 years",
        "languages": ["English", "Hindi", "Punjabi"],
        "fee": 1200,
        "available_days": ["Mon", "Wed", "Fri", "Sat"],
        "slots": ["10:00 AM", "11:30 AM", "02:00 PM", "04:30 PM", "06:00 PM"]
    },
    {
        "id": "DOC-102",
        "name": "Dr. Rajesh Kulkarni",
        "specialty": "Orthopedics & Joint Replacement",
        "qualification": "MS (Ortho), Fellowship in Arthroplasty (UK)",
        "experience": "18 years",
        "languages": ["English", "Marathi", "Hindi"],
        "fee": 1000,
        "available_days": ["Tue", "Thu", "Sat"],
        "slots": ["09:30 AM", "11:00 AM", "03:00 PM", "05:00 PM"]
    },
    {
        "id": "DOC-103",
        "name": "Dr. Ananya Iyer",
        "specialty": "General Medicine & Diabetology",
        "qualification": "MD (Internal Medicine)",
        "experience": "11 years",
        "languages": ["English", "Tamil", "Hindi"],
        "fee": 700,
        "available_days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
        "slots": ["09:00 AM", "10:30 AM", "12:00 PM", "03:30 PM", "05:30 PM"]
    },
    {
        "id": "DOC-104",
        "name": "Dr. Suresh Mehta",
        "specialty": "Neurology",
        "qualification": "DM (Neurology) - NIMHANS",
        "experience": "16 years",
        "languages": ["English", "Gujarati", "Hindi"],
        "fee": 1500,
        "available_days": ["Mon", "Wed", "Fri"],
        "slots": ["11:00 AM", "02:30 PM", "04:00 PM"]
    },
    {
        "id": "DOC-105",
        "name": "Dr. Kavita Nair",
        "specialty": "Pediatrics & Child Care",
        "qualification": "MD (Pediatrics), DNB",
        "experience": "9 years",
        "languages": ["English", "Malayalam", "Hindi"],
        "fee": 800,
        "available_days": ["Mon", "Tue", "Thu", "Fri", "Sat"],
        "slots": ["10:00 AM", "11:30 AM", "04:00 PM", "05:30 PM"]
    },
    {
        "id": "DOC-106",
        "name": "Dr. Sneha Patel",
        "specialty": "Obstetrics & Gynecology",
        "qualification": "MS (OBG), Fellowship in Laparoscopy",
        "experience": "13 years",
        "languages": ["English", "Gujarati", "Hindi"],
        "fee": 1100,
        "available_days": ["Mon", "Tue", "Wed", "Thu", "Fri"],
        "slots": ["10:00 AM", "12:00 PM", "03:00 PM", "05:00 PM"]
    }
]

# Initial Appointments
APPOINTMENTS = [
    {
        "id": "APT-7801",
        "patient_name": "Ramesh Gupta",
        "phone": "+91 98201 45872",
        "age": 58,
        "gender": "Male",
        "doctor_id": "DOC-103",
        "doctor_name": "Dr. Ananya Iyer",
        "specialty": "General Medicine & Diabetology",
        "date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "time": "10:30 AM",
        "symptoms": "High blood sugar readings, intermittent dizziness, fatigue",
        "language_preference": "hi-IN",
        "status": "Confirmed",
        "booking_mode": "Sarvam AI Voice Assistant",
        "created_at": datetime.now().isoformat()
    },
    {
        "id": "APT-7802",
        "patient_name": "Sunita Verma",
        "phone": "+91 97112 33451",
        "age": 63,
        "gender": "Female",
        "doctor_id": "DOC-102",
        "doctor_name": "Dr. Rajesh Kulkarni",
        "specialty": "Orthopedics & Joint Replacement",
        "date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
        "time": "11:00 AM",
        "symptoms": "Post-knee surgery pain and stiffness during morning walk",
        "language_preference": "mr-IN",
        "status": "Confirmed",
        "booking_mode": "Web Portal",
        "created_at": (datetime.now() - timedelta(hours=3)).isoformat()
    },
    {
        "id": "APT-7803",
        "patient_name": "Mohammed Faizan",
        "phone": "+91 98450 19823",
        "age": 47,
        "gender": "Male",
        "doctor_id": "DOC-101",
        "doctor_name": "Dr. Priya Sharma",
        "specialty": "Cardiology",
        "date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
        "time": "02:00 PM",
        "symptoms": "Palpitations after stairs climbing, routine 6-month stent review",
        "language_preference": "hi-IN",
        "status": "Confirmed",
        "booking_mode": "Sarvam AI Multilingual Intake",
        "created_at": (datetime.now() - timedelta(hours=6)).isoformat()
    }
]

# Cashless Insurance Pre-Auth Database
INSURANCE_CLAIMS = [
    {
        "id": "CLM-4091",
        "patient_name": "Ramesh Gupta",
        "policy_number": "STAR-IND-2024-88491",
        "insurer": "Star Health & Allied Insurance",
        "tpa": "Direct In-House TPA",
        "sum_insured": 750000,
        "available_balance": 620000,
        "treatment_name": "Unilateral Cataract Phacoemulsification with Foldable IOL",
        "estimated_cost": 48000,
        "room_category": "Twin Sharing",
        "room_rent_capping": "1% of Sum Insured (₹7,500/day)",
        "copay_clause": "0% (No copay)",
        "pre_existing_status": "Hypertension (declared, 3+ yrs policy tenure)",
        "approval_status": "Approved",
        "approved_amount": 45000,
        "patient_liability": 3000,
        "pre_auth_code": "STAR/PRE/MUM/2026/8912",
        "remarks": "Cataract sub-limit cap applies: ₹45,000 maximum per eye. Non-medical consumable deductions: ₹3,000.",
        "updated_at": datetime.now().isoformat()
    },
    {
        "id": "CLM-4092",
        "patient_name": "Amitav Roy",
        "policy_number": "HDFC-ERGO-MED-99321",
        "insurer": "HDFC ERGO General Insurance",
        "tpa": "Medi Assist TPA",
        "sum_insured": 1000000,
        "available_balance": 950000,
        "treatment_name": "Laparoscopic Cholecystectomy (Gallbladder Stone)",
        "estimated_cost": 135000,
        "room_category": "Single Private AC",
        "room_rent_capping": "No Cap (Up to Sum Insured)",
        "copay_clause": "10% Copay on Senior Citizen Dependent",
        "pre_existing_status": "None",
        "approval_status": "Approved",
        "approved_amount": 121500,
        "patient_liability": 13500,
        "pre_auth_code": "HDFC/MA/BLR/2026/5129",
        "remarks": "Cashless approved with 10% co-pay deduction. Admission scheduled for tomorrow 8:00 AM.",
        "updated_at": (datetime.now() - timedelta(hours=2)).isoformat()
    },
    {
        "id": "CLM-4093",
        "patient_name": "Sunita Verma",
        "policy_number": "NIVA-BUPA-REASSURE-1184",
        "insurer": "Niva Bupa Health Insurance",
        "tpa": "Paramount Health Care TPA",
        "sum_insured": 500000,
        "available_balance": 480000,
        "treatment_name": "Total Knee Replacement (Right Joint)",
        "estimated_cost": 260000,
        "room_category": "Single Private Room",
        "room_rent_capping": "Single Private AC eligible",
        "copay_clause": "0%",
        "pre_existing_status": "Osteoarthritis declared",
        "approval_status": "Initial Authorization Issued",
        "approved_amount": 220000,
        "patient_liability": 40000,
        "pre_auth_code": "NIVA/PRM/PUN/2026/3041",
        "remarks": "Initial pre-auth issued for ₹2,20,000. Final bill adjustment during discharge.",
        "updated_at": (datetime.now() - timedelta(hours=5)).isoformat()
    }
]

# Proactive Patient Reminders & Campaigns
REMINDERS = [
    {
        "id": "REM-101",
        "patient_name": "Ramesh Gupta",
        "phone": "+91 98201 45872",
        "campaign_type": "Medication & Fasting Blood Sugar Reminder",
        "language_code": "hi-IN",
        "message": "नमस्ते रमेश जी, कल सुबह डॉ. अनन्या अय्यर के साथ आपकी अपॉइंटमेंट से पहले 10 घंटे का उपवास (फास्टिंग) रखें और अपनी सुबह की दवा पानी के साथ समय पर लें।",
        "scheduled_time": "Tomorrow at 07:00 AM",
        "status": "Scheduled",
        "voice_generated": True,
        "channel": "Sarvam Bulbul Voice Call + WhatsApp"
    },
    {
        "id": "REM-102",
        "patient_name": "Sunita Verma",
        "phone": "+91 97112 33451",
        "campaign_type": "Post-Op Knee Physiotherapy & Care Reminder",
        "language_code": "mr-IN",
        "message": "नमस्कार सुनिता ताई, आज दुपारच्या फिजिओथेरपी सेशनची आठवण करून देत आहोत. गुडघ्याला सूज जाणवल्यास 15 मिनिटे बर्फाचा शेक घ्या.",
        "scheduled_time": "Today at 02:00 PM",
        "status": "Delivered",
        "voice_generated": True,
        "channel": "Sarvam Bulbul Voice Call"
    },
    {
        "id": "REM-103",
        "patient_name": "Mohammed Faizan",
        "phone": "+91 98450 19823",
        "campaign_type": "Cardiology Stent & BP Adherence Check",
        "language_code": "hi-IN",
        "message": "मोहम्मद फैज़ान जी, कृपया अपनी खून पतला करने वाली दवा और ईकोस्प्रिन को नाश्ते के बाद नियमित रूप से लें और दैनिक बीपी लॉग नोट करें।",
        "scheduled_time": "Daily at 08:30 AM",
        "status": "Active Daily",
        "voice_generated": True,
        "channel": "Automated IVR Voice Bot"
    },
    {
        "id": "REM-104",
        "patient_name": "Meenakshi Sundaram",
        "phone": "+91 99401 22987",
        "campaign_type": "Maternal 3rd Trimester Ultrasound & Tetanus Booster",
        "language_code": "ta-IN",
        "message": "வணக்கம் மீனாட்சி அவர்களே, அடுத்த வாரம் உங்கள் வளர்ச்சி ஸ்கேன் மற்றும் ரத்த பரிசோதனைக்கான தேதி நெருங்குகிறது. தயவுசெய்து உங்கள் வருகையை உறுதிப்படுத்தவும்.",
        "scheduled_time": "Saturday at 10:00 AM",
        "status": "Scheduled",
        "voice_generated": True,
        "channel": "Sarvam Bulbul Voice Call + SMS"
    }
]

# Sample Insurance Documents for 1-Click Interactive Test in UI
SAMPLE_POLICIES = {
    "star_cataract": {
        "title": "Star Health - Cataract Daycare Surgery",
        "insurer": "Star Health & Allied Insurance",
        "policy_number": "STAR-COMP-IND-920144",
        "insured_name": "Ramesh Gupta",
        "sum_insured": 750000,
        "proposed_treatment": "Cataract Phacoemulsification with Foldable Monofocal IOL",
        "estimated_hospital_bill": 48000,
        "hospital_room": "Twin Sharing Daycare Bed",
        "policy_age_years": 4,
        "document_text": """
STAR HEALTH AND ALLIED INSURANCE COMPANY LIMITED
CASHLESS PRE-AUTHORIZATION REQUEST FORM
Hospital: Indus Sanjeevani Multi-Speciality Hospital, Bandra, Mumbai
ROHINI ID: 8900412890

1. PATIENT & POLICY DETAILS:
- Insured Name: Ramesh Gupta | Age: 58 | Sex: Male
- Policy No: STAR-COMP-IND-920144 | Card No: 08992144
- Sum Insured: ₹7,50,000 | Cumulative Bonus: ₹1,50,000
- Policy Inception: 14-Aug-2022 (Tenure: 4 Years active, continuous)

2. CLINICAL DIAGNOSIS & PROCEDURE:
- Provisional Diagnosis: Nuclear Sclerosis Grade 3 Cataract (Right Eye)
- ICD-10 Code: H25.1
- Proposed Treatment: Phacoemulsification + Posterior Chamber Intraocular Lens
- Expected Length of Stay: Day Care (8 hours)
- Estimated Cost Breakdown:
  * Surgeon & OT Charges: ₹24,000
  * Foldable Hydrophobic IOL: ₹14,000
  * Pharmacy & Consumables: ₹6,000
  * Day Care Bed Charges: ₹4,000
  * Total Estimate: ₹48,000
"""
    },
    "hdfc_cholecystectomy": {
        "title": "HDFC ERGO - Laparoscopic Cholecystectomy",
        "insurer": "HDFC ERGO General Insurance",
        "policy_number": "HDFC-OPTI-901238",
        "insured_name": "Amitav Roy",
        "sum_insured": 1000000,
        "proposed_treatment": "Laparoscopic Cholecystectomy (Gallstone Pancreatitis resolution)",
        "estimated_hospital_bill": 135000,
        "hospital_room": "Single Private AC Room",
        "policy_age_years": 2,
        "document_text": """
HDFC ERGO GENERAL INSURANCE COMPANY
PRE-AUTHORIZATION CASHLESS REQUEST
Hospital: Indus Sanjeevani Hospital | Network Tier: Preferred Partner

1. PATIENT PARTICULARS:
- Insured: Amitav Roy | Age: 42 | Gender: Male
- Policy ID: HDFC-OPTI-901238 | TPA: Medi Assist India TPA
- Base Sum Insured: ₹10,00,000 | No Copay on self

2. ADMISSION & ESTIMATION:
- Diagnosis: Symptomatic Cholelithiasis with Chronic Cholecystitis
- Procedure: 4-Port Laparoscopic Cholecystectomy under GA
- Proposed Stay: 2 Days (48 Hours)
- Room Rent: Single Private Room ₹6,500/day
- Estimated Hospital Bill: ₹1,35,000
  * OT & Anesthesia: ₹55,000
  * Room Charges (2 Days): ₹13,000
  * Surgical Consumables: ₹32,000
  * Investigations & Meds: ₹35,000
"""
    },
    "ayushman_cardiac": {
        "title": "Ayushman Bharat PM-JAY - Angioplasty Pre-Auth",
        "insurer": "National Health Authority (PM-JAY)",
        "policy_number": "PMJAY-MH-77291048",
        "insured_name": "Sunil Kamble",
        "sum_insured": 500000,
        "proposed_treatment": "Percutaneous Transluminal Coronary Angioplasty (PTCA) with Drug-Eluting Stent",
        "estimated_hospital_bill": 85000,
        "hospital_room": "General Ward / CCU Care",
        "policy_age_years": 3,
        "document_text": """
AYUSHMAN BHARAT PRADHAN MANTRI JAN AROGYA YOJANA (PM-JAY)
CASHLESS SPECIALTY TREATMENT PRE-AUTHORIZATION
Empanelled Hospital: Indus Sanjeevani Super Speciality, Pune

1. BENEFICIARY DETAILS:
- Beneficiary Name: Sunil Kamble | PM-JAY ID: PMJAY-MH-77291048
- State: Maharashtra | Family Entitlement: ₹5,00,000 Cashless per annum
- Aadhaar Verified: Yes | Ration Card Status: Priority Household

2. CLINICAL & PACKAGE PARTICULARS:
- Specialty: Cardiology & Interventional Cardiac Care
- Standard Package Code: MC001B (Coronary Angioplasty with single DES)
- Package Rate Fixed by NHA: ₹85,000 (100% Cashless including stent, medicines, 5 days hospital stay)
- Patient Copay: ₹0 (Zero copay entitlement)
"""
    }
}

