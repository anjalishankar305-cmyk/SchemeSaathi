"""
SchemeSaathi - Deterministic Rule-Based Eligibility Engine
Evaluates citizen profiles against hardcoded, hand-verified criteria in Python.
No LLM hallucinations: 100% auditable and reliable.
"""

from typing import Dict, Any, List, Optional

SCHEME_METADATA = {
    "pm_kisan": {
        "name": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
        "dept": "Ministry of Agriculture & Farmers Welfare",
        "level": "Central",
        "benefits": "Rs 6,000 per year paid in 3 instalments of Rs 2,000 via DBT.",
        "link": "https://pmkisan.gov.in"
    },
    "ab_pmjay": {
        "name": "Ayushman Bharat PM-JAY",
        "dept": "National Health Authority",
        "level": "Central",
        "benefits": "Cashless health cover up to Rs 5 lakh per family per year for hospital care.",
        "link": "https://pmjay.gov.in"
    },
    "nsp_post_matric_sc": {
        "name": "Post Matric Scholarship for SC Students",
        "dept": "Ministry of Social Justice & Empowerment",
        "level": "Central",
        "benefits": "Maintenance allowance and compulsory fees reimbursement for SC students after Class 10.",
        "link": "https://scholarships.gov.in"
    },
    "pmuy": {
        "name": "PM Ujjwala Yojana (PMUY)",
        "dept": "Ministry of Petroleum & Natural Gas",
        "level": "Central",
        "benefits": "Deposit-free LPG connection plus targeted refill subsidy.",
        "link": "https://www.pmuy.gov.in"
    },
    "pmay_g": {
        "name": "PM Awaas Yojana - Gramin (PMAY-G)",
        "dept": "Ministry of Rural Development",
        "level": "Central",
        "benefits": "Housing assistance of Rs 1.20 Lakh (plain) or Rs 1.30 Lakh (hilly) for pucca house.",
        "link": "https://pmayg.nic.in"
    },
    "apy": {
        "name": "Atal Pension Yojana (APY)",
        "dept": "PFRDA / Ministry of Finance",
        "level": "Central",
        "benefits": "Guaranteed monthly pension of Rs 1,000 to Rs 5,000 after age 60.",
        "link": "https://www.jansuraksha.gov.in"
    },
    "ssy": {
        "name": "Sukanya Samriddhi Yojana (SSY)",
        "dept": "Ministry of Finance",
        "level": "Central",
        "benefits": "High-interest savings account for girl child, exempt from tax under Section 80C.",
        "link": "https://www.indiapost.gov.in"
    },
    "pm_mudra": {
        "name": "PM Mudra Yojana (PMMY)",
        "dept": "Ministry of Finance (MUDRA)",
        "level": "Central",
        "benefits": "Collateral-free business loans up to Rs 10 Lakh (Tarun Plus up to Rs 20 Lakh).",
        "link": "https://www.mudra.org.in"
    },
    "gruha_lakshmi": {
        "name": "Gruha Lakshmi (Karnataka)",
        "dept": "Dept of Women & Child Development, Karnataka",
        "level": "Karnataka",
        "benefits": "Rs 2,000 per month paid to woman head of the family by DBT.",
        "link": "https://sevasindhu.karnataka.gov.in"
    },
    "anna_bhagya": {
        "name": "Anna Bhagya (Karnataka)",
        "dept": "Dept of Food & Civil Supplies, Karnataka",
        "level": "Karnataka",
        "benefits": "Food grains under NFSA (5 kg/member) plus additional grain or DBT support.",
        "link": "https://ahara.kar.nic.in"
    },
    "gruha_jyothi": {
        "name": "Gruha Jyothi (Karnataka)",
        "dept": "Energy Dept, Karnataka",
        "level": "Karnataka",
        "benefits": "Up to 200 units of free electricity per month for domestic consumers.",
        "link": "https://sevasindhu.karnataka.gov.in"
    },
    "shakti": {
        "name": "Shakti - Free Bus Travel for Women (Karnataka)",
        "dept": "Transport Dept, Karnataka",
        "level": "Karnataka",
        "benefits": "Free travel for women in ordinary state-run buses within Karnataka.",
        "link": "https://sevasindhu.karnataka.gov.in"
    },
    "rti": {
        "name": "Right to Information Act, 2005 (RTI)",
        "dept": "Dept of Personnel & Training",
        "level": "Central",
        "benefits": "Legal right to obtain timely government information within 30 days.",
        "link": "https://rti.gov.in"
    }
}

