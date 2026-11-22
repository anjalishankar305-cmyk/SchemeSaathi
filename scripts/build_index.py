"""
SchemeSaathi - RAG Knowledge Base Indexer
Chunks scheme records by section, indexes them with BM25 (always-on, offline-ready),
and computes dense embeddings with Gemini if GEMINI_API_KEY is available.
"""

import os
import json
import pickle
import re
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

CHUNK_SECTIONS = [
    ("benefits", "Benefits and Financial Assistance"),
    ("eligibility", "Eligibility Criteria"),
    ("exclusions", "Exclusions and Non-Eligibility"),
    ("documents", "Required Documents"),
    ("apply", "Application Process and How to Apply"),
    ("official_text", "Official Scheme Overview")
]

def tokenize(text: str) -> List[str]:
    """Simple alphanumeric tokenizer suitable for multilingual/Indic text tokens."""
    return re.findall(r'\w+', text.lower())

def create_chunks_from_schemes(schemes_file: str) -> List[Dict[str, Any]]:
    chunks = []
    if not os.path.exists(schemes_file):
        raise FileNotFoundError(f"{schemes_file} does not exist.")
        
    with open(schemes_file, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            s = json.loads(line)
            s_id = s.get('id', 'unknown')
            s_name = s.get('name', 'Unknown Scheme')
            s_cat = s.get('category', 'General')
            s_level = s.get('level', 'Central')
            s_link = s.get('link', '')
            s_source = s.get('source_type', 'curated')
            
            for sec_key, sec_title in CHUNK_SECTIONS:
                content = s.get(sec_key, '')
                if not content or len(str(content).strip()) < 5:
                    continue
                    
                chunk_text = (
                    f"Scheme: {s_name} ({s_cat}, {s_level})\n"
                    f"Section: {sec_title}\n"
                    f"Details:\n{content}\n"
                    f"Official Link: {s_link}"
                )
                
                chunks.append({
                    "chunk_id": f"{s_id}_{sec_key}",
                    "scheme_id": s_id,
                    "scheme_name": s_name,
                    "category": s_cat,
                    "level": s_level,
                    "section": sec_key,
                    "section_title": sec_title,
                    "link": s_link,
                    "source_type": s_source,
                    "text": chunk_text
                })
    return chunks

def build_bm25_index(chunks: List[Dict[str, Any]], out_dir: str):
    from rank_bm25 import BM25Okapi
    tokenized_corpus = [tokenize(c["text"]) for c in chunks]
    bm25 = BM25Okapi(tokenized_corpus)
    
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "bm25_index.pkl"), "wb") as f:
        pickle.dump(bm25, f)
        
    with open(os.path.join(out_dir, "chunks.json"), "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
        
    print(f"[BM25] Built and saved BM25 index with {len(chunks)} chunks.")

def try_build_gemini_embeddings(chunks: List[Dict[str, Any]], out_dir: str):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[Embeddings] GEMINI_API_KEY not configured in environment. Skipping dense vector generation.")
        print("[Embeddings] App will seamlessly use BM25 keyword retrieval until API key is provided.")
        return
        
    print("[Embeddings] GEMINI_API_KEY found. Computing vector embeddings...")
    try:
        from google import genai
        import numpy as np
        
        client = genai.Client(api_key=api_key)
        embeddings = []
        batch_size = 10
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]
            texts = [c["text"] for c in batch]
            res = client.models.embed_content(
                model="text-embedding-004",
                contents=texts
            )
            for emb in res.embeddings:
                embeddings.append(emb.values)
                
        emb_arr = np.array(embeddings, dtype=np.float32)
        np.save(os.path.join(out_dir, "embeddings.npy"), emb_arr)
        print(f"[Embeddings] Computed and saved {len(embeddings)} dense embeddings to {out_dir}/embeddings.npy.")
    except Exception as e:
        print(f"[Embeddings] Could not compute Gemini embeddings ({e}). Falling back to BM25 index.")

def main():
    schemes_file = "data/processed/schemes.jsonl"
    out_dir = "data/index"
    
    if not os.path.exists(schemes_file):
        print(f"Error: {schemes_file} not found. Running ingestion first...")
        from ingest_datasets import main as run_ingest
        run_ingest()
        
    chunks = create_chunks_from_schemes(schemes_file)
    print(f"Extracted {len(chunks)} section chunks from processed schemes.")
    
    build_bm25_index(chunks, out_dir)
    try_build_gemini_embeddings(chunks, out_dir)
    print("[DONE] Knowledge Base indexing completed successfully.")

if __name__ == '__main__':
    main()
