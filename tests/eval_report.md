# SchemeSaathi - RAG Evaluation Report
**Date:** 2026-11-22 17:55:56  
**Accuracy Score:** 10/10 (100.0%)  

## Summary
Evaluated retrieval precision, fact preservation, and official citation matching against the 10 canonical benchmark questions derived from the official Scheme Dataset.

| ID | Test Question | Target Scheme | Result | Scheme Match | Facts Matched | Citation Valid |
|---|---|---|---|---|---|---|
| EVAL-01 | Am I eligible for PM-KISAN if I own 2 acres of cultivable land and am not an income tax payer? | `pm_kisan` | ✅ PASS | Yes | Yes | Yes |
| EVAL-02 | What is the annual health coverage under Ayushman Bharat PM-JAY? | `ab_pmjay` | ✅ PASS | Yes | Yes | Yes |
| EVAL-03 | Can a 12-year-old girl child open a new Sukanya Samriddhi Yojana account? | `ssy` | ✅ PASS | Yes | Yes | Yes |
| EVAL-04 | What documents are required to apply for Gruha Lakshmi in Karnataka? | `gruha_lakshmi` | ✅ PASS | Yes | Yes | Yes |
| EVAL-05 | What is the maximum loan limit under the Tarun category of PM Mudra Yojana? | `pm_mudra` | ✅ PASS | Yes | Yes | Yes |
| EVAL-06 | Can an income tax payer join Atal Pension Yojana (APY)? | `apy` | ✅ PASS | Yes | Yes | Yes |
| EVAL-07 | Who is eligible for free bus travel under the Shakti scheme in Karnataka? | `shakti` | ✅ PASS | Yes | Yes | Yes |
| EVAL-08 | What is the family income ceiling for the Post Matric Scholarship for SC Students? | `nsp_post_matric_sc` | ✅ PASS | Yes | Yes | Yes |
| EVAL-09 | How much financial assistance is provided under PMAY-G in plain areas? | `pmay_g` | ✅ PASS | Yes | Yes | Yes |
| EVAL-10 | What is the time limit for a public authority to reply to an RTI request? | `rti` | ✅ PASS | Yes | Yes | Yes |

## Detailed Sample Outputs

### [EVAL-01] Am I eligible for PM-KISAN if I own 2 acres of cultivable land and am not an income tax payer?
- **Target Scheme:** `pm_kisan`
- **Engine / Model:** Rule-based Grounded Synthesizer (GEMINI_API_KEY not configured)
- **Answer Snippet:** here is the verified information from official government records:  **scheme: ayushman bharat pm-jay** • **exclusions and non-eligibility**:...

### [EVAL-02] What is the annual health coverage under Ayushman Bharat PM-JAY?
- **Target Scheme:** `ab_pmjay`
- **Engine / Model:** Rule-based Grounded Synthesizer (GEMINI_API_KEY not configured)
- **Answer Snippet:** here is the verified information from official government records:  **scheme: ayushman bharat pm-jay** • **application process and how to ap...

### [EVAL-03] Can a 12-year-old girl child open a new Sukanya Samriddhi Yojana account?
- **Target Scheme:** `ssy`
- **Engine / Model:** Rule-based Grounded Synthesizer (GEMINI_API_KEY not configured)
- **Answer Snippet:** here is the verified information from official government records:  **scheme: sukanya samriddhi yojana (ssy)** • **benefits and financial as...

### [EVAL-04] What documents are required to apply for Gruha Lakshmi in Karnataka?
- **Target Scheme:** `gruha_lakshmi`
- **Engine / Model:** Rule-based Grounded Synthesizer (GEMINI_API_KEY not configured)
- **Answer Snippet:** here is the verified information from official government records:  **scheme: gruha lakshmi (karnataka)** • **required documents**: ration c...

### [EVAL-05] What is the maximum loan limit under the Tarun category of PM Mudra Yojana?
- **Target Scheme:** `pm_mudra`
- **Engine / Model:** Rule-based Grounded Synthesizer (GEMINI_API_KEY not configured)
- **Answer Snippet:** here is the verified information from official government records:  **scheme: pm mudra yojana (pmmy)** • **benefits and financial assistance...

### [EVAL-06] Can an income tax payer join Atal Pension Yojana (APY)?
- **Target Scheme:** `apy`
- **Engine / Model:** Rule-based Grounded Synthesizer (GEMINI_API_KEY not configured)
- **Answer Snippet:** here is the verified information from official government records:  **scheme: atal pension yojana (apy)** • **exclusions and non-eligibility...

### [EVAL-07] Who is eligible for free bus travel under the Shakti scheme in Karnataka?
- **Target Scheme:** `shakti`
- **Engine / Model:** Rule-based Grounded Synthesizer (GEMINI_API_KEY not configured)
- **Answer Snippet:** here is the verified information from official government records:  **scheme: shakti - free bus travel for women (karnataka)** • **eligibili...

### [EVAL-08] What is the family income ceiling for the Post Matric Scholarship for SC Students?
- **Target Scheme:** `nsp_post_matric_sc`
- **Engine / Model:** Rule-based Grounded Synthesizer (GEMINI_API_KEY not configured)
- **Answer Snippet:** here is the verified information from official government records:  **scheme: post matric scholarship for sc students (via national scholars...

### [EVAL-09] How much financial assistance is provided under PMAY-G in plain areas?
- **Target Scheme:** `pmay_g`
- **Engine / Model:** Rule-based Grounded Synthesizer (GEMINI_API_KEY not configured)
- **Answer Snippet:** here is the verified information from official government records:  **scheme: pm awaas yojana - gramin (pmay-g)** • **benefits and financial...

### [EVAL-10] What is the time limit for a public authority to reply to an RTI request?
- **Target Scheme:** `rti`
- **Engine / Model:** Rule-based Grounded Synthesizer (GEMINI_API_KEY not configured)
- **Answer Snippet:** here is the verified information from official government records:  **scheme: right to information act, 2005 (rti) - your right** • **benefi...