def evaluate_scheme(scheme_id: str, profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates profile against a specific scheme.
    Returns status: 'eligible' | 'not_eligible' | 'needs_more_info'
    along with passed_rules, failed_rules, missing_info, documents, and next steps.
    """
    meta = SCHEME_METADATA.get(scheme_id)
    if not meta:
        return {
            "scheme_id": scheme_id,
            "status": "not_eligible",
            "passed_rules": [],
            "failed_rules": ["Scheme ID not recognized in verified database."],
            "missing_info": [],
            "documents": [],
            "apply_url": "https://www.myscheme.gov.in",
            "next_steps": "Check the national scheme portal for this scheme."
        }
        
    passed = []
    failed = []
    missing = []
    docs = []
    apply_url = meta["link"]
    next_steps = ""

    # Safe profile getters
    age = profile.get("age")
    gender = str(profile.get("gender", "")).lower()
    state = str(profile.get("state", "")).title()
    income = profile.get("annual_income")
    occupation = str(profile.get("occupation", "")).lower()
    category = str(profile.get("category", "")).upper()
    owns_land = profile.get("owns_land")
    has_ration_card = profile.get("has_ration_card")
    ration_card_type = str(profile.get("ration_card_type", "")).upper()
    is_taxpayer = profile.get("is_income_tax_payer")
    is_student = profile.get("is_student")
    has_lpg = profile.get("has_lpg_connection")
    owns_pucca = profile.get("owns_pucca_house")
    owns_vehicle = profile.get("owns_motorized_vehicle")
    is_power_consumer = profile.get("is_domestic_electricity_consumer")

    if scheme_id == "pm_kisan":
        docs = ["Aadhaar Card", "Land ownership records (RTC / Khata / Patta)", "Aadhaar-seeded Bank Account Passbook", "Active Mobile Number"]
        next_steps = "Visit pmkisan.gov.in > Farmers Corner > New Farmer Registration or visit your nearest CSC center."
        
        if owns_land is None:
            missing.append("Cultivable agricultural land ownership")
        elif owns_land is True:
            passed.append("Family owns cultivable agricultural land.")
        else:
            failed.append("Cultivable agricultural land in family name is mandatory.")

        if occupation:
            if occupation == "farmer" or owns_land is True:
                passed.append("Farming occupation criterion satisfied.")
            else:
                failed.append("Applicant must be engaged in farming.")

        if is_taxpayer is None:
            missing.append("Income tax payer status")
        elif is_taxpayer is False:
            passed.append("Not an income tax payer.")
        else:
            failed.append("Income tax payers in last assessment year are strictly excluded.")

    elif scheme_id == "ab_pmjay":
        docs = ["Aadhaar Card", "Ration Card / Family ID document", "Mobile Number"]
        next_steps = "Visit pmjay.gov.in to verify your name in the database, or approach an Ayushman Mitra at any empanelled hospital."
        
        # 70+ Universal Vay Vandana extension
        if age is not None and age >= 70:
            passed.append(f"Senior citizen aged 70+ (Age: {age}) eligible under universal Vay Vandana health coverage.")
        else:
            # Check BPL / low income criteria
            is_bpl = ration_card_type in ["BPL", "AAY", "PHH"] or has_ration_card is True
            if is_bpl:
                passed.append("Identified through BPL / Antyodaya / Priority ration card criteria.")
            elif income is not None:
                if income <= 250000:
                    passed.append(f"Family income (Rs {income:,.0f}) falls within low-income welfare threshold.")
                else:
                    failed.append(f"Annual income (Rs {income:,.0f}) exceeds welfare assistance criteria (unless age 70+).")
            elif age is None and has_ration_card is None:
                missing.append("Age or Ration Card / Income details")

    elif scheme_id == "nsp_post_matric_sc":
        docs = ["Caste Certificate (SC)", "Family Income Certificate", "Previous Academic Marksheet", "Admission & Fee Receipt", "Bank Passbook (Aadhaar linked)"]
        next_steps = "Register and apply online on scholarships.gov.in during the open national scholarship cycle."

        if not category:
            missing.append("Social Category (SC/ST/OBC/General)")
        elif category == "SC":
            passed.append("Belongs to Scheduled Caste (SC) category.")
        else:
            failed.append("Scheme is specifically restricted to Scheduled Caste (SC) candidates.")

        if is_student is None and not occupation:
            missing.append("Student enrollment status")
        elif is_student is True or occupation == "student":
            passed.append("Currently pursuing post-matric/post-secondary education.")
        else:
            failed.append("Must be an active student enrolled in recognized post-matric course.")

        if income is None:
            missing.append("Annual Family Income")
        elif income <= 250000:
            passed.append(f"Family income (Rs {income:,.0f}) is within the Rs 2.5 Lakh limit.")
        else:
            failed.append(f"Family income (Rs {income:,.0f}) exceeds the Rs 2.5 Lakh annual ceiling.")

    elif scheme_id == "pmuy":
        docs = ["Aadhaar Card", "BPL / Priority Ration Card or 14-point declaration", "Bank Account Details", "Passport Size Photograph", "Address Proof"]
        next_steps = "Submit the KYC form at your local LPG distributor (Indane, BharatGas, HP) or apply on pmuy.gov.in."

        if not gender:
            missing.append("Gender")
        elif gender in ["female", "woman", "f"]:
            passed.append("Applicant is a female head/representative.")
        else:
            failed.append("Only adult women are eligible to receive the LPG connection in their name.")

        if age is None:
            missing.append("Age")
        elif age >= 18:
            passed.append(f"Applicant is an adult ({age} years old).")
        else:
            failed.append("Applicant must be at least 18 years of age.")

        if has_lpg is None:
            missing.append("Existing LPG connection status in household")
        elif has_lpg is False:
            passed.append("No prior LPG cylinder connection in household.")
        else:
            failed.append("Households with an existing LPG connection are ineligible.")

        is_poor = ration_card_type in ["BPL", "AAY", "PHH"] or (income is not None and income <= 200000)
        if is_poor:
            passed.append("Poor/BPL household criteria satisfied.")
        elif ration_card_type == "APL":
            failed.append("APL ration card holders are generally excluded from PM Ujjwala free connection.")

    elif scheme_id == "pmay_g":
        docs = ["Aadhaar Card", "MGNREGA Job Card (if available)", "Bank Account Details", "Land/House site photo"]
        next_steps = "Contact your Gram Panchayat Secretary or Block Development Officer; verify your name in Awaas+ list."

        if owns_pucca is None:
            missing.append("Pucca (concrete) house ownership status")
        elif owns_pucca is False:
            passed.append("Does not own a permanent pucca house.")
        else:
            failed.append("Households owning a pucca house are excluded.")

        if owns_vehicle is None:
            pass  # not strictly blocking unless confirmed
        elif owns_vehicle is False:
            passed.append("Does not own motorized vehicles.")
        elif owns_vehicle is True:
            failed.append("Owning a motorized vehicle triggers automatic exclusion under SECC rules.")

    elif scheme_id == "apy":
        docs = ["Aadhaar Card", "Savings Bank Account details with Auto-Debit consent", "Mobile Number", "Nominee Details"]
        next_steps = "Visit your bank branch or log in to your Internet Banking portal and enroll under Atal Pension Yojana."

        if age is None:
            missing.append("Age")
        elif 18 <= age <= 40:
            passed.append(f"Age ({age}) is within the permissible 18 to 40 years bracket.")
        else:
            failed.append(f"Age ({age}) is outside the permissible 18 to 40 years window.")

        if is_taxpayer is None:
            missing.append("Income tax payer status")
        elif is_taxpayer is False:
            passed.append("Non-income tax payer.")
        else:
            failed.append("Income tax payers are barred from enrolling in APY (rule since Oct 2022).")

    elif scheme_id == "ssy":
        docs = ["Girl Child's Birth Certificate", "Parent / Legal Guardian ID Proof", "Address Proof", "Initial deposit (min Rs 250)"]
        next_steps = "Visit any authorized Post Office or commercial bank branch with the child's birth certificate."

        if not gender:
            missing.append("Gender of child")
        elif gender in ["female", "girl", "woman", "f"]:
            passed.append("Account is opened for a girl child.")
        else:
            failed.append("Sukanya Samriddhi Yojana is exclusively for girl children.")

        if age is None:
            missing.append("Age of the girl child")
        elif age <= 10:
            passed.append(f"Child age ({age}) is under 10 years at account opening.")
        else:
            failed.append(f"Child age ({age}) exceeds the maximum entry age of 10 years.")

    elif scheme_id == "pm_mudra":
        docs = ["Identity Proof (Aadhaar / Voter ID)", "Address Proof", "Detailed Business Plan / Proposal", "Bank statements of last 6 months"]
        next_steps = "Approach your commercial bank, RRB, MFI or apply online at udyamimitra.in."

        if age is not None:
            if age >= 18:
                passed.append(f"Applicant is an adult ({age} years).")
            else:
                failed.append("Applicant must be at least 18 years old to secure a business loan.")
        passed.append("Non-farm micro or small business enterprise eligibility.")

    elif scheme_id == "gruha_lakshmi":
        docs = ["Karnataka Ration Card (BPL / AAY / APL)", "Aadhaar Card of Woman Head", "Aadhaar-linked Bank Account Passbook", "Mobile Number"]
        next_steps = "Apply on Seva Sindhu portal (sevasindhu.karnataka.gov.in) or visit Grama One / Bangalore One / Karnataka One center."

        if not state:
            missing.append("State of residence")
        elif state == "Karnataka":
            passed.append("Resident of Karnataka.")
        else:
            failed.append(f"Scheme is strictly restricted to Karnataka residents (Applicant state: {state}).")

        if not gender:
            missing.append("Gender")
        elif gender in ["female", "woman", "f"]:
            passed.append("Beneficiary is a woman head of household.")
        else:
            failed.append("Only the female head of the family is eligible.")

        if has_ration_card is None and not ration_card_type:
            missing.append("Ration Card possession in Karnataka")
        elif has_ration_card is True or ration_card_type in ["BPL", "AAY", "APL"]:
            passed.append(f"Valid Karnataka ration card holder ({ration_card_type or 'Standard'}).")
        else:
            failed.append("Must possess an active BPL, APL, or Antyodaya ration card in Karnataka.")

        if is_taxpayer is None:
            missing.append("Income tax / GST payer status of woman or spouse")
        elif is_taxpayer is False:
            passed.append("Neither applicant nor spouse is an income tax / GST payer.")
        else:
            failed.append("Families where the woman head or spouse pays income tax or GST are excluded.")

    elif scheme_id == "anna_bhagya":
        docs = ["BPL / Antyodaya Ration Card", "Aadhaar Cards of all family members", "Aadhaar-seeded Bank Account for DBT component"]
        next_steps = "Collect rations at your assigned Fair Price Shop (PDS); check DBT status on ahara.kar.nic.in."

        if not state:
            missing.append("State of residence")
        elif state == "Karnataka":
            passed.append("Resident of Karnataka.")
        else:
            failed.append(f"Only applicable in Karnataka (Applicant state: {state}).")

        if not ration_card_type:
            missing.append("Ration card type (BPL/AAY/APL)")
        elif ration_card_type in ["BPL", "AAY", "PHH"]:
            passed.append(f"Eligible ration card category ({ration_card_type}).")
        else:
            failed.append(f"APL cardholders ({ration_card_type}) are excluded from Anna Bhagya NFSA foodgrain subsidy.")

    elif scheme_id == "gruha_jyothi":
        docs = ["Consumer ID / Account ID from electricity bill", "Aadhaar Card", "Rental / Lease agreement (if tenant)"]
        next_steps = "Register your electricity account ID on the Seva Sindhu portal (sevasindhu.karnataka.gov.in)."

        if not state:
            missing.append("State of residence")
        elif state == "Karnataka":
            passed.append("Resident of Karnataka.")
        else:
            failed.append(f"Only applicable in Karnataka (Applicant state: {state}).")

        if is_power_consumer is not False:
            passed.append("Domestic electricity consumer in Karnataka ESCOM area.")
        else:
            failed.append("Only domestic residential meter connections qualify (commercial meters excluded).")

    elif scheme_id == "shakti":
        docs = ["Government ID with Karnataka Address (Voter ID, Aadhaar, Driving License, or Shakti Smart Card)"]
        next_steps = "Board ordinary non-luxury buses (KSRTC/BMTC/NWKRTC/KKRTC) and show your valid Karnataka ID card."

        if not state:
            missing.append("State of residence")
        elif state == "Karnataka":
            passed.append("Resident of Karnataka.")
        else:
            failed.append(f"Free bus travel is for Karnataka residents (Applicant state: {state}).")

        if not gender:
            missing.append("Gender")
        elif gender in ["female", "woman", "f"]:
            passed.append("Eligible woman citizen.")
        else:
            failed.append("Shakti free bus travel is exclusively for women citizens.")

    elif scheme_id == "rti":
        docs = ["Application form / letter specifying requested info", "BPL Certificate (if claiming fee exemption)"]
        next_steps = "File online at rtionline.gov.in (for Central ministries) or state RTI portal, or post to the Public Information Officer (PIO) with Rs 10 fee."
        passed.append("All Indian citizens have the legal right to seek public records.")

    # Determine final status
    if failed:
        status = "not_eligible"
    elif missing:
        status = "needs_more_info"
    else:
        status = "eligible"

    return {
        "scheme_id": scheme_id,
        "scheme_name": meta["name"],
        "category": meta.get("category", "General"),
        "dept": meta["dept"],
        "level": meta["level"],
        "benefits": meta["benefits"],
        "status": status,
        "passed_rules": passed,
        "failed_rules": failed,
        "missing_info": missing,
        "documents": docs,
        "apply_url": apply_url,
        "next_steps": next_steps
    }

def find_eligible_schemes(profile: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Evaluates all curated schemes against a citizen's profile and returns a ranked list."""
    results = []
    for s_id in SCHEME_METADATA.keys():
        eval_res = evaluate_scheme(s_id, profile)
        results.append(eval_res)
        
    status_order = {"eligible": 0, "needs_more_info": 1, "not_eligible": 2}
    results.sort(key=lambda r: (status_order.get(r["status"], 3), -len(r["passed_rules"])))
    return results
