"""
SchemeSaathi - Government Notice & Circular Explainer
Parses uploaded notice images or PDFs and simplifies them into 
structured, plain-language insights (what, who, deadlines, actions, docs) with verification warning.
"""

import os
import re
import io
from typing import Dict, Any
from PIL import Image
from .config import GEMINI_API_KEY
from .i18n import LANGUAGES, get_disclaimer

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """Extract plain text from PDF bytes using pdfplumber."""
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            pages_text = [p.extract_text() or "" for p in pdf.pages[:5]]
            return "\n\n".join(pages_text).strip()
    except Exception as e:
        return f"Error extracting PDF text: {e}"

def extract_dates_and_deadlines(text: str) -> list:
    """Heuristic regex search for dates, deadlines, and time limits."""
    date_patterns = [
        r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
        r'\b\d{1,2}(?:st|nd|rd|th)?\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{2,4}\b',
        r'\b(?:within|before|by|last date:?)\s+[^.,;\n]{1,30}'
    ]
    found = []
    for pat in date_patterns:
        for match in re.finditer(pat, text, re.IGNORECASE):
            found.append(match.group(0).strip())
    return list(dict.fromkeys(found))[:5]

def explain_notice(file_bytes: bytes, filename: str, content_type: str, language: str = "en") -> Dict[str, Any]:
    """Explains a notice image or PDF in simple language."""
    if language not in LANGUAGES:
        language = "en"

    is_pdf = filename.lower().endswith(".pdf") or "pdf" in content_type.lower()
    api_key = GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "").strip()

    lang_name = LANGUAGES[language]
    warning_text = (
        "OFFICIAL VERIFICATION WARNING: This is an AI-assisted simplification of the document. "
        "Government guidelines and notifications are legally binding only in their official gazette/order form. "
        "Always confirm dates, procedures, and conditions with your local Gram Panchayat, Taluk Office, or the official department portal."
    )

    if api_key:
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=api_key)
            prompt = (
                f"You are SchemeSaathi. Explain this Indian government circular/notice/order in simple {lang_name} at a 6th-grade reading level.\n"
                f"Format your response with the following clear markdown headings:\n"
                f"1. **Summary & Title**: What is this notice about?\n"
                f"2. **Issuing Authority**: Which department or ministry issued it?\n"
                f"3. **Who Is It For?**: Who qualifies or is affected by this?\n"
                f"4. **Key Decisions & Benefits**: What help, funds, or changes are announced?\n"
                f"5. **Important Deadlines**: What are the critical dates to remember?\n"
                f"6. **What You Need To Do**: Step-by-step actions for the citizen.\n"
                f"7. **Required Documents**: Documents to carry or submit.\n\n"
                f"Ensure the language is empathetic and plain {lang_name}."
            )

            target_model = "gemini-3.8-flash"
            try:
                if is_pdf:
                    extracted_text = extract_text_from_pdf_bytes(file_bytes)
                    if not extracted_text or len(extracted_text) < 20:
                        extracted_text = f"Notice filename: {filename}. (PDF scanned / non-selectable text)."
                    contents = f"{prompt}\n\nNOTICE CONTENT:\n{extracted_text[:6000]}"
                    res = client.models.generate_content(
                        model=target_model,
                        contents=contents
                    )
                else:
                    image = Image.open(io.BytesIO(file_bytes))
                    res = client.models.generate_content(
                        model=target_model,
                        contents=[image, prompt]
                    )
            except Exception:
                target_model = "gemini-2.5-flash"
                if is_pdf:
                    contents = f"{prompt}\n\nNOTICE CONTENT:\n{extracted_text[:6000]}"
                    res = client.models.generate_content(
                        model=target_model,
                        contents=contents
                    )
                else:
                    image = Image.open(io.BytesIO(file_bytes))
                    res = client.models.generate_content(
                        model=target_model,
                        contents=[image, prompt]
                    )

            return {
                "success": True,
                "filename": filename,
                "explanation": res.text.strip(),
                "language": language,
                "warning": warning_text,
                "model_used": f"Gemini ({target_model}) Vision/Text"
            }
        except Exception as e:
            print(f"[Notice] Gemini multimodal error: {e}")

    # Fallback offline analysis
    if is_pdf:
        extracted_text = extract_text_from_pdf_bytes(file_bytes)
        deadlines = extract_dates_and_deadlines(extracted_text)
        sample_preview = " ".join(extracted_text.split()[:120])
        
        explanation = (
            f"**Notice Document:** `{filename}`\n\n"
            f"**1. What It Is:**\nExtracted official notice text:\n> \"{sample_preview}...\"\n\n"
            f"**2. Potential Deadlines / Timelines Detected:**\n" +
            ("\n".join([f"- {d}" for d in deadlines]) if deadlines else "- No explicit date patterns detected; check official circular text.") +
            f"\n\n**3. Required Action:**\nPresent this document to your local administrative officer (Grama Panchayat / Seva Kendra / Department Officer) to confirm whether your village or household is covered."
        )
    else:
        explanation = (
            f"**Notice Image:** `{filename}`\n\n"
            f"Image successfully uploaded and received for notice explanation.\n\n"
            f"- **Next Steps:** When `GEMINI_API_KEY` is configured in `.env`, SchemeSaathi automatically runs Gemini Vision to extract Marathi, Kannada, Hindi, Tamil, or English handwriting and typography into simple citizen-friendly summaries.\n"
            f"- **Immediate Guidance:** Please inspect the header of your document for the department name and stamp, and take it to your local Grama One or CSC center for physical verification."
        )

    return {
        "success": True,
        "filename": filename,
        "explanation": explanation,
        "language": language,
        "warning": warning_text,
        "model_used": "Offline Structural Parser (Configure GEMINI_API_KEY for Vision synthesis)"
    }
