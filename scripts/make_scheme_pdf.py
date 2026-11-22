import json
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_pdf():
    with open('schemes_dataset.json', 'r', encoding='utf-8') as f:
        schemes = json.load(f)

    c = canvas.Canvas('Scheme_Dataset.pdf', pagesize=letter)
    c.setFont('Helvetica-Bold', 16)
    c.drawString(50, 750, 'SchemeSaathi - Curated Scheme Dataset & Evaluation Questions')
    c.setFont('Helvetica', 10)
    c.drawString(50, 735, 'IDEA//FORGE Hackathon Track 1, Problem 1 - Trusted Core Data')

    y = 700
    c.setFont('Helvetica-Bold', 12)
    c.drawString(50, y, '1. Curated Government Schemes (Summary)')
    y -= 20
    c.setFont('Helvetica', 8)
    for s in schemes[:8]:
        c.drawString(50, y, f"[{s['id']}] {s['name']} ({s['category']}, {s['level']})")
        y -= 12
        desc = f"Benefits: {s['benefits'][:90]}..."
        c.drawString(60, y, desc)
        y -= 15

    c.showPage()
    c.setFont('Helvetica-Bold', 14)
    c.drawString(50, 750, '2. Sample Evaluation Questions (10 Core Test Cases)')
    y = 720
    sample_questions = [
        ('Q1: Am I eligible for PM-KISAN if I own 2 acres of cultivable land and am not an income tax payer?', 'Eligible. PM-KISAN provides Rs 6,000/yr for landholding farmer families who are not income tax payers.'),
        ('Q2: What is the annual health coverage under Ayushman Bharat PM-JAY?', 'Ayushman Bharat PM-JAY provides health cover up to Rs 5 lakh per family per year for secondary and tertiary hospitalization.'),
        ('Q3: Can a 12-year-old girl child open a new Sukanya Samriddhi Yojana account?', 'Not eligible. The girl child must be below 10 years of age at the time of opening.'),
        ('Q4: What documents are required to apply for Gruha Lakshmi in Karnataka?', 'Ration card (BPL/AAY/APL), Aadhaar card, Aadhaar-seeded bank account details, and mobile number.'),
        ('Q5: What is the maximum loan limit under the Tarun category of PM Mudra Yojana?', 'Under Tarun, loans are from Rs 5 lakh up to Rs 10 lakh (with Tarun Plus up to Rs 20 lakh for eligible borrowers).'),
        ('Q6: Can an income tax payer join Atal Pension Yojana (APY)?', 'No. Since October 2022, income tax payers are excluded from joining Atal Pension Yojana.'),
        ('Q7: Who is eligible for free bus travel under the Shakti scheme in Karnataka?', 'All women who are residents of Karnataka are eligible for free travel in ordinary state-run buses.'),
        ('Q8: What is the family income ceiling for the Post Matric Scholarship for SC Students?', 'The family income ceiling is Rs 2.5 lakh per annum.'),
        ('Q9: How much financial assistance is provided under PMAY-G in plain areas?', 'Rs 1.20 lakh in plain areas (and Rs 1.30 lakh in hilly/difficult areas).'),
        ('Q10: What is the time limit for a public authority to reply to an RTI request?', 'A reply is due within 30 days (or within 48 hours if life and liberty are involved).')
    ]

    for q, a in sample_questions:
        c.setFont('Helvetica-Bold', 9)
        c.drawString(50, y, q)
        y -= 12
        c.setFont('Helvetica', 8)
        c.drawString(60, y, 'Expected Answer: ' + a)
        y -= 22

    c.save()
    shutil.copy('Scheme_Dataset.pdf', 'input/Scheme_Dataset.pdf')
    print('Successfully generated Scheme_Dataset.pdf and copied to input/')

if __name__ == '__main__':
    create_pdf()
