import json
import uuid
from datetime import datetime
from typing import Dict, Any, List
from data.mock_db import INSURANCE_CLAIMS, SAMPLE_POLICIES
from services.sarvam_client import sarvam_service

INSURANCE_ADJUDICATION_PROMPT = """
You are an expert Chief Medical Officer and Health Insurance Pre-Authorization Specialist adhering to IRDAI (Insurance Regulatory and Development Authority of India) and Indian TPA cashless claim guidelines.
Analyze the provided hospital cashless pre-authorization request and render an authoritative pre-authorization decision.

Review the following details:
- Insured Name, Policy Number, Insurer & TPA
- Base Sum Insured and Cumulative Bonus
- Proposed Procedure / Treatment / Surgery
- Estimated Hospital Bill & Room Category
- Policy Tenure (Years continuous) and Pre-Existing Diseases (PED)

Apply standard Indian insurance norms:
1. Room Rent Capping: Typically 1% of Sum Insured for Normal Room, 2% for ICU. If exceeded, proportionate deduction applies to associated medical charges.
2. Specific Procedure Sub-limits: Cataract surgery usually capped at ₹40,000 - ₹50,000 per eye; Joint replacement often capped at ₹1,80,000 - ₹2,50,000 depending on sum insured.
3. PED Waiting Period: Cataracts, Joint replacements, Hernia typically have 2-year waiting periods.
4. Non-Medical Consumables: Standard ~5% to 8% deduction for gloves, syringes, registration, administrative kits.
5. Co-Payment: Deduct if applicable (e.g. 10% senior citizen co-pay).

Output strictly valid JSON matching this structure:
{
  "approval_status": "Approved" or "Query Raised" or "Initial Authorization Issued",
  "approved_amount": <number in INR>,
  "patient_liability": <number in INR>,
  "room_rent_eligible_per_day": <number in INR>,
  "non_medical_deductions": <number in INR>,
  "copay_amount": <number in INR>,
  "adjudication_summary": "<concise explanation of approvals and deductions in 2-3 sentences>",
  "coordinator_checklist": [
    "<Document or test required e.g. Intraocular lens sticker, Histopathology report, Pre-operative ECG>"
  ]
}
"""

class InsuranceAgent:
    def verify_preauth(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs comprehensive cashless verification and pre-authorization adjudication.
        """
        prompt_input = f"""
Case Data for Cashless Verification:
- Patient Name: {case_data.get('patient_name')}
- Policy Number: {case_data.get('policy_number')}
- Insurance Provider: {case_data.get('insurer')}
- Sum Insured: ₹{case_data.get('sum_insured', 500000)}
- Policy Active Tenure: {case_data.get('policy_age_years', 3)} years
- Proposed Treatment: {case_data.get('treatment_name')}
- Estimated Hospital Bill: ₹{case_data.get('estimated_cost', 50000)}
- Room Category Chosen: {case_data.get('room_category', 'Twin Sharing')}
- Pre-Existing Ailments: {case_data.get('pre_existing_status', 'None declared')}
- Additional Clinical Notes/Text: {case_data.get('document_text', '')}
"""

        messages = [
            {"role": "system", "content": INSURANCE_ADJUDICATION_PROMPT},
            {"role": "user", "content": prompt_input}
        ]

        # Call Sarvam LLM for clinical insurance reasoning
        raw_response = sarvam_service.chat_complete(messages=messages, temperature=0.2)

        # Parse JSON from LLM response safely
        try:
            clean_json = raw_response.strip()
            if "```json" in clean_json:
                clean_json = clean_json.split("```json")[1].split("```")[0].strip()
            elif "```" in clean_json:
                clean_json = clean_json.split("```")[1].split("```")[0].strip()
            
            adjudication = json.loads(clean_json)
        except Exception:
            # Deterministic fallback calculation if JSON parsing encounters irregularities
            est_cost = float(case_data.get('estimated_cost', 60000))
            non_med = round(est_cost * 0.06)
            approved = round(est_cost - non_med)
            adjudication = {
                "approval_status": "Approved",
                "approved_amount": approved,
                "patient_liability": non_med,
                "room_rent_eligible_per_day": round(float(case_data.get('sum_insured', 500000)) * 0.01),
                "non_medical_deductions": non_med,
                "copay_amount": 0,
                "adjudication_summary": f"Cashless pre-authorization approved for ₹{approved:,}. Standard non-medical consumables (₹{non_med:,}) payable by patient.",
                "coordinator_checklist": ["Pre-operative diagnostic reports", "Implant barcode sticker (if applicable)", "Signed TPA cashless request form"]
            }

        claim_id = f"CLM-{uuid.uuid4().hex[:6].upper()}"
        pre_auth_code = f"{case_data.get('insurer', 'TPA')[:4].upper()}/PRE/INDUS/{datetime.now().year}/{uuid.uuid4().hex[:4].upper()}"

        claim_record = {
            "id": claim_id,
            "patient_name": case_data.get("patient_name", "Insured Member"),
            "policy_number": case_data.get("policy_number", "POL-UNKNOWN"),
            "insurer": case_data.get("insurer", "Star Health"),
            "tpa": case_data.get("tpa", "In-House Hospital TPA Desk"),
            "sum_insured": case_data.get("sum_insured", 500000),
            "treatment_name": case_data.get("treatment_name", "General Surgical Care"),
            "estimated_cost": case_data.get("estimated_cost", 50000),
            "room_category": case_data.get("room_category", "Twin Sharing"),
            "approval_status": adjudication.get("approval_status", "Approved"),
            "approved_amount": adjudication.get("approved_amount", 45000),
            "patient_liability": adjudication.get("patient_liability", 5000),
            "pre_auth_code": pre_auth_code,
            "remarks": adjudication.get("adjudication_summary", "Pre-authorization granted as per IRDAI guidelines."),
            "checklist": adjudication.get("coordinator_checklist", []),
            "updated_at": datetime.now().isoformat()
        }

        INSURANCE_CLAIMS.insert(0, claim_record)

        return {
            "success": True,
            "claim": claim_record,
            "adjudication": adjudication
        }

    def get_claims(self) -> List[Dict[str, Any]]:
        return INSURANCE_CLAIMS

    def get_sample_policy(self, sample_key: str) -> Dict[str, Any]:
        return SAMPLE_POLICIES.get(sample_key, {})

insurance_agent = InsuranceAgent()

