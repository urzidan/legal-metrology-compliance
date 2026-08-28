# LegalMetro-Hackathon: Architecture

## Data Flow
```mermaid
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