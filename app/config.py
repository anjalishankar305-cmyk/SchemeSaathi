import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
SCHEMES_FILE = BASE_DIR / "data" / "processed" / "schemes.jsonl"
INDEX_DIR = BASE_DIR / "data" / "index"
CHUNKS_FILE = INDEX_DIR / "chunks.json"
BM25_FILE = INDEX_DIR / "bm25_index.pkl"
EMBEDDINGS_FILE = INDEX_DIR / "embeddings.npy"

SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "हिन्दी (Hindi)",
    "kn": "ಕನ್ನಡ (Kannada)",
    "ta": "தமிழ் (Tamil)"
}

RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "120"))
