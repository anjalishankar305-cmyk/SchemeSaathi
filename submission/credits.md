# SchemeSaathi - Project Credits & Attribution

In compliance with IDEA//FORGE Hackathon guidelines regarding academic originality, open-source attribution, and third-party licensing, the authors gratefully acknowledge the datasets, APIs, models, and open-source libraries that made **SchemeSaathi** possible.

---

## 1. Datasets & Government Portals
- **myScheme Portal (Government of India):** The official national welfare platform (`myscheme.gov.in`) developed by the Ministry of Electronics and Information Technology (MeitY) and the National e-Governance Division (NeGD). Used as the authoritative ground truth for scheme eligibility, benefits, and required documentation.
- **Curated High-Priority Scheme Dataset:** Hand-verified dataset of 13 flagship Central and Karnataka state welfare initiatives (PM-KISAN, Ayushman Bharat PM-JAY, Post-Matric SC Scholarship, PM Ujjwala Yojana, PMAY-G, Atal Pension Yojana, Sukanya Samriddhi Yojana, PM Mudra Yojana, Gruha Lakshmi, Anna Bhagya, Gruha Jyothi, Shakti, and the Right to Information Act, 2005).
- **Hugging Face Community Datasets:**
  - `ronitnandeshwar/gov_myscheme`: Community-curated tabular welfare scheme database.
  - `shrijayan/gov_myscheme`: Scheme documentation and process descriptions.
- **State Portals:**
  - Seva Sindhu & Ahara Karnataka (`sevasindhu.karnataka.gov.in`, `ahara.kar.nic.in`): Source of truth for Karnataka Guarantee schemes.

---

## 2. Artificial Intelligence & Language Technology
- **Google Gemini API (`google-genai`):**
  - `gemini-2.5-flash` / `gemini-1.5-flash`: Multilingual vernacular synthesis, Grade-6 reading level adaptation, and multimodal visual document deconstruction.
  - `text-embedding-004`: Dense semantic embeddings for multilingual knowledge retrieval.
- **Web Speech API (W3C Standard):** Native browser speech recognition (`SpeechRecognition` / `webkitSpeechRecognition`) and speech synthesis (`SpeechSynthesisUtterance`) with Indian locale configurations (`en-IN`, `hi-IN`, `kn-IN`, `ta-IN`), ensuring zero-latency, private, and cost-free voice interaction without heavy server-side speech models.
- **Research References:** AI4Bharat (IIT Madras) and Bhashini language models referenced during design for Indic acoustic and lexical compatibility.

---

## 3. Core Open-Source Libraries & Frameworks
- **Backend & Web Framework:**
  - **FastAPI** (`fastapi.tiangolo.com`): High-performance, asynchronous REST API gateway.
  - **Uvicorn** (`uvicorn.org`): Lightning-fast ASGI server implementation.
  - **Pydantic** (`pydantic-docs.helpmanual.io`): Data validation and strict typing for citizen profiles.
- **Knowledge Retrieval & Document Processing:**
  - **Rank-BM25** (`rank-bm25`): Inverted index BM25Okapi implementation for offline keyword search.
  - **pdfplumber** (`github.com/jsvine/pdfplumber`): High-precision PDF layout and hyperlink extraction.
  - **BeautifulSoup4** (`crummy.com/software/BeautifulSoup`): Polite HTML document parsing for government public portals.
  - **Pillow (PIL)** (`python-pillow.org`): Image processing and validation for notice scans.
  - **Pandas & NumPy**: Data normalization, tabular manipulation, and vector array operations.
- **Testing & Quality Assurance:**
  - **Pytest** (`pytest.org`): Automated test runner verifying 47 unit, integration, and RAG benchmark test cases.

---

## 4. Statement of Originality
All deterministic rule formulations, multilingual localization dictionaries (`locales.js`), RAG chunking logic, custom mobile-first UI components, and API integration layers were authored originally for Track 1, Problem 1 of the IDEA//FORGE Hackathon.
