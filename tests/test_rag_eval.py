"""
SchemeSaathi - RAG Evaluation Suite
Evaluates RAG retrieval and answer generation using the 10 sample benchmark questions.
Generates a comprehensive evaluation report in tests/eval_report.md.
"""

import os
import time
import pytest
from app.rag import rag_engine

EVAL_BENCHMARKS = [
    {
        "id": "EVAL-01",
        "question": "Am I eligible for PM-KISAN if I own 2 acres of cultivable land and am not an income tax payer?",
        "expected_scheme_id": "pm_kisan",
        "expected_keywords": ["6,000", "farmer", "land", "dbt"],
        "expected_link": "pmkisan.gov.in"
    },
    {
        "id": "EVAL-02",
        "question": "What is the annual health coverage under Ayushman Bharat PM-JAY?",
        "expected_scheme_id": "ab_pmjay",
        "expected_keywords": ["5 lakh", "hospital"],
        "expected_link": "pmjay.gov.in"
    },
    {
        "id": "EVAL-03",
        "question": "Can a 12-year-old girl child open a new Sukanya Samriddhi Yojana account?",
        "expected_scheme_id": "ssy",
        "expected_keywords": ["10", "girl"],
        "expected_link": "indiapost.gov.in"
    },
    {
        "id": "EVAL-04",
        "question": "What documents are required to apply for Gruha Lakshmi in Karnataka?",
        "expected_scheme_id": "gruha_lakshmi",
        "expected_keywords": ["ration card", "aadhaar", "bank"],
        "expected_link": "sevasindhu.karnataka.gov.in"
    },
    {
        "id": "EVAL-05",
        "question": "What is the maximum loan limit under the Tarun category of PM Mudra Yojana?",
        "expected_scheme_id": "pm_mudra",
        "expected_keywords": ["10 lakh", "tarun", "loan"],
        "expected_link": "mudra.org.in"
    },
    {
        "id": "EVAL-06",
        "question": "Can an income tax payer join Atal Pension Yojana (APY)?",
        "expected_scheme_id": "apy",
        "expected_keywords": ["income tax", "pension"],
        "expected_link": "jansuraksha.gov.in"
    },
    {
        "id": "EVAL-07",
        "question": "Who is eligible for free bus travel under the Shakti scheme in Karnataka?",
        "expected_scheme_id": "shakti",
        "expected_keywords": ["women", "karnataka", "bus"],
        "expected_link": "sevasindhu.karnataka.gov.in"
    },
    {
        "id": "EVAL-08",
        "question": "What is the family income ceiling for the Post Matric Scholarship for SC Students?",
        "expected_scheme_id": "nsp_post_matric_sc",
        "expected_keywords": ["2.5 lakh", "sc"],
        "expected_link": "scholarships.gov.in"
    },
    {
        "id": "EVAL-09",
        "question": "How much financial assistance is provided under PMAY-G in plain areas?",
        "expected_scheme_id": "pmay_g",
        "expected_keywords": ["1.20 lakh", "plain"],
        "expected_link": "pmayg.nic.in"
    },
    {
        "id": "EVAL-10",
        "question": "What is the time limit for a public authority to reply to an RTI request?",
        "expected_scheme_id": "rti",
        "expected_keywords": ["30 days", "information"],
        "expected_link": "rti.gov.in"
    }
]

def run_evaluation():
    results = []
    passed_count = 0

    for item in EVAL_BENCHMARKS:
        q = item["question"]
        expected_scheme = item["expected_scheme_id"]
        keywords = item["expected_keywords"]
        expected_link = item["expected_link"]

        # Run RAG answer generation
        res = rag_engine.generate_answer(q, language="en")
        answer = res["answer"].lower()
        citations = res.get("citations", [])
        
        # 1. Scheme match in citations or text
        retrieved_scheme_ids = [c["link"].lower() for c in citations]
        scheme_matched = any(expected_link in l for l in retrieved_scheme_ids) or expected_scheme in answer
        
        # 2. Key facts presence in answer
        facts_present = any(kw.lower() in answer for kw in keywords)

        # 3. Citation link present
        link_present = any(expected_link in c["link"].lower() for c in citations)

        passed = scheme_matched and (facts_present or link_present)
        if passed:
            passed_count += 1

        results.append({
            "id": item["id"],
            "question": q,
            "target_scheme": expected_scheme,
            "passed": passed,
            "scheme_matched": scheme_matched,
            "facts_present": facts_present,
            "link_present": link_present,
            "citations_count": len(citations),
            "model_used": res.get("model_used", "N/A"),
            "sample_snippet": answer[:140].replace("\n", " ") + "..."
        })

    return results, passed_count, len(EVAL_BENCHMARKS)

def test_rag_benchmark_suite():
    results, passed_count, total = run_evaluation()

    # Generate markdown report
    report_lines = [
        "# SchemeSaathi - RAG Evaluation Report",
        f"**Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}  ",
        f"**Accuracy Score:** {passed_count}/{total} ({(passed_count/total)*100:.1f}%)  \n",
        "## Summary",
        "Evaluated retrieval precision, fact preservation, and official citation matching against the 10 canonical benchmark questions derived from the official Scheme Dataset.\n",
        "| ID | Test Question | Target Scheme | Result | Scheme Match | Facts Matched | Citation Valid |",
        "|---|---|---|---|---|---|---|"
    ]

    for r in results:
        status_badge = "✅ PASS" if r["passed"] else "❌ FAIL"
        report_lines.append(
            f"| {r['id']} | {r['question']} | `{r['target_scheme']}` | {status_badge} | "
            f"{'Yes' if r['scheme_matched'] else 'No'} | {'Yes' if r['facts_present'] else 'No'} | {'Yes' if r['link_present'] else 'No'} |"
        )

    report_lines.append("\n## Detailed Sample Outputs\n")
    for r in results:
        report_lines.append(f"### [{r['id']}] {r['question']}")
        report_lines.append(f"- **Target Scheme:** `{r['target_scheme']}`")
        report_lines.append(f"- **Engine / Model:** {r['model_used']}")
        report_lines.append(f"- **Answer Snippet:** {r['sample_snippet']}")
        report_lines.append("")

    os.makedirs("tests", exist_ok=True)
    with open("tests/eval_report.md", "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(f"\n[EVAL] Passed {passed_count}/{total} benchmark tests. Report saved to tests/eval_report.md.")
    assert passed_count >= 9, f"Expected at least 9/10 passed, got {passed_count}/{total}"

if __name__ == "__main__":
    test_rag_benchmark_suite()
