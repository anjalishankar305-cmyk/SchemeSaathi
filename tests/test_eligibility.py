"""
SchemeSaathi - Unit Tests for Deterministic Eligibility Engine
Tests all 13 curated welfare schemes across Eligible, Ineligible, and Missing Info scenarios.
"""

import pytest
from app.eligibility import evaluate_scheme, find_eligible_schemes, SCHEME_METADATA

def test_metadata_completeness():
    assert len(SCHEME_METADATA) == 13
    for s_id, meta in SCHEME_METADATA.items():
        assert "name" in meta
        assert "link" in meta
        assert "benefits" in meta

# 1. PM-KISAN
def test_pm_kisan_eligible():
    res = evaluate_scheme("pm_kisan", {
        "owns_land": True,
        "occupation": "farmer",
        "is_income_tax_payer": False
    })
    assert res["status"] == "eligible"
    assert len(res["passed_rules"]) >= 2
    assert len(res["failed_rules"]) == 0

def test_pm_kisan_ineligible_taxpayer():
    res = evaluate_scheme("pm_kisan", {
        "owns_land": True,
        "occupation": "farmer",
        "is_income_tax_payer": True
    })
    assert res["status"] == "not_eligible"
    assert any("Income tax" in f for f in res["failed_rules"])

def test_pm_kisan_missing_land():
    res = evaluate_scheme("pm_kisan", {
        "is_income_tax_payer": False
    })
    assert res["status"] == "needs_more_info"
    assert any("agricultural land" in m for m in res["missing_info"])

# 2. Ayushman Bharat PM-JAY
def test_pmjay_eligible_senior_vay_vandana():
    res = evaluate_scheme("ab_pmjay", {
        "age": 72,
        "annual_income": 800000
    })
    assert res["status"] == "eligible"
    assert any("70+" in p for p in res["passed_rules"])

def test_pmjay_eligible_bpl():
    res = evaluate_scheme("ab_pmjay", {
        "age": 35,
        "ration_card_type": "BPL"
    })
    assert res["status"] == "eligible"

def test_pmjay_ineligible_high_income_under_70():
    res = evaluate_scheme("ab_pmjay", {
        "age": 45,
        "annual_income": 600000,
        "ration_card_type": "APL"
    })
    assert res["status"] == "not_eligible"

# 3. Post Matric SC Scholarship
def test_nsp_sc_eligible():
    res = evaluate_scheme("nsp_post_matric_sc", {
        "category": "SC",
        "occupation": "student",
        "annual_income": 180000
    })
    assert res["status"] == "eligible"

def test_nsp_sc_ineligible_category():
    res = evaluate_scheme("nsp_post_matric_sc", {
        "category": "General",
        "occupation": "student",
        "annual_income": 100000
    })
    assert res["status"] == "not_eligible"

def test_nsp_sc_ineligible_high_income():
    res = evaluate_scheme("nsp_post_matric_sc", {
        "category": "SC",
        "occupation": "student",
        "annual_income": 350000
    })
    assert res["status"] == "not_eligible"

# 4. PM Ujjwala Yojana
def test_pmuy_eligible():
    res = evaluate_scheme("pmuy", {
        "gender": "female",
        "age": 30,
        "has_lpg_connection": False,
        "ration_card_type": "BPL"
    })
    assert res["status"] == "eligible"

def test_pmuy_ineligible_already_has_lpg():
    res = evaluate_scheme("pmuy", {
        "gender": "female",
        "age": 30,
        "has_lpg_connection": True,
        "ration_card_type": "BPL"
    })
    assert res["status"] == "not_eligible"

def test_pmuy_ineligible_male():
    res = evaluate_scheme("pmuy", {
        "gender": "male",
        "age": 30,
        "has_lpg_connection": False
    })
    assert res["status"] == "not_eligible"

# 5. PMAY-G (Rural Housing)
def test_pmay_g_eligible():
    res = evaluate_scheme("pmay_g", {
        "owns_pucca_house": False,
        "owns_motorized_vehicle": False
    })
    assert res["status"] == "eligible"

def test_pmay_g_ineligible_owns_pucca():
    res = evaluate_scheme("pmay_g", {
        "owns_pucca_house": True
    })
    assert res["status"] == "not_eligible"

# 6. Atal Pension Yojana (APY)
def test_apy_eligible():
    res = evaluate_scheme("apy", {
        "age": 28,
        "is_income_tax_payer": False
    })
    assert res["status"] == "eligible"

