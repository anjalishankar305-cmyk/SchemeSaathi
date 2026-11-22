# SchemeSaathi - 2 to 3 Minute Hackathon Demo Video Script
**Target Duration:** 2 minutes 45 seconds  
**Tone:** Empathetic, crisp, confident, solution-focused  
**Actors/Audio:** Presenter voiceover + live browser interaction (clean incognito window)

---

## Timeline & Scene-by-Scene Breakdown

### [0:00 - 0:25] Scene 1: The Problem & The Mission
- **Screen:** Open SchemeSaathi homepage in an incognito browser window. Show the clean header with the Indian flag emblem and tagline.
- **Action:** Move mouse across the four language options (English, हिन्दी, ಕನ್ನಡ, தமிழ்).
- **Voiceover:**
  > *"Millions of rural and non-English speaking citizens across India miss out on life-changing welfare schemes. Why? Because government notifications and rules are buried in complex legalistic English across fragmented portals. Welcome to **SchemeSaathi** — an AI-powered, multilingual welfare explainer and eligibility engine designed for every citizen in their mother tongue."*

---

### [0:25 - 1:05] Scene 2: Vernacular Voice & RAG Chat (Kannada Flow)
- **Screen:** Click the language selector and choose **ಕನ್ನಡ (Kannada)**.
- **Action:** Note that all UI labels instantly translate into Kannada.
- **Action:** Click the 🎤 microphone button on the input bar. Speak or tap the Kannada quick-question chip:
  > *"ಗೃಹ ಲಕ್ಷ್ಮಿ ಯೋಜನೆಗೆ ಯಾವ ದಾಖಲೆಗಳು ಬೇಕು?" (What documents are needed for Gruha Lakshmi?)*
- **Screen:** The system immediately retrieves verified government records and answers in simple, Grade-6 Kannada bullet points.
- **Action:** Click the 🔊 Listen button to play back the audio via Web Speech synthesis.
- **Action:** Point out the official citation badge (`sevasindhu.karnataka.gov.in`) and the persistent verification disclaimer.
- **Voiceover:**
  > *"Notice how the entire interface switches seamlessly to Kannada. Using browser-native speech recognition, a citizen can simply speak their question. Our RAG engine searches verified scheme records and explains the exact documents needed in short, simple Kannada sentences, read aloud with one tap. Underneath, every single answer cites the official verified government portal."*

---

### [1:05 - 1:55] Scene 3: Deterministic Eligibility Engine (Central & Karnataka Schemes)
- **Screen:** Click on the second tab: **📋 Check Eligibility (ಅರ್ಹತೆ ಪರಿಶೀಲಿಸಿ)**.
- **Action:** Fill in a sample citizen profile:
  - Age: `32`
  - Gender: `Female`
  - State: `Karnataka`
  - Income: `₹85,000`
  - Occupation: `Farmer / Agriculture`
  - Landownership: `Yes`
  - Ration Card: `BPL`
  - Income Tax Payer: `No`
- **Action:** Click the large blue button: **🔍 Check All Schemes For Me**.
- **Screen:** Instant display of ranked result cards:
  - **Green Cards (Eligible):** Gruha Lakshmi (₹2,000/mo), PM-KISAN (₹6,000/yr), Shakti (Free Bus Travel), Anna Bhagya.
  - Expand Gruha Lakshmi card: show the exact checklist of passed rules ("Resident of Karnataka", "Female head of family", "BPL Ration Card holder", "Non-taxpayer").
  - Show the required documents checklist and the direct "Where to Apply" button linking directly to Seva Sindhu.
- **Voiceover:**
  > *"Here is the most critical innovation: SchemeSaathi does NOT use an LLM to guess eligibility. Decisions are computed by a 100% deterministic Python rules engine. In less than 100 milliseconds, SchemeSaathi cross-references 13 flagship welfare schemes. It displays clear green cards for schemes the citizen qualifies for, explains the exact reasons why, lists the exact physical documents to carry to the Taluk office, and provides a direct link to apply. Zero hallucinations, total auditability."*

---

### [1:55 - 2:30] Scene 4: Government Notice & Circular Explainer
- **Screen:** Click on the third tab: **📄 Explain Notice (ಸರ್ಕಾರಿ ಆದೇಶ ವಿವರಣೆ)**.
- **Action:** Drag and drop a sample government circular / order image (or PDF) into the upload dropzone.
- **Action:** Click **Explain This Document**.
- **Screen:** The system parses the document and outputs a structured breakdown:
  1. *What is this notice about?*
  2. *Which department issued it?*
  3. *Who is affected?*
  4. *Deadlines & dates*
  5. *What you need to do*
  - Prominent amber warning banner: *"Official Verification Warning: Confirm with your local Gram Panchayat or Taluk office."*
- **Voiceover:**
  > *"Whenever a citizen receives a confusing government order or printed village circular, they can upload a photo or PDF right here. SchemeSaathi extracts the core message: who it is for, key benefits, and application deadlines, accompanied by a prominent reminder to verify with local Panchayat officers before taking action."*

---

### [2:30 - 2:45] Scene 5: Privacy by Design & Conclusion
- **Screen:** Scroll down to the footer highlighting the privacy guarantee:
  *"🔒 Privacy Protected: We do NOT collect or store Aadhaar numbers or personal information. Your profile exists only in this browser session."*
- **Voiceover:**
  > *"Most importantly, we respect citizen privacy: zero Aadhaar numbers or personal data are stored. SchemeSaathi is lightweight, runs on low-end mobile phones, and is 100% demo-ready. Empowering every citizen with their rightful welfare, in their own language."*
- **Closing Title Card:** SchemeSaathi | IDEA//FORGE Hackathon Track 1, Problem 1.
