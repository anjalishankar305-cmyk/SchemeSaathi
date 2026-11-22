# SchemeSaathi Dataset Ingestion Report
**Date:** 2026-11-22 17:42:05  
**Execution Mode:** Offline / Air-gapped (Fallback)  

## 1. Input Source & PDF URL Extraction
- Extracted **29** unique URLs from `input/Scheme_Explainer_Datasets.pdf`.

### URL Classification Summary
- **Hugging Face Datasets:** 14
- **Official Gov Sites (.gov.in / .nic.in / .org.in):** 8
- **GitHub Repos:** 1
- **Other / Skipped:** 6

**Offline / Air-gapped Fallback Active:** Network access is disabled or unreachable. All network downloads safely skipped; strictly loading trusted hand-verified curated scheme repository.

## 2. Core Curated Dataset
- Loaded **13** high-priority hand-verified core schemes.

## 3. Data Ingestion & Harmonization Summary
- **Total Unified Schemes Processed:** 13
- **Curated Hand-Verified Schemes:** 13
- **Hugging Face Extra Schemes Ingested:** 0
- **Official Gov Pages Captured:** 0
- **Skipped Datasets (Audio, TTS, Large Models):** 14
  - `ai4bharat/BP (Skipped: audio/TTS/large weights not needed)`
  - `ai4bharat/BPCC (Skipped: audio/TTS/large weights not needed)`
  - `ai4bharat/Indi (Skipped: audio/TTS/large weights not needed)`
  - `ai4bharat/IndicVoices (Skipped: audio/TTS/large weights not needed)`
  - `ai4bharat/MIL (Skipped: audio/TTS/large weights not needed)`
  - `ai4bharat/MILU (Skipped: audio/TTS/large weights not needed)`
  - `ai4bharat/Rur (Skipped: audio/TTS/large weights not needed)`
  - `ai4bharat/Rural_Women_ASR_v2 (Skipped: audio/TTS/large weights not needed)`
- **Processed File:** `data/processed/schemes.jsonl`
- **Execution Time:** 0.30 seconds

## 4. Unified Schema Specification
| Field | Type | Description |
|---|---|---|
| `id` | string | Unique scheme identifier |
| `name` | string | Official full scheme name |
| `category` | string | Agriculture, Health, Housing, etc. |
| `level` | string | Central or State |
| `state` | string | State name or 'All India' |
| `dept` | string | Ministry or Department |
| `benefits` | string | Clear benefits & monetary assistance |
| `eligibility` | string | Plain-text eligibility conditions |
| `exclusions` | string | Who is not eligible |
| `documents` | string | Required documents to apply |
| `apply` | string | How & where to submit application |
| `link` | string | Official portal link |
| `rules` | dict | Deterministic rule criteria for programmatic eligibility |
| `official_text` | string | Scraped context or verified portal note |
| `source_type` | string | `curated`, `huggingface`, or `official_site` |
| `source_url` | string | Source origin link |
| `last_fetched` | string | YYYY-MM-DD timestamp |