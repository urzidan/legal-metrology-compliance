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

- Deliverable: Repeatable 2-minute demo

Stretch Goals (If Time)

- Add manufacturer/date validation
- Export reports as CSV
- Deploy as Android APK (Buildozer)