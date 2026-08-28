LegalMetro-Hackathon: Project Requirements

Problem Statement

Packaged commodities in India must comply with Legal Metrology (Packaged Commodities) Rules, 2011. Manual label verification is slow and error-prone for inspectors.

Target Users

- Primary: Legal Metrology field inspectors (govt. officials)
- Secondary: Retail QC teams, consumer groups, manufacturers

Core Features (MVP)

1. Image Input: Upload or camera capture (JPEG/PNG)
2. YOLOv8 Detection: Find MRP, quantity, manufacturer, date regions
3. OCR Extraction: Tesseract/EasyOCR on detected regions
4. Rule Validation: Check:
   - MRP format (must start with "₹" or "Rs.")
   - Quantity format (number + valid unit: g, kg, ml, l)
   - Manufacturer presence (non-empty)
   - Date format (MM/YY or DD/MM/YY)
5. Result Display: Pass/Fail with violations + annotated image
6. History Log: SQLite storage of past inspections

Success Criteria for Demo

- Scan 5+ real product labels
- Correctly validate MRP/quantity for ≥80% of samples
- Clear UI showing pass/fail with visual annotations

Architecture.md:
LegalMetro-Hackathon: Architecture

Data Flow

mermaid
graph LR
    A[Image Input] --> B[Preprocessing]
    B --> C[YOLOv8 Detection]
    C --> D[Region Cropping]
    D --> E[OCR Processing]
    E --> F[Rule Validation]
    F --> G[Result Presentation]
    F --> H[Storage]

Component Responsibilities

┌──────────────┬──────────────────────────────────────────┬─────────────────────────┐
│    Folder    │              Responsibility              │        Your Tech        │
├──────────────┼──────────────────────────────────────────┼─────────────────────────┤
│ detection/   │ Find label regions (MRP, quantity, etc.) │ YOLOv8 (you)            │
├──────────────┼──────────────────────────────────────────┼─────────────────────────┤
│ processing/  │ Extract text from regions                │ Tesseract/EasyOCR (TM2) │
├──────────────┼──────────────────────────────────────────┼─────────────────────────┤
│ validation/  │ Check text against rules                 │ Regex/pint (TM3)        │
├──────────────┼──────────────────────────────────────────┼─────────────────────────┤
│ ui/          │ Show results & history                   │ Streamlit (TM4)         │
├──────────────┼──────────────────────────────────────────┼─────────────────────────┤
│ storage/     │ Save inspection logs                     │ SQLite (TM5)            │
├──────────────┼──────────────────────────────────────────┼─────────────────────────┤
│ integration/ │ Orchestrate pipeline                     │ Pure Python (TM6)       │
└──────────────┴──────────────────────────────────────────┴─────────────────────────┘

Technical Stack

- Detection: Ultralytics YOLOv8 (nano model)
- OCR: Tesseract 5 + pytesseract OR easyocr
- UI: Streamlit (fastest for hackathon demo)
- Storage: SQLite (zero-config file DB)
- Validation: Python regex + pint for units

Rules.md:
LegalMetro-Hackathon: Development Rules

General Principles

1. Work in your folder only: Edit ONLY files in your assigned directory
2. Small commits: e.g., fix: MRP regex allows spaces
3. Pull before push: Always git pull origin main first
4. Test locally: Run relevant tests before pushing
5. Blocked >15 min?: Ping team in #hackathon channel

Language & Environment

