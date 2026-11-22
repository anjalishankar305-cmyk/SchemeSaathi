# SchemeSaathi 🇮🇳
### Multilingual Policy, Rights & Scheme Explainer
**IDEA//FORGE Hackathon | Track 1, Problem 1**

[![Tests](https://img.shields.io/badge/pytest-47%20passed-brightgreen.svg)](tests/)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.14-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-1.0.0-009688.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## The Problem
> Millions of people in India, especially rural, low-literacy and non-English speakers (farmers, women, students, senior citizens), miss welfare benefits because government notices and scheme rules are written in complex English/legalese, spread across many websites, and hard to check for eligibility. SchemeSaathi explains schemes, notices and rights in simple language in English, Hindi, Kannada and Tamil, by text and by voice, checks eligibility, and tells people exactly which documents to carry and where to apply.

---

## Key Features

1. **🌐 4-Language Vernacular UI & Localization:**
   - Full bilingual / localized interface supporting **English, हिन्दी (Hindi), ಕನ್ನಡ (Kannada), and தமிழ் (Tamil)**.
   - All UI labels, placeholders, buttons, and system responses translate dynamically with zero lag.

2. **🎙️ Two-Way Voice Accessibility (Speech-to-Text & Text-to-Speech):**
   - Built on the native browser **Web Speech API** configured for Indian speech accents (`en-IN`, `hi-IN`, `kn-IN`, `ta-IN`).
   - Illiterate or semi-literate citizens can tap the microphone to ask questions and tap the speaker icon to listen to answers read aloud.

3. **⚡ Hybrid Knowledge Base & RAG:**
   - Combines BM25 keyword inverted indexing with Gemini dense vector embeddings.
   - **Guaranteed 100% Offline Mode:** Functions flawlessly without network access or when `GEMINI_API_KEY` is not present, using grounded rule synthesizers with verifiable portal citations.

4. **📋 Deterministic, Auditable Eligibility Engine:**
   - Evaluates citizen profiles against **13 flagship welfare schemes** in Python code (not probabilistic LLM guesswork).
   - Generates color-coded cards: **Eligible (Green)**, **Needs More Info (Amber)**, and **Not Eligible (Red)**.
   - Explicitly explains *why* a citizen qualifies, reasons for failure, exact required documents to carry, and official portal links (`pmkisan.gov.in`, `sevasindhu.karnataka.gov.in`).

5. **📄 Multimodal Notice & Circular Explainer:**
   - Accepts mobile photos, scans, or PDFs of official government orders and notices.
   - Simplifies documents into clear sections: *What is this?*, *Issuing Department*, *Target Beneficiaries*, *Deadlines*, and *Action Steps*, accompanied by an official verification advisory.

6. **🔒 Privacy by Design:**
   - **Zero Aadhaar or Personal ID Collection:** Citizen profiles exist purely in client-side memory during the active session. No PII is logged, stored, or sent to third-party databases.

---

## Curated Schemes Covered

| Scheme Identifier | Scheme Name | Level | Key Benefit |
|---|---|---|---|
| `pm_kisan` | PM-KISAN (Pradhan Mantri Kisan Samman Nidhi) | Central | ₹6,000/yr DBT in 3 installments |
| `ab_pmjay` | Ayushman Bharat PM-JAY & Vay Vandana | Central | Cashless hospital cover up to ₹5 Lakh/yr (universal for 70+) |
| `nsp_post_matric_sc` | Post Matric Scholarship for SC Students | Central | Maintenance allowance + compulsory fee waiver |
| `pmuy` | PM Ujjwala Yojana (PMUY) | Central | Deposit-free LPG cylinder connection + refill subsidy |
| `pmay_g` | PM Awaas Yojana - Gramin | Central | ₹1.20L (plain) / ₹1.30L (hilly) assistance for pucca house |
| `apy` | Atal Pension Yojana (APY) | Central | Guaranteed monthly pension ₹1,000 - ₹5,000 after age 60 |
| `ssy` | Sukanya Samriddhi Yojana (SSY) | Central | High-interest girl child savings account (tax-free under 80C) |
| `pm_mudra` | PM Mudra Yojana (PMMY) | Central | Collateral-free business loans up to ₹10-20 Lakh |
| `gruha_lakshmi` | Gruha Lakshmi (Karnataka) | Karnataka | ₹2,000/month DBT to female head of household |
| `anna_bhagya` | Anna Bhagya (Karnataka) | Karnataka | 5kg foodgrains/member + cash support for BPL/AAY |
| `gruha_jyothi` | Gruha Jyothi (Karnataka) | Karnataka | Up to 200 units of free electricity per month |
| `shakti` | Shakti Free Bus Travel (Karnataka) | Karnataka | Free travel for women on ordinary state-run buses |
| `rti` | Right to Information Act, 2005 (RTI) | Central | Legal right to timely government information within 30 days |

---

## Project Structure

```
schemesaathi/
├── input/                          # Core input files (CSV, JSON, PDFs)
│   ├── schemes_dataset.csv
│   ├── schemes_dataset.json
│   ├── Scheme_Dataset.pdf
│   └── Scheme_Explainer_Datasets.pdf
├── data/
│   ├── raw/                        # Ingested raw datasets (HF, official sites)
│   ├── processed/
│   │   └── schemes.jsonl           # Unified normalized scheme records
│   ├── index/                      # Pre-built RAG indexes
│   │   ├── bm25_index.pkl          # BM25 inverted index
│   │   └── chunks.json             # Structured section chunks
│   └── ingest_report.md            # Comprehensive ingestion pipeline audit
├── scripts/
│   ├── ingest_datasets.py          # Automated ingestion & PDF URL extractor
│   └── build_index.py              # Knowledge base chunker and indexer
├── app/
│   ├── main.py                     # FastAPI backend & static mount
│   ├── config.py                   # App configuration & environment loader
│   ├── rag.py                      # RAG retrieval and answer synthesizer
│   ├── eligibility.py              # 100% deterministic rule engine
│   ├── notice.py                   # Multimodal notice parser
│   └── i18n.py                     # Multilingual constants and system prompts
├── static/
│   ├── index.html                  # Accessible, mobile-first responsive UI
│   ├── style.css                   # High-contrast accessible styling
│   ├── app.js                      # Voice interaction, chat & eligibility client
│   └── locales.js                  # Complete 4-language localization strings
├── tests/
│   ├── test_eligibility.py         # Unit tests for all 13 schemes (32 tests)
│   ├── test_ingest.py              # PDF extraction and classifier tests (3 tests)
│   ├── test_api.py                 # FastAPI endpoint & asset tests (11 tests)
│   ├── test_rag_eval.py            # 10 canonical benchmark questions
│   └── eval_report.md              # RAG benchmark evaluation report (100% score)
├── submission/                     # Hackathon submission materials
│   ├── project_name.txt
│   ├── problem_statement.md
│   ├── solution_description.md
│   ├── architecture.md
│   ├── demo_script.md
│   ├── credits.md
│   └── readiness_checklist.md
├── requirements.txt                # Production dependencies
├── .env.example                    # Environment variable template
├── Dockerfile                      # Production container spec
├── render.yaml                     # Render 1-click blueprint
└── README.md
```

---




- **Core Technology:** FastAPI, Python, Gemini 2.5 Flash, Web Speech API, BM25 Okapi, pdfplumber.
- **Evaluation Accuracy:** 10/10 (100%) on official benchmark test cases.
- **Auditable Rules:** Zero hallucinations on eligibility.
