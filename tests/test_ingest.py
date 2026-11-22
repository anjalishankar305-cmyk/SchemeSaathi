"""
SchemeSaathi - Ingestion Pipeline & URL Classifier Tests
"""

import os
import pytest
from scripts.ingest_datasets import (
    extract_urls_from_pdf,
    classify_url,
    load_curated_schemes
)

def test_extract_urls_from_pdf():
    pdf_path = "input/Scheme_Explainer_Datasets.pdf" if os.path.exists("input/Scheme_Explainer_Datasets.pdf") else "Scheme_Explainer_Datasets.pdf"
    assert os.path.exists(pdf_path), "PDF file should exist in workspace."
    urls = extract_urls_from_pdf(pdf_path)
    assert len(urls) > 5, "Should extract multiple URLs from Scheme_Explainer_Datasets.pdf."
    
    # Check key URLs extracted
    urls_str = " ".join(urls)
    assert "myscheme" in urls_str
    assert "huggingface.co" in urls_str

def test_classify_url():
    assert classify_url("https://huggingface.co/datasets/ronitnandeshwar/gov_myscheme") == "huggingface"
    assert classify_url("https://github.com/AI4Bharat/IndicTrans2") == "github"
    assert classify_url("https://pmkisan.gov.in") == "official_site"
    assert classify_url("https://sevasindhu.karnataka.gov.in") == "official_site"
    assert classify_url("https://scholarships.gov.in") == "official_site"
    assert classify_url("https://mudra.org.in") == "official_site"
    assert classify_url("https://random-blog.com/schemes") == "ignore"

def test_load_curated_schemes():
    schemes = load_curated_schemes()
    assert len(schemes) >= 12, "Curated scheme repository must have at least 12 schemes."
    
    required_fields = ["id", "name", "category", "level", "dept", "benefits", "eligibility", "documents", "apply", "link"]
    for s in schemes:
        for f in required_fields:
            assert f in s, f"Field '{f}' missing in scheme {s.get('id')}"
