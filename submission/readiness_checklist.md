# IDEA//FORGE Hackathon - Submission Readiness Checklist
**Track 1, Problem 1 | Deadline: 22 Nov 11:59 PM IST**

This checklist verifies that the SchemeSaathi submission adheres strictly to all mandatory hackathon requirements and evaluation rubrics.

---

## 1. Hackathon Eligibility & Deliverables Checklist

| Requirement | Status | Verification Details |
|---|:---:|---|
| **Problem Statement Clarity** | ✅ READY | `submission/problem_statement.md` clearly specifies **who faces the problem** (smallholder farmers, rural women, low-literacy vernacular speakers, SC/ST students, senior citizens) and **why it matters**. |
| **Complete Solution Description** | ✅ READY | `submission/solution_description.md` details what was built, how it works, technical architecture, why AI is essential, key features, and current limitations. |
| **System Architecture Diagram** | ✅ READY | `submission/architecture.md` contains an end-to-end Mermaid diagram illustrating the data ingestion, RAG retrieval, deterministic rule engine, and client voice layer. |
| **Demo Script & Video Plan** | ✅ READY | `submission/demo_script.md` provides a timed 2 to 3 minute script demonstrating Kannada voice query, spoken TTS response, deterministic eligibility, and notice upload. |
| **Attribution & Credits** | ✅ READY | `submission/credits.md` attributes all datasets (myScheme, Hugging Face), APIs (Gemini, Web Speech API), and open-source libraries. |
| **Public MVP Link (Incognito Ready)** | 📋 PENDING USER DEPLOY | Dockerfile, `render.yaml`, and step-by-step 1-click deployment instructions are prepared in `README.md`. App runs publicly without login or authentication walls. |
| **Project Tagline & Metadata** | ✅ READY | `submission/project_name.txt` contains clean project title and compelling one-line tagline. |
| **Code Reliability & Tests** | ✅ READY | 47 automated unit and integration tests passing (`pytest tests/`), including 10/10 RAG benchmark questions in `tests/eval_report.md`. |
| **Air-Gapped / Offline Fallback** | ✅ READY | System operates 100% offline on curated data without network access or when `GEMINI_API_KEY` is not provided. |
| **Privacy by Design** | ✅ READY | No Aadhaar numbers, PANs, or personal identity documents are collected or stored. |
| **Final Submission on Challazo** | 📋 PENDING USER ACTION | Ensure submission status is changed from **Draft** to **Submitted** before **22 Nov 11:59 PM IST**. |

---

## 2. Immediate Action Steps for the Team
1. **Configure GEMINI_API_KEY in `.env`:** Copy `.env.example` to `.env` and paste your Google AI Studio API key.
2. **Deploy to Render or Hugging Face Spaces:** Follow the 4-click guide in `README.md` to get your public MVP URL. Test the public URL in a private/incognito window.
3. **Record Demo Video (2m 45s):** Follow `submission/demo_script.md`. Use Loom, OBS, or Chrome screen recorder. Upload to YouTube (Unlisted) or Google Drive (Public view).
4. **Submit on Challazo:** Paste the problem statement, solution description, GitHub repo link, public MVP link, and demo video link. Click **Submit** (do not leave in Draft state)!
