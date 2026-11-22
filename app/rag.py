"""
SchemeSaathi - Retrieval Augmented Generation (RAG) Engine
Retrieves verified scheme chunks using BM25 / Vector search and generates simple,
grade-6 explanations in English, Hindi, Kannada, or Tamil with strict citations.
"""

import os
import json
import pickle
import re
from typing import List, Dict, Any, Tuple
from .config import CHUNKS_FILE, BM25_FILE, EMBEDDINGS_FILE, GEMINI_API_KEY
from .i18n import get_system_prompt, get_disclaimer, LANGUAGES

def tokenize(text: str) -> List[str]:
    return re.findall(r'\w+', text.lower())

class RAGEngine:
    def __init__(self):
        self.chunks = []
        self.bm25 = None
        self.embeddings = None
        self.load_index()

    def load_index(self):
        """Loads chunks and BM25 index into memory."""
        if os.path.exists(CHUNKS_FILE):
            with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
                self.chunks = json.load(f)
        else:
            self.chunks = []
            
        if os.path.exists(BM25_FILE):
            try:
                with open(BM25_FILE, "rb") as f:
                    self.bm25 = pickle.load(f)
            except Exception as e:
                print(f"[RAG] Error loading BM25 index: {e}")
                self.bm25 = None

        if os.path.exists(EMBEDDINGS_FILE):
            try:
                import numpy as np
                self.embeddings = np.load(EMBEDDINGS_FILE)
            except Exception as e:
                print(f"[RAG] Error loading vector embeddings: {e}")
                self.embeddings = None

    def retrieve(self, query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        """Retrieves top relevant chunks using BM25 with query expansion for scheme terms."""
        if not self.chunks:
            return []

        if not self.bm25:
            # Simple substring match fallback
            q_lower = query.lower()
            matched = [c for c in self.chunks if any(w in c["text"].lower() for w in tokenize(q_lower))]
            return matched[:top_k] or self.chunks[:top_k]

        tokens = tokenize(query)
        if not tokens:
            return self.chunks[:top_k]

        scores = self.bm25.get_scores(tokens)
        ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        
        top_chunks = []
        seen_schemes_sections = set()
        for idx in ranked_indices:
            c = self.chunks[idx]
            key = (c["scheme_id"], c["section"])
            if key not in seen_schemes_sections:
                seen_schemes_sections.add(key)
                top_chunks.append(c)
            if len(top_chunks) >= top_k:
                break
                
        return top_chunks

    def synthesize_fallback_offline_answer(self, query: str, chunks: List[Dict[str, Any]], lang: str) -> str:
        """Deterministic, grounded answer synthesizer when offline or GEMINI_API_KEY is not set."""
        if not chunks:
            if lang == "hi":
                return "माफ़ कीजिए, आपके सवाल से संबंधित जानकारी हमारे सत्यापित रिकॉर्ड में नहीं मिली। कृपया आधिकारिक सरकारी पोर्टल देखें।"
            elif lang == "kn":
                return "ಕ್ಷಮಿಸಿ, ನಿಮ್ಮ ಪ್ರಶ್ನೆಗೆ ಸಂಬಂಧಿಸಿದ ಮಾಹಿತಿ ನಮ್ಮ ಪರಿಶೀಲಿಸಿದ ದಾಖಲೆಗಳಲ್ಲಿ ಕಂಡುಬಂದಿಲ್ಲ. ದಯವಿಟ್ಟು ಅಧಿಕೃತ ಸರ್ಕಾರಿ ಪೋರ್ಟಲ್ ಪರಿಶೀಲಿಸಿ."
            elif lang == "ta":
                return "மன்னிக்கவும், உங்கள் கேள்வி தொடர்பான தகவல் எங்கள் சரிபார்க்கப்பட்ட பதிவுகளில் இல்லை. அதிகாரப்பூர்வ இணையதளத்தைப் பார்க்கவும்."
            else:
                return "Sorry, no relevant information was found in the verified welfare records. Please consult the official government portal."

        # Group by scheme
        schemes_info = {}
        for c in chunks:
            s_name = c["scheme_name"]
            if s_name not in schemes_info:
                schemes_info[s_name] = []
            schemes_info[s_name].append(c)

        lines = []
        if lang == "hi":
            lines.append("यहाँ आपके प्रश्न से संबंधित सत्यापित सरकारी जानकारी दी गई है:\n")
            for s_name, ch_list in schemes_info.items():
                lines.append(f"**योजना: {s_name}**")
                for ch in ch_list:
                    lines.append(f"• **{ch['section_title']}**: {ch['text'].split('Details:')[-1].split('Official Link:')[0].strip()}")
                lines.append("")
        elif lang == "kn":
            lines.append("ನಿಮ್ಮ ಪ್ರಶ್ನೆಗೆ ಸಂಬಂಧಿಸಿದ ಪರಿಶೀಲಿಸಿದ ಸರ್ಕಾರಿ ಮಾಹಿತಿ ಇಲ್ಲಿದೆ:\n")
            for s_name, ch_list in schemes_info.items():
                lines.append(f"**ಯೋಜನೆ: {s_name}**")
                for ch in ch_list:
                    lines.append(f"• **{ch['section_title']}**: {ch['text'].split('Details:')[-1].split('Official Link:')[0].strip()}")
                lines.append("")
        elif lang == "ta":
            lines.append("உங்கள் கேள்வி தொடர்பான சரிபார்க்கப்பட்ட அரசு விவரங்கள் இதோ:\n")
            for s_name, ch_list in schemes_info.items():
                lines.append(f"**திட்டம்: {s_name}**")
                for ch in ch_list:
                    lines.append(f"• **{ch['section_title']}**: {ch['text'].split('Details:')[-1].split('Official Link:')[0].strip()}")
                lines.append("")
        else:
            lines.append("Here is the verified information from official government records:\n")
            for s_name, ch_list in schemes_info.items():
                lines.append(f"**Scheme: {s_name}**")
                for ch in ch_list:
                    lines.append(f"• **{ch['section_title']}**: {ch['text'].split('Details:')[-1].split('Official Link:')[0].strip()}")
                lines.append("")

        return "\n".join(lines).strip()

    def generate_answer(self, message: str, language: str = "en", history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """Main chat generation method using RAG + Gemini with seamless offline fallback."""
        if language not in LANGUAGES:
            language = "en"

        chunks = self.retrieve(message, top_k=4)
        citations = []
        seen_cit = set()
        for c in chunks:
            cit_key = (c["scheme_name"], c["section_title"], c["link"])
            if cit_key not in seen_cit:
                seen_cit.add(cit_key)
                citations.append({
                    "scheme_name": c["scheme_name"],
                    "section": c["section_title"],
                    "link": c["link"]
                })

        context_text = "\n\n---\n\n".join([c["text"] for c in chunks])
        api_key = GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "").strip()

        if api_key:
            try:
                # Try google-genai
                from google import genai
                from google.genai import types

                client = genai.Client(api_key=api_key)
                sys_prompt = get_system_prompt(language)
                
                user_content = (
                    f"USER QUESTION: {message}\n\n"
                    f"TARGET LANGUAGE: {LANGUAGES[language]}\n\n"
                    f"VERIFIED CONTEXT FROM OFFICIAL GOVERNMENT SCHEMES:\n{context_text}\n\n"
                    f"Respond concisely in simple language (Grade-6 reading level) in {LANGUAGES[language]} strictly using the context above."
                )

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=user_content,
                    config=types.GenerateContentConfig(
                        system_instruction=sys_prompt,
                        temperature=0.2,
                        max_output_tokens=700
                    )
                )
                answer_text = response.text.strip()
                model_used = "Gemini 2.5 Flash"
            except Exception as e:
                # Try fallback model gemini-1.5-flash or google.generativeai
                try:
                    import google.generativeai as gai
                    gai.configure(api_key=api_key)
                    model = gai.GenerativeModel("gemini-1.5-flash", system_instruction=get_system_prompt(language))
                    res = model.generate_content(
                        f"USER QUESTION: {message}\n\nCONTEXT:\n{context_text}\n\nLanguage: {LANGUAGES[language]}"
                    )
                    answer_text = res.text.strip()
                    model_used = "Gemini 1.5 Flash"
                except Exception as e2:
                    print(f"[RAG] Gemini call failed ({e2}). Using deterministic offline synthesizer.")
                    answer_text = self.synthesize_fallback_offline_answer(message, chunks, language)
                    model_used = "Rule-based Grounded Synthesizer (Offline/Fallback)"
        else:
            answer_text = self.synthesize_fallback_offline_answer(message, chunks, language)
            model_used = "Rule-based Grounded Synthesizer (GEMINI_API_KEY not configured)"

        return {
            "answer": answer_text,
            "citations": citations,
            "language": language,
            "disclaimer": get_disclaimer(language),
            "model_used": model_used
        }

rag_engine = RAGEngine()
