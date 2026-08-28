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