def test_apy_ineligible_age_over_40():
    res = evaluate_scheme("apy", {
        "age": 45,
        "is_income_tax_payer": False
    })
    assert res["status"] == "not_eligible"

def test_apy_ineligible_taxpayer():
    res = evaluate_scheme("apy", {
        "age": 25,
        "is_income_tax_payer": True
    })
    assert res["status"] == "not_eligible"

# 7. Sukanya Samriddhi Yojana (SSY)
def test_ssy_eligible():
    res = evaluate_scheme("ssy", {
        "gender": "female",
        "age": 6
    })
    assert res["status"] == "eligible"

def test_ssy_ineligible_age_12():
    res = evaluate_scheme("ssy", {
        "gender": "female",
        "age": 12
    })
    assert res["status"] == "not_eligible"

def test_ssy_ineligible_male():
    res = evaluate_scheme("ssy", {
        "gender": "male",
        "age": 5
    })
    assert res["status"] == "not_eligible"

# 8. PM Mudra Yojana
def test_pm_mudra_eligible():
    res = evaluate_scheme("pm_mudra", {
        "age": 29,
        "occupation": "self_employed"
    })
    assert res["status"] == "eligible"

# 9. Gruha Lakshmi (Karnataka)
def test_gruha_lakshmi_eligible():
    res = evaluate_scheme("gruha_lakshmi", {
        "state": "Karnataka",
        "gender": "female",
        "has_ration_card": True,
        "ration_card_type": "BPL",
        "is_income_tax_payer": False
    })
    assert res["status"] == "eligible"

def test_gruha_lakshmi_ineligible_outside_karnataka():
    res = evaluate_scheme("gruha_lakshmi", {
        "state": "Maharashtra",
        "gender": "female",
        "has_ration_card": True,
        "is_income_tax_payer": False
    })
    assert res["status"] == "not_eligible"

def test_gruha_lakshmi_ineligible_male():
    res = evaluate_scheme("gruha_lakshmi", {
        "state": "Karnataka",
        "gender": "male",
        "has_ration_card": True,
        "is_income_tax_payer": False
    })
    assert res["status"] == "not_eligible"

# 10. Anna Bhagya (Karnataka)
def test_anna_bhagya_eligible():
    res = evaluate_scheme("anna_bhagya", {
        "state": "Karnataka",
        "ration_card_type": "BPL"
    })
    assert res["status"] == "eligible"

def test_anna_bhagya_ineligible_apl():
    res = evaluate_scheme("anna_bhagya", {
        "state": "Karnataka",
        "ration_card_type": "APL"
    })
    assert res["status"] == "not_eligible"

# 11. Gruha Jyothi (Karnataka)
def test_gruha_jyothi_eligible():
    res = evaluate_scheme("gruha_jyothi", {
        "state": "Karnataka",
        "is_domestic_electricity_consumer": True
    })
    assert res["status"] == "eligible"

# 12. Shakti (Karnataka)
def test_shakti_eligible():
    res = evaluate_scheme("shakti", {
        "state": "Karnataka",
        "gender": "female"
    })
    assert res["status"] == "eligible"

def test_shakti_ineligible_male():
    res = evaluate_scheme("shakti", {
        "state": "Karnataka",
        "gender": "male"
    })
    assert res["status"] == "not_eligible"

# 13. RTI
def test_rti_eligible():
    res = evaluate_scheme("rti", {})
    assert res["status"] == "eligible"

# Multi-Scheme Evaluation
def test_find_eligible_schemes_ranking():
    profile = {
        "age": 32,
        "gender": "female",
        "state": "Karnataka",
        "annual_income": 90000,
        "occupation": "farmer",
        "category": "OBC",
        "owns_land": True,
        "ration_card_type": "BPL",
        "has_ration_card": True,
        "is_income_tax_payer": False,
        "has_lpg_connection": False,
        "owns_pucca_house": False
    }
    ranked = find_eligible_schemes(profile)
    assert len(ranked) == 13
    assert ranked[0]["status"] == "eligible"
    # Should qualify for multiple Karnataka and Central schemes
    eligible_ids = [r["scheme_id"] for r in ranked if r["status"] == "eligible"]
    assert "gruha_lakshmi" in eligible_ids
    assert "pm_kisan" in eligible_ids
    assert "shakti" in eligible_ids
    assert "anna_bhagya" in eligible_ids
