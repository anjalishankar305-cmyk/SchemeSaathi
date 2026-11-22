# SchemeSaathi - Solution Description

## 1. What We Built
**SchemeSaathi** is a full-stack, voice-enabled, multilingual welfare explainer and deterministic eligibility engine engineered specifically for Indian citizens. It bridges the critical last-mile welfare gap by:
1. Explaining complex government policies, scheme rules, and legal rights in simple, 6th-grade language in **English, Hindi (हिन्दी), Kannada (ಕನ್ನಡ), and Tamil (தமிழ்)**.
2. Providing **two-way voice accessibility** via browser Web Speech recognition and text-to-speech synthesis, enabling illiterate and semi-literate citizens to speak their questions and hear answers spoken aloud.
3. Conducting **100% deterministic, auditable eligibility evaluations** in Python code (not probabilistic LLM guesswork), telling citizens precisely why they qualify or why they are excluded, what documents to take, and providing direct links to official government portals.
4. Parsing uploaded photos and PDFs of **official government circulars and notices**, isolating critical deadlines, affected beneficiaries, and required next steps with strict disclaimers to verify with local authorities.

---

## 2. Why AI is Essential (Not Decoration)
In many hackathon applications, AI is applied superficially as a chat wrapper. In **SchemeSaathi, AI serves indispensable, functional roles**:
- **Semantic Cross-Lingual Knowledge Retrieval (RAG):** Government policies use dense administrative terminology ("Direct Benefit Transfer", "Institutional Landholder", "Secondary Hospital Care"). AI vector embeddings and BM25 indexing map everyday conversational vernacular queries (e.g., "Doctor ke kharche ke liye kya sarkari madad hai?") to the exact statutory clauses of Ayushman Bharat PM-JAY.
- **Reading-Level Simplification & Vernacular Adaptation:** Official scheme descriptions often exceed a 14th-grade collegiate reading level. Gemini generative models actively translate and simplify legalistic gazette sentences into concise, empathetic Grade-6 explanations in Kannada, Tamil, Hindi, and English.
- **Multimodal Notice & Gazette Deconstruction:** Rural citizens frequently receive printed notices, village wall posters, or WhatsApp circulars. AI vision models inspect these unstructured multi-lingual documents, extracting issuing authorities, dates, and action items that traditional keyword search cannot parse.
- **Auditable Safety Guardrails:** AI generation is strictly constrained by prompt engineering to answer *only* from verified context with mandatory official portal citations. Crucially, eligibility decision-making is delegated to deterministic Python logic, eliminating LLM hallucinations where citizens' benefits are concerned.

---

## 3. Key Features
- **🌐 4-Language Vernacular UI & Full Localization:** Complete label switching across English, Hindi, Kannada, and Tamil.
- **🎙️ Inclusive Voice Interaction:** Built-in speech-to-text and text-to-speech synthesis tailored with Indian accent codes (`en-IN`, `hi-IN`, `kn-IN`, `ta-IN`), requiring zero additional heavy model downloads.
- **⚡ Dual-Engine Retrieval (Dense Vector + BM25):** Seamless fallback ensuring the app operates 100% offline on curated data when disconnected, or enriches answers with Gemini when online.
- **📋 13-Scheme Deterministic Rule Engine:** Evaluates Central schemes (PM-KISAN, AB-PMJAY, PM Ujjwala, APY, Sukanya Samriddhi, PMAY-G, Mudra, Post-Matric SC, RTI) and Karnataka State schemes (Gruha Lakshmi, Anna Bhagya, Gruha Jyothi, Shakti).
- **🔒 Zero-PII Privacy by Design:** No Aadhaar numbers, PANs, or personal identity records are ever collected or stored on servers. Citizen profiles exist only in the temporary browser session.
- **📑 Notice Explainer:** Drag-and-drop or camera capture of circulars with warning banners reminding citizens to verify with local panchayat officers.

---

## 4. Current Limitations & Scope for Future Scale
- **Curated Corpus Size:** The current production MVP centers on a hand-verified, high-priority dataset of 13 flagship Central and Karnataka schemes. While an ingestion pipeline is built to pull from Hugging Face and myScheme, scaling to all 2,000+ national and state schemes requires ongoing official schema verification.
- **Dynamic Policy Shifts:** Budgetary revisions and cutoff updates occur periodically. While SchemeSaathi includes persistent disclaimer banners and official portal links, real-time live synchronization with gazette RSS feeds remains a future roadmap milestone.
- **Browser Speech Variability:** Web Speech API relies on browser-native synthesis engines, which may vary across legacy Android webviews. Integrating server-side Bhashini or AI4Bharat Indic-Parler APIs would provide uniform acoustic clarity across all low-end devices.
