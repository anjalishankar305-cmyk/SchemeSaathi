"""
SchemeSaathi - FastAPI Endpoint Unit & Integration Tests
Directly validates all API handler functions, request validation, logic, and static assets.
"""

import os
import pytest
from app.main import (
    health,
    get_all_schemes,
    get_scheme_by_id,
    chat,
    check_single_eligibility,
    find_all_eligible,
    ChatRequest,
    EligibilitySingleRequest,
    ProfileFindRequest
)

def test_health_endpoint():
    res = health()
    assert res["status"] == "healthy"
    assert res["app"] == "SchemeSaathi"
    assert res["schemes_loaded"] >= 12
    assert res["chunks_indexed"] >= 50
    assert "en" in res["supported_languages"]
    assert "kn" in res["supported_languages"]
    assert "hi" in res["supported_languages"]
    assert "ta" in res["supported_languages"]

def test_get_all_schemes():
    res = get_all_schemes()
    assert res["count"] >= 12
    assert len(res["schemes"]) >= 12
    first = res["schemes"][0]
    assert "name" in first
    assert "benefits" in first
    assert "link" in first

def test_get_scheme_by_id_valid():
    s = get_scheme_by_id("pm_kisan")
    assert s["id"] == "pm_kisan"
    assert "PM-KISAN" in s["name"]

def test_get_scheme_by_id_invalid():
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as exc:
        get_scheme_by_id("non_existent_scheme")
    assert exc.value.status_code == 404

def test_chat_english():
    req = ChatRequest(message="What documents are required for Gruha Lakshmi?", language="en")
    res = chat(req)
    assert "answer" in res
    assert len(res["answer"]) > 10
    assert res["language"] == "en"
    assert len(res["citations"]) > 0
    assert any("gruha lakshmi" in c["scheme_name"].lower() for c in res["citations"])

def test_chat_kannada():
    req = ChatRequest(message="ಗೃಹ ಲಕ್ಷ್ಮಿ ಯೋಜನೆಗೆ ಯಾವ ದಾಖಲೆಗಳು ಬೇಕು?", language="kn")
    res = chat(req)
    assert "answer" in res
    assert res["language"] == "kn"

def test_chat_hindi():
    req = ChatRequest(message="पीएम किसान योजना के लिए कौन पात्र है?", language="hi")
    res = chat(req)
    assert "answer" in res
    assert res["language"] == "hi"

def test_chat_tamil():
    req = ChatRequest(message="பிஎம்-கிசான் திட்டத்திற்கு என்ன தகுதி?", language="ta")
    res = chat(req)
    assert "answer" in res
    assert res["language"] == "ta"

def test_eligibility_single():
    req = EligibilitySingleRequest(
        scheme_id="gruha_lakshmi",
        profile={
            "state": "Karnataka",
            "gender": "female",
            "has_ration_card": True,
            "is_income_tax_payer": False
        }
    )
    res = check_single_eligibility(req)
    assert res["status"] == "eligible"
    assert len(res["passed_rules"]) > 0
    assert len(res["documents"]) > 0
    assert "sevasindhu.karnataka.gov.in" in res["apply_url"]

def test_eligibility_find():
    req = ProfileFindRequest(
        profile={
            "age": 30,
            "gender": "female",
            "state": "Karnataka",
            "has_ration_card": True,
            "ration_card_type": "BPL",
            "is_income_tax_payer": False,
            "owns_land": True,
            "occupation": "farmer"
        }
    )
    res = find_all_eligible(req)
    assert res["total_checked"] >= 12
    eligible_ids = [r["scheme_id"] for r in res["results"] if r["status"] == "eligible"]
    assert "gruha_lakshmi" in eligible_ids
    assert "pm_kisan" in eligible_ids

def test_static_assets_exist():
    assert os.path.exists("static/index.html")
    assert os.path.exists("static/style.css")
    assert os.path.exists("static/app.js")
    assert os.path.exists("static/locales.js")
    
    with open("static/index.html", "r", encoding="utf-8") as f:
        html = f.read()
        assert "SchemeSaathi" in html
        assert "tabAsk" in html or "tabAskBtn" in html
        assert "langSelect" in html
