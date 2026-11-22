"""
SchemeSaathi - FastAPI Application Backend
Endpoints for Multilingual Policy Explanations, Rule-Based Eligibility,
Notice Clarification, Rate Limiting, and CORS.
"""

import os
import json
import time
from typing import Dict, Any, List, Optional
from collections import defaultdict
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .config import SCHEMES_FILE, GEMINI_API_KEY, RATE_LIMIT_PER_MINUTE
from .rag import rag_engine
from .eligibility import evaluate_scheme, find_eligible_schemes, SCHEME_METADATA
from .notice import explain_notice
from .i18n import SUPPORTED_LANGUAGES, SAMPLE_QUESTIONS

# In-memory sliding window rate limiter
request_history = defaultdict(list)

def rate_limiter(request: Request):
    client_ip = request.client.host if request.client else "127.0.0.1"
    now = time.time()
    cutoff = now - 60
    history = request_history[client_ip]
    request_history[client_ip] = [t for t in history if t > cutoff]
    if len(request_history[client_ip]) >= RATE_LIMIT_PER_MINUTE:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please wait a moment before sending more queries."
        )
    request_history[client_ip].append(now)

def load_schemes_data():
    if os.path.exists(SCHEMES_FILE):
        schemes = []
        with open(SCHEMES_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    schemes.append(json.loads(line))
        return schemes
    else:
        from scripts.ingest_datasets import load_curated_schemes
        return load_curated_schemes()

# Initialize immediately on module import
CACHED_SCHEMES = load_schemes_data()

@asynccontextmanager
async def lifespan(app: FastAPI):
    global CACHED_SCHEMES
    if not CACHED_SCHEMES:
        CACHED_SCHEMES = load_schemes_data()
    print(f"[Lifespan] SchemeSaathi active with {len(CACHED_SCHEMES)} schemes.")
    yield

app = FastAPI(
    title="SchemeSaathi API",
    description="Multilingual Policy, Rights & Scheme Explainer for Indian Citizens",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Request Models
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    language: str = Field(default="en")
    history: Optional[List[Dict[str, str]]] = Field(default_factory=list)

class EligibilitySingleRequest(BaseModel):
    scheme_id: str
    profile: Dict[str, Any]

class ProfileFindRequest(BaseModel):
    profile: Dict[str, Any]

# Endpoints
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "app": "SchemeSaathi",
        "version": "1.0.0",
        "schemes_loaded": len(CACHED_SCHEMES),
        "chunks_indexed": len(rag_engine.chunks),
        "gemini_api_key_configured": bool(os.getenv("GEMINI_API_KEY", "").strip() or GEMINI_API_KEY),
        "supported_languages": SUPPORTED_LANGUAGES,
        "sample_questions": SAMPLE_QUESTIONS
    }

@app.get("/api/schemes", dependencies=[Depends(rate_limiter)])
def get_all_schemes():
    return {
        "count": len(CACHED_SCHEMES),
        "schemes": [
            {
                "id": s.get("id"),
                "name": s.get("name"),
                "category": s.get("category"),
                "level": s.get("level"),
                "dept": s.get("dept"),
                "benefits": s.get("benefits"),
                "link": s.get("link")
            }
            for s in CACHED_SCHEMES
        ]
    }

@app.get("/api/schemes/{scheme_id}", dependencies=[Depends(rate_limiter)])
def get_scheme_by_id(scheme_id: str):
    for s in CACHED_SCHEMES:
        if s.get("id") == scheme_id:
            return s
    raise HTTPException(status_code=404, detail="Scheme not found")

@app.post("/api/chat", dependencies=[Depends(rate_limiter)])
def chat(payload: ChatRequest):
    result = rag_engine.generate_answer(
        message=payload.message,
        language=payload.language,
        history=payload.history
    )
    return result

@app.post("/api/eligibility", dependencies=[Depends(rate_limiter)])
def check_single_eligibility(payload: EligibilitySingleRequest):
    res = evaluate_scheme(payload.scheme_id, payload.profile)
    return res

@app.post("/api/eligibility/find", dependencies=[Depends(rate_limiter)])
def find_all_eligible(payload: ProfileFindRequest):
    results = find_eligible_schemes(payload.profile)
    return {
        "total_checked": len(results),
        "results": results
    }

@app.post("/api/explain-notice", dependencies=[Depends(rate_limiter)])
async def handle_explain_notice(
    file: UploadFile = File(...),
    language: str = Form("en")
):
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds 10MB limit.")
        
    result = explain_notice(
        file_bytes=content,
        filename=file.filename or "uploaded_notice",
        content_type=file.content_type or "application/octet-stream",
        language=language
    )
    return result

# Mount static frontend
static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