- Python: 3.8+ (python --version)
- Deps: pip install -r requirements.txt
- VS Code: Use built-in terminal (Ctrl+`)
- Git: Never edit .git/ folder

Component-Specific Rules

Detection (detection/ - YOU)

- Use yolov8n.pt (nano) for speed
- Return format: [{"class": 0, "bbox": [x1,y1,x2,y2], "conf": 0.92}, ...]
- Never hardcode image paths - accept numpy array or file path

OCR (processing/ - TM2)

- Pipeline: Grayscale → CLAHE → Denoise → OCR
- Return: {"text": "₹ 199.00", "confidence": 0.87, "engine": "tesseract"}
- On failure: Return empty string + confidence 0.0

Validation (validation/ - TM3)

- Rules as JSON in validation/rules/:
{ "id": "mrp_format", "pattern": "₹\\s*\\d+(\\.\\d+)?", "severity": "critical" }
- Output: { "passed": bool, "violations": [{ "field": "mrp", "message": "..." }] }

UI (ui/ - TM4)

- Streamlit only (no React Native for hackathon)
- One primary action per screen (e.g., "Scan Label")
- Show st.spinner() during processing

Storage (storage/ - TM5)

- SQLite table: inspections (id, timestamp, image_name, result_json, passed)
- Never store raw images in DB - store filename only

Integration (integration/ - TM6)

- Orchestrate: detect → crop → OCR → validate → store → return
- CLI tool: python run_inspection.py path/to/image.jpg

Phases.md:
LegalMetro-Hackathon: Phased Plan

Phase 0: Foundation (0-2 hrs) - ALL

- Repo setup, .gitignore, requirements.txt
- Verify: git status works + all deps import
- Deliverable: Repo cloned, ready to code

Phase 1: Core Pipeline (2-6 hrs) - YOU + TM2 + TM6

- You: YOLOv8 detector + synthetic data generator
- TM2: OCR processor (grayscale + CLAHE + Tesseract)
- TM6: Integration script (main.py) linking detect→OCR
- Deliverable: CLI returns detections + OCR text

Phase 2: Validation & UI (6-12 hrs) - TM3 + TM4 + TM6

- TM3: Rule validator (MRP/quantity regex checks)
- TM4: Streamlit UI (upload → show boxes + results table)
- TM6: Add validation + storage to pipeline
- Deliverable: UI shows PASS/FAIL for MRP/quantity

Phase 3: Storage & History (12-18 hrs) - TM5 + TM4 + TM6

- TM5: SQLite DB (database.py with save/get functions)
- TM4: History tab in sidebar (recent inspections)
- TM6: Auto-save results after validation
- Deliverable: History tab shows past scans

Phase 4: Demo Prep (18-24 hrs) - TM6 + ALL

- TM6: Demo script + sample images (PASS/FAIL/edge cases)
- TM4: Final UI polish (logo, tooltips, mobile layout)
- ALL: Create 1-pager cheat sheet + rehearse demo
- Deliverable: Repeatable 2-minute demo

Stretch Goals (If Time)

- Add manufacturer/date validation
- Export reports as CSV
- Deploy as Android APK (Buildozer)

Design.md:
LegalMetro-Hackathon: Design

Color Palette (WCAG 2.1 AA Compliant)

┌──────────────┬──────────────────┬─────────┬────────────────────────┐
│    Usage     │      Color       │   Hex   │      When to Use       │
├──────────────┼──────────────────┼─────────┼────────────────────────┤
│ Primary      │ Metrology Blue   │ #1976D2 │ Buttons, active states │
├──────────────┼──────────────────┼─────────┼────────────────────────┤
│ Success      │ Compliance Green │ #388E3C │ PASS indicators        │
├──────────────┼──────────────────┼─────────┼────────────────────────┤
│ Error        │ Alert Amber      │ #F57C00 │ FAIL indicators        │
├──────────────┼──────────────────┼─────────┼────────────────────────┤
│ Background   │ Paper White      │ #FAFAFA │ Main canvas, cards     │
├──────────────┼──────────────────┼─────────┼────────────────────────┤
│ Text Primary │ Dark Charcoal    │ #212121 │ Body text, labels      │
└──────────────┴──────────────────┴─────────┴────────────────────────┘

Typography (Use Google Fonts)

- Headers: Roboto Slab (Bold, 24px)
- Body: Roboto (Regular, 16px)
- Monospace: Roboto Mono (14px for timestamps/JSON)
- Implement in Streamlit:
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&family=Roboto+Slab:wght@600&family=Roboto+Mono&display=swap');
.stApp { font-family: 'Roboto', sans-serif; }
h1, h2, h3 { font-family: 'Roboto Slab', serif; }
.code, pre { font-family: 'Roboto Mono', monospace; }
</style>
""", unsafe_allow_html=True)

Layout & Components

Scan Screen (Main)

+--------------------------------------------------+
| [Logo] LegalMetro-Hackathon                      |
|                                                  |
|  [📁 Upload]  [📷 Camera]                        |
|                                                  |
|  +------------------------------------------+    |
|  |   [ IMAGE PREVIEW WITH BOXES ]           |    |
|  +------------------------------------------+    |
|                                                  |
|  FIELD     | STATUS  | DETAILS                |
|  ----------|---------|--------------------------|
|  MRP       | ✅ PASS | ₹ 199.00                 |
|  Quantity  | ❌ FAIL | 500 (missing unit)       |
|  Manufacturer| ✅ PASS| ABC Foods Ltd            |
|  Date      | ⚠️ UNCERTAIN| 03/24 (low conf)     |
|                                                  |
|  [📊 History]  [🔄 Rescan]                        |
+--------------------------------------------------+

Key UX Rules

- PASS/FAIL: Always show icon + text + color (never color alone)
- Loading State: st.spinner("Analyzing label...") during processing
- Error Messages: Actionable (e.g., "Image too blurry - retake with better light")
- Accessibility:
  - Minimum 4.5:1 color contrast (use WebAIM checker (https://webaim.org/resources/contrastchecker/))
  - Touch targets ≥48x48dp
  - Alt text for all images (e.g., "Label showing MRP ₹199.00")