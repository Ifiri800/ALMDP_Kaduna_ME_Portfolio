from pathlib import Path
from pypdf import PdfReader

pdf_path = (
    Path(__file__).resolve().parent.parent
    / "10_Reporting"
    / "ALMDP_Baseline_Assessment_Report_2026.pdf"
)

reader = PdfReader(str(pdf_path))

text = "".join(
    page.extract_text() or ""
    for page in reader.pages
)

print("PDF VALIDATION")
print("===============")
print(f"File exists: {pdf_path.exists()}")
print(f"File size: {pdf_path.stat().st_size:,} bytes")
print(f"Pages: {len(reader.pages)}")
print(f"Text characters: {len(text):,}")

checks = {
    "Contains ALMDP": "ALMDP" in text,
    "Contains Executive Summary": "Executive Summary" in text,
    "Contains Baseline Indicator Results": "Baseline Indicator Results" in text,
    "Contains Conclusions": "Baseline Conclusions and Recommendations" in text,
    "Contains Synthetic disclosure": "synthetic/simulated" in text.lower(),
}

for label, passed in checks.items():
    print(f"{label}: {'PASS' if passed else 'FAIL'}")

if not all(checks.values()):
    raise RuntimeError("One or more PDF content checks failed.")

print("PDF READ: PASS")
