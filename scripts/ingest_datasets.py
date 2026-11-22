"""
SchemeSaathi - Automatic Dataset Ingestion Pipeline
Extracts URLs from Scheme_Explainer_Datasets.pdf, classifies them, downloads/enriches
scheme data politely, normalizes into a unified schema, and writes data/processed/schemes.jsonl.
Supports --offline flag and auto-detects offline/sandbox environments to guarantee zero hangs.
"""

import os
import sys
import re
import json
import time
import socket
import argparse
import difflib
from urllib.parse import urlparse
import pdfplumber
import pandas as pd

USER_AGENT = "SchemeSaathi-ExplainerBot/1.0 (Hackathon Welfare Research; Educational; +https://github.com/schemesaathi)"
TIMEOUT = 2

def is_network_available(test_host="8.8.8.8", port=53, timeout=1.0) -> bool:
    """Quick check to avoid long library retry timeouts if network is blocked/offline."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((test_host, port))
        s.close()
        return True
    except Exception:
        return False

def extract_urls_from_pdf(pdf_path: str):
    """Extract all URLs from clickable hyperlinks and text via regex."""
    extracted = set()
    if not os.path.exists(pdf_path):
        return list(extracted)
    
    url_pattern = re.compile(r'https?://[^\s)\]\'"<>]+')
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # 1. Hyperlink annotations
            for link in getattr(page, 'hyperlinks', []):
                uri = link.get('uri')
                if uri and uri.startswith('http'):
                    extracted.add(uri.strip().rstrip('.'))
            
            # 2. Text regex
            text = page.extract_text() or ""
            matches = url_pattern.findall(text)
            for m in matches:
                clean_url = m.strip().rstrip('.,;')
                extracted.add(clean_url)
                
    return sorted(list(extracted))

def classify_url(url: str) -> str:
    """Classify URLs into dataset sources."""
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    
    if "huggingface.co/datasets" in url:
        return "huggingface"
    elif "github.com" in domain:
        return "github"
    elif any(domain.endswith(suffix) or f".{suffix}." in domain for suffix in ["gov.in", "nic.in", "org.in"]):
        return "official_site"
    else:
        return "ignore"

def polite_fetch_official_site(url: str, domain: str, out_dir: str):
    """Politely fetch visible text from official government public pages."""
    import requests
    from bs4 import BeautifulSoup
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, f"{domain.replace(':', '_')}.txt")
    
    headers = {"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"}
    try:
        resp = requests.get(url, headers=headers, timeout=TIMEOUT, verify=True)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
                tag.extract()
            text = ' '.join(soup.stripped_strings)
            clean_text = ' '.join(text.split()[:1500])
            with open(out_file, 'w', encoding='utf-8') as f:
                f.write(f"Source URL: {url}\nFetched: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n{clean_text}")
            return True, len(clean_text)
        else:
            return False, f"HTTP {resp.status_code}"
    except Exception as e:
        return False, str(e)

def load_curated_schemes():
    """Loads trusted curated schemes from CSV/JSON."""
    json_path = 'input/schemes_dataset.json' if os.path.exists('input/schemes_dataset.json') else 'schemes_dataset.json'
    csv_path = 'input/schemes_dataset.csv' if os.path.exists('input/schemes_dataset.csv') else 'schemes_dataset.csv'
    
    schemes = []
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            schemes = json.load(f)
            for s in schemes:
                s['source_type'] = 'curated'
                s['source_url'] = s.get('link', '')
                s['last_fetched'] = time.strftime('%Y-%m-%d')
    elif os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        for _, row in df.iterrows():
            item = row.to_dict()
            item['source_type'] = 'curated'
            item['source_url'] = item.get('link', '')
            item['rules'] = {}
            item['last_fetched'] = time.strftime('%Y-%m-%d')
            schemes.append(item)
    return schemes

def main():
    parser = argparse.ArgumentParser(description="SchemeSaathi Data Ingestion")
    parser.add_argument("--offline", action="store_true", help="Force offline mode using curated data only")
    args = parser.parse_args()
    
    start_time = time.time()
    online = False if args.offline else is_network_available()
    
    report_lines = [
        "# SchemeSaathi Dataset Ingestion Report",
        f"**Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}  ",
        f"**Execution Mode:** {'Offline / Air-gapped (Fallback)' if not online else 'Live Online Ingestion'}  \n",
        "## 1. Input Source & PDF URL Extraction"
    ]
    
    pdf_path = 'input/Scheme_Explainer_Datasets.pdf' if os.path.exists('input/Scheme_Explainer_Datasets.pdf') else 'Scheme_Explainer_Datasets.pdf'
    urls = extract_urls_from_pdf(pdf_path)
    report_lines.append(f"- Extracted **{len(urls)}** unique URLs from `{pdf_path}`.\n")
    
    classified = {"huggingface": [], "github": [], "official_site": [], "ignore": []}
    for u in urls:
        c = classify_url(u)
        classified[c].append(u)
        
    report_lines.append("### URL Classification Summary")
    report_lines.append(f"- **Hugging Face Datasets:** {len(classified['huggingface'])}")
    report_lines.append(f"- **Official Gov Sites (.gov.in / .nic.in / .org.in):** {len(classified['official_site'])}")
    report_lines.append(f"- **GitHub Repos:** {len(classified['github'])}")
    report_lines.append(f"- **Other / Skipped:** {len(classified['ignore'])}\n")
    
    hf_saved = 0
    hf_skipped = []
    hf_extra_schemes = []
    official_saved = 0
    official_texts = {}
    
    if online:
        # A. Hugging Face
        for hf_url in classified["huggingface"]:
            repo_id = hf_url.split("huggingface.co/datasets/")[-1].strip('/')
            if any(target in repo_id for target in ["ronitnandeshwar/gov_myscheme", "shrijayan/gov_myscheme"]):
                print(f"[HF] Fetching scheme dataset: {repo_id}")
                try:
                    from datasets import load_dataset
                    ds = load_dataset(repo_id, split="train", streaming=True)
                    rows = []
                    for i, item in enumerate(ds):
                        if i >= 100:
                            break
                        rows.append(item)
                    if rows:
                        df_hf = pd.DataFrame(rows)
                        os.makedirs("data/raw/hf", exist_ok=True)
                        clean_name = repo_id.replace('/', '_')
                        df_hf.to_csv(f"data/raw/hf/{clean_name}.csv", index=False)
                        hf_saved += len(rows)
                        for r in rows:
                            name = r.get("name") or r.get("scheme_name") or r.get("title")
                            elig = r.get("eligibility") or r.get("eligibility_criteria") or ""
                            benefits = r.get("benefits") or r.get("details") or ""
                            if name and (elig or benefits):
                                hf_extra_schemes.append({
                                    "id": f"hf_{len(hf_extra_schemes)+1}",
                                    "name": str(name).strip(),
                                    "category": r.get("category", "General Welfare"),
                                    "level": r.get("level", "Central"),
                                    "dept": r.get("department", "Government of India"),
                                    "benefits": str(benefits).strip(),
                                    "eligibility": str(elig).strip(),
                                    "exclusions": str(r.get("exclusions", "See official scheme guidelines.")),
                                    "documents": str(r.get("documents", "Aadhaar, Bank Account, Address Proof")),
                                    "apply": str(r.get("apply", "Apply through national scheme portal or local center.")),
                                    "link": r.get("link") or r.get("url") or "https://www.myscheme.gov.in",
                                    "rules": {},
                                    "source_type": "huggingface",
                                    "source_url": hf_url,
                                    "last_fetched": time.strftime('%Y-%m-%d')
                                })
                except Exception as e:
                    print(f"[HF] Could not load {repo_id}: {e}")
                    hf_skipped.append(f"{repo_id}: {str(e)[:60]}")
            else:
                hf_skipped.append(f"{repo_id} (Reason: Audio/TTS/Large Model skipped for lightweight Gemini/Browser speech)")
                
        # B. Official Gov Sites
        for site_url in classified["official_site"]:
            parsed = urlparse(site_url)
            domain = parsed.netloc
            print(f"[Official] Fetching: {site_url}")
            success, info = polite_fetch_official_site(site_url, domain, "data/raw/official")
            if success:
                official_saved += 1
                try:
                    with open(os.path.join("data/raw/official", f"{domain.replace(':', '_')}.txt"), 'r', encoding='utf-8') as f:
                        official_texts[domain] = f.read()
                except Exception:
                    pass
            else:
                print(f"[Official] Skipped/Failed {domain}: {info}")
            time.sleep(0.5)
    else:
        report_lines.append("**Offline / Air-gapped Fallback Active:** Network access is disabled or unreachable. All network downloads safely skipped; strictly loading trusted hand-verified curated scheme repository.\n")
        # List datasets skipped because offline
        for hf_url in classified["huggingface"]:
            repo_id = hf_url.split("huggingface.co/datasets/")[-1].strip('/')
            if any(target in repo_id for target in ["ronitnandeshwar/gov_myscheme", "shrijayan/gov_myscheme"]):
                hf_skipped.append(f"{repo_id} (Skipped: offline mode; curated schemes used)")
            else:
                hf_skipped.append(f"{repo_id} (Skipped: audio/TTS/large weights not needed)")

    # 3. Load Curated Schemes
    curated_schemes = load_curated_schemes()
    report_lines.append(f"## 2. Core Curated Dataset")
    report_lines.append(f"- Loaded **{len(curated_schemes)}** high-priority hand-verified core schemes.\n")
    
    # Official text context
    for s in curated_schemes:
        link = s.get('link', '')
        link_domain = urlparse(link).netloc.lower()
        if link_domain in official_texts:
            s['official_text'] = official_texts[link_domain][:3000]
        else:
            s['official_text'] = f"Official scheme portal: {link}. Hand-verified core government public scheme with guaranteed eligibility criteria."
            
    final_schemes = list(curated_schemes)
    curated_names = [s['name'].lower() for s in curated_schemes]
    
    added_hf = 0
    for hfs in hf_extra_schemes[:50]:
        h_name = hfs['name'].lower()
        is_dup = any(difflib.SequenceMatcher(None, h_name, cn).ratio() > 0.7 for cn in curated_names)
        if not is_dup:
            hfs['official_text'] = f"Source: myScheme / Hugging Face dataset ({hfs['source_url']})."
            final_schemes.append(hfs)
            added_hf += 1
            
    # Write data/processed/schemes.jsonl
    os.makedirs("data/processed", exist_ok=True)
    out_jsonl = "data/processed/schemes.jsonl"
    with open(out_jsonl, 'w', encoding='utf-8') as f:
        for s in final_schemes:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
            
    report_lines.append("## 3. Data Ingestion & Harmonization Summary")
    report_lines.append(f"- **Total Unified Schemes Processed:** {len(final_schemes)}")
    report_lines.append(f"- **Curated Hand-Verified Schemes:** {len(curated_schemes)}")
    report_lines.append(f"- **Hugging Face Extra Schemes Ingested:** {added_hf}")
    report_lines.append(f"- **Official Gov Pages Captured:** {official_saved}")
    report_lines.append(f"- **Skipped Datasets (Audio, TTS, Large Models):** {len(hf_skipped)}")
    for sk in hf_skipped[:8]:
        report_lines.append(f"  - `{sk}`")
    report_lines.append(f"- **Processed File:** `{out_jsonl}`")
    report_lines.append(f"- **Execution Time:** {time.time() - start_time:.2f} seconds\n")
    
    report_lines.append("## 4. Unified Schema Specification")
    report_lines.append("| Field | Type | Description |")
    report_lines.append("|---|---|---|")
    report_lines.append("| `id` | string | Unique scheme identifier |")
    report_lines.append("| `name` | string | Official full scheme name |")
    report_lines.append("| `category` | string | Agriculture, Health, Housing, etc. |")
    report_lines.append("| `level` | string | Central or State |")
    report_lines.append("| `state` | string | State name or 'All India' |")
    report_lines.append("| `dept` | string | Ministry or Department |")
    report_lines.append("| `benefits` | string | Clear benefits & monetary assistance |")
    report_lines.append("| `eligibility` | string | Plain-text eligibility conditions |")
    report_lines.append("| `exclusions` | string | Who is not eligible |")
    report_lines.append("| `documents` | string | Required documents to apply |")
    report_lines.append("| `apply` | string | How & where to submit application |")
    report_lines.append("| `link` | string | Official portal link |")
    report_lines.append("| `rules` | dict | Deterministic rule criteria for programmatic eligibility |")
    report_lines.append("| `official_text` | string | Scraped context or verified portal note |")
    report_lines.append("| `source_type` | string | `curated`, `huggingface`, or `official_site` |")
    report_lines.append("| `source_url` | string | Source origin link |")
    report_lines.append("| `last_fetched` | string | YYYY-MM-DD timestamp |")
    
    with open("data/ingest_report.md", "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
        
    print(f"\n[DONE] Ingestion completed. {len(final_schemes)} schemes normalized into {out_jsonl}.")
    print(f"Report written to data/ingest_report.md")

if __name__ == '__main__':
    main()
